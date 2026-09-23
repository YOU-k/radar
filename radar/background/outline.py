"""动态大纲：节树 + 每节挂的证据 id。markdown 往返；LLM 只输出操作，程序执行。

outline.md 格式：
  ## 1 背景与定义
  ### 1.1 xxx
  - doi:10.xxx
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from .llmio import LLM, parse_json_array, tagged
from .models import Evidence
from .spec import TopicSpec

UNSORTED = "未归类新证据"
SYNTHESIS_HINTS = ("背景", "定义", "趋势", "空白", "结论", "展望")


def is_synthesis_title(title: str) -> bool:
    """综合节：由全部证据与正文综合而成，不挂具体论文（背景与定义、空白与趋势）。"""
    return any(h in title for h in SYNTHESIS_HINTS)


@dataclass
class Section:
    id: str
    title: str
    evidence_ids: list[str] = field(default_factory=list)
    children: list["Section"] = field(default_factory=list)


class Outline:
    def __init__(self, sections: list[Section] | None = None):
        self.sections = sections or []

    # ---- 构造 ----
    @classmethod
    def from_spec(cls, spec: TopicSpec) -> "Outline":
        def build(nodes: list[dict], prefix: str) -> list[Section]:
            out = []
            for i, n in enumerate(nodes, 1):
                sid = f"{prefix}{i}"
                out.append(Section(id=sid, title=str(n.get("title", sid)),
                                   children=build(n.get("children") or [], sid + ".")))
            return out
        skeleton = spec.outline or [{"title": "背景与定义"}, {"title": "方法学"},
                                    {"title": "数据与资源"}, {"title": "应用与结果"},
                                    {"title": "评测、争议与空白"}]
        return cls(build(skeleton, ""))

    @classmethod
    def from_markdown(cls, text: str) -> "Outline":
        root: list[Section] = []
        stack: list[tuple[int, Section]] = []
        for line in text.splitlines():
            m = re.match(r"^(#{2,4})\s+(\S+)\s+(.*)$", line)
            if m:
                level = len(m.group(1))
                sec = Section(id=m.group(2), title=m.group(3).strip())
                while stack and stack[-1][0] >= level:
                    stack.pop()
                (stack[-1][1].children if stack else root).append(sec)
                stack.append((level, sec))
                continue
            m = re.match(r"^\s*-\s+(\S+)\s*$", line)
            if m and stack:
                stack[-1][1].evidence_ids.append(m.group(1))
        return cls(root)

    def to_markdown(self) -> str:
        lines = []
        def emit(secs: list[Section], level: int):
            for s in secs:
                lines.append(f"{'#' * level} {s.id} {s.title}")
                lines.extend(f"- {e}" for e in s.evidence_ids)
                lines.append("")
                emit(s.children, level + 1)
        emit(self.sections, 2)
        return "\n".join(lines).rstrip() + "\n"

    # ---- 查询 / 操作（确定性） ----
    def walk(self) -> list[Section]:
        out = []
        def rec(secs):
            for s in secs:
                out.append(s)
                rec(s.children)
        rec(self.sections)
        return out

    def find(self, sid: str) -> Section | None:
        return next((s for s in self.walk() if s.id == sid), None)

    def attached(self) -> set[str]:
        return {e for s in self.walk() for e in s.evidence_ids}

    def attach(self, sid: str, eids: list[str]) -> None:
        s = self.find(sid)
        if s is None:
            s = self.add_section(None, sid if not sid[0].isdigit() else UNSORTED)
        for e in eids:
            if e not in s.evidence_ids:
                s.evidence_ids.append(e)

    def detach(self, eid: str) -> None:
        for s in self.walk():
            if eid in s.evidence_ids:
                s.evidence_ids.remove(eid)

    def add_section(self, parent_id: str | None, title: str) -> Section:
        title = re.sub(r"^\s*\d+(\.\d+)*\s*[.、:：]?\s*", "", title).strip() or title  # LLM 常把编号写进节名
        existing = next((s for s in self.walk() if s.title == title), None)
        if existing:
            return existing
        siblings = self.find(parent_id).children if parent_id and self.find(parent_id) else self.sections
        prefix = f"{parent_id}." if parent_id and self.find(parent_id) else ""
        sec = Section(id=f"{prefix}{len(siblings) + 1}", title=title)
        siblings.append(sec)
        return sec

    def rename(self, sid: str, title: str) -> None:
        s = self.find(sid)
        if s:
            s.title = re.sub(r"^\s*\d+(\.\d+)*\s*[.、:：]?\s*", "", title).strip() or title

    def unsorted_ids(self) -> list[str]:
        s = next((x for x in self.walk() if x.title == UNSORTED), None)
        return list(s.evidence_ids) if s else []

    def sweep_unsorted(self) -> None:
        """已挂到正式节的证据，从「未归类」里移除；空的「未归类」节删掉。"""
        uns = next((x for x in self.walk() if x.title == UNSORTED), None)
        if not uns:
            return
        elsewhere = {e for x in self.walk() if x is not uns for e in x.evidence_ids}
        uns.evidence_ids = [e for e in uns.evidence_ids if e not in elsewhere]
        if not uns.evidence_ids:
            self.sections = [x for x in self.sections if x is not uns]

    def apply(self, ops: list[dict]) -> int:
        n = 0
        for op in ops:
            kind = op.get("op")
            try:
                if kind == "attach":
                    self.attach(str(op["section"]), [str(x) for x in op.get("ids", [])])
                elif kind == "add_section":
                    self.add_section(op.get("parent") or None, str(op["title"]))
                elif kind == "rename":
                    self.rename(str(op["section"]), str(op["title"]))
                elif kind == "detach":
                    self.detach(str(op["id"]))
                else:
                    continue
                n += 1
            except (KeyError, TypeError):
                continue
        return n

    def clear_synthesis(self) -> list[str]:
        """把误挂在综合节上的证据摘下来，返回其 id。"""
        moved = []
        for s in self.walk():
            if is_synthesis_title(s.title) and s.evidence_ids:
                moved += s.evidence_ids
                s.evidence_ids = []
        return moved

    def place_unsorted(self, eids: list[str]) -> None:
        missing = [e for e in eids if e not in self.attached()]
        if missing:
            self.attach(self.add_section(None, UNSORTED).id, missing)


def revise(outline: Outline, new_evidence: list[Evidence], spec: TopicSpec,
           llm: LLM | None) -> tuple[Outline, list[dict]]:
    """LLM 给操作（attach / add_section / rename），程序执行；未挂上的进「未归类」。
    new_evidence 里应同时包含上次留在「未归类」的证据，让它们有机会被重新归位。"""
    if not new_evidence:
        outline.sweep_unsorted()
        return outline, []
    ops: list[dict] = []
    if llm is not None:
        rows = [{"id": e.id, "title": e.candidate.title, "venue": e.candidate.venue,
                 "year": e.candidate.year, "method": e.extraction.get("method", ""),
                 "scenario": e.extraction.get("scenario", ""),
                 "summary": e.extraction.get("summary", "")[:200]} for e in new_evidence]
        synth = [s.id + " " + s.title for s in outline.walk() if is_synthesis_title(s.title)]
        prompt = tagged("outline", (
            f"{spec.profile_text()}\n\n当前大纲：\n{outline.to_markdown()}\n\n"
            f"注意：以下是综合节，由正文综合生成，不要往上面挂证据：{'; '.join(synth) or '无'}\n\n"
            "新入库证据：\n" + "\n".join(
                f"- {r['id']} | {r['title']} | {r['method']} | {r['scenario']} | {r['summary']}"
                for r in rows) +
            "\n\n请把每条新证据挂到最合适的节；若现有节都不合适，可新建节（parent 可空表示顶层）；"
            "节名过时可 rename。只输出 JSON 数组的操作：\n"
            '[{"op":"attach","section":"2.1","ids":["doi:..."]},'
            '{"op":"add_section","parent":"2","title":"..."},'
            '{"op":"rename","section":"3","title":"..."}]'))
        try:
            ops = parse_json_array(llm.chat(prompt, task="outline"))
        except Exception as exc:
            print(f"[outline] llm failed: {exc}")
            ops = []
        outline.apply(ops)
    moved = outline.clear_synthesis()
    outline.place_unsorted([e.id for e in new_evidence] + moved)
    outline.sweep_unsorted()
    return outline, ops
