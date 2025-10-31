from __future__ import annotations

from statistics import mean
from typing import Iterable, List

from ..types import AgentState, AgentStep


def scoring_step(metric_name: str, scorer) -> AgentStep:
    def _run(state: AgentState) -> AgentState:
        score = scorer(state)
        state.scratchpad.setdefault("metrics", {})[metric_name] = score
        state.transcript.append({"step": f"score_{metric_name}", "content": f"{score:.2f}"})
        return state

    return _run


def aggregate_scores_step(metric: str) -> AgentStep:
    def _run(state: AgentState) -> AgentState:
        metrics = state.scratchpad.get("metrics", {})
        values = metrics.get(metric, [])
        if isinstance(values, Iterable) and not isinstance(values, (str, bytes)):
            values = list(values)
            result = mean(values) if values else 0.0
        else:
            result = float(values or 0.0)
        state.scratchpad[f"metric_{metric}"] = result
        state.transcript.append({"step": f"aggregate_{metric}", "content": f"{result:.2f}"})
        return state

    return _run
