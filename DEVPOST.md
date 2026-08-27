# Devpost paste — QuietDesk

Track: **Professional Agents**

## Built with

Strands Agents SDK, Amazon Bedrock AgentCore (entrypoint), FastAPI, Next.js, Python policy gate

## Tagline

The shop is closed. The desk is open.

## Elevator pitch (≤ 200 chars)

Overnight front office for independent shops. A Strands Graph files the night inbox and drafts the work. Python — not the model — decides what can move. The owner binds in the morning.

## Description (paste into Devpost)

### The problem

Independent shops do not have a night desk. After 6pm the lock screen fills up: move this appointment, quote those brakes, refund me tonight, is the inspection fail covered. In the morning the owner is already behind the counter. Sixty messages, zero decisions made.

### Who it is for

Owners of independent service shops — auto, dental, veterinary, HVAC. The Harbor Auto demo is Tacoma, but the policy pattern is the same anywhere a human must bind refunds, warranty, and angry customers.

### Why it matters

Another chatbot is another app to open. QuietDesk runs the overnight shift and only surfaces what is irreversible. Two jobs can move while everyone sleeps. Four binds wait on a morning card. That is hours back, every weekday.

### How it works

A **Strands Agents Graph** of five specialists:

1. **Intake** files each inbound item (`file_case`)
2. **Scout** writes the operating picture
3. **Clerk** drafts SMS, quotes, and POs (`draft_work`) — never claims it sent
4. **Gate** calls `apply_shop_gate` — **Python policy**, not an LLM vote
5. **Closer** writes the 06:30 brief (`write_morning_brief`)

The owner opens the night board and binds HOLD items. AUTO items already moved.

Harbor Auto policy (code, not a prompt):

- AUTO: same-day reschedule into an open bay; NAPA standing PO restock under $80
- HOLD: refunds, warranty/inspection, angry sentiment, quotes $150+, unknown vendors

Optional Amazon Bedrock AgentCore runtime is in `agents/quietdesk/runtime.py`. Local demo runs without AWS keys via a fixture that uses the **same policy**.

### What to click

1. Clone the repo, start the API + UI (README)
2. Click **Run Harbor Auto overnight**
3. Confirm Maya 10:30 and NAPA 5W-30 are AUTO
4. Bind Chris's $187 refund in the morning

Architecture diagram: `docs/architecture.png` (also `docs/architecture.svg`). Demo video: https://youtu.be/lr9uhRi2YV8

## Built with (checkboxes)

- Strands Agents SDK
- Amazon Bedrock / AgentCore (optional deploy)
- Python
- Next.js
