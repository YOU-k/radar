"""日报 → 资源登记的收件箱（data/resources_inbox.json）。

以前这里维护一份独立的 /resources.md（"新发布资源" + "领域基础设施"），与 background/_resources 的登记表、
registry/*.md 手工清单三份并存、互不同步（2026-09 内容审计）。现在只保留一份登记表：
- 日报发现的新资源、周报用量挖掘出的基础设施，都写进收件箱，标 status=new（未核验）；
- 站点资源库把收件箱条目单列为"新发现 · 未核验"；
- 每周 `background resources` 把收件箱并入 registry.json（已登记的只记一次提及），再统一做种子覆盖与内容核验。
收件箱放在 data/ 下，是因为日报工作流只提交 digests/ 与 data/。

两个入口保持原名原签名（radar/run.py 调用）：
A. append_resources(items, day)：新论文自发布的数据集/模型，≥7 分进收件箱。不再调 LLM 补字段——
   规模/获取方式这类 LLM 猜测正是审计指出的错误来源，未核验条目只保留标题、链接和打分理由。
B. mine_infrastructure(recs, day)：从抽取记录聚合"每篇用了什么数据"，被 ≥2 篇高分工作使用的资源进收件箱。
"""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

from .. import llm, themes
from ..config import ROOT
from ..schema import Item

INBOX = ROOT / "data" / "resources_inbox.json"
LEGACY_MD = ROOT / "resources.md"
RESOURCE_KINDS = {"dataset", "model"}
MIN_SCORE = 7.0
KEEP_DAYS = 180


def is_resource(it: Item) -> bool:
    return it.extra.get("kind") in RESOURCE_KINDS


def load_inbox(path: Path | None = None) -> list[dict]:
    path = path or INBOX
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except (OSError, json.JSONDecodeError):
        return []


def save_inbox(entries: list[dict], day: date, path: Path | None = None) -> None:
    path = path or INBOX
    keep = [e for e in entries if not e.get("day") or (day - date.fromisoformat(e["day"])).days <= KEEP_DAYS]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(keep, ensure_ascii=False, indent=1), encoding="utf-8")


def _name_key(name: str) -> str:
    return re.sub(r"[^a-z0-9一-鿿]+", " ", name.lower()).strip()


def append_resources(items: list[Item], day: date) -> int:
    """通道 A：≥7 分、被打分判为 dataset/model 的新条目进收件箱（按 URL 去重）。返回新增条数。"""
    cand = [it for it in items if it.score >= MIN_SCORE and is_resource(it)]
    if not cand:
        return 0
    inbox = load_inbox()
    urls = {e.get("url") for e in inbox}
    added = 0
    for it in cand:
        if not it.url or it.url in urls:
            continue
        inbox.append({"name": " ".join(it.title.split())[:160], "kind": it.extra.get("kind"), "url": it.url,
                      "note": it.reason_zh[:160], "score": round(float(it.score), 1), "day": day.isoformat(),
                      "source": "daily", "theme": themes.for_domain(it.domain) or ""})
        urls.add(it.url)
        added += 1
    if added:
        save_inbox(inbox, day)
    return added


def mine_infrastructure(recs: list[dict], day: date) -> int:
    """通道 B：从抽取记录聚合"每篇用了什么数据"，被 ≥2 篇独立高分工作使用的资源进收件箱，附使用证据。

    recs: extract 模块的记录（需含 title / data 字段）。"""
    pool = [{"id": i, "title": r.get("title", ""), "data": r.get("data", "")}
            for i, r in enumerate(recs) if r.get("data")]
    if len(pool) < 3 or not llm.available():
        return 0
    prompt = (
        "下面是一批高分科研文献的标题和它们「训练/评测所用的数据」字段。"
        "请识别被 ≥2 篇独立文献使用的数据集 / 数据库 / 基准资源"
        "（如 Tahoe-100M、DepMap PRISM、TCGA 这类被反复使用的基础设施）。\n"
        "对每个资源输出：name（标准英文名）、"
        "usage（它被用来干什么，≤20字，如 扰动预测训练基准）、"
        "used_by（使用它的文献 id 列表，从输入抄）。\n"
        "只在单篇出现的自发布数据集不要收录；常识性小工具不要收录。\n\n"
        "【文献数据字段】\n" + json.dumps(pool, ensure_ascii=False)[:16000]
        + '\n\n只输出 JSON 数组，形如 [{"name":"...","usage":"...","used_by":[0,3]}]。'
    )
    try:
        content = llm.chat(prompt, model=llm.SCORE_MODEL, temperature=0.1, timeout=180)
        m = re.search(r"\[.*\]", content, re.DOTALL)
        rows = json.loads(m.group(0)) if m else []
    except Exception as exc:
        print(f"[resources] infrastructure mining failed: {exc}")
        return 0

    inbox = load_inbox()
    names = {_name_key(e.get("name", "")) for e in inbox}
    added = 0
    for r in rows:
        name = str(r.get("name", "")).strip()
        used = [pool[j]["title"] for j in r.get("used_by", [])
                if isinstance(j, int) and 0 <= j < len(pool)]
        if not name or len(used) < 2 or _name_key(name) in names:
            continue
        inbox.append({"name": name[:120], "kind": "dataset", "url": "",
                      "note": f"{str(r.get('usage', '')).strip()[:40]} · 被 {len(used)} 篇高分工作使用："
                              + " / ".join(t[:40] for t in used[:3]),
                      "day": day.isoformat(), "source": "daily-infra", "used_by_titles": used[:5]})
        names.add(_name_key(name))
        added += 1
    if added:
        save_inbox(inbox, day)
    return added


LEGACY_THEME = {"单细胞 / 空间组学": "singlecell", "衰老时钟 / 表观遗传": "aging", "人群队列 / 多模态": "cohort"}


def migrate_legacy_md(md_path: Path | None = None, inbox_path: Path | None = None, day: date | None = None) -> int:
    """一次性：把旧 /resources.md 的条目搬进收件箱（新发布资源带链接；基础设施只有名字）。返回搬入条数。"""
    md_path = md_path or LEGACY_MD
    if not md_path.exists():
        return 0
    inbox = load_inbox(inbox_path)
    urls = {e.get("url") for e in inbox if e.get("url")}
    names = {_name_key(e.get("name", "")) for e in inbox}
    added, section = 0, ""
    lines = md_path.read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines):
        if line.startswith("## "):
            section = line[3:].strip()
            continue
        nxt = lines[i + 1] if i + 1 < len(lines) and lines[i + 1].startswith("  ") else ""
        d = re.search(r"(\d{4}-\d{2}-\d{2})", nxt)
        m = re.match(r"^- \[(?P<t>.+?)\]\((?P<u>\S+)\) — (?P<v>.*)$", line)
        if m:
            if m.group("u") in urls:
                continue
            k = re.search(r"`(dataset|model)`", nxt)
            s = re.search(r"`([0-9.]+)` 分", nxt)
            inbox.append({"name": m.group("t")[:160], "kind": k.group(1) if k else "dataset", "url": m.group("u"),
                          "note": m.group("v")[:160], "score": float(s.group(1)) if s else None,
                          "day": d.group(1) if d else "", "source": "daily", "theme": LEGACY_THEME.get(section, ""),
                          "legacy_section": section})
            urls.add(m.group("u"))
            added += 1
            continue
        m = re.match(r"^- \*\*(?P<n>.+?)\*\* — (?P<v>.*)$", line)
        if m and _name_key(m.group("n")) not in names:
            inbox.append({"name": m.group("n")[:120], "kind": "dataset", "url": "",
                          "note": (m.group("v") + " · " + nxt.strip())[:200], "day": d.group(1) if d else "",
                          "source": "daily-infra", "legacy_section": section})
            names.add(_name_key(m.group("n")))
            added += 1
    save_inbox(inbox, day or date.today(), inbox_path)
    return added
