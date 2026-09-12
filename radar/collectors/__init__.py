from . import arxiv, europepmc, github, huggingface, rss, semantic_scholar

COLLECTORS = {
    "arxiv": arxiv,
    "europepmc": europepmc,
    "semantic_scholar": semantic_scholar,
    "huggingface": huggingface,
    "github": github,
    "rss": rss,
}
