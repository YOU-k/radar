"""日报「今日要点」：把当天进 digest 的条目按主题归纳成 3-5 条，给出今天最值得读的一篇。"""
from __future__ import annotations

import json

from .. import llm, themes
from ..schema import Item


def item_themes(it: Item) -> list[str]:
    """条目主题：LLM 标签 → 方向背景定位的方向 → 领域默认，去重后最多 3 个。"""
    tags = list(it.extra.get("themes") or [])
    bg = it.extra.get("bg", "")
    if bg:
        k = themes.for_topic(bg.split(" › ", 1)[0].strip(), themes.topic_names())
        if k and k not in tags:
            tags.append(k)
    if not tags:
        k = themes.for_domain(it.domain)
        if k:
            tags.append(k)
    return tags[:3]


def day_summary(entries: list[dict]) -> list[str]:
    """entries: [{title, score, reason, themes:[label], venue}] → markdown 列表行。LLM 不可用或失败返回 []。"""
    if not entries or not llm.available():
        return []
    prompt = (
        "下面是一位生物信息学博后今天情报日报里的条目（已按他的研究画像打分过，带主题标签与出处）。"
        "请写「今日要点」：3-5 条中文要点，每条以一个或两个主题标签开头（形如 #心血管 #人群队列，只能用条目里出现过的标签），"
        "把同一主题的相关条目归并成一句判断（写清新东西是什么：数据/方法/结论，带关键数字），不要逐条复述；"
        "最后单独一条以「必读：」开头，指出今天最值得花时间读的一篇（写标题前半截）和一句理由。每条不超过 70 字。\n\n"
        + json.dumps(entries, ensure_ascii=False)[:12000]
        + "\n\n只输出 markdown 列表，每行以 '- ' 开头，不要标题。")
    try:
        out = llm.chat(prompt, model=llm.SCORE_MODEL, temperature=0.3, timeout=180)
    except Exception as exc:
        print(f"[summary] failed: {exc}")
        return []
    return [l.strip() for l in out.splitlines() if l.strip().startswith("- ")][:6]
