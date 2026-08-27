# QuietDesk

**The shop is closed. The desk is open.**

Overnight front office for independent shops, built as a **Strands Agents Graph**.
Submitted to [Agents for Humans](https://agentsforhumans.devpost.com/) · **Professional Agents**.

QuietDesk does not chat with the owner at 11pm. It files the night inbox, drafts the work, and **stops before anything irreversible**. Refunds, warranty, and angry customers stay on a morning board. Standing-PO oil can move while everyone sleeps.

## Why this can win

Judges score Strands depth, a complete product, a real audience, non-obvious agent work, and a demo that actually runs.

| Criterion | What we built |
| --- | --- |
| Technical | Strands `GraphBuilder`: intake → scout → clerk → gate → closer. Custom tools persist cases. AgentCore entrypoint in `runtime.py`. |
| Design | Night board + morning brief + owner bind. Not a chat transcript. |
| Impact | Independent shops lose jobs in the after-hours SMS pile. Harbor Auto is the proof, not a toy FAQ bot. |
| Originality | The LLM never binds. `policy.py` is the product. |
| Presentation | Three-minute Harbor Auto overnight. AUTO vs HOLD is visible. |

## Architecture

![Architecture](docs/architecture.svg)

```text
Inbox (SMS / email / voicemail)
        │
        ▼
 Strands Graph
 intake → scout → clerk → gate → closer
        │              │
        │              └── apply_shop_gate()  [Python, not the model]
        ▼
 Shift JSON  →  Next.js night board  →  owner bind
        │
        └── optional Amazon Bedrock AgentCore runtime
```

## Quick start

Needs Python 3.12 (not 3.14). No AWS key required for the Harbor Auto fixture.

```bash
cd quietdesk/agents
python3.12 -m venv .venv
source .venv/bin/activate
pip install strands-agents strands-agents-tools fastapi "uvicorn[standard]" pydantic python-dotenv pytest
QUIETDESK_ENGINE=fixture PYTHONPATH=. python -m quietdesk.server
```

In another terminal:

```bash
cd quietdesk/app
npm install
AGENT_URL=http://127.0.0.1:8787 npm run dev
```

Open http://127.0.0.1:3010 and click **Run Harbor Auto overnight**.

Demo recording (needs the API + UI running):

```bash
cd app
APP_URL=http://127.0.0.1:3010 npm run demo:video
```

The cut is `docs/demo.mp4` (~47s). Upload it to **public** YouTube or Vimeo for Devpost. Architecture still: `docs/architecture.svg` and `docs/architecture.png`.

### Live models (optional)

```bash
export GEMINI_API_KEY=...          # or OPENAI_API_KEY, or AWS creds for Bedrock
unset QUIETDESK_ENGINE             # allow strands-graph
```

If the graph throws, the runner falls back to the fixture so the demo never dies.

### Tests

```bash
cd agents && pytest -q
```

Expect Maya's reschedule AUTO, NAPA oil AUTO, refund/warranty/big quote HOLD.

## AgentCore

```bash
pip install -e ".[agentcore]"
# then: agentcore configure --entrypoint quietdesk/runtime.py --name quietdesk
#        agentcore launch
```

Payload: `{"action":"demo"}` or `{"action":"bind","shift_id":"...","item_id":"msg-3","decision":"approve"}`.

## License

Apache-2.0

Submission paste: `DEVPOST.md`. Recording script: `VIDEO_SCRIPT.md`. Diagram: `docs/architecture.svg`.
