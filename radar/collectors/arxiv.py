"""arXiv 采集：OAI-PMH 为主，分类 RSS 兜底。

为什么不用 export.arxiv.org/api/query：2026-09-20 起对未缓存的检索一律 HTTP 406
（CI 和本机都复现，源站拒绝，与 User-Agent 无关）。

主通道 OAI-PMH（https://oaipmh.arxiv.org/oai，metadataPrefix=arXivRaw）：
- 按分类 set + from=<cutoff> 拉"该日期后有变动"的全部记录，按日期可回补：
  漏跑一天，下次窗口仍能取到，不像 RSS 只有当天 listing、周末为空。
- datestamp 包括旧论文的新版本（replacement）。arXivRaw 带完整版本历史，
  用 v1 日期判断"是不是新论文"：v1 早于 cutoff - SLACK_DAYS 的视为旧文替换，丢掉。
  SLACK 用来容纳"提交 → 公告"的滞后（周四提交、周一公告常见）。
- 同一分类在一次运行里只拉一次（cs.LG 被多个领域共用），再按领域 query 词在标题+摘要里筛。

兜底 RSS（rss.arxiv.org）：只收 announce_type=new/cross，用 pubDate 作发布日期并套 cutoff。

id 统一：arxiv:NNNN.NNNNN（去版本号），url 统一 https://arxiv.org/abs/NNNN.NNNNN，
与 background/models.normalize_id 口径一致。
"""
from __future__ import annotations

import re
import time
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta
from email.utils import parsedate_to_datetime
from typing import Callable

import requests

from . import feed_parse
from ..schema import Item

OAI = "https://oaipmh.arxiv.org/oai"
RSS = "https://rss.arxiv.org/rss/"
OAI_NS = {"o": "http://www.openarchives.org/OAI/2.0/", "r": "http://arxiv.org/OAI/arXivRaw/"}
UA = "bio-radar/0.2 (+https://github.com/YOU-k/radar)"
SLACK_DAYS = 7
MAX_PAGES = 15  # 每个分类最多翻页数（arXiv 每页约 1000 条，足够覆盖几天）

_NEW_ID = re.compile(r"(\d{4}\.\d{4,5})(?:v\d+)?")
_OLD_ID = re.compile(r"([a-z][a-z\-]*(?:\.[A-Z]{2})?/\d{7})(?:v\d+)?")
_TOP_GROUPS = {"cs", "math", "q-bio", "q-fin", "stat", "eess", "econ"}
_TAG = re.compile(r"<[^>]+>")


def norm_id(s: str) -> str:
    """任何形态（URL / oai:arXiv.org:X / arXiv:XvN / 裸号）→ 'NNNN.NNNNN' 或 'hep-th/9901001'；认不出返回 ''。"""
    s = (s or "").strip()
    m = _NEW_ID.search(s)
    if m:
        return m.group(1)
    m = _OLD_ID.search(s)
    return m.group(1) if m else ""


def item_id(aid: str) -> str:
    return f"arxiv:{aid}"


def abs_url(aid: str) -> str:
    return f"https://arxiv.org/abs/{aid}"


def oai_set(cat: str) -> str:
    """分类 → OAI set spec：cs.LG → cs:cs:LG；q-bio.GN → q-bio:q-bio:GN；astro-ph.CO → physics:astro-ph:CO。"""
    arch, _, sub = cat.partition(".")
    group = arch if arch in _TOP_GROUPS else "physics"
    return f"{group}:{arch}:{sub}" if sub else f"{group}:{arch}"


def _http_get(url: str, params: dict) -> str:
    """GET，503 按 Retry-After 退避（OAI 翻页时常见），其他错误抛出。"""
    for attempt in range(4):
        r = requests.get(url, params=params, timeout=120, headers={"User-Agent": UA})
        if r.status_code == 503 and attempt < 3:
            try:
                wait = int(r.headers.get("Retry-After", "10"))
            except ValueError:
                wait = 10
            time.sleep(min(max(wait, 1), 30))
            continue
        r.raise_for_status()
        return r.text
    r.raise_for_status()
    return r.text


def _v1_date(rec: ET.Element) -> str:
    vs = rec.findall(".//r:version", OAI_NS)
    first = next((v for v in vs if v.get("version") == "v1"), vs[0] if vs else None)
    raw = (first.findtext("r:date", "", OAI_NS) if first is not None else "") or ""
    try:
        return parsedate_to_datetime(raw).date().isoformat()
    except (TypeError, ValueError):
        return ""


def _parse_oai(xml_text: str) -> tuple[list[dict], str]:
    """一页 ListRecords → (rows, resumptionToken)。noRecordsMatch 返回空。"""
    root = ET.fromstring(xml_text.encode("utf-8") if isinstance(xml_text, str) else xml_text)
    err = root.find("o:error", OAI_NS)
    if err is not None:
        if err.get("code") == "noRecordsMatch":
            return [], ""
        raise RuntimeError(f"OAI error {err.get('code')}: {(err.text or '').strip()}")
    rows = []
    for rec in root.iter(f"{{{OAI_NS['o']}}}record"):
        header = rec.find("o:header", OAI_NS)
        if header is not None and header.get("status") == "deleted":
            continue
        meta = rec.find(".//r:arXivRaw", OAI_NS)
        if meta is None:
            continue
        aid = norm_id(meta.findtext("r:id", "", OAI_NS))
        if not aid:
            continue
        authors = " ".join((meta.findtext("r:authors", "", OAI_NS) or "").split())
        names = [a.strip() for a in re.split(r",| and ", authors) if a.strip()]
        rows.append({
            "aid": aid,
            "title": " ".join((meta.findtext("r:title", "", OAI_NS) or "").split()),
            "abstract": " ".join((meta.findtext("r:abstract", "", OAI_NS) or "").split()),
            "authors": ", ".join(names[:5]),
            "published": _v1_date(rec),
            "categories": (meta.findtext("r:categories", "", OAI_NS) or "").split(),
        })
    tok = root.find(".//o:resumptionToken", OAI_NS)
    return rows, ((tok.text or "").strip() if tok is not None else "")


def fetch_oai(cat: str, since: str, get: Callable[[str, dict], str] = _http_get) -> list[dict]:
    """一个分类自 since（含）以来的全部变动记录，按 resumptionToken 翻页。"""
    params = {"verb": "ListRecords", "metadataPrefix": "arXivRaw", "set": oai_set(cat), "from": since}
    rows: list[dict] = []
    for page in range(MAX_PAGES):
        got, tok = _parse_oai(get(OAI, params))
        rows += got
        if not tok:
            break
        params = {"verb": "ListRecords", "resumptionToken": tok}
        if get is _http_get:  # arXiv OAI 要求翻页间隔
            time.sleep(3)
    else:
        print(f"[arxiv-oai] {cat}: hit MAX_PAGES={MAX_PAGES}, truncated")
    return rows


def _norm_text(s: str) -> str:
    return re.sub(r"[\s\-_]+", " ", s.lower())


def match_queries(row: dict, queries: list[str]) -> bool:
    """query 词（短语，忽略大小写与连字符差异）出现在标题或摘要里。"""
    if not queries:
        return True
    hay = _norm_text(f"{row['title']} {row['abstract']}")
    return any(_norm_text(q).strip() in hay for q in queries)


def _rss_date(e) -> str:
    for attr in ("published", "updated"):
        raw = getattr(e, attr, "") or ""
        if raw:
            try:
                return parsedate_to_datetime(raw).date().isoformat()
            except (TypeError, ValueError):
                try:
                    return datetime.fromisoformat(raw[:10]).date().isoformat()
                except ValueError:
                    pass
    return ""


def fetch_rss(cat: str, parse: Callable = feed_parse) -> list[dict]:
    """分类 RSS 当日 listing；只留新文（new/cross），replace 类公告丢掉。"""
    feed = parse(f"{RSS}{cat}")
    rows = []
    for e in feed.entries:
        kind = (getattr(e, "arxiv_announce_type", "") or "new").lower()
        if kind.startswith("replace"):
            continue
        aid = norm_id(getattr(e, "id", "") or "") or norm_id(getattr(e, "link", "") or "")
        if not aid:
            continue
        summary = _TAG.sub(" ", getattr(e, "summary", "") or "")
        summary = re.sub(r"^\s*arXiv:\S+\s+Announce Type:\s*\S+\s*(Abstract:)?", "", summary)
        rows.append({
            "aid": aid,
            "title": " ".join((getattr(e, "title", "") or "").split()),
            "abstract": " ".join(summary.split()),
            "authors": " ".join((getattr(e, "author", "") or "").split()),
            "published": _rss_date(e),
        })
    return rows


def _legacy_seen() -> set[str]:
    """过渡期：旧版以 https://arxiv.org/abs/<id> 为 id 写进 seen.json；id 改成 arxiv:<id> 后，
    窗口内已推送过的论文会以新 id 再冒出来一次。这里只读、只查旧 URL 键。"""
    try:
        from ..pipeline.dedup import STATE, _load
        return {k for k in _load(STATE) if k.startswith("https://arxiv.org/abs/")}
    except Exception:
        return set()


def collect(cfg: dict, freqs: dict[str, int], today: date | None = None,
            oai: Callable[[str, str], list[dict]] | None = None,
            rss: Callable[[str], list[dict]] | None = None,
            legacy_seen: set[str] | None = None) -> list[Item]:
    today = today or date.today()
    oai = oai or fetch_oai
    rss = rss or fetch_rss
    legacy = _legacy_seen() if legacy_seen is None else legacy_seen
    oai_cache: dict[tuple[str, str], list[dict] | None] = {}
    rss_cache: dict[str, list[dict]] = {}
    items: list[Item] = []
    for dom in cfg.get("domains", []):
        spec = dom.get("arxiv") or {}
        cadence = spec.get("cadence", "daily")
        if cadence not in freqs:
            continue
        queries = spec.get("queries") or []
        cats = spec.get("categories") or []
        if not queries or not cats:
            continue
        cutoff = (today - timedelta(days=freqs[cadence])).isoformat()
        new_since = (today - timedelta(days=freqs[cadence] + SLACK_DAYS)).isoformat()
        rows: list[dict] = []
        for cat in cats:
            key = (cat, cutoff)
            if key not in oai_cache:
                try:
                    oai_cache[key] = oai(cat, cutoff)
                    print(f"[arxiv-oai] {cat} since {cutoff}: {len(oai_cache[key])} records")
                except Exception as exc:
                    print(f"[arxiv-oai] {cat} failed: {exc}; RSS fallback")
                    oai_cache[key] = None
            got = oai_cache[key]
            if got is not None:
                # OAI：v1 太早的是旧文替换
                rows += [r for r in got if r.get("published") and r["published"] >= new_since]
                continue
            if cat not in rss_cache:
                try:
                    rss_cache[cat] = rss(cat)
                except Exception as exc:
                    print(f"[arxiv-rss] {cat} failed: {exc}")
                    rss_cache[cat] = []
            # RSS：pubDate 即公告日，直接套 cutoff；无日期的不收（避免旧文混入）
            rows += [r for r in rss_cache[cat] if r.get("published") and r["published"] >= cutoff]
        seen: set[str] = set()
        for r in rows:
            if r["aid"] in seen or abs_url(r["aid"]).lower() in legacy or not match_queries(r, queries):
                continue
            seen.add(r["aid"])
            items.append(Item(
                id=item_id(r["aid"]), source="arxiv", domain=dom["name"],
                title=r["title"], url=abs_url(r["aid"]), authors=r["authors"],
                abstract=r["abstract"], published=r["published"],
            ))
    return items
