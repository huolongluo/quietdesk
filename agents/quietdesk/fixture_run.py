from __future__ import annotations

from datetime import datetime, timezone

from . import store
from .models import CaseFile, DecisionLog, MorningBrief, Shift
from .policy import decide
from .tools import CURRENT_SHIFT


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def run_fixture(shift: Shift) -> Shift:
    token = CURRENT_SHIFT.set(shift.id)
    try:
        shift.engine = "fixture"
        shift.graph_order = ["intake", "scout", "clerk", "gate", "closer"]
        shift.status = "running"
        shift.current_agent = "intake"
        shift.cases = [
            CaseFile(
                item_id="msg-1",
                kind="reschedule",
                summary="Maya Chen wants Civic oil change moved 08:30 → 10:30.",
                requested_slot="2026-08-25 10:30",
                current_slot="2026-08-25 08:30",
                bay="2",
            ),
            CaseFile(
                item_id="msg-2",
                kind="quote",
                summary="Jordan Blake: 2019 RAV4 front pads and rotors, squeal only.",
                amount_usd=420,
            ),
            CaseFile(
                item_id="msg-3",
                kind="refund",
                summary="Chris Alvarez demands $187 diagnostic refund after a 90-minute wait.",
                amount_usd=187,
                sentiment="angry",
            ),
            CaseFile(
                item_id="msg-4",
                kind="restock",
                summary="Pacific Parts: Duralast rotors backordered; Wagner WD1855 alt at $64.20.",
                amount_usd=64.20,
                vendor="Wagner",
            ),
            CaseFile(
                item_id="msg-5",
                kind="warranty",
                summary="Priya Nair: WA inspection fail on rusted brake line after last month's brake job.",
                legal_or_warranty=True,
                sentiment="frustrated",
            ),
            CaseFile(
                item_id="msg-6",
                kind="restock",
                summary="Luis: out of 5W-30; NAPA standing PO can drop 4 gallons for $52 before 8am.",
                amount_usd=52,
                vendor="NAPA",
            ),
        ]
        shift.logs.append(
            DecisionLog(at=_now(), agent="intake", decision="FILE:6", rationale="Harbor overnight inbox classified.")
        )

        shift.current_agent = "scout"
        shift.logs.append(
            DecisionLog(
                at=_now(),
                agent="scout",
                decision="PICTURE",
                rationale="8am oil board dies without 5W-30. Bay 2 at 10:30 is free for Maya. Owner binds: refund, warranty, $420 quote, Wagner sub.",
            )
        )

        drafts = {
            "msg-1": (
                "Move Maya Chen Civic oil change 08:30 → 10:30 bay 2",
                "Maya — you're moved to 10:30 tomorrow with Luis in bay 2. Reply if that misses dropoff.",
            ),
            "msg-2": (
                "Draft $420 pads+rotors quote for 2019 RAV4",
                "Jordan — front pads and rotors on the RAV4 are $420 parts and labor. Usually same week. Draft only until the owner sends it.",
            ),
            "msg-3": (
                "Hold $187 diagnostic refund request",
                "Chris — we have the voicemail about the wait and the $187 diagnostic. The owner will call at open. No refund overnight.",
            ),
            "msg-4": (
                "Hold Wagner rotor substitute $64.20 — not on standing PO",
                "Pacific Parts — hold the Wagner WD1855 sub. Owner will confirm at 08:00 whether to wait on Duralast or switch.",
            ),
            "msg-5": (
                "Hold warranty question on brake line vs last month's job",
                "Priya — we have the inspection note. Coverage on a brake line vs a pad/rotor job is an owner call. We'll ring after 8.",
            ),
            "msg-6": (
                "Release NAPA standing PO for 4 gal 5W-30 at $52",
                "NAPA — drop 4 gallons 5W-30 on the Harbor Auto standing PO tonight. $52. Two 8am oil changes on the board.",
            ),
        }
        shift.current_agent = "clerk"
        for case in shift.cases:
            action, draft = drafts[case.item_id]
            case.action = action
            case.draft = draft
            shift.logs.append(
                DecisionLog(
                    at=_now(),
                    agent="clerk",
                    decision="DRAFT",
                    rationale=action,
                    payload={"item_id": case.item_id},
                )
            )

        shift.current_agent = "gate"
        for case in shift.cases:
            disposition, reason = decide(case, shift.policy)
            case.disposition = disposition  # type: ignore[assignment]
            case.gate_reason = reason
            shift.logs.append(
                DecisionLog(
                    at=_now(),
                    agent="gate",
                    decision=disposition,
                    rationale=reason,
                    payload={"item_id": case.item_id},
                )
            )

        shift.current_agent = "closer"
        auto = [c.summary for c in shift.cases if c.disposition == "AUTO"]
        hold = [c.summary for c in shift.cases if c.disposition == "HOLD"]
        shift.brief = MorningBrief(
            headline="Two jobs auto-moved. Four owner binds before the bay doors open.",
            auto_handled=auto,
            waiting_on_owner=hold,
            risks=[
                "Chris Alvarez wants $187 back tonight.",
                "Priya Nair inspection fail may be a comeback.",
            ],
            first_hour=[
                "Call Chris before the waiting room fills.",
                "Decide Wagner sub vs wait on Duralast.",
                "Tell Priya whether the line is on us.",
                "Send or hold the $420 RAV4 quote.",
            ],
        )
        shift.logs.append(DecisionLog(at=_now(), agent="closer", decision="BRIEF", rationale=shift.brief.headline))
        shift.status = "briefed"
        shift.current_agent = None
        shift.closed_at = _now()
        return store.save(shift)
    finally:
        CURRENT_SHIFT.reset(token)


def seed_if_graph_skipped_tools(shift: Shift) -> Shift:
    if shift.cases:
        for case in shift.cases:
            if not case.bound:
                disposition, reason = decide(case, shift.policy)
                case.disposition = disposition  # type: ignore[assignment]
                case.gate_reason = reason
        if shift.brief is None:
            auto = [c.summary for c in shift.cases if c.disposition == "AUTO"]
            hold = [c.summary for c in shift.cases if c.disposition == "HOLD"]
            shift.brief = MorningBrief(
                headline="Overnight desk filed the board. Owner binds remain.",
                auto_handled=auto,
                waiting_on_owner=hold,
                risks=[c.summary for c in shift.cases if c.kind in {"refund", "warranty"} or c.sentiment == "angry"],
                first_hour=["Walk HOLD items in log order."],
            )
        return store.save(shift)
    return run_fixture(shift)
