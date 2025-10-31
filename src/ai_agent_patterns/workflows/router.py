from __future__ import annotations

from typing import Dict

from ..prompts import routing_prompt
from ..types import AgentState, AgentStep, LLMClient


def intent_router_step(llm: LLMClient, options: Dict[str, str]) -> AgentStep:
    def _run(state: AgentState) -> AgentState:
        prompt = routing_prompt(state.input_text)
        agent_config = state.context.get("agent_config")
        if agent_config is None:
            raise ValueError("agent_config missing from state context.")
        decision = llm.generate(prompt, config=agent_config, context={"intent": "route"})
        state.scratchpad["route_decision_raw"] = decision
        routed = _normalize_decision(decision, options)
        state.scratchpad["route_decision"] = routed
        state.transcript.append({"step": "route", "content": f"Decision: {routed}"})
        return state

    return _run


def _normalize_decision(decision: str, mapping: Dict[str, str]) -> str:
    lowered = decision.strip().lower()
    for key, value in mapping.items():
        if key in lowered:
            return value
    return mapping.get("default", "general")
