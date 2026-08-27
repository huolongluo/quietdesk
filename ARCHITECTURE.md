# QuietDesk architecture

## Product loop

Harbor Auto closes at 18:00. Six inbound items arrive. QuietDesk runs one shift:

1. **Intake** files each item (`file_case`).
2. **Scout** writes the overnight picture (bays, parts, legal heat).
3. **Clerk** drafts SMS / quotes / POs (`draft_work`) and never claims send.
4. **Gate** calls `apply_shop_gate` — **Python policy**, not an LLM vote.
5. **Closer** writes the 06:30 card (`write_morning_brief`).
6. Owner binds HOLD items on the night board.

## Policy (the actual product)

| AUTO | HOLD |
| --- | --- |
| Same-day reschedule into an open bay | Refunds |
| NAPA standing PO restock ≤ $80 | Warranty / inspection / legal |
| | Angry sentiment |
| | Quotes ≥ $150 |
| | Non-preferred vendors |

The model may argue. The gate ignores it.

## Strands usage

- `Agent` specialists with shared tools
- `GraphBuilder` DAG with timeout
- Tools write `Shift` JSON via `ContextVar`
- Optional `BedrockAgentCoreApp` in `runtime.py`

## Fallback

No keys → `QUIETDESK_ENGINE=fixture` (or automatic). Same policy, same board, so the video does not depend on Bedrock quota.
