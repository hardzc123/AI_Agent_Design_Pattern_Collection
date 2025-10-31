from __future__ import annotations

from ..config import AgentConfig, DemoConfig
from ..core import Agent
from ..factory import resolve_llm
from ..types import AgentRunResult, PatternMetadata
from . import register_pattern


METADATA = PatternMetadata(
    name="reasoning",
    summary="Showcases deliberate reasoning strategies like CoT and ReAct.",
    chapter="Chapter 17",
    part="Part Four",
    tags=["reasoning", "analysis"],
)


def build_agent(config: AgentConfig) -> Agent:
    llm = resolve_llm(config)

    def think_step(state):
        prompt = (
            "Use chain-of-thought reasoning to break down the problem step-by-step.\n"
            f"Problem: {state.input_text}"
        )
        thoughts = llm.generate(prompt, config=config, context={"intent": "reason"})
        state.scratchpad["thoughts"] = thoughts
        state.transcript.append({"step": "think", "content": thoughts})
        return state

    def act_step(state):
        prompt = (
            "Given the thoughts below, produce a concise final answer.\n"
            f"Thoughts:\n{state.scratchpad['thoughts']}"
        )
        answer = llm.generate(prompt, config=config, context={"intent": "summarize"})
        state.output = answer
        state.transcript.append({"step": "answer", "content": answer})
        return state

    return Agent(
        name=METADATA.name,
        llm=llm,
        steps=[think_step, act_step],
        config=config,
    )


def demo(demo_config: DemoConfig) -> AgentRunResult:
    agent = build_agent(demo_config.agent_config)
    return agent.run(demo_config.input_text, context={"demo": True})


register_pattern(METADATA, build_agent, demo)
