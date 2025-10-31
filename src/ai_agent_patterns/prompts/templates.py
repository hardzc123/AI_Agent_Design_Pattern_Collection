from __future__ import annotations

from typing import Dict


def prompt_chain_template(topic: str) -> str:
    return (
        "Task: produce a refined answer.\n"
        f"Topic: {topic}\n"
        "Steps:\n"
        "1. Draft an initial answer.\n"
        "2. Critique weaknesses.\n"
        "3. Produce improved final answer."
    )


def critique_prompt(draft: str) -> str:
    return f"Critique the following draft answer:\n---\n{draft}\n---\nList weaknesses."


def final_answer_prompt(draft: str, critique: str) -> str:
    return (
        "Improve the answer by addressing critique.\n"
        f"Draft:\n{draft}\n"
        f"Critique:\n{critique}\n"
        "Return final polished answer."
    )


def routing_prompt(question: str) -> str:
    return (
        "You are a router. Decide which specialist should handle the request.\n"
        f"Question: {question}\n"
        "Options: billing, technical, general, escalate_to_specialist.\n"
        "Respond with decision keyword."
    )


def compile_plan_prompt(goal: str) -> str:
    return (
        f"Create a concise 3-step plan to accomplish: {goal}\n"
        "Return numbered list."
    )
