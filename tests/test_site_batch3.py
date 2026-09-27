"""站点第三批：拆分页面与归档、默认日报、链接/引用/表格后处理、暗色、状态持久化。"""
import json
import re
import shutil
import subprocess
from datetime import date, timedelta

import pytest

from radar.pipeline import site


def test_linkify_skips_existing_links_and_trims_punct():
    h = '<p>见 https://doi.org/10.1/x。和 <a href="https://a.org">https://a.org</a> (https://b.org/p(1))</p>'
    out = site.linkify(h)
    assert '<a href="https://doi.org/10.1/x" target="_blank" rel="noopener">https://doi.org/10.1/x</a>。' in out
    assert out.count('href="https://a.org"') == 1
    assert 'href="https://b.org/p(1)"' in out and out.endswith(")</p>")


def test_linkify_does_not_touch_escaped_script():
    h = site._md("x https://ok.org <script>alert(1)</script> [a](javascript:alert(2))", ["extra"])
    out = site.post(h)
    assert "<script>" not in out and "javascript:" not in out and 'href="https://ok.org"' in out


def test_citations_link_to_reference_anchors():
    md = "## 摘要\n\n- 结论 [1] 与 [2, 3]，超范围 [9]\n\n## 参考文献\n\n1. A. https://doi.org/10.1/a\n2. B\n3. C\n"
    out = site.post(site._md(md, ["extra", "sane_lists"]), "aging")
    assert '<li id="ref-aging-1">' in out and '<li id="ref-aging-3">' in out
    assert '[<a class="cite" href="#ref-aging-1">1</a>]' in out
    assert '<a class="cite" href="#ref-aging-2">2</a>, <a class="cite" href="#ref-aging-3">3</a>' in out
    assert "[9]" in out  # 没有对应条目的不链接
    assert 'href="https://doi.org/10.1/a"' in out  # 参考文献里的裸 DOI 可点


def test_tables_wrapped_for_horizontal_scroll():
    out = site.post(site._md("| a | b |\n|---|---|\n| 1 | 2 |\n", ["extra", "tables"]))
    assert out.startswith('<div class="tw"><table>') and out.endswith("</table></div>")


def test_css_dark_mode_and_scroll_margin():
    assert "@media (prefers-color-scheme:dark)" in site.CSS and "--bg:#0d1117" in site.CSS
    assert "scroll-margin-top" in site.CSS and "overflow-wrap:anywhere" in site.CSS
    css = site.theme_css()
    assert "[data-t=cardio]" in css and "--cd:" in css  # 暗色下用调亮的主题色


def test_js_storage_wrapped_in_try_catch():
    for m in re.finditer(r"(localStorage|sessionStorage)\.\w+", site.JS):
        before = site.JS[max(0, m.start() - 40):m.start()]
        assert "try{" in before, m.group(0)


@pytest.fixture
def fake_root(tmp_path, monkeypatch):
    root = tmp_path
    (root / "digests").mkdir()
    (root / "weekly").mkdir()
    d0 = date(2026, 9, 27)
    for i in range(20):
        d = (d0 - timedelta(days=i)).isoformat()
        (root / "digests" / f"{d}.md").write_text(
            f"# {d}\n\n## 领域（1 条）\n\n- **[Paper {i}](https://doi.org/10.1016/s0140-6736(24)0000{i % 10}-x)** `7.0` — r\n"
            "  <sub>主题：#心血管</sub>\n", encoding="utf-8")
    for w in range(10):
        (root / "weekly" / f"2026-W{30 + w:02d}.md").write_text(
            f"# 每周 W{30 + w}\n\n# 第二个标题\n\n- 链接 https://www.semanticscholar.org/very/long/url/{'x' * 80}\n",
            encoding="utf-8")
    bg = root / "background" / "cardio-omics"
    (bg / "deep").mkdir(parents=True)
    refs = "\n".join(f"{n}. Ref {n}. https://doi.org/10.1/{n}" for n in range(1, 4))
    (bg / "report.md").write_text("# 心血管 · 方向背景报告\n\n证据 3 篇\n\n## 摘要（TL;DR）\n\n- 要点 [1]\n\n"
                                  "## 1 背景\n\n正文 [2]\n\n| a | b |\n|---|---|\n| 1 | 2 |\n\n## 参考文献\n\n" + refs + "\n",
                                  encoding="utf-8")
    (bg / "deep" / "2026-09-27-深度.md").write_text("# 深度标题\n\n内容 https://x.org/y\n", encoding="utf-8")
    (root / "background" / "_resources").mkdir()
    (root / "background" / "_resources" / "registry.json").write_text(json.dumps({
        "chinaheart": {"name": "ChinaHEART", "kind": "dataset", "used_by": ["a"], "topics": [], "themes": ["cardio"],
                       "pinned": True, "seed": True, "priority": "P0", "open": "controlled", "verified": "n/a",
                       "why": "目标队列"}}), encoding="utf-8")
    (root / "data").mkdir()
    (root / "data" / "resources_inbox.json").write_text(json.dumps([
        {"name": "New atlas", "kind": "dataset", "url": "https://doi.org/10.1/new", "day": "2026-09-26",
         "source": "daily", "theme": "singlecell", "note": "新图谱"}]), encoding="utf-8")
    monkeypatch.setattr(site, "ROOT", root)
    monkeypatch.setattr(site, "DOCS", root / "docs")
    monkeypatch.setattr(site, "OUT", root / "docs" / "index.html")
    return root


def test_build_site_structure(fake_root):
    out = site.build_site(date(2026, 9, 27))
    t = out.read_text(encoding="utf-8")
    docs = fake_root / "docs"
    # 默认日报 tab
    assert re.search(r'class="tab on" data-tab="day"', t) and '<div id="panel-day" class="panel on">' in t
    # 只内联最近 14 天，其余归档并在日报 tab 链接
    assert t.count('<details class="day"') == site.RECENT_DAYS
    assert (docs / "archive" / "2026-09.html").exists() and 'href="archive/2026-09.html"' in t
    assert "Paper 19" not in t and "Paper 19" in (docs / "archive" / "2026-09.html").read_text(encoding="utf-8")
    # 括号 DOI 的条目没丢
    assert "s0140-6736(24)00000-x" in t
    # 周报：最近 8 份内联，其余归档；正文多余 H1 降级
    assert t.count('<div class="wk"') == site.RECENT_WEEKS and (docs / "archive" / "weekly.html").exists()
    assert "<h1>第二个标题" not in t
    # 方向报告：卡片只内联 TL;DR，全文在 docs/bg/，深度调研也拆页
    assert 'data-src="bg/cardio.html"' in t and "正文 [" not in t and "要点 [" in t
    page = (docs / "bg" / "cardio.html").read_text(encoding="utf-8")
    assert 'id="doc-rest"' in page and '<li id="ref-cardio-2">' in page and 'class="tw"' in page
    assert '<a class="cite" href="#ref-cardio-1">1</a>' in t  # TL;DR 里的引用链到懒加载部分
    deep = list((docs / "bg").glob("cardio-omics-deep-*.html"))
    assert len(deep) == 1 and 'href="https://x.org/y"' in deep[0].read_text(encoding="utf-8")
    # 资源库单独成页，含置顶与"新发现 · 未核验"
    assert 'data-src="res.html"' in t
    res = (docs / "res.html").read_text(encoding="utf-8")
    assert "ChinaHEART" in res and "受控申请" in res and "新发现 · 未核验（1）" in res and "New atlas" in res
    # 过期页面会被清掉
    (docs / "bg" / "stale.html").write_text("x")
    site.build_site(date(2026, 9, 27))
    assert not (docs / "bg" / "stale.html").exists()


def test_inline_js_parses(fake_root):
    if not shutil.which("node"):
        pytest.skip("node not installed")
    t = site.build_site(date(2026, 9, 27)).read_text(encoding="utf-8")
    js = re.search(r"<script>(.*?)</script>", t, re.S).group(1)
    p = fake_root / "inline.js"
    p.write_text(js, encoding="utf-8")
    r = subprocess.run(["node", "--check", str(p)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
