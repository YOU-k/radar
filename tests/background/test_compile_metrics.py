import json

from radar.background import metrics as m
from radar.background.compile import (assemble, check_citations, compile_report, is_synthesis,
                                      number_citations, strip_headings, target_length)
from radar.background.outline import Section
from radar.background.models import Evidence, Vote
from radar.background.outline import Outline
from radar.background.store import EvidenceStore
from tests.background.conftest import FakeLLM, make_cand


def _evs(n):
    return [Evidence(candidate=make_cand(i), panel=[Vote("bio", "yes")],
                     extraction={"summary": f"s{i}", "results": "AUC 0.8"}) for i in range(n)]


def test_check_and_number_citations():
    known = {"doi:10.1/a", "arxiv:2601.00001"}
    text = "x [doi:10.1/a] y [arxiv:2601.00001] z [doi:10.1/zzz] [doi:10.1/a]"
    ok, bad = check_citations(text, known)
    assert ok == ["doi:10.1/a", "arxiv:2601.00001"] and bad == ["doi:10.1/zzz"]
    assert number_citations(text, ok) == "x [1] y [2] z  [1]"


def test_compile_report_drops_hallucinated_and_numbers(spec):
    evs = _evs(3)
    o = Outline.from_spec(spec)
    o.attach("2.1", [e.id for e in evs[:2]]); o.attach("3", [evs[2].id])
    rep = compile_report(spec, o, evs, FakeLLM(), coverage=0.5, round_no=2, changelog="- 新增 x")
    assert "doi:10.9999/fake" not in rep and "[doi:" not in rep  # 幻觉引用被删、合法引用已编号
    assert "## 参考文献" in rep and rep.count("\n1. ") == 1 and "## 本次变更" in rep
    assert "证据 3 篇 · 覆盖度 0.50 · 第 2 轮" in rep
    assert "（本节暂无入库证据）" in rep  # 空叶节点有占位


def test_compile_only_feeds_section_evidence(spec):
    evs = _evs(2)
    o = Outline.from_spec(spec); o.attach("2.1", [evs[0].id]); o.attach("3", [evs[1].id])
    llm = FakeLLM()
    compile_report(spec, o, evs, llm, 0.1, 1)
    sec_prompts = [p for t, p in llm.calls if t == "compile" and "TL;DR" not in p]
    p21 = next(p for p in sec_prompts if "生成式疾病轨迹模型" in p)
    assert evs[0].id in p21 and evs[1].id not in p21


def test_coverage_and_stop(spec, tmp_path):
    st = EvidenceStore(tmp_path / "e", tmp_path / "r.jsonl")
    o = Outline.from_spec(spec)
    cov0 = m.coverage(spec, st, o, None, 1)
    assert cov0.score == 0.0 and cov0.seed_hit == 0.0
    seed = Evidence(candidate=make_cand(0, doi="10.1038/s41586-025-09529-3"), panel=[])
    st.add(seed)
    for i in range(3):
        st.add(_evs(3)[i]); o.attach("2.1", [_evs(3)[i].id])
    cov = m.coverage(spec, st, o, top_cited=[seed.id, "doi:10.1/none"], round_no=2)
    assert cov.seed_hit == 0.5 and cov.saturation == 0.2 and cov.highcite == 0.5
    assert cov.score == round(0.3 * 0.5 + 0.3 * 0.2 + 0.4 * 0.5, 3)
    hist = m.append_metrics(tmp_path / "metrics.json", cov0)
    hist = m.append_metrics(tmp_path / "metrics.json", cov)
    assert len(json.loads((tmp_path / "metrics.json").read_text())) == 2
    assert m.should_stop(hist, 0.02) is False
    assert m.should_stop([{"score": .5}, {"score": .505}, {"score": .51}], 0.02) is True
    assert m.should_stop([{"score": .5}, {"score": .6}, {"score": .605}], 0.02) is False


def test_target_length_scales():
    assert target_length(1) == (2, 600) and target_length(21) == (7, 3780) and target_length(100) == (12, 6000)


def test_synthesis_sections_written_from_body(spec):
    evs = _evs(2)
    o = Outline.from_spec(spec); o.attach("2.1", [e.id for e in evs])
    assert is_synthesis(o.find("1"), spec) and not is_synthesis(o.find("2.1"), spec)
    llm = FakeLLM()
    rep = compile_report(spec, o, evs, llm, 0.1, 1)
    synth_prompts = [p for t, p in llm.calls if "综合节" in p]
    assert len(synth_prompts) == 2 and "【已写正文】" in synth_prompts[0]  # 背景与定义 + 评测、争议与空白
    assert "（本节暂无入库证据）" not in rep.split("## 1 背景与定义")[1].split("## 2")[0]


def test_section_prompt_states_length(spec):
    evs = _evs(9)
    o = Outline.from_spec(spec); o.attach("2.1", [e.id for e in evs])
    llm = FakeLLM(); compile_report(spec, o, evs, llm, 0.1, 1)
    p21 = next(p for t, p in llm.calls if "生成式疾病轨迹模型" in p and "综合节" not in p)
    assert "9 篇证据" in p21 and "约 3 段、不少于 1620 字" in p21


def test_strip_headings():
    assert strip_headings("## 背景与定义\n\n正文 [doi:1]\n### 小标题\n更多") == "正文 [doi:1]\n\n更多\n"


def test_synthesis_even_if_evidence_attached(spec):
    o = Outline.from_spec(spec)
    o.attach("1", ["doi:10.1000/paper0"])  # 误挂
    assert is_synthesis(o.find("1"), spec)


def test_seed_hit_matches_alt_ids(spec, tmp_path):
    st = EvidenceStore(tmp_path / "e", tmp_path / "r.jsonl")
    c = make_cand(0, doi="10.1038/some-journal-version")
    c.extra["alt_ids"] = [spec.seeds[0]]
    st.add(Evidence(candidate=c, panel=[]))
    assert m.coverage(spec, st, Outline.from_spec(spec), None, 1).seed_hit == 0.5
