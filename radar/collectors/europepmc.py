from __future__ import annotations

import re
import time
from datetime import date, timedelta

import requests

from ..schema import Item

API = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
_TAG = re.compile(r"<[^>]+>")
# 整刊订阅里剔除的文体：Nature 每天 5-8 条 Daily briefing / 新闻 / 社论，白占直通 LLM 的名额。
# Review 保留（CNS 综述由 LLM 按画像评估）。
_NOISE_PUBTYPES = {"news", "editorial", "comment", "published erratum",
                   "retraction of publication", "letter"}


def _is_noise(r: dict) -> bool:
    types = {str(t).lower() for t in (r.get("pubTypeList") or {}).get("pubType", [])}
    return bool(types & _NOISE_PUBTYPES)


def _search(query: str, start: str, end: str, page_size: int = 250,
            sort: str = "", date_field: str = "FIRST_PDATE") -> list[dict]:
    """date_field:
    - FIRST_PDATE：论文首次发表日期。适合回溯调研（deepdive）按"发表时间窗"取存量。
    - CREATION_DATE：记录进入 Europe PMC 的日期。每日增量采集必须用它——
      Nature/Science/Cell 正刊进 PubMed 索引普遍滞后 3-20 天，按发表日期取 1 天窗口
      几乎抓不到 CNS 新文（实测 1 天窗口 FIRST_PDATE 1 条 vs CREATION_DATE 17 条）。
    """
    q = f'({query}) AND (SRC:MED OR SRC:PPR) AND {date_field}:[{start} TO {end}]'
    params = {"query": q, "format": "json", "pageSize": page_size,
              "resultType": "core"}
    if sort:
        params["sort"] = sort
    r = requests.get(API, params=params, timeout=60)
    r.raise_for_status()
    return r.json().get("resultList", {}).get("result", [])


def _journal_query(journals: list[str]) -> str:
    """整刊订阅：不加关键词限制，新文全收，相关性交给 LLM 打分筛。"""
    return " OR ".join(f'JOURNAL:"{j}"' for j in journals)


def _to_item(r: dict, domain: str, journal_watch: bool = False) -> Item:
    src = r.get("source", "MED")
    uid = r.get("id", "")
    doi = (r.get("doi") or "").strip()
    url = f"https://doi.org/{doi}" if doi else f"https://europepmc.org/article/{src}/{uid}"
    journal = ((r.get("journalInfo") or {}).get("journal") or {}).get("title", "")
    return Item(
        id=(f"doi:{doi.lower()}" if doi else f"eupmc:{src}:{uid}"),
        source="europepmc", domain=domain,
        title=" ".join((r.get("title") or "").split()),
        url=url,
        authors=r.get("authorString", "") or "",
        abstract=_TAG.sub(" ", r.get("abstractText") or "").strip(),
        published=r.get("firstPublicationDate", "") or "",
        extra={"journal": journal or r.get("journalTitle", "") or "",
               "journal_watch": journal_watch,
               "pmcid": r.get("pmcid", "") or "",
               "is_oa": (r.get("isOpenAccess") == "Y")},
    )


def collect(cfg: dict, freqs: dict[str, int]) -> list[Item]:
    end = date.today()
    items = []
    for dom in cfg.get("domains", []):
        cadence = dom.get("europepmc_cadence", "daily")
        if cadence not in freqs:
            continue
        # 多回看 1 天：Actions 偶发排队/失败时不漏，重复条目由 dedup 吃掉
        start = (end - timedelta(days=freqs[cadence] + 1)).isoformat()
        queries = []
        keyword_query = (dom.get("europepmc_query") or "").strip()
        if keyword_query:
            queries.append((keyword_query, False))
        journals = dom.get("journals") or []
        if journals:
            queries.append((_journal_query(journals), True))
        for q, is_journal_watch in queries:
            try:
                rows = _search(q, start, end.isoformat(), date_field="CREATION_DATE")
            except Exception as exc:
                print(f"[europepmc] domain {dom['name']} failed: {exc}")
                continue
            for r in rows:
                if is_journal_watch and _is_noise(r):
                    continue
                it = _to_item(r, dom["name"], journal_watch=is_journal_watch)
                if it.title:
                    items.append(it)
            time.sleep(1)
    return items
