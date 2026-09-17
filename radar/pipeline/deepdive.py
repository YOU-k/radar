"""专题深研报告：单主题 × 长时间窗的深度调研，手动触发。

与日报（2天窗口的流式过滤）互补：给定主题和月份窗口，
查询扩展 → 回溯采集（EuropePMC/arXiv 存量 + Google News 产业动态）→
主题相关性筛选 → 每篇结构化抽取 → 固定模板综合。
产出 reports/<date>-<slug>.md，站点「专题报告」Tab 渲染。
"""
from __future__ import annotations

import json
import re
import time
from datetime import date, timedelta
from pathlib import Path

import requests

from .. import llm
from ..collectors import feed_parse
from ..collectors.europepmc import _search, _to_item
from ..config import ROOT, load_profile
from ..schema import Item
from .extract import extract_items

ARXIV_API = "https://export.arxiv.org/api/query"
MAX_PAPERS = 120   # 抽取上限：控制 LLM 成本
MAX_PER_QUERY = 60  # 每个查询词最多保留的候选


def _expand_topic(topic: str, months: int) -> dict:
    """LLM 把主题扩成英文查询词组；失败时用主题本身兜底。"""
    fallback = {"slug": re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")[:40]
                or "topic",
                "queries": [topic], "news_queries": [topic]}
    if not llm.available():
        return fallback
    prompt = (
        f"你是科研情报专家。用户要调研主题「{topic}」（近 {months} 个月）。\n"
        "请输出：\n"
        "slug：该主题的英文短标识（小写连字符，≤30字符，如 virtual-cell）。\n"
        "queries：5-8 个英文检索词组，用于 EuropePMC/arXiv 检索该主题文献，"
        "覆盖核心术语、同义词、相关技术路线（如世界模型/扰动预测/基础模型），"
        "每个≤6个单词，可用英文双引号短语。\n"
        "news_queries：2-3 个英文检索词，用于 Google News 检索该主题的产业/公司合作动态。\n\n"
        '只输出 JSON，形如 {"slug":"...","queries":["..."],"news_queries":["..."]}。'
    )
    try:
        content = llm.chat(prompt, model=llm.SCORE_MODEL, temperature=0.2, timeout=120)
        m = re.search(r"\{.*\}", content, re.DOTALL)
        d = json.loads(m.group(0))
        if d.get("queries"):
            d["slug"] = re.sub(r"[^a-z0-9-]", "", str(d.get("slug", "")).lower())[:40] or fallback["slug"]
            d["queries"] = [str(q)[:60] for q in d["queries"][:8]]
            d["news_queries"] = [str(q)[:60] for q in (d.get("news_queries") or [topic])[:3]]
            return d
    except Exception as exc:
        print(f"[deepdive] topic expansion failed: {exc}")
    return fallback


def _collect_europepmc(queries: list[str], start: str, end: str) -> list[Item]:
    items = {}
    for q in queries:
        try:
            rows = _search(q, start, end, page_size=100, sort="CITED desc")
        except Exception as exc:
            print(f"[deepdive] europepmc {q!r} failed: {exc}")
            continue
        for r in rows[:MAX_PER_QUERY]:
            it = _to_item(r, "deepdive")
            if it.title:
                items[it.id] = it
        time.sleep(1)
    return list(items.values())


def _collect_arxiv(queries: list[str], start: str, end: str) -> list[Item]:
    or_q = " OR ".join(f'all:"{q.strip(chr(34))}"' for q in queries[:6])
    d0, d1 = start.replace("-", ""), end.replace("-", "")
    q = f"({or_q}) AND submittedDate:[{d0}0000 TO {d1}2359]"
    for attempt in (1, 2):
        try:
            r = requests.get(ARXIV_API, params={
                "search_query": q, "sortBy": "relevance", "max_results": 100,
            }, timeout=150)
            r.raise_for_status()
            break
        except Exception as exc:
            print(f"[deepdive] arxiv attempt {attempt} failed: {exc}")
            time.sleep(10)
    else:
        return []
    import feedparser
    feed = feedparser.parse(r.text)
    items = []
    for e in feed.entries:
        aid = (e.get("id") or "").rsplit("/", 1)[-1]
        items.append(Item(
            id=f"arxiv:{aid}", source="arxiv", domain="deepdive",
            title=" ".join((e.get("title") or "").split()),
            url=f"https://arxiv.org/abs/{aid}",
            authors=", ".join(a.get("name", "") for a in e.get("authors", [])[:8]),
            abstract=" ".join((e.get("summary") or "").split()),
            published=(e.get("published") or "")[:10]))
    return items


def _collect_news(queries: list[str], months: int) -> list[dict]:
    news = {}
    for q in queries:
        url = (f"https://news.google.com/rss/search?"
               f"q={requests.utils.quote(q)}+when:{months}m&hl=en-US&gl=US&ceid=US:en")
        try:
            feed = feed_parse(url)
        except Exception as exc:
            print(f"[deepdive] news {q!r} failed: {exc}")
            continue
        for e in feed.entries[:10]:
            news[e.get("link", e.get("title", ""))] = {
                "title": e.get("title", ""),
                "published": e.get("published", "")}
        time.sleep(1)
    return list(news.values())[:25]


def _filter_relevant(items: list[Item], topic: str) -> list[Item]:
    """LLM 按主题相关性打分（0-10），保留 ≥5，上限 MAX_PAPERS。"""
    if not llm.available() or not items:
        return items[:MAX_PAPERS]
    scored: list[tuple[float, Item]] = []
    for i in range(0, len(items), 20):
        chunk = items[i:i + 20]
        payload = [{"id": j, "title": it.title,
                    "abstract": (it.abstract or "")[:400]}
                   for j, it in enumerate(chunk)]
        prompt = (
            f"判断每篇文献与调研主题「{topic}」的相关性，打分 0-10"
            "（10=主题核心工作，7=直接相关，5=沾边可参考，0=无关）。\n"
            "只输出 JSON 数组，形如 [{\"id\":0,\"score\":8}]。\n\n"
            + json.dumps(payload, ensure_ascii=False))
        try:
            content = llm.chat(prompt, model=llm.SCORE_MODEL, temperature=0.1, timeout=180)
            m = re.search(r"\[.*\]", content, re.DOTALL)
            for s in json.loads(m.group(0)) if m else []:
                j = int(s.get("id", -1))
                if 0 <= j < len(chunk):
                    scored.append((float(s.get("score", 0)), chunk[j]))
        except Exception as exc:
            print(f"[deepdive] relevance batch {i // 20} failed: {exc}")
    keep = [it for sc, it in sorted(scored, key=lambda x: -x[0]) if sc >= 5]
    return keep[:MAX_PAPERS]


TEMPLATE = """请输出中文调研报告，严格用以下章节结构（markdown）：
## 摘要（TL;DR）——5-8 条要点
## 背景与定义——一段
## 关键时间线——按月列出重要工作/事件
## 使用的技术——按方法学归类分小节，每个代表工作一段：方法、数据、关键结果（保留数字）
## 数据——按类型/规模/来源归类
## 应用场景——归类分小节
## 评测与可靠性反思——基准、批判性结果、没跑赢基线的证据
## 产业动态——公司/合作/授权（基于提供的新闻）
## 趋势结论与空白——编号列表，指出没人做的方向
## 参考文献——编号列表，格式 [n] 标题, 期刊/来源, 日期, URL
写作要求：每个论点落到具体工作；保留所有定量结果；宁缺勿滥，没有内容的章节写"本期无足够信息"；不要编造文献列表之外的引用。"""


def _synthesize(topic: str, months: int, papers: list[Item],
                extractions: list[dict], news: list[dict]) -> str:
    recs = []
    for it, ex in zip(papers, extractions):
        recs.append({
            "title": it.title, "url": it.url, "date": it.published,
            "journal": it.extra.get("journal", "") or it.source,
            **{k: v for k, v in ex.items() if v}})
    material = json.dumps(recs, ensure_ascii=False, indent=None)
    news_txt = "\n".join(f"- {n['title']} ({n['published'][:10]})" for n in news)
    prompt = (
        f"下面是关于「{topic}」近 {months} 个月的 {len(recs)} 篇文献的结构化抽取"
        f"和相关产业新闻。研究者的背景画像附后供校准深度。\n\n"
        f"【兴趣画像】\n{load_profile()[:2000]}\n\n"
        f"【文献抽取】\n{material[:28000]}\n\n"
        f"【产业新闻】\n{news_txt[:3000]}\n\n{TEMPLATE}")
    return llm.chat(prompt, model=llm.SYNTH_MODEL, temperature=0.3, timeout=600)


def run_deepdive(topic: str, months: int = 6) -> Path:
    end = date.today()
    start = (end - timedelta(days=months * 30)).isoformat()
    print(f"[deepdive] topic={topic!r} window={start}~{end}")

    plan = _expand_topic(topic, months)
    print(f"[deepdive] queries: {plan['queries']}")

    papers = _collect_europepmc(plan["queries"], start, end.isoformat())
    print(f"[deepdive] europepmc candidates: {len(papers)}")
    papers += _collect_arxiv(plan["queries"], start, end.isoformat())
    print(f"[deepdive] + arxiv candidates: {len(papers)}")

    seen = set()
    uniq = []
    for it in papers:
        key = it.id.lower()
        if key not in seen:
            seen.add(key)
            uniq.append(it)
    papers = _filter_relevant(uniq, topic)
    print(f"[deepdive] after relevance filter: {len(papers)}")

    news = _collect_news(plan["news_queries"], months)
    print(f"[deepdive] news: {len(news)}")

    extractions = extract_items(papers, topic=topic)
    print(f"[deepdive] extracted: {sum(1 for e in extractions if e['summary'])}")

    body = _synthesize(topic, months, papers, extractions, news)
    out = ROOT / "reports" / f"{end.isoformat()}-{plan['slug']}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        f"# 专题调研：{topic}（{start} ~ {end}）\n\n{body}\n",
        encoding="utf-8")
    print(f"[deepdive] wrote {out}")
    return out
