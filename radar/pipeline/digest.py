from __future__ import annotations

from datetime import date
from pathlib import Path

from ..config import ROOT, load_sources
from ..schema import Item


def write_digest(items: list[Item], day: date) -> Path:
    cfg = load_sources()
    labels = {d["name"]: d.get("label_zh", d["name"]) for d in cfg.get("domains", [])}
    labels.setdefault("tracked", "追踪更新（种子论文引用 / 关注作者）")
    order = [d["name"] for d in cfg.get("domains", [])]
    order += sorted({it.domain for it in items} - set(order))

    lines = [
        f"# 科研情报 digest — {day.isoformat()}",
        "",
        f"共 {len(items)} 条（抓取 → 去重 → 关键词粗筛 → LLM 精排）。分数 0-10，10 = 必须马上读。",
        "",
    ]
    for dom in order:
        group = [it for it in items if it.domain == dom]
        if not group:
            continue
        lines.append(f"## {labels.get(dom, dom)}（{len(group)} 条）")
        lines.append("")
        for it in group:
            reason = f" — {it.reason_zh}" if it.reason_zh else ""
            lines.append(f"- **[{it.title}]({it.url})** `{it.score:.1f}`{reason}")
            lines.append(f"  <sub>{it.source} · {it.published} · {it.authors[:80]}</sub>")
        lines.append("")

    out = ROOT / "digests" / f"{day.isoformat()}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    return out
