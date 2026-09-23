"""全文抓取（尽力而为）：Europe PMC OA 全文 XML → 文本；arXiv PDF → 文本。缓存到 cache/。"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Callable

import requests

from .models import Candidate

EUPMC_FT = "https://www.ebi.ac.uk/europepmc/webservices/rest/{pmcid}/fullTextXML"
EUPMC_SEARCH = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
_TAG = re.compile(r"<[^>]+>")


def _get_text(url: str, timeout: int = 60) -> bytes:
    r = requests.get(url, timeout=timeout, headers={"User-Agent": "radar-background/0.1"})
    r.raise_for_status()
    return r.content


def resolve_pmcid(cand: Candidate, get: Callable = _get_text) -> str:
    """没有 pmcid 时按 DOI 反查 Europe PMC；只在 OA 时返回 pmcid，否则空。"""
    if cand.extra.get("pmcid"):
        return cand.extra["pmcid"]
    if not cand.id.startswith("doi:"):
        return ""
    import json
    from urllib.parse import urlencode
    q = urlencode({"query": f'DOI:"{cand.id[4:]}"', "format": "json", "pageSize": 1})
    try:
        d = json.loads(get(f"{EUPMC_SEARCH}?{q}").decode("utf-8", "ignore"))
        rows = d.get("resultList", {}).get("result", [])
        if rows and rows[0].get("pmcid") and rows[0].get("isOpenAccess") == "Y":
            cand.extra["pmcid"] = rows[0]["pmcid"]
            return rows[0]["pmcid"]
    except Exception as exc:
        print(f"[fetch] resolve pmcid {cand.id} failed: {exc}")
    return ""


def _cache_path(cache_dir: Path, cid: str) -> Path:
    return cache_dir / (re.sub(r"[^a-z0-9._-]+", "_", cid.lower())[:120] + ".txt")


def fetch_fulltext(cand: Candidate, cache_dir: Path, get: Callable = _get_text,
                   max_chars: int = 60000) -> str:
    """返回全文文本（可能为空）。有缓存直接读。"""
    cache_dir.mkdir(parents=True, exist_ok=True)
    p = _cache_path(cache_dir, cand.id)
    if p.exists():
        return p.read_text(encoding="utf-8")
    text = ""
    try:
        pmcid = resolve_pmcid(cand, get)
        if pmcid:
            xml = get(EUPMC_FT.format(pmcid=pmcid)).decode("utf-8", "ignore")
            body = re.search(r"<body>(.*)</body>", xml, re.DOTALL)
            text = _TAG.sub(" ", body.group(1) if body else "")
        elif cand.id.startswith("arxiv:"):
            from io import BytesIO
            from pypdf import PdfReader
            pdf = get(f"https://arxiv.org/pdf/{cand.id[6:]}")
            reader = PdfReader(BytesIO(pdf))
            text = "\n".join((pg.extract_text() or "") for pg in reader.pages[:40])
    except Exception as exc:
        print(f"[fetch] {cand.id} failed: {exc}")
        text = ""
    text = re.sub(r"\s+", " ", text).strip()[:max_chars]
    if text:
        p.write_text(text, encoding="utf-8")
    return text
