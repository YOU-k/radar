"""评审团：每个角色独立投票 → 有分歧时互看理由、可修订一次 → 规则裁决。

规则 "all"：全体 yes 才入库（用户要求：生物专家和媒体专家都感兴趣）。
一票 yes 记 borderline，落选但可被后续滚雪球复审。"""
from __future__ import annotations

import json

from .llmio import LLM, parse_json_array, tagged
from .models import Candidate, Decision, Vote
from .spec import TopicSpec

BATCH = 10


def _payload(cands: list[Candidate]) -> list[dict]:
    return [{"id": i, "title": c.title, "venue": c.venue, "year": c.year,
             "citations": c.citations, "abstract": (c.abstract or "")[:700]}
            for i, c in enumerate(cands)]


def _vote_prompt(spec: TopicSpec, role: dict, cands: list[Candidate],
                 others: dict[int, list[Vote]] | None = None) -> str:
    body = (f"你是「{role.get('label', role['name'])}」。评审口径：{role['rubric']}\n\n"
            f"{spec.profile_text()}\n\n"
            "对下面每篇文献投票：vote 只能是 yes（值得进入该方向的背景报告）或 no，"
            "reason 一句中文（≤40 字），说清依据。宁缺毋滥。\n")
    if others:
        body += ("\n这是第二轮：其他评审对部分文献与你意见不同，他们的理由列在 others 字段里。"
                 "你可以维持或修订，修订时说明为什么被说服。\n")
    rows = _payload(cands)
    if others:
        for r in rows:
            if r["id"] in others:
                r["others"] = [{"role": v.role, "vote": v.vote, "reason": v.reason}
                               for v in others[r["id"]]]
    body += ("\n【文献】\n" + json.dumps(rows, ensure_ascii=False) +
             '\n\n只输出 JSON 数组：[{"id":0,"vote":"yes","reason":"..."}]')
    return tagged("screen", body)


def _ask_role(llm: LLM, spec: TopicSpec, role: dict, cands: list[Candidate],
              others: dict[int, list[Vote]] | None = None) -> dict[int, Vote]:
    votes: dict[int, Vote] = {}
    try:
        rows = parse_json_array(llm.chat(_vote_prompt(spec, role, cands, others), task="screen"))
    except Exception as exc:
        print(f"[screen] role {role['name']} failed: {exc}")
        rows = []
    for r in rows:
        try:
            i = int(r.get("id", -1))
        except (TypeError, ValueError):
            continue
        if 0 <= i < len(cands):
            v = str(r.get("vote", "no")).strip().lower()
            votes[i] = Vote(role=role["name"], vote="yes" if v == "yes" else "no",
                            reason=str(r.get("reason", ""))[:120], revised=others is not None)
    return votes


def decide(votes: list[Vote], rule: str = "all") -> tuple[bool, bool]:
    yes = [v for v in votes if v.yes]
    if not votes:
        return False, False
    if rule == "majority":
        accepted = len(yes) * 2 > len(votes)
    else:
        accepted = len(yes) == len(votes)
    return accepted, (not accepted and bool(yes))


def screen(cands: list[Candidate], spec: TopicSpec, llm: LLM, round_no: int = 0,
           rule: str = "all", discuss: bool = True) -> list[Decision]:
    out: list[Decision] = []
    for b in range(0, len(cands), BATCH):
        chunk = cands[b:b + BATCH]
        first: dict[str, dict[int, Vote]] = {
            role["name"]: _ask_role(llm, spec, role, chunk) for role in spec.roles}
        # 分歧项进入第二轮讨论
        split: dict[int, list[Vote]] = {}
        for i in range(len(chunk)):
            vs = [first[r["name"]][i] for r in spec.roles if i in first[r["name"]]]
            if vs and len({v.vote for v in vs}) > 1:
                split[i] = vs
        if discuss and split:
            sub = [chunk[i] for i in sorted(split)]
            remap = {k: i for k, i in enumerate(sorted(split))}
            for role in spec.roles:
                others = {k: [v for v in split[remap[k]] if v.role != role["name"]]
                          for k in remap}
                rev = _ask_role(llm, spec, role, sub, others)
                for k, v in rev.items():
                    first[role["name"]][remap[k]] = v
        for i, c in enumerate(chunk):
            vs = [first[r["name"]][i] for r in spec.roles if i in first[r["name"]]]
            # 某角色没返回该条 → 视为 no（缺票不放行）
            missing = [r["name"] for r in spec.roles if i not in first[r["name"]]]
            vs += [Vote(role=m, vote="no", reason="未返回投票") for m in missing]
            accepted, borderline = decide(vs, rule)
            out.append(Decision(candidate_id=c.id, votes=vs, accepted=accepted,
                                borderline=borderline, round=round_no))
    return out
