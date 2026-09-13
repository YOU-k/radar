from __future__ import annotations

import re
import time
from datetime import date, timedelta

import requests

from ..schema import Item

API = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
_TAG = re.compile(r"<[^>]+>")


def _search(query: str, start: str, end: str, page_size: int = 50) -> list[dict]:
    q = f'({query}) AND (SRC:MED OR SRC:PPR) AND FIRST_PDATE:[{start} TO {end}]'
    r = requests.get(API, params={
        "query": q, "format": "json", "pageSize": page_size,
        "resultType": "core",
    }, timeout=60)
    r.raise_for_status()
    return r.json().get("resultList", {}).get("result", [])


def collect(cfg: dict, freqs: dict[str, int]) -> list[Item]:
    end = date.today()
    items = []
    for dom in cfg.get("domains", []):
        query = (dom.get("europepmc_query") or "").strip()
        cadence = dom.get("europepmc_cadence", "daily")
        if not query or cadence not in freqs:
            continue
        start = end - timedelta(days=freqs[cadence])
        try:
            rows = _search(query, start.isoformat(), end.isoformat())
        except Exception as exc:
            print(f"[europepmc] domain {dom['name']} failed: {exc}")
            continue
        for r in rows:
            src = r.get("source", "MED")
            uid = r.get("id", "")
            doi = (r.get("doi") or "").strip()
            url = f"https://doi.org/{doi}" if doi else f"https://europepmc.org/article/{src}/{uid}"
            items.append(Item(
                id=(f"doi:{doi.lower()}" if doi else f"eupmc:{src}:{uid}"),
                source="europepmc", domain=dom["name"],
                title=" ".join((r.get("title") or "").split()),
                url=url,
                authors=r.get("authorString", "") or "",
                abstract=_TAG.sub(" ", r.get("abstractText") or "").strip(),
                published=r.get("firstPublicationDate", "") or "",
                extra={"journal": r.get("journalTitle", "") or ""},
            ))
        time.sleep(1)
    return items
