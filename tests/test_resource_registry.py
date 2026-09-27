"""资源登记：种子 / 别名 / 拆分 / 开放性默认 / 内容核验 / 置顶 / 日报收件箱。全部用假数据，不联网、不调 LLM。"""
import json
from datetime import date
from pathlib import Path

import pytest
import requests

from radar.background import resources as R
from radar.pipeline import resources as P
from radar.schema import Item

SEEDS_FILE = Path(__file__).resolve().parents[1] / "config" / "resource_seeds.yaml"


@pytest.fixture(scope="module")
def seeds():
    return R.load_seeds(SEEDS_FILE)


def row(name, kind="dataset", used_by=("a",), topics=("t1",), **kw):
    base = {"name": name, "kind": kind, "modality": "", "scale": "", "access": "", "open": "unknown",
            "used_by": list(used_by), "topics": list(topics), "note": ""}
    return {**base, **kw}


def test_seed_file_covers_profile_and_hand_registry(seeds):
    res = seeds["resources"]
    for name in ("ChinaHEART", "China Kadoorie Biobank", "China-PAR", "Pooled Cohort Equations", "Delphi-2M",
                 "ALADYNOULLI", "PhenoAge", "GrimAge", "LongevityBench"):
        s = res[R._norm(name)]
        assert s.get("pin") in ("P0", "P1"), name
    for name in ("UK Biobank", "All of Us Research Program", "ChinaHEART", "China Kadoorie Biobank"):
        assert res[R._norm(name)]["open"] == "controlled", name
    # 原 registry/*.md 手工条目（审计指出自动登记里缺的）
    for name in ("Aging Atlas", "Human Protein Atlas", "LINCS L1000", "DepMap", "CELLxGENE Census",
                 "GrimAge", "DunedinPACE"):
        assert R._norm(name, seeds["aliases"]) in res, name
    for s in res.values():
        assert s.get("open", "unknown") in R.OPEN_VALUES and s.get("kind") in R.KINDS


def test_aliases_merge_and_split_and_exclude(seeds):
    rows = [row("UK Biobank", scale="30,376人；2,923蛋白"), row("UKBB", used_by=["b"]),
            row("CHS", used_by=["c"]), row("Cardiovascular Health Study", used_by=["d"]),
            row("DI-NOv2", kind="model"), row("DINOv2", kind="model", used_by=["e"]),
            row("Olink Explore 3072", kind="tool"), row("Olink Proteomics", kind="tool", used_by=["f"]),
            row("DISCO", kind="database", access="https://www.immunesinglecell.org"),
            row("DISCO", kind="model", used_by=["g"]),
            row("GRPO", kind="tool")]
    reg = R.merge(rows, seeds=seeds)
    assert len(reg["uk biobank"]["used_by"]) == 2
    assert len(reg["cardiovascular health study"]["used_by"]) == 2
    assert len(reg["dinov2"]["used_by"]) == 2 and len(reg["olink"]["used_by"]) == 2
    discos = sorted(r["name"] for k, r in reg.items() if k.startswith("disco"))
    assert discos == ["DISCO (ECG HFrEF study)", "DISCO (single-cell database)"]
    assert not any("grpo" in k for k in reg)


def test_apply_seeds_overrides_scale_open_and_pins(seeds):
    reg = R.merge([row("UK Biobank", scale="30,376人；2,923蛋白", open="yes", access="https://x.org"),
                   row("China Kadoorie Biobank", open="restricted"),
                   row("ChinaHEART", scale="巢式病例对照")], seeds=seeds)
    R.apply_seeds(reg, seeds)
    ukb = reg["uk biobank"]
    assert "50 万" in ukb["scale"] and ukb["scale_src"] == "seed" and ukb["access"] == "https://www.ukbiobank.ac.uk/"
    R.finalize_open(reg)
    assert ukb["open"] == "controlled" and reg["chinaheart"]["open"] == "controlled"
    assert reg["china kadoorie biobank"]["priority"] == "P0" and reg["chinaheart"]["pinned"]
    # 种子里有、证据里没有的也进登记且进主表
    assert R.is_core(reg[R._norm("Delphi-2M")]) and reg[R._norm("Delphi-2M")]["priority"] == "P0"
    assert R.is_core(reg[R._norm("Aging Atlas")])
    # 置顶的不交给 LLM 重排
    class LLM:
        def chat(self, prompt, **kw):
            assert "ChinaHEART\"" not in prompt.split("【资源】")[-1]
            return "[]"
    R.prioritize(reg, LLM(), only_missing=False)
    assert reg["chinaheart"]["priority"] == "P0"


def test_open_defaults_to_unknown_unless_confirmed():
    reg = {"a": row("ToolA", kind="model", open="yes", access="https://github.com/x/toola"),
           "b": row("PaperOnly", kind="model", open="yes", access="https://doi.org/10.1/abc"),
           "c": row("ToolC", kind="model", open="yes", access="https://github.com/x/toolc"),
           "d": row("Restricted", open="restricted")}
    for k, r in reg.items():
        r["open_claim"] = r["open"]
    reg["a"]["verified"], reg["b"]["verified"], reg["c"]["verified"] = "ok", "ok", "mismatch"
    R.finalize_open(reg)
    assert [reg[k]["open"] for k in "abcd"] == ["yes", "unknown", "unknown", "unknown"]
    assert reg["d"]["open_claim"] == "restricted"


LOREM = "<p>" + " ".join(f"word{i}" for i in range(200)) + "</p>"


class FakeWeb:
    def __init__(self, pages):
        self.pages, self.calls = pages, []

    def __call__(self, url):
        self.calls.append(url)
        v = self.pages.get(url, (404, ""))
        if isinstance(v, Exception):
            raise v
        return v


def test_check_link_by_content():
    web = FakeWeb({
        "https://ok.org": (200, "<title>ARCHS4</title> gene expression"),
        "https://wrong.org": (200, "<title>Dietary patterns and health</title>" + LOREM),
        "https://redirect.org": (200, "<title>Redirecting</title><p>wait</p>"),
        "https://bot.org": (403, "forbidden"),
        "https://cf.org": (200, "<title>Just a moment...</title>"),
        "https://gone.org": (404, ""),
        "https://slow.org": requests.exceptions.Timeout("t"),
        "https://nxdomain.org": requests.exceptions.ConnectionError("Failed to resolve: Name or service not known"),
        "https://api.crossref.org/works/10.1038/s41591-023-02235-5":
            (200, json.dumps({"message": {"title": ["Dietary patterns and mortality"]}})),
        "https://doi.org/10.1038/s41591-023-02235-5": (200, "<title>Dietary patterns</title> 10.1038/s41591-023-02235-5" + LOREM),
        "https://api.crossref.org/works/10.1016/j.cell.2026.08.026":
            (200, json.dumps({"message": {"title": ["LongevityBench: a benchmark for aging biology AI"]}})),
    })
    assert R.check_link({"name": "ARCHS4"}, "https://ok.org", web) == "ok"
    assert R.check_link({"name": "ARCHS4"}, "https://wrong.org", web) == "mismatch"
    assert R.check_link({"name": "ARCHS4"}, "https://redirect.org", web) == "blocked"  # 跳转壳页无从判断
    assert R.check_link({"name": "X1"}, "https://bot.org", web) == "blocked"
    assert R.check_link({"name": "X1"}, "https://cf.org", web) == "blocked"
    assert R.check_link({"name": "X1"}, "https://gone.org", web) == "dead"
    assert R.check_link({"name": "X1"}, "https://slow.org", web) == "blocked"
    assert R.check_link({"name": "X1"}, "https://nxdomain.org", web) == "dead"
    # 审计里的 CODE15 错链接：DOI 能打开，但是另一篇论文
    assert R.check_link({"name": "CODE15", "aliases": ["CODE-15%"]},
                        "https://doi.org/10.1038/s41591-023-02235-5", web) == "mismatch"
    # DOI 走 Crossref 标题，不碰出版社页面
    n = len(web.calls)
    assert R.check_link({"name": "LongevityBench"}, "https://doi.org/10.1016/j.cell.2026.08.026", web) == "ok"
    assert len(web.calls) == n + 1


def test_needles_use_parenthetical_abbrev_and_aliases():
    ns = R.needles({"name": "UK Biobank Pharma Proteomics Project (UKB-PPP)", "aliases": ["UKB PPP"]})
    assert "ukb ppp" in ns and "uk biobank pharma proteomics project" in ns


def test_needles_short_suffix_and_datacite_doi():
    assert "imagenet" in R.needles({"name": "ImageNet-1k"})
    assert "code" not in R.needles({"name": "CODE 15"})
    web = FakeWeb({"https://doi.org/10.48550/arXiv.2605.26087": (200, "<title>DiscoverPhysics benchmark</title>" + LOREM)})
    # Crossref 对 arXiv（DataCite）DOI 返回 404，不能判 dead
    assert R.check_link({"name": "DiscoverPhysics"}, "https://doi.org/10.48550/arXiv.2605.26087", web) == "ok"


def test_verify_content_mode_and_legacy_head():
    reg = {"a": row("ARCHS4", access="https://ok.org"), "b": row("Portal only", access="GEO: GSE1")}
    R.verify(reg, fetch=FakeWeb({"https://ok.org": (200, "ARCHS4 home")}))
    assert reg["a"]["verified"] == "ok" and reg["b"]["verified"] == "n/a"
    R.verify(reg, head=lambda u: 503)
    assert reg["a"]["verified"] == "blocked"


def test_fold_inbox_new_and_known(seeds):
    reg = R.merge([row("UK Biobank")], seeds=seeds)
    inbox = [{"name": "UKB", "kind": "dataset", "url": "https://doi.org/10.1/ukbpaper", "day": "2026-09-20"},
             {"name": "A new single-cell atlas", "kind": "dataset", "url": "https://doi.org/10.1/new",
              "note": "新图谱", "day": "2026-09-26", "theme": "singlecell"}]
    assert R.fold_inbox(reg, inbox, seeds) == 1
    assert reg["uk biobank"]["daily_urls"] == ["https://doi.org/10.1/ukbpaper"]
    new = reg[R._norm("A new single-cell atlas")]
    assert new["status"] == "new" and not R.is_core(new) and new["access"] == "https://doi.org/10.1/new"
    R.attach_themes(reg, topic_names={})
    assert new["themes"] == ["singlecell"]
    md = R.render(reg)
    assert "## 日报新发现（1，未核验）" in md and "A new single-cell atlas" in md


def test_run_resources_with_seeds_and_inbox(tmp_path, seeds):
    base = tmp_path / "background"
    (base / "_resources").mkdir(parents=True)
    old = R.merge([row("UK Biobank", used_by=["a", "b"], scale="30,376人", access="https://www.ukbiobank.ac.uk/",
                       priority="P2"),
                   row("scGPT", kind="model", open="yes", access="https://github.com/bowang-lab/scGPT")])
    (base / "_resources" / "registry.json").write_text(json.dumps(old), encoding="utf-8")
    inbox = [{"name": "Brand new model", "kind": "model", "url": "https://github.com/lab/new", "day": "2026-09-26",
              "source": "daily"}]
    pages = {"https://www.ukbiobank.ac.uk/": (403, ""), "https://github.com/bowang-lab/scGPT": (200, "scGPT repo"),
             "https://github.com/lab/new": (200, "Brand new model")}
    out = R.run_resources(None, root=base, fetch=lambda u: pages.get(u, (404, "")), seeds=seeds, inbox=inbox)
    reg = json.loads((base / "_resources" / "registry.json").read_text(encoding="utf-8"))
    ukb = reg["uk biobank"]
    assert ukb["priority"] == "P2" and ukb["open"] == "controlled" and "50 万" in ukb["scale"]
    assert ukb["verified"] == "blocked"
    assert reg["scgpt"]["open"] == "yes" and reg["scgpt"]["verified"] == "ok"
    assert reg["chinaheart"]["priority"] == "P0"
    assert reg["brand new model"]["status"] == "new"
    assert "日报新发现" in out.read_text(encoding="utf-8")
    # 再跑一次（周更重渲染）：种子与收件箱条目不重复、不丢
    R.run_resources(None, root=base, fetch=lambda u: pages.get(u, (404, "")), seeds=seeds, inbox=inbox)
    reg2 = json.loads((base / "_resources" / "registry.json").read_text(encoding="utf-8"))
    assert set(reg2) == set(reg)


# ---------------- 日报收件箱（pipeline/resources.py）----------------

def _item(title, url, kind="dataset", score=8.0, domain="data_models"):
    return Item(id=url, source="europepmc", domain=domain, title=title, url=url, score=score,
                reason_zh="理由", extra={"kind": kind})


def test_append_resources_writes_inbox_without_llm(tmp_path, monkeypatch):
    inbox = tmp_path / "data" / "resources_inbox.json"
    monkeypatch.setattr(P, "INBOX", inbox)
    monkeypatch.setattr(P.llm, "chat", lambda *a, **k: (_ for _ in ()).throw(AssertionError("no LLM")))
    items = [_item("Atlas A", "https://doi.org/10.1/a"), _item("Low", "https://x/low", score=5.0),
             _item("Method paper", "https://x/m", kind="method")]
    assert P.append_resources(items, date(2026, 9, 27)) == 1
    assert P.append_resources(items, date(2026, 9, 28)) == 0  # 按 URL 去重
    data = json.loads(inbox.read_text(encoding="utf-8"))
    assert data[0]["name"] == "Atlas A" and data[0]["source"] == "daily" and data[0]["theme"] == "singlecell"


def test_mine_infrastructure_feeds_inbox(tmp_path, monkeypatch):
    inbox = tmp_path / "resources_inbox.json"
    monkeypatch.setattr(P, "INBOX", inbox)
    monkeypatch.setattr(P.llm, "available", lambda: True)
    monkeypatch.setattr(P.llm, "chat", lambda *a, **k: json.dumps(
        [{"name": "Tahoe-100M", "usage": "扰动训练", "used_by": [0, 1]}, {"name": "Solo", "used_by": [2]}]))
    recs = [{"title": f"paper {i}", "data": "Tahoe-100M"} for i in range(3)]
    assert P.mine_infrastructure(recs, date(2026, 9, 27)) == 1
    assert P.mine_infrastructure(recs, date(2026, 9, 28)) == 0
    e = json.loads(inbox.read_text(encoding="utf-8"))[0]
    assert e["name"] == "Tahoe-100M" and e["source"] == "daily-infra" and len(e["used_by_titles"]) == 2


def test_migrate_legacy_md(tmp_path):
    md = tmp_path / "resources.md"
    md.write_text("# 可用资源清单\n\n## 单细胞 / 空间组学\n\n"
                  "- [Atlas](https://doi.org/10.1/atlas) — 一个图谱\n  `dataset` · 单细胞 · `7.0` 分 · 2026-09-22\n\n"
                  "## 领域基础设施（被多篇高分工作反复使用）\n\n"
                  "- **TCGA** — 训练基准\n  被 2 篇高分工作使用：a / b · 2026-09-20 收录\n", encoding="utf-8")
    ib = tmp_path / "inbox.json"
    assert P.migrate_legacy_md(md, ib, date(2026, 9, 27)) == 2
    assert P.migrate_legacy_md(md, ib, date(2026, 9, 27)) == 0
    data = json.loads(ib.read_text(encoding="utf-8"))
    assert data[0]["kind"] == "dataset" and data[0]["day"] == "2026-09-22" and data[0]["theme"] == "singlecell"
    assert data[1]["name"] == "TCGA" and data[1]["source"] == "daily-infra"
