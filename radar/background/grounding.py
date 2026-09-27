"""数字回原文校验（不经 LLM）。抽取和编译两处共用。

- numbers(text)：抽出可核对的数字（去千分位，识别 万/亿/k/M/million 等量级）。
  小于 10 的整数不查（"3 句"、"第 2 层"、版本号之类噪声太多）。
- supported(n, pool)：数字 n 能否在来源数字池里找到——同值；或按 n 的小数位四舍五入后相等
  （LLM 常把 0.767 写成 0.77）；带量级单位的约数（"约 50 万"）允许 3% 相对误差。
- cited_only(n, abstract, fulltext)：摘要里没有、全文里每次出现都紧挨引用标记（[12]、et al.、
  "classification 43 ." 这种 Europe PMC 去标签后的上标）——多半是本文引用的别人的结果。
"""
from __future__ import annotations

import re
from dataclasses import dataclass

_UNIT = {"万": 1e4, "亿": 1e8, "千": 1e3, "k": 1e3, "K": 1e3, "M": 1e6, "B": 1e9,
         "thousand": 1e3, "million": 1e6, "billion": 1e9}
_NUM = re.compile(r"(?<![A-Za-z0-9_.])(\d{1,3}(?:,\d{3})+|\d+(?:\.\d+)?)"
                  r"(?:\s*(万|亿|千|thousand|million|billion)|([kKMB])(?![A-Za-z]))?")
# 引用标记：[12] / [ 3, 5–7 ] / Smith et al. / 上标式 "word 43 ." "word 12 , 13 ,"
CITE_MARK = re.compile(r"\[\s*\d{1,3}(?:\s*[,–\-]\s*\d{1,3})*\s*\]|\bet al\b|"
                       r"[A-Za-z)]\s+\d{1,3}(?:\s*[,–\-]\s*\d{1,3})*\s+[.,;](?:\s|$)")
# 报告正文里的引用：[doi:...] 或已编号的 [12]；数字比对前先去掉
REPORT_CITE = re.compile(r"\[(?:(?:doi|arxiv|pmid|eupmc|s2|url):[^\]\s]+|\d{1,4}(?:\s*[,，]\s*\d{1,4})*)\]")


@dataclass(frozen=True)
class Num:
    raw: str        # 原文写法
    value: float    # 乘过量级后的值
    decimals: int   # 原写法的小数位
    scaled: bool    # 带量级单位（约数）


def numbers(text: str) -> list[Num]:
    out = []
    for m in _NUM.finditer(text or ""):
        digits, unit = m.group(1), m.group(2) or m.group(3) or ""
        base = float(digits.replace(",", ""))
        dec = len(digits.split(".", 1)[1]) if "." in digits else 0
        if not unit and dec == 0 and base < 10:
            continue
        out.append(Num(m.group(0).strip(), base * _UNIT.get(unit, 1.0), dec, bool(unit)))
    return out


_SPACED = re.compile(r"(?<![\d.])(\d{1,3})((?:[ \u2009\u202f\u00a0]\d{3})+)(?![\d.])")


def pool(*texts: str) -> list[float]:
    """来源数字池。另把空格千分位（"51 859"，BMJ/Circulation 常见）合并后再收一遍。"""
    vals = []
    for t in texts:
        vals.extend(n.value for n in numbers(t))
        joined = _SPACED.sub(lambda m: m.group(1) + re.sub(r"\D", "", m.group(2)), t or "")
        if joined != (t or ""):
            vals.extend(n.value for n in numbers(joined))
    return vals


def supported(n: Num, values: list[float]) -> bool:
    for v in values:
        if v == n.value:
            return True
        if n.decimals and round(v, n.decimals) == round(n.value, n.decimals):
            return True
        if n.scaled and v and abs(v - n.value) / abs(v) <= 0.03:
            return True
    return False


def _occurrences(n: Num, text: str) -> list[int]:
    return [m.start() for m in _NUM.finditer(text) if _same(n, m)]


def _same(n: Num, m: re.Match) -> bool:
    try:
        v = float(m.group(1).replace(",", "")) * _UNIT.get(m.group(2) or m.group(3) or "", 1.0)
    except ValueError:
        return False
    return v == n.value or (n.decimals and round(v, n.decimals) == round(n.value, n.decimals)) \
        or (n.scaled and v and abs(v - n.value) / abs(v) <= 0.03)


def _sentence_span(text: str, pos: int, reach: int = 250) -> str:
    lo = text.rfind(". ", max(0, pos - reach), pos)
    lo = lo + 2 if lo >= 0 else max(0, pos - reach)
    hi = text.find(". ", pos, pos + reach)
    hi = (hi + 2 + 25) if hi >= 0 else pos + reach  # 句号后紧跟的 "[ 25 ]" 也算本句
    return text[lo:hi]


def cited_only(n: Num, abstract: str, fulltext: str) -> bool:
    """摘要里没有、全文每次出现所在句都有引用标记。全文里一次都没出现不算 cited（另记 not_found）。"""
    if supported(n, pool(abstract)):
        return False
    occ = _occurrences(n, fulltext or "")
    return bool(occ) and all(CITE_MARK.search(_sentence_span(fulltext, p)) for p in occ)


CHECK_FIELDS = ("data", "results", "benchmark", "summary", "limitations")


def audit_extraction(ex: dict, abstract: str, fulltext: str = "") -> list[dict]:
    """逐字段查数字：[{field, number, reason: not_found|cited}]。"""
    values = pool(abstract, fulltext)
    out = []
    for f in CHECK_FIELDS:
        for n in numbers(ex.get(f, "")):
            if cited_only(n, abstract, fulltext):
                out.append({"field": f, "number": n.raw, "reason": "cited"})
            elif not supported(n, values):
                out.append({"field": f, "number": n.raw, "reason": "not_found"})
    return out


_CLAUSE = re.compile(r"(?<=[，,；;。])")


def drop_clauses(text: str, bad: set[str]) -> str:
    """去掉含指定数字写法的分句（按 ，；。 切）。"""
    parts = _CLAUSE.split(text)
    keep = [p for p in parts if not any(n.raw in bad for n in numbers(p))]
    return "".join(keep).strip().rstrip("，,；;")


def strip_citations(text: str) -> str:
    return REPORT_CITE.sub(" ", text)
