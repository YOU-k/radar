"""第二批（内容质量）日报侧：机构宁缺毋错、bioRxiv 优先、期刊下限、主题不兜底、要点规则、深读应用线、去重与增长。"""
import json
from datetime import date

from radar import llm as radar_llm
from radar.pipeline import deepread, dedup, score, summary
from radar.pipeline.enrich import enrich, pi_from_openalex, venue_line
from radar.schema import Item


def fake_get(table):
    def get(url, params=None, timeout=30):
        return table.get(url)
    return get


# ---- 4. 元数据 ----

def test_no_coauthor_institution_fallback():
    w = {"authorships": [{"author": {"display_name": "Pablo Muse"}, "institutions": [{"display_name": "IFUMI"}]},
                         {"author": {"display_name": "Gabriele Facciolo"}, "institutions": []}]}
    assert pi_from_openalex(w) == ("Gabriele Facciolo", "", False)
    it = Item(id="doi:10.48550/arxiv.2609.21656", source="arxiv", domain="d", title="T", url="u", score=7,
              published="2026-09-21")
    w.update({"publication_date": "2026-09-21",
              "primary_location": {"source": {"display_name": "arXiv (Cornell University)", "type": "repository"}}})
    enrich([it], 6, get=fake_get({"https://api.openalex.org/works/doi:10.48550/arxiv.2609.21656": w}), pause=0)
    assert venue_line(it) == "〔预印本〕arXiv · 2026-09 · 末位 Gabriele Facciolo" and "pi_inst" not in it.extra


def test_biorxiv_corresponding_author_beats_openalex():
    doi = "10.64898/2026.09.13.751267"
    oa = {"publication_date": "2026-09-14",
          "primary_location": {"source": {"display_name": "bioRxiv (Cold Spring Harbor Laboratory)", "type": "repository"}},
          "authorships": [{"author": {"display_name": "Hani Goodarzi"}, "is_corresponding": True,
                           "institutions": [{"display_name": "Sylvana Research"}]}]}
    it = Item(id=f"doi:{doi}", source="europepmc", domain="d", title="Synthetic atlas", url="u", score=7)
    get = fake_get({f"https://api.openalex.org/works/doi:{doi}": oa,
                    f"https://api.biorxiv.org/details/biorxiv/{doi}":
                        {"collection": [{"author_corresponding": "Hani Goodarzi",
                                         "author_corresponding_institution": "Arc Institute"}]}})
    enrich([it], 6, get=get, pause=0)
    assert venue_line(it) == "〔预印本〕bioRxiv · 2026-09 · 通讯 Hani Goodarzi（Arc Institute）"


def test_epmc_affiliation_only_for_matching_person():
    oa = {"publication_date": "2026-01-05", "primary_location": {"source": {"display_name": "Cell", "type": "journal"}},
          "authorships": [{"author": {"display_name": "Wang Y"}, "is_corresponding": True, "institutions": []}]}
    it = Item(id="doi:10.1016/z", source="europepmc", domain="d", title="T", url="u", score=7,
              extra={"journal": "Cell", "last_author": "Li X", "last_affil": "Peking University, Beijing"})
    enrich([it], 6, get=fake_get({"https://api.openalex.org/works/doi:10.1016/z": oa}), pause=0)
    assert venue_line(it) == "〔期刊〕Cell · 2026-01 · 通讯 Wang Y"  # 末位作者的单位不安到通讯作者头上


# ---- 4. 打分下限与主题 ----

CFG = {"domains": [{"name": "aging_multimodal", "keywords_en": ["aging", "senescence"]},
                   {"name": "cardio_omics", "keywords_en": ["cardiac", "coronary"]}]}


def _scored(title, journal, s, tags, abstract=""):
    return Item(id=f"doi:10.1/{title[:5]}", source="europepmc", domain="aging_multimodal", title=title, url="u",
                abstract=abstract, score=s, extra={"journal": journal, "scored_by": "llm", "themes": tags})


def test_journal_floor_in_code():
    raman = _scored("RamanOmics maps senescence in aging and repair", "Nature Aging", 5.0, ["aging"])
    commun = _scored("Senescence atlas in aging mice", "Nature Communications", 5.0, ["aging"])
    offtopic = _scored("Metagenome taxonomy at scale", "Cell", 5.0, [])
    review = _scored("Aging clocks and senescence: a review", "Nature Medicine", 5.0, ["aging"])
    cardio = _scored("ALKBH5 in cardiac aging", "Circulation", 4.0, ["cardio", "aging"])
    circ_no_cardio = _scored("Aging senescence study", "Circulation", 4.0, ["aging"])
    kw_only = Item(id="x", source="europepmc", domain="d", title="Aging senescence", url="u", score=3.0,
                   extra={"journal": "Nature", "themes": ["aging"]})  # 关键词分，未经 LLM
    items = [raman, commun, offtopic, review, cardio, circ_no_cardio, kw_only]
    assert score.apply_journal_floor(items, CFG) == 2
    assert raman.score == 7.0 and cardio.score == 7.0 and raman.extra["floor"] == "journal 5→7"
    assert commun.score == 5.0 and offtopic.score == 5.0 and review.score == 5.0
    assert circ_no_cardio.score == 4.0 and kw_only.score == 3.0


def test_rerank_prompt_constrains_tags_and_keeps_empty(monkeypatch):
    seen = {}

    def chat(prompt, **kw):
        seen["p"] = prompt
        return json.dumps([{"id": 0, "score": 6, "type": "paper", "tags": [], "reason": "r"}])
    monkeypatch.setattr(radar_llm, "available", lambda: True)
    monkeypatch.setattr(radar_llm, "chat", chat)
    monkeypatch.setattr(score, "load_profile", lambda: "画像")
    it = Item(id="a", source="europepmc", domain="data_models", title="Bulk splicing in pediatric cancer", url="u")
    assert score.llm_rerank([it])
    assert "不等于 singlecell / ssl" in seen["p"] and "给空数组" in seen["p"]
    assert "themes" not in it.extra and summary.item_themes(it) == []  # 不再按 data_models 兜底成 #单细胞


def test_summary_prompt_rules(monkeypatch):
    seen = {}
    monkeypatch.setattr(radar_llm, "available", lambda: True)
    monkeypatch.setattr(radar_llm, "chat", lambda p, **kw: seen.setdefault("p", p) and "- #衰老 x\n- 必读：y")
    out = summary.day_summary([{"title": "t", "score": 7, "reason": "r", "themes": ["#衰老"], "venue": "bioRxiv"}])
    p = seen["p"]
    assert out == ["- #衰老 x", "- 必读：y"]
    assert "每个数字都必须紧跟它所属条目的名字" in p and "不要写「你的 X 方向」" in p
    assert "带关键数字" not in p and "应用线" in p and "类器官多模态健康衰老模型" in p


# ---- 4. 深读 ----

PROFILE = "# x\n\n## 应用线（每条都要覆盖）\n\n1. **类器官多模态健康衰老模型**（合作）\n2. **人群队列 + 多组学 → 临床**（UKB）\n" \
          "3. **类器官 / 模式生物的虚拟扰动响应**\n4. **方法储备**：世界模型\n\n## 打高分\n"


def test_deepread_heading_follows_theme(monkeypatch):
    assert deepread.application_lines(PROFILE)[1] == "人群队列 + 多组学 → 临床"
    cardio = Item(id="a", source="arxiv", domain="cardio_omics", title="T", url="u", extra={"themes": ["cardio"]})
    agent = Item(id="b", source="arxiv", domain="agents", title="T", url="u", extra={"themes": ["agent"]})
    none = Item(id="c", source="arxiv", domain="agents", title="T", url="u")
    assert deepread.inspiration_heading(cardio, PROFILE) == "对「人群队列 + 多组学 → 临床」的启发"
    assert deepread.inspiration_heading(agent, PROFILE) == "对「方法储备」的启发"
    assert deepread.inspiration_heading(none, PROFILE) == "对应用线的启发"
    seen = {}
    monkeypatch.setattr(deepread, "_fulltext", lambda it: ("text", "仅摘要"))
    monkeypatch.setattr(radar_llm, "chat", lambda p, **kw: seen.setdefault("p", p))
    deepread._deepread_one(cardio, PROFILE)
    assert "对多模态衰老模型合作的启发" not in seen["p"] and "**对「人群队列 + 多组学 → 临床」的启发**" in seen["p"]


# ---- 5. 去重与增长 ----

def _it(i, title, published="2026-09-20", url="u"):
    return Item(id=i, source="x", domain="d", title=title, url=url, published=published)


def test_dedup_crosswalk_title_and_age(tmp_path):
    st = tmp_path / "seen.json"
    today = date(2026, 9, 27)
    tpami = _it("doi:10.1109/tpami.2026.1", "Domain Elastic Transform for Robust Registration")
    arx = _it("http://arxiv.org/abs/2603.21235v2", "Domain elastic transform for robust registration!")
    s2 = _it("doi:10.48550/arxiv.2603.21235", "Another title entirely different here")
    old = _it("http://arxiv.org/abs/2406.04814v1", "Lifelong Learning of Video Diffusion Models", published="2024-06-07")
    undated = _it("rss:https://x/1", "Some RSS item without date info", published="")
    out = dedup.filter_new([tpami, arx, s2, old, undated], state_path=st, commit=False, today=today)
    assert [x.id for x in out] == [tpami.id, s2.id, undated.id]  # 标题撞车 / 发表超 90 天被挡
    dedup.mark_seen([s2], state_path=st, today=today)
    rss = _it("https://arxiv.org/abs/2603.21235", "Unrelated wording of the same arxiv paper", url="https://arxiv.org/abs/2603.21235")
    assert dedup.filter_new([rss], state_path=st, commit=False, today=today) == []  # arXiv RSS 写法 ↔ DOI 互认


def test_dedup_old_seen_raw_keys_still_match(tmp_path):
    st = tmp_path / "seen.json"
    st.write_text(json.dumps({"https://arxiv.org/abs/2609.13665": "2026-09-15"}), encoding="utf-8")
    api = _it("http://arxiv.org/abs/2609.13665v1", "A paper title with enough words")
    assert dedup.filter_new([api], state_path=st, commit=False, today=date(2026, 9, 27)) == []


def test_mark_seen_prunes_old_entries(tmp_path):
    st = tmp_path / "seen.json"
    st.write_text(json.dumps({"old": "2026-01-01", "recent": "2026-08-01", "weird": 1}), encoding="utf-8")
    dedup.mark_seen([_it("doi:10.1/new", "Fresh paper about aging clocks")], state_path=st, today=date(2026, 9, 27))
    seen = json.loads(st.read_text(encoding="utf-8"))
    assert "old" not in seen and "recent" in seen and "weird" in seen
    assert seen["doi:10.1/new"] == "2026-09-27" and seen["t:fresh paper about aging clocks"] == "2026-09-27"
