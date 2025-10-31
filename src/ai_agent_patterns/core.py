from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional

try:  # pragma: no cover - fallback when rich is unavailable
    from rich.console import Console
    from rich.table import Table
except ImportError:  # pragma: no cover
    class Table:
        def __init__(self, title: str | None = None) -> None:
            self.title = title
            self.rows: List[tuple[str, str]] = []

        def add_column(self, _name: str) -> None:
            return

        def add_row(self, step: str, details: str) -> None:
            self.rows.append((step, details))

    class Console:
        def __init__(self, record: bool = False) -> None:
            self.record = record
            self._buffer: List[str] = []

        def print(self, table: Table) -> None:
            header = f"Agent run — {table.title}" if table.title else "Agent run"
            lines = [header] + [f"{step}: {details}" for step, details in table.rows]
            self._buffer.extend(lines)

        def export_text(self) -> str:
            return "\n".join(self._buffer)

from .config import AgentConfig
from .types import AgentRunResult, AgentState, AgentStep, LLMClient

logger = logging.getLogger("ai_agent_patterns.agent")


@dataclass(slots=True)
class Agent:
    """Composable agent executing a sequence of steps."""

    name: str
    llm: LLMClient
    steps: Iterable[AgentStep]
    config: AgentConfig = field(default_factory=AgentConfig)

    def run(self, input_text: str, context: Optional[Dict[str, object]] = None) -> AgentRunResult:
        state = AgentState(
            input_text=input_text,
            context=dict(context or {}),
            scratchpad={},
            transcript=[],
        )
        state.context.setdefault("agent_config", self.config)
        for step in self.steps:
            state = step(state)
        if state.output is None:
            state.output = state.scratchpad.get("final_output", "")
        return AgentRunResult(pattern=self.name, output=state.output or "", transcript=state.transcript)

    def pretty_print(self, result: AgentRunResult) -> str:
        table = Table(title=f"Agent run — {self.name}")
        table.add_column("Step")
        table.add_column("Details")
        for idx, entry in enumerate(result.transcript, start=1):
            table.add_row(str(idx), entry.get("content", ""))
        console = Console(record=True)
        console.print(table)
        return console.export_text()


def llm_step(agent: Agent, prompt_builder) -> AgentStep:
    """Utility to build a step fetching LLM output."""

    def _run(state: AgentState) -> AgentState:
        prompt = prompt_builder(state)
        response = agent.llm.generate(prompt, config=agent.config, context=state.context)
        state.transcript.append({"step": prompt_builder.__name__, "content": response})
        state.scratchpad[f"{prompt_builder.__name__}_output"] = response
        state.output = response
        return state

    return _run


def write_transcript_step(name: str, content_builder) -> AgentStep:
    """Log-only step without LLM interaction."""

    def _run(state: AgentState) -> AgentState:
        content = content_builder(state)
        state.transcript.append({"step": name, "content": content})
        return state

    _run.__name__ = name
    return _run


def finalizer_step(field: str = "output") -> AgentStep:
    def _run(state: AgentState) -> AgentState:
        if state.output is None and field in state.scratchpad:
            state.output = state.scratchpad[field]
        state.transcript.append({"step": "finalize", "content": state.output or ""})
        return state

    return _run
