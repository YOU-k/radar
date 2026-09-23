from radar.background import extract as ex
from radar.background.fetch import fetch_fulltext, resolve_pmcid
from radar.background.models import Candidate
from tests.background.conftest import FakeLLM, make_cand


def test_extract_fields_and_alignment(spec, cands):
    llm = FakeLLM()
    out = ex.extract(cands, spec, llm, fulltexts={cands[0].id: "FULL TEXT " * 100})
    assert len(out) == len(cands) and set(out[0]) == set(ex.KEYS)
    assert out[3]["summary"].endswith(cands[3].title)
    prompt = llm.calls[0][1]
    assert '"has_fulltext": true' in prompt and '"has_fulltext": false' in prompt


def test_extract_failure_leaves_empty(spec, cands):
    out = ex.extract(cands, spec, FakeLLM(fail_tasks={"extract"}))
    assert all(v == "" for r in out for v in r.values())


def test_fetch_pmc_and_cache(tmp_path):
    calls = []
    def get(url, timeout=60):
        calls.append(url)
        return b"<article><body><p>Hello <b>world</b></p></body></article>"
    c = make_cand(1); c.extra["pmcid"] = "PMC123"
    t1 = fetch_fulltext(c, tmp_path / "cache", get=get)
    t2 = fetch_fulltext(c, tmp_path / "cache", get=get)
    assert t1 == "Hello world" and t2 == t1 and len(calls) == 1
    assert calls[0].endswith("/rest/PMC123/fullTextXML")


def test_fetch_failure_returns_empty(tmp_path):
    def get(url, timeout=60):
        raise RuntimeError("boom")
    c = make_cand(2); c.extra["pmcid"] = "PMC9"
    assert fetch_fulltext(c, tmp_path / "cache", get=get) == ""
    assert not list((tmp_path / "cache").glob("*.txt"))


def test_fetch_skips_without_source(tmp_path):
    called = []
    def get(u, timeout=60):
        called.append(u); return b'{"resultList":{"result":[]}}'
    assert fetch_fulltext(make_cand(3), tmp_path / "cache", get=get) == ""
    assert len(called) == 1 and "search" in called[0]  # DOI 只做一次 pmcid 反查
    called.clear()
    assert fetch_fulltext(Candidate(id="eupmc:ppr:9", title="x"), tmp_path / "cache", get=get) == ""
    assert called == []


def test_resolve_pmcid_by_doi_only_when_oa(tmp_path):
    import json
    def get(url, timeout=60):
        if "search" in url:
            return json.dumps({"resultList": {"result": [{"pmcid": "PMC777", "isOpenAccess": "Y"}]}}).encode()
        return b"<article><body>OA text</body></article>"
    c = make_cand(5)
    assert resolve_pmcid(c, get) == "PMC777" and c.extra["pmcid"] == "PMC777"
    assert fetch_fulltext(c, tmp_path / "c", get=get) == "OA text"
    def get_closed(url, timeout=60):
        return json.dumps({"resultList": {"result": [{"pmcid": "PMC1", "isOpenAccess": "N"}]}}).encode()
    assert resolve_pmcid(make_cand(6), get_closed) == ""
    assert resolve_pmcid(Candidate(id="eupmc:ppr:1", title="x"), get_closed) == ""
