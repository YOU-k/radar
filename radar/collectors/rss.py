from __future__ import annotations

import re
import socket
import time
from datetime import date, timedelta

import feedparser

from ..schema import Item

socket.setdefaulttimeout(30)  # 防止个别 feed 挂死整个 job

_TAG = re.compile(r"<[^>]+>")


def _clean(html: str, n: int = 1200) -> str:
    return " ".join(_TAG.sub(" ", html or "").split())[:n]


def collect(cfg: dict, freqs: dict[str, int]) -> list[Item]:
    items = []
    for dom in cfg.get("domains", []):
        for entry in dom.get("rss") or []:
            # 允许 "url" 或 {url, cadence} 两种写法
            if isinstance(entry, dict):
                url = entry["url"]
                cadence = entry.get("cadence", "daily")
            else:
                url, cadence = entry, "daily"
            if cadence not in freqs:
                continue
            cutoff = (date.today() - timedelta(days=freqs[cadence])).isoformat()
            feed = feedparser.parse(url)
            if feed.bozo and not feed.entries:
                print(f"[rss] {url} returned no entries")
                continue
            feed_title = getattr(feed.feed, "title", url) if hasattr(feed, "feed") else url
            for e in feed.entries:
                pub = ""
                for attr in ("published_parsed", "updated_parsed"):
                    t = getattr(e, attr, None)
                    if t:
                        pub = date(*t[:3]).isoformat()
                        break
                if pub and pub < cutoff:
                    continue
                link = getattr(e, "link", "") or url
                items.append(Item(
                    id=f"rss:{link.lower().rstrip('/')}", source="rss",
                    domain=dom["name"],
                    title=" ".join((getattr(e, "title", "") or "").split()),
                    url=link,
                    authors=getattr(e, "author", "") or "",
                    abstract=_clean(getattr(e, "summary", "") or ""),
                    published=pub,
                    extra={"feed": feed_title},
                ))
            time.sleep(0.5)
    return items
