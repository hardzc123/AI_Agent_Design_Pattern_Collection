from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, Optional

from .base import Tool


@dataclass
class ToolRegistry:
    tools: Dict[str, Tool] = field(default_factory=dict)

    def register(self, tool: Tool) -> None:
        self.tools[tool.name] = tool

    def get(self, name: str) -> Optional[Tool]:
        return self.tools.get(name)

    def run(self, name: str, input_text: str, context) -> str:
        tool = self.get(name)
        if tool is None:
            raise KeyError(f"Tool '{name}' not found.")
        return tool.run(input_text, context)

    def list(self) -> Iterable[str]:
        return self.tools.keys()
