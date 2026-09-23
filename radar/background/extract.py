"""结构化抽取：字段与 radar/pipeline/extract.py 兼容并扩展 results / limitations。

有全文时用全文前 6000 字，否则用摘要。"""
from __future__ import annotations

import json

from .llmio import LLM, parse_json_array, tagged
from .models import Candidate
from .spec import TopicSpec

KEYS = ("method", "data", "scenario", "benchmark", "results", "availability",
        "limitations", "summary")
BATCH = 8


def empty() -> dict:
    return {k: "" for k in KEYS}


def extract(cands: list[Candidate], spec: TopicSpec, llm: LLM,
            fulltexts: dict[str, str] | None = None) -> list[dict]:
    fulltexts = fulltexts or {}
    out = [empty() for _ in cands]
    for b in range(0, len(cands), BATCH):
        chunk = cands[b:b + BATCH]
        rows = []
        for i, c in enumerate(chunk):
            ft = fulltexts.get(c.id, "")
            rows.append({"id": i, "title": c.title, "venue": c.venue, "year": c.year,
                         "text": (ft[:6000] if ft else (c.abstract or "")[:1500]),
                         "has_fulltext": bool(ft)})
        prompt = tagged("extract", (
            f"这些文献都属于方向「{spec.name}」。请对每篇输出结构化字段（中文，具体、保留数字）：\n"
            "method（≤20字）、data（数据类型与规模 ≤30字）、scenario（≤15字）、"
            "benchmark（基准或对比对象 ≤30字）、results（关键定量结果 ≤60字）、"
            "availability（代码/权重/数据是否公开，≤20字；文中没提留空）、"
            "limitations（作者承认或明显的局限 ≤40字）、summary（3 句：做了什么、怎么做、发现什么）。\n\n"
            "【文献】\n" + json.dumps(rows, ensure_ascii=False) +
            '\n\n只输出 JSON 数组：[{"id":0,"method":"...",...,"summary":"..."}]'))
        try:
            parsed = parse_json_array(llm.chat(prompt, task="extract"))
        except Exception as exc:
            print(f"[extract] batch {b // BATCH} failed: {exc}")
            parsed = []
        for r in parsed:
            try:
                i = int(r.get("id", -1))
            except (TypeError, ValueError):
                continue
            if 0 <= i < len(chunk):
                for k in KEYS:
                    out[b + i][k] = str(r.get(k, "")).strip()[:300]
    return out
