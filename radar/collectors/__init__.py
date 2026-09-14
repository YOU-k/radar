from __future__ import annotations

import urllib.parse

import feedparser
import requests


def feed_parse(url: str):
    """拉 RSS/Atom。不用 feedparser.parse(url)：它不读代理环境变量，
    且跟进 301 时可能跳到 http:// 或相对路径。改为 requests 抓取
    （自动走 HTTPS_PROXY），重定向统一升级回 https。
    失败不抛异常（返回空 feed），保持"单 feed 失效不影响整体"的契约。"""
    try:
        for _ in range(4):
            r = requests.get(url, timeout=30, allow_redirects=False,
                             headers={"User-Agent": "bio-radar/0.1"})
            if r.is_redirect or r.is_permanent_redirect:
                url = urllib.parse.urljoin(url, r.headers["Location"])
                if url.startswith("http://"):
                    url = "https://" + url[7:]
                continue
            r.raise_for_status()
            return feedparser.parse(r.content)
    except Exception as exc:
        print(f"[feed] {url} fetch failed: {exc}")
    return feedparser.parse(b"")


from . import arxiv, europepmc, github, huggingface, rss, semantic_scholar  # noqa: E402

COLLECTORS = {
    "arxiv": arxiv,
    "europepmc": europepmc,
    "semantic_scholar": semantic_scholar,
    "huggingface": huggingface,
    "github": github,
    "rss": rss,
}
