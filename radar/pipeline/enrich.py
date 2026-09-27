"""给进 digest 的论文补「发在哪、什么时候、谁的组」。

- 期刊论文：期刊名 + 年月（在线首发月）
- 预印本：预印本平台 + 年月 + 通讯作者（无标记时取末位作者，通常是 PI）及其机构
期刊论文同样附通讯/末位作者机构，便于判断团队。

数据源：OpenAlex（无 key，覆盖 DOI / arXiv / 当周新 bioRxiv），
缺机构时 bioRxiv/medRxiv 官方 API 兜底，再退到 Europe PMC 的作者单位字符串。
只对进 digest 的条目（每天十来条）查询，单条失败不影响整体。
"""
from __future__ import annotations

import re
import time

import requests

from ..schema import Item

OPENALEX = "https://api.openalex.org/works"
BIORXIV = "https://api.biorxiv.org/details"
PAPER_SOURCES = {"europepmc", "arxiv", "semantic_scholar"}

# 预印本 DOI 前缀：bioRxiv/medRxiv（旧 10.1101、2026 起 10.64898）、Research Square、
# arXiv、SSRN、Preprints.org、ChemRxiv、Authorea
PREPRINT_PREFIXES = {"10.1101": "bioRxiv/medRxiv", "10.64898": "bioRxiv/medRxiv",
                     "10.21203": "Research Square", "10.48550": "arXiv", "10.2139": "SSRN",
                     "10.20944": "Preprints.org", "10.26434": "ChemRxiv", "10.22541": "Authorea"}
_ARXIV_ID = re.compile(r"(\d{4}\.\d{4,5})(v\d+)?")
_INST_HINT = re.compile(r"(Universit|Institut|Hospital|College|Academy|Center|Centre|School|Laborator|"
                        r"Foundation|Company|Inc\b|Ltd|GmbH|大学|医院|研究所|研究院)", re.I)


def doi_of(it: Item) -> str:
    if it.id.startswith("doi:"):
        return it.id[4:]
    m = re.search(r"doi\.org/(10\.[^\s?#]+)", it.url)
    if m:
        return m.group(1).lower()
    if it.source == "arxiv" or "arxiv.org" in it.url:
        m = _ARXIV_ID.search(it.id or it.url)
        if m:
            return f"10.48550/arxiv.{m.group(1)}"
    return ""


def preprint_server(doi: str) -> str:
    return PREPRINT_PREFIXES.get(doi.split("/", 1)[0], "") if doi else ""


def short_inst(affiliation: str) -> str:
    """Europe PMC 的长单位串 → 取最像机构名的一段。"""
    parts = [p.strip(" .") for p in re.split(r"[,;]", affiliation or "") if p.strip()]
    hits = [p for p in parts if _INST_HINT.search(p)]
    pick = hits[-1] if hits else (parts[0] if parts else "")
    return re.sub(r"\s*\S+@\S+", "", pick)[:80]


def _get(url: str, params: dict | None = None, timeout: int = 30):
    for attempt in range(2):
        try:
            r = requests.get(url, params=params, timeout=timeout,
                             headers={"User-Agent": "bio-radar/0.1"})
            if r.status_code == 404:
                return None
            if r.status_code == 429 and attempt == 0:
                time.sleep(3)
                continue
            r.raise_for_status()
            return r.json() if r.text.strip() else None
        except Exception:
            if attempt == 1:
                return None
            time.sleep(2)
    return None


def _norm_title(t: str) -> str:
    return re.sub(r"[^a-z0-9]", "", (t or "").lower())[:120]


def openalex_work(doi: str, title: str, get=_get) -> dict | None:
    if doi:
        w = get(f"{OPENALEX}/doi:{doi}")
        if w:
            return w
    if title:  # 无 DOI（S2 / 部分 arXiv）：按标题搜，标题完全一致才认
        d = get(OPENALEX, {"search": title[:200], "per_page": 3})
        for w in (d or {}).get("results", []):
            if _norm_title(w.get("title") or w.get("display_name")) == _norm_title(title):
                return w
    return None


def pi_from_openalex(w: dict) -> tuple[str, str, bool]:
    """(姓名, 机构, 是否通讯作者)。优先通讯作者，否则末位作者。"""
    au = w.get("authorships") or []
    if not au:
        return "", "", False
    corr = [a for a in au if a.get("is_corresponding")]
    a = corr[-1] if corr else au[-1]
    insts = [i.get("display_name", "") for i in a.get("institutions") or [] if i.get("display_name")]
    if not insts:  # 该作者无机构时，退到任一有机构的作者（多为同组）
        for b in reversed(au):
            insts = [i.get("display_name", "") for i in b.get("institutions") or [] if i.get("display_name")]
            if insts:
                break
    return (a.get("author") or {}).get("display_name", ""), (insts[0] if insts else ""), bool(corr)


def biorxiv_corresponding(doi: str, get=_get) -> tuple[str, str]:
    for server in ("biorxiv", "medrxiv"):
        d = get(f"{BIORXIV}/{server}/{doi}")
        rows = (d or {}).get("collection") or []
        if rows:
            r = rows[-1]
            return r.get("author_corresponding", ""), r.get("author_corresponding_institution", "")
    return "", ""


def enrich_item(it: Item, get=_get) -> None:
    ex = it.extra
    doi = doi_of(it)
    server = preprint_server(doi) or ("arXiv" if it.source == "arxiv" else "")
    if ex.get("epmc_src") == "PPR" and not server:
        server = ex.get("preprint_server") or "预印本"
    w = openalex_work(doi, it.title, get=get)
    venue, ym, pi, inst, corr = "", "", "", "", False
    if w:
        src = ((w.get("primary_location") or {}).get("source") or {})
        venue = src.get("display_name", "")
        if src.get("type") == "repository" and not server:
            server = venue
        ym = (w.get("publication_date") or "")[:7]
        pi, inst, corr = pi_from_openalex(w)
    if server:
        ex["venue_type"] = "preprint"
        # OpenAlex 的仓库名带括号全称（"bioRxiv (Cold Spring Harbor Laboratory)"），取短名
        ex["venue"] = (venue.split(" (")[0] if venue else "") or ex.get("preprint_server") or server
        if doi.startswith(("10.1101/", "10.64898/")) and not inst:
            p, i = biorxiv_corresponding(doi, get=get)
            pi, inst, corr = (p or pi), i, bool(p) or corr
    else:
        ex["venue_type"] = "journal" if (venue or ex.get("journal")) else ""
        ex["venue"] = venue or ex.get("journal", "")  # OpenAlex 大小写规范（EPMC 是 "Nature medicine"）
    ex["pub_ym"] = ex.get("pub_ym") or ym or (it.published or "")[:7]
    if not inst and ex.get("last_affil"):
        inst = short_inst(ex["last_affil"])
        pi = pi or ex.get("last_author", "")
    if pi:
        ex["pi"] = pi
        ex["pi_role"] = "通讯" if corr else "末位"
    if inst:
        ex["pi_inst"] = inst


def enrich(items: list[Item], min_score: float, get=_get, pause: float = 0.2) -> int:
    n = 0
    for it in items:
        if it.score < min_score or it.source not in PAPER_SOURCES:
            continue
        try:
            enrich_item(it, get=get)
            n += 1
        except Exception as exc:
            print(f"[enrich] {it.id} failed: {exc}")
        time.sleep(pause)
    return n


def venue_line(it: Item) -> str:
    """digest 元信息行的前半段：〔期刊〕Nature Medicine · 2026-09 · 通讯 张三（某大学）"""
    ex = it.extra
    kind = {"preprint": "〔预印本〕", "journal": "〔期刊〕"}.get(ex.get("venue_type", ""), "")
    venue = ex.get("venue") or ex.get("journal") or ""
    ym = ex.get("pub_ym") or (it.published or "")[:7]
    parts = [f"{kind}{venue}".strip() or it.source]
    if ym:
        parts.append(ym)
    if ex.get("pi"):
        who = f"{ex.get('pi_role', '末位')} {ex['pi']}"
        parts.append(f"{who}（{ex['pi_inst']}）" if ex.get("pi_inst") else who)
    elif ex.get("pi_inst"):
        parts.append(ex["pi_inst"])
    return " · ".join(parts)


VENUE_RE = re.compile(r"^  <sub>〔(?P<kind>期刊|预印本)〕(?P<venue>[^·]+?) · (?P<ym>\d{4}-\d{2})")


def venue_stats(digest_texts: list[str], top: int = 12) -> str:
    """周报用：本周 digest 条目按「期刊 / 预印本平台」计数，程序统计不经 LLM。"""
    from collections import Counter
    kinds, venues = Counter(), Counter()
    for t in digest_texts:
        for line in t.splitlines():
            m = VENUE_RE.match(line)
            if m:
                kinds[m.group("kind")] += 1
                venues[(m.group("kind"), m.group("venue").strip())] += 1
    if not venues:
        return ""
    rows = [f"| {v} | {k} | {n} |" for (k, v), n in venues.most_common(top)]
    return ("\n\n## 本周来源分布\n\n"
            f"期刊 {kinds['期刊']} 篇 · 预印本 {kinds['预印本']} 篇（仅统计进 digest 的论文）\n\n"
            "| 期刊 / 平台 | 类型 | 篇数 |\n|---|---|---|\n" + "\n".join(rows) + "\n")
