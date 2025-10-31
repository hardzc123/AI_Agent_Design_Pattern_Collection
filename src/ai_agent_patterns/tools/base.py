from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, Protocol


class ToolContext(Protocol):
    def get(self, key: str, default: Any = None) -> Any:
        ...


@dataclass
class Tool:
    name: str
    description: str
    handler: Callable[[str, ToolContext], str]

    def run(self, input_text: str, context: ToolContext) -> str:
        return self.handler(input_text, context)
