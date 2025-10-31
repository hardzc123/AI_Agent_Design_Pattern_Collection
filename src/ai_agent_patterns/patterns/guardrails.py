from __future__ import annotations

from ..config import AgentConfig, DemoConfig
from ..core import Agent
from ..factory import resolve_llm
from ..types import AgentRunResult, PatternMetadata
from . import register_pattern


BLOCKED_KEYWORDS = {"hack", "exploit", "harm"}

METADATA = PatternMetadata(
    name="guardrails",
    summary="Applies safety checks and content filtering before responding.",
    chapter="Chapter 18",
    part="Part Four",
    tags=["safety", "guardrails"],
)


def build_agent(config: AgentConfig) -> Agent:
    llm = resolve_llm(config)

    def moderate(state):
        lowered = state.input_text.lower()
        violations = [word for word in BLOCKED_KEYWORDS if word in lowered]
        if violations:
            state.scratchpad["blocked"] = True
            warning = f"Request blocked due to policy: {', '.join(violations)}"
            state.output = warning
            state.transcript.append({"step": "moderate", "content": warning})
        else:
            state.scratchpad["blocked"] = False
            state.transcript.append({"step": "moderate", "content": "No issues detected."})
        return state

    def respond(state):
        if state.scratchpad.get("blocked"):
            return state
        answer = llm.generate(
            f"Comply with safety. Respond helpfully to: {state.input_text}",
            config=config,
            context={"intent": "safe"},
        )
        state.output = answer
        state.transcript.append({"step": "safe_answer", "content": answer})
        return state

    return Agent(
        name=METADATA.name,
        llm=llm,
        steps=[moderate, respond],
        config=config,
    )


def demo(demo_config: DemoConfig) -> AgentRunResult:
    agent = build_agent(demo_config.agent_config)
    return agent.run(demo_config.input_text, context={"demo": True})


register_pattern(METADATA, build_agent, demo)
