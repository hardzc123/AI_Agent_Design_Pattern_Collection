from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from ..config import AgentConfig, DemoConfig
from ..core import Agent
from ..factory import resolve_llm
from ..types import AgentRunResult, PatternMetadata
from . import register_pattern


@dataclass
class MockMCPServer:
    resources: Dict[str, str]

    def fetch(self, uri: str) -> str:
        return self.resources.get(uri, "Resource not found.")


METADATA = PatternMetadata(
    name="mcp",
    summary="Demonstrates Model Context Protocol style resource access.",
    chapter="Chapter 10",
    part="Part Two",
    tags=["mcp", "tools"],
)


def build_agent(config: AgentConfig) -> Agent:
    llm = resolve_llm(config)
    server = MockMCPServer(
        resources={
            "kb://faq/billing": "Billing FAQ — refunds processed within 5 business days.",
            "kb://runbook/outage": "Incident Runbook: gather logs, notify on-call, start bridge.",
        }
    )

    def request_resource(state):
        uri = state.context.get("resource_uri", "kb://faq/billing")
        payload = server.fetch(uri)
        state.scratchpad["resource_payload"] = payload
        state.transcript.append({"step": "mcp_fetch", "content": f"{uri} -> {payload}"})
        return state

    def respond(state):
        payload = state.scratchpad["resource_payload"]
        prompt = (
            f"Context resource:\n{payload}\n\nUser question: {state.input_text}\n"
            "Craft grounded answer."
        )
        answer = llm.generate(prompt, config=config, context={"intent": "summarize"})
        state.output = answer
        state.transcript.append({"step": "mcp_answer", "content": answer})
        return state

    return Agent(
        name=METADATA.name,
        llm=llm,
        steps=[request_resource, respond],
        config=config,
    )


def demo(demo_config: DemoConfig) -> AgentRunResult:
    context = {"demo": True, "resource_uri": "kb://runbook/outage"}
    agent = build_agent(demo_config.agent_config)
    return agent.run(demo_config.input_text, context=context)


register_pattern(METADATA, build_agent, demo)
