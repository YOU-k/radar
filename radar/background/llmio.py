"""LLM 协议 + JSON 解析。区块只依赖 LLM 协议，测试注入 FakeLLM。

每个 prompt 以 [[TASK:<name>]] 开头：日志可读，FakeLLM 按它路由。"""
from __future__ import annotations

import json
import re
from typing import Protocol

from .. import llm as radar_llm


class LLM(Protocol):
    def chat(self, prompt: str, *, task: str = "", temperature: float = 0.2,
             timeout: int = 180) -> str: ...


class RadarLLM:
    """走 radar/llm.py（OpenAI 兼容端点）。task 决定模型档位。"""

    def __init__(self, cheap: str | None = None, strong: str | None = None):
        self.cheap = cheap or radar_llm.SCORE_MODEL
        self.strong = strong or radar_llm.SYNTH_MODEL

    def chat(self, prompt: str, *, task: str = "", temperature: float = 0.2,
             timeout: int = 180) -> str:
        model = self.strong if task in ("compile", "outline", "gap") else self.cheap
        return radar_llm.chat(prompt, model=model, temperature=temperature, timeout=timeout)


def available() -> bool:
    return radar_llm.available()


def tagged(task: str, body: str) -> str:
    return f"[[TASK:{task}]]\n{body}"


def task_of(prompt: str) -> str:
    m = re.match(r"\[\[TASK:([a-z_]+)\]\]", prompt)
    return m.group(1) if m else ""


def parse_json_array(text: str) -> list:
    m = re.search(r"\[.*\]", text, re.DOTALL)
    if not m:
        return []
    try:
        v = json.loads(m.group(0))
        return v if isinstance(v, list) else []
    except json.JSONDecodeError:
        return []


def parse_json_object(text: str) -> dict:
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if not m:
        return {}
    try:
        v = json.loads(m.group(0))
        return v if isinstance(v, dict) else {}
    except json.JSONDecodeError:
        return {}
