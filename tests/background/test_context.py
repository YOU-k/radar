import json

from radar.background.context import annotate, topics_by_domain, weekly_changes
from radar.background.models import Candidate, Evidence
from radar.background.outline import Outline
from radar.background.store import EvidenceStore
from radar.schema import Item
from tests.background.conftest import make_cand


class CtxLLM:
    def __init__(self): self.calls = []
    def chat(self, prompt, *, task="", temperature=0.2, timeout=180):
        self.calls.append(prompt)
        return json.dumps([{"id": 0, "section": "2.1 生成式疾病轨迹模型", "delta": "首次加入蛋白组作为状态"},
                           {"id": 1, "section": "新子题", "delta": ""}])


def test_annotate_places_items(spec, topic_dir):
    o = Outline.from_spec(spec); o.attach("2.1", ["doi:10.1000/paper1"]); spec.outline_path.write_text(o.to_markdown(), encoding="utf-8")
    EvidenceStore(spec.evidence_dir, spec.rejected_path).add(Evidence(candidate=make_cand(1), panel=[]))
    items = [Item(id="a", source="s", domain="population_omics_ai", title="New EHR+proteome model", url="u", score=7.0),
             Item(id="b", source="s", domain="population_omics_ai", title="Odd", url="u", score=6.5),
             Item(id="c", source="s", domain="population_omics_ai", title="Low", url="u", score=3.0),
             Item(id="d", source="s", domain="agents", title="Other domain", url="u", score=9.0)]
    llm = CtxLLM()
    n = annotate(items, {}, llm=llm, base=topic_dir.parent)
    assert n == 2 and items[0].extra["bg"].startswith("人群健康与多组学 AI › 2.1") and "蛋白组" in items[0].extra["bg"]
    assert items[1].extra["bg"].endswith("新子题") and "bg" not in items[2].extra and "bg" not in items[3].extra
    assert "2.1 生成式疾病轨迹模型" in llm.calls[0] and '"n": 1' in llm.calls[0]


def test_weekly_changes_collects_blocks(spec, topic_dir):
    spec.report_path.write_text("# x · 方向背景报告\n\nstats\n\n## 本次变更\n\n- 新增 [1] A\n\n## 摘要（TL;DR）\n\n- y\n", encoding="utf-8")
    out = weekly_changes(base=topic_dir.parent)
    assert "## 方向背景本周变更" in out and "### 人群健康与多组学 AI" in out and "- 新增 [1] A" in out
    spec.report_path.write_text("# x · 方向背景报告\n\n## 本次变更\n\n- 无新增\n\n## 摘要\n", encoding="utf-8")
    assert weekly_changes(base=topic_dir.parent) == ""


def test_background_slugs_all(monkeypatch, tmp_path):
    from radar.background import spec as spec_mod
    from radar import run as run_mod
    for name in ("b-topic", "a-topic", "_joint"):
        (tmp_path / name).mkdir(); (tmp_path / name / "topic.yaml").write_text("name: x\n")
    monkeypatch.setattr(spec_mod, "BASE", tmp_path)
    assert run_mod.background_slugs("all") == ["a-topic", "b-topic"]
    assert run_mod.background_slugs("a-topic") == ["a-topic"]


def test_annotate_picks_topic_when_domain_has_several(spec, topic_dir, tmp_path):
    import shutil
    o = Outline.from_spec(spec); o.attach("2.1", ["doi:10.1000/paper1"]); spec.outline_path.write_text(o.to_markdown(), encoding="utf-8")
    EvidenceStore(spec.evidence_dir, spec.rejected_path).add(Evidence(candidate=make_cand(1), panel=[]))
    other = topic_dir.parent / "cardio"
    shutil.copytree(topic_dir, other)
    y = (other / "topic.yaml").read_text(encoding="utf-8").replace("name: 人群健康与多组学 AI", "name: 心血管方向")
    y = y.replace("radar_domain: population_omics_ai", "radar_domain: [cardio_omics, population_omics_ai]")
    (other / "topic.yaml").write_text(y, encoding="utf-8")

    class L:
        def __init__(self): self.calls = []
        def chat(self, prompt, **kw):
            self.calls.append(prompt)
            return json.dumps([{"id": 0, "topic": "心血管方向", "section": "2.2 多组学与遗传整合", "delta": "新蛋白组 CVD"}])
    llm = L()
    items = [Item(id="a", source="s", domain="population_omics_ai", title="Proteomics CAD", url="u", score=7.0)]
    assert annotate(items, {}, llm=llm, base=topic_dir.parent) == 1
    assert items[0].extra["bg"].startswith("心血管方向 › 2.2") and '"topic"' in llm.calls[0]
    assert len(llm.calls) == 1  # cardio_omics 域无条目，不调用
