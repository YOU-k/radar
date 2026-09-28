"""人工补录：元数据取数顺序 + 跳过评审入库 + 大纲挂载 + 轮次日志；不联网、不编译。"""
import json
import sys

import pytest

from radar.background import manual
from radar.background.runner import Pipeline
from tests.background.conftest import FakeLLM, make_cand


def fake_get_json(routes: dict):
    """按 URL（+ query 参数）子串路由；未命中抛错模拟网络失败。记录调用。"""
    calls = []

    def get(url, params=None, **kw):
        key = url + ("?" + json.dumps(params, sort_keys=True) if params else "")
        calls.append(key)
        for frag, resp in routes.items():
            if frag in key:
                if isinstance(resp, Exception):
                    raise resp
                return resp
        raise RuntimeError(f"no route for {key}")
    get.calls = calls
    return get


EUPMC_ROW = {"resultList": {"result": [{
    "title": "Systema: a framework for evaluating perturbation prediction.", "doi": "10.1038/S41587-025-02777-8",
    "pmid": "40854979", "pubYear": "2026", "authorString": "Vinas Torne R, et al.",
    "abstractText": "<h4>Abstract</h4>Models capture <i>systematic</i> variation.",
    "journalInfo": {"journal": {"title": "Nature biotechnology"}}, "citedByCount": 12,
    "pmcid": "PMC1", "isOpenAccess": "Y"}]}}


def test_lookup_europepmc_first_and_alt_ids(monkeypatch):
    monkeypatch.delenv("S2_API_KEY", raising=False)
    get = fake_get_json({"europepmc": EUPMC_ROW})
    c = manual.lookup("https://doi.org/10.1038/s41587-025-02777-8", get_json=get, get_text=None)
    assert c.id == "doi:10.1038/s41587-025-02777-8" and c.title.startswith("Systema")
    assert c.abstract == "Abstract Models capture systematic variation."
    assert c.venue == "Nature biotechnology" and c.year == 2026 and c.found_by == ["manual"]
    assert c.extra["alt_ids"] == ["pmid:40854979"] and c.extra["pmcid"] == "PMC1"
    assert len(get.calls) == 1  # 摘要齐了就不再往后查


def test_lookup_falls_back_to_crossref_then_datacite(monkeypatch):
    monkeypatch.delenv("S2_API_KEY", raising=False)
    get = fake_get_json({"europepmc": RuntimeError("503"),
                         "crossref.org/works/10.1101/2025.08.18.670981": {"message": {
                             "title": ["rbio1 - training scientific reasoning LLMs"], "type": "posted-content",
                             "institution": [{"name": "bioRxiv"}], "abstract": "<jats:p>Soft verifiers.</jats:p>",
                             "issued": {"date-parts": [[2025, 8, 21]]}, "author": [{"given": "A", "family": "B"}]}},
                         "datacite.org/dois/10.48550/arxiv.2407.10362": {"data": {"attributes": {
                             "titles": [{"title": "LAB-Bench"}], "publicationYear": 2024,
                             "descriptions": [{"descriptionType": "Abstract", "description": "Benchmark."}],
                             "creators": [{"name": "Laurent, Jon"}]}}}})
    c = manual.lookup("doi:10.1101/2025.08.18.670981", get_json=get, get_text=None)
    assert c.venue == "bioRxiv" and c.abstract == "Soft verifiers." and c.year == 2025
    a = manual.lookup("arxiv:2407.10362v2", get_json=get, get_text=None)
    assert a.id == "arxiv:2407.10362" and a.title == "LAB-Bench" and a.abstract == "Benchmark."
    assert manual.lookup("doi:10.9999/nothing", get_json=get, get_text=None) is None


def test_lookup_uses_s2_only_with_key(monkeypatch):
    s2 = {"title": "Kosmos", "abstract": "AI scientist.", "year": 2025, "venue": "arXiv.org",
          "externalIds": {"ArXiv": "2511.02824", "DOI": "10.48550/arXiv.2511.02824"}, "authors": []}
    get = fake_get_json({"europepmc": {"resultList": {"result": []}}, "semanticscholar": s2,
                         "datacite": RuntimeError("down")})
    monkeypatch.delenv("S2_API_KEY", raising=False)
    assert manual.lookup("arxiv:2511.02824", get_json=get, get_text=None) is None
    monkeypatch.setenv("S2_API_KEY", "x")
    c = manual.lookup("arxiv:2511.02824", get_json=get, get_text=None)
    assert c.id == "arxiv:2511.02824" and c.abstract == "AI scientist."
    assert c.extra["alt_ids"] == ["doi:10.48550/arxiv.2511.02824"]


def _pipe(spec, llm, fetched=None):
    def fetcher(c, cache_dir):
        return (fetched or {}).get(c.id, "")
    return Pipeline(spec, llm, sources=[], fetcher=fetcher)


def test_add_manual_skips_panel_and_known(spec):
    llm = FakeLLM()
    pipe = _pipe(spec, llm, fetched={"doi:10.1000/paper2": "Results AUC 0.8 " * 10})
    old = make_cand(0)
    old.extra["alt_ids"] = ["arxiv:2505.13400"]
    pipe.store.add(pipe._ingest([old], [[]], 1)[0])  # 已在库，别名是 arXiv
    looked = []
    cat = {"doi:10.1000/paper1": make_cand(1), "doi:10.1000/paper2": make_cand(2),
           "doi:10.1000/paper3": make_cand(3, title=old.title)}  # 标题与已在库的一致
    def lookup(eid):
        looked.append(eid)
        return cat.get(eid)

    res = pipe.add_manual(["arxiv:2505.13400", "doi:10.1000/PAPER1", "doi:10.1000/paper2",
                           "doi:10.1000/paper3", "doi:10.1000/missing", "doi:10.1000/paper1"],
                          note="CNS 趋势报告补录", lookup=lookup)
    assert "arxiv:2505.13400" not in looked  # alt id 命中，不再取元数据
    assert [e.id for e in res.accepted] == ["doi:10.1000/paper1", "doi:10.1000/paper2"]
    assert not any(t == "screen" for t, _ in llm.calls)  # 跳过评审团
    ev = pipe.store.get("doi:10.1000/paper2")
    assert [(v.role, v.vote, v.reason) for v in ev.panel] == [("manual", "yes", "CNS 趋势报告补录")]
    assert ev.fulltext_path == "cache" and ev.extraction["summary"] and ev.sections == ["2.1"]
    assert ev.added_round == 1 and res.log.round == 1 and res.log.n_accepted == 2
    log = spec.log_path.read_text(encoding="utf-8")
    assert "人工补录 2 篇" in log and "CNS 趋势报告补录" in log
    assert len(json.loads(spec.metrics_path.read_text())) == 1
    assert not spec.report_path.exists()  # add 不编译
    assert not any(t == "compile" for t, _ in llm.calls)

    again = pipe.add_manual(["doi:10.1000/paper1"], lookup=lookup)
    assert again.accepted == [] and len(json.loads(spec.metrics_path.read_text())) == 1


def test_add_manual_default_reason_and_requires_llm(spec):
    pipe = _pipe(spec, FakeLLM())
    res = pipe.add_manual(["doi:10.1000/paper4"], lookup=lambda eid: make_cand(4))
    assert res.accepted[0].panel[0].reason == "人工补录"
    with pytest.raises(RuntimeError):
        _pipe(spec, None).add_manual(["doi:10.1000/paper5"], lookup=lambda eid: make_cand(5))


def test_cli_add_dispatch(spec, monkeypatch, capsys):
    from radar import run
    from radar.background import llmio, runner
    import radar.background.spec as spec_mod
    got = {}
    monkeypatch.setattr(llmio, "available", lambda: True)
    monkeypatch.setattr(llmio, "RadarLLM", FakeLLM)
    monkeypatch.setattr(spec_mod, "load_spec", lambda slug: spec)
    def fake_add(self, ids, note="", lookup=None):
        got.update(ids=ids, note=note)
        return runner.RoundResult(log=runner.RoundLog(round=1, focus="人工补录", n_candidates=2, n_new=2,
                                                      n_accepted=2, n_rejected=0, n_borderline=0, coverage=0.5))
    monkeypatch.setattr(runner.Pipeline, "add_manual", fake_add)
    monkeypatch.setattr(run, "load_local_env", lambda: None)
    monkeypatch.setattr(sys, "argv", ["radar", "background", "add", "--topic", "x",
                                      "--ids", "doi:10.1/a, arxiv:2505.13400", "--note", "n"])
    run.main()
    assert got == {"ids": ["doi:10.1/a", "arxiv:2505.13400"], "note": "n"}
    monkeypatch.setattr(sys, "argv", ["radar", "background", "add", "--topic", "all", "--ids", "doi:10.1/a"])
    with pytest.raises(SystemExit):
        run.main()
