export default function HowPage() {
  return (
    <div className="wrap">
      <p className="kicker">Judges · architecture</p>
      <h1>The model drafts. Python binds.</h1>
      <p className="lede">
        QuietDesk is not a single prompt with tools glued on. It is a Strands Graph of five
        specialists, then a deterministic gate that the language model cannot override.
      </p>
      <div className="grid">
        <article className="card">
          <h3>Graph</h3>
          <p className="muted">intake → scout → clerk → gate → closer. Edges are code. Order is evidence.</p>
        </article>
        <article className="card">
          <h3>Tools</h3>
          <p className="muted">file_case, draft_work, apply_shop_gate, write_morning_brief persist a shift JSON, not chat.</p>
        </article>
        <article className="card">
          <h3>Policy</h3>
          <p className="muted">Refunds, warranty, anger, and quotes over $150 HOLD. NAPA standing PO under $80 AUTO.</p>
        </article>
      </div>
      <section id="architecture" className="card" style={{ marginTop: "1.5rem" }}>
        <h2>Harbor Auto overnight</h2>
        <p className="muted">
          Maya&apos;s oil change moves because bay 2 is open at 10:30. Luis&apos;s 5W-30 drop is a
          standing PO. Chris wants $187 back — that never auto-sends. Priya&apos;s inspection fail
          is legal. Jordan&apos;s $420 quote waits. Wagner is not NAPA.
        </p>
        <img
          src="/architecture.svg"
          alt="QuietDesk Strands Graph: inbox to intake, scout, clerk, Python gate, closer, then owner bind"
          style={{ width: "100%", marginTop: "1rem", borderRadius: 12 }}
        />
      </section>
    </div>
  );
}
