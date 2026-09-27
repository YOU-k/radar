"""日报「今日要点」：把当天进 digest 的条目按主题归纳成 3-5 条，给出今天最值得读的一篇。"""
from __future__ import annotations

import json

from .. import llm, themes
from ..schema import Item


def item_themes(it: Item) -> list[str]:
    """条目主题：LLM 标签 + 方向背景定位的方向，去重后最多 3 个；都没有就不打标签。
    不再按采集领域兜底——data_models / ml_algorithms 领域的兜底把无关条目都标成 #单细胞 / #世界模型。"""
    tags = list(it.extra.get("themes") or [])
    bg = it.extra.get("bg", "")
    if bg:
        k = themes.for_topic(bg.split(" › ", 1)[0].strip(), themes.topic_names())
        if k and k not in tags:
            tags.append(k)
    return tags[:3]


def _profile_lines() -> str:
    """画像的标题与应用线，供要点提示「只可引用这些方向」。"""
    try:
        from ..config import load_profile
        text = load_profile()
    except Exception:
        return ""
    import re
    heads = re.findall(r"^##+ (.+)$", text, re.M)
    lines = re.findall(r"^\d+\. \*\*(.+?)\*\*", text, re.M)
    return "；".join(h for h in heads + lines if not h.startswith(("打", "中间档")))[:800]


def day_summary(entries: list[dict]) -> list[str]:
    """entries: [{title, score, reason, themes:[label], venue}] → markdown 列表行。LLM 不可用或失败返回 []。"""
    if not entries or not llm.available():
        return []
    prompt = (
        "下面是一位生物信息学博后今天情报日报里的条目（已按他的研究画像打分过，带主题标签与出处）。"
        "请写「今日要点」：3-5 条中文要点，每条以一个或两个主题标签开头（形如 #心血管 #人群队列，只能用条目里出现过的标签），"
        "把同一主题的相关条目归并成一句判断（写清新东西是什么：数据/方法/结论），不要逐条复述；"
        "最后单独一条以「必读：」开头，指出今天最值得花时间读的一篇（写标题前半截）和一句理由。每条不超过 70 字。\n"
        "规则：1) 每个数字都必须紧跟它所属条目的名字（标题前几个词或模型/数据名），只写条目 reason 或标题里出现过的数字，"
        "不要把两篇的数字、队列或结论并进同一个分句；不确定数字属于哪篇就不写数字。"
        "2) 期刊/平台照条目的 venue 字段写，预印本不要说成期刊，不要写「两篇 Nature Medicine」这类未经核对的计数。"
        "3) 不要写「你的 X 方向」「对标你的…」这类第二人称兴趣判断，除非 X 是下面画像摘录里原样出现的方向。\n\n"
        f"【画像里的方向（只可引用这些）】{_profile_lines()}\n\n"
        + json.dumps(entries, ensure_ascii=False)[:12000]
        + "\n\n只输出 markdown 列表，每行以 '- ' 开头，不要标题。")
    try:
        out = llm.chat(prompt, model=llm.SCORE_MODEL, temperature=0.3, timeout=180)
    except Exception as exc:
        print(f"[summary] failed: {exc}")
        return []
    return [l.strip() for l in out.splitlines() if l.strip().startswith("- ")][:6]
