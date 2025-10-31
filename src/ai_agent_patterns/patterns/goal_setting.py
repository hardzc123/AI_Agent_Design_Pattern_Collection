from __future__ import annotations

from typing import List

from ..config import AgentConfig, DemoConfig
from ..core import Agent
from ..factory import resolve_llm
from ..types import AgentRunResult, PatternMetadata
from . import register_pattern


METADATA = PatternMetadata(
    name="goal_setting",
    summary="Captures goals, milestones, and monitors completion checkpoints.",
    chapter="Chapter 11",
    part="Part Two",
    tags=["goals", "monitoring"],
)


def build_agent(config: AgentConfig) -> Agent:
    llm = resolve_llm(config)
    goals: List[str] = []
    checkpoints = {}

    def parse_goals(state):
        raw_goals = [item.strip() for item in state.input_text.split("\n") if item.strip()]
        goals.clear()
        goals.extend(raw_goals)
        state.transcript.append({"step": "parse_goals", "content": ", ".join(goals)})
        return state

    def generate_checkpoints(state):
        for goal in goals:
            prompt = f"Break down goal into 3 checkpoints:\nGoal: {goal}"
            checkpoints[goal] = llm.generate(prompt, config=config, context={"intent": "plan"})
        combined = "\n".join(f"{goal}: {checkpoints[goal]}" for goal in goals)
        state.scratchpad["checkpoints"] = combined
        state.transcript.append({"step": "generate_checkpoints", "content": combined})
        return state

    def monitor(state):
        progress = "\n".join(f"{goal}: {checkpoints[goal].splitlines()[0]}" for goal in goals)
        state.output = f"Goals tracked: {len(goals)}\n{progress}"
        state.transcript.append({"step": "monitor", "content": state.output})
        return state

    return Agent(
        name=METADATA.name,
        llm=llm,
        steps=[parse_goals, generate_checkpoints, monitor],
        config=config,
    )


def demo(demo_config: DemoConfig) -> AgentRunResult:
    sample_goals = "Improve onboarding docs\nReduce ticket backlog"
    agent = build_agent(demo_config.agent_config)
    return agent.run(sample_goals, context={"demo": True})


register_pattern(METADATA, build_agent, demo)
