"""日报去重。状态 data/seen.json：{key: 首次见到的日期}。

一篇论文的 key 不止 item.id：
- DOI ↔ arXiv 互认：arXiv 2603.21235 同时记 arxiv:2603.21235 与 doi:10.48550/arxiv.2603.21235；
  arXiv API（http://arxiv.org/abs/NNNNvK）与 RSS（https://arxiv.org/abs/NNNN）写法归一；
- 规范化标题 t:<前 12 个词>（≥4 个词才记，避免 "Editorial" 这类撞车）：同一篇以期刊 DOI 和 arXiv 两个身份出现
  （审计里的 Domain Elastic Transform：TPAMI 6 分 + arXiv 7 分）只收第一次。

另外：已知发表日期早于 MAX_AGE_DAYS 的条目不收（RSS 的 replace 公告会把 2024 年的论文当新条目送进来）；
写盘时删掉 PRUNE_DAYS 天前的记录——最宽的采集窗口是 30 天，180 天足够挡住回流，seen.json 不再无限增长。"""
from __future__ import annotations

import json
import re
from datetime import date, timedelta
from pathlib import Path

from ..config import ROOT
from ..schema import Item

STATE = ROOT / "data" / "seen.json"
MAX_AGE_DAYS = 90
PRUNE_DAYS = 180

_ARXIV = re.compile(r"(?:arxiv\.org/(?:abs|pdf)/|arxiv[:.])(\d{4}\.\d{4,5})(?:v\d+)?", re.I)
_DOI = re.compile(r"(?:^doi:|doi\.org/)(10\.\d{4,9}/\S+)", re.I)


def _load(state_path: Path) -> dict:
    if state_path.exists():
        try:
            return json.loads(state_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def _key(it: Item) -> str:
    return it.id.strip().lower().rstrip("/")


def title_key(title: str) -> str:
    words = re.sub(r"[^a-z0-9 ]", " ", (title or "").lower()).split()
    return "t:" + " ".join(words[:12]) if len(words) >= 4 else ""


def id_keys(raw: str, include_raw: bool = True) -> set[str]:
    """一个 id / url 的全部等价写法（含 DOI ↔ arXiv 互认）。include_raw=False 只要派生出的 doi:/arxiv: 键。"""
    k = (raw or "").strip().lower().rstrip("/")
    if not k:
        return set()
    out = {k} if include_raw else set()
    m = _ARXIV.search(k)
    if m:
        out |= {f"arxiv:{m.group(1)}", f"doi:10.48550/arxiv.{m.group(1)}"}
    m = _DOI.search(k)
    if m:
        out.add("doi:" + m.group(1).rstrip(".,;"))
    return out


def item_keys(it: Item) -> set[str]:
    keys = id_keys(it.id) | id_keys(it.url, include_raw=False)  # url 本身太泛（RSS/占位），只取其中的 DOI/arXiv
    doi = str(it.extra.get("doi") or "").lower()
    if doi:
        keys |= id_keys(doi if doi.startswith("doi:") else "doi:" + doi)
    ax = str(it.extra.get("arxiv_id") or "").lower()
    if ax:
        keys |= id_keys(ax if ax.startswith("arxiv:") else "arxiv:" + ax)
    t = title_key(it.title)
    if t:
        keys.add(t)
    return keys


def _published(it: Item) -> date | None:
    try:
        return date.fromisoformat((it.published or "")[:10])
    except ValueError:
        return None


def _lookup(seen: dict) -> set[str]:
    """旧 seen.json 存的是原始 id：展开成等价写法再比，避免 API/RSS 写法不同导致已读论文回流。"""
    out = set()
    for k in seen:
        out.add(k)
        if not k.startswith("t:"):
            out |= id_keys(k)
    return out


def filter_new(items: list[Item], state_path: Path = STATE, commit: bool = True,
               today: date | None = None, max_age_days: int = MAX_AGE_DAYS) -> list[Item]:
    """按 id（含 DOI/arXiv 互认）与规范化标题去重，丢弃发表日期过旧的条目；状态落在 state_path。

    commit=False：只过滤不落盘，调用方处理成功后再用 mark_seen 标记——
    这样 LLM 打分失败的条目不会被永久吞掉，下次运行会重新出现。"""
    today = today or date.today()
    oldest = today - timedelta(days=max_age_days)
    seen = _lookup(_load(state_path))
    fresh, batch = [], set()
    n_old = 0
    for it in items:
        if not _key(it):
            continue
        keys = item_keys(it)
        if keys & seen or keys & batch:
            continue
        pub = _published(it)
        if pub and pub < oldest:
            n_old += 1
            continue
        batch |= keys
        fresh.append(it)
    if n_old:
        print(f"[dedup] dropped {n_old} items published before {oldest}")
    if commit:
        mark_seen(fresh, state_path, today=today)
    return fresh


def prune(seen: dict, today: date, keep_days: int = PRUNE_DAYS) -> dict:
    cutoff = (today - timedelta(days=keep_days)).isoformat()
    return {k: v for k, v in seen.items() if not (isinstance(v, str) and len(v) >= 10 and v[:10] < cutoff)}


def mark_seen(items: list[Item], state_path: Path = STATE, today: date | None = None) -> int:
    today = today or date.today()
    seen = _load(state_path)
    stamp = today.isoformat()
    for it in items:
        if _key(it):
            for k in item_keys(it):
                seen.setdefault(k, stamp)
    seen = prune(seen, today)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(seen, ensure_ascii=False), encoding="utf-8")
    return len(items)
