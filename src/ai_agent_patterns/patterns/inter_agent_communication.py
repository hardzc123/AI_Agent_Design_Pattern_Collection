from __future__ import annotations

from collections import defaultdict

from ..config import AgentConfig, DemoConfig
from ..core import Agent
from ..factory import resolve_llm
from ..types import AgentRunResult, PatternMetadata
from . import register_pattern


METADATA = PatternMetadata(
    name="inter_agent_communication",
    summary="Illustrates agent-to-agent messaging over a shared bus.",
    chapter="Chapter 15",
    part="Part Four",
    tags=["communication", "multi-agent"],
)


def build_agent(config: AgentConfig) -> Agent:
    llm = resolve_llm(config)

    def message_bus(state):
        bus = defaultdict(list)
        roles = ["planner", "executor", "reviewer"]
        previous = state.input_text
        for role in roles:
            prompt = (
                f"Role: {role}\n"
                f"Incoming messages:\n{previous}\n"
                "Craft your broadcast update."
            )
            message = llm.generate(prompt, config=config, context={"intent": role})
            bus[role].append(message)
            previous = message
        transcript = "\n".join(f"{role.upper()}: {msgs[0]}" for role, msgs in bus.items())
        state.output = transcript
        state.transcript.append({"step": "message_bus", "content": transcript})
        return state

    return Agent(
        name=METADATA.name,
        llm=llm,
        steps=[message_bus],
        config=config,
    )


def demo(demo_config: DemoConfig) -> AgentRunResult:
    agent = build_agent(demo_config.agent_config)
    input_text = demo_config.input_text or "Sync on product launch checklist."
    return agent.run(input_text, context={"demo": True})


register_pattern(METADATA, build_agent, demo)
