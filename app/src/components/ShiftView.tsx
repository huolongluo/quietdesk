"use client";

import { useState } from "react";
import type { CaseFile, Shift } from "@/lib/types";

export function ShiftView({ initial }: { initial: Shift }) {
  const [shift, setShift] = useState(initial);
  const [note, setNote] = useState("");
  const [error, setError] = useState("");

  async function bind(itemId: string, decision: string) {
    setError("");
    const res = await fetch(`/agent/shifts/${shift.id}/bind`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ item_id: itemId, decision, note }),
    });
    const data = await res.json();
    if (!res.ok) {
      setError(data.detail || "Bind failed");
      return;
    }
    setShift(data);
    setNote("");
  }

  return (
    <div className="wrap">
      <p className="kicker">
        {shift.shop} · {shift.engine} · {shift.status}
      </p>
      <h1>Overnight board</h1>
      <p className="lede">
        Graph order: {(shift.graph_order || []).join(" → ") || "intake → scout → clerk → gate → closer"}.
        AUTO already moved. HOLD waits for you.
      </p>
      {shift.error ? <p className="error">Fell back after: {shift.error}</p> : null}
      {error ? <p className="error">{error}</p> : null}

      {shift.brief ? (
        <section className="card" style={{ margin: "1.2rem 0" }}>
          <p className="kicker">Morning brief</p>
          <h2>{shift.brief.headline}</h2>
          <div className="grid">
            <div>
              <strong>AUTO</strong>
              <ul>
                {shift.brief.auto_handled.map((x) => (
                  <li key={x}>{x}</li>
                ))}
              </ul>
            </div>
            <div>
              <strong>Owner binds</strong>
              <ul>
                {shift.brief.waiting_on_owner.map((x) => (
                  <li key={x}>{x}</li>
                ))}
              </ul>
            </div>
            <div>
              <strong>First hour</strong>
              <ul>
                {shift.brief.first_hour.map((x) => (
                  <li key={x}>{x}</li>
                ))}
              </ul>
            </div>
          </div>
        </section>
      ) : null}

      <label className="muted">
        Bind note
        <input
          value={note}
          onChange={(e) => setNote(e.target.value)}
          placeholder="Call Chris at 8:05. Offer a $50 make-good, not a full refund."
          style={{
            display: "block",
            width: "100%",
            margin: "0.4rem 0 1rem",
            padding: "0.7rem",
            borderRadius: 12,
            border: "1px solid var(--line)",
            background: "transparent",
            color: "inherit",
          }}
        />
      </label>

      {shift.cases.map((c) => (
        <CaseRow key={c.item_id} c={c} onBind={bind} />
      ))}

      <section style={{ marginTop: "2rem" }}>
        <p className="kicker">Decision log</p>
        {shift.logs.map((log, i) => (
          <p key={`${log.at}-${i}`} className="mono muted">
            {log.agent} · {log.decision} — {log.rationale}
          </p>
        ))}
      </section>
    </div>
  );
}

function CaseRow({
  c,
  onBind,
}: {
  c: CaseFile;
  onBind: (id: string, decision: string) => void;
}) {
  const auto = c.disposition === "AUTO";
  return (
    <article className="case">
      <p>
        <span className={`pill ${auto ? "auto" : "hold"}`}>{c.disposition}</span>{" "}
        <strong>{c.kind}</strong> · {c.item_id}
      </p>
      <p>{c.summary}</p>
      <p className="muted">{c.gate_reason}</p>
      {c.draft ? <p className="mono">{c.draft}</p> : null}
      {c.action ? <p className="muted">{c.action}</p> : null}
      {!auto && !c.bound ? (
        <div className="row">
          <button className="btn lamp" onClick={() => onBind(c.item_id, "approve")}>
            Bind send
          </button>
          <button className="btn ghost" onClick={() => onBind(c.item_id, "refuse")}>
            Bind hold / refuse
          </button>
        </div>
      ) : null}
      {c.bound ? (
        <p className="kicker">
          Owner bound: {c.bind_decision} {c.bind_note}
        </p>
      ) : null}
    </article>
  );
}
