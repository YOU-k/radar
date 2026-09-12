from __future__ import annotations

import time
from datetime import datetime, timedelta, timezone

import requests

from ..schema import Item

API = "https://huggingface.co/api"


def _search(kind: str, query: str, cutoff: datetime, limit: int = 10) -> list[dict]:
    r = requests.get(f"{API}/{kind}", params={
        "search": query, "sort": "lastModified", "direction": -1, "limit": limit,
    }, timeout=30)
    r.raise_for_status()
    out = []
    for m in r.json():
        lm = m.get("lastModified") or ""
        try:
            dt = datetime.fromisoformat(lm.replace("Z", "+00:00"))
        except ValueError:
            continue
        if dt >= cutoff:
            out.append(m)
    return out


def collect(cfg: dict, days: int) -> list[Item]:
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    items = []
    for dom in cfg.get("domains", []):
        for q in dom.get("hf_queries") or []:
            for kind in ("models", "datasets"):
                try:
                    rows = _search(kind, q, cutoff)
                except Exception as exc:
                    print(f"[hf] {kind} {q!r} failed: {exc}")
                    continue
                for m in rows:
                    mid = m.get("id", "")
                    if not mid:
                        continue
                    url = (f"https://huggingface.co/{mid}" if kind == "models"
                           else f"https://huggingface.co/datasets/{mid}")
                    desc = m.get("description")
                    items.append(Item(
                        id=f"hf:{kind}:{mid}", source="huggingface",
                        domain=dom["name"],
                        title=f"[{kind[:-1]}] {mid}", url=url,
                        authors=m.get("author", "") or "",
                        abstract=(desc if isinstance(desc, str) and desc else
                                  ", ".join((m.get("tags") or [])[:8])),
                        published=(m.get("lastModified") or "")[:10],
                        extra={"likes": m.get("likes", 0),
                               "downloads": m.get("downloads", 0)},
                    ))
                time.sleep(0.5)
    return items
