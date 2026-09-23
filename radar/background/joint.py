"""联合分析：跨方向的全景、交叉点与联合行动建议。

输入是各方向已编译报告里的 TL;DR、阶段判断段落和头部证据，不重新读论文。
产物 background/_joint/report.md，站点「方向背景」tab 排在最前。"""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

from .llmio import LLM, tagged
from .spec import BASE, TopicSpec, load_spec
from .store import EvidenceStore

JOINT_DIR_NAME = "_joint"


def _block(text: str, heading_prefix: str) -> str:
    """取 '## <heading_prefix>…' 到下一个二级标题之间的正文。"""
    m = re.search(rf"^## [^\n]*{re.escape(heading_prefix)}[^\n]*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    return m.group(1).strip() if m else ""


def topic_digest(spec: TopicSpec, max_top: int = 8) -> dict:
    rep = spec.report_path.read_text(encoding="utf-8") if spec.report_path.exists() else ""
    st = EvidenceStore(spec.evidence_dir, spec.rejected_path)
    evs = st.all()
    top = sorted(evs, key=lambda e: -(e.candidate.citations or 0))[:max_top]
    hist = json.loads(spec.metrics_path.read_text(encoding="utf-8")) if spec.metrics_path.exists() else []
    return {"slug": spec.slug, "name": spec.name, "n_evidence": len(evs),
            "coverage": hist[-1]["score"] if hist else None,
            "tldr": _block(rep, "摘要")[:3000],
            "stage": _block(rep, "阶段判断")[:3000],
            "top": [{"title": e.candidate.title[:90], "year": e.candidate.year,
                     "venue": e.candidate.venue} for e in top],
            "methods": sorted({e.extraction.get("method", "") for e in evs if e.extraction.get("method")})[:40],
            "data": sorted({e.extraction.get("data", "") for e in evs if e.extraction.get("data")})[:40]}


def joint_report(specs: list[TopicSpec], llm: LLM, resources_md: str = "") -> str:
    digests = [topic_digest(s) for s in specs]
    prompt = tagged("joint", (
        "你为一位提供算法支持的生物信息学博后（衰老 + 单细胞/PBMC + 药筛 + AI 方法；合作项目：类器官等多模态健康衰老模型，"
        "先用公共数据做 demo）做跨方向联合分析。下面是他维护的各方向背景报告的摘要、阶段判断、头部文献、方法与数据清单：\n"
        + json.dumps(digests, ensure_ascii=False)[:60000]
        + ("\n\n【已核验的共享资源（数据集/模型）】\n" + resources_md[:6000] if resources_md else "")
        + "\n\n请输出 markdown，章节固定：\n"
        "## 全景\n一张表：方向 | 阶段 | 证据数 | 一句话现状。\n"
        "## 方向间交叉点\n哪些方法、数据、问题同时出现在 ≥2 个方向（写明是哪几个方向、哪些具体工作），"
        "哪些方向的进展会直接改变另一方向的做法。\n"
        "## 联合行动建议\n3-5 个具体项目设想，每个：目标、用到的方向与具体方法/数据、为什么现在、预期产出（可发表点或合作交付）、主要风险。"
        "优先能与类器官 + 多组学合作项目结合、能先用公共数据做 demo 的。\n"
        "## 不要做的事\n2-3 条：看起来热但对他不划算的方向，给依据。\n"
        "关键判断用 **加粗**。只依据给定材料，引用文献时写「方向名：文献标题」。直接从表格开始。"))
    try:
        body = llm.chat(prompt, task="joint", temperature=0.3, timeout=400).strip()
    except Exception as exc:
        print(f"[joint] failed: {exc}")
        body = "（生成失败）"
    head = (f"# 联合分析 · 方向背景报告\n\n"
            f"{len(specs)} 个方向 · 证据 {sum(d['n_evidence'] for d in digests)} 篇 · 更新 {date.today().isoformat()}\n\n")
    return head + body + "\n"


def run_joint(llm: LLM, root: Path | None = None, resources_md: str = "") -> Path:
    base = root or BASE
    specs = [load_spec(p) for p in sorted(base.glob("*/topic.yaml")) if not p.parent.name.startswith("_")]
    specs = [s for s in specs if s.report_path.exists()]  # 还没 bootstrap 的方向不进联合分析
    out_dir = base / JOINT_DIR_NAME
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / "report.md"
    out.write_text(joint_report(specs, llm, resources_md), encoding="utf-8")
    return out
