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


def filter_new(items: list[Item], state_path: Path = STATE) -> list[Item]:
    """按 item.id 去重，状态落在 state_path（可注入，供其他项目复用本模块）。"""
    seen = _load(state_path)
    today = date.today().isoformat()
    fresh = []
    for it in items:
        key = it.id.strip().lower().rstrip("/")
        if not key or key in seen:
            continue
        seen[key] = today
        fresh.append(it)
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(seen, ensure_ascii=False), encoding="utf-8")
    return fresh
