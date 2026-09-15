from __future__ import annotations

import os
from datetime import date
from pathlib import Path

from ..config import ROOT, load_sources
from ..schema import Item
from .resources import is_resource

MIN_SCORE = float(os.environ.get("DIGEST_MIN_SCORE", "6"))  # 低于此分不进 digest：领域噪音多，只呈现高价值条目


def write_digest(items: list[Item], day: date) -> Path:
    cfg = load_sources()
    labels = {d["name"]: d.get("label_zh", d["name"]) for d in cfg.get("domains", [])}
    labels.setdefault("tracked", "追踪更新（种子论文引用 / 关注作者）")
    order = [d["name"] for d in cfg.get("domains", [])]
    order += sorted({it.domain for it in items} - set(order))

    kept = [it for it in items if it.score >= MIN_SCORE]
    dropped = len(items) - len(kept)

    lines = [
        f"# 科研情报 digest — {day.isoformat()}",
        "",
        f"共 {len(kept)} 条（仅保留 ≥{MIN_SCORE:g} 分；另有 {dropped} 条低分已过滤）。"
        "分数 0-10，10 = 必须马上读。",
        "",
    ]
    if not kept:
        lines.append("今日无高分条目。")
        lines.append("")
    for dom in order:
        group = [it for it in kept if it.domain == dom]
        if not group:
            continue
        lines.append(f"## {labels.get(dom, dom)}（{len(group)} 条）")
        lines.append("")
        for it in group:
            reason = f" — {it.reason_zh}" if it.reason_zh else ""
            tag = "〔资源〕" if is_resource(it) else ""
            lines.append(f"- **[{it.title}]({it.url})** `{it.score:.1f}`{tag}{reason}")
            lines.append(f"  <sub>{it.source} · {it.published} · {it.authors[:80]}</sub>")
            if it.deepread:
                body = "\n".join(f"  {l}" for l in it.deepread.splitlines())
                lines.append(f"  <details markdown=\"1\"><summary>深读</summary>\n\n{body}\n\n  </details>")
        lines.append("")

    out = ROOT / "digests" / f"{day.isoformat()}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")
    return out
