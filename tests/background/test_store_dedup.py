from radar.background.dedup import dedup, merge_duplicates
from radar.background.models import Decision, Evidence, Vote
from radar.background.store import EvidenceStore
from tests.background.conftest import make_cand


def _store(tmp_path):
    return EvidenceStore(tmp_path / "evidence", tmp_path / "rejected.jsonl")


def test_store_add_get_stats(tmp_path):
    st = _store(tmp_path)
    ev = Evidence(candidate=make_cand(1), panel=[Vote("bio", "yes"), Vote("media", "yes")],
                  extraction={"summary": "s"}, added_round=1)
    st.add(ev)
    assert st.get(ev.id).candidate.title == ev.candidate.title
    assert st.ids() == {ev.id} and st.stats()["evidence"] == 1
    ev.sections = ["2.1"]
    st.update(ev)
    assert st.get(ev.id).sections == ["2.1"] and len(st.all()) == 1


def test_reject_and_seen(tmp_path):
    st = _store(tmp_path)
    c = make_cand(2)
    st.reject(c, Decision(c.id, [Vote("bio", "yes"), Vote("media", "no")], False, True, 1))
    assert st.rejected()[c.id]["borderline"] is True
    assert st.is_seen(c)
    same_title = make_cand(99, doi="10.1000/other", title=c.title)
    assert st.is_seen(make_cand(3)) is False


def test_merge_duplicates_merges_provenance():
    a = make_cand(1, citations=None, found_by="s2")
    b = make_cand(1, citations=50, found_by="eupmc", abstract="a much longer abstract text")
    c = make_cand(7, doi="10.1000/z", title=a.title, found_by="journal-retro")  # 同标题不同 id
    out = merge_duplicates([a, b, c])
    assert len(out) == 1
    assert set(out[0].found_by) == {"s2", "eupmc", "journal-retro"}
    assert out[0].citations == 50 and out[0].abstract == "a much longer abstract text"


def test_dedup_against_store(tmp_path):
    st = _store(tmp_path)
    st.add(Evidence(candidate=make_cand(1), panel=[]))
    st.reject(make_cand(2), Decision("doi:10.1000/paper2", [], False, False))
    new = dedup([make_cand(1), make_cand(2), make_cand(3)], st)
    assert [c.id for c in new] == ["doi:10.1000/paper3"]


def test_alt_ids_prevent_duplicate_versions(tmp_path):
    st = _store(tmp_path)
    nature = make_cand(1, doi="10.1038/s41586-025-09422-z", title="DeepSeek-R1 incentivizes reasoning")
    nature.extra["alt_ids"] = ["arxiv:2501.12948"]
    st.add(Evidence(candidate=nature, panel=[]))
    assert "arxiv:2501.12948" in st.all_ids()
    from radar.background.models import Candidate
    preprint = Candidate(id="arxiv:2501.12948", title="DeepSeek-R1: Incentivizing Reasoning Capability", url="")
    assert st.is_seen(preprint)
