from __future__ import annotations

from ..config import AgentConfig, DemoConfig
from ..core import Agent
from ..factory import resolve_llm
from ..memory import ConversationBuffer, KeywordVectorMemory
from ..types import AgentRunResult, PatternMetadata
from . import register_pattern


METADATA = PatternMetadata(
    name="memory_management",
    summary="Balances short-term and long-term memory for contextual grounding.",
    chapter="Chapter 8",
    part="Part Two",
    tags=["memory", "context"],
)


def build_agent(config: AgentConfig) -> Agent:
    llm = resolve_llm(config)
    conversation = ConversationBuffer()
    vector_memory = KeywordVectorMemory()

    def ingest(state):
        entry = {"role": "user", "content": state.input_text}
        conversation.add(entry)
        vector_memory.add(entry)
        state.transcript.append({"step": "memory_ingest", "content": state.input_text})
        return state

    def recall(state):
        recent = conversation.fetch(limit=3)
        similar = [item for item, _score in vector_memory.query(state.input_text, limit=2)]
        context_blocks = [item["content"] for item in recent + similar]
        context_text = "\n".join(context_blocks[-5:])
        state.scratchpad["memory_context"] = context_text
        state.transcript.append({"step": "memory_recall", "content": context_text})
        return state

    def respond(state):
        context_snippet = state.scratchpad.get("memory_context", "")
        prompt = (
            f"Leverage context to answer.\n"
            f"Context:\n{context_snippet}\n"
            f"Question: {state.input_text}"
        )
        answer = llm.generate(prompt, config=config, context={"intent": "summarize"})
        conversation.add({"role": "assistant", "content": answer})
        state.output = answer
        state.transcript.append({"step": "memory_response", "content": answer})
        return state

    return Agent(
        name=METADATA.name,
        llm=llm,
        steps=[ingest, recall, respond],
        config=config,
    )


def demo(demo_config: DemoConfig) -> AgentRunResult:
    agent = build_agent(demo_config.agent_config)
    return agent.run(demo_config.input_text, context={"demo": True})


register_pattern(METADATA, build_agent, demo)
