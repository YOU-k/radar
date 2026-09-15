from __future__ import annotations

import re
import time
from datetime import date, timedelta

import requests

from ..schema import Item

API = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
_TAG = re.compile(r"<[^>]+>")


def _search(query: str, start: str, end: str, page_size: int = 250) -> list[dict]:
    q = f'({query}) AND (SRC:MED OR SRC:PPR) AND FIRST_PDATE:[{start} TO {end}]'
    r = requests.get(API, params={
        "query": q, "format": "json", "pageSize": page_size,
        "resultType": "core",
    }, timeout=60)
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
               "journal_watch": journal_watch},
    )


def collect(cfg: dict, freqs: dict[str, int]) -> list[Item]:
    end = date.today()
    items = []
    for dom in cfg.get("domains", []):
        cadence = dom.get("europepmc_cadence", "daily")
        if cadence not in freqs:
            continue
        start = (end - timedelta(days=freqs[cadence])).isoformat()
        queries = []
        keyword_query = (dom.get("europepmc_query") or "").strip()
        if keyword_query:
            queries.append((keyword_query, False))
        journals = dom.get("journals") or []
        if journals:
            queries.append((_journal_query(journals), True))
        for q, is_journal_watch in queries:
            try:
                rows = _search(q, start, end.isoformat())
            except Exception as exc:
                print(f"[europepmc] domain {dom['name']} failed: {exc}")
                continue
            for r in rows:
                it = _to_item(r, dom["name"], journal_watch=is_journal_watch)
                if it.title:
                    items.append(it)
            time.sleep(1)
    return items
