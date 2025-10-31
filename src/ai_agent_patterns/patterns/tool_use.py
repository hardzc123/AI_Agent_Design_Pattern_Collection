from __future__ import annotations

from ..config import AgentConfig, DemoConfig
from ..core import Agent
from ..factory import resolve_llm
from ..tools import CALCULATOR_TOOL, FAQ_TOOL, FileReadTool, ToolRegistry
from ..types import AgentRunResult, PatternMetadata
from . import register_pattern


METADATA = PatternMetadata(
    name="tool_use",
    summary="Combines LLM reasoning with structured tool invocations.",
    chapter="Chapter 5",
    part="Part One",
    tags=["tools", "react"],
)


def build_agent(config: AgentConfig) -> Agent:
    llm = resolve_llm(config)
    registry = ToolRegistry()
    registry.register(CALCULATOR_TOOL)
    registry.register(FAQ_TOOL)
    registry.register(FileReadTool())

    def select_tool(state):
        text = state.input_text.lower()
        if any(keyword in text for keyword in ["add", "sum", "calculate", "multiply"]):
            tool = "calculator"
        elif any(keyword in text for keyword in ["invoice", "billing", "faq"]):
            tool = "faq_lookup"
        elif "show file" in text:
            tool = "file_read"
        else:
            tool = "faq_lookup"
        state.scratchpad["tool_name"] = tool
        state.transcript.append({"step": "select_tool", "content": tool})
        return state

    def invoke_tool(state):
        tool_name = state.scratchpad["tool_name"]
        output = registry.run(tool_name, state.input_text, state.context)
        state.scratchpad["tool_output"] = output
        state.transcript.append({"step": "invoke_tool", "content": output})
        return state

    def synthesize(state):
        summary = llm.generate(
            f"Summarize tool result for user query.\nQuery: {state.input_text}\nResult: {state.scratchpad['tool_output']}",
            config=config,
            context={"intent": "summarize"},
        )
        state.output = summary
        state.transcript.append({"step": "synthesize", "content": summary})
        return state

    return Agent(
        name=METADATA.name,
        llm=llm,
        steps=[select_tool, invoke_tool, synthesize],
        config=config,
    )


def demo(demo_config: DemoConfig) -> AgentRunResult:
    agent = build_agent(demo_config.agent_config)
    context = {"demo": True, "root_dir": "."}
    return agent.run(demo_config.input_text, context=context)


register_pattern(METADATA, build_agent, demo)
