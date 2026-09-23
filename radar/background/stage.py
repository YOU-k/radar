"""阶段判断：用证据库的可计算信号（年份分布、近两年占比、引用、CNS 占比、逐轮新增衰减）
给每个子题打 萌芽 / 朝阳 / 成熟 / 夕阳，并给"作为算法提供方接下来怎么做"的建议。

数字由程序算，LLM 只负责解读；每条判断必须引用证据 id。"""
from __future__ import annotations

import json
import statistics
from datetime import date

from .llmio import LLM, tagged
from .models import Evidence
from .outline import Outline, UNSORTED, is_synthesis_title
from .spec import TopicSpec

CNS = ("nature", "science", "cell")
STAGES = "萌芽（少量探索性工作）/ 朝阳（近两年爆发、CNS 频出、方法未收敛）/ 成熟（方法收敛、增量为主）/ 夕阳（新工作稀少、被替代）"


def _is_cns(venue: str) -> bool:
    v = (venue or "").lower()
    return any(v == c or v.startswith(c + " ") or v.startswith("nat ") or v.startswith("cell ") for c in CNS) \
        or v in ("nature", "science", "cell")


def section_stats(evs: list[Evidence], outline: Outline, this_year: int | None = None) -> list[dict]:
    this_year = this_year or date.today().year
    by_id = {e.id: e for e in evs}
    out = []
    for s in outline.walk():
        if s.children or s.title == UNSORTED or is_synthesis_title(s.title):
            continue
        sec = [by_id[i] for i in s.evidence_ids if i in by_id]
        years = [e.candidate.year for e in sec if e.candidate.year]
        cites = [e.candidate.citations or 0 for e in sec]
        out.append({
            "section": f"{s.id} {s.title}", "n": len(sec),
            "recent_share": round(sum(1 for y in years if y >= this_year - 1) / len(years), 2) if years else 0.0,
            "year_span": f"{min(years)}-{max(years)}" if years else "",
            "median_citations": int(statistics.median(cites)) if cites else 0,
            "cns_share": round(sum(1 for e in sec if _is_cns(e.candidate.venue)) / len(sec), 2) if sec else 0.0,
            "top": [{"id": e.id, "title": e.candidate.title[:80], "year": e.candidate.year,
                     "citations": e.candidate.citations}
                    for e in sorted(sec, key=lambda e: -(e.candidate.citations or 0))[:4]],
        })
    return out


def topic_stats(evs: list[Evidence], hist: list[dict], this_year: int | None = None) -> dict:
    this_year = this_year or date.today().year
    years = [e.candidate.year for e in evs if e.candidate.year]
    n_by_round = [h.get("n_evidence", 0) for h in hist]
    added = [b - a for a, b in zip([0] + n_by_round[:-1], n_by_round)] if n_by_round else []
    return {"n_evidence": len(evs),
            "recent_share": round(sum(1 for y in years if y >= this_year - 1) / len(years), 2) if years else 0.0,
            "year_hist": {str(y): years.count(y) for y in sorted(set(years))},
            "cns_share": round(sum(1 for e in evs if _is_cns(e.candidate.venue)) / len(evs), 2) if evs else 0.0,
            "accepted_per_round": added,
            "coverage": [h.get("score") for h in hist]}


def stage_section(spec: TopicSpec, evs: list[Evidence], outline: Outline, hist: list[dict],
                  llm: LLM) -> str:
    if not evs:
        return "（暂无证据）\n"
    stats = {"topic": topic_stats(evs, hist), "sections": section_stats(evs, outline)}
    prompt = tagged("stage", (
        f"你是资深评审，为方向「{spec.name}」做阶段判断。读者是一位提供算法支持的生物信息学博后"
        f"（衰老 + 单细胞 + 多模态建模），他要决定把精力投到哪个细分方向、怎么切入。\n{spec.profile_text()}\n\n"
        "下面是程序从证据库算出的信号（不要重新数，直接引用）：\n" + json.dumps(stats, ensure_ascii=False) +
        f"\n\n请输出 markdown：\n"
        "1. 一张表：细分方向 | 阶段 | 依据（引用数字与 [id]）。阶段四选一：" + STAGES + "。\n"
        "2. 「整体判断」一段：这个方向整体处于什么阶段，窗口期还有多久，最大的不确定性是什么。\n"
        "3. 「接下来怎么做」：3-5 条具体建议，每条说明切入点（用什么数据、什么方法、能产出什么）、"
        "为什么现在做、引用支撑的 [id]。优先能与他的合作项目（类器官 + 多组学、公共数据 demo）结合的。\n"
        "关键判断和数字用 **加粗**。只引用给定的 [id]。直接从表格开始，不要开场白。"))
    try:
        return llm.chat(prompt, task="stage", temperature=0.3, timeout=300).strip() + "\n"
    except Exception as exc:
        print(f"[stage] failed: {exc}")
        return "（生成失败）\n"
