from __future__ import annotations

import os
from datetime import date
from pathlib import Path

from .. import themes
from ..config import ROOT
from ..schema import Item
from .enrich import venue_line
from .resources import is_resource
from .summary import day_summary, item_themes

MIN_SCORE = float(os.environ.get("DIGEST_MIN_SCORE", "6"))  # 低于此分不进 digest：领域噪音多，只呈现高价值条目
OTHER = "其他"


def item_block(it: Item, tags: list[str]) -> list[str]:
    """一条条目的 markdown 行：标题行 + 出处行 + 主题行 + 定位行 + 深读块。"""
    reason = f" — {it.reason_zh}" if it.reason_zh else ""
    tag = "〔资源〕" if is_resource(it) else ""
    lines = [f"- **[{it.title}]({it.url})** `{it.score:.1f}`{tag}{reason}"]
    if it.extra.get("venue_type") or it.extra.get("pi"):
        lines.append(f"  <sub>{venue_line(it)} · {it.authors[:60]}</sub>")
    else:  # 非论文（GitHub/HF/博客）或未补全
        journal = it.extra.get("journal")
        src = f"{journal} · {it.source}" if journal else it.source
        lines.append(f"  <sub>{src} · {it.published} · {it.authors[:80]}</sub>")
    if tags:
        lines.append(f"  <sub>主题：{themes.line(tags)}</sub>")
    if it.extra.get("bg"):
        lines.append(f"  <sub>定位：{it.extra['bg']}</sub>")
    if it.deepread:
        body = "\n".join(f"  {l}" for l in it.deepread.splitlines())
        lines.append(f"  <details markdown=\"1\"><summary>深读</summary>\n\n{body}\n\n  </details>")
    return lines


def assemble(day: date, blocks: list[dict], summary: list[str], dropped: int) -> str:
    """blocks: [{themes:[key], score, lines}] → 整篇 digest。按第一主题分节、节内按分数排序，节序跟 themes.yaml。"""
    bk = themes.by_key()
    lines = [f"# 科研情报 digest — {day.isoformat()}", "",
             f"共 {len(blocks)} 条（仅保留 ≥{MIN_SCORE:g} 分；另有 {dropped} 条低分已过滤）。"
             "分数 0-10，10 = 必须马上读。", ""]
    if not blocks:
        return "\n".join(lines + ["今日无高分条目。", ""])
    if summary:
        lines += ["## 今日要点", ""] + summary + [""]
    order = themes.keys() + [OTHER]
    for key in order:
        group = sorted((b for b in blocks if (b["themes"][0] if b["themes"] else OTHER) == key),
                       key=lambda b: -b["score"])
        if not group:
            continue
        label = bk[key]["label"] if key in bk else OTHER
        lines += [f"## {label}（{len(group)} 条）", ""]
        for b in group:
            lines += b["lines"]
        lines.append("")
    return "\n".join(lines)


def summary_entries(blocks: list[dict]) -> list[dict]:
    bk = themes.by_key()
    return [{"title": b["title"][:120], "score": b["score"], "reason": b.get("reason", ""),
             "themes": [bk[k]["label"] for k in b["themes"] if k in bk], "venue": b.get("venue", "")}
            for b in sorted(blocks, key=lambda b: -b["score"])]


def write_digest(items: list[Item], day: date, use_llm: bool = True) -> Path:
    kept = [it for it in items if it.score >= MIN_SCORE]
    blocks = []
    for it in kept:
        tags = item_themes(it)
        blocks.append({"themes": tags, "score": it.score, "lines": item_block(it, tags),
                       "title": it.title, "reason": it.reason_zh,
                       "venue": venue_line(it) if it.extra.get("venue_type") else it.source})
    summary = day_summary(summary_entries(blocks)) if use_llm else []
    out = ROOT / "digests" / f"{day.isoformat()}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(assemble(day, blocks, summary, len(items) - len(kept)), encoding="utf-8")
    return out
