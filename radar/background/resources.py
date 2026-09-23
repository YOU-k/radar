"""资源登记：从全部方向的证据库里挖真实、可获取、大规模的数据集 / 模型 / 基准。

流程：LLM 从每篇证据的 data / availability / summary 抽命名资源 → 按名字合并、统计被多少篇、多少个方向使用
→ 对 http 链接做可达性核验 → 按类型分表渲染。只有"有名字、有规模、有获取途径"的才收。
产物 background/_resources/registry.json + resources.md，站点「资源库」tab 排在最前。"""
from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import Callable

import requests

from .llmio import LLM, parse_json_array, tagged
from .models import Evidence
from .spec import BASE, TopicSpec, load_spec
from .store import EvidenceStore

RES_DIR_NAME = "_resources"
KINDS = ("dataset", "model", "benchmark", "database", "tool")
KIND_ZH = {"dataset": "数据集", "model": "模型", "benchmark": "基准", "database": "数据库", "tool": "工具"}
BATCH = 12


ALIASES = {  # 归一化后的别名 → 规范名（只放确定无歧义的）
    "ukb": "uk biobank", "ukbb": "uk biobank", "uk biobank ukb": "uk biobank", "uk biobank ukbb": "uk biobank",
    "all of us": "all of us research program", "aou": "all of us research program",
    "ukb ppp": "uk biobank pharma proteomics project", "uk biobank pharma proteomics project ukb ppp": "uk biobank pharma proteomics project",
    "mimic iv": "mimic-iv", "mimic iii": "mimic-iii", "czi cellxgene": "cellxgene", "cz cellxgene": "cellxgene",
    "tahoe 100m": "tahoe-100m", "gtex": "gtex", "tcga": "tcga", "geo": "gene expression omnibus",
}


def _norm(name: str) -> str:
    """去括号内容与版本号、小写、去标点；再查别名表。"""
    n = re.sub(r"\([^)]*\)", " ", name)
    n = re.sub(r"\b(v\d+(\.\d+)*|version \d+)\b", " ", n, flags=re.I)
    n = re.sub(r"[^a-z0-9]+", " ", n.lower()).strip()
    return ALIASES.get(n, n)


def is_core(r: dict) -> bool:
    """进主表的门槛：被 ≥2 篇工作用、或跨方向、或（开放 + 链接核验通过 + 有规模，且不是小工具）。"""
    if len(r.get("used_by", [])) >= 2 or len(r.get("topics", [])) >= 2:
        return True
    return (r.get("open") == "yes" and r.get("verified") == "ok" and bool(r.get("scale"))
            and r.get("kind") in ("dataset", "model", "database", "benchmark"))


def mine(evs: list[Evidence], topic_name: str, llm: LLM) -> list[dict]:
    rows_out: list[dict] = []
    for b in range(0, len(evs), BATCH):
        chunk = evs[b:b + BATCH]
        payload = [{"id": e.id, "title": e.candidate.title, "url": e.candidate.url,
                    "data": e.extraction.get("data", ""), "availability": e.extraction.get("availability", ""),
                    "summary": e.extraction.get("summary", "")[:300]} for e in chunk]
        prompt = tagged("resources", (
            f"这些文献属于方向「{topic_name}」。请从中识别**有名字、可获取、可复用**的资源：数据集 / 模型（含预训练权重）/ "
            "基准 / 数据库 / 工具。只收满足以下条件的：有正式名称（如 UK Biobank、Tahoe-100M、scGPT、CZ CELLxGENE）、"
            "规模或覆盖面明确、有公开获取途径（URL、GEO/Zenodo/HF 编号、门户）。"
            "不要收：泛称（'单细胞数据'）、未公开的私有队列、仅在文中提到但无获取途径的。\n"
            "每个资源输出：name（标准英文名）、kind（dataset/model/benchmark/database/tool）、modality（数据类型，≤15字中文）、"
            "scale（规模，如 50 万人 / 1 亿细胞 / 参数量，≤20字）、access（URL 或编号或门户名，没有写空）、"
            "open（yes/no/restricted/unknown）、used_by（文献 id 列表，原样抄）、note（一句话它被用来干什么）。\n\n"
            "【文献】\n" + json.dumps(payload, ensure_ascii=False) +
            '\n\n只输出 JSON 数组：[{"name":"...","kind":"dataset","modality":"...","scale":"...","access":"...",'
            '"open":"yes","used_by":["doi:..."],"note":"..."}]'))
        try:
            rows = parse_json_array(llm.chat(prompt, task="resources", temperature=0.1, timeout=240))
        except Exception as exc:
            print(f"[resources] batch {b // BATCH} failed: {exc}")
            rows = []
        ids = {e.id for e in chunk}
        for r in rows:
            name = str(r.get("name", "")).strip()
            kind = str(r.get("kind", "")).strip().lower()
            if not name or kind not in KINDS:
                continue
            rows_out.append({"name": name, "kind": kind, "modality": str(r.get("modality", ""))[:40],
                             "scale": str(r.get("scale", ""))[:40], "access": str(r.get("access", ""))[:200],
                             "open": str(r.get("open", "unknown")).lower(),
                             "used_by": [i for i in r.get("used_by", []) if i in ids],
                             "note": str(r.get("note", ""))[:120], "topics": [topic_name]})
    return rows_out


def merge(rows: list[dict], existing: dict | None = None) -> dict:
    """按归一化名字合并；被引证据、方向取并集；字段取更长的。"""
    reg = dict(existing or {})
    for r in rows:
        key = _norm(r["name"])
        if not key:
            continue
        cur = reg.get(key)
        if cur is None:
            reg[key] = {**r, "used_by": list(dict.fromkeys(r["used_by"])), "topics": list(r["topics"])}
            continue
        cur["used_by"] = list(dict.fromkeys(cur["used_by"] + r["used_by"]))
        cur["topics"] = list(dict.fromkeys(cur["topics"] + r["topics"]))
        for k in ("modality", "scale", "access", "note"):
            if len(r.get(k, "")) > len(cur.get(k, "")):
                cur[k] = r[k]
        if cur.get("open") in ("", "unknown") and r.get("open"):
            cur["open"] = r["open"]
    return reg


def _head(url: str, timeout: int = 15) -> int:
    r = requests.head(url, timeout=timeout, allow_redirects=True,
                      headers={"User-Agent": "radar-background/0.1"})
    if r.status_code in (403, 405):  # 有些站不许 HEAD
        r = requests.get(url, timeout=timeout, allow_redirects=True, stream=True,
                         headers={"User-Agent": "radar-background/0.1"})
    return r.status_code


def verify(reg: dict, head: Callable = _head) -> int:
    """对 http(s) 获取链接做可达性核验；非链接（编号/门户名）标 unverified。"""
    n = 0
    for r in reg.values():
        acc = r.get("access", "")
        m = re.search(r"https?://\S+", acc)
        if not m:
            r["verified"] = "n/a"
            continue
        try:
            code = head(m.group(0))
            r["verified"] = "ok" if code < 400 else ("blocked" if code in (401, 403, 429, 503) else "dead")
        except Exception:
            r["verified"] = "dead"
        n += 1
    return n


def render(reg: dict, day: date | None = None) -> str:
    day = day or date.today()
    all_rows = sorted(reg.values(), key=lambda r: (-len(r["topics"]), -len(r["used_by"]), r["name"].lower()))
    rows = [r for r in all_rows if is_core(r)]
    tail = [r for r in all_rows if not is_core(r)]
    out = [f"# 资源登记（数据集 / 模型 / 基准）\n",
           f"从 {sum(len(r['used_by']) for r in all_rows)} 处证据引用中挖出 {len(all_rows)} 项命名资源；"
           f"主表 {len(rows)} 项（被 ≥2 篇工作使用、或跨方向、或开放且链接核验通过且规模明确），"
           f"其余 {len(tail)} 项单篇提及的列在末尾。核验：ok 可达 / blocked 站点拒绝探测 / dead 失效 / n/a 非链接。更新 {day.isoformat()}\n"]
    for kind in KINDS:
        sub = [r for r in rows if r["kind"] == kind]
        if not sub:
            continue
        out.append(f"\n## {KIND_ZH[kind]}（{len(sub)}）\n")
        out.append("| 名称 | 模态 | 规模 | 获取 | 开放 | 核验 | 方向 | 证据 | 用途 |")
        out.append("|---|---|---|---|---|---|---|---|---|")
        for r in sub:
            acc = r.get("access", "")
            m = re.search(r"https?://\S+", acc)
            acc_md = f"[链接]({m.group(0)})" if m else acc
            out.append(f"| **{r['name']}** | {r.get('modality','')} | {r.get('scale','')} | {acc_md} | {r.get('open','')} | "
                       f"{r.get('verified','')} | {len(r['topics'])} | {len(r['used_by'])} | {r.get('note','')} |")
    if tail:
        out.append(f"\n## 单篇提及（{len(tail)}，未进主表）\n")
        by_kind: dict[str, list[str]] = {}
        for r in tail:
            by_kind.setdefault(r["kind"], []).append(r["name"])
        for kind in KINDS:
            if by_kind.get(kind):
                out.append(f"- {KIND_ZH[kind]}：" + "、".join(sorted(by_kind[kind])[:80]))
    return "\n".join(out) + "\n"


def run_resources(llm: LLM | None, root: Path | None = None, head: Callable = _head) -> Path:
    """llm=None：不重新挖，只用已有 registry.json 重新合并（别名归一）、核验、渲染。"""
    base = root or BASE
    out_dir = base / RES_DIR_NAME
    out_dir.mkdir(parents=True, exist_ok=True)
    rows: list[dict] = []
    reg_path = out_dir / "registry.json"
    if llm is None:
        if not reg_path.exists():
            raise SystemExit("[resources] 没有 registry.json，需要带 LLM 先挖一次")
        rows = list(json.loads(reg_path.read_text(encoding="utf-8")).values())
    else:
        for p in sorted(base.glob("*/topic.yaml")):
            if p.parent.name.startswith("_"):
                continue
            spec = load_spec(p)
            evs = EvidenceStore(spec.evidence_dir, spec.rejected_path).all()
            got = mine(evs, spec.name, llm)
            print(f"[resources] {spec.slug}: {len(got)} mentions from {len(evs)} evidence")
            rows += got
    reg = merge(rows)
    verify(reg, head)
    reg_path.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
    out = out_dir / "resources.md"
    out.write_text(render(reg), encoding="utf-8")
    print(f"[resources] {len(reg)} resources → {out}")
    return out
