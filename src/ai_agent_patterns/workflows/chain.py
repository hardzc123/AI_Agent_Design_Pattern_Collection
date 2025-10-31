from __future__ import annotations

from typing import Callable

from ..core import Agent
from ..types import AgentState, AgentStep


def seq_step(name: str, fn: Callable[[AgentState], str]) -> AgentStep:
    """Wraps a state mutating callable into an AgentStep with transcript logging."""

    def _run(state: AgentState) -> AgentState:
        result = fn(state)
        state.output = result
        state.transcript.append({"step": name, "content": result})
        return state

    _run.__name__ = name
    return _run
