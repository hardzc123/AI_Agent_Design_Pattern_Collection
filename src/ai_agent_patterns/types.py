from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Protocol

from .config import AgentConfig


class LLMClient(Protocol):
    """Protocol implemented by LLM client adapters."""

    name: str

    def generate(self, prompt: str, *, config: AgentConfig, context: Optional[Dict[str, Any]] = None) -> str:
        ...


@dataclass(slots=True)
class PatternMetadata:
    name: str
    summary: str
    chapter: str
    part: str
    tags: List[str] = field(default_factory=list)


@dataclass(slots=True)
class AgentState:
    input_text: str
    context: Dict[str, Any] = field(default_factory=dict)
    scratchpad: Dict[str, Any] = field(default_factory=dict)
    transcript: List[Dict[str, Any]] = field(default_factory=list)
    output: Optional[str] = None


AgentStep = Callable[[AgentState], AgentState]


@dataclass(slots=True)
class AgentRunResult:
    pattern: str
    output: str
    transcript: List[Dict[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pattern": self.pattern,
            "output": self.output,
            "transcript": self.transcript,
        }

    def to_markdown(self) -> str:
        lines = [f"### Pattern: {self.pattern}", "", f"**Output**: {self.output}", "", "#### Transcript"]
        for idx, step in enumerate(self.transcript, start=1):
            operation = step.get("step", f"step-{idx}")
            content = step.get("content", "")
            lines.append(f"{idx}. **{operation}** — {content}")
        return "\n".join(lines)
