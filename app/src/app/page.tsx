import Link from "next/link";
import { DemoButton } from "@/components/DemoButton";

export default function HomePage() {
  return (
    <>
      <section className="wrap" style={{ paddingTop: "2.5rem" }}>
        <p className="kicker">Professional Agents · Strands Graph</p>
        <h1>The shop is closed. The desk is open.</h1>
        <p className="lede">
          Independent shops drown in after-hours texts: move this, quote that, refund me tonight.
          QuietDesk is a Strands Graph that files the inbox, drafts the work, and stops before
          anything irreversible. The owner binds in the morning. Not another chatbot.
        </p>
        <div className="row">
          <DemoButton />
          <Link href="/how" className="btn ghost">
            Why the gate is code
          </Link>
        </div>
      </section>

      <section className="wrap grid">
        <article className="card">
          <p className="kicker">01 Intake</p>
          <h3>Classify the night</h3>
          <p className="muted">Six inbound items. Reschedule, quote, refund, parts, warranty, restock. Filed, not chatted.</p>
        </article>
        <article className="card">
          <p className="kicker">02 Clerk</p>
          <h3>Draft the work</h3>
          <p className="muted">Replies, quotes, POs, bay moves. Harbor Auto book rates. Never claims it already sent.</p>
        </article>
        <article className="card">
          <p className="kicker">03 Gate</p>
          <h3>Python binds, not the model</h3>
          <p className="muted">Refunds, warranty, angry customers, and big quotes stay HOLD. Standing PO oil can AUTO.</p>
        </article>
      </section>
    </>
  );
}
