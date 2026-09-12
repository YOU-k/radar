from __future__ import annotations

import argparse
import os
import re
from datetime import date, timedelta

import requests

from .collectors import COLLECTORS
from .config import ROOT, load_profile, load_sources
from .pipeline.dedup import filter_new
from .pipeline.digest import write_digest
from .pipeline.score import ARK_BASE, ARK_MODEL, score_items


def cmd_daily(days: int, use_llm: bool) -> None:
    cfg = load_sources()
    items = []
    for name, mod in COLLECTORS.items():
        try:
            got = mod.collect(cfg, days)
            print(f"[{name}] {len(got)} items")
            items.extend(got)
        except Exception as exc:
            print(f"[{name}] collector failed: {exc}")
    fresh = filter_new(items)
    print(f"[dedup] {len(items)} -> {len(fresh)} new")
    scored = score_items(fresh, cfg, use_llm=use_llm)
    out = write_digest(scored, date.today())
    print(f"[digest] wrote {out}")


def cmd_weekly(use_llm: bool) -> None:
    today = date.today()
    week_start = today - timedelta(days=6)
    texts = []
    for i in range(7):
        p = ROOT / "digests" / f"{(week_start + timedelta(days=i)).isoformat()}.md"
        if p.exists():
            texts.append(p.read_text(encoding="utf-8"))
    iso = today.isocalendar()
    out = ROOT / "weekly" / f"{iso.year}-W{iso.week:02d}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    header = f"# 每周综合 — {iso.year}-W{iso.week:02d}（{week_start} ~ {today}）\n\n"
    if not texts:
        out.write_text(header + "本周无 digest。\n", encoding="utf-8")
        print(f"[weekly] no digests, wrote {out}")
        return
    body = _weekly_llm(texts) if use_llm else None
    if body is None:
        body = _weekly_fallback(texts)
    out.write_text(header + body, encoding="utf-8")
    print(f"[weekly] wrote {out}")


def _weekly_llm(texts: list[str]) -> str | None:
    key = os.environ.get("ARK_API_KEY")
    if not key:
        return None
    joined = "\n\n---\n\n".join(t[:6000] for t in texts)[:24000]
    prompt = (
        "下面是某研究者的兴趣画像和本周每日科研情报 digest。\n\n"
        f"【兴趣画像】\n{load_profile()}\n\n【本周 digest】\n{joined}\n\n"
        "请输出中文 markdown，含三节：\n"
        "## 跨域趋势\n本周值得注意的 3-5 个跨领域信号（不是条目罗列，是趋势判断）。\n"
        "## 对多模态衰老模型合作的启发\n结合画像里的合作项目，给 3 个具体、可执行的启发（数据/方法/实验设计层面）。\n"
        "## Registry 增补建议\n本周出现的数据库/模型/人物中，建议加入 registry 长期知识库的条目，"
        "按 databases.md / models.md / people.md 分组，每条一行。"
    )
    try:
        r = requests.post(
            f"{ARK_BASE}/chat/completions",
            headers={"Authorization": f"Bearer {key}",
                     "Content-Type": "application/json"},
            json={"model": ARK_MODEL,
                  "messages": [{"role": "user", "content": prompt}],
                  "temperature": 0.3},
            timeout=300,
        )
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    except Exception as exc:
        print(f"[weekly] LLM failed, fallback to raw list: {exc}")
        return None


def _weekly_fallback(texts: list[str]) -> str:
    titles = []
    for t in texts:
        for line in t.splitlines():
            if line.startswith("- **["):
                titles.append(line)
    return ("（未启用 LLM，以下为本周 digest 高分条目汇总）\n\n"
            + "\n".join(titles[:80]) + "\n")


def main() -> None:
    ap = argparse.ArgumentParser(prog="radar")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("daily", "weekly"):
        p = sub.add_parser(name)
        p.add_argument("--days", type=int, default=1)
        p.add_argument("--no-llm", action="store_true")
    args = ap.parse_args()
    if args.cmd == "daily":
        cmd_daily(args.days, use_llm=not args.no_llm)
    else:
        cmd_weekly(use_llm=not args.no_llm)


if __name__ == "__main__":
    main()
