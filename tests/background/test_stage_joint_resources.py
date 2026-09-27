import json

from radar.background import resources as R
from radar.background.joint import _block, joint_report, run_joint, topic_digest
from radar.background.models import Candidate, Evidence, Vote
from radar.background.outline import Outline
from radar.background.compile import compile_report
from radar.background.stage import section_stats, topic_stats, stage_section
from radar.background.store import EvidenceStore
from tests.background.conftest import FakeLLM, make_cand


def _evs():
    out = []
    for i, (year, venue, cites) in enumerate([(2026, "Nature", 5), (2025, "Nature Genetics", 40), (2019, "PLoS One", 900), (2024, "bioRxiv", 3)]):
        out.append(Evidence(candidate=make_cand(i, venue=venue, year=year, citations=cites), panel=[Vote("bio", "yes")],
                            extraction={"summary": f"s{i}", "method": f"m{i}", "data": "UK Biobank 500k", "availability": "public"}))
    return out


def test_section_and_topic_stats(spec):
    evs = _evs()
    o = Outline.from_spec(spec); o.attach("2.1", [e.id for e in evs[:3]]); o.attach("3", [evs[3].id])
    st = section_stats(evs, o, this_year=2026)
    s21 = next(x for x in st if x["section"].startswith("2.1"))
    assert s21["n"] == 3 and s21["recent_share"] == round(2 / 3, 2) and s21["cns_share"] == round(2 / 3, 2)
    assert s21["year_span"] == "2019-2026" and s21["median_citations"] == 40 and s21["top"][0]["citations"] == 900
    assert not any(x["section"].startswith("1 ") for x in st)  # 综合节不计
    ts = topic_stats(evs, [{"n_evidence": 2, "score": .3}, {"n_evidence": 4, "score": .5}], this_year=2026)
    assert ts["accepted_per_round"] == [2, 2] and ts["coverage"] == [.3, .5] and ts["year_hist"]["2026"] == 1


def test_stage_section_in_report(spec):
    evs = _evs()
    o = Outline.from_spec(spec); o.attach("2.1", [e.id for e in evs])
    llm = FakeLLM()
    rep = compile_report(spec, o, evs, llm, 0.5, 2, hist=[{"n_evidence": 4, "score": .5}])
    assert "## 阶段判断与行动建议" in rep and "**朝阳**" in rep
    sp = next(p for t, p in llm.calls if t == "stage")
    assert '"accepted_per_round"' not in sp and '"coverage"' not in sp and "算法支持" in sp
    assert "雷达检索统计，非领域属性" in sp
    assert "**" in rep  # 加粗保留


def test_joint_report(spec, tmp_path):
    evs = _evs()
    o = Outline.from_spec(spec); o.attach("2.1", [e.id for e in evs])
    rep = compile_report(spec, o, evs, FakeLLM(), 0.5, 2)
    spec.report_path.write_text(rep, encoding="utf-8")
    st = EvidenceStore(spec.evidence_dir, spec.rejected_path)
    for e in evs: st.add(e)
    d = topic_digest(spec)
    assert d["n_evidence"] == 4 and "要点" in d["tldr"] and "朝阳" in d["stage"] and d["top"][0]["year"] == 2019
    out = joint_report([spec], FakeLLM(), resources_md="| UK Biobank |")
    assert out.startswith("# 联合分析 · 方向背景报告") and "## 联合行动建议" in out and "1 个方向 · 证据 4 篇" in out
    p = run_joint(FakeLLM(), root=spec.dir.parent)
    assert p == spec.dir.parent / "_joint" / "report.md" and p.exists()


def test_block_extracts_section():
    txt = "# t\n\n## 摘要（TL;DR）\n\n- a\n- b\n\n## 1 背景\n\nx\n"
    assert _block(txt, "摘要") == "- a\n- b" and _block(txt, "不存在") == ""


def test_resources_mine_merge_verify_render(spec, tmp_path):
    evs = _evs()
    rows = R.mine(evs, spec.name, FakeLLM())
    assert {r["name"] for r in rows} == {"UK Biobank", "scGPT"}  # kind 非法的被丢
    rows2 = R.mine(evs, "另一方向", FakeLLM())
    reg = R.merge(rows + rows2)
    ukb = reg["uk biobank"]
    assert ukb["topics"] == [spec.name, "另一方向"] and len(ukb["used_by"]) == 2
    n = R.verify(reg, head=lambda u: 200 if "ukbiobank" in u else 404)
    assert n == 2 and ukb["verified"] == "ok" and reg["scgpt"]["verified"] == "dead"
    md = R.render(reg)
    assert "**UK Biobank**" in md and "**scGPT**" in md and "## P2 了解即可（2）" in md and "| 数据库 |" in md
    assert "[链接](https://www.ukbiobank.ac.uk)" in md and md.index("**scGPT**") < md.index("**UK Biobank**")  # 同一优先级内按类型排序


def test_run_resources_end_to_end(spec):
    st = EvidenceStore(spec.evidence_dir, spec.rejected_path)
    for e in _evs(): st.add(e)
    out = R.run_resources(FakeLLM(), root=spec.dir.parent, head=lambda u: 200)
    reg = json.loads((spec.dir.parent / "_resources" / "registry.json").read_text())
    assert out.exists() and set(reg) == {"uk biobank", "scgpt"}


def test_norm_aliases_and_core_filter():
    assert R._norm("UK Biobank (UKB)") == "uk biobank" and R._norm("UKB") == "uk biobank" and R._norm("scGPT v2") == "scgpt"
    reg = R.merge([{"name": "UK Biobank", "kind": "dataset", "used_by": ["a"], "topics": ["t1"], "scale": "50万", "access": "", "open": "restricted", "note": "", "modality": ""},
                   {"name": "UKB", "kind": "dataset", "used_by": ["b"], "topics": ["t2"], "scale": "", "access": "", "open": "", "note": "", "modality": ""},
                   {"name": "TinyTool", "kind": "tool", "used_by": ["c"], "topics": ["t1"], "scale": "1", "access": "https://x", "open": "yes", "note": "", "modality": ""}])
    assert set(reg) == {"uk biobank", "tinytool"} and len(reg["uk biobank"]["used_by"]) == 2
    R.verify(reg, head=lambda u: 200)
    assert R.is_core(reg["uk biobank"]) and not R.is_core(reg["tinytool"])  # 单篇小工具不进主表
    md = R.render(reg)
    assert "**UK Biobank**" in md and "## 单篇提及（1，未进主表）" in md and "TinyTool" in md


def test_verify_blocked_status():
    reg = {"x": {"name": "x", "kind": "dataset", "access": "https://a", "used_by": [], "topics": []}}
    R.verify(reg, head=lambda u: 403)
    assert reg["x"]["verified"] == "blocked"


def test_run_resources_rerender_without_llm(spec):
    st = EvidenceStore(spec.evidence_dir, spec.rejected_path)
    for e in _evs(): st.add(e)
    R.run_resources(FakeLLM(), root=spec.dir.parent, head=lambda u: 200)
    out = R.run_resources(None, root=spec.dir.parent, head=lambda u: 403)
    assert "blocked" in out.read_text(encoding="utf-8")


def test_joint_prompt_asks_every_application_line(spec, monkeypatch):
    from radar.background import joint
    monkeypatch.setattr(joint, "_profile", lambda: "## 应用线\n1. 衰老\n2. 心血管队列")
    seen = []

    class L:
        def chat(self, prompt, **kw):
            seen.append(prompt); return "## 全景"
    joint.joint_report([spec], L())
    assert "心血管队列" in seen[0] and "每条都必须有" in seen[0] and "类器官等多模态健康衰老模型" not in seen[0]


def test_prioritize_and_themes(monkeypatch):
    from radar import themes
    reg = {"uk biobank": {"name": "UK Biobank", "kind": "database", "used_by": ["a", "b"], "topics": ["心血管方向", "人群方向"],
                          "open": "restricted", "note": "n"},
           "scgpt": {"name": "scGPT", "kind": "model", "used_by": ["c", "d"], "topics": ["单细胞方向"], "open": "yes",
                     "note": "n", "priority": "P1", "why": "旧理由"}}
    R.attach_themes(reg, {"心血管方向": "cardio-omics", "人群方向": "population-omics-ai", "单细胞方向": "single-cell-foundation"})
    assert reg["uk biobank"]["themes"] == ["cardio", "cohort"] and reg["scgpt"]["themes"] == ["singlecell"]
    seen = []

    class L:
        def chat(self, prompt, **kw):
            seen.append(prompt)
            return '[{"id":0,"priority":"P0","why":"ChinaHEART 迁移参照队列"}]'
    assert R.prioritize(reg, L()) == 1 and len(seen) == 1 and "scGPT" not in seen[0]  # 已有优先级不重打
    assert reg["uk biobank"]["priority"] == "P0" and reg["scgpt"]["why"] == "旧理由"
    md = R.render(reg)
    assert md.index("## P0 优先上手（1）") < md.index("## P1 值得登记（1）") and "#心血管 #人群队列" in md


def test_principles_report(spec, monkeypatch):
    from radar.background import principles as P
    monkeypatch.setattr(P, "_profile", lambda: "应用线：心血管")
    evs = _evs()
    o = Outline.from_spec(spec); o.attach("2.1", [e.id for e in evs])
    spec.report_path.write_text(compile_report(spec, o, evs, FakeLLM(), 0.5, 2), encoding="utf-8")
    calls = []

    class L:
        def chat(self, prompt, task="", **kw):
            calls.append((task, prompt))
            if "跨领域的全局判断" in prompt:
                return "## 总判断\n| 领域 | 问题 |\n|---|---|\n| A | b |"
            return "## 某方向\n### 这个领域真正想回答的生物学问题\n- 问题 [常识]\n### 对他的含义\n- x [证据]"
    out = P.principles_report([spec], L())
    assert all(t == "principles" for t, _ in calls) and len(calls) == 2
    assert "[证据]" in calls[0][1] and "[常识]" in calls[0][1] and spec.name in calls[1][1]
    assert out.startswith("# 全局判断：从第一性原理看各领域 · 方向背景报告")
    assert out.index("## 总判断") < out.index("## 分领域分析") < out.index(f"### {spec.name}")
    assert "#### 这个领域真正想回答的生物学问题" in out and "## 某方向" not in out  # 小节降级、重复标题剥掉
