"""阶段判断：用证据库的可计算信号（年份分布、近两年占比、引用、CNS 占比、逐轮新增衰减）
给每个子题打 萌芽 / 朝阳 / 成熟 / 夕阳，并给"作为算法提供方接下来怎么做"的建议。

数字由程序算，LLM 只负责解读；每条判断必须引用 ≥2 篇证据 id（程序复核，不足的行阶段改为「证据不足」）。

这些数字是**雷达检索统计，非领域属性**：证据库是按检索词、评审口径抽出来的样本，
section n、近两年占比、CNS 占比只描述"雷达收到了什么"。逐轮入库数（accepted_per_round）
与覆盖度只反映检索进度，不进 prompt——审计发现 LLM 会把 51→8→7→29 读成"审稿门槛抬高"。"""
from __future__ import annotations

import json
import statistics
from datetime import date

import re

from ..journals import is_cns
from .llmio import LLM, tagged
from .models import Evidence
from .outline import Outline, UNSORTED, is_synthesis_title
from .spec import TopicSpec

STAGES = "萌芽（少量探索性工作）/ 朝阳（近两年爆发、CNS 频出、方法未收敛）/ 成熟（方法收敛、增量为主）/ 夕阳（新工作稀少、被替代）"


def _is_cns(venue: str) -> bool:
    """CNS 正刊或主要子刊，精确白名单（radar/journals.py）。旧版前缀匹配会把 Nat Commun、Cell Reports 算进来。"""
    return is_cns(venue)


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
    ts = topic_stats(evs, hist)
    stats = {"说明": "雷达检索统计，非领域属性：只描述雷达证据库这份样本，不代表领域整体规模或发表趋势",
             "topic": {k: v for k, v in ts.items() if k not in ("accepted_per_round", "coverage")},
             "sections": section_stats(evs, outline)}
    prompt = tagged("stage", (
        f"你是资深评审，为方向「{spec.name}」做阶段判断。读者是一位提供算法支持的生物信息学博后"
        f"（衰老 + 单细胞 + 多模态建模），他要决定把精力投到哪个细分方向、怎么切入。\n{spec.profile_text()}\n\n"
        "下面是程序从雷达证据库算出的信号——**雷达检索统计，非领域属性**：n 是雷达收录的篇数，不是领域发文量；"
        "近两年占比、CNS 占比受检索词和评审口径影响。它们只能作为辅助线索，不能单独推出「审稿门槛变化」"
        "「领域是空白」「领域成熟」这类结论；某节 n 很小可能只是证据挂到了别的节。"
        "阶段判断的依据必须是证据本身的内容（方法是否收敛、是否出现大规模验证、是否被替代），"
        "引用统计数字时写成「雷达样本中…」。\n" + json.dumps(stats, ensure_ascii=False) +
        f"\n\n请输出 markdown：\n"
        "1. 一张表：细分方向 | 阶段 | 依据（每行至少引用 2 篇不同证据的 [id]，说明它们的内容为什么支持这个阶段；"
        "证据不足 2 篇的细分方向阶段写「证据不足」）。阶段四选一：" + STAGES + "。\n"
        "2. 「整体判断」一段：这个方向整体处于什么阶段，窗口期还有多久，最大的不确定性是什么。\n"
        "3. 「接下来怎么做」：3-5 条具体建议，每条说明切入点（用什么数据、什么方法、能产出什么）、"
        "为什么现在做、引用支撑的 [id]。优先能与他的合作项目（类器官 + 多组学、公共数据 demo）结合的。\n"
        "关键判断和数字用 **加粗**。只引用给定的 [id]。直接从表格开始，不要开场白。"))
    try:
        return enforce_min_citations(llm.chat(prompt, task="stage", temperature=0.3, timeout=300).strip()) + "\n"
    except Exception as exc:
        print(f"[stage] failed: {exc}")
        from .llmio import FAILED
        return FAILED + "\n"


_CITE = re.compile(r"\[((?:doi|arxiv|pmid|eupmc|s2|url):[^\]\s]+)\]")
_STAGE_WORDS = ("萌芽", "朝阳", "成熟", "夕阳")


def enforce_min_citations(md: str, min_ids: int = 2) -> str:
    """阶段表每行至少引用 min_ids 篇不同证据；不够的行，把阶段格改成「证据不足」并注明。"""
    out = []
    for line in md.split("\n"):
        cells = line.strip().strip("|").split("|") if line.lstrip().startswith("|") else []
        is_row = len(cells) >= 3 and not set(line.replace("|", "").strip()) <= set("-: ")
        if is_row and any(w in cells[1] for w in _STAGE_WORDS):
            if len(set(_CITE.findall(line))) < min_ids:
                cells[1] = " 证据不足 "
                cells[2] = cells[2].rstrip() + f"（引用少于 {min_ids} 篇证据，不下阶段结论） "
                line = "|" + "|".join(cells) + "|"
        out.append(line)
    return "\n".join(out)
