from __future__ import annotations

from ai_agent_patterns.memory import KeywordVectorMemory


def test_keyword_vector_memory_similarity() -> None:
    memory = KeywordVectorMemory()
    memory.add({"content": "outage incident response playbook"})
    memory.add({"content": "billing dispute resolution guide"})

    results = memory.query("How do I respond to an outage?")
    assert results
    top_item, score = results[0]
    assert "outage" in top_item["content"]
    assert score > 0
