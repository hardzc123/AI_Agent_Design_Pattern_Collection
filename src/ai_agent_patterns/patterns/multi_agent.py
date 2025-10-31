from __future__ import annotations

from ..config import AgentConfig, DemoConfig
from ..core import Agent
from ..factory import resolve_llm
from ..types import AgentRunResult, PatternMetadata
from . import register_pattern


METADATA = PatternMetadata(
    name="multi_agent",
    summary="Coordinates specialist agents via structured turn-taking.",
    chapter="Chapter 7",
    part="Part One",
    tags=["multi-agent", "coordination"],
)


def build_agent(config: AgentConfig) -> Agent:
    llm = resolve_llm(config)

    roles = [
        ("architect", "Outline solution approach and identify modules needed."),
        ("executor", "Translate the plan into concrete actions and highlights blockers."),
    ]

    def conversation(state):
        dialogue = []
        previous = state.input_text
        for round_idx in range(2):
            for role, instruction in roles:
                prompt = (
                    f"Role: {role}\n"
                    f"Instruction: {instruction}\n"
                    f"Previous context:\n{previous}\n"
                    "Respond with next message."
                )
                response = llm.generate(prompt, config=config, context={"intent": role})
                dialogue.append(f"{role.capitalize()}: {response}")
                previous = response
        transcript = "\n".join(dialogue)
        state.transcript.append({"step": "multi_agent_dialogue", "content": transcript})
        state.output = transcript
        return state

    return Agent(
        name=METADATA.name,
        llm=llm,
        steps=[conversation],
        config=config,
    )


def demo(demo_config: DemoConfig) -> AgentRunResult:
    agent = build_agent(demo_config.agent_config)
    return agent.run(demo_config.input_text, context={"demo": True})


register_pattern(METADATA, build_agent, demo)
