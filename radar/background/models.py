"""数据契约：区块之间只传这些对象。全部可 JSON 往返。"""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from datetime import date

from ..schema import Item

_DOI = re.compile(r"10\.\d{4,9}/[^\s\"'<>]+", re.I)
_ARXIV = re.compile(r"(?:arxiv[:/]|abs/)(\d{4}\.\d{4,5})(?:v\d+)?", re.I)
_PMID = re.compile(r"(?:pmid[:/]|pubmed(?:\.ncbi\.nlm\.nih\.gov)?/)(\d{5,9})", re.I)


def normalize_id(raw: str = "", url: str = "") -> str:
    """统一成 doi:<小写> / arxiv:<id 去版本> / pmid:<n>；都没有则原样小写。"""
    for text in (raw, url):
        if not text:
            continue
        t = text.strip()
        m = _DOI.search(t)
        if m:
            return "doi:" + m.group(0).lower().rstrip(".,;)")
        m = _ARXIV.search(t)
        if m:
            return "arxiv:" + m.group(1)
        m = _PMID.search(t)
        if m:
            return "pmid:" + m.group(1)
    return (raw or url).strip().lower()


def title_key(title: str) -> str:
    """标题指纹：小写、去标点、前 12 个词。用于无 DOI 时的去重。"""
    words = re.sub(r"[^a-z0-9 ]", " ", title.lower()).split()
    return " ".join(words[:12])


@dataclass
class Candidate:
    id: str
    title: str
    url: str = ""
    abstract: str = ""
    authors: str = ""
    venue: str = ""
    year: int | None = None
    citations: int | None = None
    found_by: list[str] = field(default_factory=list)
    extra: dict = field(default_factory=dict)

    @classmethod
    def from_item(cls, it: Item, found_by: str) -> "Candidate":
        year = None
        if it.published and it.published[:4].isdigit():
            year = int(it.published[:4])
        return cls(id=normalize_id(it.id, it.url), title=it.title, url=it.url,
                   abstract=it.abstract or "", authors=it.authors or "",
                   venue=str(it.extra.get("journal", "") or ""), year=year,
                   found_by=[found_by],
                   extra={k: v for k, v in it.extra.items() if k != "journal"})

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "Candidate":
        return cls(**{k: d.get(k) for k in cls.__dataclass_fields__ if k in d})


@dataclass
class Vote:
    role: str
    vote: str          # "yes" | "no"
    reason: str = ""
    revised: bool = False

    @property
    def yes(self) -> bool:
        return self.vote == "yes"


@dataclass
class Decision:
    candidate_id: str
    votes: list[Vote]
    accepted: bool
    borderline: bool          # 有人 yes 但未全体通过
    round: int = 0

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Evidence:
    """证据库里的一条记录 = 通过评审的文献 + 抽取字段 + 挂载节点。"""
    candidate: Candidate
    panel: list[Vote]
    extraction: dict = field(default_factory=dict)
    sections: list[str] = field(default_factory=list)
    fulltext_path: str = ""
    added_round: int = 0
    added_on: str = ""

    @property
    def id(self) -> str:
        return self.candidate.id

    def to_dict(self) -> dict:
        return {"candidate": self.candidate.to_dict(),
                "panel": [asdict(v) for v in self.panel],
                "extraction": self.extraction, "sections": self.sections,
                "fulltext_path": self.fulltext_path,
                "added_round": self.added_round, "added_on": self.added_on}

    @classmethod
    def from_dict(cls, d: dict) -> "Evidence":
        return cls(candidate=Candidate.from_dict(d["candidate"]),
                   panel=[Vote(**v) for v in d.get("panel", [])],
                   extraction=d.get("extraction", {}), sections=d.get("sections", []),
                   fulltext_path=d.get("fulltext_path", ""),
                   added_round=d.get("added_round", 0), added_on=d.get("added_on", ""))


@dataclass
class DiscoveryPlan:
    """一轮检索计划：gap 区块产出，discover 区块消费。"""
    queries: list[str] = field(default_factory=list)
    journals: list[str] = field(default_factory=list)
    months: int = 24
    snowball_ids: list[str] = field(default_factory=list)
    focus: str = ""      # 本轮想补的缺口，写进日志

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class RoundLog:
    round: int
    focus: str
    n_candidates: int
    n_new: int
    n_accepted: int
    n_rejected: int
    n_borderline: int
    coverage: float
    note: str = ""
    day: str = field(default_factory=lambda: date.today().isoformat())

    def to_markdown(self) -> str:
        return (f"## 第 {self.round} 轮 · {self.day}\n\n"
                f"- 缺口：{self.focus or '（冷启动）'}\n"
                f"- 候选 {self.n_candidates} → 新 {self.n_new} → 入库 {self.n_accepted}，"
                f"拒 {self.n_rejected}（边缘 {self.n_borderline}）\n"
                f"- 覆盖度：{self.coverage:.3f}\n"
                + (f"- 备注：{self.note}\n" if self.note else "") + "\n")
