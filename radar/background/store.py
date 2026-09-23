"""证据库：唯一真源。每篇一个 JSON 文件；落选进 rejected.jsonl。

CorpusIndex 是全文检索索引的可选插件（PaperQA2 等），默认 NullIndex；
证据库本身不依赖它，所以测试和无 GPU 环境都能跑。"""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import Protocol

from .models import Candidate, Decision, Evidence, title_key


class CorpusIndex(Protocol):
    def add(self, ev: Evidence, text: str) -> None: ...
    def ask(self, question: str, k: int = 8) -> str: ...


class NullIndex:
    def add(self, ev: Evidence, text: str) -> None:
        return None

    def ask(self, question: str, k: int = 8) -> str:
        return ""


def _safe_name(eid: str) -> str:
    return re.sub(r"[^a-z0-9._-]+", "_", eid.lower())[:120] + ".json"


class EvidenceStore:
    def __init__(self, evidence_dir: Path, rejected_path: Path,
                 index: CorpusIndex | None = None):
        self.dir = Path(evidence_dir)
        self.rejected_path = Path(rejected_path)
        self.index = index or NullIndex()
        self.dir.mkdir(parents=True, exist_ok=True)

    # ---- 读 ----
    def ids(self) -> set[str]:
        return {self.get_by_path(p).id for p in self.dir.glob("*.json")}

    def get_by_path(self, p: Path) -> Evidence:
        return Evidence.from_dict(json.loads(p.read_text(encoding="utf-8")))

    def get(self, eid: str) -> Evidence | None:
        p = self.dir / _safe_name(eid)
        return self.get_by_path(p) if p.exists() else None

    def all(self) -> list[Evidence]:
        return sorted((self.get_by_path(p) for p in self.dir.glob("*.json")),
                      key=lambda e: (e.added_round, e.id))

    def title_keys(self) -> set[str]:
        return {title_key(e.candidate.title) for e in self.all()}

    def rejected(self) -> dict[str, dict]:
        out = {}
        if self.rejected_path.exists():
            for line in self.rejected_path.read_text(encoding="utf-8").splitlines():
                try:
                    d = json.loads(line)
                    out[d["candidate_id"]] = d
                except (json.JSONDecodeError, KeyError):
                    continue
        return out

    def is_seen(self, cand: Candidate) -> bool:
        return (cand.id in self.ids() or cand.id in self.rejected()
                or title_key(cand.title) in self.title_keys())

    # ---- 写 ----
    def add(self, ev: Evidence, fulltext: str = "") -> Path:
        if not ev.added_on:
            ev.added_on = date.today().isoformat()
        p = self.dir / _safe_name(ev.id)
        p.write_text(json.dumps(ev.to_dict(), ensure_ascii=False, indent=1),
                     encoding="utf-8")
        if fulltext:
            self.index.add(ev, fulltext)
        return p

    def update(self, ev: Evidence) -> Path:
        return self.add(ev)

    def reject(self, cand: Candidate, decision: Decision) -> None:
        rec = {"candidate_id": cand.id, "title": cand.title, "url": cand.url,
               "borderline": decision.borderline, "round": decision.round,
               "votes": [v.__dict__ for v in decision.votes],
               "day": date.today().isoformat()}
        self.rejected_path.parent.mkdir(parents=True, exist_ok=True)
        with self.rejected_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    def stats(self) -> dict:
        evs = self.all()
        rej = self.rejected()
        return {"evidence": len(evs), "rejected": len(rej),
                "borderline": sum(1 for r in rej.values() if r.get("borderline")),
                "with_fulltext": sum(1 for e in evs if e.fulltext_path),
                "venues": sorted({e.candidate.venue for e in evs if e.candidate.venue})}
