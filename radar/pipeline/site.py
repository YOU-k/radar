"""把 digests/ 和 weekly/ 渲染成卡片式移动站点 docs/index.html。

GitHub Pages 直接以 main 分支 /docs 发布，零构建、零外部资源。
日报 md 是本仓库 digest.py 生成的固定格式，这里解析成结构化条目渲染卡片；
周报是自由 markdown，直接整篇转换。
顶部 Tab：周报 / 日报，点击切换，默认周报。
"""
from __future__ import annotations

import html
import re
from datetime import date
from pathlib import Path

import markdown

from ..config import ROOT

OUT = ROOT / "docs" / "index.html"

CSS = """
:root{color-scheme:light}
*{box-sizing:border-box}
body{margin:0;background:#f6f8fa;color:#1f2328;font:16px/1.7 -apple-system,"PingFang SC","Noto Sans SC",sans-serif}
main{max-width:720px;margin:0 auto;padding:0 12px 80px}
a{color:#0969da;text-decoration:none}
a:active{opacity:.7}
.top{position:sticky;top:0;z-index:9;background:rgba(246,248,250,.94);backdrop-filter:blur(8px);padding:12px 0 10px;border-bottom:1px solid #d0d7de;margin:0 -12px 16px;padding-left:12px;padding-right:12px}
.top h1{font-size:17px;margin:0 0 2px}
.top .meta{color:#57606a;font-size:12px;margin-bottom:10px}
.tabs{display:flex;gap:8px}
.tab{flex:1;text-align:center;padding:9px 0;border:1px solid #d0d7de;border-radius:20px;background:#fff;color:#57606a;font-size:14.5px;font-weight:600;cursor:pointer;user-select:none}
.tab.on{background:#1f6feb;border-color:#1f6feb;color:#fff}
#panel-week,#panel-day,#panel-res,#panel-report{display:none}
#panel-week.on,#panel-day.on,#panel-res.on,#panel-report.on{display:block}
#q{width:100%;padding:9px 14px;border:1px solid #d0d7de;border-radius:20px;background:#fff;color:#1f2328;font-size:14px;outline:none;margin-bottom:12px}
#q:focus{border-color:#0969da}
.wk{background:#fff;border:1px solid #d0d7de;border-radius:12px;padding:4px 16px 14px;margin:0 0 10px;font-size:14.5px;box-shadow:0 1px 2px rgba(31,35,40,.04)}
.wk h2{font-size:15px;color:#1a7f37}
.wk h3{font-size:14.5px;color:#8250df;margin-bottom:4px}
details.day{margin:0 0 10px}
details.day>summary{cursor:pointer;list-style:none;display:flex;justify-content:space-between;align-items:center;padding:11px 4px;border-bottom:1px solid #d0d7de;font-weight:600;font-size:15px}
details.day>summary::-webkit-details-marker{display:none}
details.day>summary .cnt{font-weight:400;color:#57606a;font-size:12px}
details.day>summary::after{content:"›";color:#8c959f;transition:transform .15s}
details.day[open]>summary::after{transform:rotate(90deg)}
details.day>.daybody{padding-top:8px}
.dom{color:#8250df;font-size:13px;font-weight:600;margin:14px 2px 6px}
.card{background:#fff;border:1px solid #d0d7de;border-radius:12px;padding:11px 13px;margin:0 0 10px;box-shadow:0 1px 2px rgba(31,35,40,.04)}
.card .t{font-size:15px;line-height:1.5}
.card .t a{color:#1f2328;font-weight:600}
.badge{display:inline-block;min-width:34px;text-align:center;font-size:12px;font-weight:700;border-radius:6px;padding:1px 6px;margin-left:6px;vertical-align:2px}
.badge.hi{background:#dafbe1;color:#1a7f37}
.badge.mid{background:#fff8c5;color:#9a6700}
.badge.lo{background:#eaeef2;color:#57606a}
.badge.res{background:#ddf4ff;color:#0969da}
.reason{color:#4b5563;font-size:13.5px;margin-top:5px}
.meta{color:#57606a;font-size:12px;margin-top:5px}
details.deep{margin-top:8px;border-top:1px dashed #d0d7de;padding-top:6px}
details.deep>summary{cursor:pointer;list-style:none;color:#0969da;font-size:13px}
details.deep>summary::-webkit-details-marker{display:none}
details.deep>summary::before{content:"▸ "}
details.deep[open]>summary::before{content:"▾ "}
details.deep .deepbody{font-size:13.5px;color:#4b5563;padding-top:4px}
details.deep .deepbody h2,details.deep .deepbody h3{font-size:13.5px;color:#1a7f37;margin:10px 0 2px}
details.deep .deepbody p{margin:4px 0}
.empty{color:#57606a;font-size:13px;padding:6px 2px}
.hide{display:none!important}
"""

JS = """
const tabs=[...document.querySelectorAll('.tab')];
const panels={};
tabs.forEach(t=>panels[t.dataset.tab]=document.getElementById('panel-'+t.dataset.tab));
tabs.forEach(t=>t.addEventListener('click',()=>{
  tabs.forEach(x=>x.classList.toggle('on',x===t));
  Object.entries(panels).forEach(([k,p])=>p.classList.toggle('on',k===t.dataset.tab));
}));
const q=document.getElementById('q');
const days=[...document.querySelectorAll('details.day')];
q.addEventListener('input',()=>{
  const s=q.value.trim().toLowerCase();
  days.forEach(d=>{
    let any=false;
    d.querySelectorAll('.card').forEach(c=>{
      const hit=!s||c.textContent.toLowerCase().includes(s);
      c.classList.toggle('hide',!hit); any=any||hit;
    });
    d.querySelectorAll('.dom').forEach(g=>{
      let n=g.nextElementSibling, has=false;
      while(n&&n.classList.contains('card')){if(!n.classList.contains('hide'))has=true;n=n.nextElementSibling}
      g.classList.toggle('hide',!has);
    });
    d.classList.toggle('hide',!any);
    if(s)d.open=any; else d.open=d.dataset.first==='1';
  });
});
"""

ITEM_RE = re.compile(
    r"^- \*\*\[(?P<title>.+?)\]\((?P<url>[^)]+)\)\*\*"
    r" `(?P<score>[0-9.]+)`(?P<tag>〔资源〕)?(?: — (?P<reason>.*))?$")
SEC_RE = re.compile(r"^## (?P<name>.+?)（\d+ 条）$")
META_RE = re.compile(r"^  <sub>(?P<meta>.*)</sub>$")
DEEP_RE = re.compile(
    r'^  <details markdown="1"><summary>深读</summary>\n\n(?P<body>.*?)\n\n  </details>$',
    re.DOTALL)

WEEKDAYS = "一二三四五六日"


def _score_class(score: float) -> str:
    return "hi" if score >= 7.5 else ("mid" if score >= 4 else "lo")


def _parse_digest(text: str) -> list[tuple[str, list[dict]]]:
    """固定格式 digest md → [(领域名, [条目])]。"""
    sections: list[tuple[str, list[dict]]] = []
    cur: list[dict] | None = None
    lines = text.splitlines()
    i = 0
    while i < len(lines):
        m = SEC_RE.match(lines[i])
        if m:
            cur = []
            sections.append((m.group("name"), cur))
            i += 1
            continue
        m = ITEM_RE.match(lines[i]) if cur is not None else None
        if m:
            it = {"title": m.group("title"), "url": m.group("url"),
                  "score": float(m.group("score")),
                  "reason": m.group("reason") or "", "meta": "", "deep": "",
                  "tag": m.group("tag") or ""}
            cur.append(it)
            i += 1
            if i < len(lines):
                mm = META_RE.match(lines[i])
                if mm:
                    it["meta"] = mm.group("meta")
                    i += 1
            # 深读块跨行，拼起来再匹配
            if i < len(lines) and lines[i].startswith('  <details markdown="1">'):
                block = [lines[i]]
                i += 1
                while i < len(lines) and not lines[i].startswith("  </details>"):
                    block.append(lines[i])
                    i += 1
                if i < len(lines):
                    block.append(lines[i])
                    i += 1
                dm = DEEP_RE.match("\n".join(block))
                if dm:
                    body = "\n".join(l[2:] if l.startswith("  ") else l
                                     for l in dm.group("body").splitlines())
                    it["deep"] = markdown.markdown(body, extensions=["extra"])
            continue
        i += 1
    return sections


def _render_digest(path: Path, first: bool) -> str:
    text = path.read_text(encoding="utf-8")
    sections = _parse_digest(text)
    total = sum(len(items) for _, items in sections)
    try:
        d = date.fromisoformat(path.stem)
        label = f"{path.stem} · 周{WEEKDAYS[d.weekday()]}"
    except ValueError:
        label = path.stem
    cards = []
    for name, items in sections:
        if not items:
            continue
        cards.append(f'<div class="dom">{html.escape(name)}</div>')
        for it in items:
            badge = (f'<span class="badge {_score_class(it["score"])}">'
                     f'{it["score"]:.1f}</span>')
            if it.get("tag"):
                badge += '<span class="badge res">资源</span>'
            parts = [f'<div class="card" data-score="{it["score"]}">',
                     f'<div class="t"><a href="{html.escape(it["url"])}">'
                     f'{html.escape(it["title"])}</a>{badge}</div>']
            if it["reason"]:
                parts.append(f'<div class="reason">{html.escape(it["reason"])}</div>')
            if it["meta"]:
                parts.append(f'<div class="meta">{html.escape(it["meta"])}</div>')
            if it["deep"]:
                parts.append(
                    '<details class="deep"><summary>深读笔记</summary>'
                    f'<div class="deepbody">{it["deep"]}</div></details>')
            parts.append("</div>")
            cards.append("".join(parts))
    body = "\n".join(cards) or '<div class="empty">当日无条目。</div>'
    open_attr = " open" if first else ""
    return (f'<details class="day" data-first="{1 if first else 0}"{open_attr}>'
            f'<summary>{html.escape(label)}<span class="cnt">{total} 条</span></summary>'
            f'<div class="daybody">{body}</div></details>')


def _render_weekly(path: Path) -> str:
    text = re.sub(r"\A# [^\n]*\n+", "", path.read_text(encoding="utf-8"))
    body = markdown.markdown(text, extensions=["extra", "sane_lists"])
    return f'<div class="wk"><h3>{html.escape(path.stem)}</h3>{body}</div>'


def build_site(today: date | None = None) -> Path:
    today = today or date.today()
    digests = sorted((ROOT / "digests").glob("*.md"), reverse=True)
    weeklies = sorted((ROOT / "weekly").glob("*.md"), reverse=True)

    week_html = ("\n".join(_render_weekly(p) for p in weeklies)
                 if weeklies else '<div class="empty">暂无周报。</div>')
    day_html = ("\n".join(_render_digest(p, i == 0) for i, p in enumerate(digests))
                if digests else '<div class="empty">暂无日报。</div>')
    reports = sorted((ROOT / "reports").glob("*.md"), reverse=True)
    report_html = ("\n".join(_render_weekly(p) for p in reports)
                   if reports else '<div class="empty">暂无专题报告。</div>')
    res_file = ROOT / "resources.md"
    res_html = ('<div class="wk">'
                + markdown.markdown(res_file.read_text(encoding="utf-8"),
                                    extensions=["extra", "sane_lists"])
                + "</div>") if res_file.exists() else '<div class="empty">暂无资源条目。</div>'

    parts = [
        "<!doctype html><html lang=zh><head>",
        '<meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">',
        "<title>radar · 科研情报</title>",
        f"<style>{CSS}</style></head><body><main>",
        '<div class="top"><h1>radar · 科研情报</h1>',
        f'<div class="meta">更新至 {today.isoformat()} · '
        f'{len(digests)} 份日报 / {len(weeklies)} 份周报 / {len(reports)} 份专题</div>',
        '<div class="tabs">'
        '<div class="tab on" data-tab="week">周报</div>'
        '<div class="tab" data-tab="day">日报</div>'
        '<div class="tab" data-tab="report">专题报告</div>'
        '<div class="tab" data-tab="res">资源库</div>'
        "</div></div>",
        f'<div id="panel-week" class="on">{week_html}</div>',
        '<div id="panel-day">',
        '<input id=q placeholder="过滤条目（标题 / 关键词 / 领域）…">',
        f"{day_html}</div>",
        f'<div id="panel-report">{report_html}</div>',
        f'<div id="panel-res">{res_html}</div>',
        f"<script>{JS}</script></main></body></html>",
    ]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(parts), encoding="utf-8")
    return OUT
