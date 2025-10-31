from __future__ import annotations

from random import Random

from ..config import AgentConfig, DemoConfig
from ..core import Agent
from ..factory import resolve_llm
from ..types import AgentRunResult, PatternMetadata
from ..workflows.evaluation import aggregate_scores_step, scoring_step
from . import register_pattern


METADATA = PatternMetadata(
    name="evaluation_monitoring",
    summary="Captures runtime metrics to monitor agent quality trends.",
    chapter="Chapter 19",
    part="Part Four",
    tags=["evaluation", "metrics"],
)


def build_agent(config: AgentConfig) -> Agent:
    llm = resolve_llm(config)
    rng = Random(42)

    def answer(state):
        reply = llm.generate(
            f"Provide solution to: {state.input_text}",
            config=config,
            context={"intent": "summarize"},
        )
        state.output = reply
        state.transcript.append({"step": "answer", "content": reply})
        return state

    def satisfaction(state):
        score = 0.6 + 0.4 * rng.random()
        return score

    def latency(state):
        return 0.3 + 0.1 * rng.random()

    steps = [
        answer,
        scoring_step("satisfaction_samples", satisfaction),
        scoring_step("latency", latency),
        aggregate_scores_step("satisfaction_samples"),
    ]

    return Agent(
        name=METADATA.name,
        llm=llm,
        steps=steps,
        config=config,
    )


def demo(demo_config: DemoConfig) -> AgentRunResult:
    agent = build_agent(demo_config.agent_config)
    result = agent.run(demo_config.input_text, context={"demo": True})
    return result


register_pattern(METADATA, build_agent, demo)
