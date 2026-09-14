from __future__ import annotations

import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date, timedelta

from . import feed_parse
from ..schema import Item

API = "https://export.arxiv.org/api/query"
RSS = "https://arxiv.org/rss/"
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
    for attempt in range(2):  # Actions IP 基本必被 429，快速转 RSS 兜底
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "bio-radar/0.1"})
            with urllib.request.urlopen(req, timeout=150) as r:
                root = ET.fromstring(r.read())
            break
        except urllib.error.HTTPError as exc:
            last_exc = exc
            if exc.code == 429:  # 限流：共享出口 IP 常见，长退避
                time.sleep(30)
            else:
                time.sleep(5 * (attempt + 1))
        except Exception as exc:  # 网络抖动常见，重试一次
            last_exc = exc
            time.sleep(10)
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


_TAG = re.compile(r"<[^>]+>")


def _rss_fallback(categories: list[str], queries: list[str]) -> list[dict]:
    """export.arxiv.org 对数据中心 IP（GitHub Actions）长期 429。

    退路：主站分类 RSS（CDN 前置，一般不墙）拉当日新 listing，
    再用本领域的 query 词在标题+摘要里过滤，语义接近 query 检索。
    """
    kws = [q.lower() for q in queries]
    rows = []
    for cat in categories:
        try:
            feed = feed_parse(f"{RSS}{cat}")
        except Exception as exc:
            print(f"[arxiv-rss] {cat} failed: {exc}")
            continue
        if not feed.entries:
            print(f"[arxiv-rss] {cat} returned no entries")
            continue
        for e in feed.entries:
            title = " ".join((getattr(e, "title", "") or "").split())
            abstract = " ".join(_TAG.sub(" ", getattr(e, "summary", "") or "").split())
            haystack = f"{title} {abstract}".lower()
            if kws and not any(k in haystack for k in kws):
                continue
            link = getattr(e, "link", "") or ""
            if not link:
                continue
            rows.append({
                "id": link,
                "title": title,
                "abstract": abstract,
                "authors": getattr(e, "author", "") or "",
                "published": "",  # RSS 即当日 listing，发布日期由调用方窗口隐含
            })
        time.sleep(3)
    print(f"[arxiv-rss] fallback collected {len(rows)} rows")
    return rows


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
            print(f"[arxiv] domain {dom['name']} API failed: {exc}; trying RSS fallback")
            rows = _rss_fallback(cats, queries)
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
