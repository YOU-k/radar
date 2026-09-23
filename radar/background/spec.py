"""TopicSpec：一个方向的全部人工输入，来自 background/<slug>/topic.yaml。

新方向 = 写一份 topic.yaml，其余全自动。"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from ..config import ROOT

BASE = ROOT / "background"

DEFAULT_ROLES = [
    {"name": "bio",
     "label": "生物专家",
     "rubric": "科学价值与可复用性：方法是否有实质新意、数据/代码是否公开、是否与方向定义和纳入标准契合、"
               "结论是否有定量支撑。纯关联统计、无数据无代码的小样本工作投 no。"},
    {"name": "media",
     "label": "媒体专家",
     "rubric": "影响力与传播价值：发表载体（CNS 及子刊加分）、是否代表转折点而非增量、是否被产业/新闻/"
               "社区跟进或引用增长快、是否是该方向绕不开的'必读'。冷门增量工作投 no。"
               "注意：Nature/Cell/Science 及其子刊上的综述、评述属于方向背景必读，不要因'无数据无代码'投 no；"
               "通用方法在小众垂直领域（无线、语音、点云等）的套用不算影响力，投 no。"},
]

DEFAULT_BUDGET = {"rounds": 8, "max_candidates": 80, "max_screen": 60,
                  "max_extract": 40, "stop_delta": 0.02}


@dataclass
class TopicSpec:
    slug: str
    name: str
    definition: str = ""
    include: list[str] = field(default_factory=list)
    exclude: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    queries: list[str] = field(default_factory=list)
    journals: list[str] = field(default_factory=list)
    seeds: list[str] = field(default_factory=list)
    radar_domain: str = ""
    months: int = 24
    outline: list[dict] = field(default_factory=list)
    roles: list[dict] = field(default_factory=lambda: [dict(r) for r in DEFAULT_ROLES])
    budget: dict = field(default_factory=lambda: dict(DEFAULT_BUDGET))
    root: Path | None = None

    # ---- 路径约定：区块之间用这些路径交接 ----
    @property
    def dir(self) -> Path:
        return self.root or (BASE / self.slug)

    @property
    def evidence_dir(self) -> Path:
        return self.dir / "evidence"

    @property
    def cache_dir(self) -> Path:
        return self.dir / "cache"

    @property
    def rejected_path(self) -> Path:
        return self.dir / "rejected.jsonl"

    @property
    def outline_path(self) -> Path:
        return self.dir / "outline.md"

    @property
    def report_path(self) -> Path:
        return self.dir / "report.md"

    @property
    def log_path(self) -> Path:
        return self.dir / "log.md"

    @property
    def metrics_path(self) -> Path:
        return self.dir / "metrics.json"

    def profile_text(self) -> str:
        """给 LLM 看的方向画像（screen / gap / outline 共用）。"""
        inc = "\n".join(f"- {x}" for x in self.include) or "-（未写）"
        exc = "\n".join(f"- {x}" for x in self.exclude) or "-（未写）"
        return (f"方向：{self.name}\n定义：{self.definition}\n\n纳入标准：\n{inc}\n\n"
                f"排除标准：\n{exc}\n\n关键词：{', '.join(self.keywords)}")

    def validate(self) -> list[str]:
        errs = []
        if not self.slug or not self.slug.replace("-", "").isalnum():
            errs.append("slug 必须是小写字母/数字/连字符")
        if not self.name:
            errs.append("name 不能为空")
        if not (self.queries or self.keywords or self.seeds):
            errs.append("queries / keywords / seeds 至少填一个，否则无法检索")
        if not self.roles or len(self.roles) < 1:
            errs.append("roles 至少一个评审角色")
        for r in self.roles:
            if not r.get("name") or not r.get("rubric"):
                errs.append(f"role 缺 name 或 rubric: {r}")
        if self.budget.get("rounds", 0) < 1:
            errs.append("budget.rounds 必须 ≥1")
        return errs


def load_spec(slug_or_path: str | Path, root: Path | None = None) -> TopicSpec:
    p = Path(slug_or_path)
    if p.suffix != ".yaml":
        p = (root or BASE) / str(slug_or_path) / "topic.yaml"
    d = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    d.setdefault("slug", p.parent.name)
    roles = d.get("roles") or [dict(r) for r in DEFAULT_ROLES]
    budget = dict(DEFAULT_BUDGET)
    budget.update(d.get("budget") or {})
    spec = TopicSpec(
        slug=d["slug"], name=d.get("name", d["slug"]), definition=d.get("definition", ""),
        include=list(d.get("include") or []), exclude=list(d.get("exclude") or []),
        keywords=list(d.get("keywords") or []), queries=list(d.get("queries") or []),
        journals=list(d.get("journals") or []), seeds=list(d.get("seeds") or []),
        radar_domain=d.get("radar_domain", ""), months=int(d.get("months", 24)),
        outline=list(d.get("outline") or []), roles=roles, budget=budget,
        root=p.parent)
    errs = spec.validate()
    if errs:
        raise ValueError("topic.yaml 无效：" + "; ".join(errs))
    return spec


TEMPLATE = """# 方向定义（人改；其余文件由流水线生成）
name: {name}
definition: >
  一两句话说清这个方向是什么、边界在哪。
include:
  - 什么样的工作应该进来（方法/数据/规模/载体）
exclude:
  - 什么样的工作不要（纯关联、无数据、纯综述……）
keywords: []          # 标题/摘要粗筛用
queries: []           # EuropePMC / arXiv 检索词组（英文）
journals: []          # 整刊回溯的期刊（如 Nature, Nature Medicine）
seeds: []             # 必收文献 doi:... / arxiv:...，也是引用滚雪球的起点
radar_domain: ""      # 对应 sources.yaml 的 domain name，renew 时从日报接收条目
months: 24            # 回溯窗口
outline:              # 大纲骨架，流水线会在此基础上增删
  - title: 背景与定义
  - title: 方法学
  - title: 数据与资源
  - title: 应用与结果
  - title: 评测、争议与空白
budget:
  rounds: 8
  max_candidates: 80
  max_screen: 60
  max_extract: 40
  stop_delta: 0.02
"""


def init_topic(slug: str, name: str, root: Path | None = None) -> Path:
    d = (root or BASE) / slug
    d.mkdir(parents=True, exist_ok=True)
    p = d / "topic.yaml"
    if not p.exists():
        p.write_text(TEMPLATE.format(name=name), encoding="utf-8")
    (d / "evidence").mkdir(exist_ok=True)
    return p
