from __future__ import annotations

from ai_agent_patterns.config import AgentConfig
from ai_agent_patterns.llm import MockLLMClient


def test_mock_llm_consistency() -> None:
    config = AgentConfig()
    client = MockLLMClient()
    out1 = client.generate("Summarize the outage.", config=config, context={"intent": "summarize"})
    out2 = client.generate("Summarize the outage.", config=config, context={"intent": "summarize"})
    assert out1 == out2
