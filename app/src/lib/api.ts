import type { Shift } from "./types";

const AGENT = process.env.AGENT_URL || "http://127.0.0.1:8787";

export async function runDemo(): Promise<Shift> {
  const res = await fetch(`${AGENT}/shifts/demo`, { method: "POST", cache: "no-store" });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export async function getShift(id: string): Promise<Shift> {
  const res = await fetch(`${AGENT}/shifts/${id}`, { cache: "no-store" });
  if (!res.ok) throw new Error("shift not found");
  return res.json();
}

export async function listShifts(): Promise<Shift[]> {
  const res = await fetch(`${AGENT}/shifts`, { cache: "no-store" });
  if (!res.ok) throw new Error("cannot list shifts");
  return res.json();
}

export async function bindCase(id: string, itemId: string, decision: string, note = "") {
  const res = await fetch(`${AGENT}/shifts/${id}/bind`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ item_id: itemId, decision, note }),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json() as Promise<Shift>;
}
