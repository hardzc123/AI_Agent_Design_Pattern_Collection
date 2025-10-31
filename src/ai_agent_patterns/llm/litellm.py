from __future__ import annotations

from typing import Any, Dict, Optional

from ..config import AgentConfig
from .base import BaseLLMClient, LLMError


class LiteLLMClient(BaseLLMClient):
    """Thin wrapper around litellm router."""

    def __init__(self, model: str = "gpt-4o-mini") -> None:
        super().__init__(name="litellm")
        self.model = model

    def generate(
        self,
        prompt: str,
        *,
        config: AgentConfig,
        context: Optional[Dict[str, Any]] = None,
    ) -> str:
        try:
            from litellm import completion
        except ImportError as exc:  # pragma: no cover - import guard
            raise LLMError("litellm package is not installed.") from exc

        response = completion(
            model=config.extras.get("model", self.model),
            messages=[{"role": "user", "content": prompt}],
            temperature=config.temperature,
            max_tokens=config.max_tokens,
        )
        return response["choices"][0]["message"]["content"]
