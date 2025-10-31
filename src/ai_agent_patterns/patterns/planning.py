from __future__ import annotations

from ..config import AgentConfig, DemoConfig
from ..core import Agent
from ..factory import resolve_llm
from ..types import AgentRunResult, PatternMetadata
from ..workflows.planner import plan_execution_step, plan_generation_step
from . import register_pattern


METADATA = PatternMetadata(
    name="planning",
    summary="Creates explicit action plans and executes them step-by-step.",
    chapter="Chapter 6",
    part="Part One",
    tags=["planning", "execution"],
)


def build_agent(config: AgentConfig) -> Agent:
    llm = resolve_llm(config)

    plan_step = plan_generation_step(llm)

    def executor(step_description: str, state):
        return llm.generate(
            f"Perform plan step: {step_description}\nContext: {state.input_text}",
            config=config,
            context={"intent": "summarize"},
        )

    execute_step = plan_execution_step(executor)

    return Agent(
        name=METADATA.name,
        llm=llm,
        steps=[plan_step, execute_step],
        config=config,
    )


def demo(demo_config: DemoConfig) -> AgentRunResult:
    agent = build_agent(demo_config.agent_config)
    return agent.run(demo_config.input_text, context={"demo": True})


register_pattern(METADATA, build_agent, demo)
