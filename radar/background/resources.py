"""资源登记：从全部方向的证据库里挖真实、可获取、大规模的数据集 / 模型 / 基准。

流程：LLM 从每篇证据的 data / availability / summary 抽命名资源 → 按名字（+ 别名表 / 拆分表）合并、
统计被多少篇、多少个方向使用 → 人工种子（config/resource_seeds.yaml）覆盖规模 / 获取 / 开放性并置顶画像点名的资源
→ 并入日报收件箱（data/resources_inbox.json，标"新发现 · 未核验"）→ 按内容核验链接 → 渲染。
产物 background/_resources/registry.json + resources.md，站点「资源库」tab 展示。

2026-09 审计后的规则：
- 规模以种子为准；非种子的规模来自某篇引用文献（scale_src=paper），站点注明"据文献"。
- 开放性默认 unknown：只有种子声明，或 LLM 说 yes 且链接指向代码/数据仓库（GitHub/HF/Zenodo…）并核验通过，才算公开。
  LLM 的原始判断保存在 open_claim。
- 链接核验看内容：浏览器 UA 取页面，标题或正文须出现资源名/别名（DOI 先查 Crossref 标题摘要）；
  ok 通过 / mismatch 页面在但不是这个资源 / blocked 站点拒绝或超时，无法判断 / dead 404、域名失效。
- 画像点名的资源（ChinaHEART、CKB、China-PAR、PCE、Delphi-2M、ALADYNOULLI、PhenoAge/GrimAge、LongevityBench）
  在种子里 pin 到 P0/P1，无论被引几次都进主表，LLM 重排不动它们。
"""
from __future__ import annotations

import json
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path
from typing import Callable

import requests

from .llmio import LLM, parse_json_array, tagged
from .models import Evidence
from .spec import BASE, load_spec
from .store import EvidenceStore

RES_DIR_NAME = "_resources"
KINDS = ("dataset", "model", "benchmark", "database", "tool")
KIND_ZH = {"dataset": "数据集", "model": "模型", "benchmark": "基准", "database": "数据库", "tool": "工具"}
OPEN_VALUES = ("yes", "partial", "registration", "controlled", "commercial", "no", "unknown")
OPEN_ZH = {"yes": "公开", "partial": "部分公开", "registration": "注册即可", "controlled": "受控申请",
           "commercial": "商业", "no": "不公开", "unknown": "开放性未确认"}
VERIFIED_ZH = {"ok": "链接已核验", "mismatch": "链接可能指错", "blocked": "站点拒绝探测", "dead": "链接失效",
               "n/a": "无链接", "unverified": "未核验"}
BATCH = 12

ALIASES = {  # 归一化后的别名 → 规范名（只放确定无歧义的；更多别名在种子文件里）
    "ukb": "uk biobank", "ukbb": "uk biobank", "uk biobank ukb": "uk biobank", "uk biobank ukbb": "uk biobank",
    "all of us": "all of us research program", "aou": "all of us research program",
    "ukb ppp": "uk biobank pharma proteomics project", "uk biobank pharma proteomics project ukb ppp": "uk biobank pharma proteomics project",
    "mimic iv": "mimic-iv", "mimic iii": "mimic-iii", "czi cellxgene": "cellxgene", "cz cellxgene": "cellxgene",
    "tahoe 100m": "tahoe-100m", "gtex": "gtex", "tcga": "tcga", "geo": "gene expression omnibus",
}

# 这些站点上的链接指向的就是代码 / 权重 / 数据本身；只有这类链接核验通过，LLM 说的"公开"才采信
DATA_HOSTS = ("github.com", "gitlab.com", "huggingface.co", "zenodo.org", "figshare.com", "datadryad.org",
              "osf.io", "kaggle.com", "bioconductor.org", "cran.r-project.org", "pypi.org",
              "ncbi.nlm.nih.gov/geo", "ebi.ac.uk", "physionet.org/content", "synapse.org", "cellxgene.cziscience.com")
BROWSER_HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/126.0 Safari/537.36"),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8",
}
_CHALLENGE = re.compile(r"just a moment\.\.\.|cf-chl|captcha|are you a robot|access denied|enable javascript and cookies",
                        re.I)
_DOI = re.compile(r"(?:doi\.org/|doi:\s*)(10\.\d{4,9}/[^\s\"<>]+)", re.I)


def _base_norm(name: str) -> str:
    n = re.sub(r"\([^)]*\)", " ", name)
    n = re.sub(r"\b(v\d+(\.\d+)*|version \d+)\b", " ", n, flags=re.I)
    return re.sub(r"[^a-z0-9]+", " ", n.lower()).strip()


def _norm(name: str, aliases: dict[str, str] | None = None) -> str:
    """去括号内容与版本号、小写、去标点；再查别名表（内置 + 种子）。"""
    n = _base_norm(name)
    if aliases and n in aliases:
        return aliases[n]
    return ALIASES.get(n, n)


def _raw_key(name: str) -> str:
    """拆分目标用：保留括号内容，避免 'DISCO (a)' 与 'DISCO (b)' 归一成同一个键。"""
    return re.sub(r"[^a-z0-9]+", " ", name.lower()).strip()


# ---------------- 种子 ----------------

def seeds_path(root: Path | None = None) -> Path:
    return (root or BASE).parent / "config" / "resource_seeds.yaml"


def load_seeds(path: Path | None = None) -> dict:
    """→ {"resources": {key: seed}, "aliases": {归一化别名: key}, "split": {key: {kind: 名}}, "exclude": {key}}。
    文件不存在返回空种子（测试 / 其他项目复用时）。"""
    empty = {"resources": {}, "aliases": {}, "split": {}, "exclude": set()}
    path = path or seeds_path()
    if not path.exists():
        return empty
    import yaml
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    out = {"resources": {}, "aliases": {}, "split": {}, "exclude": set()}
    for s in raw.get("resources") or []:
        if isinstance(s.get("open"), bool):  # YAML 1.1 把 yes/no 读成布尔
            s["open"] = "yes" if s["open"] else "no"
        key = _norm(s["name"])
        out["resources"][key] = s
        for a in [s["name"]] + list(s.get("aliases") or []):
            out["aliases"][_base_norm(a)] = key
    for a, canon in (raw.get("aliases") or {}).items():
        out["aliases"][_base_norm(a)] = _norm(canon, out["aliases"])
    for name, by_kind in (raw.get("split") or {}).items():
        out["split"][_base_norm(name)] = dict(by_kind)
    out["exclude"] = {_base_norm(x) for x in raw.get("exclude") or []}
    return out


def resolve_key(name: str, kind: str = "", seeds: dict | None = None) -> tuple[str, str]:
    """(registry 键, 显示名)。拆分表优先（同名异物按 kind 拆开），再走别名表；排除表返回 ("", "")。"""
    seeds = seeds or {}
    base = _base_norm(name)
    if base in seeds.get("exclude", ()):
        return "", ""
    split = seeds.get("split", {}).get(base)
    if split and kind in split:
        return _raw_key(split[kind]), split[kind]
    return _norm(name, seeds.get("aliases")), name


def is_core(r: dict) -> bool:
    """进主表的门槛：种子 / 置顶；或被 ≥2 篇工作用、或跨方向、或（开放 + 链接核验通过 + 有规模，且不是小工具）。
    日报收件箱来的新条目（status=new）不进主表，站点单独列"新发现 · 未核验"。"""
    if r.get("pinned") or r.get("seed"):
        return True
    if r.get("status") == "new":
        return False
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


def merge(rows: list[dict], existing: dict | None = None, seeds: dict | None = None) -> dict:
    """按归一化名字（+ 种子别名 / 拆分 / 排除）合并；被引证据、方向取并集；描述字段取更长的；
    各行的开放性判断收进 open_claim（第一个非 unknown 的），最终 open 由 finalize_open 决定。"""
    reg = dict(existing or {})
    for r in rows:
        key, name = resolve_key(r["name"], r.get("kind", ""), seeds)
        if not key:
            continue
        claim = r.get("open_claim") or r.get("open") or "unknown"
        cur = reg.get(key)
        if cur is None:
            reg[key] = {**r, "name": name, "used_by": list(dict.fromkeys(r.get("used_by", []))),
                        "topics": list(r.get("topics", [])), "open_claim": claim}
            continue
        cur["used_by"] = list(dict.fromkeys(cur.get("used_by", []) + r.get("used_by", [])))
        cur["topics"] = list(dict.fromkeys(cur.get("topics", []) + r.get("topics", [])))
        for k in ("modality", "scale", "access", "note"):
            if len(r.get(k, "")) > len(cur.get(k, "")):
                cur[k] = r[k]
        if cur.get("open_claim") in (None, "", "unknown") and claim:
            cur["open_claim"] = claim
        if cur.get("open") in (None, "", "unknown") and r.get("open"):
            cur["open"] = r["open"]
    return reg


def fold_inbox(reg: dict, inbox: list[dict], seeds: dict | None = None) -> int:
    """日报收件箱（pipeline/resources.py 写入）→ registry：已登记的只记一次日报提及；
    新的以 status=new（未核验）进 registry，不进主表。返回新增条数。"""
    added = 0
    for e in inbox:
        key, name = resolve_key(e.get("name", ""), e.get("kind", ""), seeds)
        if not key:
            continue
        url = e.get("url", "")
        cur = reg.get(key)
        if cur is not None:
            if url and url not in cur.setdefault("daily_urls", []):
                cur["daily_urls"].append(url)
            continue
        reg[key] = {"name": name, "kind": e.get("kind") if e.get("kind") in KINDS else "dataset",
                    "modality": "", "scale": "", "access": url, "open_claim": "unknown", "used_by": [],
                    "topics": [], "note": e.get("note", "")[:160], "status": "new", "source": e.get("source", "daily"),
                    "added": e.get("day", ""), "themes_fixed": [t for t in [e.get("theme", "")] if t]}
        added += 1
    return added


def apply_seeds(reg: dict, seeds: dict) -> int:
    """种子覆盖：规范名 / kind / 模态 / 规模 / 获取 / 开放性 / 主题 / 置顶。种子条目即使没被证据引用也加进来。"""
    n = 0
    for key, s in seeds.get("resources", {}).items():
        r = reg.setdefault(key, {"name": s["name"], "kind": s.get("kind", "dataset"), "modality": "", "scale": "",
                                 "access": "", "used_by": [], "topics": [], "note": "", "open_claim": "unknown"})
        r["name"] = s["name"]
        r["seed"] = True
        r.pop("status", None)
        if s.get("kind") in KINDS:
            r["kind"] = s["kind"]
        for f in ("modality", "scale", "access"):
            if f in s:
                r[f] = s[f] or ""
        if s.get("scale"):
            r["scale_src"] = "seed"
        if s.get("open") in OPEN_VALUES:
            r["open"] = r["open_seed"] = s["open"]
        r["aliases"] = list(s.get("aliases") or [])
        if s.get("match"):
            r["match"] = list(s["match"])
        r["themes_fixed"] = list(dict.fromkeys(list(r.get("themes_fixed") or []) + list(s.get("themes") or [])))
        if s.get("pin") in ("P0", "P1"):
            r["priority"], r["pinned"] = s["pin"], True
            if s.get("why"):
                r["why"] = s["why"]
        n += 1
    for r in reg.values():  # 非种子的规模来自某篇引用文献
        if r.get("scale") and r.get("scale_src") != "seed":
            r["scale_src"] = "paper"
    return n


def _is_data_host(url: str) -> bool:
    u = re.sub(r"^https?://(www\.)?", "", url.lower())
    return any(u.startswith(h) or u.startswith("www." + h) for h in DATA_HOSTS)


def finalize_open(reg: dict) -> None:
    """默认 unknown，除非确认：种子声明，或 LLM 说 yes 且链接是代码/数据仓库并核验通过。"""
    for r in reg.values():
        if r.get("open_seed"):
            r["open"] = r["open_seed"]
            continue
        claim = r.get("open_claim") or r.get("open") or "unknown"
        r["open_claim"] = claim
        m = re.search(r"https?://\S+", r.get("access", ""))
        confirmed = claim == "yes" and m and _is_data_host(m.group(0)) and r.get("verified") == "ok"
        r["open"] = "yes" if confirmed else "unknown"


# ---------------- 链接核验 ----------------

def _fetch(url: str, timeout: int = 20) -> tuple[int, str]:
    """浏览器 UA GET，最多读 400 KB 文本。"""
    r = requests.get(url, timeout=timeout, allow_redirects=True, stream=True, headers=BROWSER_HEADERS)
    chunks, size = [], 0
    for c in r.iter_content(65536):
        chunks.append(c)
        size += len(c)
        if size > 400_000:
            break
    r.close()
    enc = r.encoding or "utf-8"
    return r.status_code, b"".join(chunks).decode(enc, errors="replace")


def _head(url: str, timeout: int = 15) -> int:
    """旧的只看状态码的探测（保留给调用方注入 head= 的兼容路径）。"""
    r = requests.head(url, timeout=timeout, allow_redirects=True, headers=BROWSER_HEADERS)
    if r.status_code in (403, 405):
        r = requests.get(url, timeout=timeout, allow_redirects=True, stream=True, headers=BROWSER_HEADERS)
    return r.status_code


def _text_norm(s: str) -> str:
    return " " + re.sub(r"[^a-z0-9一-鿿]+", " ", s.lower()).strip() + " "


def needles(r: dict) -> list[str]:
    """页面里应该出现的字符串：名称（含去括号版与括号内缩写）、别名、种子 match。太短的（<3）不用。"""
    names = [r.get("name", "")] + list(r.get("aliases") or []) + list(r.get("match") or [])
    out = []
    for n in names:
        for v in (n, re.sub(r"\([^)]*\)", " ", n), *re.findall(r"\(([^)]*)\)", n)):
            t = _text_norm(v).strip()
            if len(t) >= 3 and t not in out:
                out.append(t)
    # "ImageNet-1k" / "Tahoe-100M"：主名 + 短后缀，页面上常只写主名
    toks = _text_norm(re.sub(r"\([^)]*\)", " ", r.get("name", ""))).split()
    if len(toks) >= 2 and len(toks[0]) >= 5 and all(len(t) <= 3 for t in toks[1:]) and toks[0] not in out:
        out.append(toks[0])
    return out


def _mentions(text: str, ns: list[str]) -> bool:
    hay = _text_norm(text)
    return any(f" {n} " in hay for n in ns)


def check_link(r: dict, url: str, fetch: Callable[[str], tuple[int, str]] = _fetch) -> str:
    """→ ok / mismatch / blocked / dead。DOI 先查 Crossref（出版社页常拒绝机器人）。"""
    ns = needles(r)
    m = _DOI.search(url)
    if m:
        doi = m.group(1).rstrip(").,;")
        try:
            # Crossref 404 不等于 DOI 失效（arXiv / Zenodo 的 DOI 在 DataCite），交给下面的页面判断
            code, body = fetch(f"https://api.crossref.org/works/{doi}")
            if code == 200:
                msg = json.loads(body).get("message", {})
                meta = " ".join(msg.get("title") or []) + " " + " ".join(msg.get("subtitle") or []) + " " + \
                    (msg.get("abstract") or "")
                if _mentions(meta, ns):
                    return "ok"
        except Exception:
            pass
    try:
        code, body = fetch(url)
    except requests.exceptions.Timeout:
        return "blocked"
    except requests.exceptions.SSLError:
        return "blocked"
    except requests.exceptions.ConnectionError as exc:
        s = str(exc)
        return "dead" if re.search(r"Name or service not known|NameResolution|nodename nor servname|getaddrinfo", s) \
            else "blocked"
    except Exception:
        return "blocked"
    if code in (404, 410):
        return "dead"
    if code in (401, 403, 429) or code >= 500:
        return "blocked"
    if code >= 400:
        return "dead"
    if _mentions(body, ns):
        return "ok"
    if _CHALLENGE.search(body[:5000]) or _interstitial(body):
        return "blocked"
    return "mismatch"


def _interstitial(body: str) -> bool:
    """跳转页 / JS 壳页（出版社 DOI 落地常见）：内容太少，无从判断是不是这个资源。"""
    t = re.search(r"<title[^>]*>(.*?)</title>", body[:20000], re.S | re.I)
    title = (t.group(1) if t else "").strip().lower()
    if re.search(r"redirect|loading|attention required|please wait|^$", title):
        return True
    if re.search(r'http-equiv=["\']?refresh', body[:20000], re.I):
        return True
    text = re.sub(r"<script.*?</script>|<style.*?</style>|<[^>]+>", " ", body, flags=re.S | re.I)
    return len(text.split()) < 80


def verify(reg: dict, head: Callable | None = None, fetch: Callable | None = None, workers: int = 8) -> int:
    """核验每条的 http(s) 获取链接；非链接（编号/门户名）标 n/a。

    默认按内容核验（check_link）。传 head=（只返回状态码的旧接口）则退回只看状态码：ok / blocked / dead。"""
    todo = []
    for r in reg.values():
        m = re.search(r"https?://\S+", r.get("access", ""))
        if not m:
            r["verified"] = "n/a"
            continue
        todo.append((r, m.group(0).rstrip(").,;")))

    def one(item):
        r, url = item
        if head is not None:
            try:
                code = head(url)
                return "ok" if code < 400 else ("blocked" if code in (401, 403, 429, 503) else "dead")
            except Exception:
                return "dead"
        return check_link(r, url, fetch or _fetch)

    if workers > 1 and len(todo) > 1:
        with ThreadPoolExecutor(workers) as ex:
            results = list(ex.map(one, todo))
    else:
        results = [one(t) for t in todo]
    for (r, _), st in zip(todo, results):
        r["verified"] = st
    return len(todo)


PRIORITIES = ("P0", "P1", "P2")
PRI_ZH = {"P0": "P0 优先上手", "P1": "P1 值得登记", "P2": "P2 了解即可"}
PRI_BATCH = 40


def attach_themes(reg: dict, topic_names: dict[str, str] | None = None) -> None:
    """资源的方向（中文名）→ 主题 key，供站点彩色标签与筛选；并上种子 / 收件箱指定的主题。"""
    from .. import themes
    names = topic_names if topic_names is not None else themes.topic_names()
    for r in reg.values():
        keys_ = [themes.for_topic(t, names) for t in r.get("topics", [])] + list(r.get("themes_fixed") or [])
        r["themes"] = list(dict.fromkeys(k for k in keys_ if k))


def _profile_lines() -> str:
    try:
        from ..config import load_profile
        text = load_profile()
    except Exception:
        return ""
    i = text.find("## 应用线")
    return text[i:i + 1500] if i >= 0 else text[:1500]


def prioritize(reg: dict, llm: LLM, only_missing: bool = True) -> int:
    """主表资源按研究者的应用线打 P0/P1/P2 + 一句理由。已有优先级默认保留（only_missing）；种子置顶的永远不动。"""
    from .. import themes
    bk = themes.by_key()
    todo = [r for r in reg.values() if is_core(r) and not r.get("pinned")
            and (not only_missing or r.get("priority") not in PRIORITIES)]
    n = 0
    for b in range(0, len(todo), PRI_BATCH):
        chunk = todo[b:b + PRI_BATCH]
        payload = [{"id": i, "name": r["name"], "kind": r["kind"], "modality": r.get("modality", ""),
                    "scale": r.get("scale", ""), "open": r.get("open", ""), "n_evidence": len(r.get("used_by", [])),
                    "themes": [bk[k]["label"] for k in r.get("themes", []) if k in bk], "note": r.get("note", "")}
                   for i, r in enumerate(chunk)]
        prompt = tagged("prioritize", (
            "研究者是提供算法支持的生物信息学博后。他的应用线：\n" + _profile_lines()
            + "\n\n请给下面每个资源定优先级：\n"
              "P0 = 某条应用线**现在就要用**：做 demo 的可下载公开数据、必须对标的基线模型/评分、"
              "迁移到 ChinaHEART 或类器官项目时的参照队列/基准；每批 P0 不超过 15%。\n"
              "P1 = 用途明确、接下来可能用到。\nP2 = 了解即可（通用工具、边缘数据、与应用线弱相关）。\n"
              "why：≤40 字中文，写清用在哪、怎么用（P2 可写空）；不要写「应用线N」这类编号，"
              "直接写具体场景名，如 ChinaHEART 迁移、类器官衰老 demo、虚拟扰动建模。\n\n【资源】\n"
            + json.dumps(payload, ensure_ascii=False)
            + '\n\n只输出 JSON 数组：[{"id":0,"priority":"P0","why":"..."}]'))
        try:
            rows = parse_json_array(llm.chat(prompt, task="prioritize", temperature=0.1, timeout=240))
        except Exception as exc:
            print(f"[resources] prioritize batch {b // PRI_BATCH} failed: {exc}")
            continue
        for row in rows:
            try:
                i = int(row.get("id", -1))
            except (TypeError, ValueError):
                continue
            pr = str(row.get("priority", "")).upper().strip()
            if 0 <= i < len(chunk) and pr in PRIORITIES:
                chunk[i]["priority"], chunk[i]["why"] = pr, str(row.get("why", ""))[:80]
                n += 1
    return n


def _pri(r: dict) -> str:
    return r.get("priority") if r.get("priority") in PRIORITIES else "P2"


def render(reg: dict, day: date | None = None) -> str:
    day = day or date.today()
    all_rows = sorted(reg.values(), key=lambda r: (-len(r["topics"]), -len(r["used_by"]), r["name"].lower()))
    rows = [r for r in all_rows if is_core(r)]
    new = [r for r in all_rows if r.get("status") == "new"]
    tail = [r for r in all_rows if not is_core(r) and r.get("status") != "new"]
    out = [f"# 资源登记（数据集 / 模型 / 基准）\n",
           f"从 {sum(len(r['used_by']) for r in all_rows)} 处证据引用中挖出资源，并入人工种子与日报新发现，共 {len(all_rows)} 项；"
           f"主表 {len(rows)} 项（种子/置顶，或被 ≥2 篇工作使用、或跨方向、或开放且链接核验通过且规模明确），"
           f"日报新发现 {len(new)} 项（未核验），其余 {len(tail)} 项单篇提及的列在末尾。"
           f"开放：yes 公开 / partial 部分 / registration 注册 / controlled 受控 / commercial 商业 / unknown 未确认。"
           f"核验：ok 内容匹配 / mismatch 页面不是该资源 / blocked 站点拒绝探测 / dead 失效 / n/a 非链接。"
           f"规模带 * 的取自单篇引用文献。更新 {day.isoformat()}\n"]
    from .. import themes
    bk = themes.by_key()
    for pr in PRIORITIES:
        sub = sorted((r for r in rows if _pri(r) == pr), key=lambda r: (KINDS.index(r["kind"]), -len(r["used_by"])))
        if not sub:
            continue
        out.append(f"\n## {PRI_ZH[pr]}（{len(sub)}）\n")
        out.append("| 名称 | 类型 | 主题 | 规模 | 获取 | 开放 | 证据 | 为什么 / 用途 |")
        out.append("|---|---|---|---|---|---|---|---|")
        for r in sub:
            acc = r.get("access", "")
            m = re.search(r"https?://\S+", acc)
            acc_md = f"[链接]({m.group(0)})" if m else acc
            tags = " ".join(f"#{bk[k]['label']}" for k in r.get("themes", []) if k in bk)
            scale = r.get("scale", "") + ("*" if r.get("scale") and r.get("scale_src") == "paper" else "")
            out.append(f"| **{r['name']}** | {KIND_ZH[r['kind']]} | {tags} | {scale} | {acc_md} | "
                       f"{r.get('open','')} | {len(r['used_by'])} | {r.get('why') or r.get('note','')} |")
    if new:
        out.append(f"\n## 日报新发现（{len(new)}，未核验）\n")
        for r in sorted(new, key=lambda r: r.get("added", ""), reverse=True):
            out.append(f"- {r['name']}（{KIND_ZH.get(r['kind'], r['kind'])}，{r.get('added', '')}）{r.get('access', '')}")
    if tail:
        out.append(f"\n## 单篇提及（{len(tail)}，未进主表）\n")
        by_kind: dict[str, list[str]] = {}
        for r in tail:
            by_kind.setdefault(r["kind"], []).append(r["name"])
        for kind in KINDS:
            if by_kind.get(kind):
                out.append(f"- {KIND_ZH[kind]}：" + "、".join(sorted(by_kind[kind])[:80]))
    return "\n".join(out) + "\n"


def inbox_path(root: Path | None = None) -> Path:
    return (root or BASE).parent / "data" / "resources_inbox.json"


def load_inbox(path: Path) -> list[dict]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except (OSError, json.JSONDecodeError):
        return []


def run_prioritize(llm: LLM, root: Path | None = None, redo: bool = False) -> Path:
    """不重挖不重核验：给现有 registry 补主题与优先级，重渲染。redo=True 全部重打（置顶的不动）。"""
    out_dir = (root or BASE) / RES_DIR_NAME
    reg_path = out_dir / "registry.json"
    reg = json.loads(reg_path.read_text(encoding="utf-8"))
    attach_themes(reg)
    print(f"[resources] prioritized {prioritize(reg, llm, only_missing=not redo)}")
    reg_path.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
    out = out_dir / "resources.md"
    out.write_text(render(reg), encoding="utf-8")
    return out


SEED_FIELDS = ("seed", "pinned", "open_seed", "aliases", "match", "themes_fixed", "scale_src", "status",
               "source", "added", "daily_urls", "verified")


def run_resources(llm: LLM | None, root: Path | None = None, head: Callable | None = None,
                  fetch: Callable | None = None, seeds: dict | None = None,
                  inbox: list[dict] | None = None) -> Path:
    """llm=None：不重新挖，只用已有 registry.json 重新合并（别名 / 种子 / 收件箱）、核验、渲染。
    head=（旧接口，只看状态码）或 fetch=（内容核验，测试注入）；都不给则联网做内容核验。"""
    base = root or BASE
    out_dir = base / RES_DIR_NAME
    out_dir.mkdir(parents=True, exist_ok=True)
    seeds = seeds if seeds is not None else load_seeds(seeds_path(root))
    inbox = inbox if inbox is not None else load_inbox(inbox_path(root))
    rows: list[dict] = []
    reg_path = out_dir / "registry.json"
    old = json.loads(reg_path.read_text(encoding="utf-8")) if reg_path.exists() else {}
    if llm is None:
        if not reg_path.exists():
            raise SystemExit("[resources] 没有 registry.json，需要带 LLM 先挖一次")
        # 只取证据挖出的部分重合并；种子与收件箱条目下面重新并入
        rows = [{k: v for k, v in r.items() if k not in SEED_FIELDS} for r in old.values()
                if r.get("used_by") or not (r.get("seed") or r.get("status") == "new")]
    else:
        for p in sorted(base.glob("*/topic.yaml")):
            if p.parent.name.startswith("_"):
                continue
            spec = load_spec(p)
            evs = EvidenceStore(spec.evidence_dir, spec.rejected_path).all()
            got = mine(evs, spec.name, llm)
            print(f"[resources] {spec.slug}: {len(got)} mentions from {len(evs)} evidence")
            rows += got
    reg = merge(rows, seeds=seeds)
    for k, r in reg.items():  # 优先级是人读过的判断，重挖不丢
        if old.get(k, {}).get("priority"):
            r["priority"], r["why"] = old[k]["priority"], old[k].get("why", "")
    print(f"[resources] inbox: {fold_inbox(reg, inbox, seeds)} new from {len(inbox)} daily entries")
    print(f"[resources] seeds applied: {apply_seeds(reg, seeds)}")
    verify(reg, head=head, fetch=fetch)
    finalize_open(reg)
    attach_themes(reg)
    if llm is not None:
        print(f"[resources] prioritized {prioritize(reg, llm)}")
    reg_path.write_text(json.dumps(reg, ensure_ascii=False, indent=1), encoding="utf-8")
    out = out_dir / "resources.md"
    out.write_text(render(reg), encoding="utf-8")
    from collections import Counter
    print(f"[resources] {len(reg)} resources → {out}; verified {dict(Counter(r.get('verified') for r in reg.values()))}")
    return out
