from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

from ai_agent_patterns import AgentConfig, registry

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "support_tickets.json"


@dataclass
class SmartSupportResult:
    ticket_id: str
    route_decision: str
    plan: str
    answer: str
    priority: str
    transcript: Dict[str, Dict[str, str]]

    def to_markdown(self) -> str:
        return (
            f"### Ticket {self.ticket_id}\n"
            f"- **Route**: {self.route_decision}\n"
            f"- **Priority**: {self.priority}\n"
            f"- **Plan**:\n{self.plan}\n"
            f"- **Answer**:\n{self.answer}\n"
        )

    def to_dict(self) -> Dict[str, str]:
        return {
            "ticket_id": self.ticket_id,
            "route_decision": self.route_decision,
            "plan": self.plan,
            "answer": self.answer,
            "priority": self.priority,
            "transcript": self.transcript,
        }


def load_tickets() -> Dict[str, Dict[str, str]]:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    return {ticket["id"]: ticket for ticket in data}


def run_smart_support_demo(ticket_id: str, *, mock: bool = True, provider: str = "mock") -> SmartSupportResult:
    tickets = load_tickets()
    ticket = tickets[ticket_id]
    prompt = f"{ticket['subject']}\n\n{ticket['body']}"
    context = {"ticket": ticket, "demo": True}
    agent_config = AgentConfig(provider="mock" if mock else provider)

    routing_definition = registry.get("routing")
    routing_agent = routing_definition.build_agent(agent_config)
    routing_result = routing_agent.run(prompt, context=context)
    route_decision = routing_result.transcript[-1]["content"]

    planning_definition = registry.get("planning")
    planning_agent = planning_definition.build_agent(agent_config)
    plan_result = planning_agent.run(prompt, context=context)

    rag_definition = registry.get("knowledge_retrieval")
    rag_agent = rag_definition.build_agent(agent_config)
    rag_result = rag_agent.run(prompt, context=context)

    reflection_definition = registry.get("reflection")
    reflection_agent = reflection_definition.build_agent(agent_config)
    answer_result = reflection_agent.run(prompt + "\n\n" + rag_result.output, context=context)

    priority_definition = registry.get("prioritization")
    priority_agent = priority_definition.build_agent(agent_config)
    priority_input = "\n".join(
        [
            "Resolve production outage now",
            "Send acknowledgement email",
            f"Follow up with {ticket['customer']}",
        ]
    )
    priority_result = priority_agent.run(priority_input, context=context)
    priority_line = priority_result.output.splitlines()[0]

    transcript = {
        "routing": {"output": routing_result.output, "route": route_decision},
        "plan": {"output": plan_result.output},
        "rag": {"output": rag_result.output},
        "answer": {"output": answer_result.output},
        "priority": {"output": priority_result.output},
    }

    return SmartSupportResult(
        ticket_id=ticket_id,
        route_decision=route_decision,
        plan=plan_result.output,
        answer=answer_result.output,
        priority=priority_line,
        transcript=transcript,
    )


if __name__ == "__main__":
    result = run_smart_support_demo("TCK-101")
    print(result.to_markdown())
