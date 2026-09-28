"""人工补录：按 id 取元数据 + 摘要，交给 Pipeline.add_manual 跳过评审直接入库。

取数顺序：Europe PMC（DOI；arXiv 走 10.48550 DOI；PMID）→ Semantic Scholar（有 S2_API_KEY 才查，
无 key 共享限速太容易 429）→ Crossref（DOI）/ arXiv API + DataCite（arXiv）。
先拿到标题的源定基本信息，摘要为空就继续往后补；各源给出的其他 id 记为 alt_ids。"""
from __future__ import annotations

import os
import re
from typing import Callable

from .discover import S2, S2_FIELDS, S2Snowball, _get_json
from .models import Candidate, normalize_id

EUPMC_SEARCH = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
CROSSREF = "https://api.crossref.org/works/"
DATACITE = "https://api.datacite.org/dois/"
ARXIV_API = "https://export.arxiv.org/api/query"
_TAG = re.compile(r"<[^>]+>")


def _clean(text: str) -> str:
    return " ".join(_TAG.sub(" ", text or "").split())


def _eupmc_query(eid: str) -> str:
    if eid.startswith("doi:"):
        return f'DOI:"{eid[4:]}"'
    if eid.startswith("arxiv:"):
        return f'DOI:"10.48550/arxiv.{eid[6:]}"'
    if eid.startswith("pmid:"):
        return f"EXT_ID:{eid[5:]} AND SRC:MED"
    return ""


def _retry_5xx(fn: Callable, tries: int = 3, wait: float = 5.0):
    """Europe PMC 偶发 502/503：退避重试；其他错误直接抛。"""
    import time
    for i in range(tries):
        try:
            return fn()
        except Exception as exc:
            code = getattr(getattr(exc, "response", None), "status_code", 0) or 0
            if code < 500 or i == tries - 1:
                raise
            time.sleep(wait * (i + 1))


def from_europepmc(eid: str, get_json: Callable) -> Candidate | None:
    q = _eupmc_query(eid)
    if not q:
        return None
    d = _retry_5xx(lambda: get_json(EUPMC_SEARCH, {"query": q, "format": "json", "resultType": "core",
                                                   "pageSize": 1}))
    rows = (d.get("resultList") or {}).get("result") or []
    if not rows or not rows[0].get("title"):
        return None
    r = rows[0]
    alts = {normalize_id(f"doi:{r['doi']}") if r.get("doi") else "",
            f"pmid:{r['pmid']}" if r.get("pmid") else ""}
    venue = ((r.get("journalInfo") or {}).get("journal") or {}).get("title", "")
    if not venue and r.get("source") == "PPR":  # 预印本：bioRxiv / arXiv 等
        venue = (r.get("bookOrReportDetails") or {}).get("publisher", "") or "preprint"
    year = int(r["pubYear"]) if str(r.get("pubYear", "")).isdigit() else None
    extra = {"alt_ids": sorted(a for a in alts if a)}
    if r.get("pmcid") and r.get("isOpenAccess") == "Y":
        extra["pmcid"] = r["pmcid"]
    return Candidate(id=eid, title=_clean(r["title"]).rstrip("."), url=_url(eid),
                     abstract=_clean(r.get("abstractText", "")), authors=r.get("authorString", "")[:300],
                     venue=venue or "", year=year, citations=r.get("citedByCount"),
                     found_by=["manual"], extra=extra)


def from_s2(eid: str, get_json: Callable) -> Candidate | None:
    if not os.environ.get("S2_API_KEY"):
        return None
    p = get_json(f"{S2}/paper/{S2Snowball._s2_id(eid)}", {"fields": S2_FIELDS})
    return S2Snowball(get_json)._to_cand(p, "manual")


def from_crossref(eid: str, get_json: Callable) -> Candidate | None:
    if not eid.startswith("doi:"):
        return None
    m = get_json(CROSSREF + eid[4:]).get("message") or {}
    title = ((m.get("title") or [""])[0]) or ""
    if not title:
        return None
    parts = ((m.get("issued") or {}).get("date-parts") or [[None]])[0]
    authors = ", ".join(f"{a.get('given', '')} {a.get('family', '')}".strip()
                        for a in (m.get("author") or [])[:8])
    venue = (m.get("container-title") or [""])[0]
    if not venue and m.get("type") == "posted-content":  # 预印本：Crossref 把服务器名放在 institution
        venue = ((m.get("institution") or [{}])[0].get("name", "")) or "preprint"
    return Candidate(id=eid, title=_clean(title), url=_url(eid), abstract=_clean(m.get("abstract", "")),
                     authors=authors, venue=venue or "", year=parts[0] if parts and parts[0] else None,
                     citations=m.get("is-referenced-by-count"), found_by=["manual"])


def from_arxiv(eid: str, get_json: Callable, get_text: Callable | None = None) -> Candidate | None:
    """arXiv API 在部分网络下 406，先试它，不通再走 DataCite（10.48550/arxiv.<id>）。"""
    if not eid.startswith("arxiv:"):
        return None
    aid = eid[6:]
    if get_text is not None:
        try:
            import feedparser
            feed = feedparser.parse(get_text(ARXIV_API, {"id_list": aid}))
            for e in feed.entries:
                if e.get("title") and "Error" not in e.get("title", ""):
                    year = (e.get("published") or "")[:4]
                    return Candidate(id=eid, title=" ".join(e["title"].split()), url=_url(eid),
                                     abstract=" ".join((e.get("summary") or "").split()),
                                     authors=", ".join(a.get("name", "") for a in e.get("authors", [])[:8]),
                                     venue="arXiv", year=int(year) if year.isdigit() else None,
                                     found_by=["manual"])
        except Exception as exc:
            print(f"[manual] arXiv API {eid} failed: {exc}")
    a = (get_json(DATACITE + f"10.48550/arxiv.{aid}").get("data") or {}).get("attributes") or {}
    titles = a.get("titles") or []
    if not titles:
        return None
    desc = next((x.get("description", "") for x in a.get("descriptions") or []
                 if x.get("descriptionType") == "Abstract"), "")
    return Candidate(id=eid, title=_clean(titles[0].get("title", "")), url=_url(eid), abstract=_clean(desc),
                     authors=", ".join(c.get("name", "") for c in (a.get("creators") or [])[:8]),
                     venue="arXiv", year=a.get("publicationYear"), found_by=["manual"])


def _url(eid: str) -> str:
    if eid.startswith("doi:"):
        return f"https://doi.org/{eid[4:]}"
    if eid.startswith("arxiv:"):
        return f"https://arxiv.org/abs/{eid[6:]}"
    if eid.startswith("pmid:"):
        return f"https://pubmed.ncbi.nlm.nih.gov/{eid[5:]}/"
    return ""


def _get_text(url: str, params: dict | None = None, timeout: int = 60) -> str:
    import requests
    r = requests.get(url, params=params, timeout=timeout, headers={"User-Agent": "radar-background/0.1"})
    r.raise_for_status()
    return r.text


def lookup(raw: str, get_json: Callable = _get_json, get_text: Callable | None = _get_text) -> Candidate | None:
    """id → Candidate（带摘要）。所有源都拿不到标题时返回 None。"""
    eid = normalize_id(raw)
    sources = [("europepmc", lambda: from_europepmc(eid, get_json)),
               ("s2", lambda: from_s2(eid, get_json)),
               ("crossref", lambda: from_crossref(eid, get_json)),
               ("arxiv", lambda: from_arxiv(eid, get_json, get_text))]
    base: Candidate | None = None
    alts: set[str] = set()
    for name, fn in sources:
        try:
            c = fn()
        except Exception as exc:
            print(f"[manual] {name} {eid} failed: {exc}")
            continue
        if c is None:
            continue
        alts |= {c.id, *(c.extra.get("alt_ids") or [])}
        if base is None:
            base = c
        else:  # 补空字段
            for f in ("abstract", "venue", "authors", "year", "citations"):
                if not getattr(base, f) and getattr(c, f):
                    setattr(base, f, getattr(c, f))
            if c.extra.get("pmcid") and not base.extra.get("pmcid"):
                base.extra["pmcid"] = c.extra["pmcid"]
        if base.abstract:
            break
    if base is None:
        return None
    base.id = eid
    base.found_by = ["manual"]
    alts = sorted(a for a in alts if a and a != eid)
    if alts:
        base.extra["alt_ids"] = alts
    else:
        base.extra.pop("alt_ids", None)
    return base
