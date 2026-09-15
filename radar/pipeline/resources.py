"""资源清单：数据集 / 数据库 / 模型 / 工具 的长期沉淀，与日报资讯分流。

日报是流动的（当天看过就过），resources.md 是累积的（长期留存、持续更新）。
每天 daily 跑完，把 ≥6 分的资源类条目追加进来；同 URL 不重复。
"""
from __future__ import annotations

import re
from datetime import date

from ..config import ROOT, load_sources
from ..schema import Item

FILE = ROOT / "resources.md"
RESOURCE_KINDS = {"dataset", "model", "tool"}
RESOURCE_SOURCES = {"huggingface", "github"}  # 这两个源天然是资源
MIN_SCORE = 6.0

HEADER = ("# 可用资源清单（数据集 / 数据库 / 模型 / 工具）\n\n"
          "自动累积：每日打分 ≥6 的资源类条目沉淀在此，持续更新。资讯请看日报。\n")


def is_resource(it: Item) -> bool:
    return it.extra.get("kind") in RESOURCE_KINDS or it.source in RESOURCE_SOURCES


def append_resources(items: list[Item], day: date) -> int:
    cand = [it for it in items if it.score >= MIN_SCORE and is_resource(it)]
    if not cand:
        return 0
    cfg = load_sources()
    labels = {d["name"]: d.get("label_zh", d["name"]) for d in cfg.get("domains", [])}
    order = [d.get("label_zh", d["name"]) for d in cfg.get("domains", [])]

    body: dict[str, list[str]] = {}
    if FILE.exists():
        cur = None
        for line in FILE.read_text(encoding="utf-8").splitlines():
            m = re.match(r"## (.+)", line)
            if m:
                cur = m.group(1).strip()
                body.setdefault(cur, [])
            elif cur and line.startswith("- "):
                body[cur].append(line)
    existing = FILE.read_text(encoding="utf-8") if FILE.exists() else ""

    added = 0
    for it in cand:
        if f"]({it.url})" in existing:
            continue
        label = labels.get(it.domain, it.domain)
        kind = it.extra.get("kind") or it.source
        reason = f"{it.reason_zh} " if it.reason_zh else ""
        line = (f"- [{it.title}]({it.url}) — {reason}"
                f"`{it.score:.1f}` · {kind} · {it.source} · {day.isoformat()}")
        body.setdefault(label, []).insert(0, line)
        added += 1

    out = [HEADER]
    for label in order + sorted(set(body) - set(order)):
        if body.get(label):
            out.append(f"## {label}\n")
            out.extend(body[label])
            out.append("")
    FILE.write_text("\n".join(out), encoding="utf-8")
    return added
