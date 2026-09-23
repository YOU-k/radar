from __future__ import annotations

import argparse
import json
from datetime import date, timedelta

from . import llm
from .collectors import COLLECTORS
from .config import ROOT, load_local_env, load_profile, load_sources
from .pipeline import extract
from .pipeline.dedup import filter_new
from .pipeline.deepread import deepread_top
from .pipeline.digest import write_digest
from .pipeline.resources import append_resources, mine_infrastructure
from .pipeline.score import score_items
from .pipeline.site import build_site

FREQ_DAYS = {"daily": 2, "weekly": 7, "monthly": 30}  # daily 重叠收 2 天：某天采集失败次日自动补回，重复由 dedup 挡


def active_freqs(today: date) -> dict[str, int]:
    """每天跑 daily 源；周日顺带收 weekly 慢源；每月 1 号顺带收 monthly 慢源。"""
    freqs = {"daily": FREQ_DAYS["daily"]}
    if today.weekday() == 6:
        freqs["weekly"] = FREQ_DAYS["weekly"]
    if today.day == 1:
        freqs["monthly"] = FREQ_DAYS["monthly"]
    return freqs


def cmd_daily(days: int, use_llm: bool) -> None:
    cfg = load_sources()
    freqs = active_freqs(date.today())
    if days > 1:  # 手动回补窗口
        freqs = {f: days for f in freqs}
    print(f"[plan] cadences: {sorted(freqs)}")
    items = []
    for name, mod in COLLECTORS.items():
        try:
            got = mod.collect(cfg, freqs)
            print(f"[{name}] {len(got)} items")
            items.extend(got)
        except Exception as exc:
            print(f"[{name}] collector failed: {exc}")
    fresh = filter_new(items)
    print(f"[dedup] {len(items)} -> {len(fresh)} new")
    scored = score_items(fresh, cfg, use_llm=use_llm)
    if use_llm:
        n = deepread_top(scored)
        print(f"[deepread] {n} items")
        from .background.context import annotate
        n = annotate(scored, cfg)
        print(f"[context] {n} items placed against background")
    n = append_resources(scored, date.today())
    print(f"[resources] {n} new")
    if use_llm:
        hot = [it for it in scored if it.score >= 7.0]
        n = extract.store(hot, extract.extract_items(hot), date.today())
        print(f"[extract] {n} records")
    out = write_digest(scored, date.today())
    print(f"[digest] wrote {out}")


def cmd_weekly(use_llm: bool) -> None:
    today = date.today()
    week_start = today - timedelta(days=6)
    texts = []
    for i in range(7):
        p = ROOT / "digests" / f"{(week_start + timedelta(days=i)).isoformat()}.md"
        if p.exists():
            texts.append(p.read_text(encoding="utf-8"))
    iso = today.isocalendar()
    out = ROOT / "weekly" / f"{iso.year}-W{iso.week:02d}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    header = f"# 每周综合 — {iso.year}-W{iso.week:02d}（{week_start} ~ {today}）\n\n"
    if not texts:
        out.write_text(header + "本周无 digest。\n", encoding="utf-8")
        print(f"[weekly] no digests, wrote {out}")
        return
    body = _weekly_llm(texts) if use_llm else None
    if body is None:
        body = _weekly_fallback(texts)
    from .background.context import weekly_changes
    out.write_text(header + body + weekly_changes(), encoding="utf-8")
    print(f"[weekly] wrote {out}")
    if use_llm:
        n = mine_infrastructure(extract.load_since(30), today)
        print(f"[weekly] infrastructure resources: {n}")


def cmd_landscape(use_llm: bool) -> None:
    """每月一次：LLM 对照近 30 天 digest 审查 registry，提增补/修订建议。"""
    today = date.today()
    out = ROOT / "registry_updates" / f"{today.year}-{today.month:02d}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    header = f"# Registry 月度刷新建议 — {today.year}-{today.month:02d}\n\n"

    registry_text = "\n\n".join(
        f"### 文件 registry/{p.name}\n{p.read_text(encoding='utf-8')}"
        for p in sorted((ROOT / "registry").glob("*.md"))
    )
    news = []
    for i in range(30):
        p = ROOT / "digests" / f"{(today - timedelta(days=i)).isoformat()}.md"
        if p.exists():
            news.extend(l for l in p.read_text(encoding="utf-8").splitlines()
                        if l.startswith("- **["))

    if not llm.available() or not use_llm:
        out.write_text(header + "（未启用 LLM，跳过本月刷新。）\n", encoding="utf-8")
        print(f"[landscape] no LLM, wrote {out}")
        return

    prompt = (
        "下面是某研究者的兴趣画像、他的长期知识库 registry 现状、以及近一个月情报 digest 的条目清单。\n\n"
        f"【兴趣画像】\n{load_profile()}\n\n"
        f"【registry 现状】\n{registry_text[:12000]}\n\n"
        f"【近一月情报条目】\n" + "\n".join(news[:400])[:12000] + "\n\n"
        "请审查：近一月的信息里，有没有应该进入长期知识库、或使现有条目过时的内容？\n"
        "只输出有建议的文件，按 '## databases.md' / '## models.md' / '## people.md' 分节，"
        "每条一行 markdown（沿用各文件现有格式，标注 [新增] 或 [修订]）。"
        "背景格局没有实质变化的分节不要出现。都没有就回复'本月无建议'。"
    )
    try:
        body = llm.chat(prompt, model=llm.SYNTH_MODEL, temperature=0.3, timeout=300)
    except Exception as exc:
        body = f"（LLM 调用失败：{exc}）"
    out.write_text(header + body + "\n", encoding="utf-8")
    print(f"[landscape] wrote {out}")


def _weekly_llm(texts: list[str]) -> str | None:
    if not llm.available():
        return None
    cfg = load_sources()
    labels = {d["name"]: d.get("label_zh", d["name"]) for d in cfg.get("domains", [])}
    by_dom: dict[str, list[dict]] = {}
    for r in extract.load_since(7):
        r = {k: v for k, v in r.items() if k != "date" and v}
        by_dom.setdefault(labels.get(r.get("domain", ""), r.get("domain", "")), []).append(r)
    material = json.dumps(by_dom, ensure_ascii=False)[:16000]
    joined = "\n\n---\n\n".join(t[:4000] for t in texts)[:12000]
    prompt = (
        "下面是某研究者的兴趣画像、本周高分条目的结构化抽取（按领域分组）、以及本周每日 digest。\n\n"
        f"【兴趣画像】\n{load_profile()}\n\n"
        f"【本周结构化抽取】\n{material}\n\n"
        f"【本周 digest 全文】\n{joined}\n\n"
        "请输出中文 markdown，按领域分开总结，不要跨领域混合。\n"
        "对本周实际有内容的每个领域写一节 '## <领域名>'，固定四个小节：\n"
        "### 本周亮点 —— 2-4 个最重要工作，每个 1-2 句，要具体（方法/数据/关键数字），附链接；\n"
        "### 数据与资源 —— 本周出现的数据集/模型（没有就写：无）；\n"
        "### 评测与警示 —— 基准结果、没跑赢基线、可复现性等值得警惕的信号（没有就写：无）；\n"
        "### 一句话判断 —— 该领域本周的实质进展。\n"
        "没有实质内容的领域不写。\n"
        "最后加一节 '## Registry 增补建议'：本周出现的数据库/模型/人物中，"
        "建议加入 registry 长期知识库的条目，按 databases.md / models.md / people.md 分组，每条一行。"
    )
    try:
        return llm.chat(prompt, model=llm.SYNTH_MODEL, temperature=0.3, timeout=300)
    except Exception as exc:
        print(f"[weekly] LLM failed, fallback to raw list: {exc}")
        return None


def _weekly_fallback(texts: list[str]) -> str:
    titles = []
    for t in texts:
        for line in t.splitlines():
            if line.startswith("- **["):
                titles.append(line)
    return ("（未启用 LLM，以下为本周 digest 条目汇总）\n\n"
            + "\n".join(titles[:80]) + "\n")


def cmd_background(args) -> None:
    from .background import llmio
    from .background.spec import BASE, init_topic, load_spec
    if args.action == "init":
        p = init_topic(args.topic, args.name or args.topic)
        print(f"[background] wrote {p}，填好 topic.yaml 再跑 bootstrap")
        return
    from .background.runner import Pipeline
    llm = llmio.RadarLLM() if (llmio.available() and not args.no_llm) else None
    if llm is None:
        print("[background] 无 LLM key：只做检索/去重，不评审、不编译")
    if args.action in ("resources", "joint"):
        if llm is None and args.action == "joint":
            raise SystemExit("[background] joint 需要 LLM")
        from .background.joint import run_joint
        from .background.resources import run_resources
        if args.action == "resources":
            print(f"[background] wrote {run_resources(llm)}")
        else:
            res = BASE / "_resources" / "resources.md"
            print(f"[background] wrote {run_joint(llm, resources_md=res.read_text(encoding='utf-8') if res.exists() else '')}")
        return
    slugs = background_slugs(args.topic)
    for slug in slugs:
        if len(slugs) > 1:
            print(f"[background] === {slug} ===")
        spec = load_spec(slug)
        pipe = Pipeline(spec, llm, fetch_text=not args.no_fulltext)
        if args.action == "bootstrap":
            for res in pipe.bootstrap(args.rounds or None):
                print(res.log.to_markdown())
        elif args.action == "renew":
            res = pipe.renew(ROOT / "data" / "extractions.jsonl")
            print(res.log.to_markdown())
        elif args.action == "refetch":
            print(f"[background] refetched {pipe.refetch()}")
        elif args.action == "compile":
            print(f"[background] wrote {pipe.compile_only()}")


def background_slugs(topic: str) -> list[str]:
    """--topic all → 全部方向（跳过 _joint / _resources 这类下划线目录）。"""
    from .background.spec import BASE
    if topic != "all":
        return [topic]
    return sorted(p.parent.name for p in BASE.glob("*/topic.yaml") if not p.parent.name.startswith("_"))

def main() -> None:
    load_local_env()  # 本机运行时注入 /data3/yy/key.env（不打印、不覆盖已有变量）
    ap = argparse.ArgumentParser(prog="radar")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("daily", "weekly", "landscape"):
        p = sub.add_parser(name)
        p.add_argument("--days", type=int, default=1)
        p.add_argument("--no-llm", action="store_true")
    p = sub.add_parser("background", help="方向背景库：init / bootstrap / renew / compile")
    p.add_argument("action", choices=["init", "bootstrap", "renew", "compile", "refetch", "resources", "joint"])
    p.add_argument("--topic", required=True, help="slug，如 population-omics-ai；all = 全部方向")
    p.add_argument("--name", default="", help="init 用：方向中文名")
    p.add_argument("--rounds", type=int, default=0, help="bootstrap 轮数，0 = topic.yaml 的 budget.rounds")
    p.add_argument("--no-fulltext", action="store_true")
    p.add_argument("--no-llm", action="store_true", help="只检索/去重，不评审不编译（冒烟用）")
    sub.add_parser("site")
    args = ap.parse_args()
    use_llm = not getattr(args, "no_llm", False)
    if args.cmd == "daily":
        cmd_daily(args.days, use_llm)
    elif args.cmd == "weekly":
        cmd_weekly(use_llm)
    elif args.cmd == "landscape":
        cmd_landscape(use_llm)
    elif args.cmd == "background":
        cmd_background(args)
    else:
        out = build_site()
        print(f"[site] wrote {out}")


if __name__ == "__main__":
    main()
