"""联网冒烟测试：默认跳过，RADAR_LIVE=1 时跑。只验证真实 API 契约没变。"""
import os

import pytest

from radar.background import discover as d
from radar.background.models import DiscoveryPlan

live = pytest.mark.skipif(not os.environ.get("RADAR_LIVE"), reason="set RADAR_LIVE=1")


@live
def test_eupmc_live(spec):
    out = d.EuropePMCKeyword(per_query=5).fetch(spec, DiscoveryPlan(queries=["UK Biobank proteomics"], months=12))
    assert out and out[0].id.startswith(("doi:", "eupmc:")) and out[0].citations is not None


@live
def test_s2_live(spec):
    out = d.S2Snowball(per_seed=5).fetch(spec, DiscoveryPlan(snowball_ids=["doi:10.1038/s41586-025-09529-3"]))
    assert out and any("Delphi" in c.title or c.citations is not None for c in out)


@live
def test_journal_retro_live(spec):
    out = d.EuropePMCJournal(page_size=20).fetch(spec, DiscoveryPlan(journals=["Nature"], months=12))
    assert isinstance(out, list)
