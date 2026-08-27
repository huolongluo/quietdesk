from quietdesk.fixture_run import run_fixture
from quietdesk.graph import new_harbor_shift


def test_harbor_fixture_binds_only_what_policy_allows():
    shift = run_fixture(new_harbor_shift())
    by_id = {c.item_id: c for c in shift.cases}
    assert by_id["msg-1"].disposition == "AUTO"
    assert by_id["msg-6"].disposition == "AUTO"
    assert by_id["msg-2"].disposition == "HOLD"
    assert by_id["msg-3"].disposition == "HOLD"
    assert by_id["msg-4"].disposition == "HOLD"
    assert by_id["msg-5"].disposition == "HOLD"
    assert shift.brief is not None
    assert shift.status == "briefed"
