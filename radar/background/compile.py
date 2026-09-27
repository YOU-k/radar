"""整篇重编：每节只喂该节挂载的证据 → 节文本（逐句 [id]）→ 数字核验 → 装配（去重段落）→ 引用校验 → 编号。

报告永远从证据库 + 大纲整体生成；不打补丁。

数字核验（check_claims）：凡同时含数字与 [id] 的句子，句中每个数字都必须出现在所引证据的
摘要 / 标题 / 抽取字段里（抽取时已标为原文找不到的数字不算）。不通过的句子**直接删除**，
不做标注——这样报告里留下的每个带引用的数字都有出处，全局判断与联合分析从 TL;DR 取 [证据]
时也不会再把错数字复制下去。被删的句子写进 <topic>/claim_check.json 备查，报告头部显示删句数。"""
from __future__ import annotations

import json
import re
from datetime import date

from . import grounding
from .llmio import LLM, tagged, FAILED, GenerationFailed
from .models import Evidence
from .outline import Outline, Section, is_synthesis_title
from .spec import TopicSpec

CITE = re.compile(r"\[((?:doi|arxiv|pmid|eupmc|s2|url):[^\]\s]+)\]")  # 与 models.normalize_id 的前缀一致
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


ABSTRACT_CHARS = 600


def _ev_rows(evs: list[Evidence]) -> list[dict]:
    return [{"id": e.id, "title": e.candidate.title, "venue": e.candidate.venue,
             "year": e.candidate.year, "citations": e.candidate.citations,
             "abstract": (e.candidate.abstract or "")[:ABSTRACT_CHARS],
             **{k: v for k, v in e.extraction.items() if v and not k.startswith("_")}} for e in evs]


# ---- 数字核验 ----

def evidence_numbers(e: Evidence) -> list[float]:
    """证据可作为出处的数字：摘要、标题、年份、期刊、抽取字段（去掉抽取时标为原文找不到的）。"""
    ex_text = " ".join(v for k, v in e.extraction.items() if isinstance(v, str) and not k.startswith("_"))
    for it in e.extraction.get("_unverified_numbers") or []:
        if it.get("reason") == "not_found" and it.get("number"):
            ex_text = re.sub(rf"(?<![\d.]){re.escape(it['number'])}(?![\d.])", " ", ex_text)
    c = e.candidate
    return grounding.pool(c.abstract or "", c.title or "", str(c.year or ""), c.venue or "", ex_text)


_SENT = re.compile(r"[^。！？!?]+(?:[。！？!?]+|$)")


def _is_year(n: grounding.Num) -> bool:
    return not n.scaled and n.decimals == 0 and 1950 <= n.value <= 2100


def claim_ok(sentence: str, by_id: dict[str, Evidence], cache: dict | None = None) -> bool:
    """句中无引用或无数字 → 不查；有数字有引用 → 每个数字都要在所引证据里找到。只引了未知 id 的也不通过。"""
    ids = CITE.findall(sentence)
    if not ids:
        return True
    nums = [n for n in grounding.numbers(grounding.strip_citations(sentence).replace("**", "")) if not _is_year(n)]
    if not nums:
        return True
    known = [i for i in ids if i in by_id]
    if not known:
        return False
    cache = cache if cache is not None else {}
    values = []
    for i in known:
        if i not in cache:
            cache[i] = evidence_numbers(by_id[i])
        values.extend(cache[i])
    return all(grounding.supported(n, values) for n in nums)


def check_claims(text: str, by_id: dict[str, Evidence], cache: dict | None = None) -> tuple[str, list[str]]:
    """删掉数字对不上所引证据的句子。表格行与标题行不动。返回（新文本，被删句子）。"""
    cache = cache if cache is not None else {}
    out, dropped = [], []
    for line in text.split("\n"):
        if not line.strip() or line.lstrip().startswith(("|", "#")):
            out.append(line)
            continue
        m = re.match(r"^(\s*(?:[-*]|\d+\.)\s+)?(.*)$", line)
        prefix, body = m.group(1) or "", m.group(2)
        kept = []
        for sent in _SENT.findall(body):
            if claim_ok(sent, by_id, cache):
                kept.append(sent)
            else:
                dropped.append(sent.strip())
        new = "".join(kept).strip()
        if new:
            out.append(prefix + new)
        elif not body.strip():
            out.append(line)
    return "\n".join(out), dropped


def dedupe_paragraphs(parts: list[str], min_len: int = 40) -> list[str]:
    """跨节去掉逐字重复的段落（背景节常整段抄后面的节）。短段、标题、表格不去。"""
    seen: set[str] = set()
    out = []
    for part in parts:
        paras = re.split(r"\n\s*\n", part)
        keep = []
        for p in paras:
            key = re.sub(r"\s+", "", p)
            if len(key) >= min_len and not p.lstrip().startswith(("#", "|")):
                if key in seen:
                    continue
                seen.add(key)
            keep.append(p)
        out.append("\n\n".join(keep))
    return out


def write_section(sec: Section, evs: list[Evidence], spec: TopicSpec, llm: LLM) -> str:
    if not evs:
        return f"（本节暂无入库证据）\n"
    paras, _ = target_length(len(evs))
    prompt = tagged("compile", (
        f"你在为方向「{spec.name}」写背景报告的一节：「{sec.title}」。本节有 {len(evs)} 篇证据，"
        f"写中文，最多约 {paras} 段；篇幅由证据里实际有的信息决定，信息少就写短，不要为凑篇幅重复或泛泛而谈，"
        "没有实质内容的证据可以不展开。\n"
        "只依据下面的证据（abstract 是摘要，其余是抽取字段）写，不要引入证据之外的事实。每个具体论断后面用 [id] 标注来源，"
        "id 原样照抄。数字只能照抄该 [id] 的摘要或抽取字段里的原数，不要换算、相减或估算；"
        "句中数字在所引证据里找不到的句子会被程序删掉。不同队列、人群或研究设计得到的数字不要直接比高低，"
        "要比较只比同一研究内部的对照。按方法/时间/子问题组织，对比不同工作的差异与争议，"
        "证据之间冲突要指出。关键结论、模型/数据集名称、核心数字用 **加粗**（每段 1-3 处，不要通篇加粗）。"
        "直接从正文开始，不要写「本节」「综上」「以下为」这类套话。\n\n"
        "【证据】\n" + json.dumps(_ev_rows(evs), ensure_ascii=False)))
    try:
        return strip_headings(llm.chat(prompt, task="compile", temperature=0.3, timeout=300))
    except Exception as exc:
        print(f"[compile] section {sec.id} failed: {exc}")
        return FAILED + "\n"


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
        "只引用清单里的 [id]，不要编造；不要大段复述已写正文（正文会原样出现在报告里），"
        "数字只照抄正文或清单里的原数，不要自己计算或跨研究比较。关键判断用 **加粗**。直接从正文开始，不要写「以下为…」之类的开场白。\n\n"
        "【证据清单】\n" + json.dumps(rows, ensure_ascii=False)[:12000] +
        "\n\n【已写正文】\n" + body[:16000]))
    try:
        return strip_headings(llm.chat(prompt, task="compile", temperature=0.3, timeout=300))
    except Exception as exc:
        print(f"[compile] synthesis {sec.id} failed: {exc}")
        return FAILED + "\n"


def write_tldr(spec: TopicSpec, body: str, llm: LLM) -> str:
    prompt = tagged("compile", (
        f"下面是方向「{spec.name}」背景报告的正文。请写 6-10 条 TL;DR 要点（中文，每条一句，"
        "保留 [id] 引用和数字，覆盖趋势/关键工作/数据/争议/空白）。数字与 [id] 必须和正文里的原句一致，"
        "不要把两句的数字合并到一条、不要换 [id]。只输出要点列表：\n\n" + body[:20000]))
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
             tldr: str, coverage: float, round_no: int, changelog: str = "",
             extra_sections: list[tuple[str, str]] | None = None, dropped_claims: int = 0) -> str:
    by_id = {e.id: e for e in evs}
    body_parts = []
    def emit(secs: list[Section], level: int):
        for s in secs:
            body_parts.append(f"{'#' * level} {s.id} {s.title}\n\n{sections_md.get(s.id, '')}")
            emit(s.children, level + 1)
    emit(outline.sections, 2)
    for title, md in (extra_sections or []):
        body_parts.append(f"## {title}\n\n{md}")
    body = "\n".join(dedupe_paragraphs(body_parts))
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
            f"证据 {len(evs)} 篇 · 覆盖度 {coverage:.2f} · 第 {round_no} 轮 · 更新 {date.today().isoformat()}"
            + (f" · 数字核验删句 {dropped_claims}" if dropped_claims else "") + "\n\n"
            + (f"## 本次变更\n\n{changelog}\n\n" if changelog else "")
            + (f"## 摘要（TL;DR）\n\n{tldr}\n" if tldr else ""))
    full = head + body + "\n## 参考文献\n\n" + "\n".join(refs) + "\n"
    return number_citations(full, order)


def compile_report(spec: TopicSpec, outline: Outline, evs: list[Evidence], llm: LLM,
                   coverage: float, round_no: int, changelog: str = "",
                   hist: list[dict] | None = None) -> str:
    by_id = {e.id: e for e in evs}
    sections_md = {}
    synth = []
    for s in outline.walk():
        sec_evs = [by_id[i] for i in s.evidence_ids if i in by_id]
        if is_synthesis(s, spec):
            synth.append(s)
            continue
        sections_md[s.id] = write_section(s, sec_evs, spec, llm) if (sec_evs or not s.children) else ""
    cache: dict = {}
    dropped: list[dict] = []

    def verify(key: str, text: str) -> str:
        if text.startswith(FAILED):
            return text
        kept, bad = check_claims(text, by_id, cache)
        dropped.extend({"part": key, "sentence": b} for b in bad)
        return kept

    sections_md = {k: verify(k, v) for k, v in sections_md.items()}
    body = "\n".join(sections_md.values())
    for s in synth:  # 综合节最后写，能看到全部正文
        sections_md[s.id] = verify(s.id, write_synthesis(s, spec, body, evs, llm))
    raw_tldr = write_tldr(spec, body, llm) if evs else ""
    tldr = verify("TL;DR", raw_tldr) if raw_tldr else ""
    from .stage import stage_section
    extra = [("阶段判断与行动建议", stage_section(spec, evs, outline, hist or [], llm))] if evs else []
    failed = [k for k, v in sections_md.items() if v.startswith(FAILED)] + \
             [k for k, v in extra if v.startswith(FAILED)] + (["TL;DR"] if evs and not raw_tldr else [])
    if failed:  # 残缺报告不发布：调用方保留上一版
        raise GenerationFailed(f"{spec.slug}: {len(failed)} parts failed ({', '.join(failed[:5])})")
    if dropped:
        print(f"[compile] claim check dropped {len(dropped)} sentences")
    try:
        (spec.dir / "claim_check.json").write_text(json.dumps(
            {"date": date.today().isoformat(), "dropped": dropped}, ensure_ascii=False, indent=1), encoding="utf-8")
    except OSError:
        pass
    return assemble(spec, outline, evs, sections_md, tldr, coverage, round_no, changelog, extra,
                    dropped_claims=len(dropped))
