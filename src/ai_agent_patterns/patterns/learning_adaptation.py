from __future__ import annotations

from ..config import AgentConfig, DemoConfig
from ..core import Agent
from ..factory import resolve_llm
from ..types import AgentRunResult, PatternMetadata
from . import register_pattern


METADATA = PatternMetadata(
    name="learning_adaptation",
    summary="Adjusts strategy weights based on feedback to improve over time.",
    chapter="Chapter 9",
    part="Part Two",
    tags=["learning", "feedback"],
)


def build_agent(config: AgentConfig) -> Agent:
    llm = resolve_llm(config)
    policy = {"explore": 0.4, "exploit": 0.6}

    def choose_strategy(state):
        mode = "exploit" if policy["exploit"] >= policy["explore"] else "explore"
        state.scratchpad["strategy_mode"] = mode
        state.transcript.append({"step": "choose_strategy", "content": f"Mode: {mode}"})
        return state

    def respond(state):
        mode = state.scratchpad["strategy_mode"]
        prompt = (
            f"Respond in {mode} mode.\n"
            f"User request: {state.input_text}\n"
            "Exploit = direct answer; Explore = propose alternative ideas."
        )
        answer = llm.generate(prompt, config=config, context={"intent": mode})
        state.output = answer
        state.transcript.append({"step": "respond", "content": answer})
        return state

    def learn(state):
        feedback = float(state.context.get("feedback_score", 0.7))
        if state.scratchpad["strategy_mode"] == "exploit":
            policy["exploit"] = 0.8 * policy["exploit"] + 0.2 * feedback
        else:
            policy["explore"] = 0.8 * policy["explore"] + 0.2 * feedback
        normalized_sum = policy["explore"] + policy["exploit"]
        policy["explore"] /= normalized_sum
        policy["exploit"] /= normalized_sum
        state.transcript.append({"step": "learn", "content": f"Policy: {policy}"})
        return state

    return Agent(
        name=METADATA.name,
        llm=llm,
        steps=[choose_strategy, respond, learn],
        config=config,
    )


def demo(demo_config: DemoConfig) -> AgentRunResult:
    context = {"demo": True, "feedback_score": 0.85}
    agent = build_agent(demo_config.agent_config)
    return agent.run(demo_config.input_text, context=context)


register_pattern(METADATA, build_agent, demo)
