from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

from ..config import AgentConfig, DemoConfig
from ..core import Agent
from ..factory import resolve_llm
from ..types import AgentRunResult, PatternMetadata
from . import register_pattern


METADATA = PatternMetadata(
    name="parallelization",
    summary="Executes independent sub-tasks concurrently and merges the results.",
    chapter="Chapter 3",
    part="Part One",
    tags=["parallel", "efficiency"],
)


def build_agent(config: AgentConfig) -> Agent:
    llm = resolve_llm(config)

    def fan_out(state):
        tasks = [chunk.strip() for chunk in state.input_text.split(";") if chunk.strip()]
        if not tasks:
            tasks = [state.input_text]
        state.scratchpad["fanout_tasks"] = tasks
        state.transcript.append({"step": "fan_out", "content": f"{len(tasks)} tasks spawned"})
        return state

    def execute_parallel(state):
        tasks = state.scratchpad["fanout_tasks"]
        with ThreadPoolExecutor(max_workers=min(len(tasks), 4)) as executor:
            outputs = list(
                executor.map(
                    lambda task: llm.generate(
                        f"Address sub-task: {task}", config=config, context={"intent": "summarize"}
                    ),
                    tasks,
                )
            )
        state.scratchpad["parallel_outputs"] = outputs
        state.transcript.append({"step": "execute_parallel", "content": "\n".join(outputs)})
        return state

    def aggregate(state):
        outputs = state.scratchpad.get("parallel_outputs", [])
        aggregated = "\n".join(outputs)
        state.output = aggregated
        state.transcript.append({"step": "aggregate", "content": aggregated})
        return state

    return Agent(
        name=METADATA.name,
        llm=llm,
        steps=[fan_out, execute_parallel, aggregate],
        config=config,
    )


def demo(demo_config: DemoConfig) -> AgentRunResult:
    agent = build_agent(demo_config.agent_config)
    return agent.run(demo_config.input_text, context={"demo": True})


register_pattern(METADATA, build_agent, demo)
