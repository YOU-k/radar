"""第二批（内容质量）：抽取回原文、编译时数字核验、阶段判断去检索统计、试验状态表、重抽取命令。"""
import json
from argparse import Namespace

from radar.background import extract as ex
from radar.background import grounding as g
from radar.background import trials
from radar.background.compile import check_claims, compile_report, dedupe_paragraphs
from radar.background.joint import joint_report, topic_digest, verified_sentences
from radar.background.models import Evidence, Vote
from radar.background.outline import Outline
from radar.background.principles import principles_report
from radar.background.stage import _is_cns, enforce_min_citations
from radar.background.store import EvidenceStore
from tests.background.conftest import FakeLLM, make_cand

CKB_ABS = ("Participants from the China Kadoorie Biobank were divided into training (n = 28,490) and testing sets "
           "(n = 72,150). The HR per standard deviation of the optimal PRS was 1.26 (95% CI:1.19-1.33). "
           "Harrell's C increased by 0.001 in women and 0.003 in men; the best NRI was 3.2%.")
CKB_FT = ("Introduction Polygenic scores were studied in East Asian populations. Adding a PRS to China-PAR improved "
          "Harrell's C by 0.01 and NRI of 3.5%. [ 25 ] Other work used UK Biobank. " + "Methods text. " * 500 +
          " Results In the testing set, 1214 hard and 7201 soft CAD cases were documented during 11.2 years. "
          "The HR was 1.26 for hard CAD. " + "More results 0.003. " * 20 + " Discussion We found small gains.")


class ExtractLLM(FakeLLM):
    """extract 任务返回指定字段（模拟把引用数字当成本文结果的 LLM）。"""

    def __init__(self, row: dict):
        super().__init__()
        self.row = row

    def chat(self, prompt, *, task="", temperature=0.2, timeout=180):
        from radar.background.llmio import task_of
        if (task or task_of(prompt)) == "extract":
            self.calls.append(("extract", prompt))
            from tests.background.conftest import _payload
            return json.dumps([{"id": r["id"], **self.row} for r in _payload(prompt)])
        return super().chat(prompt, task=task, temperature=temperature, timeout=timeout)


BAD_ROW = {"method": "PRS", "data": "CKB约10万例", "scenario": "CAD", "benchmark": "China-PAR",
           "results": "HR 1.26，参考东亚研究C指数提升约0.01、NRI 3.5%",
           "summary": "评估 PRS。样本 99,999 人。增益很小。", "availability": "", "limitations": ""}


# ---- grounding ----

def test_numbers_units_and_separators():
    vals = [n.value for n in g.numbers("约10万例；UKB 400k；25.6M；283,540 人；3 句；C 0.77")]
    assert vals == [1e5, 4e5, 25.6e6, 283540.0, 0.77]  # 小于 10 的整数不查
    assert g.supported(g.numbers("0.77")[0], g.pool("C 0.767"))          # LLM 四舍五入
    assert g.supported(g.numbers("约28万")[0], g.pool("283,540"))          # 约数 3% 容差
    assert g.supported(g.numbers("51,859")[0], g.pool("Among 51 859 UK Biobank"))  # 空格千分位
    assert not g.supported(g.numbers("0.01")[0], g.pool("0.001 and 0.003"))


def test_cited_only_detects_numbers_next_to_citation():
    n35 = g.numbers("3.5%")[0]
    assert g.cited_only(n35, CKB_ABS, CKB_FT)
    assert not g.cited_only(g.numbers("1.26")[0], CKB_ABS, CKB_FT)  # 摘要里有


def test_results_slice_prefers_results_section():
    s = ex.results_slice(CKB_FT, limit=400)
    assert s.startswith("In the testing set") and "[ 25 ]" not in s
    assert ex.results_slice("short text") == "short text"
    nohead = ("Intro cites [ 1 ] a lot [ 2 ] here [ 3 ]. " * 60) + ("We observed 0.81, 0.77 and 12,345 cells. " * 40)
    assert "0.81" in ex.results_slice(nohead, limit=1500) and "[ 1 ]" not in ex.results_slice(nohead, limit=1500)


# ---- 1. 抽取 ----

def test_extract_sends_abstract_and_results_and_grounds_numbers(spec):
    c = make_cand(1, abstract=CKB_ABS)
    llm = ExtractLLM(BAD_ROW)
    out = ex.extract([c], spec, llm, fulltexts={c.id: CKB_FT})[0]
    prompt = llm.calls[0][1]
    assert "28,490" in prompt and "In the testing set" in prompt and "Methods text. Methods text. Methods" not in prompt
    assert "只抽取本文自身的结果；引用他人研究的数字不得写入" in prompt
    assert "3.5" not in out["results"] and "HR 1.26" in out["results"]  # 引用他人数字所在分句被删
    flags = {(x["number"], x["reason"]) for x in out["_unverified_numbers"]}
    assert ("3.5", "cited") in flags and ("99,999", "not_found") in flags
    assert ("10万", "not_found") in flags  # 原文只有 28,490 / 72,150，"约10万" 是 LLM 自己加总的
    assert out["_basis"] == "abstract+results"


def test_extract_abstract_only_basis(spec):
    c = make_cand(2, abstract=CKB_ABS)
    out = ex.extract([c], spec, ExtractLLM({**BAD_ROW, "results": "HR 1.26", "summary": "s", "data": "CKB"}))[0]
    assert out["_basis"] == "abstract" and out["_unverified_numbers"] == []


# ---- 2. 编译时数字核验 ----

def _ev(i, abstract, extraction):
    return Evidence(candidate=make_cand(i, abstract=abstract), panel=[Vote("bio", "yes")], extraction=extraction)


def test_check_claims_drops_unsupported_sentences():
    a = _ev(1, CKB_ABS, {"results": "HR 1.26", "_unverified_numbers": [{"number": "99,999", "reason": "not_found"}],
                         "data": "99,999 人"})
    b = _ev(2, "Spurious rewards improved MATH by 21.4 points.", {})
    by_id = {a.id: a, b.id: b}
    text = (f"PRS 的 HR 为 **1.26** [{a.id}]。C 指数提升约 0.01 [{a.id}]。样本 99,999 人 [{a.id}]。\n"
            f"- 伪奖励提升 21.4 [{a.id}]。\n"
            f"两者合看：1.26 与 21.4 [{a.id}][{b.id}]。2023 年以来 [{a.id}] 多项工作。无引用的 42.0 保留。\n"
            f"幻觉 0.55 [doi:10.9/none]。\n| 表 | 0.99 [{a.id}] |")
    kept, dropped = check_claims(text, by_id)
    assert "1.26** [" in kept and "0.01" not in kept and "99,999" not in kept   # 抽取时标为找不到的数字不算有据
    assert "伪奖励提升 21.4" not in kept                                         # 换错引用（RLVR [13]→[91]）被删
    assert "两者合看" in kept and "2023 年以来" in kept and "42.0 保留" in kept
    assert "0.55" not in kept and "| 表 | 0.99" in kept                         # 未知 id 带数字删；表格行不动
    assert len(dropped) == 4 and "- 伪奖励" not in kept


def test_dedupe_paragraphs_across_sections():
    para = "这是一段足够长的重复段落，背景节常把后面方法节的整段原样抄过来，装配时应当只保留第一次出现。"
    parts = [f"## 1 背景\n\n{para}\n\n短句", f"## 2 方法\n\n{para}\n\n短句\n\n另一段不同的内容也足够长足够长足够长足够长足够长足够长足够长。"]
    out = "\n".join(dedupe_paragraphs(parts))
    assert out.count(para) == 1 and out.count("短句") == 2 and "## 2 方法" in out


class NumberLLM(FakeLLM):
    """section 写一句有据、一句无据的数字句。"""

    def chat(self, prompt, *, task="", temperature=0.2, timeout=180):
        from radar.background.llmio import task_of
        t = task or task_of(prompt)
        if t == "compile" and "TL;DR" not in prompt and "综合节" not in prompt:
            self.calls.append((t, prompt))
            import re
            ids = re.findall(r'"id": "(doi:[^"]+)"', prompt)
            return f"HR 为 1.26 [{ids[0]}]。C 提升 0.01 [{ids[0]}]。\n"
        return super().chat(prompt, task=task, temperature=temperature, timeout=timeout)


def test_compile_report_applies_claim_check_and_passes_abstract(spec):
    e = _ev(1, CKB_ABS, {"summary": "s", "results": "HR 1.26"})
    o = Outline.from_spec(spec); o.attach("2.1", [e.id])
    llm = NumberLLM()
    rep = compile_report(spec, o, [e], llm, 0.5, 1)
    sec_prompt = next(p for t, p in llm.calls if t == "compile" and "生成式疾病轨迹模型" in p)
    assert "28,490" in sec_prompt and "_unverified" not in sec_prompt       # 摘要（截短）喂给节写作
    assert "HR 为 1.26 [1]" in rep and "0.01" not in rep and "数字核验删句 1" in rep
    log = json.loads((spec.dir / "claim_check.json").read_text(encoding="utf-8"))
    assert log["dropped"][0]["sentence"].startswith("C 提升 0.01")


# ---- 3. 阶段判断 / 联合 / 全局 ----

def test_is_cns_exact_whitelist():
    assert _is_cns("Nature") and _is_cns("Nature Genetics") and _is_cns("Nat Med") and _is_cns("Cell Stem Cell")
    assert _is_cns("Science Translational Medicine") and _is_cns("Nature medicine")
    for v in ("Nature Communications", "Nat Commun", "Cell Reports", "Scientific Reports", "Science Advances",
              "Cell Research", "Nature Reviews Something Else", ""):
        assert not _is_cns(v), v


def test_enforce_min_citations():
    md = ("| 细分 | 阶段 | 依据 |\n|---|---|---|\n| A | **朝阳** | x [doi:1/a][doi:1/b] |\n"
          "| B | 成熟 | 只一篇 [doi:1/a] |\n| C | 证据不足 | 无 |")
    out = enforce_min_citations(md)
    rows = out.split("\n")
    assert "**朝阳**" in rows[2] and "证据不足" in rows[3] and "引用少于 2 篇" in rows[3] and rows[4] == "| C | 证据不足 | 无 |"


def test_trial_table_loaded_and_corrected():
    d = trials.load()
    names = {t["name"]: t for t in d["trials"]}
    for n in ("Lp(a)HORIZON", "ZEUS", "VESALIUS-CV", "OCEANIC-STROKE", "PREVAIL", "OCEAN(a)-Outcomes"):
        assert n in names and names[n]["source"].startswith("https://") and names[n]["date"]
    assert "2028-03-31" in names["OCEAN(a)-Outcomes"]["date"] and "失败" in names["ZEUS"]["status"]
    block = trials.prompt_block()
    assert "| ZEUS |" in block and "待核实" in block


def _write_topic(spec, evs, tldr_lines):
    st = EvidenceStore(spec.evidence_dir, spec.rejected_path)
    for e in evs:
        st.add(e)
    refs = "\n".join(f"{n}. {e.candidate.title}. Nature 2026. {e.candidate.url}" for n, e in enumerate(evs, 1))
    spec.report_path.write_text("# r\n\n## 摘要（TL;DR）\n\n" + "\n".join(tldr_lines) +
                                "\n\n## 阶段判断与行动建议\n\n| 2.1 | 朝阳 | 雷达样本 n=3 [1][2] |\n\n## 参考文献\n\n" + refs + "\n",
                                encoding="utf-8")


def test_joint_and_principles_take_only_verified_tldr_and_trials(spec):
    a = _ev(1, CKB_ABS, {"summary": "s"})
    b = _ev(2, "We found 21.4 point gains.", {"summary": "s"})
    _write_topic(spec, [a, b], ["- PRS HR **1.26** [1]。", "- C 提升 0.01、NRI 3.5% [1]。", "- 伪奖励 +21.4 [1]。",
                                "- 伪奖励 +21.4 [2]。", "- 没有数字的判断 [1][2]。"])
    rep = spec.report_path.read_text(encoding="utf-8")
    assert verified_sentences("- a 0.01 [7]。", rep, [a, b]) == ""  # 编号对不上参考文献的数字句不用
    d = topic_digest(spec)
    assert "1.26** [1]" in d["tldr"] and "0.01" not in d["tldr"] and "+21.4 [2]" in d["tldr"]
    assert "+21.4 [1]" not in d["tldr"] and "没有数字的判断 [1][2]" in d["tldr"]
    assert "coverage" not in d and d["stage"].startswith("（以下阶段判断的依据含雷达检索统计，非领域属性")
    llm = FakeLLM()
    joint_report([spec], llm)
    jp = next(p for t, p in llm.calls if t == "joint")
    assert "| ZEUS |" in jp and "雷达检索统计，非领域属性" in jp and "3.5%" not in jp
    llm2 = FakeLLM()
    principles_report([spec], llm2)
    view, synth = [p for t, p in llm2.calls if t == "principles"]
    assert "| OCEAN(a)-Outcomes |" in view and "试验规则" in view and "| ZEUS |" in synth
    assert "已通过数字核验" in view and "0.01、NRI" not in view


# ---- 6. 重抽取 ----

def test_reextract_only_flagged_updates_json_without_compiling(spec):
    st = EvidenceStore(spec.evidence_dir, spec.rejected_path)
    good = _ev(1, CKB_ABS, {"summary": "old good", "results": "HR 1.26"})
    bad = _ev(2, CKB_ABS, {"summary": "old bad", "results": "C 提升 0.01、NRI 3.5%"})
    bad.sections = ["2.1"]
    st.add(good); st.add(bad)
    assert ex.needs_reextract(bad) and not ex.needs_reextract(good)
    llm = ExtractLLM({**BAD_ROW, "results": "HR 1.26", "summary": "new", "data": "CKB 72,150 人"})
    res = ex.reextract(spec, st, llm, only_flagged=True, fulltext_of=lambda eid: "")
    assert res == {"checked": 2, "todo": 1, "updated": 1, "still_flagged": 0}
    assert st.get(bad.id).extraction["summary"] == "new" and st.get(bad.id).sections == ["2.1"]
    assert st.get(good.id).extraction["summary"] == "old good"
    assert {t for t, _ in llm.calls} == {"extract"} and not spec.report_path.exists()  # 不编译


def test_reextract_keeps_old_on_llm_failure(spec):
    st = EvidenceStore(spec.evidence_dir, spec.rejected_path)
    bad = _ev(2, CKB_ABS, {"summary": "old bad", "results": "NRI 3.5%"})
    st.add(bad)
    res = ex.reextract(spec, st, FakeLLM(fail_tasks={"extract"}), only_flagged=False, fulltext_of=lambda eid: "")
    assert res["updated"] == 0 and st.get(bad.id).extraction["summary"] == "old bad"


def test_cli_reextract_dispatch(spec, monkeypatch):
    from radar import run
    st = EvidenceStore(spec.evidence_dir, spec.rejected_path)
    st.add(_ev(2, CKB_ABS, {"summary": "old", "results": "NRI 3.5%"}))
    monkeypatch.setattr("radar.background.spec.load_spec", lambda slug: spec)
    seen = {}
    real = ex.reextract

    def spy(sp, store, llm, only_flagged=True, fulltext_of=None):
        seen["only_flagged"] = only_flagged
        return real(sp, store, llm, only_flagged, fulltext_of=lambda eid: "")
    monkeypatch.setattr(ex, "reextract", spy)
    args = Namespace(action="reextract", topic=spec.slug, only_flagged=True, no_fulltext=False)
    run._background_one(args, spec.slug, ExtractLLM({**BAD_ROW, "summary": "new", "results": "HR 1.26"}))
    assert seen == {"only_flagged": True} and st.all()[0].extraction["summary"] == "new"
