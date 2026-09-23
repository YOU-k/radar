import json

from radar.background import discover as d
from radar.background.gap import fallback_plan, plan_round
from radar.background.models import DiscoveryPlan, Evidence
from radar.background.outline import Outline
from radar.background.store import EvidenceStore
from tests.background.conftest import FakeLLM, make_cand


def _row(i, cites=5, journal="Nature", abstract="UK Biobank cohort"):
    return {"id": f"{i}", "source": "MED", "doi": f"10.1000/e{i}", "title": f"EuPMC paper {i}",
            "abstractText": abstract, "firstPublicationDate": "2026-01-01", "citedByCount": cites,
            "journalInfo": {"journal": {"title": journal}}, "authorString": "A, B"}


def test_eupmc_keyword_source(spec):
    seen = []
    def search(q, start, end, page_size=250, sort=""):
        seen.append((q, sort)); return [_row(1), _row(2, cites=50)]
    src = d.EuropePMCKeyword(search=search)
    out = src.fetch(spec, DiscoveryPlan(queries=["q1", "q2"], months=24))
    assert len(out) == 4 and out[1].citations == 50 and out[0].found_by == ["eupmc:q1"]
    assert seen[0][1] == "CITED desc" and len(seen) == 2


def test_journal_retro_filters_by_keyword(spec):
    def search(q, start, end, page_size=250, sort=""):
        assert 'JOURNAL:"Nature"' in q and "biobank" in q.lower()
        return [_row(1, abstract="UK Biobank proteomics"), _row(2, abstract="tutankhamun tomb")]
    out = d.EuropePMCJournal(search=search).fetch(spec, DiscoveryPlan(journals=["Nature"]))
    assert [c.title for c in out] == ["EuPMC paper 1"] and out[0].found_by == ["journal-retro"]


def test_s2_snowball_maps_ids_and_rel(spec):
    calls = []
    def get_json(url, params=None, timeout=60):
        calls.append(url)
        return {"data": [{"citedPaper" if "references" in url else "citingPaper": {
            "title": "Snow", "externalIds": {"DOI": "10.5/SNOW", "ArXiv": "2501.00001"}, "year": 2025, "venue": "Cell",
            "citationCount": 99, "authors": [{"name": "X"}]}}]}
    out = d.S2Snowball(get_json=get_json, sleep=0).fetch(spec, DiscoveryPlan(snowball_ids=["doi:10.1/seed"]))
    assert len(out) == 2 and out[0].id == "doi:10.5/snow" and out[0].citations == 99
    assert out[0].extra["alt_ids"] == ["arxiv:2501.00001"]
    assert calls[0].endswith("/paper/DOI:10.1/seed/references") and calls[1].endswith("/citations")


def test_relevance_beats_raw_citations(spec):
    generic = make_cand(1, title="Attention is all you need", abstract="transformer", citations=190000)
    relevant = make_cand(2, title="Generative model of disease trajectories in UK Biobank",
                         abstract="biobank EHR", citations=40)
    seed = make_cand(3, doi="10.1038/s41586-025-09529-3", title="unrelated words", citations=1)
    out = d.discover(spec, DiscoveryPlan(), [type("S", (), {"name": "s", "fetch": lambda self, sp, pl: [generic, relevant, seed]})()])
    assert [c.id for c in out] == [seed.id, relevant.id, generic.id]


def test_s2_fetches_seed_itself(spec):
    def get_json(url, params=None, timeout=60):
        if url.endswith("/references") or url.endswith("/citations"):
            return {"data": []}
        return {"title": "Delphi", "externalIds": {"DOI": "10.1038/s41586-025-09529-3"}, "year": 2025,
                "venue": "Nature", "citationCount": 300, "authors": []}
    out = d.S2Snowball(get_json=get_json, sleep=0).fetch(spec, DiscoveryPlan(snowball_ids=[spec.seeds[0]]))
    assert [c.found_by for c in out] == [["seed"]] and out[0].id == spec.seeds[0]


def test_empty_result_retried(spec, monkeypatch):
    monkeypatch.setattr(d.time, "sleep", lambda s: None)
    n = {"calls": 0}
    def search(q, start, end, page_size=250, sort=""):
        n["calls"] += 1
        return [] if n["calls"] == 1 else [_row(1, abstract="UK Biobank")]
    out = d.EuropePMCJournal(search=search).fetch(spec, DiscoveryPlan(journals=["Nature"]))
    assert len(out) == 1 and n["calls"] == 2


def test_s2_keyword_source(spec):
    calls = []
    def get_json(url, params=None, timeout=60):
        calls.append((url, params))
        return {"data": [{"title": "JEPA paper", "externalIds": {"ArXiv": "2301.08243"}, "year": 2023,
                          "venue": "CVPR", "citationCount": 800, "authors": []}]}
    out = d.S2Keyword(get_json=get_json, sleep=0).fetch(spec, DiscoveryPlan(queries=['"joint embedding"'], months=24))
    assert out[0].id == "arxiv:2301.08243" and out[0].url.endswith("2301.08243") and out[0].found_by == ['s2kw:"joint embedding"']
    assert calls[0][0].endswith("/paper/search") and calls[0][1]["query"] == "joint embedding" and calls[0][1]["year"].endswith("-")


def test_get_json_backs_off_on_429(monkeypatch):
    import requests as rq
    monkeypatch.setattr(d.time, "sleep", lambda s: None)
    seq = iter([429, 429, 200])
    class R:
        def __init__(self, code): self.status_code = code
        def raise_for_status(self):
            if self.status_code >= 400: raise rq.HTTPError(str(self.status_code))
        def json(self): return {"ok": True}
    monkeypatch.setattr(d.requests, "get", lambda *a, **k: R(next(seq)))
    assert d._get_json("https://api.semanticscholar.org/x") == {"ok": True}


def test_source_failure_isolated(spec):
    class Bad:
        name = "bad"
        def fetch(self, spec, plan): raise RuntimeError("down")
    class Good:
        name = "good"
        def fetch(self, spec, plan): return [make_cand(1, citations=1), make_cand(2, citations=9)]
    out = d.discover(spec, DiscoveryPlan(), [Bad(), Good()], max_candidates=1)
    assert [c.id for c in out] == ["doi:10.1000/paper2"]  # 按引用排序并截断


def test_inbox_filters_domain_score_and_age(spec, tmp_path):
    p = tmp_path / "extractions.jsonl"
    from datetime import date, timedelta
    today = date.today().isoformat(); old = (date.today() - timedelta(days=30)).isoformat()
    rows = [{"date": today, "domain": "population_omics_ai", "score": 8, "title": "keep", "url": "https://doi.org/10.1000/k", "summary": "s"},
            {"date": today, "domain": "population_omics_ai", "score": 6, "title": "low", "url": "https://doi.org/10.1000/l"},
            {"date": today, "domain": "agents", "score": 9, "title": "other", "url": "https://doi.org/10.1000/o"},
            {"date": old, "domain": "population_omics_ai", "score": 9, "title": "old", "url": "https://doi.org/10.1000/d"}]
    p.write_text("\n".join(json.dumps(r) for r in rows), encoding="utf-8")
    out = d.Inbox(p, since_days=7).fetch(spec, DiscoveryPlan())
    assert [c.title for c in out] == ["keep"] and out[0].id == "doi:10.1000/k" and out[0].found_by == ["inbox"]


def test_gap_fallback_and_llm(spec, tmp_path):
    st = EvidenceStore(tmp_path / "e", tmp_path / "r.jsonl")
    plan = fallback_plan(spec, st, 1)
    assert plan.queries == spec.queries and plan.snowball_ids[:2] == spec.seeds and "冷启动" in plan.focus
    st.add(Evidence(candidate=make_cand(1, citations=500), panel=[]))
    plan2 = plan_round(spec, st, Outline.from_spec(spec), 2, FakeLLM())
    assert plan2.queries == ["gap query one", "gap query two"] and plan2.focus == "补生成式疾病轨迹"
    assert plan2.snowball_ids == ["doi:10.1000/paper1"]
    plan3 = plan_round(spec, st, Outline.from_spec(spec), 2, FakeLLM(fail_tasks={"gap"}))
    assert plan3.queries == spec.queries  # LLM 失败退化到规则
