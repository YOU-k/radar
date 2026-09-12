from __future__ import annotations

import os
import time
from datetime import date, timedelta

import requests

from ..schema import Item

API = "https://api.github.com/search/repositories"


def collect(cfg: dict, days: int) -> list[Item]:
    since = (date.today() - timedelta(days=days)).isoformat()
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "bio-radar/0.1"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    items = []
    for dom in cfg.get("domains", []):
        for q in dom.get("github_queries") or []:
            try:
                r = requests.get(API, headers=headers, params={
                    "q": f"{q} created:>{since}",
                    "sort": "stars", "order": "desc", "per_page": 10,
                }, timeout=30)
                r.raise_for_status()
                rows = r.json().get("items", [])
            except Exception as exc:
                print(f"[github] {q!r} failed: {exc}")
                continue
            for repo in rows:
                items.append(Item(
                    id=f"gh:{repo['full_name']}", source="github",
                    domain=dom["name"],
                    title=repo["full_name"], url=repo["html_url"],
                    authors=(repo.get("owner") or {}).get("login", ""),
                    abstract=repo.get("description") or "",
                    published=(repo.get("created_at") or "")[:10],
                    extra={"stars": repo.get("stargazers_count", 0),
                           "language": repo.get("language") or ""},
                ))
            time.sleep(3 if not token else 1)  # 未认证搜索限 10 req/min
    return items
