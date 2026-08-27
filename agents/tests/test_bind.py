from quietdesk.fixture_run import run_fixture
from quietdesk.graph import new_harbor_shift
from quietdesk.runner import bind_case


def test_owner_can_bind_hold_but_not_auto():
    shift = run_fixture(new_harbor_shift())
    auto = next(c for c in shift.cases if c.disposition == "AUTO")
    hold = next(c for c in shift.cases if c.item_id == "msg-3")
    bound = bind_case(shift.id, hold.item_id, "refuse", "call at open")
    case = next(c for c in bound.cases if c.item_id == "msg-3")
    assert case.bound is True
    assert case.bind_decision == "refuse"
    try:
        bind_case(shift.id, auto.item_id, "refuse")
        raise AssertionError("AUTO should already be bound by policy")
    except ValueError:
        pass
