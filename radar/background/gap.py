"""缺口分析：读大纲 + 指标 + 上轮日志 → 本轮 DiscoveryPlan。

LLM 不可用或解析失败时退化为规则：spec 的 queries/journals + 高引已入库文献做滚雪球种子。"""
from __future__ import annotations

from .llmio import LLM, parse_json_object, tagged
from .models import DiscoveryPlan
from .outline import Outline
from .spec import TopicSpec
from .store import EvidenceStore


def fallback_plan(spec: TopicSpec, store: EvidenceStore, round_no: int) -> DiscoveryPlan:
    evs = store.all()
    ranked = sorted(evs, key=lambda e: -(e.candidate.citations or 0))
    snow = [e.id for e in ranked[:10]] if evs else list(spec.seeds)
    if round_no <= 1:
        snow = list(spec.seeds) + snow
    return DiscoveryPlan(queries=list(spec.queries) or list(spec.keywords[:6]),
                         journals=list(spec.journals), months=spec.months,
                         snowball_ids=list(dict.fromkeys(snow))[:15],
                         focus="冷启动：全量检索 + 种子滚雪球" if round_no <= 1 else "规则计划")


def plan_round(spec: TopicSpec, store: EvidenceStore, outline: Outline,
               round_no: int, llm: LLM | None, last_log: str = "") -> DiscoveryPlan:
    base = fallback_plan(spec, store, round_no)
    if llm is None or round_no <= 1:
        return base
    thin = [s for s in outline.walk() if len(s.evidence_ids) < 3]
    prompt = tagged("gap", (
        f"{spec.profile_text()}\n\n"
        f"当前大纲（节 → 已挂证据数）：\n" +
        "\n".join(f"- {s.id} {s.title}: {len(s.evidence_ids)}" for s in outline.walk()) +
        f"\n\n证据不足 3 篇的节：{', '.join(s.title for s in thin) or '无'}\n"
        f"上轮日志：\n{last_log[-1500:]}\n\n"
        "请给出本轮检索计划：queries（4-8 个英文检索词组，针对薄弱节）、"
        "journals（要回溯的期刊，可空）、focus（一句话说明本轮补什么缺口）。\n"
        '只输出 JSON：{"queries":[...],"journals":[...],"focus":"..."}'))
    try:
        d = parse_json_object(llm.chat(prompt, task="gap"))
    except Exception as exc:  # LLM 失败不阻断
        print(f"[gap] llm failed: {exc}")
        d = {}
    if d.get("queries"):
        base.queries = [str(q)[:80] for q in d["queries"][:8]]
    if d.get("journals"):
        base.journals = [str(j) for j in d["journals"][:10]]
    base.focus = str(d.get("focus", "")) or base.focus
    return base
