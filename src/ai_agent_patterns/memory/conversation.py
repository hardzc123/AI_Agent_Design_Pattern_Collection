from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

from .base import MemoryStore


@dataclass
class ConversationBuffer(MemoryStore):
    capacity: int = 20
    _items: List[Dict[str, Any]] = field(default_factory=list)

    def add(self, item: Dict[str, Any]) -> None:
        self._items.append(item)
        if len(self._items) > self.capacity:
            self._items.pop(0)

    def fetch(self, limit: int = 5) -> List[Dict[str, Any]]:
        return self._items[-limit:]
