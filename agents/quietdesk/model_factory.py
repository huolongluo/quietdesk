from __future__ import annotations

import os
from typing import Any


def has_live_model() -> bool:
    if os.getenv("QUIETDESK_ENGINE") == "fixture":
        return False
    return bool(
        os.getenv("GEMINI_API_KEY")
        or os.getenv("GOOGLE_API_KEY")
        or os.getenv("OPENAI_API_KEY")
        or os.getenv("AWS_ACCESS_KEY_ID")
        or os.getenv("AWS_PROFILE")
        or os.getenv("AWS_BEARER_TOKEN_BEDROCK")
    )


def load_model() -> Any | None:
    if os.getenv("QUIETDESK_ENGINE") == "fixture":
        return None

    gemini = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if gemini:
        os.environ.setdefault("GOOGLE_API_KEY", gemini)
        model_id = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        try:
            from strands.models.gemini import GeminiModel

            return GeminiModel(model_id=model_id)
        except Exception:
            from strands.models.litellm import LiteLLMModel

            return LiteLLMModel(model_id=f"gemini/{model_id}")

    if os.getenv("OPENAI_API_KEY"):
        from strands.models.openai import OpenAIModel

        return OpenAIModel(model_id=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"))

    if (
        os.getenv("AWS_ACCESS_KEY_ID")
        or os.getenv("AWS_PROFILE")
        or os.getenv("AWS_BEARER_TOKEN_BEDROCK")
    ):
        from strands.models import BedrockModel

        return BedrockModel(
            model_id=os.getenv(
                "BEDROCK_MODEL_ID",
                "anthropic.claude-sonnet-4-20250514-v1:0",
            ),
            region_name=os.getenv("AWS_REGION", "us-east-1"),
        )

    return None
