from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Dict

from .base import Tool

FAKE_FAQ: Dict[str, str] = {
    "billing": "Billing questions are handled within 1 business day. Contact billing@support.local.",
    "outage": "For outages, escalate to the on-call engineer and initiate incident response.",
    "feature request": "Collect requirements and log them in the product backlog.",
}


def calculator_handler(expression: str, context) -> str:
    try:
        value = eval(expression, {"__builtins__": {"pow": pow}}, {"math": math})
    except Exception as exc:  # pragma: no cover - defensive
        return f"Calculator error: {exc}"
    return f"Result: {value}"


def faq_handler(question: str, context) -> str:
    lowered = question.lower()
    for key, answer in FAKE_FAQ.items():
        if key in lowered:
            return answer
    return "No FAQ entry found; escalate to human."


def file_read_handler(path: str, context) -> str:
    root = Path(context.get("root_dir", "."))
    target = (root / path).resolve()
    if not target.exists():
        return f"File not found: {target}"
    if target.is_dir():
        return f"{target} is a directory."
    return target.read_text(encoding="utf-8")[:2000]


CALCULATOR_TOOL = Tool(
    name="calculator",
    description="Evaluate arithmetic expressions.",
    handler=calculator_handler,
)

FAQ_TOOL = Tool(
    name="faq_lookup",
    description="Search the customer FAQ knowledge base.",
    handler=faq_handler,
)


class FileReadTool(Tool):
    def __init__(self) -> None:
        super().__init__(
            name="file_read",
            description="Read a local file (sandboxed).",
            handler=file_read_handler,
        )
