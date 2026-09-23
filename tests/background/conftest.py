"""共享夹具：FakeLLM 按 [[TASK:x]] 路由；临时 topic 目录；样例候选。"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from radar.background.llmio import task_of
from radar.background.models import Candidate
from radar.background.spec import TopicSpec, load_spec

TOPIC_YAML = """
name: 人群健康与多组学 AI
definition: 大规模队列/生物样本库上的生成式建模、疾病轨迹预测、人群多组学与遗传整合
include:
  - 大规模队列（UK Biobank 等）上的深度/生成式模型
  - 人群蛋白组/代谢组/甲基化 + 遗传整合
exclude:
  - 单中心小样本关联研究
keywords: [UK Biobank, biobank, disease trajectory, plasma proteome, generative model]
queries: ["UK Biobank deep learning", "disease trajectory generative"]
journals: [Nature, Nature Medicine]
seeds: ["doi:10.1038/s41586-025-09529-3", "doi:10.1038/s41586-026-10780-5"]
radar_domain: population_omics_ai
months: 24
outline:
  - title: 背景与定义
  - title: 方法学
    children:
      - title: 生成式疾病轨迹模型
      - title: 多组学与遗传整合
  - title: 数据与资源
  - title: 评测、争议与空白
budget: {rounds: 3, max_candidates: 50, max_screen: 20, max_extract: 10, stop_delta: 0.02}
"""


@pytest.fixture
def topic_dir(tmp_path: Path) -> Path:
    d = tmp_path / "population-omics-ai"
    d.mkdir()
    (d / "topic.yaml").write_text(TOPIC_YAML, encoding="utf-8")
    return d


@pytest.fixture
def spec(topic_dir: Path) -> TopicSpec:
    return load_spec(topic_dir / "topic.yaml")


def make_cand(i: int, *, doi: str | None = None, title: str | None = None, venue: str = "Nature",
              year: int = 2026, citations: int = 10, abstract: str = "", found_by: str = "test") -> Candidate:
    doi = doi or f"10.1000/paper{i}"
    return Candidate(id=f"doi:{doi}", title=title or f"Paper {i} on UK Biobank disease trajectory",
                     url=f"https://doi.org/{doi}", abstract=abstract or f"abstract {i} biobank",
                     venue=venue, year=year, citations=citations, found_by=[found_by])


@pytest.fixture
def cands() -> list[Candidate]:
    return [make_cand(i) for i in range(6)]


def _payload(prompt: str) -> list:
    """取 prompt 里【文献】块的 JSON 数组（不含末尾的格式示例）。"""
    m = re.search(r"【文献】\n(\[.*?\])\n\n只输出", prompt, re.DOTALL)
    return json.loads(m.group(1)) if m else []


class FakeLLM:
    """按任务标签返回可控 JSON。记录每次调用便于断言。
    screen 策略：默认所有角色对偶数 id 投 yes、奇数投 no；可用 votes 覆盖：{role: {i: 'yes'/'no'}}。
    """

    def __init__(self, votes: dict[str, dict[int, str]] | None = None, fail_tasks: set[str] | None = None,
                 outline_ops: list[dict] | None = None, revise_to: dict[str, dict[int, str]] | None = None):
        self.votes = votes or {}
        self.fail_tasks = fail_tasks or set()
        self.outline_ops = outline_ops
        self.revise_to = revise_to or {}
        self.calls: list[tuple[str, str]] = []

    def chat(self, prompt: str, *, task: str = "", temperature: float = 0.2, timeout: int = 180) -> str:
        t = task or task_of(prompt)
        self.calls.append((t, prompt))
        if t in self.fail_tasks:
            raise RuntimeError(f"fake failure for {t}")
        if t == "screen":
            return self._screen(prompt)
        if t == "extract":
            rows = _payload(prompt)
            return json.dumps([{"id": r["id"], "method": f"method-{r['id']}", "data": "UKB 400k",
                                "scenario": "risk", "benchmark": "Cox", "results": "AUC 0.8",
                                "availability": "code public", "limitations": "single cohort",
                                "summary": f"summary of {r['title']}"} for r in rows])
        if t == "outline":
            if self.outline_ops is not None:
                return json.dumps(self.outline_ops)
            ids = re.findall(r"^- (doi:\S+|arxiv:\S+)", prompt, re.M)
            return json.dumps([{"op": "attach", "section": "2.1", "ids": ids}])
        if t == "gap":
            return json.dumps({"queries": ["gap query one", "gap query two"], "journals": ["Nature"],
                               "focus": "补生成式疾病轨迹"})
        if t == "compile":
            ids = re.findall(r'"id": "((?:doi|arxiv|pmid):[^"]+)"', prompt)
            if "TL;DR" in prompt:
                return "- 要点一 [" + (ids[0] if ids else "doi:none") + "]\n- 要点二"
            return " ".join(f"论断 {i} [{eid}]." for i, eid in enumerate(ids)) + " 幻觉 [doi:10.9999/fake]."
        return "{}"

    def _screen(self, prompt: str) -> str:
        role = re.search(r"你是「(.+?)」", prompt).group(1)
        role_key = {"生物专家": "bio", "媒体专家": "media"}.get(role, role)
        rows = _payload(prompt)
        second = "第二轮" in prompt
        out = []
        for r in rows:
            i = r["id"]
            if second and role_key in self.revise_to and i in self.revise_to[role_key]:
                v = self.revise_to[role_key][i]
            elif role_key in self.votes and i in self.votes[role_key]:
                v = self.votes[role_key][i]
            else:
                v = "yes" if i % 2 == 0 else "no"
            out.append({"id": i, "vote": v, "reason": f"{role_key} says {v}"})
        return json.dumps(out)
