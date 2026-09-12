from __future__ import annotations

import json
from datetime import date

from ..config import ROOT
from ..schema import Item

STATE = ROOT / "data" / "seen.json"


def _load() -> dict:
    if STATE.exists():
        try:
            return json.loads(STATE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def filter_new(items: list[Item]) -> list[Item]:
    seen = _load()
    today = date.today().isoformat()
    fresh = []
    for it in items:
        key = it.id.strip().lower().rstrip("/")
        if not key or key in seen:
            continue
        seen[key] = today
        fresh.append(it)
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(seen, ensure_ascii=False), encoding="utf-8")
    return fresh
