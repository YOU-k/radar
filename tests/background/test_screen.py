from radar.background.screen import decide, screen
from radar.background.models import Vote
from tests.background.conftest import FakeLLM


def test_decide_rules():
    yy = [Vote("bio", "yes"), Vote("media", "yes")]
    yn = [Vote("bio", "yes"), Vote("media", "no")]
    nn = [Vote("bio", "no"), Vote("media", "no")]
    assert decide(yy) == (True, False)
    assert decide(yn) == (False, True)
    assert decide(nn) == (False, False)
    assert decide([]) == (False, False)
    assert decide(yn, rule="majority") == (False, True)
    assert decide(yy + [Vote("x", "no")], rule="majority") == (True, False)


def test_unanimous_required(spec, cands):
    llm = FakeLLM()  # 偶数 yes 奇数 no，两角色一致
    ds = screen(cands, spec, llm, round_no=1, discuss=False)
    assert [d.accepted for d in ds] == [True, False] * 3
    assert all(len(d.votes) == 2 for d in ds) and all(d.round == 1 for d in ds)


def test_split_vote_triggers_discussion_and_can_flip(spec, cands):
    # 文献 0：bio yes, media no → 分歧；第二轮 media 被说服改 yes
    llm = FakeLLM(votes={"media": {0: "no"}}, revise_to={"media": {0: "yes"}})
    ds = screen(cands[:2], spec, llm, round_no=1)
    assert ds[0].accepted is True
    media = next(v for v in ds[0].votes if v.role == "media")
    assert media.revised is True and media.yes
    tasks = [t for t, _ in llm.calls]
    assert tasks.count("screen") == 4  # 两角色首轮 + 两角色讨论轮


def test_no_discussion_when_agree(spec, cands):
    llm = FakeLLM()
    screen(cands[:2], spec, llm, round_no=1)
    assert [t for t, _ in llm.calls].count("screen") == 2


def test_missing_vote_counts_as_no(spec, cands):
    llm = FakeLLM(fail_tasks={"screen"})
    ds = screen(cands[:1], spec, llm, discuss=False)
    assert ds[0].accepted is False and {v.reason for v in ds[0].votes} == {"未返回投票"}


def test_borderline_recorded(spec, cands):
    llm = FakeLLM(votes={"media": {0: "no"}}, revise_to={"media": {0: "no"}})
    ds = screen(cands[:1], spec, llm)
    assert ds[0].accepted is False and ds[0].borderline is True
