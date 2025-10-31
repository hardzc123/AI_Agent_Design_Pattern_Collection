from __future__ import annotations

from ..prompts import critique_prompt, final_answer_prompt
from ..types import AgentState, AgentStep, LLMClient


def reflection_step(llm: LLMClient, iterations: int = 1) -> AgentStep:
    def _run(state: AgentState) -> AgentState:
        agent_config = state.context["agent_config"]
        draft = state.output or state.scratchpad.get("initial_answer", "")
        for index in range(iterations):
            critique = llm.generate(critique_prompt(draft), config=agent_config, context={"intent": "reflect"})
            improved = llm.generate(final_answer_prompt(draft, critique), config=agent_config, context=None)
            state.transcript.append({"step": f"reflect_{index}", "content": critique})
            state.transcript.append({"step": f"improve_{index}", "content": improved})
            draft = improved
        state.output = draft
        return state

    return _run
