from quietdesk.fixtures import HARBOR_POLICY
from quietdesk.models import CaseFile, ShopPolicy
from quietdesk.policy import decide


def test_reschedule_open_bay_is_auto():
    case = CaseFile(
        item_id="1",
        kind="reschedule",
        summary="move oil",
        requested_slot="2026-08-25 10:30",
        bay="2",
    )
    disposition, _ = decide(case, HARBOR_POLICY)
    assert disposition == "AUTO"


def test_refund_is_always_hold():
    case = CaseFile(item_id="2", kind="refund", summary="give money back", amount_usd=187)
    disposition, _ = decide(case, HARBOR_POLICY)
    assert disposition == "HOLD"


def test_napa_standing_po_under_cap_is_auto():
    case = CaseFile(item_id="3", kind="restock", summary="oil", amount_usd=52, vendor="NAPA")
    disposition, _ = decide(case, HARBOR_POLICY)
    assert disposition == "AUTO"


def test_big_quote_holds():
    case = CaseFile(item_id="4", kind="quote", summary="brakes", amount_usd=420)
    disposition, _ = decide(case, HARBOR_POLICY)
    assert disposition == "HOLD"


def test_unknown_vendor_holds():
    policy = ShopPolicy(name="x", preferred_vendors=["NAPA"], standing_po_vendors=["NAPA"])
    case = CaseFile(item_id="5", kind="restock", summary="x", amount_usd=10, vendor="Acme")
    disposition, _ = decide(case, policy)
    assert disposition == "HOLD"
