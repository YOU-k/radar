"""把 digests/ 和 weekly/ 渲染成卡片式移动站点 docs/index.html。

GitHub Pages 直接以 main 分支 /docs 发布，零构建、零外部资源。
日报 md 是本仓库 digest.py 生成的固定格式，这里解析成结构化条目渲染卡片；
周报是自由 markdown，直接整篇转换。
顶部 Tab：方向背景（默认，联合分析置顶）/ 周报 / 日报 / 资源库。
"""
from __future__ import annotations

import html
import re
from datetime import date
from pathlib import Path

import markdown

from .. import themes
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
#panel-week,#panel-day,#panel-res,#panel-bg{display:none}
#panel-week.on,#panel-day.on,#panel-res.on,#panel-bg.on{display:block}
details.bg{background:#fff;border:1px solid #d0d7de;border-radius:12px;margin:0 0 10px;padding:0 16px}
details.bg>summary{cursor:pointer;list-style:none;padding:12px 0;font-weight:600;font-size:15px}
details.bg>summary::-webkit-details-marker{display:none}
details.bg>summary .cnt{display:block;font-weight:400;color:#57606a;font-size:12px;margin-top:2px}
details.bg .bgbody{font-size:14.5px;padding-bottom:14px}
details.bg .bgbody h2{font-size:15px;color:#1a7f37}
details.bg .bgbody h3{font-size:14.5px;color:#8250df;margin-bottom:4px}
details.bg .bgbody ol{padding-left:20px;font-size:13px;color:#4b5563}
#q{width:100%;padding:9px 14px;border:1px solid #d0d7de;border-radius:20px;background:#fff;color:#1f2328;font-size:14px;outline:none;margin-bottom:12px}
#q:focus{border-color:#0969da}
.wk{background:#fff;border:1px solid #d0d7de;border-radius:12px;padding:4px 16px 14px;margin:0 0 10px;font-size:14.5px;box-shadow:0 1px 2px rgba(31,35,40,.04)}
.wk h2{font-size:15px;color:#1a7f37}
.wk h3{font-size:14.5px;color:#8250df;margin-bottom:4px}
.wk table,.bgbody table{border-collapse:collapse;width:100%;font-size:12.5px;display:block;overflow-x:auto}
.wk th,.wk td,.bgbody th,.bgbody td{border:1px solid #d0d7de;padding:4px 6px;text-align:left;vertical-align:top}
.wk th,.bgbody th{background:#f6f8fa}
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
.vt{display:inline-block;font-size:11px;font-weight:700;border-radius:4px;padding:0 5px;margin-right:4px}
.vt.jr{background:#dafbe1;color:#1a7f37}
.vt.pp{background:#fff1e5;color:#bc4c00}
.reason{color:#4b5563;font-size:13.5px;margin-top:5px}
.meta{color:#57606a;font-size:12px;margin-top:5px}
.bgline{color:#8250df;font-size:12.5px;margin-top:4px;border-left:3px solid #8250df;padding-left:6px}
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
.sec{margin:18px 2px 8px}
.sec-t{font-size:15px;font-weight:700}
.sec-d{font-size:12.5px;color:#57606a}
a.ov{display:block;background:#fff;border:1px solid #d0d7de;border-left:4px solid #d0d7de;border-radius:10px;padding:8px 12px;margin:0 0 8px;color:#1f2328;font-size:13px}
.ov-h{display:flex;align-items:center;flex-wrap:wrap;gap:2px}
.ov-n{font-weight:700;font-size:14px}
.ov-deep{margin-left:auto;font-size:11px;color:#0969da;border:1px solid #0969da55;border-radius:8px;padding:0 6px}
.ov-s{color:#57606a;font-size:12px;margin:2px 0}
.ov-l{margin-top:2px;line-height:1.5}
.ov-l b{color:#57606a;font-weight:600;margin-right:4px}
details.bg.sub{border-style:dashed;margin:0 0 10px;background:#f6f8fa}
.th{display:inline-block;font-size:11.5px;font-weight:600;border-radius:10px;padding:0 7px;margin:0 4px 2px 0;line-height:18px;white-space:nowrap}
.card.tagged{border-left:4px solid var(--tc,#d0d7de)}
.tags{margin-top:5px}
.fbar{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 10px}
.fchip{font-size:12.5px;font-weight:600;border-radius:14px;padding:3px 10px;cursor:pointer;user-select:none;border:1px solid #d0d7de;background:#fff;color:#57606a}
.fchip.on{box-shadow:inset 0 0 0 2px currentColor}
.fchip .n{font-weight:400;opacity:.75;margin-left:3px}
.sum{background:#fff;border:1px solid #d0d7de;border-radius:12px;padding:8px 14px;margin:0 0 12px;font-size:14px}
.sum h4{margin:4px 0 2px;font-size:13px;color:#57606a}
.sum ul{margin:4px 0;padding-left:18px}
.sum li{margin:3px 0}
.pri{font-size:13px;font-weight:700;margin:16px 2px 6px}
.pri.p0{color:#cf222e}.pri.p1{color:#9a6700}.pri.p2{color:#57606a}
.rcard{background:#fff;border:1px solid #d0d7de;border-radius:10px;padding:8px 12px;margin:0 0 8px;font-size:13.5px}
.rcard .rn{font-weight:700;font-size:14.5px}
.rcard .rk{font-size:11.5px;color:#57606a;border:1px solid #d0d7de;border-radius:4px;padding:0 4px;margin-left:6px}
.rcard .why{color:#1f2328;margin-top:3px}
.rcard .rm{color:#57606a;font-size:12px;margin-top:3px}
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
let dayTheme='';
function applyDay(){
  const s=q.value.trim().toLowerCase();
  const active=s||dayTheme;
  days.forEach(d=>{
    let any=false;
    d.querySelectorAll('.card').forEach(c=>{
      const hit=(!s||c.textContent.toLowerCase().includes(s))&&(!dayTheme||(' '+c.dataset.themes+' ').includes(' '+dayTheme+' '));
      c.classList.toggle('hide',!hit); any=any||hit;
    });
    d.querySelectorAll('.dom').forEach(g=>{
      let n=g.nextElementSibling, has=false;
      while(n&&n.classList.contains('card')){if(!n.classList.contains('hide'))has=true;n=n.nextElementSibling}
      g.classList.toggle('hide',!has);
    });
    d.querySelectorAll('.sum').forEach(x=>x.classList.toggle('hide',!!dayTheme));
    d.classList.toggle('hide',!any);
    if(active)d.open=any; else d.open=d.dataset.first==='1';
  });
}
q.addEventListener('input',applyDay);
function bindChips(bar,onPick){
  if(!bar)return;
  const chips=[...bar.querySelectorAll('.fchip')];
  chips.forEach(c=>c.addEventListener('click',()=>{
    const v=c.classList.contains('on')?'':c.dataset.v;
    chips.forEach(x=>x.classList.toggle('on',x===c&&v!==''));
    onPick(v);
  }));
}
bindChips(document.getElementById('fbar-day'),v=>{dayTheme=v;applyDay();});
document.querySelectorAll('a.ov').forEach(a=>a.addEventListener('click',()=>{const d=document.getElementById(a.getAttribute('href').slice(1));if(d)d.open=true;}));
let resTheme='',resKind='';
function applyRes(){
  document.querySelectorAll('.rcard').forEach(c=>{
    const hit=(!resTheme||(' '+c.dataset.themes+' ').includes(' '+resTheme+' '))&&(!resKind||c.dataset.kind===resKind);
    c.classList.toggle('hide',!hit);
  });
  document.querySelectorAll('.rgroup').forEach(g=>g.classList.toggle('hide',!g.querySelector('.rcard:not(.hide)')));
}
bindChips(document.getElementById('fbar-res'),v=>{resTheme=v;applyRes();});
bindChips(document.getElementById('fbar-kind'),v=>{resKind=v;applyRes();});
"""

ITEM_RE = re.compile(
    r"^- \*\*\[(?P<title>.+?)\]\((?P<url>[^)]+)\)\*\*"
    r" `(?P<score>[0-9.]+)`(?P<tag>〔资源〕)?(?: — (?P<reason>.*))?$")
SEC_RE = re.compile(r"^## (?P<name>.+?)（\d+ 条）$")
META_RE = re.compile(r"^  <sub>(?!定位：)(?P<meta>.*)</sub>$")
BG_RE = re.compile(r"^  <sub>定位：(?P<bg>.*)</sub>$")
SUB_RE = re.compile(r"^  <sub>(?P<body>.*)</sub>$")
SUMMARY_RE = re.compile(r"^## 今日要点\n+(?P<body>(?:- .*\n?)+)", re.M)
DEEP_RE = re.compile(
    r'^  <details markdown="1"><summary>深读</summary>\n\n(?P<body>.*?)\n\n  </details>$',
    re.DOTALL)

WEEKDAYS = "一二三四五六日"


def _chip(key: str) -> str:
    t = themes.by_key().get(key)
    if not t:
        return ""
    c = t["color"]
    return (f'<span class="th" style="color:{c};background:{c}14;border:1px solid {c}55">'
            f'{html.escape(t["label"])}</span>')


def _chips_html(keys_: list[str]) -> str:
    return "".join(_chip(k) for k in keys_)


def _filter_bar(bar_id: str, counts: dict[str, int]) -> str:
    """主题筛选条：只列有条目的主题，点一下只看该主题，再点取消。"""
    out = [f'<div class="fbar" id="{bar_id}">']
    for t in themes.load_themes():
        n = counts.get(t["key"], 0)
        if not n:
            continue
        c = t["color"]
        out.append(f'<span class="fchip" data-v="{t["key"]}" style="color:{c};border-color:{c}66">'
                   f'{html.escape(t["label"])}<span class="n">{n}</span></span>')
    out.append("</div>")
    return "".join(out)


def _summary_html(text: str) -> str:
    m = SUMMARY_RE.search(text)
    if not m:
        return ""
    items = []
    for line in m.group("body").splitlines():
        line = line[2:].strip()
        if not line:
            continue
        words, rest = [], line
        while rest.startswith("#"):  # 行首的 #主题 渲染成彩色标签
            w, _, rest = rest.partition(" ")
            words.append(w)
        keys_ = themes.parse_line(" ".join(words))
        body = html.escape(rest if keys_ else line)
        if body.startswith("必读："):
            body = "<b>必读：</b>" + body[3:]
        items.append(f"<li>{_chips_html(keys_)}{body}</li>")
    return f'<div class="sum"><h4>今日要点</h4><ul>{"".join(items)}</ul></div>' if items else ""


def _meta_html(meta: str) -> str:
    """〔期刊〕/〔预印本〕前缀渲染成小标签，其余原样转义。"""
    for tag, cls in (("〔期刊〕", "jr"), ("〔预印本〕", "pp")):
        if meta.startswith(tag):
            return f'<span class="vt {cls}">{tag[1:-1]}</span>' + html.escape(meta[len(tag):])
    return html.escape(meta)


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
                  "tag": m.group("tag") or "", "bg": "", "themes": []}
            cur.append(it)
            i += 1
            while i < len(lines) and SUB_RE.match(lines[i]):
                body = SUB_RE.match(lines[i]).group("body")
                if body.startswith("定位："):
                    it["bg"] = body[3:]
                elif body.startswith("主题："):
                    it["themes"] = themes.parse_line(body[3:])
                elif not it["meta"]:
                    it["meta"] = body
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
            tks = it.get("themes") or []
            color = themes.by_key().get(tks[0], {}).get("color", "") if tks else ""
            cls = "card tagged" if color else "card"
            style = f' style="--tc:{color}"' if color else ""
            parts = [f'<div class="{cls}"{style} data-score="{it["score"]}" data-themes="{" ".join(tks)}">',
                     f'<div class="t"><a href="{html.escape(it["url"])}">'
                     f'{html.escape(it["title"])}</a>{badge}</div>']
            if it["reason"]:
                parts.append(f'<div class="reason">{html.escape(it["reason"])}</div>')
            if it["meta"]:
                parts.append(f'<div class="meta">{_meta_html(it["meta"])}</div>')
            if tks:
                parts.append(f'<div class="tags">{_chips_html(tks)}</div>')
            if it.get("bg"):
                parts.append(f'<div class="bgline">{html.escape(it["bg"])}</div>')
            if it["deep"]:
                parts.append(
                    '<details class="deep"><summary>深读笔记</summary>'
                    f'<div class="deepbody">{it["deep"]}</div></details>')
            parts.append("</div>")
            cards.append("".join(parts))
    body = _summary_html(text) + ("\n".join(cards) or '<div class="empty">当日无条目。</div>')
    open_attr = " open" if first else ""
    return (f'<details class="day" data-first="{1 if first else 0}"{open_attr}>'
            f'<summary>{html.escape(label)}<span class="cnt">{total} 条</span></summary>'
            f'<div class="daybody">{body}</div></details>')


def _render_weekly(path: Path) -> str:
    text = re.sub(r"\A# [^\n]*\n+", "", path.read_text(encoding="utf-8"))
    body = markdown.markdown(text, extensions=["extra", "sane_lists"])
    return f'<div class="wk"><h3>{html.escape(path.stem)}</h3>{body}</div>'


BG_HEAD_RE = re.compile(r"^# (?P<name>.+?) · 方向背景报告\n+(?P<stats>[^\n]+)", re.M)


def _render_background(report: Path, title: str = "", chip: str = "", anchor: str = "", prefix: str = "") -> str:
    """background/<slug>/report.md → 折叠卡片；标题行取方向名（或 title），副行取统计行；prefix 放在正文前（深度调研）。"""
    text = report.read_text(encoding="utf-8")
    m = BG_HEAD_RE.match(text)
    name = title or (m.group("name") if m else report.parent.name)
    stats = m.group("stats") if m else ""
    body = text[m.end():] if m else text
    html_body = markdown.markdown(body, extensions=["extra", "sane_lists", "tables"])
    ident = f' id="{anchor}"' if anchor else ""
    return (f'<details class="bg"{ident}><summary>{_chip(chip) if chip else ""}{html.escape(name)}'
            f'<span class="cnt">{html.escape(stats)}</span></summary>'
            f'<div class="bgbody">{prefix}{html_body}</div></details>')


KIND_ZH = {"dataset": "数据集", "model": "模型", "benchmark": "基准", "database": "数据库", "tool": "工具"}
PRI_ZH = {"P0": "P0 优先上手", "P1": "P1 值得登记", "P2": "P2 了解即可"}


def _render_resources(reg_path: Path) -> str:
    """registry.json → 按优先级分组的资源卡片 + 主题 / 类型筛选条。只展示主表（与 resources.md 同口径）。"""
    import json
    from ..background.resources import is_core
    reg = json.loads(reg_path.read_text(encoding="utf-8"))
    rows = [r for r in reg.values() if is_core(r)]
    if not rows:
        return ""
    counts: dict[str, int] = {}
    for r in rows:
        for k in r.get("themes", []):
            counts[k] = counts.get(k, 0) + 1
    kinds = [k for k in KIND_ZH if any(r["kind"] == k for r in rows)]
    kind_bar = ('<div class="fbar" id="fbar-kind">' + "".join(
        f'<span class="fchip" data-v="{k}">{KIND_ZH[k]}<span class="n">'
        f'{sum(r["kind"] == k for r in rows)}</span></span>' for k in kinds) + "</div>")
    out = [f'<div class="meta" style="margin:0 2px 8px">主表 {len(rows)} 项 · 按你的应用线排优先级 · '
           f'点主题/类型筛选，再点取消</div>', _filter_bar("fbar-res", counts), kind_bar]
    for pr in ("P0", "P1", "P2"):
        sub = [r for r in rows if (r.get("priority") if r.get("priority") in PRI_ZH else "P2") == pr]
        if not sub:
            continue
        sub.sort(key=lambda r: (-len(r.get("themes", [])), -len(r.get("used_by", [])), r["name"].lower()))
        cards = []
        for r in sub:
            m = re.search(r"https?://\S+", r.get("access", ""))
            name = html.escape(r["name"])
            name = f'<a href="{html.escape(m.group(0))}">{name}</a>' if m else name
            meta = " · ".join(x for x in (r.get("modality", ""), r.get("scale", ""),
                                          f"开放 {r.get('open', '')}", f"证据 {len(r.get('used_by', []))} 篇",
                                          f"核验 {r.get('verified', '')}") if x)
            why = r.get("why") or r.get("note", "")
            tks = r.get("themes", [])
            color = themes.by_key().get(tks[0], {}).get("color", "") if tks else ""
            style = f' style="border-left:4px solid {color}"' if color else ""
            cards.append(f'<div class="rcard"{style} data-themes="{" ".join(tks)}" data-kind="{r["kind"]}">'
                         f'<div class="rn">{name}<span class="rk">{KIND_ZH.get(r["kind"], r["kind"])}</span></div>'
                         f'<div class="tags">{_chips_html(tks)}</div>'
                         f'<div class="why">{html.escape(why)}</div><div class="rm">{html.escape(meta)}</div></div>')
        out.append(f'<div class="rgroup"><div class="pri {pr.lower()}">{PRI_ZH[pr]}（{len(sub)}）</div>'
                   + "".join(cards) + "</div>")
    return "\n".join(out)


def _day_theme_counts(paths: list[Path]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for p in paths:
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.startswith("  <sub>主题："):
                for k in themes.parse_line(line[len("  <sub>主题："):-len("</sub>")]):
                    counts[k] = counts.get(k, 0) + 1
    return counts


def _render_deep(path: Path, nested: bool = False) -> str:
    """background/<slug>/deep/*.md：会话里用 deep-research + expert-panel 做的深度调研（人工触发，不自动更新）。"""
    text = path.read_text(encoding="utf-8")
    m = re.match(r"# (?P<t>[^\n]+)\n", text)
    title = m.group("t") if m else path.stem
    body = text[m.end():] if m else text
    stats = f"深度调研 · {path.parent.parent.name} · {path.name[:10]}"
    html_body = markdown.markdown(body, extensions=["extra", "sane_lists", "tables"])
    cls = "bg sub" if nested else "bg"
    return (f'<details class="{cls}"><summary>〔深度〕{html.escape(title)}'
            f'<span class="cnt">{html.escape(stats)}</span></summary>'
            f'<div class="bgbody">{html_body}</div></details>')


def _md_table_rows(text: str, heading: str) -> list[list[str]]:
    """取 '## heading' 下第一张 markdown 表的数据行（去表头、分隔行），单元格去掉加粗与 [证据]/[常识] 标注。"""
    m = re.search(rf"^## {re.escape(heading)}[^\n]*\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    rows = []
    for line in (m.group(1) if m else "").splitlines():
        if not line.startswith("|") or re.match(r"^\|[\s:|-]+\|$", line):
            continue
        cells = [re.sub(r"\*\*|\[(证据|常识)\]", "", c).strip() for c in line.strip("|").split("|")]
        rows.append(cells)
    return rows[1:]  # 第一行是表头


def _match_row(name: str, rows: list[list[str]]) -> list[str]:
    """表里的方向名常被缩写（"LLM 科研智能体与可验证奖励 RL"），按相似度匹配。"""
    import difflib
    keys = [r[0] for r in rows]
    hit = difflib.get_close_matches(name, keys, n=1, cutoff=0.45)
    return rows[keys.index(hit[0])] if hit else []


def _short(text: str, n: int) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text if len(text) <= n else text[:n - 1] + "…"


SECTION = '<div class="sec"><div class="sec-t">{t}</div><div class="sec-d">{d}</div></div>'


def _render_overview() -> tuple[str, int]:
    """总览页三层：一页总览（每主题一张小卡）→ 跨方向（为什么 / 做什么）→ 各方向（深度调研收在所属方向里）。"""
    base = ROOT / "background"
    principles, joint = base / "_principles" / "report.md", base / "_joint" / "report.md"
    p_rows = _md_table_rows(principles.read_text(encoding="utf-8"), "总判断") if principles.exists() else []
    j_rows = _md_table_rows(joint.read_text(encoding="utf-8"), "全景") if joint.exists() else []
    topics = []  # (theme, spec_name, report_path, stats, deep_paths)
    for t in themes.load_themes():
        rp = base / t.get("topic", "") / "report.md"
        if not rp.exists():
            continue
        m = BG_HEAD_RE.match(rp.read_text(encoding="utf-8"))
        deep = sorted((rp.parent / "deep").glob("*.md"),
                      key=lambda p: (p.name[:10], "评审" not in p.name, p.name), reverse=True)
        topics.append((t, m.group("name") if m else rp.parent.name, rp, m.group("stats") if m else "", deep))

    out = [SECTION.format(t="一页总览", d="每个主题一行：处在什么阶段、真正要回答的问题、卡在哪。点主题名跳到该方向的完整报告。")]
    for t, name, rp, stats, deep in topics:
        pr, jr = _match_row(name, p_rows), _match_row(name, j_rows)
        c = t["color"]
        stage = _short(jr[1], 28) if len(jr) > 1 else ""
        q = _short(pr[1], 70) if len(pr) > 1 else ""
        neck = _short(pr[2], 70) if len(pr) > 2 else ""
        deep_tag = f'<span class="ov-deep">深度调研 {len(deep)}</span>' if deep else ""
        out.append(
            f'<a class="ov" href="#topic-{t["key"]}" style="border-left-color:{c}">'
            f'<div class="ov-h">{_chip(t["key"])}<span class="ov-n">{html.escape(name)}</span>{deep_tag}</div>'
            + (f'<div class="ov-s">{html.escape(stage)}</div>' if stage else "")
            + (f'<div class="ov-l"><b>问题</b> {html.escape(q)}</div>' if q else "")
            + (f'<div class="ov-l"><b>瓶颈</b> {html.escape(neck)}</div>' if neck else "")
            + "</a>")

    out.append(SECTION.format(t="跨方向", d="两份报告分工不同：一份讲为什么（底层逻辑，每月更新），一份讲做什么（联合项目建议，每周更新）。"))
    for path, label in ((principles, "为什么 · 全局判断（第一性原理）"), (joint, "做什么 · 联合行动建议")):
        if path.exists():
            out.append(_render_background(path, title=label))

    out.append(SECTION.format(t="各方向", d="每个方向一份证据综述（每周吃日报增量重编）。有深度调研的，放在该方向卡片最上面。"))
    for t, name, rp, stats, deep in topics:
        extra = "".join(_render_deep(p, nested=True) for p in deep)
        out.append(_render_background(rp, title=name, chip=t["key"], anchor=f"topic-{t['key']}", prefix=extra))
    return "\n".join(out), len(topics)


def build_site(today: date | None = None) -> Path:
    today = today or date.today()
    digests = sorted((ROOT / "digests").glob("*.md"), reverse=True)
    weeklies = sorted((ROOT / "weekly").glob("*.md"), reverse=True)

    week_html = ("\n".join(_render_weekly(p) for p in weeklies)
                 if weeklies else '<div class="empty">暂无周报。</div>')
    day_html = ("\n".join(_render_digest(p, i == 0) for i, p in enumerate(digests))
                if digests else '<div class="empty">暂无日报。</div>')
    bg_html, n_topics = _render_overview()
    res_parts = []
    reg_json = ROOT / "background" / "_resources" / "registry.json"
    if reg_json.exists():
        res_parts.append(_render_resources(reg_json))
    daily_res = ROOT / "resources.md"
    if daily_res.exists():
        res_parts.append('<details class="bg"><summary>日报新发现的资源（未核验）</summary><div class="bgbody">'
                         + markdown.markdown(daily_res.read_text(encoding="utf-8"), extensions=["extra", "sane_lists"])
                         + "</div></details>")
    res_html = "\n".join(res_parts) or '<div class="empty">暂无资源条目。</div>'

    parts = [
        "<!doctype html><html lang=zh><head>",
        '<meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">',
        "<title>radar · 科研情报</title>",
        f"<style>{CSS}</style></head><body><main>",
        '<div class="top"><h1>radar · 科研情报</h1>',
        f'<div class="meta">更新至 {today.isoformat()} · '
        f'{n_topics} 个方向 / {len(weeklies)} 份周报 / {len(digests)} 份日报</div>',
        '<div class="tabs">'
        '<div class="tab on" data-tab="bg">总览</div>'
        '<div class="tab" data-tab="week">周报</div>'
        '<div class="tab" data-tab="day">日报</div>'
        '<div class="tab" data-tab="res">资源库</div>'
        "</div></div>",
        f'<div id="panel-bg" class="on">{bg_html}</div>',
        f'<div id="panel-week">{week_html}</div>',
        '<div id="panel-day">',
        _filter_bar("fbar-day", _day_theme_counts(digests)),
        '<input id=q placeholder="过滤条目（标题 / 关键词）…">',
        f"{day_html}</div>",
        f'<div id="panel-res">{res_html}</div>',
        f"<script>{JS}</script></main></body></html>",
    ]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(parts), encoding="utf-8")
    return OUT
