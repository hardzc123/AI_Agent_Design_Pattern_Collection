from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, Iterable

from ..config import AgentConfig, DemoConfig
from ..core import Agent
from ..types import AgentRunResult, PatternMetadata


@dataclass
class PatternDefinition:
    metadata: PatternMetadata
    build_agent: Callable[[AgentConfig], Agent]
    demo: Callable[[DemoConfig], AgentRunResult]


class PatternRegistry:
    def __init__(self) -> None:
        self._definitions: Dict[str, PatternDefinition] = {}

    def register(self, definition: PatternDefinition) -> None:
        key = definition.metadata.name
        self._definitions[key] = definition

    def get(self, name: str) -> PatternDefinition:
        try:
            return self._definitions[name]
        except KeyError as exc:
            raise KeyError(f"Pattern '{name}' not found.") from exc

    def patterns(self) -> Iterable[str]:
        return self._definitions.keys()

    def metadata(self) -> Iterable[PatternMetadata]:
        return (definition.metadata for definition in self._definitions.values())


registry = PatternRegistry()


def register_pattern(metadata: PatternMetadata, build_agent, demo) -> None:
    registry.register(PatternDefinition(metadata=metadata, build_agent=build_agent, demo=demo))


# Import modules to trigger registration
from . import (  # noqa: E402,F401
    exception_handling,
    exploration_discovery,
    goal_setting,
    guardrails,
    human_in_loop,
    inter_agent_communication,
    knowledge_retrieval,
    learning_adaptation,
    mcp,
    memory_management,
    multi_agent,
    planning,
    parallelization,
    prioritization,
    prompt_chaining,
    reflection,
    resource_aware_optimization,
    routing,
    tool_use,
    evaluation_monitoring,
    reasoning,
)
