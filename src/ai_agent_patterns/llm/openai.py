from __future__ import annotations

from typing import Any, Dict, Optional

from ..config import AgentConfig
from .base import BaseLLMClient, LLMError


class OpenAILLMClient(BaseLLMClient):
    """OpenAI API integration (requires `openai` package)."""

    def __init__(self, model: str = "gpt-4o-mini") -> None:
        super().__init__(name="openai")
        self.model = model

    def generate(
        self,
        prompt: str,
        *,
        config: AgentConfig,
        context: Optional[Dict[str, Any]] = None,
    ) -> str:
        try:
            from openai import OpenAI
        except ImportError as exc:  # pragma: no cover - import guard
            raise LLMError("openai package is not installed.") from exc

        self.require_env(["OPENAI_API_KEY"])
        client = OpenAI()
        completion = client.responses.create(
            model=config.extras.get("model", self.model),
            input=prompt,
            temperature=config.temperature,
            max_output_tokens=config.max_tokens,
        )
        return completion.output_text  # type: ignore[attr-defined]
