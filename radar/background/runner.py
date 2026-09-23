"""编排：bootstrap（N 轮）与 renew（增量）共用一条区块链。

run_round(spec, candidates_source) 是唯一的回合函数：
  bootstrap 每轮用 gap → discover 产生候选；
  renew 用 Inbox（radar 日报）产生候选，其余完全相同。"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

from . import extract as extract_mod
from . import metrics as metrics_mod
from .compile import compile_report
from .dedup import dedup
from .discover import Inbox, Source, default_sources, discover
from .fetch import fetch_fulltext
from .gap import plan_round
from .llmio import LLM
from .models import Candidate, DiscoveryPlan, Evidence, RoundLog
from .outline import Outline, revise
from .screen import screen
from .spec import TopicSpec
from .store import CorpusIndex, EvidenceStore


@dataclass
class RoundResult:
    log: RoundLog
    accepted: list[Evidence] = field(default_factory=list)
    plan: DiscoveryPlan | None = None
    report_path: Path | None = None


class Pipeline:
    def __init__(self, spec: TopicSpec, llm: LLM | None, sources: list[Source] | None = None,
                 index: CorpusIndex | None = None, fetch_text: bool = True, fetcher=fetch_fulltext):
        self.spec = spec
        self.llm = llm
        self.sources = sources if sources is not None else default_sources()
        self.store = EvidenceStore(spec.evidence_dir, spec.rejected_path, index)
        self.fetch_text = fetch_text
        self.fetcher = fetcher
        self.spec.dir.mkdir(parents=True, exist_ok=True)

    # ---- 状态文件 ----
    def load_outline(self) -> Outline:
        if self.spec.outline_path.exists():
            return Outline.from_markdown(self.spec.outline_path.read_text(encoding="utf-8"))
        return Outline.from_spec(self.spec)

    def save_outline(self, outline: Outline) -> None:
        self.spec.outline_path.write_text(outline.to_markdown(), encoding="utf-8")

    def round_no(self) -> int:
        if self.spec.metrics_path.exists():
            return len(json.loads(self.spec.metrics_path.read_text(encoding="utf-8")))
        return 0

    @property
    def cited_path(self) -> Path:
        return self.spec.dir / "seen_cited.json"

    def remember_citations(self, cands: list[Candidate]) -> list[str]:
        """累计所有见过的候选的引用数；高引覆盖率用稳定的累计 top-50，而不是本轮候选，
        否则指标会随每轮候选集波动（实跑第 7 轮出现过 0.727 → 0.713 的假回落）。"""
        seen = json.loads(self.cited_path.read_text(encoding="utf-8")) if self.cited_path.exists() else {}
        for c in cands:
            if c.citations is not None:
                seen[c.id] = max(int(c.citations), int(seen.get(c.id, 0)))
        self.cited_path.write_text(json.dumps(seen, ensure_ascii=False), encoding="utf-8")
        return [k for k, _ in sorted(seen.items(), key=lambda kv: -kv[1])[:50]]

    def compile_only(self, changelog: str = "") -> Path:
        outline = self.load_outline()
        cov = metrics_mod.coverage(self.spec, self.store, outline, self.top_cited(), self.round_no())
        report = compile_report(self.spec, outline, self.store.all(), self.llm, cov.score,
                                self.round_no(), changelog)
        self.spec.report_path.write_text(report, encoding="utf-8")
        return self.spec.report_path

    def top_cited(self) -> list[str] | None:
        if not self.cited_path.exists():
            return None
        seen = json.loads(self.cited_path.read_text(encoding="utf-8"))
        return [k for k, _ in sorted(seen.items(), key=lambda kv: -kv[1])[:50]] or None

    def last_log(self) -> str:
        return self.spec.log_path.read_text(encoding="utf-8") if self.spec.log_path.exists() else ""

    # ---- 核心回合 ----
    def run_round(self, candidates: list[Candidate], round_no: int, focus: str = "",
                  top_cited: list[str] | None = None, compile_now: bool = True) -> RoundResult:
        b = self.spec.budget
        new = dedup(candidates, self.store)[: b["max_screen"]]
        print(f"[round {round_no}] candidates {len(candidates)} → new {len(new)}")

        decisions = screen(new, self.spec, self.llm, round_no=round_no) if (self.llm and new) else []
        by_id = {c.id: c for c in new}
        accepted_c = [by_id[d.candidate_id] for d in decisions if d.accepted][: b["max_extract"]]
        n_rej = n_bord = 0
        for d in decisions:
            if not d.accepted:
                self.store.reject(by_id[d.candidate_id], d)
                n_rej += 1
                n_bord += int(d.borderline)

        fulltexts: dict[str, str] = {}
        if self.fetch_text:
            for c in accepted_c:
                t = self.fetcher(c, self.spec.cache_dir)
                if t:
                    fulltexts[c.id] = t
        extractions = extract_mod.extract(accepted_c, self.spec, self.llm, fulltexts) if accepted_c else []

        accepted: list[Evidence] = []
        for c, ex, d in zip(accepted_c, extractions, [d for d in decisions if d.accepted]):
            ev = Evidence(candidate=c, panel=d.votes, extraction=ex,
                          fulltext_path=(str(self.spec.cache_dir) if c.id in fulltexts else ""),
                          added_round=round_no, added_on=date.today().isoformat())
            self.store.add(ev, fulltexts.get(c.id, ""))
            accepted.append(ev)

        outline = self.load_outline()
        retry = [self.store.get(i) for i in outline.unsorted_ids()]
        retry = [e for e in retry if e and e.id not in {a.id for a in accepted}]
        outline, ops = revise(outline, accepted + retry, self.spec, self.llm)
        # 挂载信息回写证据记录
        for ev in accepted:
            ev.sections = [s.id for s in outline.walk() if ev.id in s.evidence_ids]
            self.store.update(ev)
        self.save_outline(outline)

        cov = metrics_mod.coverage(self.spec, self.store, outline, top_cited, round_no)
        hist = metrics_mod.append_metrics(self.spec.metrics_path, cov)
        log = RoundLog(round=round_no, focus=focus, n_candidates=len(candidates), n_new=len(new),
                       n_accepted=len(accepted), n_rejected=n_rej, n_borderline=n_bord,
                       coverage=cov.score, note=f"大纲操作 {len(ops)} 条")
        with self.spec.log_path.open("a", encoding="utf-8") as f:
            f.write(log.to_markdown())

        report_path = None
        if compile_now and self.llm is not None:
            changelog = "\n".join(f"- 新增 [{e.id}] {e.candidate.title}" for e in accepted) or "- 无新增"
            report = compile_report(self.spec, outline, self.store.all(), self.llm,
                                    cov.score, round_no, changelog)
            self.spec.report_path.write_text(report, encoding="utf-8")
            report_path = self.spec.report_path
        return RoundResult(log=log, accepted=accepted, report_path=report_path)

    def refetch(self, limit: int = 80) -> int:
        """给还没有全文的证据补全文并重新抽取（不改评审结果、不改大纲）。"""
        if self.llm is None:
            return 0
        todo = [e for e in self.store.all() if not e.fulltext_path][:limit]
        texts = {}
        for e in todo:
            t = self.fetcher(e.candidate, self.spec.cache_dir)
            if t:
                texts[e.id] = t
        got = [e for e in todo if e.id in texts]
        if not got:
            return 0
        exs = extract_mod.extract([e.candidate for e in got], self.spec, self.llm, texts)
        for e, ex in zip(got, exs):
            if ex.get("summary"):
                e.extraction = ex
            e.fulltext_path = str(self.spec.cache_dir)
            self.store.update(e)
        print(f"[refetch] fulltext for {len(got)}/{len(todo)}")
        return len(got)

    # ---- 两种入口 ----
    def bootstrap(self, rounds: int | None = None) -> list[RoundResult]:
        rounds = rounds or self.spec.budget["rounds"]
        results = []
        start = self.round_no() + 1
        for r in range(start, start + rounds):
            plan = plan_round(self.spec, self.store, self.load_outline(), r, self.llm, self.last_log())
            cands = discover(self.spec, plan, self.sources, self.spec.budget["max_candidates"])
            top = self.remember_citations(cands)
            res = self.run_round(cands, r, plan.focus, top, compile_now=(r == start + rounds - 1))
            res.plan = plan
            results.append(res)
            hist = json.loads(self.spec.metrics_path.read_text(encoding="utf-8"))
            if metrics_mod.should_stop(hist, self.spec.budget.get("stop_delta", 0.02)):
                print(f"[bootstrap] coverage plateau, stop at round {r}")
                if res.report_path is None and self.llm is not None:
                    res.report_path = self.compile_only("- 覆盖度平台期收尾编译")
                break
        return results

    def renew(self, inbox_path: Path, since_days: int = 7, min_score: float = 7.0) -> RoundResult:
        r = self.round_no() + 1
        cands = Inbox(inbox_path, since_days, min_score).fetch(self.spec, DiscoveryPlan())
        return self.run_round(cands, r, focus=f"renew：日报近 {since_days} 天",
                              top_cited=self.top_cited(), compile_now=True)
