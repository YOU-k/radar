from radar.pipeline import score
from radar.pipeline.enrich import doi_of, enrich, short_inst, venue_line, venue_stats
from radar.schema import Item

OA_PREPRINT = {"publication_date": "2026-09-23",
               "primary_location": {"source": {"display_name": "bioRxiv (Cold Spring Harbor Laboratory)", "type": "repository"}},
               "authorships": [{"author": {"display_name": "A First"}, "institutions": []},
                               {"author": {"display_name": "Xin Gao"}, "is_corresponding": True,
                                "institutions": [{"display_name": "KAUST"}]}]}
OA_JOURNAL = {"publication_date": "2026-09-22",
              "primary_location": {"source": {"display_name": "Nature Medicine", "type": "journal"}},
              "authorships": [{"author": {"display_name": "A"}, "institutions": [{"display_name": "Uni A"}]},
                              {"author": {"display_name": "Last B"}, "institutions": [{"display_name": "Sichuan Cancer Hospital"}]}]}


def fake_get(table):
    def get(url, params=None, timeout=30):
        return table.get(url)
    return get


def test_preprint_gets_server_month_and_corresponding_pi():
    it = Item(id="doi:10.64898/2026.09.22.752128", source="europepmc", domain="d", title="T", url="u",
              published="2026-09-23", score=7, extra={"epmc_src": "PPR", "preprint_server": "bioRxiv"})
    enrich([it], 6, get=fake_get({"https://api.openalex.org/works/doi:10.64898/2026.09.22.752128": OA_PREPRINT}), pause=0)
    assert venue_line(it) == "〔预印本〕bioRxiv · 2026-09 · 通讯 Xin Gao（KAUST）"


def test_journal_uses_openalex_venue_and_last_author():
    it = Item(id="doi:10.1038/x", source="europepmc", domain="d", title="T", url="u", score=7,
              extra={"journal": "Nature medicine"})
    enrich([it], 6, get=fake_get({"https://api.openalex.org/works/doi:10.1038/x": OA_JOURNAL}), pause=0)
    assert venue_line(it) == "〔期刊〕Nature Medicine · 2026-09 · 末位 Last B（Sichuan Cancer Hospital）"


def test_biorxiv_fallback_and_epmc_affiliation_fallback():
    it = Item(id="doi:10.1101/2024.1", source="europepmc", domain="d", title="T", url="u", score=7, published="2024-02-20")
    get = fake_get({"https://api.biorxiv.org/details/biorxiv/10.1101/2024.1":
                    {"collection": [{"author_corresponding": "Jane Doe", "author_corresponding_institution": "Broad"}]}})
    enrich([it], 6, get=get, pause=0)
    assert venue_line(it) == "〔预印本〕bioRxiv/medRxiv · 2024-02 · 通讯 Jane Doe（Broad）"
    it2 = Item(id="doi:10.1016/y", source="europepmc", domain="d", title="T", url="u", score=7, published="2026-01-05",
               extra={"journal": "Cell", "last_author": "Li X",
                      "last_affil": "Department of X, Peking University, Beijing, China. lx@pku.edu.cn"})
    enrich([it2], 6, get=fake_get({}), pause=0)
    assert venue_line(it2) == "〔期刊〕Cell · 2026-01 · 末位 Li X（Peking University）"


def test_skips_low_score_and_non_papers():
    lo = Item(id="doi:10.1/a", source="europepmc", domain="d", title="T", url="u", score=3)
    gh = Item(id="gh:x", source="github", domain="d", title="T", url="u", score=9)
    assert enrich([lo, gh], 6, get=fake_get({}), pause=0) == 0 and "venue_type" not in gh.extra


def test_doi_of_arxiv_and_short_inst():
    assert doi_of(Item(id="http://arxiv.org/abs/2506.09985v2", source="arxiv", domain="d", title="", url="")) == "10.48550/arxiv.2506.09985"
    assert short_inst("Dept A, Fuwai Hospital, Chinese Academy of Medical Sciences, Beijing") == "Chinese Academy of Medical Sciences"


def test_venue_stats_counts_digest_lines():
    md = ("- **[a](u)** `7.0`\n  <sub>〔期刊〕Nature Medicine · 2026-09 · 末位 X · A</sub>\n"
          "- **[b](u)** `7.0`\n  <sub>〔预印本〕bioRxiv · 2026-09 · 通讯 Y（Z） · B</sub>\n"
          "- **[c](u)** `7.0`\n  <sub>〔期刊〕Nature Medicine · 2026-09 · C</sub>\n")
    out = venue_stats([md])
    assert "期刊 2 篇 · 预印本 1 篇" in out and "| Nature Medicine | 期刊 | 2 |" in out
    assert venue_stats(["no meta"]) == ""


def test_prefilter_keeps_small_domain_floor():
    items = [Item(id=f"a{i}", source="x", domain="big", title="aging clock", url="u") for i in range(80)]
    items += [Item(id=f"b{i}", source="x", domain="small", title="organoid", url="u") for i in range(3)]
    cfg = {"domains": [{"name": "big", "keywords_en": ["aging clock"]}, {"name": "small", "keywords_en": []}]}
    out = score.prefilter(items, cfg)
    assert len(out) == score.PREFILTER_TOP and sum(it.domain == "small" for it in out) == 3
