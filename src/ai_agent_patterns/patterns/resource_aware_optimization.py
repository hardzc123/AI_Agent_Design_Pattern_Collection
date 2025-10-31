from __future__ import annotations

from ..config import AgentConfig, DemoConfig
from ..core import Agent
from ..factory import resolve_llm
from ..types import AgentRunResult, PatternMetadata
from . import register_pattern


METADATA = PatternMetadata(
    name="resource_aware_optimization",
    summary="Balances quality and cost under dynamic budget constraints.",
    chapter="Chapter 16",
    part="Part Four",
    tags=["optimization", "budget"],
)


def build_agent(config: AgentConfig) -> Agent:
    llm = resolve_llm(config)

    def allocate_resources(state):
        budget = state.context.get("budget", config.budget or 1.0)
        if budget >= 1.5:
            mode = "comprehensive"
            temperature = 0.2
        elif budget >= 1.0:
            mode = "balanced"
            temperature = 0.4
        else:
            mode = "lean"
            temperature = 0.6
        state.scratchpad["llm_temperature"] = temperature
        state.scratchpad["mode"] = mode
        state.transcript.append({"step": "allocate", "content": f"Mode={mode}, temp={temperature}"})
        return state

    def respond(state):
        temperature = state.scratchpad["llm_temperature"]
        mode = state.scratchpad["mode"]
        config.temperature = temperature
        answer = llm.generate(
            f"Respond in {mode} mode to: {state.input_text}",
            config=config,
            context={"intent": mode},
        )
        state.output = answer
        state.transcript.append({"step": "respond", "content": answer})
        return state

    return Agent(
        name=METADATA.name,
        llm=llm,
        steps=[allocate_resources, respond],
        config=config,
    )


def demo(demo_config: DemoConfig) -> AgentRunResult:
    context = {"demo": True, "budget": 0.8}
    agent = build_agent(demo_config.agent_config)
    return agent.run(demo_config.input_text, context=context)


register_pattern(METADATA, build_agent, demo)
