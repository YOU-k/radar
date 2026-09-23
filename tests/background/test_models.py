from radar.background.models import Candidate, Evidence, Vote, normalize_id, title_key
from radar.schema import Item


def test_normalize_id_variants():
    assert normalize_id("DOI:10.1038/S41586-025-09529-3") == "doi:10.1038/s41586-025-09529-3"
    assert normalize_id("", "https://doi.org/10.1016/j.cell.2026.08.026.") == "doi:10.1016/j.cell.2026.08.026"
    assert normalize_id("arxiv:2609.17801v2") == "arxiv:2609.17801"
    assert normalize_id("", "https://arxiv.org/abs/2605.31111") == "arxiv:2605.31111"
    assert normalize_id("", "https://pubmed.ncbi.nlm.nih.gov/42632465/") == "pmid:42632465"
    assert normalize_id("eupmc:PPR:123") == "eupmc:ppr:123"


def test_title_key_ignores_case_and_punct():
    assert title_key("Delphi: Learning the Natural History!") == title_key("delphi learning the natural history")


def test_candidate_from_item_and_roundtrip():
    it = Item(id="doi:10.1/X", source="europepmc", domain="d", title="T", url="https://doi.org/10.1/X",
              published="2026-07-15", extra={"journal": "Nature", "pmcid": "PMC1", "is_oa": True})
    c = Candidate.from_item(it, "eupmc:q")
    assert c.id == "doi:10.1/x" and c.venue == "Nature" and c.year == 2026 and c.extra == {"pmcid": "PMC1", "is_oa": True}
    assert Candidate.from_dict(c.to_dict()) == c


def test_evidence_roundtrip():
    c = Candidate(id="doi:10.1/a", title="A")
    ev = Evidence(candidate=c, panel=[Vote("bio", "yes", "ok")], extraction={"summary": "s"},
                  sections=["2.1"], added_round=1, added_on="2026-09-23")
    assert Evidence.from_dict(ev.to_dict()) == ev
