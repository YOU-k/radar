from radar.background.models import Evidence, Vote
from radar.background.outline import UNSORTED, Outline, revise
from tests.background.conftest import FakeLLM, make_cand


def test_from_spec_ids_and_markdown_roundtrip(spec):
    o = Outline.from_spec(spec)
    assert [s.id for s in o.walk()] == ["1", "2", "2.1", "2.2", "3", "4"]
    o.attach("2.1", ["doi:10.1/a", "doi:10.1/b"])
    md = o.to_markdown()
    o2 = Outline.from_markdown(md)
    assert o2.to_markdown() == md and o2.find("2.1").evidence_ids == ["doi:10.1/a", "doi:10.1/b"]


def test_ops_apply(spec):
    o = Outline.from_spec(spec)
    n = o.apply([{"op": "add_section", "parent": "2", "title": "医学基础模型"},
                 {"op": "attach", "section": "2.3", "ids": ["doi:10.1/x"]},
                 {"op": "rename", "section": "4", "title": "评测与争议"},
                 {"op": "detach", "id": "doi:10.1/x"},
                 {"op": "bogus"}, {"op": "attach"}])
    assert n == 4
    assert o.find("2.3").title == "医学基础模型" and o.find("2.3").evidence_ids == []
    assert o.find("4").title == "评测与争议"
    o.apply([{"op": "add_section", "parent": "2", "title": "医学基础模型"}])
    assert len(o.find("2").children) == 3  # 同名不重复建


def test_revise_attaches_and_places_unsorted(spec):
    o = Outline.from_spec(spec)
    evs = [Evidence(candidate=make_cand(i), panel=[Vote("bio", "yes")]) for i in range(3)]
    llm = FakeLLM(outline_ops=[{"op": "attach", "section": "2.1", "ids": [evs[0].id]}])
    o, ops = revise(o, evs, spec, llm)
    assert o.find("2.1").evidence_ids == [evs[0].id]
    uns = next(s for s in o.walk() if s.title == UNSORTED)
    assert set(uns.evidence_ids) == {evs[1].id, evs[2].id}


def test_revise_without_llm(spec):
    o = Outline.from_spec(spec)
    evs = [Evidence(candidate=make_cand(1), panel=[])]
    o, ops = revise(o, evs, spec, None)
    assert ops == [] and evs[0].id in o.attached()


def test_revise_moves_evidence_off_synthesis_sections(spec):
    o = Outline.from_spec(spec)
    evs = [Evidence(candidate=make_cand(1), panel=[])]
    llm = FakeLLM(outline_ops=[{"op": "attach", "section": "1", "ids": [evs[0].id]}])  # 挂到「背景与定义」
    o, _ = revise(o, evs, spec, llm)
    assert o.find("1").evidence_ids == []
    assert evs[0].id in next(s for s in o.walk() if s.title == UNSORTED).evidence_ids
    assert "综合节" in llm.calls[0][1]


def test_add_section_strips_numbering(spec):
    o = Outline.from_spec(spec)
    sec = o.add_section("2", "2.4 组学衰老时钟")
    assert sec.id == "2.3" and sec.title == "组学衰老时钟"
    o.rename("3", "3. 数据资源")
    assert o.find("3").title == "数据资源"


def test_unsorted_swept_when_placed_later(spec):
    o = Outline.from_spec(spec)
    ev = Evidence(candidate=make_cand(1), panel=[])
    o, _ = revise(o, [ev], spec, FakeLLM(outline_ops=[]))          # 第一次没挂上 → 未归类
    assert o.unsorted_ids() == [ev.id]
    o, _ = revise(o, [ev], spec, FakeLLM(outline_ops=[{"op": "attach", "section": "2.2", "ids": [ev.id]}]))
    assert o.find("2.2").evidence_ids == [ev.id] and o.unsorted_ids() == []
    assert all(s.title != UNSORTED for s in o.walk())               # 空的未归类节被删
