from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

from .base import MemoryStore


def tokenize(text: str) -> List[str]:
    tokens: List[str] = []
    for raw in text.split():
        cleaned = "".join(ch for ch in raw.lower() if ch.isalnum())
        if cleaned:
            tokens.append(cleaned)
    return tokens


def cosine_similarity(a: Counter[str], b: Counter[str]) -> float:
    shared = set(a) & set(b)
    numerator = sum(a[t] * b[t] for t in shared)
    denom_a = math.sqrt(sum(v * v for v in a.values()))
    denom_b = math.sqrt(sum(v * v for v in b.values()))
    if denom_a == 0 or denom_b == 0:
        return 0.0
    return numerator / (denom_a * denom_b)


@dataclass
class KeywordVectorMemory(MemoryStore):
    """Lightweight vector-like memory without external deps."""

    _items: List[Dict[str, Any]] = field(default_factory=list)

    def add(self, item: Dict[str, Any]) -> None:
        self._items.append(item)

    def fetch(self, limit: int = 5) -> List[Dict[str, Any]]:
        return self._items[-limit:]

    def query(self, text: str, limit: int = 3) -> List[Tuple[Dict[str, Any], float]]:
        query_vec = Counter(tokenize(text))
        scored = []
        for item in self._items:
            content = item.get("content", "")
            score = cosine_similarity(query_vec, Counter(tokenize(content)))
            scored.append((item, score))
        scored.sort(key=lambda pair: pair[1], reverse=True)
        return scored[:limit]
