"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export function DemoButton() {
  const router = useRouter();
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  async function run() {
    setBusy(true);
    setError("");
    try {
      const res = await fetch("/agent/shifts/demo", { method: "POST" });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Demo failed");
      router.push(`/shift/${data.id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Demo failed");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div>
      <button className="btn lamp" onClick={run} disabled={busy}>
        {busy ? "Working the night inbox…" : "Run Harbor Auto overnight"}
      </button>
      {error ? <p className="error">{error}</p> : null}
    </div>
  );
}
