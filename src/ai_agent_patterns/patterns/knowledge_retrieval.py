from __future__ import annotations

from typing import List

from ..config import AgentConfig, DemoConfig
from ..core import Agent
from ..factory import resolve_llm
from ..memory import KeywordVectorMemory
from ..types import AgentRunResult, PatternMetadata
from . import register_pattern


KNOWLEDGE_BASE = [
    "Customers experiencing outages should follow the incident response runbook.",
    "Billing disputes are resolved within five business days after ticket submission.",
    "Multi-agent scheduling requires enabling the enterprise feature flag.",
]


METADATA = PatternMetadata(
    name="knowledge_retrieval",
    summary="Retrieves relevant knowledge snippets to ground LLM answers.",
    chapter="Chapter 14",
    part="Part Three",
    tags=["rag", "retrieval"],
)


def build_agent(config: AgentConfig) -> Agent:
    llm = resolve_llm(config)
    store = KeywordVectorMemory()
    for doc in KNOWLEDGE_BASE:
        store.add({"content": doc})

    def retrieve(state):
        results: List[str] = [item["content"] for item, _score in store.query(state.input_text, limit=2)]
        context_block = "\n".join(results)
        state.scratchpad["retrieved_context"] = context_block
        state.transcript.append({"step": "retrieve", "content": context_block})
        return state

    def respond(state):
        prompt = (
            f"Reference context:\n{state.scratchpad['retrieved_context']}\n\n"
            f"Question: {state.input_text}\n"
            "Provide grounded answer and cite snippets."
        )
        answer = llm.generate(prompt, config=config, context={"intent": "summarize"})
        state.output = answer
        state.transcript.append({"step": "answer", "content": answer})
        return state

    return Agent(
        name=METADATA.name,
        llm=llm,
        steps=[retrieve, respond],
        config=config,
    )


def demo(demo_config: DemoConfig) -> AgentRunResult:
    agent = build_agent(demo_config.agent_config)
    return agent.run(demo_config.input_text, context={"demo": True})


register_pattern(METADATA, build_agent, demo)
