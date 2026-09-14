"""OpenAI 兼容 chat 客户端，全项目唯一 LLM 出口。

模型分层（均为 env 可配，默认 deepseek-chat）：
  SCORE_MODEL  每日打分（便宜档）
  DEEP_MODEL   高分论文深读
  SYNTH_MODEL  weekly / landscape 综合
"""
from __future__ import annotations

import os

import requests

from .config import llm_api_key

LLM_BASE = os.environ.get("LLM_BASE_URL") or "https://api.deepseek.com"
SCORE_MODEL = os.environ.get("SCORE_MODEL") or os.environ.get("LLM_MODEL") or "deepseek-chat"
DEEP_MODEL = os.environ.get("DEEP_MODEL") or os.environ.get("LLM_MODEL") or "deepseek-chat"
SYNTH_MODEL = os.environ.get("SYNTH_MODEL") or os.environ.get("LLM_MODEL") or "deepseek-chat"


def available() -> bool:
    return bool(llm_api_key())


def chat(prompt: str, *, model: str = SCORE_MODEL,
         temperature: float = 0.3, timeout: int = 300) -> str:
    key = llm_api_key()
    if not key:
        raise RuntimeError("no LLM api key (LLM_API_KEY / DEEPSEEK_API_KEY)")
    r = requests.post(
        f"{LLM_BASE}/chat/completions",
        headers={"Authorization": f"Bearer {key}",
                 "Content-Type": "application/json"},
        json={"model": model,
              "messages": [{"role": "user", "content": prompt}],
              "temperature": temperature},
        timeout=timeout,
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]
