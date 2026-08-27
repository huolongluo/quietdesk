from __future__ import annotations

import contextvars
from datetime import datetime, timezone

from strands import tool

from . import store
from .models import CaseFile, DecisionLog, MorningBrief
from .policy import decide

CURRENT_SHIFT = contextvars.ContextVar("quietdesk_shift_id")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _shift():
    return store.load(CURRENT_SHIFT.get())


def _save(shift):
    store.save(shift)
    return shift


@tool
def file_case(
    item_id: str,
    kind: str,
    summary: str,
    amount_usd: float | None = None,
    vendor: str | None = None,
    requested_slot: str | None = None,
    current_slot: str | None = None,
    bay: str | None = None,
    sentiment: str = "calm",
    legal_or_warranty: bool = False,
) -> str:
    """Persist a classified inbound item as a case file. Call once per inbox item."""
    shift = _shift()
    existing = next((c for c in shift.cases if c.item_id == item_id), None)
    case = existing or CaseFile(item_id=item_id, kind="other", summary="")
    case.kind = kind  # type: ignore[assignment]
    case.summary = summary
    case.amount_usd = amount_usd
    case.vendor = vendor
    case.requested_slot = requested_slot
    case.current_slot = current_slot
    case.bay = bay
    case.sentiment = sentiment  # type: ignore[assignment]
    case.legal_or_warranty = legal_or_warranty
    if existing is None:
        shift.cases.append(case)
    shift.logs.append(
        DecisionLog(
            at=_now(),
            agent="intake",
            decision=f"FILE:{kind}",
            rationale=summary,
            payload={"item_id": item_id},
        )
    )
    _save(shift)
    return f"filed {item_id} as {kind}"


@tool
def draft_work(
    item_id: str,
    action: str,
    draft: str,
    amount_usd: float | None = None,
    vendor: str | None = None,
) -> str:
    """Attach the clerk's proposed action and customer-facing draft to a case."""
    shift = _shift()
    case = next((c for c in shift.cases if c.item_id == item_id), None)
    if case is None:
        return f"unknown item {item_id}"
    case.action = action
    case.draft = draft
    if amount_usd is not None:
        case.amount_usd = amount_usd
    if vendor:
        case.vendor = vendor
    shift.logs.append(
        DecisionLog(
            at=_now(),
            agent="clerk",
            decision="DRAFT",
            rationale=action,
            payload={"item_id": item_id},
        )
    )
    _save(shift)
    return f"drafted {item_id}"


@tool
def apply_shop_gate() -> str:
    """Run deterministic shop policy over every case. Agents cannot skip this."""
    shift = _shift()
    lines = []
    for case in shift.cases:
        if case.bound:
            continue
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
        lines.append(f"{case.item_id}:{disposition}")
    _save(shift)
    return " ".join(lines) or "no cases"


@tool
def write_morning_brief(
    headline: str,
    auto_handled: list[str],
    waiting_on_owner: list[str],
    risks: list[str],
    first_hour: list[str],
) -> str:
    """Write the 06:30 brief the owner actually reads."""
    shift = _shift()
    shift.brief = MorningBrief(
        headline=headline,
        auto_handled=auto_handled,
        waiting_on_owner=waiting_on_owner,
        risks=risks,
        first_hour=first_hour,
    )
    shift.logs.append(
        DecisionLog(at=_now(), agent="closer", decision="BRIEF", rationale=headline)
    )
    _save(shift)
    return "brief written"
