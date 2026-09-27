"""全局判断：从第一性原理看各方向——在问什么生物学问题、卡在因果链哪一层、现有角度为什么成立、还有哪些研究策略。

方向报告是自下而上的证据综述（检索 → 评审 → 抽取 → 按节编译），天然只回答"大家在做什么"。
这里补自上而下的一层：每个方向一次推理（方向定义 + 报告摘要 + 阶段判断 + 头部文献作为证据，
加模型自身的领域常识，两者分开标注），最后一次跨方向综合。产物 background/_principles/report.md，
站点「方向背景」tab 置顶。领域格局变化慢，放月度任务跑。

[证据] 只取自通过数字核验的 TL;DR 句子（joint.topic_digest 已过滤）；阶段判断标为雷达检索统计。
[常识] 受 config/trial_status.yaml 约束：2025 年后读出的试验只能按状态表写，表外的写「待核实」。"""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

from . import trials
from .joint import topic_digest
from .llmio import LLM, tagged
from .spec import BASE, TopicSpec, load_spec

DIR_NAME = "_principles"
CHAIN = "遗传变异 → 分子（转录/蛋白/代谢） → 细胞状态 → 组织/器官 → 个体表型与疾病 → 人群 → 干预与转化"

TOPIC_SECTIONS = """### 这个领域真正想回答的生物学问题
2-4 个，写成可证伪、可被实验或数据回答的问题（不是"建一个更好的模型"）。

### 卡在因果链的哪一层
因果链：{chain}。判断当前主要瓶颈属于哪一类：靶点与机制未知 / 测量手段不足 / 数据规模或多样性不足 / 因果识别不足 / 转化与落地（干预时机、人群、成本）。
逐条给依据；不同疾病或子问题瓶颈不同就分开说，不要一概而论。

### 主流研究角度为什么成立、在哪里失效
对应材料里的主流做法（如大队列关联建模、基础模型、扰动预测），说清它隐含的假设、能回答到哪一层、回答不了什么。

### 被低估的其他研究策略
3-5 个，每个写具体：用什么系统（人群 / 遗传 / 类器官 / 模式生物 / 临床试验设计…）、什么扰动或自然实验、什么读出、为什么能打破上面的瓶颈、有无代表性工作。

### 对他的含义
作为算法提供者，在哪一层能做出不可替代的贡献；哪些问题算法帮不上、必须靠实验或临床设计。"""


def _profile() -> str:
    try:
        from ..config import load_profile
        return load_profile()[:5000]
    except Exception:
        return ""


def topic_view(spec: TopicSpec, llm: LLM) -> str:
    d = topic_digest(spec, max_top=12)
    material = {"方向": spec.name, "定义": spec.definition, "纳入范围": spec.include,
                "报告摘要（已通过数字核验，[证据] 只能取自这里）": d["tldr"],
                "阶段判断（雷达检索统计，非领域属性）": d["stage"], "头部文献": d["top"]}
    prompt = tagged("principles", (
        "你是这个领域资深的 PI，要给一位做算法支持的生物信息学博后讲清楚这个领域的**底层逻辑**，而不是复述文献。"
        "从第一性原理出发：疾病/生命现象的因果结构是什么，今天的研究为什么这样做，还缺什么。\n\n"
        f"【他的研究画像】\n{_profile()}\n\n【该方向的证据材料（来自他的方向背景报告）】\n"
        + json.dumps(material, ensure_ascii=False)[:14000]
        + "\n\n按以下固定小节输出 markdown（直接从第一个小节开始，不要写方向名标题）：\n"
        + TOPIC_SECTIONS.format(chain=CHAIN)
        + ("\n\n" + trials.prompt_block() if trials.prompt_block() else "")
        + "\n\n规则：依据上面「报告摘要」的判断在句末标 [证据]，带数字的 [证据] 句只能照抄报告摘要里的原数，"
          "不要把阶段判断里的篇数、占比当作 [证据]；依据你自身领域知识的判断标 [常识]，"
          "常识必须具体（写出靶点、药物、试验名、机制、代表性数据集），拿不准的写「待核实」。"
          "关键判断用 **加粗**。总长 900-1400 字。"))
    return llm.chat(prompt, task="principles", temperature=0.3, timeout=600).strip()


def synthesis(views: dict[str, str], llm: LLM) -> str:
    joined = "\n\n".join(f"【{name}】\n{v[:3500]}" for name, v in views.items())
    prompt = tagged("principles", (
        "下面是同一位研究者关注的各领域的第一性原理分析。请做跨领域的全局判断，给他一张地图。\n\n"
        f"【他的研究画像】\n{_profile()}\n\n{joined[:40000]}\n\n"
        + (trials.prompt_block() + "\n\n" if trials.prompt_block() else "") +
        "输出 markdown，固定章节：\n"
        "## 总判断\n一张表：领域 | 核心生物学问题（一句） | 主要瓶颈层（因果链上的哪一层 + 瓶颈类型） | 主流角度的盲点 | 最值得补的策略。每个领域一行。\n"
        "## 跨领域的共同规律\n3-5 条贯穿多个领域的底层规律（例如：关联到因果的鸿沟、测量先于建模、扰动是因果的硬通货、人群异质性），每条点名涉及的领域与具体例子。\n"
        "## 研究策略地图\n一张表：策略（人类遗传学/MR、天然扰动与准实验、类器官/iPSC 扰动筛选、模式生物、纵向深表型队列、实用性试验与真实世界、基础模型与表征学习 等）"
        "× 它最能打破哪个领域的哪个瓶颈 × 数据/成本门槛 × 他能否先用公共数据起步。\n"
        "## 如果只做一件事\n结合他的应用线，给出一个最该押注的研究问题（不是方法），说明为什么是它、第一步做什么。\n\n"
        "规则：沿用各领域分析里的 [证据] / [常识] 标注；关键判断 **加粗**；直接从「## 总判断」开始。"))
    return llm.chat(prompt, task="principles", temperature=0.3, timeout=600).strip()


def _strip_heading(text: str) -> str:
    return re.sub(r"\A#{1,3} [^\n]*\n+", "", text)


def principles_report(specs: list[TopicSpec], llm: LLM) -> str:
    views: dict[str, str] = {}
    for spec in specs:
        try:
            views[spec.name] = _strip_heading(topic_view(spec, llm))
            print(f"[principles] {spec.slug} done")
        except Exception as exc:
            print(f"[principles] {spec.slug} failed: {exc}")
    from .llmio import GenerationFailed
    if len(views) < len(specs):  # 任一领域失败就不发布残缺版本，保留上月的
        raise GenerationFailed(f"principles: {len(specs) - len(views)} topic views failed")
    try:
        top = synthesis(views, llm)
    except Exception as exc:
        raise GenerationFailed(f"principles synthesis: {exc}") from exc
    head = (f"# 全局判断：从第一性原理看各领域 · 方向背景报告\n\n"
            f"{len(views)} 个领域 · 每月更新 · 更新 {date.today().isoformat()} · "
            "[证据] = 来自方向背景报告；[常识] = 模型领域知识，需核实\n\n")
    parts = [head, top.strip(), "\n\n## 分领域分析\n"]
    for name, v in views.items():
        parts.append(f"\n### {name}\n\n" + re.sub(r"^### ", "#### ", v, flags=re.M) + "\n")
    return "".join(parts)


def run_principles(llm: LLM, root: Path | None = None) -> Path:
    base = root or BASE
    specs = [load_spec(p) for p in sorted(base.glob("*/topic.yaml")) if not p.parent.name.startswith("_")]
    specs = [s for s in specs if s.report_path.exists()]
    out_dir = base / DIR_NAME
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "report.md"
    out.write_text(principles_report(specs, llm), encoding="utf-8")
    return out
