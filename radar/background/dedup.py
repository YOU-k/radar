"""去重：对照证据库 + 落选记录 + 本批内部；无 DOI 时按标题指纹。"""
from __future__ import annotations

from .models import Candidate, title_key
from .store import EvidenceStore


def merge_duplicates(cands: list[Candidate]) -> list[Candidate]:
    """本批内部合并：同 id 或同标题指纹的合并 found_by，保留信息更全的一条。"""
    by_key: dict[str, Candidate] = {}
    for c in cands:
        key = c.id if not c.id.startswith("eupmc:") else title_key(c.title)
        tkey = title_key(c.title)
        hit = by_key.get(key) or by_key.get("t:" + tkey)
        if hit is None:
            by_key[key] = c
            by_key["t:" + tkey] = c
            continue
        for tag in c.found_by:
            if tag not in hit.found_by:
                hit.found_by.append(tag)
        if len(c.abstract) > len(hit.abstract):
            hit.abstract = c.abstract
        if hit.citations is None and c.citations is not None:
            hit.citations = c.citations
        if not hit.venue and c.venue:
            hit.venue = c.venue
    out, seen = [], set()
    for c in by_key.values():
        if id(c) not in seen:
            seen.add(id(c))
            out.append(c)
    return out


def dedup(cands: list[Candidate], store: EvidenceStore) -> list[Candidate]:
    merged = merge_duplicates(cands)
    return [c for c in merged if not store.is_seen(c)]
