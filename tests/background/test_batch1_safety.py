"""第一批（止血）修复的回归测试：LLM 失败不写坏状态、残缺报告不发布、括号 URL、XSS、健康摘要。"""
import json
from datetime import date, timedelta

import pytest

from radar.pipeline import retag, site
from radar.pipeline.dedup import filter_new, mark_seen
from radar.schema import Item


def _it(i):
    return Item(id=f"doi:10.1/{i}", source="europepmc", domain="d", title=f"T{i}", url="u")


def test_filter_new_without_commit_then_mark(tmp_path):
    st = tmp_path / "seen.json"
    a, b = _it("a"), _it("b")
    assert [x.id for x in filter_new([a, b, a], state_path=st, commit=False)] == [a.id, b.id]
    assert not st.exists()  # 未提交：LLM 失败时这些条目下次还能出现
    mark_seen([a], state_path=st)
    assert [x.id for x in filter_new([a, b], state_path=st, commit=False)] == [b.id]


def test_llm_retry_counts(monkeypatch):
    from radar import llm
    calls = []

    class R:
        status_code = 200
        def raise_for_status(self): pass
        def json(self): return {"choices": [{"message": {"content": "ok"}}]}

    def post(*a, **k):
        calls.append(1)
        if len(calls) < 2:
            raise TimeoutError("slow")
        return R()
    monkeypatch.setattr(llm, "llm_api_key", lambda: "k")
    monkeypatch.setattr(llm.requests, "post", post)
    monkeypatch.setattr(llm.time, "sleep", lambda s: None)
    before = dict(llm.STATS)
    assert llm.chat("x") == "ok" and len(calls) == 2 and llm.STATS["ok"] == before["ok"] + 1


PAREN = ("# d\n\n## 心血管（1 条）\n\n"
         "- **[Lancet paper](https://doi.org/10.1016/S0140-6736(24)01234-5)** `8.0` — r\n"
         "  <sub>〔期刊〕The Lancet · 2026-09 · A</sub>\n")


def test_paren_url_survives_site_and_retag(tmp_path, monkeypatch):
    it = site._parse_digest(PAREN)[0][1][0]
    assert it["url"] == "https://doi.org/10.1016/S0140-6736(24)01234-5"
    assert retag.parse_blocks(PAREN)[0]["url"].endswith("(24)01234-5")
    p = tmp_path / "2026-09-27.md"; p.write_text(PAREN, encoding="utf-8")
    monkeypatch.setattr(retag, "llm_tags", lambda b: {0: ["cardio"]})
    monkeypatch.setattr(retag, "day_summary", lambda e: [])
    assert retag.retag_digest(p) == 1 and "S0140-6736(24)01234-5" in p.read_text(encoding="utf-8")


def test_markdown_is_sanitized():
    out = site._md("x <script>alert(1)</script> [a](javascript:alert(1)) **b**", ["extra"])
    assert "<script>" not in out and "javascript:" not in out and "<strong>b</strong>" in out


def test_compile_failure_keeps_previous_report(spec, monkeypatch):
    from radar.background import compile as C
    from radar.background.llmio import GenerationFailed
    from radar.background.outline import Outline
    from tests.background.conftest import FakeLLM, make_cand
    from radar.background.models import Evidence
    evs = [Evidence(candidate=make_cand(1), panel=[])]
    o = Outline.from_spec(spec); o.attach("2.1", [evs[0].id])
    with pytest.raises(GenerationFailed):
        C.compile_report(spec, o, evs, FakeLLM(fail_tasks={"compile"}), 0.5, 2)


def test_renew_with_empty_inbox_skips(spec, tmp_path):
    from radar.background.runner import Pipeline
    from tests.background.conftest import FakeLLM
    spec.report_path.write_text("# old · 方向背景报告\n\nkeep\n", encoding="utf-8")
    inbox = tmp_path / "ex.jsonl"; inbox.write_text("", encoding="utf-8")
    res = Pipeline(spec, FakeLLM()).renew(inbox)
    assert res.report_path is None and spec.report_path.read_text(encoding="utf-8").endswith("keep\n")
    assert not spec.metrics_path.exists()


def test_weekly_changes_skips_stale_reports(spec, topic_dir):
    from radar.background.context import weekly_changes
    old = (date.today() - timedelta(days=20)).isoformat()
    spec.report_path.write_text(f"# x · 方向背景报告\n\n证据 1 篇 · 更新 {old}\n\n## 本次变更\n\n- 新增 [1] A\n", encoding="utf-8")
    assert weekly_changes(base=topic_dir.parent) == ""


def test_health_written_with_problems(tmp_path, monkeypatch):
    from radar import run
    monkeypatch.setattr(run, "ROOT", tmp_path)
    run.write_health({"date": "2026-09-27", "sources": {"arxiv": 0, "europepmc": 30, "hf": -1},
                      "errors": [], "stages": {"score": {"sent": 10, "unscored": 3}}, "llm": {"ok": 5, "fail": 2}})
    h = json.loads((tmp_path / "data" / "health.json").read_text(encoding="utf-8"))
    assert h["problems"] == ["hf 采集失败", "arxiv 0 条", "LLM 失败 2 次", "3 条未打分已顺延"]
