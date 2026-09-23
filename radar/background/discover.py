"""发现层：Source 插件 → Candidate。网络 I/O 只经 _get_json，测试可整体替换。

内置源：
  EuropePMCKeyword   关键词 × 发表日窗口，按引用排序
  EuropePMCJournal   整刊回溯（CNS 等），标题/摘要含关键词才收（CNS 什么都发）
  ArxivKeyword       arXiv API
  S2Snowball         Semantic Scholar 引用滚雪球：种子的 references + citations
  Inbox              radar 日报的抽取记录（renew 用），不走网络
"""
from __future__ import annotations

import json
import time
from datetime import date, timedelta
from pathlib import Path
from typing import Callable, Protocol

import requests

from ..collectors.europepmc import _search as eupmc_search, _to_item as eupmc_item
from .models import Candidate, DiscoveryPlan, normalize_id
from .spec import TopicSpec

S2 = "https://api.semanticscholar.org/graph/v1"
S2_FIELDS = "title,abstract,year,venue,citationCount,externalIds,authors"


def _get_json(url: str, params: dict | None = None, timeout: int = 60) -> dict:
    r = requests.get(url, params=params, timeout=timeout,
                     headers={"User-Agent": "radar-background/0.1"})
    r.raise_for_status()
    return r.json()


class Source(Protocol):
    name: str
    def fetch(self, spec: TopicSpec, plan: DiscoveryPlan) -> list[Candidate]: ...


def _search_retry(search: Callable, *args, retries: int = 2, wait: float = 3.0, **kw) -> list[dict]:
    """Europe PMC 被限流时返回 200 + 空结果（实测同一查询连发第二次得 0 条）；空结果等一下重试。"""
    for attempt in range(retries + 1):
        rows = search(*args, **kw)
        if rows or attempt == retries:
            return rows
        time.sleep(wait * (attempt + 1))
    return []


def _window(months: int) -> tuple[str, str]:
    end = date.today()
    return (end - timedelta(days=months * 30)).isoformat(), end.isoformat()


def _mentions(text: str, keywords: list[str]) -> bool:
    t = text.lower()
    return any(k.lower() in t for k in keywords) if keywords else True


class EuropePMCKeyword:
    name = "eupmc"

    def __init__(self, search: Callable = eupmc_search, per_query: int = 60):
        self.search, self.per_query = search, per_query

    def fetch(self, spec: TopicSpec, plan: DiscoveryPlan) -> list[Candidate]:
        start, end = _window(plan.months)
        out = []
        for q in plan.queries:
            try:
                rows = _search_retry(self.search, q, start, end, page_size=self.per_query, sort="CITED desc")
            except Exception as exc:
                print(f"[discover:eupmc] {q!r} failed: {exc}")
                continue
            for r in rows:
                it = eupmc_item(r, spec.slug)
                if it.title:
                    c = Candidate.from_item(it, f"eupmc:{q[:30]}")
                    c.citations = r.get("citedByCount")
                    out.append(c)
            time.sleep(1)
        return out


class EuropePMCJournal:
    name = "journal"

    def __init__(self, search: Callable = eupmc_search, page_size: int = 250):
        self.search, self.page_size = search, page_size

    def fetch(self, spec: TopicSpec, plan: DiscoveryPlan) -> list[Candidate]:
        if not plan.journals:
            return []
        start, end = _window(plan.months)
        q = " OR ".join(f'JOURNAL:"{j}"' for j in plan.journals)
        out = []
        # 关键词写进查询：整刊 24 个月量太大，不能拉回来再筛
        kw = " OR ".join(f'"{k}"' if " " in k else k for k in spec.keywords[:25])
        full_q = f"({q}) AND ({kw})" if kw else q
        try:
            rows = _search_retry(self.search, full_q, start, end, page_size=self.page_size, sort="CITED desc")
        except Exception as exc:
            print(f"[discover:journal] failed: {exc}")
            return []
        for r in rows:
            it = eupmc_item(r, spec.slug, journal_watch=True)
            if it.title and _mentions(it.title + " " + it.abstract, spec.keywords):
                c = Candidate.from_item(it, "journal-retro")
                c.citations = r.get("citedByCount")
                out.append(c)
        return out


class ArxivKeyword:
    name = "arxiv"

    def __init__(self, collect: Callable | None = None):
        if collect is None:
            from ..pipeline.deepdive import _collect_arxiv
            collect = _collect_arxiv
        self.collect = collect

    def fetch(self, spec: TopicSpec, plan: DiscoveryPlan) -> list[Candidate]:
        if not plan.queries:
            return []
        start, end = _window(plan.months)
        try:
            items = self.collect(plan.queries, start, end)
        except Exception as exc:
            print(f"[discover:arxiv] failed: {exc}")
            return []
        return [Candidate.from_item(it, "arxiv") for it in items if it.title]


class S2Snowball:
    name = "s2"

    def __init__(self, get_json: Callable = _get_json, per_seed: int = 40, sleep: float = 1.1):
        self.get_json, self.per_seed, self.sleep = get_json, per_seed, sleep

    @staticmethod
    def _s2_id(eid: str) -> str:
        if eid.startswith("doi:"):
            return "DOI:" + eid[4:]
        if eid.startswith("arxiv:"):
            return "ARXIV:" + eid[6:]
        if eid.startswith("pmid:"):
            return "PMID:" + eid[5:]
        return eid

    def _to_cand(self, p: dict, tag: str) -> Candidate | None:
        ext = p.get("externalIds") or {}
        raw = (f"doi:{ext['DOI']}" if ext.get("DOI") else
               f"arxiv:{ext['ArXiv']}" if ext.get("ArXiv") else
               f"pmid:{ext['PubMed']}" if ext.get("PubMed") else "")
        if not raw or not p.get("title"):
            return None
        eid = normalize_id(raw)
        url = (f"https://doi.org/{ext['DOI']}" if ext.get("DOI") else
               f"https://arxiv.org/abs/{ext['ArXiv']}" if ext.get("ArXiv") else "")
        return Candidate(id=eid, title=p["title"], url=url, abstract=p.get("abstract") or "",
                         authors=", ".join(a.get("name", "") for a in (p.get("authors") or [])[:8]),
                         venue=p.get("venue") or "", year=p.get("year"),
                         citations=p.get("citationCount"), found_by=[tag])

    def fetch(self, spec: TopicSpec, plan: DiscoveryPlan) -> list[Candidate]:
        out = []
        for seed in plan.snowball_ids:
            if seed in spec.seeds:  # 种子本身也是候选（必收文献先进证据库）
                try:
                    c = self._to_cand(self.get_json(f"{S2}/paper/{self._s2_id(seed)}",
                                                    {"fields": S2_FIELDS}), "seed")
                    if c:
                        out.append(c)
                except Exception as exc:
                    print(f"[discover:s2] seed {seed} failed: {exc}")
                time.sleep(self.sleep)
            for rel, key in (("references", "citedPaper"), ("citations", "citingPaper")):
                try:
                    d = self.get_json(f"{S2}/paper/{self._s2_id(seed)}/{rel}",
                                      {"fields": S2_FIELDS, "limit": self.per_seed})
                except Exception as exc:
                    print(f"[discover:s2] {seed} {rel} failed: {exc}")
                    continue
                for row in d.get("data", []):
                    c = self._to_cand(row.get(key) or {}, f"s2:{rel}:{seed}")
                    if c:
                        out.append(c)
                time.sleep(self.sleep)
        return out


class Inbox:
    """renew 的输入：radar data/extractions.jsonl 里 domain 匹配、≥ min_score 的条目。"""
    name = "inbox"

    def __init__(self, path: Path, since_days: int = 7, min_score: float = 7.0):
        self.path, self.since_days, self.min_score = Path(path), since_days, min_score

    def fetch(self, spec: TopicSpec, plan: DiscoveryPlan) -> list[Candidate]:
        if not self.path.exists() or not spec.radar_domain:
            return []
        cutoff = date.today().toordinal() - self.since_days
        out = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            try:
                r = json.loads(line)
                if (r.get("domain") != spec.radar_domain or float(r.get("score", 0)) < self.min_score
                        or date.fromisoformat(r["date"]).toordinal() <= cutoff):
                    continue
            except (json.JSONDecodeError, KeyError, ValueError):
                continue
            out.append(Candidate(id=normalize_id(r.get("url", ""), r.get("url", "")),
                                 title=r.get("title", ""), url=r.get("url", ""),
                                 abstract=r.get("summary", ""), venue=r.get("journal", ""),
                                 found_by=["inbox"], extra={"radar_score": r.get("score")}))
        return out


def default_sources() -> list[Source]:
    return [EuropePMCKeyword(), EuropePMCJournal(), ArxivKeyword(), S2Snowball()]


def relevance(c: Candidate, spec: TopicSpec) -> tuple:
    """排序键：种子最先 → 关键词命中（标题 ×2 + 摘要）→ log 引用 → 来源数。
    纯引用排序会让种子参考文献里的通用方法（Transformer、UMAP）挤占预算。"""
    import math
    title, abstract = c.title.lower(), (c.abstract or "").lower()
    hits = sum((2 if k.lower() in title else 0) + (1 if k.lower() in abstract else 0)
               for k in spec.keywords)
    is_seed = c.id in spec.seeds or "seed" in c.found_by
    return (-int(is_seed), -hits, -math.log1p(c.citations or 0), -len(c.found_by))


def discover(spec: TopicSpec, plan: DiscoveryPlan, sources: list[Source],
             max_candidates: int = 80) -> list[Candidate]:
    """跑所有源，按相关性排序后截到预算。单源失败不影响整体。"""
    cands: list[Candidate] = []
    for s in sources:
        try:
            got = s.fetch(spec, plan)
        except Exception as exc:
            print(f"[discover:{getattr(s, 'name', '?')}] crashed: {exc}")
            continue
        print(f"[discover:{getattr(s, 'name', '?')}] {len(got)}")
        cands.extend(got)
    from .dedup import merge_duplicates
    merged = merge_duplicates(cands)
    merged.sort(key=lambda c: relevance(c, spec))
    return merged[:max_candidates]
