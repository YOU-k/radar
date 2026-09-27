from datetime import datetime, timezone

from radar.collectors import huggingface as hf

NOW = datetime(2026, 9, 27, tzinfo=timezone.utc)


def _m(mid, created, likes=0, tags=()):
    return {"id": mid, "createdAt": created, "likes": likes, "downloads": 5, "tags": list(tags)}


ROWS = [
    _m("lab/jepa-cells", "2026-09-25T01:00:00.000Z", tags=["arxiv:2609.24385", "region:us"]),
    _m("me/jepa-practice", "2026-09-26T01:00:00.000Z", tags=["arxiv:1910.09700"]),  # 模板论文，不算
    _m("org/popular", "2026-09-20T01:00:00.000Z", likes=5),
    _m("lab/old-release", "2026-07-01T01:00:00.000Z", likes=50, tags=["arxiv:2601.00001"]),  # 窗口外
    _m("lab/jepa-cells-v2", "2026-09-25T02:00:00.000Z", tags=["arxiv:2609.24385"]),  # 同一论文第二个仓库
    _m("me/ft-of-old-paper", "2026-09-24T01:00:00.000Z", tags=["arxiv:2410.19008"]),  # 老论文的微调
    _m("q/Big-Agentic-Merge-GGUF", "2026-09-24T01:00:00.000Z", likes=9, tags=["gguf"]),  # 量化二次打包
]


def test_select_quality_gate_and_window():
    cutoff = NOW.replace(day=13)
    kept, n_recent = hf.select(ROWS, cutoff, NOW)
    assert n_recent == 6
    assert sorted(m["id"] for m in kept) == ["lab/jepa-cells", "org/popular"]


def test_collect_uses_created_and_min_window():
    calls = []

    def fetch(kind, q):
        calls.append((kind, q))
        return ROWS if kind == "models" else []

    cfg = {"domains": [{"name": "ml", "hf_queries": ["jepa"], "hf_cadence": "weekly"},
                       {"name": "skip", "hf_queries": ["x"], "hf_cadence": "monthly"}]}
    items = hf.collect(cfg, {"daily": 2, "weekly": 7}, fetch=fetch, now=NOW)
    assert calls == [("models", "jepa"), ("datasets", "jepa")]
    # weekly 节奏也至少看 14 天：09-20 的 org/popular 仍在窗口内
    assert {it.id for it in items} == {"hf:models:lab/jepa-cells", "hf:models:org/popular"}
    it = next(i for i in items if i.id == "hf:models:lab/jepa-cells")
    assert it.published == "2026-09-25" and it.extra["arxiv"] == ["2609.24385"]
    assert "arXiv:2609.24385" in it.abstract
