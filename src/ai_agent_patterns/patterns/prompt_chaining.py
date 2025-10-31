from __future__ import annotations

from ..config import AgentConfig, DemoConfig
from ..core import Agent
from ..factory import resolve_llm
from ..prompts import critique_prompt, final_answer_prompt, prompt_chain_template
from ..types import AgentRunResult, PatternMetadata
from . import register_pattern


METADATA = PatternMetadata(
    name="prompt_chaining",
    summary="Decompose tasks into sequential prompts for draft, critique, and refinement.",
    chapter="Chapter 1",
    part="Part One",
    tags=["prompting", "sequential"],
)


def build_agent(config: AgentConfig) -> Agent:
    llm = resolve_llm(config)

    def draft_step(state):
        prompt = prompt_chain_template(state.input_text)
        draft = llm.generate(prompt, config=config, context={"intent": "draft"})
        state.scratchpad["draft"] = draft
        state.output = draft
        state.transcript.append({"step": "draft", "content": draft})
        return state

    def critique_step(state):
        draft = state.scratchpad["draft"]
        critique = llm.generate(critique_prompt(draft), config=config, context={"intent": "reflect"})
        state.scratchpad["critique"] = critique
        state.transcript.append({"step": "critique", "content": critique})
        return state

    def improve_step(state):
        draft = state.scratchpad["draft"]
        critique = state.scratchpad["critique"]
        improved = llm.generate(final_answer_prompt(draft, critique), config=config, context=None)
        state.output = improved
        state.transcript.append({"step": "improve", "content": improved})
        return state

    return Agent(
        name=METADATA.name,
        llm=llm,
        steps=[draft_step, critique_step, improve_step],
        config=config,
    )


def demo(demo_config: DemoConfig) -> AgentRunResult:
    agent = build_agent(demo_config.agent_config)
    return agent.run(demo_config.input_text, context={"demo": True})


register_pattern(METADATA, build_agent, demo)
