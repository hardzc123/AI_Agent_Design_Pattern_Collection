from __future__ import annotations

from .config import AgentConfig
from .llm import LiteLLMClient, MockLLMClient, OpenAILLMClient
from .types import LLMClient


def resolve_llm(config: AgentConfig) -> LLMClient:
    provider = config.provider.lower()
    if provider in {"mock", "test"}:
        return MockLLMClient()
    if provider == "openai":
        return OpenAILLMClient(model=config.model)
    if provider in {"litellm", "router"}:
        return LiteLLMClient(model=config.model)
    raise ValueError(f"Unsupported LLM provider: {config.provider}")
