from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass
class Item:
    id: str
    source: str   # arxiv / europepmc / semantic_scholar / huggingface / github / rss
    domain: str   # sources.yaml 里的 domain name
    title: str
    url: str
    authors: str = ""
    abstract: str = ""
    published: str = ""  # ISO date
    extra: dict = field(default_factory=dict)

    score: float = 0.0
    reason_zh: str = ""
    deepread: str = ""  # 深读环节产出的中文 markdown（空 = 未深读）

    def to_dict(self) -> dict:
        return asdict(self)
