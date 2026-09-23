"""覆盖度：种子命中 ×0.3 + 子题饱和（≥3 篇证据的节占比）×0.3 + 高引覆盖 ×0.4。

高引列表由 discover 阶段的 S2 结果给（该方向被发现的候选里引用最高的 N 篇），
没有就退化为前两项归一。"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .outline import Outline, UNSORTED
from .spec import TopicSpec
from .store import EvidenceStore


@dataclass
class Coverage:
    seed_hit: float
    saturation: float
    highcite: float
    score: float
    n_evidence: int
    round: int


def coverage(spec: TopicSpec, store: EvidenceStore, outline: Outline,
             top_cited: list[str] | None, round_no: int) -> Coverage:
    ids = store.all_ids()
    seeds = [s.lower() for s in spec.seeds]
    seed_hit = (sum(1 for s in seeds if s in ids) / len(seeds)) if seeds else 1.0
    leaves = [s for s in outline.walk() if not s.children and s.title != UNSORTED]
    sat = (sum(1 for s in leaves if len(s.evidence_ids) >= 3) / len(leaves)) if leaves else 0.0
    if top_cited:
        hc = sum(1 for t in top_cited if t in ids) / len(top_cited)
        score = 0.3 * seed_hit + 0.3 * sat + 0.4 * hc
    else:
        hc = 0.0
        score = 0.5 * seed_hit + 0.5 * sat
    return Coverage(round(seed_hit, 3), round(sat, 3), round(hc, 3), round(score, 3),
                    len(ids), round_no)


def append_metrics(path: Path, cov: Coverage) -> list[dict]:
    hist = json.loads(path.read_text(encoding="utf-8")) if path.exists() else []
    hist.append(asdict(cov))
    path.write_text(json.dumps(hist, ensure_ascii=False, indent=1), encoding="utf-8")
    return hist


def should_stop(hist: list[dict], delta: float) -> bool:
    """连续两轮提升都小于 delta 则停。"""
    if len(hist) < 3:
        return False
    s = [h["score"] for h in hist[-3:]]
    return (s[1] - s[0]) < delta and (s[2] - s[1]) < delta
