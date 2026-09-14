from __future__ import annotations

import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date, timedelta

from ..schema import Item

API = "https://export.arxiv.org/api/query"
NS = {"a": "http://www.w3.org/2005/Atom"}


def _search(queries: list[str], categories: list[str], max_results: int = 50) -> list[dict]:
    """一个领域的所有 query 合并成一次 OR 请求。

    arXiv API 响应慢（30-120s 常见），逐 query 请求既慢又容易触发限流；
    合并后每领域一次请求，重复条目交给下游 dedup。
    """
    q = " OR ".join(f'all:"{query}"' for query in queries)
    if len(queries) > 1:
        q = f"({q})"
    if categories:
        q += " AND (" + " OR ".join(f"cat:{c}" for c in categories) + ")"
    params = urllib.parse.urlencode({
        "search_query": q,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    })
    url = f"{API}?{params}"
    last_exc: Exception | None = None
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "bio-radar/0.1"})
            with urllib.request.urlopen(req, timeout=150) as r:
                root = ET.fromstring(r.read())
            break
        except urllib.error.HTTPError as exc:
            last_exc = exc
            if exc.code == 429:  # 限流：共享出口 IP 常见，长退避
                time.sleep(30 * (attempt + 1))
            else:
                time.sleep(5 * (attempt + 1))
        except Exception as exc:  # 网络抖动常见，重试两次
            last_exc = exc
            time.sleep(10 * (attempt + 1))
    else:
        raise last_exc  # type: ignore[misc]
    out = []
    for e in root.findall("a:entry", NS):
        out.append({
            "id": (e.findtext("a:id", "", NS) or "").strip(),
            "title": " ".join((e.findtext("a:title", "", NS) or "").split()),
            "abstract": " ".join((e.findtext("a:summary", "", NS) or "").split()),
            "authors": ", ".join(
                (a.findtext("a:name", "", NS) or "")
                for a in e.findall("a:author", NS)[:5]),
            "published": (e.findtext("a:published", "", NS) or "")[:10],
        })
    return out


def collect(cfg: dict, freqs: dict[str, int]) -> list[Item]:
    items = []
    for dom in cfg.get("domains", []):
        spec = dom.get("arxiv") or {}
        cadence = spec.get("cadence", "daily")
        if cadence not in freqs:
            continue
        cutoff = (date.today() - timedelta(days=freqs[cadence])).isoformat()
        queries = spec.get("queries") or []
        cats = spec.get("categories") or []
        if not queries:
            continue
        try:
            rows = _search(queries, cats)
        except Exception as exc:
            print(f"[arxiv] domain {dom['name']} failed: {exc}")
            continue
        for r in rows:
            if not r["id"] or (r["published"] and r["published"] < cutoff):
                continue
            items.append(Item(
                id=r["id"], source="arxiv", domain=dom["name"],
                title=r["title"], url=r["id"], authors=r["authors"],
                abstract=r["abstract"], published=r["published"],
            ))
        time.sleep(3)  # arxiv 要求请求间隔
    return items
