"""把 digests/ 和 weekly/ 渲染成单个移动优化静态页 docs/index.html。

GitHub Pages 直接以 main 分支 /docs 发布，零构建、零外部资源。
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
:root{color-scheme:dark}
*{box-sizing:border-box}
body{margin:0;background:#0d1117;color:#e6edf3;font:16px/1.65 -apple-system,"PingFang SC","Noto Sans SC",sans-serif}
main{max-width:760px;margin:0 auto;padding:16px 14px 60px}
h1{font-size:20px;margin:8px 0 12px}
h2{font-size:17px;margin:22px 0 8px;color:#7ee787}
h3{font-size:15px}
a{color:#58a6ff;text-decoration:none}
input#q{width:100%;padding:10px 12px;margin:6px 0 14px;border:1px solid #30363d;border-radius:8px;background:#161b22;color:#e6edf3;font-size:15px;position:sticky;top:0;z-index:9}
details{border:1px solid #21262d;border-radius:10px;margin:0 0 10px;background:#161b22;overflow:hidden}
details>summary{padding:10px 12px;cursor:pointer;font-weight:600;list-style:none}
details>summary::before{content:"▸ ";color:#7ee787}
details[open]>summary::before{content:"▾ "}
details>.body{padding:0 12px 10px;border-top:1px solid #21262d}
details details{margin:8px 0;background:#0d1117}
details details>summary{font-weight:400;color:#8b949e}
sub{color:#8b949e}
code{background:#21262d;border-radius:4px;padding:0 4px;font-size:13px;color:#f0883e}
ul{padding-left:20px}
li{margin:6px 0}
.meta{color:#8b949e;font-size:13px}
"""

JS = """
const q=document.getElementById('q'),days=[...document.querySelectorAll('details.day')];
q.addEventListener('input',()=>{
  const s=q.value.trim().toLowerCase();
  days.forEach(d=>{
    if(!s){d.style.display='';d.open=false;return}
    const hit=d.textContent.toLowerCase().includes(s);
    d.style.display=hit?'':'none';d.open=!!s&&hit;
  });
  if(!s&&days[0])days[0].open=true;
});
"""


def _md2html(text: str) -> str:
    # 列表里嵌套的 <details markdown="1"> 不会被 md_in_html 处理，
    # 先抽出来单独渲染，再用占位符回填。
    stashes: list[str] = []

    def stash(m: re.Match) -> str:
        inner = markdown.markdown(m.group(2), extensions=["extra"])
        stashes.append(
            f'<details class="deep"><summary>{m.group(1)}</summary>'
            f'<div class="body">{inner}</div></details>'
        )
        return f"\n\nDRSTASH{len(stashes) - 1}\n\n"

    text = re.sub(
        r'<details markdown="1"><summary>(.*?)</summary>\s*(.*?)\s*</details>',
        stash, text, flags=re.DOTALL,
    )
    out = markdown.markdown(text, extensions=["extra", "sane_lists"])
    for i, s in enumerate(stashes):
        out = out.replace(f"<p>DRSTASH{i}</p>", s).replace(f"DRSTASH{i}", s)
    return out


def _strip_h1(text: str) -> str:
    return re.sub(r"\A# [^\n]*\n+", "", text)


def _section(files: list, cls: str, open_first: bool) -> str:
    out = []
    for i, p in enumerate(files):
        body = _md2html(_strip_h1(p.read_text(encoding="utf-8")))
        open_attr = " open" if open_first and i == 0 else ""
        out.append(
            f'<details class="{cls}"{open_attr}><summary>{html.escape(p.stem)}</summary>'
            f'<div class="body">{body}</div></details>'
        )
    return "\n".join(out)


def build_site(today: date | None = None) -> Path:
    today = today or date.today()
    digests = sorted((ROOT / "digests").glob("*.md"), reverse=True)
    weeklies = sorted((ROOT / "weekly").glob("*.md"), reverse=True)

    parts = [
        "<!doctype html><html lang=zh><head>",
        '<meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">',
        "<title>radar · 科研情报</title>",
        f"<style>{CSS}</style></head><body><main>",
        "<h1>radar · 科研情报</h1>",
        f'<div class=meta>更新至 {today.isoformat()} · {len(digests)} 份日报 / {len(weeklies)} 份周报</div>',
        '<input id=q placeholder="过滤日报（标题 / 关键词）…">',
    ]
    if weeklies:
        parts.append("<h2>周报</h2>")
        parts.append(_section(weeklies, "week", open_first=True))
    parts.append("<h2>日报</h2>")
    parts.append(_section(digests, "day", open_first=True) if digests
                 else '<p class=meta>暂无日报。</p>')
    parts.append(f"<script>{JS}</script></main></body></html>")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(parts), encoding="utf-8")
    return OUT
