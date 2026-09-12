from __future__ import annotations

import time
from datetime import date, timedelta

import requests

from ..schema import Item

API = "https://api.semanticscholar.org/graph/v1"
FIELDS = "title,abstract,year,url,externalIds,publicationDate,authors"


def _get(path: str, **params) -> dict:
    for attempt in (1, 2):
        try:
            r = requests.get(f"{API}{path}", params=params, timeout=60)
            if r.status_code == 429 and attempt == 1:
                time.sleep(10)
                continue
            r.raise_for_status()
            return r.json()
        except Exception:
            if attempt == 2:
                raise
            time.sleep(5)
    return {}


def _to_item(p: dict, kind: str, via: str) -> Item | None:
    if not p.get("title"):
        return None
    ext = p.get("externalIds") or {}
    doi = ext.get("DOI")
    pid = p.get("paperId", "")
    return Item(
        id=(f"doi:{doi.lower()}" if doi else f"s2:{pid}"),
        source="semantic_scholar", domain="tracked",
        title=p["title"],
        url=p.get("url") or f"https://www.semanticscholar.org/paper/{pid}",
        authors=", ".join(a.get("name", "") for a in (p.get("authors") or [])[:5]),
        abstract=p.get("abstract") or "",
        published=p.get("publicationDate") or "",
        extra={"via": f"{kind}:{via}"},
    )


def collect(cfg: dict, days: int) -> list[Item]:
    cutoff = (date.today() - timedelta(days=days)).isoformat()
    items = []

    for pid in cfg.get("seed_papers") or []:
        try:
            data = _get(f"/paper/{pid}/citations", fields=FIELDS, limit=100)
        except Exception as exc:
            print(f"[s2] citations for {pid} failed: {exc}")
            continue
        for row in data.get("data", []):
            p = row.get("citingPaper") or {}
            pub = p.get("publicationDate")
            if pub and pub < cutoff:
                continue
            it = _to_item(p, "citation_watch", str(pid))
            if it:
                items.append(it)
        time.sleep(2)

    for aid in cfg.get("tracked_authors") or []:
        try:
            data = _get(f"/author/{aid}/papers", fields=FIELDS, limit=50)
        except Exception as exc:
            print(f"[s2] author {aid} failed: {exc}")
            continue
        for p in data.get("data", []):
            pub = p.get("publicationDate")
            if pub and pub < cutoff:
                continue
            it = _to_item(p, "author_watch", str(aid))
            if it:
                items.append(it)
        time.sleep(2)

    return items
