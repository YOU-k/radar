"""主题标签（config/themes.yaml）：日报、资源库、站点共用的颜色 tag。"""
from __future__ import annotations

from functools import lru_cache

import yaml

from .config import ROOT


@lru_cache(maxsize=1)
def load_themes() -> tuple[dict, ...]:
    p = ROOT / "config" / "themes.yaml"
    return tuple((yaml.safe_load(p.read_text(encoding="utf-8")) or {}).get("themes") or [])


def keys() -> list[str]:
    return [t["key"] for t in load_themes()]


def by_key() -> dict[str, dict]:
    return {t["key"]: t for t in load_themes()}


def by_label() -> dict[str, dict]:
    return {t["label"]: t for t in load_themes()}


def for_domain(domain: str) -> str:
    """日报 domain → 默认主题 key（没有对应就空）。"""
    for t in load_themes():
        if domain in (t.get("domains") or []):
            return t["key"]
    return ""


def for_topic(topic: str, topic_names: dict[str, str] | None = None) -> str:
    """方向 slug 或方向中文名 → 主题 key。topic_names: {方向中文名: slug}。"""
    slug = (topic_names or {}).get(topic, topic)
    for t in load_themes():
        if t.get("topic") == slug:
            return t["key"]
    return ""


def topic_names() -> dict[str, str]:
    """{方向中文名: slug}，从 background/*/topic.yaml 读。"""
    out = {}
    for p in sorted((ROOT / "background").glob("*/topic.yaml")):
        if p.parent.name.startswith("_"):
            continue
        d = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        out[d.get("name", p.parent.name)] = p.parent.name
    return out


def clean(tags, limit: int = 3) -> list[str]:
    """LLM 给的标签（key 或中文 label 都认）→ 去重、合法、限量的 key 列表。"""
    valid, labels = by_key(), by_label()
    out: list[str] = []
    for t in tags or []:
        t = str(t).strip().lstrip("#")
        k = t if t in valid else (labels[t]["key"] if t in labels else "")
        if k and k not in out:
            out.append(k)
    return out[:limit]


def prompt_list() -> str:
    return "；".join(f"{t['key']}={t['label']}（{t.get('hint', '')}）" for t in load_themes())


def line(keys_: list[str]) -> str:
    """digest 里的主题行正文：#心血管 #人群队列"""
    bk = by_key()
    return " ".join(f"#{bk[k]['label']}" for k in keys_ if k in bk)


def parse_line(text: str) -> list[str]:
    labels = by_label()
    return [labels[w[1:]]["key"] for w in text.split() if w.startswith("#") and w[1:] in labels]
