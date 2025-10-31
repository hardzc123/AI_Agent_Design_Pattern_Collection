from __future__ import annotations

import pytest

from ai_agent_patterns import AgentConfig, DemoConfig, registry


@pytest.mark.parametrize("pattern_name", sorted(list(registry.patterns())))
def test_pattern_demo_runs(pattern_name: str) -> None:
    definition = registry.get(pattern_name)
    demo_config = DemoConfig(agent_config=AgentConfig(), input_text="Provide support guidance.")
    result = definition.demo(demo_config)
    assert isinstance(result.output, str)
    assert result.output != ""
    assert isinstance(result.transcript, list)
