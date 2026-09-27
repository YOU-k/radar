"""把 digests/、weekly/、background/ 渲染成卡片式移动站点 docs/。

GitHub Pages 直接以 main 分支 /docs 发布，零构建、零外部资源。
- docs/index.html：落地页，只放轻量内容。Tab：日报（默认）/ 周报 / 总览 / 资源库。
  日报内联最近 RECENT_DAYS 天，周报内联最近 RECENT_WEEKS 份；更早的进 docs/archive/。
- docs/bg/*.html：各方向完整报告、跨方向报告、深度调研各一页。总览里只内联一页总览和各方向 TL;DR，
  展开卡片时 fetch 对应页面的正文（#doc-rest）插进来；页面本身也能单独打开、分享。
- 所有 markdown 都走 _md()（先转义原始 HTML 再清掉 javascript:/data: 链接），之后的自动链接、[n] 引用链接、
  表格横滑容器都是在已净化的 HTML 上做的后处理。
- 前端状态（当前 tab、筛选、上次看到的日报日期）存 localStorage，所有读写都 try/catch。
"""
from __future__ import annotations

import hashlib
import html
import re
import shutil
from datetime import date
from pathlib import Path

import markdown

from .. import themes
from ..config import ROOT

DOCS = ROOT / "docs"
OUT = DOCS / "index.html"
RECENT_DAYS = 14
RECENT_WEEKS = 8

CSS = """
:root{color-scheme:light dark;--bg:#f6f8fa;--card:#fff;--fg:#1f2328;--muted:#57606a;--muted2:#4b5563;--border:#d0d7de;
--link:#0969da;--accent:#1f6feb;--green:#1a7f37;--purple:#8250df;--topbg:rgba(246,248,250,.94);--thbg:#f6f8fa;
--hi-bg:#dafbe1;--hi-fg:#1a7f37;--mid-bg:#fff8c5;--mid-fg:#9a6700;--lo-bg:#eaeef2;--lo-fg:#57606a;--res-bg:#ddf4ff;--res-fg:#0969da;
--pp-bg:#fff1e5;--pp-fg:#bc4c00;--new:#cf222e;--warn-bg:#fff8c5;--warn-fg:#9a6700;--shadow:0 1px 2px rgba(31,35,40,.04)}
@media (prefers-color-scheme:dark){:root{--bg:#0d1117;--card:#161b22;--fg:#e6edf3;--muted:#9198a1;--muted2:#b1bac4;--border:#30363d;
--link:#4493f8;--accent:#1f6feb;--green:#3fb950;--purple:#bc8cff;--topbg:rgba(13,17,23,.92);--thbg:#1c2128;
--hi-bg:#12361f;--hi-fg:#56d364;--mid-bg:#3a2e0a;--mid-fg:#e3b341;--lo-bg:#262c36;--lo-fg:#9198a1;--res-bg:#0c2d4b;--res-fg:#79c0ff;
--pp-bg:#3d1f0a;--pp-fg:#ffa657;--new:#ff7b72;--warn-bg:#3a2e0a;--warn-fg:#e3b341;--shadow:none}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.7 -apple-system,"PingFang SC","Noto Sans SC",sans-serif}
main{max-width:720px;margin:0 auto;padding:0 12px 80px}
a{color:var(--link);text-decoration:none}
a:active{opacity:.7}
[id]{scroll-margin-top:150px}
.top{position:sticky;top:0;z-index:9;background:var(--topbg);backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px);padding:12px 12px 10px;border-bottom:1px solid var(--border);margin:0 -12px 16px}
.top h1{font-size:17px;margin:0 0 2px}
.top .meta{color:var(--muted);font-size:12px;margin-bottom:10px}
.tabs{display:flex;gap:8px}
.tab{flex:1;text-align:center;padding:9px 0;border:1px solid var(--border);border-radius:20px;background:var(--card);color:var(--muted);font:600 14.5px/1.4 inherit;cursor:pointer;user-select:none;position:relative}
.tab.on{background:var(--accent);border-color:var(--accent);color:#fff}
.tab .nb{position:absolute;top:-6px;right:4px;background:var(--new);color:#fff;border-radius:9px;font-size:10.5px;line-height:17px;min-width:17px;padding:0 4px}
.panel{display:none}.panel.on{display:block}
details.bg{background:var(--card);border:1px solid var(--border);border-radius:12px;margin:0 0 10px;padding:0 16px}
details.bg>summary{cursor:pointer;list-style:none;padding:12px 0;font-weight:600;font-size:15px}
details.bg>summary::-webkit-details-marker{display:none}
details.bg>summary .cnt{display:block;font-weight:400;color:var(--muted);font-size:12px;margin-top:2px}
.bgbody{font-size:14.5px;padding-bottom:14px;overflow-wrap:anywhere}
.bgbody h2{font-size:15px;color:var(--green)}
.bgbody h3{font-size:14.5px;color:var(--purple);margin-bottom:4px}
.bgbody ol{padding-left:20px;font-size:13px;color:var(--muted2)}
.bgbody li:target{background:var(--mid-bg)}
a.cite{font-size:.85em;vertical-align:.1em}
a.full{display:inline-block;font-size:13px;margin-top:6px}
.lazy .empty{padding:10px 0}
#q{width:100%;padding:9px 14px;border:1px solid var(--border);border-radius:20px;background:var(--card);color:var(--fg);font-size:14px;outline:none;margin-bottom:12px}
#q:focus{border-color:var(--link)}
.wk{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:4px 16px 14px;margin:0 0 10px;font-size:14.5px;box-shadow:var(--shadow);overflow-wrap:anywhere}
.wk h2{font-size:15px;color:var(--green)}
.wk h3{font-size:14.5px;color:var(--purple);margin-bottom:4px}
.tw{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:8px 0;max-width:100%}
.tw table{border-collapse:collapse;font-size:12.5px;width:max-content;max-width:none}
.tw th,.tw td{border:1px solid var(--border);padding:4px 6px;text-align:left;vertical-align:top;min-width:7em;max-width:22em;overflow-wrap:anywhere}
.tw th{background:var(--thbg)}
details.day{margin:0 0 10px}
details.day>summary{cursor:pointer;list-style:none;display:flex;align-items:center;gap:8px;padding:11px 4px;border-bottom:1px solid var(--border);font-weight:600;font-size:15px}
details.day>summary::-webkit-details-marker{display:none}
details.day>summary .cnt{font-weight:400;color:var(--muted);font-size:12px;margin-left:auto}
details.day>summary::after{content:"›";color:var(--muted);transition:transform .15s}
details.day[open]>summary::after{transform:rotate(90deg)}
details.day>.daybody{padding-top:8px}
.newdot{display:none;font-size:11px;font-weight:700;color:#fff;background:var(--new);border-radius:8px;padding:0 6px;line-height:18px}
.isnew .newdot{display:inline-block}
.dom{color:var(--purple);font-size:13px;font-weight:600;margin:14px 2px 6px}
.card{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:11px 13px;margin:0 0 10px;box-shadow:var(--shadow)}
.card .t{font-size:15px;line-height:1.5}
.card .t a{color:var(--fg);font-weight:600}
.badge{display:inline-block;min-width:34px;text-align:center;font-size:12px;font-weight:700;border-radius:6px;padding:1px 6px;margin-left:6px;vertical-align:2px}
.badge.hi{background:var(--hi-bg);color:var(--hi-fg)}
.badge.mid{background:var(--mid-bg);color:var(--mid-fg)}
.badge.lo{background:var(--lo-bg);color:var(--lo-fg)}
.badge.res{background:var(--res-bg);color:var(--res-fg)}
.vt{display:inline-block;font-size:11px;font-weight:700;border-radius:4px;padding:0 5px;margin-right:4px}
.vt.jr{background:var(--hi-bg);color:var(--hi-fg)}
.vt.pp{background:var(--pp-bg);color:var(--pp-fg)}
.reason{color:var(--muted2);font-size:13.5px;margin-top:5px}
.meta{color:var(--muted);font-size:12px;margin-top:5px}
.legend{color:var(--muted);font-size:11.5px;margin:-4px 2px 10px}
.bgline{color:var(--purple);font-size:12.5px;margin-top:4px;border-left:3px solid var(--purple);padding-left:6px}
details.deep{margin-top:8px;border-top:1px dashed var(--border);padding-top:6px}
details.deep>summary{cursor:pointer;list-style:none;color:var(--link);font-size:13px;padding:4px 0}
details.deep>summary::-webkit-details-marker{display:none}
details.deep>summary::before{content:"▸ "}
details.deep[open]>summary::before{content:"▾ "}
details.deep .deepbody{font-size:13.5px;color:var(--muted2);padding-top:4px;overflow-wrap:anywhere}
details.deep .deepbody h2,details.deep .deepbody h3{font-size:13.5px;color:var(--green);margin:10px 0 2px}
details.deep .deepbody p{margin:4px 0}
.empty{color:var(--muted);font-size:13px;padding:6px 2px}
.hide{display:none!important}
.health{font-size:12px;color:var(--warn-fg);background:var(--warn-bg);border-radius:6px;padding:2px 8px;margin:2px 0 6px}
.sec{margin:18px 2px 8px}
.sec-t{font-size:15px;font-weight:700}
.sec-d{font-size:12.5px;color:var(--muted)}
a.ov{display:block;background:var(--card);border:1px solid var(--border);border-left:4px solid var(--border);border-radius:10px;padding:8px 12px;margin:0 0 8px;color:var(--fg);font-size:13px}
.ov-h{display:flex;align-items:center;flex-wrap:wrap;gap:2px}
.ov-n{font-weight:700;font-size:14px}
.ov-deep{margin-left:auto;font-size:11px;color:var(--link);border:1px solid var(--border);border-radius:8px;padding:0 6px}
.ov-s{color:var(--muted);font-size:12px;margin:2px 0}
.ov-l{margin-top:2px;line-height:1.5}
.ov-l b{color:var(--muted);font-weight:600;margin-right:4px}
details.bg.sub{border-style:dashed;margin:0 0 10px;background:var(--bg)}
.th{display:inline-block;font-size:11.5px;font-weight:600;border-radius:10px;padding:0 7px;margin:0 4px 2px 0;line-height:18px;white-space:nowrap;color:var(--c);background:var(--cb);border:1px solid var(--cl)}
.card.tagged{border-left:4px solid var(--tc,var(--border))}
.tags{margin-top:5px}
.fbar{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 10px}
.fchip{font:600 12.5px/1.4 inherit;border-radius:16px;padding:6px 12px;cursor:pointer;user-select:none;border:1px solid var(--cl,var(--border));background:var(--card);color:var(--c,var(--muted))}
.fchip.on{box-shadow:inset 0 0 0 2px currentColor}
.fchip .n{font-weight:400;opacity:.75;margin-left:3px}
@media (prefers-color-scheme:dark){.th[data-t],.fchip[data-t]{--c:var(--cd);--cb:var(--cbd)}}
.sum{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:8px 14px;margin:0 0 12px;font-size:14px}
.sum h4{margin:4px 0 2px;font-size:13px;color:var(--muted)}
.sum ul{margin:4px 0;padding-left:18px}
.sum li{margin:3px 0}
.pri{font-size:13px;font-weight:700;margin:16px 2px 6px}
.pri.p0{color:var(--new)}.pri.p1{color:var(--mid-fg)}.pri.p2{color:var(--muted)}.pri.pn{color:var(--link)}
.rcard{background:var(--card);border:1px solid var(--border);border-radius:10px;padding:8px 12px;margin:0 0 8px;font-size:13.5px;overflow-wrap:anywhere}
.rcard .rn{font-weight:700;font-size:14.5px}
.rcard .rk{font-size:11.5px;color:var(--muted);border:1px solid var(--border);border-radius:4px;padding:0 4px;margin-left:6px;font-weight:400}
.rcard .why{color:var(--fg);margin-top:3px}
.rcard .rm{color:var(--muted);font-size:12px;margin-top:3px}
.rcard.new{border-style:dashed}
.st{display:inline-block;font-size:11px;border-radius:4px;padding:0 5px;margin-left:4px;font-weight:600}
.st.ok{background:var(--hi-bg);color:var(--hi-fg)}.st.warn{background:var(--mid-bg);color:var(--mid-fg)}.st.bad{background:var(--pp-bg);color:var(--pp-fg)}
.arch{margin:16px 2px;font-size:13.5px}
.arch a{display:inline-block;margin:4px 10px 4px 0}
.back{display:inline-block;margin:10px 0}
"""

JS = r"""
const LS={get(k){try{return JSON.parse(localStorage.getItem('radar.'+k))}catch(e){return null}},
  set(k,v){try{localStorage.setItem('radar.'+k,JSON.stringify(v))}catch(e){}}};
const SS={get(k){try{return JSON.parse(sessionStorage.getItem('radar.'+k))}catch(e){return null}},
  set(k,v){try{sessionStorage.setItem('radar.'+k,JSON.stringify(v))}catch(e){}}};
const state=Object.assign({tab:'day',dayTheme:'',q:'',resTheme:'',resKind:''},LS.get('state')||{});
function save(){LS.set('state',state)}
const tabs=[...document.querySelectorAll('.tab')];
function showTab(name,push){
  if(!document.getElementById('panel-'+name))name='day';
  tabs.forEach(t=>{const on=t.dataset.tab===name;t.classList.toggle('on',on);t.setAttribute('aria-selected',on)});
  document.querySelectorAll('.panel').forEach(p=>p.classList.toggle('on',p.id==='panel-'+name));
  state.tab=name;save();
  if(push!==false){try{history.replaceState(null,'','#'+name)}catch(e){}}
}
tabs.forEach(t=>t.addEventListener('click',()=>showTab(t.dataset.tab)));
/* 懒加载：details[data-src] 展开时 fetch 对应页面的 #doc-rest */
function load(d){
  if(d._p)return d._p;
  const box=d.querySelector(':scope>.bgbody>.lazy');
  if(!box)return Promise.resolve();
  d._p=fetch(d.dataset.src).then(r=>{if(!r.ok)throw new Error(r.status);return r.text()}).then(t=>{
    const doc=new DOMParser().parseFromString(t,'text/html');const a=doc.getElementById('doc-rest');
    box.innerHTML=a?a.innerHTML:'<div class="empty">全文为空。</div>';
  }).catch(()=>{d._p=null;box.innerHTML='<div class="empty">加载失败（离线或本地打开）。<a href="'+d.dataset.src+'">打开全文页</a></div>'});
  return d._p;
}
document.querySelectorAll('details[data-src]').forEach(d=>d.addEventListener('toggle',()=>{if(d.open)load(d)}));
function openTo(id){
  const t=document.getElementById(id);if(!t)return;
  let p=t;while(p){if(p.tagName==='DETAILS'){p.open=true;if(p.dataset.src)load(p)}p=p.parentElement}
  const pn=t.closest('.panel');if(pn)showTab(pn.id.slice(6),false);
  setTimeout(()=>t.scrollIntoView({block:'start'}),30);
}
document.addEventListener('click',e=>{
  const a=e.target.closest('a.cite,a.ov');if(!a)return;
  const id=a.getAttribute('href').slice(1);e.preventDefault();
  if(document.getElementById(id)){openTo(id);return}
  const d=a.closest('details[data-src]');
  if(d){d.open=true;load(d).then(()=>openTo(id))}
});
/* 上次访问以来的新内容：按日报日期 / 周报编号比较；同一会话内保持标记不消失 */
const days=[...document.querySelectorAll('details.day')];
const newestDay=days.length?days[0].dataset.date:'';
let prevDay=SS.get('prevDay');
if(prevDay===null){prevDay=LS.get('seenDay')||'';SS.set('prevDay',prevDay)}
const weeks=[...document.querySelectorAll('.wk[data-week]')];
let prevWeek=SS.get('prevWeek');
if(prevWeek===null){prevWeek=LS.get('seenWeek')||'';SS.set('prevWeek',prevWeek)}
let nNew=0;
if(prevDay){days.forEach(d=>{if(d.dataset.date>prevDay){d.classList.add('isnew');nNew+=d.querySelectorAll('.card').length}})}
if(prevWeek){weeks.forEach(w=>{if(w.dataset.week>prevWeek)w.classList.add('isnew')})}
function badge(tab,n){const t=tabs.find(x=>x.dataset.tab===tab);if(t&&n){const s=document.createElement('span');s.className='nb';s.textContent=n;t.appendChild(s)}}
badge('day',nNew);badge('week',prevWeek?weeks.filter(w=>w.classList.contains('isnew')).length:0);
if(newestDay)LS.set('seenDay',newestDay);
if(weeks.length)LS.set('seenWeek',weeks[0].dataset.week);
LS.set('lastVisit',new Date().toISOString());
/* 日报筛选 */
const q=document.getElementById('q');
function applyDay(){
  const s=(q?q.value:'').trim().toLowerCase();const th=state.dayTheme;const active=s||th;
  days.forEach(d=>{
    let n=0,tot=0;
    d.querySelectorAll('.card').forEach(c=>{
      const hit=(!s||c.textContent.toLowerCase().includes(s))&&(!th||(' '+c.dataset.themes+' ').includes(' '+th+' '));
      c.classList.toggle('hide',!hit);tot++;if(hit)n++;
    });
    d.querySelectorAll('.dom').forEach(g=>{
      let x=g.nextElementSibling,has=false;
      while(x&&x.classList.contains('card')){if(!x.classList.contains('hide'))has=true;x=x.nextElementSibling}
      g.classList.toggle('hide',!has);
    });
    d.querySelectorAll('.sum li').forEach(li=>li.classList.toggle('hide',!!th&&!(' '+(li.dataset.themes||'')+' ').includes(' '+th+' ')));
    const c=d.querySelector('summary .cnt');if(c)c.textContent=active?n+' / '+tot+' 条':tot+' 条';
    d.classList.toggle('hide',!n&&!!active);
    if(active)d.open=n>0;else d.open=d.dataset.first==='1';
  });
}
if(q){q.value=state.q||'';q.addEventListener('input',()=>{state.q=q.value;save();applyDay()})}
function bindChips(bar,key,after){
  if(!bar)return;
  const chips=[...bar.querySelectorAll('.fchip')];
  const paint=()=>chips.forEach(x=>{const on=x.dataset.v===state[key];x.classList.toggle('on',on);x.setAttribute('aria-pressed',on)});
  if(state[key]&&!chips.some(x=>x.dataset.v===state[key]))state[key]='';
  paint();
  chips.forEach(c=>c.addEventListener('click',()=>{state[key]=state[key]===c.dataset.v?'':c.dataset.v;save();paint();after()}));
}
bindChips(document.getElementById('fbar-day'),'dayTheme',applyDay);
function applyRes(){
  document.querySelectorAll('.rcard').forEach(c=>{
    const hit=(!state.resTheme||(' '+c.dataset.themes+' ').includes(' '+state.resTheme+' '))&&(!state.resKind||c.dataset.kind===state.resKind);
    c.classList.toggle('hide',!hit);
  });
  document.querySelectorAll('.rgroup').forEach(g=>g.classList.toggle('hide',!g.querySelector('.rcard:not(.hide)')));
}
function initRes(){
  bindChips(document.getElementById('fbar-res'),'resTheme',applyRes);
  bindChips(document.getElementById('fbar-kind'),'resKind',applyRes);
  if(state.resTheme||state.resKind)applyRes();
}
/* 资源库单独成页：第一次切到该 tab 再 fetch */
let resP=null;
function loadRes(){
  const box=document.getElementById('res-lazy');
  if(!box){if(!resP){resP=Promise.resolve();initRes()}return resP}
  if(resP)return resP;
  resP=fetch(box.dataset.src).then(r=>{if(!r.ok)throw new Error(r.status);return r.text()}).then(t=>{
    const doc=new DOMParser().parseFromString(t,'text/html');const a=doc.getElementById('doc-rest');
    box.innerHTML=a?a.innerHTML:'';initRes();
  }).catch(()=>{resP=null;box.innerHTML='<div class="empty">加载失败（离线或本地打开）。<a href="'+box.dataset.src+'">打开资源库页</a></div>'});
  return resP;
}
tabs.forEach(t=>t.addEventListener('click',()=>{if(t.dataset.tab==='res')loadRes()}));
if(days.length&&(state.dayTheme||state.q))applyDay();
/* 初始 tab：URL #hash 优先（#day/#week/#bg/#res 或 #topic-x），否则上次的 tab，默认日报 */
const h=decodeURIComponent(location.hash.slice(1));
if(h&&document.getElementById('panel-'+h))showTab(h);
else if(h&&document.getElementById(h)){showTab(state.tab,false);openTo(h)}
else showTab(tabs.length?state.tab:'day',false);
if(state.tab==='res')loadRes();
"""

ITEM_RE = re.compile(
    r"^- \*\*\[(?P<title>.+?)\]\((?P<url>(?:[^()\s]|\([^()\s]*\))+)\)\*\*"
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
EXT = ' target="_blank" rel="noopener"'

_BAD_HREF = re.compile(r'(href|src)="\s*(?:javascript|data|vbscript):[^"]*"', re.I)


def _md(text: str, extensions: list[str]) -> str:
    """markdown → HTML，防存储型 XSS：先把原始 HTML 当文本转义（本站 markdown 源都不需要内嵌 HTML；
    标题、摘要与 LLM 输出都来自不可信来源），再清掉 javascript:/data: 链接。"""
    out = markdown.markdown(text.replace("<", "&lt;"), extensions=extensions)
    return _BAD_HREF.sub(r'\1="#"', out)


# ---------------- 已净化 HTML 的后处理 ----------------

_TAG_SPLIT = re.compile(r"(<[^>]+>)")
_URL = re.compile(r"https?://[^\s<>\"'　-〿＀-￯一-鿿]+")
_CITE = re.compile(r"\[(\d{1,3}(?:\s*[,，、]\s*\d{1,3})*)\]")


def _map_text(h: str, fn) -> str:
    """只对 <a>…</a>、<code>、<pre> 之外的文本段调用 fn。"""
    out, skip = [], 0
    for part in _TAG_SPLIT.split(h):
        if part.startswith("<"):
            m = re.match(r"<(/?)(a|code|pre)\b", part, re.I)
            if m:
                skip += -1 if m.group(1) else 1
                skip = max(skip, 0)
            out.append(part)
        else:
            out.append(fn(part) if skip == 0 and part else part)
    return "".join(out)


def _trim_url(u: str) -> tuple[str, str]:
    tail = ""
    while u and u[-1] in ".,;:!?)]}'\"":
        if u[-1] == ")" and u.count("(") >= u.count(")"):
            break
        tail = u[-1] + tail
        u = u[:-1]
    return u, tail


def linkify(h: str) -> str:
    """裸 URL → 可点链接（新窗口）。"""
    def fn(text: str) -> str:
        def rep(m):
            u, tail = _trim_url(m.group(0))
            return f'<a href="{u}"{EXT}>{u}</a>{tail}' if len(u) > 10 else m.group(0)
        return _URL.sub(rep, text)
    return _map_text(h, fn)


def external_links(h: str) -> str:
    """markdown 生成的外链也在新窗口打开，读完论文不丢位置。"""
    return re.sub(r'<a href="(https?://[^"]+)"(?![^>]*target=)', r'<a href="\1"' + EXT, h)


def wrap_tables(h: str) -> str:
    return re.sub(r"<table>(.*?)</table>", r'<div class="tw"><table>\1</table></div>', h, flags=re.S)


def link_citations(h: str, scope: str) -> str:
    """'## 参考文献' 下的有序列表条目加锚点 ref-<scope>-<n>，正文里的 [n] / [n, m] 链到对应条目。
    没有参考文献表的（深度调研用作者-年份引用）原样返回。"""
    m = re.search(r"<h2>参考文献</h2>\s*<ol(?: start=\"(\d+)\")?>(.*?)</ol>", h, re.S)
    if not m:
        return h
    start = int(m.group(1) or 1)
    n_refs = 0

    def add_id(mm):
        nonlocal n_refs
        n_refs += 1
        return f'<li id="ref-{scope}-{start + n_refs - 1}">'
    ol = re.sub(r"<li>", add_id, m.group(2))
    body, refs = h[:m.start()], h[m.start():m.start(2)] + ol + h[m.end(2):]
    valid = range(start, start + n_refs)

    def fn(text: str) -> str:
        def rep(mm):
            nums = [int(x) for x in re.split(r"\s*[,，、]\s*", mm.group(1))]
            if not all(n in valid for n in nums):
                return mm.group(0)
            return "[" + ", ".join(f'<a class="cite" href="#ref-{scope}-{n}">{n}</a>' for n in nums) + "]"
        return _CITE.sub(rep, text)
    return _map_text(body, fn) + refs


def post(h: str, scope: str = "") -> str:
    """净化后的 markdown HTML → 表格横滑、裸链接可点、外链新窗口、[n] 引用可点。"""
    h = wrap_tables(external_links(linkify(h)))
    return link_citations(h, scope) if scope else h


# ---------------- 主题标签 ----------------

def _lighten(hexc: str, f: float = 0.45) -> str:
    """暗色模式下主题色调亮，保证在深底上可读。"""
    try:
        r, g, b = (int(hexc[i:i + 2], 16) for i in (1, 3, 5))
    except ValueError:
        return hexc
    return "#%02x%02x%02x" % tuple(int(c + (255 - c) * f) for c in (r, g, b))


def _cvars(c: str) -> str:
    d = _lighten(c)
    return f"--c:{c};--cb:{c}14;--cl:{c}55;--cd:{d};--cbd:{d}1f"


def theme_css() -> str:
    """每个主题一条 .t-<key> 规则（颜色变量），标签只带 class，不再每个内联 style。"""
    return "".join(f"[data-t={t['key']}]{{{_cvars(t['color'])}}}" for t in themes.load_themes())


def _chip(key: str) -> str:
    t = themes.by_key().get(key)
    if not t:
        return ""
    return f'<span class="th" data-t="{key}">{html.escape(t["label"])}</span>'


def _chips_html(keys_: list[str]) -> str:
    return "".join(_chip(k) for k in keys_)


def _filter_bar(bar_id: str, counts: dict[str, int]) -> str:
    """主题筛选条：只列有条目的主题，点一下只看该主题，再点取消。"""
    out = [f'<div class="fbar" id="{bar_id}">']
    for t in themes.load_themes():
        n = counts.get(t["key"], 0)
        if not n:
            continue
        out.append(f'<button type="button" class="fchip" data-t="{t["key"]}" aria-pressed="false" data-v="{t["key"]}">'
                   f'{html.escape(t["label"])}<span class="n">{n}</span></button>')
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
        items.append(f'<li data-themes="{" ".join(keys_)}">{_chips_html(keys_)}{body}</li>')
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
                    it["deep"] = post(_md(body, extensions=["extra"]))
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
                     f'<div class="t"><a href="{html.escape(it["url"])}"{EXT}>'
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
    return (f'<details class="day" data-date="{html.escape(path.stem)}" data-first="{1 if first else 0}"{open_attr}>'
            f'<summary>{html.escape(label)}<span class="newdot">新</span><span class="cnt">{total} 条</span></summary>'
            f'<div class="daybody">{body}</div></details>')


def _render_weekly(path: Path) -> str:
    text = re.sub(r"\A# [^\n]*\n+", "", path.read_text(encoding="utf-8"))
    text = re.sub(r"^# ", "## ", text, flags=re.M)  # 正文里多余的 H1 降级，手机上不出巨型标题
    body = post(_md(text, extensions=["extra", "sane_lists"]))
    return (f'<div class="wk" data-week="{html.escape(path.stem)}"><h3>{html.escape(path.stem)}'
            f' <span class="newdot">新</span></h3>{body}</div>')


BG_HEAD_RE = re.compile(r"^# (?P<name>.+?) · 方向背景报告\n+(?P<stats>[^\n]+)", re.M)
SPLIT = "RADARSPLITTLDR7F3"
TLDR_RE = re.compile(r"^## 摘要[^\n]*\n.*?(?=^## |\Z)", re.S | re.M)


def _page_name(label: str) -> str:
    return re.sub(r"[^a-z0-9-]+", "-", label.lower()).strip("-") or hashlib.md5(label.encode()).hexdigest()[:8]


def _render_background(report: Path, title: str = "", chip: str = "", anchor: str = "", prefix: str = "",
                       pages: dict | None = None, page: str = "", scope: str = "") -> str:
    """background/<slug>/report.md → 折叠卡片；标题行取方向名（或 title），副行取统计行；prefix 放在正文前（深度调研）。

    pages 为 None：全文内联（旧行为）。否则全文写成 docs/bg/<page>.html（pages[路径] = (标题, tldr, 其余)），
    卡片里只内联 TL;DR，展开时再 fetch 其余部分。"""
    text = report.read_text(encoding="utf-8")
    m = BG_HEAD_RE.match(text)
    name = title or (m.group("name") if m else report.parent.name)
    stats = m.group("stats") if m else ""
    body = text[m.end():] if m else text
    ident = f' id="{anchor}"' if anchor else ""
    head = (f'<summary>{_chip(chip) if chip else ""}{html.escape(name)}'
            f'<span class="cnt">{html.escape(stats)}</span></summary>')
    scope = scope or chip or _page_name(page or name)
    if pages is None:
        html_body = post(_md(body, extensions=["extra", "sane_lists", "tables"]), scope)
        return f'<details class="bg"{ident}>{head}<div class="bgbody">{prefix}{html_body}</div></details>'
    tm = TLDR_RE.search(body)
    tldr_md = tm.group(0) if tm else ""
    rest_md = (body[:tm.start()] + body[tm.end():]) if tm else body
    # 引用编号与参考文献在同一份 HTML 里才能配对：整篇转换后再按 TL;DR 边界切开
    full = post(_md(tldr_md + f"\n\n{SPLIT}\n\n" + rest_md, extensions=["extra", "sane_lists", "tables"]), scope)
    tldr_html, _, rest_html = full.partition(f"<p>{SPLIT}</p>")
    if not rest_html:
        tldr_html, rest_html = "", full
    src = f"bg/{page}.html"
    pages[src] = (name, stats, tldr_html, rest_html)
    return (f'<details class="bg"{ident} data-src="{src}">{head}<div class="bgbody">{prefix}{tldr_html}'
            f'<div class="lazy"><div class="empty">正在加载全文…</div></div>'
            f'<a class="full" href="{src}"{EXT}>单独打开全文 →</a></div></details>')


KIND_ZH = {"dataset": "数据集", "model": "模型", "benchmark": "基准", "database": "数据库", "tool": "工具"}
PRI_ZH = {"P0": "P0 优先上手", "P1": "P1 值得登记", "P2": "P2 了解即可"}


def _res_card(r: dict, new: bool = False) -> str:
    from ..background.resources import OPEN_ZH, VERIFIED_ZH
    m = re.search(r"https?://\S+", r.get("access", "") or r.get("url", ""))
    name = html.escape(r["name"])
    name = f'<a href="{html.escape(m.group(0))}"{EXT}>{name}</a>' if m else name
    scale = r.get("scale", "")
    if scale and r.get("scale_src") == "paper":
        scale += "（据引用文献）"
    op = r.get("open", "unknown") or "unknown"
    ver = r.get("verified", "") or ("unverified" if new else "")
    st_cls = {"ok": "ok", "mismatch": "bad", "dead": "bad", "blocked": "warn"}.get(ver, "warn")
    status = (f'<span class="st {st_cls}">{VERIFIED_ZH.get(ver, ver)}</span>' if ver and ver != "n/a" else "")
    bits = [r.get("modality", ""), scale, OPEN_ZH.get(op, op)]
    if r.get("used_by"):
        bits.append(f"证据 {len(r['used_by'])} 篇")
    if new:
        bits.append(f"日报 {r.get('added') or r.get('day', '')}")
    meta = " · ".join(b for b in bits if b)
    why = r.get("why") or r.get("note", "")
    tks = r.get("themes") or ([r["theme"]] if r.get("theme") else [])
    color = themes.by_key().get(tks[0], {}).get("color", "") if tks else ""
    style = f' style="border-left:4px solid {color}"' if color else ""
    kind = r.get("kind", "dataset")
    return (f'<div class="rcard{" new" if new else ""}"{style} data-themes="{" ".join(tks)}" data-kind="{html.escape(kind)}">'
            f'<div class="rn">{name}<span class="rk">{KIND_ZH.get(kind, html.escape(kind))}</span>{status}</div>'
            f'<div class="tags">{_chips_html(tks)}</div>'
            f'<div class="why">{html.escape(why)}</div><div class="rm">{html.escape(meta)}</div></div>')


def _render_resources(reg_path: Path, inbox_path: Path | None = None) -> str:
    """registry.json → 按优先级分组的资源卡片 + 主题 / 类型筛选条；再列日报收件箱里的新发现（未核验）。"""
    import json
    from ..background.resources import is_core, resolve_key
    reg = json.loads(reg_path.read_text(encoding="utf-8")) if reg_path.exists() else {}
    rows = [r for r in reg.values() if is_core(r)]
    new = [r for r in reg.values() if r.get("status") == "new"]
    if inbox_path and inbox_path.exists():
        try:
            for e in json.loads(inbox_path.read_text(encoding="utf-8")):
                key, _ = resolve_key(e.get("name", ""), e.get("kind", ""))
                if key and key not in reg:
                    new.append({**e, "added": e.get("day", "")})
        except (ValueError, TypeError):
            pass
    new.sort(key=lambda r: r.get("added", ""), reverse=True)
    if not rows and not new:
        return ""
    counts: dict[str, int] = {}
    for r in rows + new:
        for k in r.get("themes") or ([r["theme"]] if r.get("theme") else []):
            counts[k] = counts.get(k, 0) + 1
    kinds = [k for k in KIND_ZH if any(r.get("kind") == k for r in rows + new)]
    kind_bar = ('<div class="fbar" id="fbar-kind">' + "".join(
        f'<button type="button" class="fchip" aria-pressed="false" data-v="{k}">{KIND_ZH[k]}<span class="n">'
        f'{sum(r.get("kind") == k for r in rows + new)}</span></button>' for k in kinds) + "</div>")
    out = [f'<div class="meta" style="margin:0 2px 8px">主表 {len(rows)} 项 · 日报新发现 {len(new)} 项（未核验）· '
           f'按你的应用线排优先级；规模、开放性以人工种子为准，其余标注来源。点主题/类型筛选，再点取消</div>',
           _filter_bar("fbar-res", counts), kind_bar]
    for pr in ("P0", "P1", "P2"):
        sub = [r for r in rows if (r.get("priority") if r.get("priority") in PRI_ZH else "P2") == pr]
        if not sub:
            continue
        sub.sort(key=lambda r: (not r.get("pinned"), -len(r.get("themes", [])), -len(r.get("used_by", [])),
                                r["name"].lower()))
        out.append(f'<div class="rgroup"><div class="pri {pr.lower()}">{PRI_ZH[pr]}（{len(sub)}）</div>'
                   + "".join(_res_card(r) for r in sub) + "</div>")
    if new:
        out.append(f'<div class="rgroup"><div class="pri pn">新发现 · 未核验（{len(new)}）'
                   f'<span class="sec-d"> 日报自动收录，每周并入登记表后核验</span></div>'
                   + "".join(_res_card(r, new=True) for r in new[:40]) + "</div>")
    return "\n".join(out)


def _day_theme_counts(paths: list[Path]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for p in paths:
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.startswith("  <sub>主题："):
                for k in themes.parse_line(line[len("  <sub>主题："):-len("</sub>")]):
                    counts[k] = counts.get(k, 0) + 1
    return counts


def _render_deep(path: Path, nested: bool = False, pages: dict | None = None, label: str = "") -> str:
    """background/<slug>/deep/*.md：会话里用 deep-research + expert-panel 做的深度调研（人工触发，不自动更新）。"""
    text = path.read_text(encoding="utf-8")
    m = re.match(r"# (?P<t>[^\n]+)\n", text)
    title = m.group("t") if m else path.stem
    body = text[m.end():] if m else text
    stats = f"深度调研 · {label or path.parent.parent.name} · {path.name[:10]}"
    cls = "bg sub" if nested else "bg"
    head = (f'<summary>深度调研：{html.escape(title)}'
            f'<span class="cnt">{html.escape(stats)}</span></summary>')
    html_body = post(_md(body, extensions=["extra", "sane_lists", "tables"]))
    if pages is None:
        return f'<details class="{cls}">{head}<div class="bgbody">{html_body}</div></details>'
    src = f"bg/{_page_name(path.parent.parent.name)}-deep-{hashlib.md5(path.name.encode()).hexdigest()[:8]}.html"
    pages[src] = (title, stats, "", html_body)
    return (f'<details class="{cls}" data-src="{src}">{head}<div class="bgbody">'
            f'<div class="lazy"><div class="empty">正在加载全文…</div></div>'
            f'<a class="full" href="{src}"{EXT}>单独打开全文 →</a></div></details>')


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


def _render_overview(pages: dict | None = None) -> tuple[str, int]:
    """总览页三层：一页总览（每主题一张小卡）→ 跨方向（为什么 / 做什么）→ 各方向（深度调研收在所属方向里）。
    pages 不为 None 时，完整报告写成独立页面按需加载（见 _render_background）。"""
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

    out = [SECTION.format(t="一页总览", d="每个主题一行：处在什么阶段、真正要回答的问题、卡在哪。点主题名跳到该方向的报告。")]
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
    for path, label, page in ((principles, "为什么 · 全局判断（第一性原理）", "principles"),
                              (joint, "做什么 · 联合行动建议", "joint")):
        if path.exists():
            out.append(_render_background(path, title=label, pages=pages, page=page))

    out.append(SECTION.format(t="各方向", d="每个方向一份证据综述（每周吃日报增量重编）。卡片里先给 TL;DR，展开后加载全文；有深度调研的放在最上面。"))
    for t, name, rp, stats, deep in topics:
        extra = "".join(_render_deep(p, nested=True, pages=pages, label=t["label"]) for p in deep)
        out.append(_render_background(rp, title=name, chip=t["key"], anchor=f"topic-{t['key']}", prefix=extra,
                                      pages=pages, page=_page_name(t["key"])))
    return "\n".join(out), len(topics)


def _health_html(today: date) -> str:
    """data/health.json（日报运行写入）有问题且是近两天的，就在页头提示一行。"""
    import json
    p = ROOT / "data" / "health.json"
    if not p.exists():
        return ""
    try:
        h = json.loads(p.read_text(encoding="utf-8"))
        if (today - date.fromisoformat(h.get("date", "1970-01-01"))).days > 2 or not h.get("problems"):
            return ""
        return (f'<div class="health">采集提示（{html.escape(h["date"])}）：'
                f'{html.escape("；".join(h["problems"][:4]))}</div>')
    except Exception:
        return ""


HEAD = ('<!doctype html><html lang=zh><head><meta charset=utf-8>'
        '<meta name=viewport content="width=device-width,initial-scale=1">'
        '<meta name=color-scheme content="light dark"><title>{title}</title>'
        '<style>{css}</style></head><body><main>')


def _head(title: str) -> str:
    return HEAD.format(title=title, css=CSS + theme_css())


def _standalone(title: str, sub: str, body: str, back: str = "../index.html") -> str:
    return (_head(html.escape(title) + " · radar")
            + f'<a class="back" href="{back}">← 返回 radar</a>'
            + f'<h1 style="font-size:18px;margin:4px 0">{html.escape(title)}</h1>'
            + (f'<div class="meta">{html.escape(sub)}</div>' if sub else "")
            + body + "</main></body></html>")


def _write_pages(pages: dict) -> None:
    for rel, (title, stats, tldr, rest) in pages.items():
        body = (f'<article class="bgbody" id="doc">{f"<section id=doc-tldr>{tldr}</section>" if tldr else ""}'
                f'<section id="doc-rest">{rest}</section></article>')
        p = DOCS / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(_standalone(title, stats, body), encoding="utf-8")


def _write_archives(old_digests: list[Path], old_weeklies: list[Path]) -> list[tuple[str, str, int]]:
    """较早的日报按月、较早的周报合成一页，写到 docs/archive/。返回 [(链接, 标题, 份数)]。"""
    links = []
    by_month: dict[str, list[Path]] = {}
    for p in old_digests:
        by_month.setdefault(p.stem[:7], []).append(p)
    for month, ps in sorted(by_month.items(), reverse=True):
        body = "\n".join(_render_digest(p, False) for p in ps)
        (DOCS / "archive").mkdir(parents=True, exist_ok=True)
        (DOCS / "archive" / f"{month}.html").write_text(
            _standalone(f"日报归档 {month}", f"{len(ps)} 份日报", body), encoding="utf-8")
        links.append((f"archive/{month}.html", f"{month} 日报", len(ps)))
    if old_weeklies:
        body = "\n".join(_render_weekly(p) for p in old_weeklies)
        (DOCS / "archive").mkdir(parents=True, exist_ok=True)
        (DOCS / "archive" / "weekly.html").write_text(
            _standalone("周报归档", f"{len(old_weeklies)} 份周报", body), encoding="utf-8")
        links.append(("archive/weekly.html", "更早的周报", len(old_weeklies)))
    return links


def build_site(today: date | None = None) -> Path:
    today = today or date.today()
    digests = sorted((ROOT / "digests").glob("*.md"), reverse=True)
    weeklies = sorted((ROOT / "weekly").glob("*.md"), reverse=True)
    recent_d, old_d = digests[:RECENT_DAYS], digests[RECENT_DAYS:]
    recent_w, old_w = weeklies[:RECENT_WEEKS], weeklies[RECENT_WEEKS:]

    for sub in ("bg", "archive"):  # 生成物目录整体重建，删掉过期页面
        shutil.rmtree(DOCS / sub, ignore_errors=True)
    arch = _write_archives(old_d, old_w)
    arch_d = [a for a in arch if a[0] != "archive/weekly.html"]
    arch_w = [a for a in arch if a[0] == "archive/weekly.html"]

    def arch_html(items):
        return ('<div class="arch">更早：' + "".join(
            f'<a href="{h}">{html.escape(t)}（{n}）</a>' for h, t, n in items) + "</div>") if items else ""

    week_html = ("\n".join(_render_weekly(p) for p in recent_w)
                 if weeklies else '<div class="empty">暂无周报。</div>') + arch_html(arch_w)
    day_html = ("\n".join(_render_digest(p, i == 0) for i, p in enumerate(recent_d))
                if digests else '<div class="empty">暂无日报。</div>') + arch_html(arch_d)
    pages: dict = {}
    bg_html, n_topics = _render_overview(pages)
    _write_pages(pages)
    reg_json = ROOT / "background" / "_resources" / "registry.json"
    res_body = _render_resources(reg_json, ROOT / "data" / "resources_inbox.json")
    if res_body:  # 资源库单独成页，切到该 tab 时再加载，落地页不背这 100 KB
        (DOCS / "res.html").write_text(
            _standalone("资源库", "数据集 / 模型 / 基准登记", f'<div id="doc-rest">{res_body}</div>',
                        back="index.html"), encoding="utf-8")
        res_html = ('<div class="lazy" id="res-lazy" data-src="res.html"><div class="empty">正在加载资源库…</div></div>'
                    f'<a class="full" href="res.html"{EXT}>单独打开资源库 →</a>')
    else:
        (DOCS / "res.html").unlink(missing_ok=True)
        res_html = '<div class="empty">暂无资源条目。</div>'

    parts = [
        _head("radar · 科研情报"),
        '<div class="top"><h1>radar · 科研情报</h1>',
        _health_html(today),
        f'<div class="meta">构建 {today.isoformat()} · 最新日报 {digests[0].stem if digests else "—"} · '
        f'{len(digests)} 份日报 / {len(weeklies)} 份周报 / {n_topics} 个方向</div>',
        '<div class="tabs" role="tablist">'
        '<button type="button" role="tab" class="tab on" data-tab="day">日报</button>'
        '<button type="button" role="tab" class="tab" data-tab="week">周报</button>'
        '<button type="button" role="tab" class="tab" data-tab="bg">总览</button>'
        '<button type="button" role="tab" class="tab" data-tab="res">资源库</button>'
        "</div></div>",
        '<div id="panel-day" class="panel on">',
        _filter_bar("fbar-day", _day_theme_counts(recent_d)),
        '<div class="legend">分数 = 与你方向的相关度（0–10，≥7.5 绿）· 期刊/预印本 · 左色条 = 主题 · 红色"新" = 上次访问后新增</div>',
        f'<input id=q placeholder="过滤最近 {len(recent_d)} 天的条目（标题 / 关键词）…">',
        f"{day_html}</div>",
        f'<div id="panel-week" class="panel">{week_html}</div>',
        f'<div id="panel-bg" class="panel">{bg_html}</div>',
        f'<div id="panel-res" class="panel">{res_html}</div>',
        f"<script>{JS}</script></main></body></html>",
    ]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(parts), encoding="utf-8")
    return OUT
