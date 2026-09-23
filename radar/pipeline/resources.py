"""资源清单：公开可获取的大数据集 / 模型的长期沉淀，与日报资讯分流。

日报是流动的（当天看过就过），resources.md 是累积的（长期留存、持续更新）。
门槛从严：只收 LLM 判定为 dataset/model 且 ≥7 分的——即确实存在、
公开可获取、能直接拿来用的；普通方法论文和小工具不进清单。
条目由 LLM 补结构化字段（数据类型/规模/获取方式/一句话价值），按使用场景分组。

资源判断双通道：
A. 发布驱动（append_resources）：新论文自发布的数据集/模型，≥7 分进「新发布资源」。
B. 用量挖掘（mine_infrastructure）：聚合抽取记录里每篇文献"用了什么数据"，
   被 ≥2 篇独立高分工作反复使用的资源才是真基础设施（Tahoe-100M、TCGA 这类），
   进「领域基础设施」区并附使用证据。这是主通道——用量投票比单次打分可靠。
"""
from __future__ import annotations

import json
import re
from datetime import date

from .. import llm
from ..config import ROOT
from ..schema import Item

FILE = ROOT / "resources.md"
RESOURCE_KINDS = {"dataset", "model"}
MIN_SCORE = 7.0

CATEGORIES = [
    "单细胞 / 空间组学",
    "衰老时钟 / 表观遗传",
    "蛋白组 / 蛋白模型",
    "基因组 / 调控",
    "人群队列 / 多模态",
    "通用 ML / 其他",
]

INFRA_SECTION = "领域基础设施（被多篇高分工作反复使用）"

HEADER = ("# 可用资源清单\n\n"
          "「领域基础设施」：用量挖掘——被多篇高分工作反复用于训练/评测的数据集与基准，附使用证据。\n"
          "「新发布资源」：只收确认公开可获取、打分 ≥7 的新数据集/模型，按场景分组。资讯请看日报。\n")


def is_resource(it: Item) -> bool:
    return it.extra.get("kind") in RESOURCE_KINDS


def _enrich(cands: list[Item]) -> list[dict]:
    """LLM 补结构化字段；失败时回退到 reason_zh + 空字段。"""
    fallback = [{"category": "", "modality": "", "scale": "", "access": "",
                 "value": it.reason_zh} for it in cands]
    if not llm.available():
        return fallback
    payload = [{"id": i, "title": it.title, "abstract": (it.abstract or "")[:500],
                "reason": it.reason_zh} for i, it in enumerate(cands)]
    prompt = (
        "下面是几个新发布的数据集/模型条目。请为每个条目输出结构化字段，供资源清单展示。\n"
        f"category {len(CATEGORIES)} 选一：{'；'.join(CATEGORIES)}。\n"
        "modality：数据类型/模态（≤12字，如 单细胞转录组、DNA甲基化、蛋白序列）。\n"
        "scale：规模（≤15字，如 50万细胞、1亿条序列；不确定就留空，不要编）。\n"
        "access：获取方式（≤15字，如 HF权重公开、GEO:GSExxx、GitHub；不确定就留空）。\n"
        "value：一句话说明它是什么、适合什么使用场景（≤40字，要具体，不要套话）。\n\n"
        "【条目】\n" + json.dumps(payload, ensure_ascii=False)
        + '\n\n只输出 JSON 数组，形如 [{"id":0,"category":"...","modality":"...",'
          '"scale":"...","access":"...","value":"..."}]，不要输出其他内容。'
    )
    try:
        content = llm.chat(prompt, model=llm.SCORE_MODEL, temperature=0.2, timeout=120)
        m = re.search(r"\[.*\]", content, re.DOTALL)
        rows = json.loads(m.group(0)) if m else []
        out = list(fallback)
        for r in rows:
            j = int(r.get("id", -1))
            if 0 <= j < len(cands):
                cat = str(r.get("category", "")).strip()
                out[j] = {
                    "category": cat if cat in CATEGORIES else "",
                    "modality": str(r.get("modality", "")).strip()[:20],
                    "scale": str(r.get("scale", "")).strip()[:20],
                    "access": str(r.get("access", "")).strip()[:20],
                    "value": str(r.get("value", "")).strip()[:80] or cands[j].reason_zh,
                }
        return out
    except Exception as exc:
        print(f"[resources] enrich failed, fallback: {exc}")
        return fallback


def _parse_existing() -> dict[str, list[str]]:
    """读出已有分组和条目块（- 开头行 + 后续缩进属同一条）。"""
    body: dict[str, list[str]] = {}
    if not FILE.exists():
        return body
    cur = None
    for line in FILE.read_text(encoding="utf-8").splitlines():
        m = re.match(r"## (.+)", line)
        if m:
            cur = m.group(1).strip()
            body.setdefault(cur, [])
        elif cur and line.startswith("- "):
            body[cur].append(line)
        elif cur and line.startswith("  ") and body[cur]:
            body[cur][-1] += "\n" + line
    return body


def _write(body: dict[str, list[str]]) -> None:
    out = [HEADER]
    order = [INFRA_SECTION] + CATEGORIES
    for cat in order + sorted(set(body) - set(order)):
        if body.get(cat):
            out.append(f"## {cat}\n")
            out.extend(body[cat])
            out.append("")
    FILE.write_text("\n".join(out), encoding="utf-8")


def append_resources(items: list[Item], day: date) -> int:
    cand = [it for it in items if it.score >= MIN_SCORE and is_resource(it)]
    if not cand:
        return 0
    existing = FILE.read_text(encoding="utf-8") if FILE.exists() else ""
    cand = [it for it in cand if f"]({it.url})" not in existing]
    if not cand:
        return 0
    metas = _enrich(cand)
    body = _parse_existing()

    for it, meta in zip(cand, metas):
        kind = it.extra.get("kind") or "resource"
        detail = f"`{kind}`"
        if meta["modality"]:
            detail += f" · {meta['modality']}"
        if meta["scale"]:
            detail += f" · 规模 {meta['scale']}"
        if meta["access"]:
            detail += f" · 获取：{meta['access']}"
        detail += f" · `{it.score:.1f}` 分 · {day.isoformat()}"
        block = f"- [{it.title}]({it.url}) — {meta['value']}\n  {detail}"
        body.setdefault(meta["category"] or CATEGORIES[-1], []).insert(0, block)

    _write(body)
    return len(cand)


def mine_infrastructure(recs: list[dict], day: date) -> int:
    """通道 B（主通道）：从抽取记录聚合"每篇用了什么数据"，
    被 ≥2 篇独立高分工作使用的资源 → 「领域基础设施」区，附使用证据。

    recs: extract 模块的记录（需含 title / data / summary 字段）。
    """
    pool = [{"id": i, "title": r.get("title", ""), "data": r.get("data", "")}
            for i, r in enumerate(recs) if r.get("data")]
    if len(pool) < 3 or not llm.available():
        return 0
    prompt = (
        "下面是一批高分科研文献的标题和它们「训练/评测所用的数据」字段。"
        "请识别被 ≥2 篇独立文献使用的数据集 / 数据库 / 基准资源"
        "（如 Tahoe-100M、DepMap PRISM、TCGA 这类被反复使用的基础设施）。\n"
        "对每个资源输出：name（标准英文名）、scale（规模，提及才写）、"
        "usage（它被用来干什么，≤20字，如 扰动预测训练基准）、"
        "used_by（使用它的文献 id 列表，从输入抄）。\n"
        "只在单篇出现的自发布数据集不要收录；常识性小工具不要收录。\n\n"
        "【文献数据字段】\n" + json.dumps(pool, ensure_ascii=False)[:16000]
        + '\n\n只输出 JSON 数组，形如 [{"name":"...","scale":"...","usage":"...","used_by":[0,3]}]。'
    )
    try:
        content = llm.chat(prompt, model=llm.SCORE_MODEL, temperature=0.1, timeout=180)
        m = re.search(r"\[.*\]", content, re.DOTALL)
        rows = json.loads(m.group(0)) if m else []
    except Exception as exc:
        print(f"[resources] infrastructure mining failed: {exc}")
        return 0

    body = _parse_existing()
    existing_names = {
        re.sub(r"\*\*", "", e.split("—")[0]).strip(" -[]").lower()
        for e in body.get(INFRA_SECTION, [])}
    added = 0
    for r in rows:
        name = str(r.get("name", "")).strip()
        used = [pool[j]["title"] for j in r.get("used_by", [])
                if isinstance(j, int) and 0 <= j < len(pool)]
        if not name or len(used) < 2 or name.lower() in existing_names:
            continue
        scale = f"{str(r.get('scale', '')).strip()} · " if r.get("scale") else ""
        shown = " / ".join(t[:40] for t in used[:3])
        block = (f"- **{name}** — {scale}{str(r.get('usage', '')).strip()}\n"
                 f"  被 {len(used)} 篇高分工作使用：{shown} · {day.isoformat()} 收录")
        body.setdefault(INFRA_SECTION, []).insert(0, block)
        existing_names.add(name.lower())
        added += 1
    if added:
        _write(body)
    return added
