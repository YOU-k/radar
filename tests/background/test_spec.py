import pytest

from radar.background.spec import DEFAULT_ROLES, init_topic, load_spec


def test_load_spec_defaults_and_paths(spec, topic_dir):
    assert spec.slug == "population-omics-ai"
    assert [r["name"] for r in spec.roles] == [r["name"] for r in DEFAULT_ROLES]
    assert spec.budget["rounds"] == 3 and spec.budget["stop_delta"] == 0.02
    assert spec.evidence_dir == topic_dir / "evidence"
    assert "纳入标准" in spec.profile_text() and "UK Biobank" in spec.profile_text()


def test_invalid_spec_rejected(tmp_path):
    d = tmp_path / "bad"; d.mkdir()
    (d / "topic.yaml").write_text("name: x\nroles: [{name: bio}]\n", encoding="utf-8")
    with pytest.raises(ValueError) as e:
        load_spec(d / "topic.yaml")
    assert "queries" in str(e.value) and "rubric" in str(e.value)


def test_init_topic_writes_template_once(tmp_path):
    p = init_topic("new-topic", "新方向", root=tmp_path)
    assert p.exists() and (tmp_path / "new-topic" / "evidence").is_dir()
    p.write_text("name: kept\nqueries: [q]\n", encoding="utf-8")
    init_topic("new-topic", "again", root=tmp_path)
    assert load_spec(p).name == "kept"
