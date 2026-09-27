"""arXiv 采集：OAI-PMH 为主（录制的 arXivRaw 响应），RSS 兜底，id 统一。"""
from datetime import date
from pathlib import Path

import feedparser

from radar.collectors import arxiv

FIX = Path(__file__).parent / "fixtures"


def _pages():
    return [(FIX / "arxiv_oai_page1.xml").read_text(encoding="utf-8"),
            (FIX / "arxiv_oai_page2.xml").read_text(encoding="utf-8")]


def test_norm_id_forms():
    for s in ("https://arxiv.org/abs/2609.27532v2", "http://arxiv.org/abs/2609.27532", "oai:arXiv.org:2609.27532",
              "arXiv:2609.27532v1", "2609.27532"):
        assert arxiv.norm_id(s) == "2609.27532"
    assert arxiv.norm_id("hep-th/9901001v2") == "hep-th/9901001"
    assert arxiv.norm_id("nothing") == ""


def test_oai_set_mapping():
    assert arxiv.oai_set("cs.LG") == "cs:cs:LG"
    assert arxiv.oai_set("q-bio.GN") == "q-bio:q-bio:GN"
    assert arxiv.oai_set("stat.ML") == "stat:stat:ML"
    assert arxiv.oai_set("astro-ph.CO") == "physics:astro-ph:CO"


def test_fetch_oai_pages_and_v1_dates():
    pages, calls = _pages(), []

    def get(url, params):
        calls.append(dict(params))
        return pages[len(calls) - 1]

    rows = arxiv.fetch_oai("cs.LG", "2026-09-25", get=get)
    assert [c.get("resumptionToken") for c in calls] == [None, "tok123"]
    assert calls[0]["set"] == "cs:cs:LG" and calls[0]["from"] == "2026-09-25"
    by = {r["aid"]: r for r in rows}
    assert set(by) == {"2609.27532", "2609.28570", "2004.09073", "2609.02986"}
    # v1 日期取版本历史（不是 OAI created，后者是最新版本日期）
    assert by["2004.09073"]["published"] == "2020-04-20"
    assert by["2609.27532"]["published"] == "2026-09-23"
    assert by["2609.27532"]["title"].startswith("ProCredit")


def test_no_records_match_is_empty():
    xml = ('<?xml version="1.0"?><OAI-PMH xmlns="http://www.openarchives.org/OAI/2.0/">'
           "<error code='noRecordsMatch'>empty</error></OAI-PMH>")
    assert arxiv.fetch_oai("cs.LG", "2026-09-27", get=lambda u, p: xml) == []


CFG = {"domains": [
    {"name": "A", "arxiv": {"categories": ["cs.LG"], "queries": ["reinforcement learning", "policy optimization"]}},
    {"name": "B", "arxiv": {"categories": ["cs.LG"], "queries": ["image similarity"]}},
]}


def _no_rss(cat):
    raise AssertionError("RSS should not be used when OAI works")


def test_collect_oai_filters_replacements_and_normalizes():
    pages = _pages()
    n = {"oai": 0}

    def oai(cat, since):
        n["oai"] += 1
        return arxiv._parse_oai(pages[0])[0] + arxiv._parse_oai(pages[1])[0]

    items = arxiv.collect(CFG, {"daily": 2}, today=date(2026, 9, 27), oai=oai, rss=_no_rss, legacy_seen=set())
    assert n["oai"] == 1  # 同一分类只拉一次
    ids = {(it.domain, it.id) for it in items}
    # 2004.09073（CatSIM，2020 年旧文的新版本）被当替换丢掉，B 领域因此为空
    assert ids and all(d == "A" for d, _ in ids)
    assert ("A", "arxiv:2609.28570") in ids
    for it in items:
        assert it.id == f"arxiv:{arxiv.norm_id(it.id)}" and it.url == f"https://arxiv.org/abs/{it.id[6:]}"
        assert it.published >= "2026-09-18"


def test_collect_legacy_seen_url_skipped():
    rows = arxiv._parse_oai(_pages()[0])[0]
    items = arxiv.collect(CFG, {"daily": 2}, today=date(2026, 9, 27), oai=lambda c, s: rows, rss=_no_rss,
                          legacy_seen={"https://arxiv.org/abs/2609.28570"})
    assert "arxiv:2609.28570" not in {it.id for it in items}


def test_collect_rss_fallback_dates_and_cutoff():
    feed = feedparser.parse((FIX / "arxiv_rss.xml").read_bytes())
    rows = arxiv.fetch_rss("cs.LG", parse=lambda url: feed)
    by = {r["aid"]: r for r in rows}
    assert "2401.00001" not in by  # replace 公告丢掉
    assert by["2609.30001"]["published"] == "2026-09-25"
    assert by["2609.30001"]["abstract"].startswith("We train")

    def boom(cat, since):
        raise RuntimeError("HTTP 406")

    cfg = {"domains": [{"name": "W", "arxiv": {"categories": ["cs.LG"], "queries": ["world model"]}}]}
    items = arxiv.collect(cfg, {"daily": 2}, today=date(2026, 9, 27), oai=boom, rss=lambda c: rows,
                          legacy_seen=set())
    # 09-14 的 cross 早于 cutoff（09-25），不收
    assert [it.id for it in items] == ["arxiv:2609.30001"]
    assert items[0].url == "https://arxiv.org/abs/2609.30001" and items[0].published == "2026-09-25"
