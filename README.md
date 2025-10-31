# AI Agent Design Pattern Collection

Curated implementations of 21 AI agent design patterns inspired by the Agentic Design Patterns reference. The project delivers runnable Python modules, tests, and demos (CLI + Gradio) alongside a real-world Smart Support triage scenario.

## Quick Start
```bash
make install            # install runtime dependencies in .venv
make demo               # run prompt chaining demo with mock LLM
make gradio             # launch interactive playground on http://localhost:7860
```

Provide live LLM access by setting `OPENAI_API_KEY` (or other provider env vars) and running with `--provider openai`.

## Repository Tour
- `src/ai_agent_patterns/` — package containing reusable building blocks (LLM adapters, memory, tools, workflows) and one module per pattern.
- `demos/` — CLI driver, Gradio interface, and Smart Support triage workflow.
- `docs/` — specification, pattern overviews, and deployment guide.
- `tests/` — Pytest suite ensuring factories and utilities behave deterministically with the mock LLM.
- `huggingface_space/` — ready-to-deploy wrapper for Hugging Face Spaces.

## Pattern Catalog
Patterns are grouped into four parts mirroring the original text. Each pattern exports metadata, an `Agent` factory, and a `demo` helper.

| Part | Chapters | Highlights |
| --- | --- | --- |
| Part One | Prompt Chaining · Routing · Parallelization · Reflection · Tool Use · Planning · Multi-Agent | Foundational prompting and orchestration techniques |
| Part Two | Memory Management · Learning & Adaptation · MCP · Goal Setting & Monitoring | State, feedback, and protocol integrations |
| Part Three | Exception Handling & Recovery · Human-in-the-Loop · Knowledge Retrieval (RAG) | Resilience and grounding |
| Part Four | Inter-Agent Communication · Resource-Aware Optimization · Reasoning Techniques · Guardrails · Evaluation & Monitoring · Prioritization · Exploration & Discovery | Advanced coordination, safety, and optimization |

View concise summaries under `docs/patterns/part_*.md`.

## Demos
- **CLI**: `python -m demos.run_pattern --pattern routing --input "Invoice discrepancy for enterprise plan" --mock`
- **Gradio**: Run `make gradio` then open the browser UI to explore patterns or triage real support tickets via the Smart Support tab.
- **Smart Support Scenario**: `python -m demos.smart_support_triage` (import and call `run_smart_support_demo(ticket_id="TCK-101")` within Python). Uses routing, planning, retrieval, reflection, and prioritization to produce action plans and answers.

## Deployment
- **Docker**: `docker build -t ai-agent-patterns .` then `docker run -p 7860:7860 ai-agent-patterns`
- **Hugging Face Spaces**: copy `huggingface_space/`, set secrets for API keys, entrypoint `huggingface_space/app.py`.
- More details in `docs/deployment.md`.

## Development
```bash
make install-dev
make lint
make test
```

All patterns default to a deterministic `MockLLMClient`, ensuring tests and demos run without external API calls. Configure providers via `AgentConfig` when integrating real models.

## References
1. https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system
2. https://docs.google.com/document/d/1rsaK53T3Lg5KoGwvf8ukOUvbELRtH-V0LnOIFDxBryE/preview
3. https://github.com/ginobefun/agentic-design-patterns-cn
