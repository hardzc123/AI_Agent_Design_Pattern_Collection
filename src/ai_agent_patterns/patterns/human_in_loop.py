from __future__ import annotations

from ..config import AgentConfig, DemoConfig
from ..core import Agent
from ..factory import resolve_llm
from ..types import AgentRunResult, PatternMetadata
from . import register_pattern


METADATA = PatternMetadata(
    name="human_in_loop",
    summary="Introduces human review checkpoints for critical decisions.",
    chapter="Chapter 13",
    part="Part Three",
    tags=["human-loop", "review"],
)


def build_agent(config: AgentConfig) -> Agent:
    llm = resolve_llm(config)

    def draft(state):
        answer = llm.generate(
            f"Draft response for: {state.input_text}",
            config=config,
            context={"intent": "draft"},
        )
        state.scratchpad["draft"] = answer
        state.transcript.append({"step": "draft", "content": answer})
        return state

    def request_review(state):
        reviewer_comment = state.context.get("human_feedback", "Looks good!")
        state.scratchpad["human_feedback"] = reviewer_comment
        state.transcript.append({"step": "human_review", "content": reviewer_comment})
        return state

    def apply_feedback(state):
        prompt = (
            f"Original draft:\n{state.scratchpad['draft']}\n"
            f"Reviewer feedback:\n{state.scratchpad['human_feedback']}\n"
            "Produce approved final response."
        )
        final = llm.generate(prompt, config=config, context={"intent": "improve"})
        state.output = final
        state.transcript.append({"step": "finalize", "content": final})
        return state

    return Agent(
        name=METADATA.name,
        llm=llm,
        steps=[draft, request_review, apply_feedback],
        config=config,
    )


def demo(demo_config: DemoConfig) -> AgentRunResult:
    context = {"demo": True, "human_feedback": "Adjust tone to be friendlier and add reassurance."}
    agent = build_agent(demo_config.agent_config)
    return agent.run(demo_config.input_text, context=context)


register_pattern(METADATA, build_agent, demo)
