from __future__ import annotations

from typing import List, Tuple

from ..config import AgentConfig, DemoConfig
from ..core import Agent
from ..factory import resolve_llm
from ..types import AgentRunResult, PatternMetadata
from . import register_pattern


METADATA = PatternMetadata(
    name="prioritization",
    summary="Scores and orders tasks to maximize impact under constraints.",
    chapter="Chapter 20",
    part="Part Four",
    tags=["prioritization", "ranking"],
)


def build_agent(config: AgentConfig) -> Agent:
    llm = resolve_llm(config)

    def parse_tasks(state):
        tasks = [line.strip() for line in state.input_text.split("\n") if line.strip()]
        state.scratchpad["tasks"] = tasks
        state.transcript.append({"step": "parse_tasks", "content": f"{len(tasks)} tasks parsed"})
        return state

    def score_tasks(state):
        def score(task: str) -> float:
            base = 1.0
            if any(word in task.lower() for word in ["outage", "critical", "p0"]):
                base += 2.0
            if any(word in task.lower() for word in ["vip", "executive"]):
                base += 1.0
            if "feature" in task.lower():
                base += 0.3
            return base

        scored: List[Tuple[str, float]] = [(task, score(task)) for task in state.scratchpad["tasks"]]
        scored.sort(key=lambda pair: pair[1], reverse=True)
        state.scratchpad["scored_tasks"] = scored
        transcript_lines = [f"{task} -> {value:.2f}" for task, value in scored]
        state.transcript.append({"step": "score_tasks", "content": "\n".join(transcript_lines)})
        return state

    def summarize(state):
        lines = "\n".join(f"{idx+1}. {task}" for idx, (task, _score) in enumerate(state.scratchpad["scored_tasks"]))
        prompt = f"Given prioritized tasks:\n{lines}\nProvide concise summary plan."
        summary = llm.generate(prompt, config=config, context={"intent": "summarize"})
        state.output = f"{lines}\n\nSummary:\n{summary}"
        state.transcript.append({"step": "summary", "content": state.output})
        return state

    return Agent(
        name=METADATA.name,
        llm=llm,
        steps=[parse_tasks, score_tasks, summarize],
        config=config,
    )


def demo(demo_config: DemoConfig) -> AgentRunResult:
    sample_input = "Resolve P0 outage for Acme\nPrepare executive briefing\nReview feature request backlog"
    agent = build_agent(demo_config.agent_config)
    return agent.run(sample_input, context={"demo": True})


register_pattern(METADATA, build_agent, demo)
