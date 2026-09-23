"""端到端：bootstrap 2 轮 + renew 1 轮，全部用 FakeLLM 和假来源，不联网。"""
import json

from radar.background.models import DiscoveryPlan
from radar.background.runner import Pipeline
from tests.background.conftest import FakeLLM, make_cand


class FakeSource:
    name = "fake"
    def __init__(self, batches):
        self.batches, self.n = batches, 0
    def fetch(self, spec, plan):
        b = self.batches[min(self.n, len(self.batches) - 1)]; self.n += 1
        return list(b)


def test_bootstrap_two_rounds_then_renew(spec, tmp_path):
    seed = make_cand(0, doi="10.1038/s41586-025-09529-3", citations=300)
    r1 = [seed] + [make_cand(i, citations=10 - i) for i in range(1, 5)]
    r2 = [make_cand(i, citations=3) for i in range(3, 8)]  # 3,4 已见过 → 去重
    llm = FakeLLM()  # 偶数序号 yes；序号按 dedup 后顺序，所以只断言结构
    pipe = Pipeline(spec, llm, sources=[FakeSource([r1, r2])], fetch_text=False)
    results = pipe.bootstrap(rounds=2)
    assert len(results) == 2
    assert results[0].report_path is None and results[1].report_path == spec.report_path  # 只在末轮编译
    assert results[1].log.n_new == 3  # 5 个候选里 3,4 已在第一轮见过

    st = pipe.store
    assert st.stats()["evidence"] + st.stats()["rejected"] == 8
    assert all(len(e.panel) == 2 and e.extraction["summary"] for e in st.all())
    assert all(e.sections for e in st.all())  # 都挂到了大纲上
    hist = json.loads(spec.metrics_path.read_text())
    assert [h["round"] for h in hist] == [1, 2] and "第 1 轮" in spec.log_path.read_text()
    rep = spec.report_path.read_text()
    assert "## 参考文献" in rep and "[doi:" not in rep and "## 本次变更" in rep

    # renew：日报 inbox 里一条新的、一条已见过
    from datetime import date
    inbox = tmp_path / "extractions.jsonl"
    inbox.write_text("\n".join(json.dumps(r) for r in [
        {"date": date.today().isoformat(), "domain": "population_omics_ai", "score": 8,
         "title": "Brand new paper", "url": "https://doi.org/10.2000/new", "summary": "x"},
        {"date": date.today().isoformat(), "domain": "population_omics_ai", "score": 9,
         "title": seed.title, "url": seed.url, "summary": "dup"}]), encoding="utf-8")
    res = pipe.renew(inbox)
    assert res.log.round == 3 and res.log.n_candidates == 2 and res.log.n_new == 1
    assert res.report_path == spec.report_path
    assert len(json.loads(spec.metrics_path.read_text())) == 3


def test_plateau_stops_early_and_still_compiles(spec, tmp_path, monkeypatch):
    from radar.background import metrics as m
    monkeypatch.setattr(m, "should_stop", lambda hist, delta: len(hist) >= 2)
    pipe = Pipeline(spec, FakeLLM(), sources=[FakeSource([[make_cand(i) for i in range(4)], []])],
                    fetch_text=False)
    results = pipe.bootstrap(rounds=5)
    assert len(results) == 2 and results[-1].report_path == spec.report_path
    assert len(json.loads(spec.metrics_path.read_text())) == 2  # 收尾编译不再多记一轮
    assert spec.log_path.read_text().count("## 第") == 2


def test_without_llm_only_collects(spec):
    pipe = Pipeline(spec, None, sources=[FakeSource([[make_cand(1), make_cand(2)]])], fetch_text=False)
    res = pipe.bootstrap(rounds=1)[0]
    assert res.log.n_new == 2 and res.log.n_accepted == 0 and res.report_path is None
    assert pipe.store.stats()["evidence"] == 0


def test_fulltext_fetcher_injected(spec):
    calls = []
    def fetcher(cand, cache_dir):
        calls.append(cand.id); return "full text"
    allyes = {"bio": {0: "yes", 1: "yes"}, "media": {0: "yes", 1: "yes"}}
    pipe = Pipeline(spec, FakeLLM(votes=allyes), sources=[FakeSource([[make_cand(0), make_cand(2)]])], fetcher=fetcher)
    pipe.bootstrap(rounds=1)
    assert len(calls) == 2 and all(e.fulltext_path for e in pipe.store.all())


def test_refetch_fills_fulltext_and_reextracts(spec):
    allyes = {"bio": {0: "yes", 1: "yes"}, "media": {0: "yes", 1: "yes"}}
    pipe = Pipeline(spec, FakeLLM(votes=allyes), sources=[FakeSource([[make_cand(0), make_cand(2)]])],
                    fetcher=lambda c, d: "")  # 第一次拿不到全文
    pipe.bootstrap(rounds=1)
    assert all(not e.fulltext_path for e in pipe.store.all())
    pipe.fetcher = lambda c, d: "now full text"
    assert pipe.refetch() == 2
    assert all(e.fulltext_path and e.extraction["summary"] for e in pipe.store.all())


def test_top_cited_is_cumulative(spec):
    src = FakeSource([[make_cand(1, citations=900)], [make_cand(2, citations=5)]])
    pipe = Pipeline(spec, FakeLLM(), sources=[src], fetch_text=False)
    pipe.bootstrap(rounds=2)
    top = pipe.top_cited()
    assert top[0] == "doi:10.1000/paper1" and "doi:10.1000/paper2" in top  # 第 1 轮的高引仍在
