"""结构化抽取：字段与 radar/pipeline/extract.py 兼容并扩展 results / limitations。

输入永远带摘要；有全文时再加 Results 节（找不到节标题就挑数字密、引用少的段落），
不再用全文前 6000 字——那一段主要是引言和方法，满是引用别人研究的数字。
抽取后逐个数字回摘要 + 全文核对（grounding.audit_extraction）：
- 只出现在引用标记旁（本文引用的别人的结果）→ 删掉所在分句；
- 摘要和全文里都找不到 → 保留但记入 extraction["_unverified_numbers"]，编译时这些数字不算有据。"""
from __future__ import annotations

import json
import re

from . import grounding
from .llmio import LLM, parse_json_array, tagged
from .models import Candidate, Evidence
from .spec import TopicSpec

KEYS = ("method", "data", "scenario", "benchmark", "results", "availability",
        "limitations", "summary")
BATCH = 8
ABSTRACT_CHARS = 2000
RESULTS_CHARS = 6000

_RESULTS_HEAD = re.compile(r"(?:^|\s)(?:\d+\.?\s*)?(?:Results(?: and Discussion)?|RESULTS|Experiments?|EXPERIMENTS)"
                           r"\s+(?=[A-Z0-9])")
_DISCUSSION_HEAD = re.compile(r"\s(?:\d+\.?\s*)?(?:Discussion|DISCUSSION|Conclusions?|CONCLUSIONS?|Methods|METHODS)\s+(?=[A-Z])")


def empty() -> dict:
    return {k: "" for k in KEYS}


def results_slice(fulltext: str, limit: int = RESULTS_CHARS) -> str:
    """全文里本文自己的结果段：优先 Results/Experiments 节；否则按「数字密度 − 引用标记」挑块。"""
    ft = fulltext or ""
    if len(ft) <= limit:
        return ft
    heads = [m.end() for m in _RESULTS_HEAD.finditer(ft) if m.start() > len(ft) * 0.05]
    if heads:
        start = heads[0]
        end = _DISCUSSION_HEAD.search(ft, start + 500)
        stop = min(end.start(), start + limit) if end else start + limit
        return ft[start:stop]
    chunk = 1500
    blocks = [(i, ft[i:i + chunk]) for i in range(0, len(ft), chunk)]
    def score(b: str) -> float:
        return len(grounding.numbers(b)) - 3 * len(grounding.CITE_MARK.findall(b))
    best = sorted(blocks, key=lambda x: -score(x[1]))[:max(1, limit // chunk)]
    return " … ".join(b for _, b in sorted(best))


def ground(ex: dict, abstract: str, fulltext: str = "") -> dict:
    """数字回原文：删引用他人数字的分句，记下原文里找不到的数字。原地修改并返回。"""
    issues = grounding.audit_extraction(ex, abstract, fulltext)
    cited = {}
    for it in issues:
        if it["reason"] == "cited":
            cited.setdefault(it["field"], set()).add(it["number"])
    for f, nums in cited.items():
        ex[f] = grounding.drop_clauses(ex.get(f, ""), nums)
    ex["_unverified_numbers"] = [{**it, "dropped": it["reason"] == "cited"} for it in issues]
    ex["_basis"] = "abstract+results" if fulltext else "abstract"
    return ex


def _row(i: int, c: Candidate, ft: str) -> dict:
    row = {"id": i, "title": c.title, "venue": c.venue, "year": c.year,
           "abstract": (c.abstract or "")[:ABSTRACT_CHARS]}
    if ft:
        row["results_text"] = results_slice(ft)
    return row


def extract(cands: list[Candidate], spec: TopicSpec, llm: LLM,
            fulltexts: dict[str, str] | None = None) -> list[dict]:
    fulltexts = fulltexts or {}
    out = [empty() for _ in cands]
    for b in range(0, len(cands), BATCH):
        chunk = cands[b:b + BATCH]
        rows = [_row(i, c, fulltexts.get(c.id, "")) for i, c in enumerate(chunk)]
        prompt = tagged("extract", (
            f"这些文献都属于方向「{spec.name}」。请对每篇输出结构化字段（中文，具体、保留数字）：\n"
            "method（≤20字）、data（本文实际分析的数据类型与样本规模 ≤30字）、scenario（≤15字）、"
            "benchmark（基准或对比对象 ≤30字）、results（本文的关键定量结果 ≤60字）、"
            "availability（代码/权重/数据是否公开，≤20字；文中没提留空）、"
            "limitations（作者承认或明显的局限 ≤40字）、summary（3 句：做了什么、怎么做、发现什么）。\n"
            "只抽取本文自身的结果；引用他人研究的数字不得写入（正文里紧挨 [12]、et al. 这类引用标记的数字多半是别人的）。"
            "data 写本文实际纳入分析的人数/样本数，不要写队列或数据库的总规模；数字照原文写，不要换算或估算。"
            "abstract 是摘要，results_text（如有）是全文的结果部分；两者冲突时以摘要为准。\n\n"
            "【文献】\n" + json.dumps(rows, ensure_ascii=False) +
            '\n\n只输出 JSON 数组：[{"id":0,"method":"...",...,"summary":"..."}]'))
        try:
            parsed = parse_json_array(llm.chat(prompt, task="extract"))
        except Exception as exc:
            print(f"[extract] batch {b // BATCH} failed: {exc}")
            parsed = []
        for r in parsed:
            try:
                i = int(r.get("id", -1))
            except (TypeError, ValueError):
                continue
            if 0 <= i < len(chunk):
                for k in KEYS:
                    out[b + i][k] = str(r.get(k, "")).strip()[:300]
    for c, ex in zip(cands, out):
        if ex.get("summary"):
            ground(ex, c.abstract or "", fulltexts.get(c.id, ""))
    return out


# ---- 重抽取：python -m radar.run background reextract --topic <slug|all> [--only-flagged] ----

def needs_reextract(ev: Evidence, fulltext: str = "") -> bool:
    """旧抽取里有摘要/全文都找不到、或只出现在引用旁的数字。"""
    return bool(grounding.audit_extraction(ev.extraction, ev.candidate.abstract or "", fulltext))


def cached_fulltext(spec: TopicSpec, eid: str) -> str:
    """只读本地全文缓存，不联网（CI 上没有缓存时退回仅摘要）。"""
    from .fetch import _cache_path
    p = _cache_path(spec.cache_dir, eid)
    return p.read_text(encoding="utf-8") if p.exists() else ""


def reextract(spec: TopicSpec, store, llm: LLM, only_flagged: bool = True,
              fulltext_of=None) -> dict:
    """重跑证据抽取并写回证据 JSON（评审、挂载节点不动）。不编译报告——编译是单独一步。
    返回 {"checked", "todo", "updated", "still_flagged"}。"""
    fulltext_of = fulltext_of or (lambda eid: cached_fulltext(spec, eid))
    evs = store.all()
    texts = {e.id: fulltext_of(e.id) for e in evs}
    todo = [e for e in evs if not only_flagged or needs_reextract(e, texts[e.id])]
    updated = still = 0
    for b in range(0, len(todo), BATCH):
        chunk = todo[b:b + BATCH]
        exs = extract([e.candidate for e in chunk], spec, llm, {e.id: texts[e.id] for e in chunk if texts[e.id]})
        for e, ex in zip(chunk, exs):
            if not ex.get("summary"):  # LLM 失败：保留旧抽取
                continue
            e.extraction = ex
            store.update(e)
            updated += 1
            still += any(not x.get("dropped") for x in ex.get("_unverified_numbers", []))
    res = {"checked": len(evs), "todo": len(todo), "updated": updated, "still_flagged": still}
    print(f"[reextract] {spec.slug}: " + json.dumps(res))
    return res
