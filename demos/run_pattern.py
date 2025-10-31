from __future__ import annotations

import json
from typing import Optional

import typer
from rich.console import Console

from ai_agent_patterns import AgentConfig, DemoConfig, registry

console = Console()


def main(
    pattern: str = typer.Option(..., "--pattern", "-p", help="Pattern name, e.g. prompt_chaining"),
    input_text: Optional[str] = typer.Option(None, "--input", "-i", help="Override default input text"),
    provider: str = typer.Option("mock", help="LLM provider (mock, openai, litellm)"),
    model: str = typer.Option("mock-llm", help="LLM model identifier"),
    transcript_out: Optional[str] = typer.Option(None, "--transcript-out", help="Save transcript JSON"),
    list_patterns: bool = typer.Option(False, "--list", help="List available patterns and exit"),
) -> None:
    if list_patterns:
        for metadata in sorted(registry.metadata(), key=lambda m: m.name):
            console.print(f"[bold]{metadata.name}[/] — {metadata.summary}")
        raise typer.Exit()

    definition = registry.get(pattern)
    agent_config = AgentConfig(provider=provider, model=model)
    demo_config = DemoConfig(agent_config=agent_config, input_text=input_text or "Assist the user.")
    result = definition.demo(demo_config)
    console.print(result.to_markdown())
    if transcript_out:
        with open(transcript_out, "w", encoding="utf-8") as fh:
            json.dump(result.to_dict(), fh, indent=2)
        console.print(f"Transcript saved to {transcript_out}")


if __name__ == "__main__":
    typer.run(main)
