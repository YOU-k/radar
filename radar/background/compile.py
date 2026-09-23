"""整篇重编：每节只喂该节挂载的证据 → 节文本（逐句 [id]）→ 装配 → 引用校验 → 编号。

报告永远从证据库 + 大纲整体生成；不打补丁。"""
from __future__ import annotations

import json
import re
from datetime import date

from .llmio import LLM, tagged
from .models import Evidence
from .outline import Outline, Section, is_synthesis_title
from .spec import TopicSpec

CITE = re.compile(r"\[((?:doi|arxiv|pmid):[^\]\s]+)\]")
def is_synthesis(sec: Section, spec: TopicSpec) -> bool:
    """综合节：不挂证据，而是基于全部证据与其他节正文来写（背景与定义、空白与趋势）。"""
    return is_synthesis_title(sec.title)


_HEADING = re.compile(r"^\s*#{1,6}\s+.*$", re.M)


def strip_headings(text: str) -> str:
    """LLM 常把节名再写一遍成标题；装配时已有标题，去掉。"""
    return _HEADING.sub("", text).strip() + "\n"


def target_length(n_evidence: int) -> tuple[int, int]:
    """段落数与字数随证据量伸缩：每 3 篇约一段，每篇约 180 字，下限 2 段 600 字。"""
    import math
    paras = max(2, min(12, math.ceil(n_evidence / 3)))
    chars = max(600, min(6000, 180 * n_evidence))
    return paras, chars


def _ev_rows(evs: list[Evidence]) -> list[dict]:
    return [{"id": e.id, "title": e.candidate.title, "venue": e.candidate.venue,
             "year": e.candidate.year, "citations": e.candidate.citations,
             **{k: v for k, v in e.extraction.items() if v}} for e in evs]


def write_section(sec: Section, evs: list[Evidence], spec: TopicSpec, llm: LLM) -> str:
    if not evs:
        return f"（本节暂无入库证据）\n"
    paras, chars = target_length(len(evs))
    prompt = tagged("compile", (
        f"你在为方向「{spec.name}」写背景报告的一节：「{sec.title}」。本节有 {len(evs)} 篇证据，"
        f"请写约 {paras} 段、不少于 {chars} 字的中文，每篇证据都要被实质性地讨论到，不要只点名。\n"
        "只依据下面的证据写，不要引入证据之外的事实。每个具体论断后面用 [id] 标注来源，"
        "id 原样照抄；保留数字；按方法/时间/子问题组织，对比不同工作的差异与争议，"
        "证据之间冲突要指出。直接从正文开始，不要写「本节」「综上」「以下为」这类套话。\n\n"
        "【证据】\n" + json.dumps(_ev_rows(evs), ensure_ascii=False)))
    try:
        return strip_headings(llm.chat(prompt, task="compile", temperature=0.3, timeout=300))
    except Exception as exc:
        print(f"[compile] section {sec.id} failed: {exc}")
        return "（生成失败）\n"


def write_synthesis(sec: Section, spec: TopicSpec, body: str, evs: list[Evidence], llm: LLM) -> str:
    """综合节：读全部证据摘要 + 已写正文，只允许引用已有 id。"""
    if not evs:
        return "（暂无证据）\n"
    rows = [{"id": e.id, "title": e.candidate.title, "year": e.candidate.year,
             "summary": e.extraction.get("summary", "")[:160]} for e in evs]
    prompt = tagged("compile", (
        f"你在为方向「{spec.name}」写背景报告的综合节：「{sec.title}」。\n{spec.profile_text()}\n\n"
        "依据下面的证据清单与已写正文，写 3-6 段中文：若是背景/定义类，讲清方向边界、演化脉络、"
        "核心问题；若是趋势/空白类，用编号列表指出趋势与没人做的方向，每条给依据。"
        "只引用清单里的 [id]，不要编造。直接从正文开始，不要写「以下为…」之类的开场白。\n\n"
        "【证据清单】\n" + json.dumps(rows, ensure_ascii=False)[:12000] +
        "\n\n【已写正文】\n" + body[:16000]))
    try:
        return strip_headings(llm.chat(prompt, task="compile", temperature=0.3, timeout=300))
    except Exception as exc:
        print(f"[compile] synthesis {sec.id} failed: {exc}")
        return "（生成失败）\n"


def write_tldr(spec: TopicSpec, body: str, llm: LLM) -> str:
    prompt = tagged("compile", (
        f"下面是方向「{spec.name}」背景报告的正文。请写 6-10 条 TL;DR 要点（中文，每条一句，"
        "保留 [id] 引用和数字，覆盖趋势/关键工作/数据/争议/空白），只输出要点列表：\n\n" + body[:20000]))
    try:
        return llm.chat(prompt, task="compile", temperature=0.3, timeout=300).strip() + "\n"
    except Exception as exc:
        print(f"[compile] tldr failed: {exc}")
        return ""


def check_citations(text: str, known: set[str]) -> tuple[list[str], list[str]]:
    """返回（合法引用 id 列表，未知 id 列表）。"""
    ids = list(dict.fromkeys(CITE.findall(text)))
    return [i for i in ids if i in known], [i for i in ids if i not in known]


def number_citations(text: str, order: list[str]) -> str:
    idx = {eid: n for n, eid in enumerate(order, 1)}
    return CITE.sub(lambda m: f"[{idx[m.group(1)]}]" if m.group(1) in idx else "", text)


def assemble(spec: TopicSpec, outline: Outline, evs: list[Evidence], sections_md: dict[str, str],
             tldr: str, coverage: float, round_no: int, changelog: str = "") -> str:
    by_id = {e.id: e for e in evs}
    body_parts = []
    def emit(secs: list[Section], level: int):
        for s in secs:
            body_parts.append(f"{'#' * level} {s.id} {s.title}\n\n{sections_md.get(s.id, '')}")
            emit(s.children, level + 1)
    emit(outline.sections, 2)
    body = "\n".join(body_parts)
    used, unknown = check_citations(tldr + body, set(by_id))
    if unknown:
        print(f"[compile] dropped {len(unknown)} unknown citations: {unknown[:5]}")
    order = used + [e.id for e in evs if e.id not in used]
    refs = []
    for n, eid in enumerate(order, 1):
        e = by_id[eid]
        c = e.candidate
        refs.append(f"{n}. {c.title}. {c.venue or ''} {c.year or ''}. {c.url or c.id}")
    head = (f"# {spec.name} · 方向背景报告\n\n"
            f"证据 {len(evs)} 篇 · 覆盖度 {coverage:.2f} · 第 {round_no} 轮 · 更新 {date.today().isoformat()}\n\n"
            + (f"## 本次变更\n\n{changelog}\n\n" if changelog else "")
            + (f"## 摘要（TL;DR）\n\n{tldr}\n" if tldr else ""))
    full = head + body + "\n## 参考文献\n\n" + "\n".join(refs) + "\n"
    return number_citations(full, order)


def compile_report(spec: TopicSpec, outline: Outline, evs: list[Evidence], llm: LLM,
                   coverage: float, round_no: int, changelog: str = "") -> str:
    by_id = {e.id: e for e in evs}
    sections_md = {}
    synth = []
    for s in outline.walk():
        sec_evs = [by_id[i] for i in s.evidence_ids if i in by_id]
        if is_synthesis(s, spec):
            synth.append(s)
            continue
        sections_md[s.id] = write_section(s, sec_evs, spec, llm) if (sec_evs or not s.children) else ""
    body = "\n".join(sections_md.values())
    for s in synth:  # 综合节最后写，能看到全部正文
        sections_md[s.id] = write_synthesis(s, spec, body, evs, llm)
    tldr = write_tldr(spec, body, llm) if evs else ""
    return assemble(spec, outline, evs, sections_md, tldr, coverage, round_no, changelog)
