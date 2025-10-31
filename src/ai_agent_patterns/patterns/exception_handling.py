from __future__ import annotations

from ..config import AgentConfig, DemoConfig
from ..core import Agent
from ..factory import resolve_llm
from ..types import AgentRunResult, PatternMetadata
from . import register_pattern


METADATA = PatternMetadata(
    name="exception_handling",
    summary="Detects failures and applies recovery strategies.",
    chapter="Chapter 12",
    part="Part Three",
    tags=["resilience", "recovery"],
)


def build_agent(config: AgentConfig) -> Agent:
    llm = resolve_llm(config)

    def risky_operation(state):
        text = state.input_text.lower()
        if "fail" in text:
            raise RuntimeError("Simulated failure while calling external tool.")
        state.scratchpad["risky_output"] = "Operation succeeded."
        state.transcript.append({"step": "risky_operation", "content": "success"})
        return state

    def recover_step(state):
        try:
            return risky_operation(state)
        except Exception as exc:  # pragma: no cover - deterministic
            state.transcript.append({"step": "error_detected", "content": str(exc)})
            fallback = llm.generate(
                f"Provide fallback guidance for error: {exc}\nOriginal request: {state.input_text}",
                config=config,
                context={"intent": "summarize"},
            )
            state.scratchpad["risky_output"] = fallback
            state.transcript.append({"step": "fallback", "content": fallback})
            return state

    def finalize(state):
        result = state.scratchpad.get("risky_output", "No result.")
        state.output = result
        state.transcript.append({"step": "finalize", "content": result})
        return state

    return Agent(
        name=METADATA.name,
        llm=llm,
        steps=[recover_step, finalize],
        config=config,
    )


def demo(demo_config: DemoConfig) -> AgentRunResult:
    agent = build_agent(demo_config.agent_config)
    # Force failure path for demonstration.
    return agent.run("Simulate fail case to trigger recovery.", context={"demo": True})


register_pattern(METADATA, build_agent, demo)
