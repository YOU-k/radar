from radar.pipeline.site import _render_background


def test_render_background_card(tmp_path):
    d = tmp_path / "bg" / "topic-a"; d.mkdir(parents=True)
    (d / "report.md").write_text("# 方向甲 · 方向背景报告\n\n证据 3 篇 · 覆盖度 0.50 · 第 2 轮 · 更新 2026-09-23\n\n## 摘要（TL;DR）\n\n- 要点 [1]\n", encoding="utf-8")
    out = _render_background(d / "report.md")
    assert "方向甲" in out and "证据 3 篇" in out and "<h2>摘要" in out and 'class="bg"' in out
