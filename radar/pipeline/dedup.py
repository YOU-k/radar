from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from ..config import ROOT
from ..schema import Item

STATE = ROOT / "data" / "seen.json"


def _load(state_path: Path) -> dict:
    if state_path.exists():
        try:
            return json.loads(state_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def _key(it: Item) -> str:
    return it.id.strip().lower().rstrip("/")


def filter_new(items: list[Item], state_path: Path = STATE, commit: bool = True) -> list[Item]:
    """按 item.id 去重，状态落在 state_path（可注入，供其他项目复用本模块）。

    commit=False：只过滤不落盘，调用方处理成功后再用 mark_seen 标记——
    这样 LLM 打分失败的条目不会被永久吞掉，下次运行会重新出现。"""
    seen = _load(state_path)
    fresh, batch = [], set()
    for it in items:
        key = _key(it)
        if not key or key in seen or key in batch:
            continue
        batch.add(key)
        fresh.append(it)
    if commit:
        mark_seen(fresh, state_path)
    return fresh


def mark_seen(items: list[Item], state_path: Path = STATE) -> int:
    seen = _load(state_path)
    today = date.today().isoformat()
    for it in items:
        key = _key(it)
        if key:
            seen.setdefault(key, today)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(seen, ensure_ascii=False), encoding="utf-8")
    return len(items)
