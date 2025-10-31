from __future__ import annotations

import hashlib
import random
from typing import Any, Dict, Optional

from ..config import AgentConfig
from .base import BaseLLMClient


class MockLLMClient(BaseLLMClient):
    """Deterministic mock used for demos/tests."""

    def __init__(self, name: str = "mock-llm", seed: int = 13) -> None:
        super().__init__(name=name)
        self.random = random.Random(seed)

    def generate(
        self,
        prompt: str,
        *,
        config: AgentConfig,
        context: Optional[Dict[str, Any]] = None,
    ) -> str:
        context = context or {}
        digest = hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:8]
        intent = context.get("intent")
        if intent == "summarize":
            return f"[mock-summary-{digest}] Key takeaways extracted."
        if intent == "plan":
            return f"[mock-plan-{digest}] -> Step 1, Step 2, Step 3"
        if intent == "reflect":
            return f"[mock-reflection-{digest}] Suggestions: tighten answer, cite source."
        if "priority" in prompt.lower():
            return "Priority: Critical | Owner: Core Support | ETA: 2h"
        if "route" in prompt.lower():
            return "Routing decision: escalate_to_specialist"
        actions = [
            "Provide concise answer.",
            "Consult knowledge base.",
            "Collect human feedback.",
            "Execute calculation tool.",
        ]
        idx = int(digest, 16) % len(actions)
        return f"[mock-response-{digest}] {actions[idx]}"
