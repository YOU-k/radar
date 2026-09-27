"""期刊白名单：CNS 正刊与主要子刊 + 心血管顶刊。精确匹配（规范化后整名相等），不做前缀匹配——
旧版 stage._is_cns 用 "nat "/"cell " 前缀，把 Nat Commun、Cell Reports 也算成 CNS。

日报打分的「CNS/子刊 × 方向相关 ⇒ ≥7」下限、背景报告阶段判断的 cns_share 共用这里。"""
from __future__ import annotations

import re

# 规范化后的全名（小写、去标点、& → and、去前导 the）
CNS = {
    "nature", "science", "cell",
    # Nature 子刊（研究型）
    "nature medicine", "nature genetics", "nature methods", "nature biotechnology", "nature aging",
    "nature cell biology", "nature metabolism", "nature cardiovascular research",
    "nature machine intelligence", "nature biomedical engineering", "nature computational science",
    "nature immunology", "nature neuroscience", "nature structural and molecular biology",
    "nature chemical biology", "nature human behaviour", "nature microbiology", "nature cancer",
    "nature ecology and evolution", "nature plants", "nature physics", "nature chemistry",
    "nature materials", "nature electronics",
    # Nature 综述刊
    "nature reviews genetics", "nature reviews cardiology", "nature reviews drug discovery",
    "nature reviews molecular cell biology", "nature reviews immunology", "nature reviews cancer",
    "nature reviews endocrinology", "nature reviews neuroscience",
    # Cell Press 主要刊
    "cell stem cell", "cell metabolism", "cell systems", "cell genomics", "cancer cell", "immunity",
    "molecular cell", "neuron", "developmental cell", "cell host and microbe", "cell reports medicine",
    # Science 子刊
    "science translational medicine", "science immunology", "science robotics",
}

# 顶级综合医学刊 + 心血管顶刊（心血管方向的 ≥7 下限按画像："CNS、Circulation、EHJ、JACC、Nat Cardiovasc Res 级别"）
MEDICAL = {"new england journal of medicine", "lancet", "jama", "bmj"}
CARDIO = {"circulation", "european heart journal", "journal of the american college of cardiology",
          "circulation research", "nature cardiovascular research", "jama cardiology", "lancet"}

# 常见缩写（Europe PMC / NLM ISO 缩写）→ 全名
ABBREV = {
    "nat med": "nature medicine", "nat genet": "nature genetics", "nat methods": "nature methods",
    "nat biotechnol": "nature biotechnology", "nat aging": "nature aging", "nat cell biol": "nature cell biology",
    "nat metab": "nature metabolism", "nat cardiovasc res": "nature cardiovascular research",
    "nat mach intell": "nature machine intelligence", "nat biomed eng": "nature biomedical engineering",
    "nat comput sci": "nature computational science", "nat immunol": "nature immunology",
    "nat neurosci": "nature neuroscience", "nat struct mol biol": "nature structural and molecular biology",
    "nat chem biol": "nature chemical biology", "nat hum behav": "nature human behaviour",
    "nat microbiol": "nature microbiology", "nat cancer": "nature cancer",
    "nat rev genet": "nature reviews genetics", "nat rev cardiol": "nature reviews cardiology",
    "nat rev drug discov": "nature reviews drug discovery",
    "cell stem cell": "cell stem cell", "cell metab": "cell metabolism", "cell syst": "cell systems",
    "cell genom": "cell genomics", "mol cell": "molecular cell", "dev cell": "developmental cell",
    "cell host microbe": "cell host and microbe", "cell rep med": "cell reports medicine",
    "sci transl med": "science translational medicine", "sci immunol": "science immunology",
    "sci robot": "science robotics",
    "n engl j med": "new england journal of medicine", "nejm": "new england journal of medicine",
    "the lancet": "lancet", "eur heart j": "european heart journal",
    "j am coll cardiol": "journal of the american college of cardiology", "jacc": "journal of the american college of cardiology",
    "circ res": "circulation research", "jama cardiol": "jama cardiology",
}


def normalize_venue(venue: str) -> str:
    v = (venue or "").lower().replace("&", " and ")
    v = re.sub(r"\(.*?\)", " ", v)          # "bioRxiv (Cold Spring Harbor Laboratory)"
    v = re.sub(r"[^a-z0-9 ]+", " ", v)
    v = re.sub(r"\s+", " ", v).strip()
    v = re.sub(r"^the ", "", v)
    return ABBREV.get(v, v)


def is_cns(venue: str) -> bool:
    """CNS 正刊或主要子刊（精确匹配）。Nat Commun / Cell Reports / Sci Adv / Sci Rep 不算。"""
    return normalize_venue(venue) in CNS


def is_top(venue: str, cardio: bool = False) -> bool:
    """日报打分下限用：CNS/子刊，或顶级综合医学刊；cardio=True 时再加心血管顶刊。"""
    v = normalize_venue(venue)
    return v in CNS or v in MEDICAL or (cardio and v in CARDIO)
