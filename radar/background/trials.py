"""试验状态表（config/trial_status.yaml）：给全局判断 / 联合分析的 [常识] 兜底。

DeepSeek 的领域知识停在训练截止，2025 年后读出的试验（ZEUS、Lp(a)HORIZON…）它不知道结果，
会继续当作支持性证据。这里把人工维护的状态表注入 prompt，并规定表外的 2025 年后试验不许断言结果。"""
from __future__ import annotations

from pathlib import Path

import yaml

from ..config import ROOT

PATH = ROOT / "config" / "trial_status.yaml"

RULE = ("【试验规则】涉及 2025 年之后读出或尚待读出的临床试验与监管事件，只能按下面的「试验状态表」陈述其状态、"
        "日期与结果，并在句末写（来源：试验状态表）；表里没有的 2025 年后试验不得断言其结果或读出时间，"
        "一律写「待核实」。状态表里已读出为阴性/失败的试验，不能再当作支持某条靶点或机制的证据。"
        "verified=否 的条目要写「未独立核实」。")


def load(path: Path | None = None) -> dict:
    p = path or PATH
    if not p.exists():
        return {}
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {}


def render(path: Path | None = None) -> str:
    """紧凑 markdown 表，直接拼进 prompt。表不存在返回空串。"""
    d = load(path)
    rows = d.get("trials") or []
    if not rows:
        return ""
    lines = [f"【试验状态表（截至 {d.get('as_of', '')}，config/trial_status.yaml 人工维护）】",
             "| 试验 | 药物 | 状态 | 日期 | 结果 | 已核实 | 来源 |", "|---|---|---|---|---|---|---|"]
    for t in rows:
        lines.append("| " + " | ".join(str(t.get(k, "") or "").replace("|", "/") for k in
                                        ("name", "drug", "status", "date", "result")) +
                     f" | {'是' if t.get('verified') else '否'} | {t.get('source', '')} |")
    return "\n".join(lines)


def prompt_block(path: Path | None = None) -> str:
    table = render(path)
    return f"{table}\n{RULE}" if table else ""
