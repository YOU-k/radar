"""深读环节：对高分条目拉全文（arXiv PDF），用 LLM 出结构化中文深读。

成本护栏：每天最多 DEEPREAD_MAX 条，且分数 >= DEEPREAD_MIN。
任何一步失败都静默降级——条目照常进 digest，只是没有深读块。
"""
from __future__ import annotations

import io
import os

import requests

from .. import llm
from ..config import load_profile
from ..schema import Item

MAX_PER_DAY = int(os.environ.get("DEEPREAD_MAX", "3"))
MIN_SCORE = float(os.environ.get("DEEPREAD_MIN", "7.5"))
TEXT_CHARS = 25000


def _fulltext(it: Item) -> str:
    """返回 (正文, 来源标注)。非 arXiv 源 v1 用 abstract 兜底。"""
    if it.source == "arxiv" and "/abs/" in it.url:
        pdf_url = it.url.replace("/abs/", "/pdf/")
        from pypdf import PdfReader  # 重依赖，用到才导入
        r = requests.get(pdf_url, timeout=120)
        r.raise_for_status()
        reader = PdfReader(io.BytesIO(r.content))
        text = "\n".join((p.extract_text() or "") for p in reader.pages[:15])
        if len(text) > 2000:
            return text[:TEXT_CHARS], "全文"
    return (it.abstract or "")[:6000], "仅摘要"


def _deepread_one(it: Item, profile: str) -> str:
    text, basis = _fulltext(it)
    prompt = (
        "下面是某研究者的兴趣画像和一篇文献的内容。请写中文深读笔记，markdown，含五节，"
        "每节 1-3 句，直接以小标题开头：\n"
        "**总结** / **核心方法** / **数据与代码可用性**（能否直接拿来用，给出线索）/ "
        "**局限** / **对多模态衰老模型合作的启发**（结合画像，具体可执行）。\n\n"
        f"【兴趣画像】\n{profile}\n\n"
        f"【文献】\n标题：{it.title}\n作者：{it.authors}\n链接：{it.url}\n"
        f"内容（{basis}）：\n{text}"
    )
    return llm.chat(prompt, model=llm.DEEP_MODEL, temperature=0.3, timeout=300).strip()


def deepread_top(items: list[Item]) -> int:
    """对排序后的 items 里高分者深读，原地写 it.deepread，返回深读条数。"""
    if not llm.available():
        return 0
    profile = load_profile()
    picked = [it for it in items if it.score >= MIN_SCORE][:MAX_PER_DAY]
    n = 0
    for it in picked:
        try:
            it.deepread = _deepread_one(it, profile)
            n += 1
            print(f"[deepread] {it.score:.1f} {it.title[:60]}")
        except Exception as exc:
            print(f"[deepread] failed for {it.title[:60]}: {exc}")
    return n
