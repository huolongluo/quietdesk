import Link from "next/link";
import { listShifts } from "@/lib/api";

export const dynamic = "force-dynamic";

export default async function OpsPage() {
  const shifts = await listShifts();
  return (
    <div className="wrap">
      <p className="kicker">Night board</p>
      <h1>Shifts</h1>
      {shifts.length === 0 ? <p className="muted">No overnight runs yet.</p> : null}
      {shifts.map((s) => (
        <p key={s.id}>
          <Link href={`/shift/${s.id}`}>
            {s.shop} · {s.status} · {s.engine} · {s.id.slice(0, 8)}
          </Link>
        </p>
      ))}
    </div>
  );
}
