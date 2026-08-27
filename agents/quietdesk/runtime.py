"""Amazon Bedrock AgentCore entrypoint.

Deploy:
  pip install bedrock-agentcore bedrock-agentcore-starter-toolkit
  agentcore configure --entrypoint quietdesk/runtime.py --name quietdesk
  agentcore launch
"""

from __future__ import annotations

from .runner import start_demo, bind_case
from . import store

try:
    from bedrock_agentcore.runtime import BedrockAgentCoreApp

    app = BedrockAgentCoreApp()
except ImportError:  # local machines without the extra
    app = None


def invoke(payload: dict) -> dict:
    action = (payload or {}).get("action", "demo")
    if action == "demo":
        return start_demo().model_dump()
    if action == "get":
        return store.load(payload["shift_id"]).model_dump()
    if action == "bind":
        return bind_case(
            payload["shift_id"],
            payload["item_id"],
            payload.get("decision", "approve"),
            payload.get("note", ""),
        ).model_dump()
    if action == "list":
        return {"shifts": [s.model_dump() for s in store.list_shifts()]}
    return {"error": f"unknown action {action}"}


if app is not None:

    @app.entrypoint
    def agentcore_invoke(payload: dict):
        return invoke(payload or {})


if __name__ == "__main__":
    if app is None:
        raise SystemExit("pip install bedrock-agentcore")
    app.run()
