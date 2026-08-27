from __future__ import annotations

from datetime import datetime, timezone

from . import store
from .graph import new_harbor_shift, run_shift
from .models import DecisionLog, Shift
from .policy import decide


def bind_case(shift_id: str, item_id: str, decision: str, note: str = "") -> Shift:
    shift = store.load(shift_id)
    case = next((c for c in shift.cases if c.item_id == item_id), None)
    if case is None:
        raise KeyError(item_id)
    if case.disposition == "AUTO":
        raise ValueError("AUTO items are already bound by policy")
    case.bound = True
    case.bind_decision = decision
    case.bind_note = note
    shift.logs.append(
        DecisionLog(
            at=datetime.now(timezone.utc).isoformat(),
            agent="gate",
            decision=f"OWNER_{decision.upper()}",
            rationale=note or "Owner bind from the morning board",
            payload={"item_id": item_id},
        )
    )
    if all(c.disposition == "AUTO" or c.bound for c in shift.cases):
        shift.status = "closed"
    return store.save(shift)


def reapply_gate(shift: Shift) -> Shift:
    for case in shift.cases:
        if case.bound:
            continue
        disposition, reason = decide(case, shift.policy)
        case.disposition = disposition  # type: ignore[assignment]
        case.gate_reason = reason
    return store.save(shift)


def start_demo() -> Shift:
    return run_shift(new_harbor_shift())
