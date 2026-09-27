"""已有日报补主题标签 + 今日要点，并按主题重排（主题表 config/themes.yaml 调整后也可重跑）。

条目以原始行块搬运（出处 / 定位 / 深读原样保留），只插入或替换「主题：」行。"""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

from .. import llm, themes
from .digest import assemble, summary_entries
from .summary import day_summary

ITEM_HEAD = re.compile(r"^- \*\*\[(?P<title>.+?)\]\((?P<url>(?:[^()\s]|\([^()\s]*\))+)\)\*\* `(?P<score>[0-9.]+)`(?:〔资源〕)?(?: — (?P<reason>.*))?$")
SEC = re.compile(r"^## (?P<name>.+?)（\d+ 条）$")
DROPPED = re.compile(r"另有 (\d+) 条低分已过滤")


def parse_blocks(text: str) -> list[dict]:
    """digest → 条目块：{title, url, score, reason, section, lines, meta, bg, themes}。"""
    blocks, section, cur = [], "", None
    for line in text.splitlines():
        m = SEC.match(line)
        if m or line.startswith("## "):
            section = m.group("name") if m else ""
            cur = None
            continue
        m = ITEM_HEAD.match(line)
        if m:
            cur = {"title": m.group("title"), "url": m.group("url"), "score": float(m.group("score")),
                   "reason": m.group("reason") or "", "section": section, "lines": [line],
                   "meta": "", "bg": "", "themes": []}
            blocks.append(cur)
            continue
        if cur is not None and (line.startswith("  ") or line == ""):
            if line.startswith("  <sub>主题："):
                cur["themes"] = themes.parse_line(line[len("  <sub>主题："):-len("</sub>")])
                continue
            if line.startswith("  <sub>定位："):
                cur["bg"] = line[len("  <sub>定位："):-len("</sub>")]
            elif line.startswith("  <sub>") and not cur["meta"]:
                cur["meta"] = line[len("  <sub>"):-len("</sub>")]
            cur["lines"].append(line)
    for b in blocks:  # 去掉块尾空行（节间空行由 assemble 重新加）
        while b["lines"] and b["lines"][-1] == "":
            b["lines"].pop()
    return blocks


def llm_tags(blocks: list[dict]) -> dict[int, list[str]]:
    if not blocks or not llm.available():
        return {}
    payload = [{"id": i, "title": b["title"][:200], "reason": b["reason"], "section": b["section"]}
               for i, b in enumerate(blocks)]
    from .score import THEME_RULE
    prompt = ("给下面每条科研情报条目标主题：" + THEME_RULE +
              f"主题：{themes.prompt_list()}\n\n" + json.dumps(payload, ensure_ascii=False)
              + '\n\n只输出 JSON 数组：[{"id":0,"tags":["cardio","cohort"]}]')
    try:
        out = llm.chat(prompt, model=llm.SCORE_MODEL, temperature=0.1, timeout=180)
        m = re.search(r"\[.*\]", out, re.S)
        rows = json.loads(m.group(0)) if m else []
    except Exception as exc:
        print(f"[retag] tag call failed: {exc}")
        return {}
    res = {}
    for r in rows:
        try:
            res[int(r.get("id", -1))] = themes.clean(r.get("tags") or [])
        except (TypeError, ValueError):
            continue
    return res


def resolve_themes(b: dict, llm_given: list[str] | None, names: dict[str, str]) -> list[str]:
    """LLM 标签（None = LLM 没回答这条，沿用旧标签；[] = LLM 判定无主题）+ 方向背景定位。
    不再按节名/领域兜底：旧兜底把 data_models / ml_algorithms 领域的一切都标成 #单细胞 / #世界模型。"""
    tags = list(b["themes"] if llm_given is None else llm_given)
    if b["bg"]:
        k = themes.for_topic(b["bg"].split(" › ", 1)[0].strip(), names)
        if k and k not in tags:
            tags.append(k)
    return tags[:3]


def with_theme_line(lines: list[str], tags: list[str]) -> list[str]:
    """主题行插在出处行之后（第一条 <sub> 之后），没有出处行就插在标题行后。"""
    out = [l for l in lines if not l.startswith("  <sub>主题：")]
    if not tags:
        return out
    pos = 2 if len(out) > 1 and out[1].startswith("  <sub>") and not out[1].startswith("  <sub>定位：") else 1
    return out[:pos] + [f"  <sub>主题：{themes.line(tags)}</sub>"] + out[pos:]


def retag_digest(path: Path, use_llm: bool = True) -> int:
    text = path.read_text(encoding="utf-8")
    blocks = parse_blocks(text)
    given = llm_tags(blocks) if use_llm else {}
    names = themes.topic_names()
    out_blocks = []
    for i, b in enumerate(blocks):
        tags = resolve_themes(b, given.get(i), names)
        out_blocks.append({"themes": tags, "score": b["score"], "lines": with_theme_line(b["lines"], tags),
                           "title": b["title"], "reason": b["reason"], "venue": b["meta"].split(" · ")[0]})
    summary = day_summary(summary_entries(out_blocks)) if use_llm else []
    m = DROPPED.search(text)
    try:
        day = date.fromisoformat(path.stem)
    except ValueError:
        day = date.today()
    path.write_text(assemble(day, out_blocks, summary, int(m.group(1)) if m else 0), encoding="utf-8")
    return len(out_blocks)
