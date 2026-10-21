#!/usr/bin/env python3
"""给最近 N 天的日报回填专家评级（创新/证据/可用 A-C + 一线机构）。

评级管线 2026-10-21 才进 score.py，历史日报没有评级行。本脚本解析日报条目，
以 标题+期刊+理由（+ data/extractions.jsonl 里匹配到的中文摘要）批量让 LLM 补评，
把 `  <sub>评级：创新 A · 证据 B · 可用 C[ · 一线机构]</sub>` 插回 md（主题行之后）。
幂等：已有评级的条目跳过。跑完用 `python -m radar.run site` 重建站点生效。

用法：.venv/bin/python scripts/backfill_ratings.py [天数，默认 10]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from radar import llm  # noqa: E402
from radar.config import ROOT  # noqa: E402
from radar.pipeline.digest import TOP_INST  # noqa: E402
from radar.run import load_local_env  # noqa: E402

ITEM_RE = re.compile(r"^- \*\*\[(?P<title>.+?)\]\((?P<url>\S+?)\)\*\*", re.M)
SUB_RE = re.compile(r"^  <sub>(?P<body>.*?)</sub>\s*$")
BATCH = 20


def norm_title(t: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()


def load_summaries() -> dict[str, str]:
    p = ROOT / "data" / "extractions.jsonl"
    out = {}
    if p.exists():
        for line in p.read_text(encoding="utf-8").splitlines():
            try:
                e = json.loads(line)
                out[norm_title(e.get("title", ""))] = e.get("summary", "")
            except json.JSONDecodeError:
                continue
    return out


def rate_batch(items: list[dict]) -> list[dict]:
    payload = [{"id": j, "title": it["title"], "journal": it["journal"],
                "reason": it["reason"], "summary": it["summary"][:300]} for j, it in enumerate(items)]
    prompt = (
        "下面是一批科研情报条目。只给三个 A/B/C 专家评级（从严，与相关性无关，只评条目本身硬度）：\n"
        "nov 创新性（A 新范式/首创方法/新基准/新资源类型；B 有意义的改进或组合；C 例行应用/增量）、\n"
        "evi 证据强度（A 大队列/多中心/外部验证/系统性基准；B 中等规模或单队列部分验证；C 小样本/无验证/纯关联/纯观点）、\n"
        "use 可用性（A 数据与代码或权重公开可获取；B 部分开放或需申请；C 未开放或仅应要求提供）。\n\n"
        "【条目】\n" + json.dumps(payload, ensure_ascii=False)
        + '\n\n只输出 JSON 数组，形如 [{"id":0,"nov":"A","evi":"B","use":"C"}]，不要输出其他内容。'
    )
    content = llm.chat(prompt, model=llm.SCORE_MODEL, temperature=0.2, timeout=180)
    m = re.search(r"\[.*\]", content, re.DOTALL)
    return json.loads(m.group(0)) if m else []


def main() -> None:
    days = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    load_local_env()
    if not llm.available():
        raise SystemExit("LLM 不可用（key.env 没加载到）")
    summaries = load_summaries()
    files = sorted((ROOT / "digests").glob("*.md"), reverse=True)[:days]
    # 第一遍：收集全文件需要评级的条目（按标题去重，跨天共享评级）
    pending: dict[str, dict] = {}
    for path in files:
        for m in ITEM_RE.finditer(path.read_text(encoding="utf-8")):
            t = norm_title(m.group("title"))
            if t and t not in pending:
                pending[t] = {"title": m.group("title"), "journal": "", "reason": "", "summary": summaries.get(t, "")}
    print(f"[backfill] {len(pending)} 个唯一条目待评级")
    rated: dict[str, dict] = {}
    items = list(pending.values())
    for i in range(0, len(items), BATCH):
        chunk = items[i:i + BATCH]
        try:
            for s in rate_batch(chunk):
                j = int(s.get("id", -1))
                if 0 <= j < len(chunk):
                    r = {k: str(s.get(k, "")).strip().upper()[:1] for k in ("nov", "evi", "use")}
                    r = {k: v for k, v in r.items() if v in ("A", "B", "C")}
                    if r:
                        rated[norm_title(chunk[j]["title"])] = r
            print(f"[backfill] rated {min(i + BATCH, len(items))}/{len(items)}")
        except Exception as exc:
            print(f"[backfill] batch {i // BATCH} failed: {exc}")
    # 第二遍：逐文件插入评级行
    n_ins = 0
    for path in files:
        lines = path.read_text(encoding="utf-8").splitlines()
        out: list[str] = []
        i = 0
        changed = False
        while i < len(lines):
            line = lines[i]
            m = ITEM_RE.match(line)
            if not m:
                out.append(line)
                i += 1
                continue
            # 收集该条目的 sub 块
            block = [line]
            i += 1
            while i < len(lines) and SUB_RE.match(lines[i]):
                block.append(lines[i])
                i += 1
            r = rated.get(norm_title(m.group("title")), {})
            already = any("<sub>评级：" in b for b in block)
            if r and not already:
                inst_m = re.search(r"（([^）]+)）", block[1] if len(block) > 1 else "")
                top = " · 一线机构" if inst_m and TOP_INST.search(inst_m.group(1)) else ""
                zh = (("nov", "创新"), ("evi", "证据"), ("use", "可用"))
                rated_s = " · ".join(f"{z} {r[k]}" for k, z in zh if k in r)
                rating_line = f"  <sub>评级：{rated_s}{top}</sub>"
                # 插到主题行之后；没有主题行就插在第一行 meta 之后
                pos = next((k for k, b in enumerate(block) if "<sub>主题：" in b), 0)
                block = block[:pos + 1] + [rating_line] + block[pos + 1:]
                changed = True
                n_ins += 1
            out.extend(block)
        if changed:
            path.write_text("\n".join(out) + "\n", encoding="utf-8")
            print(f"[backfill] {path.name} updated")
    print(f"[backfill] 共插入 {n_ins} 条评级；重建站点：python -m radar.run site")


if __name__ == "__main__":
    main()
