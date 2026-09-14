from __future__ import annotations

import json
import re

from .. import llm
from ..config import load_profile
from ..schema import Item

PREFILTER_TOP = 40
BATCH = 20


def keyword_score(item: Item, cfg: dict) -> float:
    dom = next((d for d in cfg.get("domains", []) if d["name"] == item.domain), None)
    kws = []
    if dom:
        kws = (dom.get("keywords_en") or []) + (dom.get("keywords_zh") or [])
    title, abstract = item.title.lower(), (item.abstract or "").lower()
    score = 0.0
    for kw in kws:
        k = kw.lower()
        if k in title:
            score += 2.0
        elif k in abstract:
            score += 1.0
    score += min(item.extra.get("stars", 0), 500) / 250.0
    score += min(item.extra.get("likes", 0), 200) / 100.0
    return score


def prefilter(items: list[Item], cfg: dict) -> list[Item]:
    for it in items:
        it.score = keyword_score(it, cfg)
    items.sort(key=lambda x: x.score, reverse=True)
    return items[:PREFILTER_TOP]


def llm_rerank(items: list[Item]) -> bool:
    if not llm.available() or not items:
        return False
    profile = load_profile()
    ok = False
    for i in range(0, len(items), BATCH):
        chunk = items[i:i + BATCH]
        payload = [
            {"id": j, "title": it.title, "abstract": (it.abstract or "")[:600],
             "source": it.source, "domain": it.domain}
            for j, it in enumerate(chunk)
        ]
        prompt = (
            "下面是某研究者的兴趣画像和一批新条目。"
            "请对每条打分 0-10（10=必须马上读，0=完全无关）并用一句中文说明理由（不超过40字）。\n\n"
            f"【兴趣画像】\n{profile}\n\n【条目】\n"
            + json.dumps(payload, ensure_ascii=False)
            + '\n\n只输出 JSON 数组，形如 [{"id":0,"score":8,"reason":"..."}]，不要输出其他内容。'
        )
        try:
            content = llm.chat(prompt, model=llm.SCORE_MODEL, temperature=0.2, timeout=180)
            m = re.search(r"\[.*\]", content, re.DOTALL)
            scores = json.loads(m.group(0)) if m else []
            for s in scores:
                j = int(s.get("id", -1))
                if 0 <= j < len(chunk):
                    chunk[j].score = float(s.get("score", chunk[j].score))
                    chunk[j].reason_zh = str(s.get("reason", ""))[:120]
            ok = True
        except Exception as exc:
            print(f"[llm] batch {i // BATCH} failed, keep keyword scores: {exc}")
    return ok


def score_items(items: list[Item], cfg: dict, use_llm: bool = True) -> list[Item]:
    items = prefilter(items, cfg)
    if use_llm:
        llm_rerank(items)
    items.sort(key=lambda x: x.score, reverse=True)
    return items
