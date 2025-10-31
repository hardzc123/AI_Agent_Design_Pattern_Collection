from __future__ import annotations

from ..config import AgentConfig, DemoConfig
from ..core import Agent
from ..factory import resolve_llm
from ..types import AgentRunResult, PatternMetadata
from . import register_pattern


METADATA = PatternMetadata(
    name="exploration_discovery",
    summary="Encourages divergent thinking to surface novel solutions.",
    chapter="Chapter 21",
    part="Part Four",
    tags=["exploration", "creativity"],
)


def build_agent(config: AgentConfig) -> Agent:
    llm = resolve_llm(config)

    def generate_ideas(state):
        prompt = (
            "Produce three unconventional ideas to tackle the following challenge.\n"
            f"Challenge: {state.input_text}\n"
            "Format as numbered list."
        )
        ideas = llm.generate(prompt, config=config, context={"intent": "explore"})
        state.scratchpad["ideas"] = ideas
        state.transcript.append({"step": "generate_ideas", "content": ideas})
        return state

    def evaluate_diversity(state):
        prompt = (
            "Assess the diversity of these ideas and suggest how to test the strongest one.\n"
            f"Ideas:\n{state.scratchpad['ideas']}"
        )
        analysis = llm.generate(prompt, config=config, context={"intent": "evaluate"})
        state.output = analysis
        state.transcript.append({"step": "evaluate", "content": analysis})
        return state

    return Agent(
        name=METADATA.name,
        llm=llm,
        steps=[generate_ideas, evaluate_diversity],
        config=config,
    )


def demo(demo_config: DemoConfig) -> AgentRunResult:
    agent = build_agent(demo_config.agent_config)
    return agent.run(demo_config.input_text, context={"demo": True})


register_pattern(METADATA, build_agent, demo)
