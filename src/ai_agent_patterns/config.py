from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(slots=True)
class AgentConfig:
    """Runtime configuration for agent factories."""

    provider: str = "mock"
    model: str = "mock-llm"
    temperature: float = 0.2
    max_tokens: int = 512
    use_tools: bool = True
    budget: Optional[float] = None
    extras: Dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class DemoConfig:
    """Configuration used by demos and tests."""

    agent_config: AgentConfig = field(default_factory=AgentConfig)
    input_text: str = "Summarize the key issue."
    context: Dict[str, Any] = field(default_factory=dict)
    mock: bool = True
