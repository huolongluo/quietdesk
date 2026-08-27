from __future__ import annotations

from .models import CaseFile, ShopPolicy


def decide(case: CaseFile, policy: ShopPolicy) -> tuple[str, str]:
    """Hard gate. LLMs may draft; they cannot bind."""
    action = (case.action or "").lower()

    if case.kind == "refund" or "refund" in action:
        return "HOLD", "Refunds never auto-bind. Owner must choose make-good vs refuse."

    if case.legal_or_warranty or case.kind == "warranty":
        return "HOLD", "Warranty and inspection disputes are owner-bound. QuietDesk will not interpret coverage."

    if case.sentiment == "angry":
        return "HOLD", "Angry customer. Do not send a reply until a human reads the draft."

    if case.kind == "quote":
        amount = case.amount_usd or 0
        if amount <= 0:
            return "HOLD", "Quote has no priced line. Clerk must not invent a number the owner has not seen."
        if amount >= policy.quote_hold_above_usd:
            return "HOLD", f"Quote ${amount:.0f} is over the ${policy.quote_hold_above_usd:.0f} auto-send ceiling."
        return "AUTO", f"Quote ${amount:.0f} is under the send ceiling and uses shop book rates."

    if case.kind == "reschedule":
        if not case.requested_slot:
            return "HOLD", "Reschedule request has no concrete slot."
        bay = case.bay or "any"
        open_slots = policy.open_bays.get(bay) or policy.open_bays.get("any") or []
        if case.requested_slot not in open_slots:
            return "HOLD", f"Requested slot {case.requested_slot} is not on the open-bay board."
        return "AUTO", f"Same-day move into an open bay slot ({case.requested_slot}). Confirmation may go out."

    if case.kind == "restock":
        amount = case.amount_usd or 0
        vendor = (case.vendor or "").lower()
        preferred = [v.lower() for v in policy.preferred_vendors]
        standing = [v.lower() for v in policy.standing_po_vendors]
        if amount <= policy.auto_restock_max_usd and vendor in standing:
            return "AUTO", f"Standing PO with {case.vendor}. ${amount:.0f} is under the ${policy.auto_restock_max_usd:.0f} night cap."
        if vendor not in preferred:
            return "HOLD", f"Vendor {case.vendor or 'unknown'} is not on the preferred list."
        return "HOLD", f"Restock ${amount:.0f} needs a human because it is not on a standing PO under the night cap."

    if case.kind == "complaint":
        return "HOLD", "Complaints wait for the owner. Draft only."

    return "HOLD", "Unclassified work stays on the morning board."
