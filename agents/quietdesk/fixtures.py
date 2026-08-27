from __future__ import annotations

from .models import InboundItem, ShopPolicy

HARBOR_POLICY = ShopPolicy(
    name="Harbor Auto",
    timezone="America/Los_Angeles",
    auto_reschedule_max_hours=2.0,
    auto_restock_max_usd=80.0,
    quote_hold_above_usd=150.0,
    preferred_vendors=["NAPA", "Pacific Parts", "Wagner"],
    standing_po_vendors=["NAPA"],
    open_bays={
        "2": ["2026-08-25 10:30", "2026-08-25 14:00"],
        "1": ["2026-08-25 15:30"],
        "any": ["2026-08-25 10:30", "2026-08-25 14:00", "2026-08-25 15:30"],
    },
)

HARBOR_INBOX: list[InboundItem] = [
    InboundItem(
        id="msg-1",
        at="2026-08-24T18:14:00-07:00",
        channel="SMS",
        from_name="Maya Chen",
        body="Hi — can we move my oil change from 8:30 tomorrow to 10:30? School dropoff ran long. 2018 Civic, bay with Luis last time.",
    ),
    InboundItem(
        id="msg-2",
        at="2026-08-24T19:02:00-07:00",
        channel="email",
        from_name="Jordan Blake",
        body="Need a quote to replace front pads and rotors on a 2019 RAV4. How soon can you do it this week? No grinding yet, just a squeal.",
    ),
    InboundItem(
        id="msg-3",
        at="2026-08-24T20:41:00-07:00",
        channel="voicemail",
        from_name="Chris Alvarez",
        body="Yeah this is Chris. I waited ninety minutes for a diagnostic you already charged me $187 for. I'm done. I want that money back tonight.",
    ),
    InboundItem(
        id="msg-4",
        at="2026-08-24T21:15:00-07:00",
        channel="email",
        from_name="Pacific Parts",
        from_role="vendor",
        body="Duralast rotors SKU DL-R4488 backordered 9 days. Alternate: Wagner WD1855 in stock, $64.20/pair. Please advise if we should sub.",
    ),
    InboundItem(
        id="msg-5",
        at="2026-08-24T22:03:00-07:00",
        channel="web",
        from_name="Priya Nair",
        body="Car failed WA inspection for a rusted brake line. You did the brakes last month. Is that covered or am I paying twice?",
    ),
    InboundItem(
        id="msg-6",
        at="2026-08-24T23:22:00-07:00",
        channel="SMS",
        from_name="Luis Ortega",
        from_role="tech",
        body="We're out of 5W-30 bulk. Two oil changes on the board at 8am. NAPA can drop 4 gallons tonight on the standing PO, $52.",
    ),
]


def harbor_story() -> str:
    return (
        "Harbor Auto in Tacoma is closed 18:00–08:00. Six inbound items arrived after hours. "
        "Run the overnight desk: classify, draft, restock, reschedule. Bind nothing irreversible. "
        "Open bay 2 at 10:30 and 14:00. Standing PO: NAPA. "
        "Book rate for front pads+rotors on a RAV4 is $420 parts and labor."
    )
