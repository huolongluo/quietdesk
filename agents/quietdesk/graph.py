from __future__ import annotations

import json
from datetime import datetime, timezone
from uuid import uuid4

from strands import Agent
from strands.multiagent import GraphBuilder

from . import store
from .fixture_run import run_fixture, seed_if_graph_skipped_tools
from .fixtures import HARBOR_INBOX, HARBOR_POLICY, harbor_story
from .model_factory import load_model
from .models import DecisionLog, Shift
from .prompts import CLERK, CLOSER, GATE, INTAKE, SCOUT
from .tools import CURRENT_SHIFT, apply_shop_gate, draft_work, file_case, write_morning_brief


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _log(shift: Shift, agent: str, decision: str, rationale: str) -> None:
    shift.logs.append(
        DecisionLog(at=_now(), agent=agent, decision=decision, rationale=rationale)  # type: ignore[arg-type]
    )
    store.save(shift)


def _inbox_blob(shift: Shift) -> str:
    return (
        f"{harbor_story()}\n\nSHOP POLICY:\n{json.dumps(shift.policy.model_dump(), indent=2)}\n\n"
        f"INBOX:\n{json.dumps([item.model_dump() for item in shift.inbox], indent=2)}"
    )


def build_graph(model) -> object:
    shared = [file_case, draft_work, apply_shop_gate, write_morning_brief]
    intake = Agent(name="intake", model=model, system_prompt=INTAKE, tools=shared)
    scout = Agent(name="scout", model=model, system_prompt=SCOUT, tools=shared)
    clerk = Agent(name="clerk", model=model, system_prompt=CLERK, tools=shared)
    gate = Agent(name="gate", model=model, system_prompt=GATE, tools=shared)
    closer = Agent(name="closer", model=model, system_prompt=CLOSER, tools=shared)

    builder = GraphBuilder()
    builder.add_node(intake, "intake")
    builder.add_node(scout, "scout")
    builder.add_node(clerk, "clerk")
    builder.add_node(gate, "gate")
    builder.add_node(closer, "closer")
    builder.add_edge("intake", "scout")
    builder.add_edge("scout", "clerk")
    builder.add_edge("clerk", "gate")
    builder.add_edge("gate", "closer")
    builder.set_entry_point("intake")
    try:
        builder.set_execution_timeout(180)
    except AttributeError:
        pass
    return builder.build()


def new_harbor_shift() -> Shift:
    shift = Shift(
        id=str(uuid4()),
        shop="Harbor Auto",
        created_at=_now(),
        policy=HARBOR_POLICY,
        inbox=list(HARBOR_INBOX),
    )
    return store.save(shift)


def run_shift(shift: Shift) -> Shift:
    token = CURRENT_SHIFT.set(shift.id)
    shift.status = "running"
    store.save(shift)
    try:
        model = load_model()
        if model is None:
            return run_fixture(shift)

        graph = build_graph(model)
        shift.engine = "strands-graph"
        _log(shift, "intake", "GRAPH_START", "Strands Graph: intake → scout → clerk → gate → closer")
        result = graph(_inbox_blob(shift))
        order = []
        execution_order = getattr(result, "execution_order", None)
        if execution_order:
            order = [getattr(n, "node_id", str(n)) for n in execution_order]
        shift = store.load(shift.id)
        shift.graph_order = order or ["intake", "scout", "clerk", "gate", "closer"]
        shift = seed_if_graph_skipped_tools(shift)
        shift.status = "briefed"
        shift.current_agent = None
        shift.closed_at = _now()
        _log(shift, "closer", "GRAPH_DONE", f"status={getattr(result, 'status', 'ok')}")
        return store.save(shift)
    except Exception as exc:  # noqa: BLE001 — demo must always produce a board
        shift = store.load(shift.id)
        shift = run_fixture(shift)
        shift.engine = "fixture-fallback"
        shift.error = str(exc)
        return store.save(shift)
    finally:
        CURRENT_SHIFT.reset(token)
