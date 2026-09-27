from datetime import date

from radar import themes
from radar.pipeline import retag
from radar.pipeline.digest import assemble, item_block
from radar.pipeline.site import _parse_digest, _summary_html
from radar.schema import Item

OLD = """# 科研情报 digest — 2026-09-26

共 2 条（仅保留 ≥6 分；另有 41 条低分已过滤）。分数 0-10，10 = 必须马上读。

## 人群健康与多组学 AI（2 条）

- **[Proteomics CAD](https://doi.org/10.1/a)** `8.0` — 心血管蛋白组
  <sub>〔期刊〕Nature Medicine · 2026-09 · 通讯 X（Y） · A B</sub>
  <sub>定位：人群健康与多组学 AI › 2.2 多组学 · 新增</sub>
  <details markdown="1"><summary>深读</summary>

  **总结**
  body

  </details>
- **[EHR model](https://doi.org/10.1/b)** `6.0` — EHR
  <sub>europepmc · 2026-09-23 · C D</sub>
"""


def test_parse_blocks_keeps_raw_lines():
    bs = retag.parse_blocks(OLD)
    assert [b["title"] for b in bs] == ["Proteomics CAD", "EHR model"]
    assert bs[0]["section"] == "人群健康与多组学 AI" and bs[0]["lines"][-1] == "  </details>" and bs[0]["bg"].startswith("人群健康")


def test_resolve_and_theme_line_order():
    bs = retag.parse_blocks(OLD)
    names = {"人群健康与多组学 AI": "population-omics-ai"}
    tags = retag.resolve_themes(bs[0], ["cardio"], names)
    assert tags == ["cardio", "cohort"]  # LLM 标签在前，定位方向补在后
    lines = retag.with_theme_line(bs[0]["lines"], tags)
    assert lines[2] == "  <sub>主题：#心血管 #人群队列</sub>" and lines[3].startswith("  <sub>定位：")
    assert retag.resolve_themes(bs[1], [], names) == []  # LLM 判无主题且无定位：不再按节名（领域）兜底
    assert retag.resolve_themes(bs[1], None, names) == bs[1]["themes"]  # LLM 没回答：沿用旧标签


def test_retag_digest_regroups_by_theme(tmp_path, monkeypatch):
    p = tmp_path / "2026-09-26.md"; p.write_text(OLD, encoding="utf-8")
    monkeypatch.setattr(retag, "llm_tags", lambda blocks: {0: ["cardio"], 1: ["cohort"]})
    monkeypatch.setattr(retag, "day_summary", lambda entries: ["- #心血管 蛋白组 CAD", "- 必读：Proteomics CAD"])
    assert retag.retag_digest(p) == 2
    out = p.read_text(encoding="utf-8")
    assert out.index("## 今日要点") < out.index("## 人群队列（1 条）") < out.index("## 心血管（1 条）")  # 节序跟 themes.yaml
    assert "另有 41 条低分已过滤" in out and "  </details>" in out
    secs = _parse_digest(out)
    it = [x for _, items in secs for x in items if x["title"] == "Proteomics CAD"][0]
    assert it["themes"] == ["cardio", "cohort"] and it["bg"] and it["meta"].startswith("〔期刊〕") and it["deep"]
    html_sum = _summary_html(out)
    assert 'class="th"' in html_sum and "<b>必读：</b>" in html_sum
    assert retag.retag_digest(p) == 2 and p.read_text(encoding="utf-8").count("主题：") == 2  # 幂等


def test_item_block_and_assemble_other_section():
    it = Item(id="x", source="github", domain="zzz", title="Repo", url="u", score=7.0)
    blk = item_block(it, [])
    md = assemble(date(2026, 9, 27), [{"themes": [], "score": 7.0, "lines": blk}], [], 3)
    assert "## 其他（1 条）" in md and "主题：" not in md
    assert themes.line(["cardio", "nope"]) == "#心血管"
