"""把日报 / 周报挂到方向背景上。

annotate：日报里 ≥ 门槛分的条目，按 radar_domain 找到对应方向，让 LLM 对照该方向的大纲与已有证据，
给出「落在哪个子题 · 相对已有证据的增量是什么」，写进 item.extra["bg"]。
weekly_changes：把各方向报告里的「本次变更」块汇总成周报末尾一节。"""
from __future__ import annotations

import json

from ..schema import Item
from . import llmio
from .llmio import LLM, parse_json_array, tagged
from .outline import Outline, UNSORTED, is_synthesis_title
from .spec import BASE, TopicSpec, load_spec
from .store import EvidenceStore

MIN_SCORE = 6.0


def topics_by_domain(base=None) -> dict[str, list[TopicSpec]]:
    out: dict[str, list[TopicSpec]] = {}
    for p in sorted((base or BASE).glob("*/topic.yaml")):
        if p.parent.name.startswith("_"):
            continue
        spec = load_spec(p)
        for dom in spec.radar_domains:
            out.setdefault(dom, []).append(spec)
    return out


def _outline_brief(spec: TopicSpec, per_section: int = 3) -> list[dict]:
    if not spec.outline_path.exists():
        return []
    outline = Outline.from_markdown(spec.outline_path.read_text(encoding="utf-8"))
    st = EvidenceStore(spec.evidence_dir, spec.rejected_path)
    by_id = {e.id: e for e in st.all()}
    brief = []
    for s in outline.walk():
        if s.children or s.title == UNSORTED or is_synthesis_title(s.title):
            continue
        evs = [by_id[i] for i in s.evidence_ids if i in by_id]
        brief.append({"section": f"{s.id} {s.title}", "n": len(evs),
                      "examples": [e.candidate.title[:70] for e in
                                   sorted(evs, key=lambda e: -(e.candidate.citations or 0))[:per_section]]})
    return brief


def annotate(items: list[Item], cfg: dict, llm: LLM | None = None, base=None,
             min_score: float = MIN_SCORE) -> int:
    llm = llm or (llmio.RadarLLM() if llmio.available() else None)
    if llm is None:
        return 0
    by_dom = topics_by_domain(base)
    n = 0
    for dom, specs in by_dom.items():
        group = [it for it in items if it.domain == dom and it.score >= min_score
                 and "bg" not in it.extra]
        briefs = [(s, b) for s in specs if (b := _outline_brief(s))]
        if not group or not briefs:
            continue
        payload = [{"id": i, "title": it.title, "abstract": (it.abstract or "")[:500],
                    "reason": it.reason_zh} for i, it in enumerate(group)]
        multi = len(briefs) > 1
        if multi:  # 一个 domain 挂多个方向（如单细胞 + 虚拟细胞窄主题）：让 LLM 先选方向
            outline_txt = ("以下几个方向的背景报告大纲（方向 → 子题 → 已有证据数与代表工作）：\n"
                           + json.dumps([{"topic": s.name, "outline": b} for s, b in briefs], ensure_ascii=False)
                           + "\n\n下面是今天新出现的条目。对每条判断：topic（最贴切的方向名，照抄）；")
            fmt = '[{"id":0,"topic":"方向名","section":"2.1 ...","delta":"..."}]'
        else:
            s0, b0 = briefs[0]
            outline_txt = (f"方向「{s0.name}」的背景报告大纲（子题 → 已有证据数与代表工作）：\n"
                           + json.dumps(b0, ensure_ascii=False)
                           + "\n\n下面是今天新出现的条目。对每条判断：")
            fmt = '[{"id":0,"section":"2.1 ...","delta":"..."}]'
        prompt = tagged("context", (
            outline_txt
            + "section（落在哪个子题，抄大纲里的编号+名称；都不合适写「新子题」）；"
              "delta（≤40 字中文：相对该子题已有证据，它新增了什么——新数据/新方法/更大规模/相反结论；"
              "若只是重复已有工作，直说「与 X 重复」）。\n\n【条目】\n" + json.dumps(payload, ensure_ascii=False)
            + f"\n\n只输出 JSON 数组：{fmt}"))
        try:
            rows = parse_json_array(llm.chat(prompt, task="context", temperature=0.2, timeout=180))
        except Exception as exc:
            print(f"[context] {dom} failed: {exc}")
            continue
        names = {s.name for s, _ in briefs}
        for r in rows:
            try:
                i = int(r.get("id", -1))
            except (TypeError, ValueError):
                continue
            if 0 <= i < len(group):
                topic = str(r.get("topic", "")).strip()
                topic = topic if topic in names else briefs[0][0].name
                sec = str(r.get("section", "")).strip()[:60]
                delta = str(r.get("delta", "")).strip()[:80]
                if sec or delta:
                    group[i].extra["bg"] = f"{topic} › {sec} · {delta}".strip(" ·")
                    n += 1
    return n


def weekly_changes(base=None) -> str:
    from .joint import _block
    parts = []
    for p in sorted((base or BASE).glob("*/topic.yaml")):
        if p.parent.name.startswith("_"):
            continue
        spec = load_spec(p)
        if not spec.report_path.exists():
            continue
        block = _block(spec.report_path.read_text(encoding="utf-8"), "本次变更")
        if block and block.strip() != "- 无新增":
            parts.append(f"### {spec.name}\n\n{block}\n")
    if not parts:
        return ""
    return "\n\n---\n\n## 方向背景本周变更\n\n" + "\n".join(parts)
