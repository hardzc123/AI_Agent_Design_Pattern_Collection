from __future__ import annotations

from ..config import AgentConfig, DemoConfig
from ..core import Agent
from ..factory import resolve_llm
from ..types import AgentRunResult, PatternMetadata
from ..workflows.router import intent_router_step
from . import register_pattern


METADATA = PatternMetadata(
    name="routing",
    summary="Directs user intents to the best-suited specialist pipeline.",
    chapter="Chapter 2",
    part="Part One",
    tags=["routing", "dispatch"],
)

SPECIALISTS = {
    "billing": "Billing Specialist: Provide invoice clarification and payment steps.",
    "technical": "Technical Specialist: Perform diagnostics and suggest fixes.",
    "general": "General Support: Offer friendly response and triage guidance.",
    "escalate": "Escalation Manager: Collect details and escalate incident.",
}


def build_agent(config: AgentConfig) -> Agent:
    llm = resolve_llm(config)

    route_step = intent_router_step(
        llm,
        {
            "billing": "billing",
            "invoice": "billing",
            "technical": "technical",
            "outage": "escalate",
            "escalate": "escalate",
            "default": "general",
        },
    )

    def specialist_step(state):
        decision = state.scratchpad.get("route_decision", "general")
        playbook = SPECIALISTS.get(decision, SPECIALISTS["general"])
        state.transcript.append({"step": "specialist", "content": playbook})
        state.output = f"{decision}: {playbook}"
        return state

    return Agent(
        name=METADATA.name,
        llm=llm,
        steps=[route_step, specialist_step],
        config=config,
    )


def demo(demo_config: DemoConfig) -> AgentRunResult:
    agent = build_agent(demo_config.agent_config)
    return agent.run(demo_config.input_text, context={"demo": True})


register_pattern(METADATA, build_agent, demo)
