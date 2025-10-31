from __future__ import annotations

from typing import List

from ..prompts import compile_plan_prompt
from ..types import AgentState, AgentStep, LLMClient


def plan_generation_step(llm: LLMClient) -> AgentStep:
    def _run(state: AgentState) -> AgentState:
        agent_config = state.context["agent_config"]
        prompt = compile_plan_prompt(state.input_text)
        plan = llm.generate(prompt, config=agent_config, context={"intent": "plan"})
        steps = [step.strip() for step in plan.split("\n") if step.strip()]
        state.scratchpad["plan_steps"] = steps
        state.transcript.append({"step": "plan", "content": plan})
        return state

    return _run


def plan_execution_step(executor) -> AgentStep:
    def _run(state: AgentState) -> AgentState:
        steps: List[str] = state.scratchpad.get("plan_steps", [])
        outcomes = []
        for step in steps:
            outcomes.append(executor(step, state))
        content = "\n".join(outcomes)
        state.transcript.append({"step": "execute_plan", "content": content})
        state.output = content
        return state

    return _run
