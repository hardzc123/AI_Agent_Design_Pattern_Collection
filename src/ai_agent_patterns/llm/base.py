from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional, Protocol

from ..config import AgentConfig


class LLMError(RuntimeError):
    pass


class SupportsGenerate(Protocol):
    def generate(self, prompt: str, *, config: AgentConfig, context: Optional[Dict[str, Any]] = None) -> str:
        ...


@dataclass
class BaseLLMClient:
    name: str

    def generate(self, prompt: str, *, config: AgentConfig, context: Optional[Dict[str, Any]] = None) -> str:
        raise NotImplementedError

    @staticmethod
    def require_env(keys: list[str]) -> None:
        missing = [key for key in keys if not os.getenv(key)]
        if missing:
            raise LLMError(f"Missing environment variables: {', '.join(missing)}")
