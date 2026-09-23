from radar.pipeline.site import _parse_digest, _render_background


def test_render_background_card(tmp_path):
    d = tmp_path / "bg" / "topic-a"; d.mkdir(parents=True)
    (d / "report.md").write_text("# 方向甲 · 方向背景报告\n\n证据 3 篇 · 覆盖度 0.50 · 第 2 轮 · 更新 2026-09-23\n\n## 摘要（TL;DR）\n\n- 要点 [1]\n", encoding="utf-8")
    out = _render_background(d / "report.md")
    assert "方向甲" in out and "证据 3 篇" in out and "<h2>摘要" in out and 'class="bg"' in out


def test_digest_parse_keeps_bg_line():
    md = ("# d\n\n## 领域（1 条）\n\n- **[T](https://x)** `7.0` — r\n  <sub>arxiv · 2026 · A</sub>\n"
          "  <sub>定位：方向 › 2.1 子题 · 新增蛋白组</sub>\n")
    secs = _parse_digest(md)
    it = secs[0][1][0]
    assert it["meta"] == "arxiv · 2026 · A" and it["bg"] == "方向 › 2.1 子题 · 新增蛋白组"
