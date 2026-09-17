"""结构化抽取：把条目变成可聚合的 JSON 字段（方法/数据/场景/基准/可用性）。

一句话总结撑不起综合报告——质量来自字段级抽取。
日报里 ≥7 分的条目每天追加到 data/extractions.jsonl，作为周报综合的原料；
专题深研报告（deepdive）对所有入选文献批量走同一套抽取。
"""
from __future__ import annotations

import json
import re
from datetime import date

from .. import llm
from ..config import ROOT
from ..schema import Item

STORE = ROOT / "data" / "extractions.jsonl"
BATCH = 10

_KEYS = ("method", "data", "scenario", "benchmark", "availability", "summary")


def extract_items(items: list[Item], topic: str = "") -> list[dict]:
    """批量结构化抽取，与 items 对齐返回；LLM 不可用时返回空摘要。"""
    out = [{k: "" for k in _KEYS} for _ in items]
    if not llm.available() or not items:
        return out
    scope = f"这些文献都与「{topic}」相关。" if topic else ""
    for i in range(0, len(items), BATCH):
        chunk = items[i:i + BATCH]
        payload = [
            {"id": j, "title": it.title, "abstract": (it.abstract or "")[:800],
             "journal": it.extra.get("journal", ""), "published": it.published}
            for j, it in enumerate(chunk)
        ]
        prompt = (
            f"下面是一批科研文献。{scope}请对每篇输出结构化字段：\n"
            "method：方法类型（≤15字，如 flow matching生成模型、空间蛋白组基础模型）。\n"
            "data：训练/使用的数据类型与规模（≤25字，如 41-plex空间蛋白组/1800万细胞；不确定留空）。\n"
            "scenario：应用场景（≤15字，如 免疫治疗响应预测、药物重定位）。\n"
            "benchmark：基准/关键定量结果（≤30字，如 较扩散模型保真度+77%；没有留空）。\n"
            "availability：代码/权重/数据可用性（≤15字；摘要没提就留空，不要编）。\n"
            "summary：2-3句中文，做了什么、怎么做的、发现了什么，要具体、保留关键数字。\n\n"
            "【文献】\n" + json.dumps(payload, ensure_ascii=False)
            + '\n\n只输出 JSON 数组，形如 [{"id":0,"method":"...","data":"...","scenario":"...",'
              '"benchmark":"...","availability":"...","summary":"..."}]，不要输出其他内容。'
        )
        try:
            content = llm.chat(prompt, model=llm.SCORE_MODEL, temperature=0.2, timeout=180)
            m = re.search(r"\[.*\]", content, re.DOTALL)
            rows = json.loads(m.group(0)) if m else []
            for r in rows:
                j = int(r.get("id", -1))
                if 0 <= j < len(chunk):
                    for k in _KEYS:
                        out[i + j][k] = str(r.get(k, "")).strip()[:200]
        except Exception as exc:
            print(f"[extract] batch {i // BATCH} failed: {exc}")
    return out


def store(items: list[Item], extractions: list[dict], day: date) -> int:
    """把抽取结果追加进 JSONL 存（按 URL 去重），供周报/月度综合读取。"""
    seen = set()
    if STORE.exists():
        for line in STORE.read_text(encoding="utf-8").splitlines():
            try:
                seen.add(json.loads(line)["url"])
            except (json.JSONDecodeError, KeyError):
                continue
    n = 0
    with STORE.open("a", encoding="utf-8") as f:
        for it, ex in zip(items, extractions):
            if it.url in seen or not ex.get("summary"):
                continue
            rec = {"date": day.isoformat(), "domain": it.domain,
                   "title": it.title, "url": it.url, "score": it.score,
                   "journal": it.extra.get("journal", ""), **ex}
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            n += 1
    return n


def load_since(days: int) -> list[dict]:
    """读最近 N 天的抽取记录（周报用）。"""
    if not STORE.exists():
        return []
    cutoff = date.today().toordinal() - days
    recs = []
    for line in STORE.read_text(encoding="utf-8").splitlines():
        try:
            r = json.loads(line)
            if date.fromisoformat(r["date"]).toordinal() > cutoff:
                recs.append(r)
        except (json.JSONDecodeError, KeyError, ValueError):
            continue
    return recs
