from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

AgentName = Literal["intake", "scout", "clerk", "gate", "closer"]
ItemKind = Literal["reschedule", "quote", "refund", "restock", "warranty", "complaint", "other"]
Disposition = Literal["AUTO", "HOLD", "REJECT"]
ShiftStatus = Literal["queued", "running", "briefed", "closed", "error"]
Sentiment = Literal["calm", "frustrated", "angry"]


class ShopPolicy(BaseModel):
    name: str
    timezone: str = "America/Los_Angeles"
    auto_reschedule_max_hours: float = 2.0
    auto_restock_max_usd: float = 80.0
    quote_hold_above_usd: float = 150.0
    preferred_vendors: list[str] = Field(default_factory=list)
    standing_po_vendors: list[str] = Field(default_factory=list)
    open_bays: dict[str, list[str]] = Field(default_factory=dict)


class InboundItem(BaseModel):
    id: str
    at: str
    channel: str
    from_name: str
    from_role: str = "customer"
    body: str


class CaseFile(BaseModel):
    item_id: str
    kind: ItemKind
    summary: str
    amount_usd: float | None = None
    vendor: str | None = None
    requested_slot: str | None = None
    current_slot: str | None = None
    bay: str | None = None
    sentiment: Sentiment = "calm"
    legal_or_warranty: bool = False
    draft: str = ""
    action: str = ""
    disposition: Disposition = "HOLD"
    gate_reason: str = ""
    bound: bool = False
    bind_decision: str | None = None
    bind_note: str | None = None


class DecisionLog(BaseModel):
    at: str
    agent: AgentName
    decision: str
    rationale: str
    payload: dict[str, Any] = Field(default_factory=dict)


class MorningBrief(BaseModel):
    headline: str
    auto_handled: list[str] = Field(default_factory=list)
    waiting_on_owner: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    first_hour: list[str] = Field(default_factory=list)


class Shift(BaseModel):
    id: str
    shop: str
    status: ShiftStatus = "queued"
    engine: str = "strands-graph"
    created_at: str
    closed_at: str | None = None
    policy: ShopPolicy
    inbox: list[InboundItem]
    cases: list[CaseFile] = Field(default_factory=list)
    logs: list[DecisionLog] = Field(default_factory=list)
    brief: MorningBrief | None = None
    error: str | None = None
    current_agent: AgentName | None = None
    graph_order: list[str] = Field(default_factory=list)
