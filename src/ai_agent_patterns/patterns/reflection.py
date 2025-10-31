from __future__ import annotations

from ..config import AgentConfig, DemoConfig
from ..core import Agent
from ..factory import resolve_llm
from ..prompts import prompt_chain_template
from ..types import AgentRunResult, PatternMetadata
from ..workflows.reflection import reflection_step
from . import register_pattern


METADATA = PatternMetadata(
    name="reflection",
    summary="Incorporates self-critique loops to iteratively improve responses.",
    chapter="Chapter 4",
    part="Part One",
    tags=["reflection", "quality"],
)


def build_agent(config: AgentConfig) -> Agent:
    llm = resolve_llm(config)

    def initial_answer(state):
        prompt = prompt_chain_template(state.input_text)
        answer = llm.generate(prompt, config=config, context={"intent": "draft"})
        state.scratchpad["initial_answer"] = answer
        state.output = answer
        state.transcript.append({"step": "initial_answer", "content": answer})
        return state

    reflect = reflection_step(llm, iterations=2)

    return Agent(
        name=METADATA.name,
        llm=llm,
        steps=[initial_answer, reflect],
        config=config,
    )


def demo(demo_config: DemoConfig) -> AgentRunResult:
    agent = build_agent(demo_config.agent_config)
    return agent.run(demo_config.input_text, context={"demo": True})


register_pattern(METADATA, build_agent, demo)
