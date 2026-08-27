export type CaseFile = {
  item_id: string;
  kind: string;
  summary: string;
  amount_usd: number | null;
  vendor: string | null;
  requested_slot: string | null;
  current_slot: string | null;
  bay: string | null;
  sentiment: string;
  legal_or_warranty: boolean;
  draft: string;
  action: string;
  disposition: "AUTO" | "HOLD" | "REJECT";
  gate_reason: string;
  bound: boolean;
  bind_decision: string | null;
  bind_note: string | null;
};

export type InboundItem = {
  id: string;
  at: string;
  channel: string;
  from_name: string;
  from_role: string;
  body: string;
};

export type DecisionLog = {
  at: string;
  agent: string;
  decision: string;
  rationale: string;
};

export type MorningBrief = {
  headline: string;
  auto_handled: string[];
  waiting_on_owner: string[];
  risks: string[];
  first_hour: string[];
};

export type Shift = {
  id: string;
  shop: string;
  status: string;
  engine: string;
  created_at: string;
  closed_at: string | null;
  inbox: InboundItem[];
  cases: CaseFile[];
  logs: DecisionLog[];
  brief: MorningBrief | null;
  error: string | null;
  current_agent: string | null;
  graph_order: string[];
  policy: { name: string };
};
