from __future__ import annotations

from typing import Any, Dict, List, Protocol


class MemoryStore(Protocol):
    def add(self, item: Dict[str, Any]) -> None:
        ...

    def fetch(self, limit: int = 5) -> List[Dict[str, Any]]:
        ...
