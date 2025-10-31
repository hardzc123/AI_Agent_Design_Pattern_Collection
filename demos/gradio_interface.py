from __future__ import annotations

import json
from typing import Any, Dict

import gradio as gr

from ai_agent_patterns import AgentConfig, DemoConfig, registry
from .smart_support_triage import load_tickets, run_smart_support_demo


def _run_pattern(pattern: str, prompt: str, provider: str, model: str, mock: bool) -> Dict[str, Any]:
    definition = registry.get(pattern)
    agent_config = AgentConfig(provider="mock" if mock else provider, model=model)
    demo_config = DemoConfig(agent_config=agent_config, input_text=prompt or "Help the customer.")
    result = definition.demo(demo_config)
    return {
        "output": result.output,
        "transcript": json.dumps(result.transcript, indent=2),
        "markdown": result.to_markdown(),
    }


def _run_support(ticket_id: str, provider: str, model: str, mock: bool) -> Dict[str, Any]:
    result = run_smart_support_demo(ticket_id, mock=mock, provider=provider or "mock")
    return {
        "markdown": result.to_markdown(),
        "json": json.dumps(result.to_dict(), indent=2),
    }


def create_app() -> gr.Blocks:
    tickets = load_tickets()
    ticket_options = list(tickets.keys())

    with gr.Blocks(title="AI Agent Design Pattern Collection") as demo:
        gr.Markdown(
            "# AI Agent Design Pattern Collection\n"
            "Experiment with key patterns and explore a full Smart Support triage workflow."
        )

        with gr.Tab("Pattern Playground"):
            pattern_dropdown = gr.Dropdown(
                choices=sorted(list(registry.patterns())),
                value="prompt_chaining",
                label="Pattern",
            )
            prompt_box = gr.Textbox(
                label="Input",
                value="Summarize the key steps to onboard a new enterprise customer.",
                lines=4,
            )
            provider = gr.Textbox(label="Provider", value="mock")
            model = gr.Textbox(label="Model", value="mock-llm")
            mock_checkbox = gr.Checkbox(label="Use Mock LLM", value=True)
            run_button = gr.Button("Run Pattern")
            output_md = gr.Markdown(label="Result")
            transcript_json = gr.JSON(label="Transcript")

            def on_run(pattern, prompt, provider, model, mock):
                result = _run_pattern(pattern, prompt, provider, model, mock)
                return result["markdown"], result["transcript"]

            run_button.click(
                on_run,
                inputs=[pattern_dropdown, prompt_box, provider, model, mock_checkbox],
                outputs=[output_md, transcript_json],
            )

        with gr.Tab("Smart Support Triage"):
            ticket_choice = gr.Dropdown(choices=ticket_options, value=ticket_options[0], label="Ticket ID")
            provider2 = gr.Textbox(label="Provider", value="mock")
            model2 = gr.Textbox(label="Model", value="mock-llm")
            mock_checkbox2 = gr.Checkbox(label="Use Mock LLM", value=True)
            run_support_button = gr.Button("Run Smart Support Agent")
            support_md = gr.Markdown(label="Summary")
            support_json = gr.JSON(label="Details")

            def on_support(ticket_id, provider, model, mock):
                result = _run_support(ticket_id, provider, model, mock)
                return result["markdown"], result["json"]

            run_support_button.click(
                on_support,
                inputs=[ticket_choice, provider2, model2, mock_checkbox2],
                outputs=[support_md, support_json],
            )

    return demo


if __name__ == "__main__":
    create_app().launch()
