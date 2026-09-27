"""HuggingFace 新发布模型 / 数据集。

2026-09 审计：旧实现按 lastModified 排、limit=10，再用 7/30 天窗口过滤，几乎每次 0 条
（生物类 query 在 HF 上本来就少，最新的 aging 模型是两个月前；而 lastModified 排序被频繁
重传的个人仓库占满）。

现在的取舍（保留，不下架）：
- sort=createdAt 取最新创建的 100 个，窗口 = max(节奏天数, MIN_WINDOW_DAYS)，重复交给 dedup；
- 质量门槛：必须**挂了论文**（tags 里有 arxiv:NNNN.NNNNN，排除模型卡模板自带的 1910.09700）
  或 likes ≥ MIN_LIKES。按 createdAt 取回的绝大多数是个人练手仓库（0 like、无论文），不设门槛会刷屏；
  挂的论文须是近 PAPER_MAX_AGE_DAYS 天内的（引用老论文的微调仓库不算），同一论文多个仓库只留一个，
  每个 query 最多 PER_QUERY 条——控制进入 LLM 打分的量；
- 实测（2026-09-27）：生物类 query（aging/methylation/single-cell/biobank …）30 天内仍是 0，
  这是 HF 本身的供给问题；ML 类（jepa/world model/agent）每月有十几到几十条挂论文的发布。
  每次运行打印每个 query 的 raw / 窗口内 / 过门槛 数量，便于追踪产出，长期为 0 的 query 可从 sources.yaml 删掉。
"""
from __future__ import annotations

import re
import time
from datetime import datetime, timedelta, timezone

import requests

from ..schema import Item

API = "https://huggingface.co/api"
LIMIT = 100
MIN_WINDOW_DAYS = 14
MIN_LIKES = 2
PAPER_MAX_AGE_DAYS = 180
PER_QUERY = 5
TEMPLATE_PAPERS = {"1910.09700"}  # HF 模型卡模板里"碳排放估算"引用的论文，几乎每个自动生成的卡都有
_ARXIV_TAG = re.compile(r"^arxiv:(\d{4}\.\d{4,5})$")


def _created(m: dict) -> datetime | None:
    raw = m.get("createdAt") or ""
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00"))
    except ValueError:
        return None


def papers(m: dict) -> list[str]:
    out = []
    for t in m.get("tags") or []:
        mm = _ARXIV_TAG.match(str(t))
        if mm and mm.group(1) not in TEMPLATE_PAPERS:
            out.append(mm.group(1))
    return out


def _recent_paper(aid: str, now: datetime) -> bool:
    """论文编号 YYMM 在 PAPER_MAX_AGE_DAYS 内——"随论文发布的新模型"，而不是引用老论文的微调。"""
    y, m = 2000 + int(aid[:2]), int(aid[2:4])
    return (now.year - y) * 12 + (now.month - m) <= PAPER_MAX_AGE_DAYS // 30


def worth_keeping(m: dict, now: datetime | None = None) -> bool:
    now = now or datetime.now(timezone.utc)
    mid = str(m.get("id", "")).lower()
    if "gguf" in (m.get("tags") or []) or re.search(r"gguf|awq|gptq|exl2|mlx|-\d+bit\b|merge", mid):
        return False  # 量化 / 合并版是二次打包，不是新资源
    return any(_recent_paper(a, now) for a in papers(m)) or (m.get("likes") or 0) >= MIN_LIKES


def _fetch(kind: str, query: str) -> list[dict]:
    r = requests.get(f"{API}/{kind}", params={
        "search": query, "sort": "createdAt", "direction": -1, "limit": LIMIT, "full": "true",
    }, timeout=30)
    r.raise_for_status()
    return r.json()


def select(rows: list[dict], cutoff: datetime, now: datetime | None = None) -> tuple[list[dict], int]:
    """→ (过门槛的, 窗口内总数)。同一篇论文的多个仓库（一个组织一次传 4 个变体）只留第一个；
    每个 query 最多 PER_QUERY 条，按 likes、downloads 排。"""
    recent = [m for m in rows if (_created(m) or cutoff - timedelta(days=1)) >= cutoff]
    kept, seen_papers = [], set()
    for m in sorted(recent, key=lambda m: (-(m.get("likes") or 0), -(m.get("downloads") or 0))):
        if not worth_keeping(m, now):
            continue
        ps = set(papers(m))
        if ps and ps & seen_papers:
            continue
        seen_papers |= ps
        kept.append(m)
    return kept[:PER_QUERY], len(recent)


def collect(cfg: dict, freqs: dict[str, int], fetch=_fetch, now: datetime | None = None) -> list[Item]:
    now = now or datetime.now(timezone.utc)
    items = []
    for dom in cfg.get("domains", []):
        cadence = dom.get("hf_cadence", "daily")
        if cadence not in freqs:
            continue
        cutoff = now - timedelta(days=max(freqs[cadence], MIN_WINDOW_DAYS))
        for q in dom.get("hf_queries") or []:
            for kind in ("models", "datasets"):
                try:
                    raw = fetch(kind, q)
                except Exception as exc:
                    print(f"[hf] {kind} {q!r} failed: {exc}")
                    continue
                rows, n_recent = select(raw, cutoff, now)
                print(f"[hf] {kind} {q!r}: raw {len(raw)} · in window {n_recent} · kept {len(rows)}")
                for m in rows:
                    mid = m.get("id", "")
                    if not mid:
                        continue
                    url = (f"https://huggingface.co/{mid}" if kind == "models"
                           else f"https://huggingface.co/datasets/{mid}")
                    desc = m.get("description")
                    ps = papers(m)
                    tags = [t for t in (m.get("tags") or []) if not str(t).startswith(("arxiv:", "region:"))]
                    items.append(Item(
                        id=f"hf:{kind}:{mid}", source="huggingface",
                        domain=dom["name"],
                        title=f"[{kind[:-1]}] {mid}", url=url,
                        authors=m.get("author", "") or mid.split("/")[0],
                        abstract=(desc if isinstance(desc, str) and desc else
                                  ", ".join(tags[:8]) + (f" · paper arXiv:{ps[0]}" if ps else "")),
                        published=(m.get("createdAt") or "")[:10],
                        extra={"likes": m.get("likes", 0), "downloads": m.get("downloads", 0),
                               **({"arxiv": ps} if ps else {})},
                    ))
                if fetch is _fetch:
                    time.sleep(0.5)
    return items
