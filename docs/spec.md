# AI Agent Design Pattern Collection — Technical Specification

## 1. Objectives
- Curate, implement, and document practical AI agent design patterns spanning four parts (21 chapters) derived from the referenced corpus.
- Provide runnable examples (CLI + notebooks) and an interactive Gradio UI showcasing at least two end-to-end agent workflows:
  - **Book-aligned baseline** mirroring the original example from the reference material.
  - **New real-world scenario** (e.g., Smart Support Triage) that highlights practical pain-point resolution.
- Deliver consistent abstractions, utilities, and testing to make patterns easy to reuse, extend, and deploy.
- Offer reproducible deployment paths for local usage and a Hugging Face Spaces-ready configuration for cloud execution.

## 2. Functional Requirements
- **Pattern Modules**: Each of the 21 patterns must live under `src/ai_agent_patterns/patterns/` and expose:
  - `metadata`: name, summary, reference chapter, dependencies, recommended prompts.
  - `build_agent(config: AgentConfig) -> Agent`: factory returning a runnable agent pipeline.
  - `demo(config: DemoConfig) -> DemoResult`: thin wrapper used by CLI/tests/demos.
  - Inline docstrings describing strategy, trade-offs, and configuration expectations.
- **Common Infrastructure**:
  - `LLMClient` abstraction with implementations:
    - `OpenAILLMClient` (env-driven API access).
    - `LiteLLMClient` (configurable provider routing).
    - `MockLLMClient` (rule-based responses for offline/testing).
  - Prompt templating primitives (`PromptTemplate`, `Message`, reusable prompt fragments).
  - Memory utilities (`MemoryStore`, `ConversationBuffer`, `VectorMemory` with optional FAISS if available).
  - Tooling interfaces (`Tool`, `ToolRegistry`, built-in tools: search stub, calculator, file read, calendar stub).
  - Workflow orchestration helpers (sequential chain, router, planner executor, reflection loop, etc.).
- **Demo Layer**:
  - CLI driver `demos/run_pattern.py` enabling `python -m demos.run_pattern --pattern prompt_chaining`.
  - Gradio app `demos/gradio_interface.py` presenting selectable patterns and the real-world scenario with clear user instructions.
  - Notebook-friendly example seeds stored in `notebooks/`.
- **Real-World Scenario**:
  - Implement `SmartSupportTriageAgent` (uses routing, memory, prioritization, evaluation patterns) to triage support tickets and surface responses.
  - Provide realistic sample data in `data/support_tickets.json`.
- **Tests, Quality, Observability**:
  - Pytest suite ensuring factories build without runtime errors, mock runs succeed, and configuration validation works.
  - Lightweight telemetry hooks (structured logging helpers) to trace prompt/response cycles.
- **Documentation**:
  - Pattern catalog page per part with quickstart, diagrams (ASCII or PlantUML), and run instructions.
  - README revamp with TL;DR, setup, quick demo, architecture overview, and deployment guide.
  - CONTRIBUTING guide describing extension workflow and coding conventions.

## 3. Non-Functional Requirements
- Python 3.10+ compatibility.
- Dependency-light core; optional extras grouped via extras_require (e.g., `gradio`, `faiss`, `plot`).
- Deterministic default configuration using `MockLLMClient` to support sandbox execution without network calls.
- All scripts runnable via `make` recipes (e.g., `make install`, `make demo`, `make test`).
- Complete removal of `TODO` placeholders in committed code/documents.

## 4. Architecture Overview
```
AI_Agent_Design_Pattern_Collection/
├── README.md
├── docs/
│   ├── spec.md
│   ├── patterns/
│   │   ├── part_1.md
│   │   ├── part_2.md
│   │   ├── part_3.md
│   │   └── part_4.md
│   └── deployment.md
├── src/
│   └── ai_agent_patterns/
│       ├── __init__.py
│       ├── config.py
│       ├── llm/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── openai.py
│       │   ├── litellm.py
│       │   └── mock.py
│       ├── memory/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── conversation.py
│       │   └── vector.py
│       ├── prompts/
│       │   ├── __init__.py
│       │   └── templates.py
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── base.py
│       │   ├── builtin.py
│       │   └── registry.py
│       ├── workflows/
│       │   ├── __init__.py
│       │   ├── chain.py
│       │   ├── router.py
│       │   ├── planner.py
│       │   ├── reflection.py
│       │   └── evaluation.py
│       └── patterns/
│           ├── __init__.py
│           ├── prompt_chaining.py
│           ├── routing.py
│           ├── parallelization.py
│           ├── reflection.py
│           ├── tool_use.py
│           ├── planning.py
│           ├── multi_agent.py
│           ├── memory_management.py
│           ├── learning_adaptation.py
│           ├── mcp.py
│           ├── goal_setting.py
│           ├── exception_handling.py
│           ├── human_in_loop.py
│           ├── knowledge_retrieval.py
│           ├── inter_agent_communication.py
│           ├── resource_aware_optimization.py
│           ├── reasoning.py
│           ├── guardrails.py
│           ├── evaluation_monitoring.py
│           ├── prioritization.py
│           └── exploration_discovery.py
├── demos/
│   ├── run_pattern.py
│   ├── gradio_interface.py
│   └── smart_support_triage.py
├── data/
│   └── support_tickets.json
├── notebooks/
│   └── smart_support_walkthrough.ipynb
├── tests/
│   ├── __init__.py
│   ├── test_pattern_factories.py
│   ├── test_llm_clients.py
│   └── test_workflows.py
├── requirements.txt
├── requirements-dev.txt
├── setup.cfg
├── pyproject.toml
├── Makefile
├── Dockerfile
└── huggingface_space/
    ├── app.py
    ├── requirements.txt
    └── README.md
```

## 5. Pattern Implementation Strategy
- **Shared Agent Skeleton**: Implement a reusable `Agent` dataclass encapsulating `llm`, `memory`, optional `tools`, and an `execute` coroutine. Each pattern module composes this skeleton with configurations specialized for that pattern.
- **Factories Instead of Monoliths**: Patterns return callables or classes that accept `AgentConfig` (LLM provider, temperature, tool toggles). This ensures the CLI, tests, and Gradio UI use the same code path.
- **Mock-Friendly Demos**: Provide deterministic sample outputs for `MockLLMClient` to keep tests hermetic. Use scenario-specific heuristics (e.g., rule-based router decisions).
- **Stateful Patterns**: Patterns involving memory or multi-agent coordination persist state within the `Agent` instance; demos reset state per run.
- **Multi-Agent**: Offer a small framework under `workflows/` for orchestrating multiple agents with message passing and include an example conversation (e.g., Architect ↔ Executor).
- **RAG**: `knowledge_retrieval.py` relies on `VectorMemory`; include fallback to a simple keyword matcher when FAISS unavailable.
- **MCP**: Provide stub `MCPTool` interface illustrating protocol communication and a mock server for tests.
- **Guardrails**: Integrate content moderation stub and regex-based validation to illustrate safety patterns.

## 6. Demo & Interface Design
- **CLI Runner**:
  - Options: `--pattern`, `--config path`, `--mock`, `--transcript out.json`.
  - Prints structured logs summarizing steps and responses.
- **Gradio App**:
  - Tabs: `Pattern Playground`, `Smart Support Triage`.
  - Pattern Playground: dropdown of patterns, prompt input, results panel, explanation accordion.
  - Smart Support Triage: upload/select sample ticket, agent returns priority, suggested response, reasoning trace.
  - Provide instructions for setting API keys via textboxes or environment variables.
- **Smart Support Flow**:
  1. Preprocess ticket.
  2. Route to specialist agent (routing).
  3. Generate plan (planning).
  4. Use tools (FAQ search stub) (tool use + RAG).
  5. Reflect and refine answer (reflection).
  6. Evaluate and assign priority (evaluation + prioritization).
- Provide `smart_support_walkthrough.ipynb` replicating the end-to-end agent with commentary.

## 7. Deployment Approach
- **Local**: `make install` (creates virtualenv), `make demo` (runs CLI), `make gradio` (launches interface with MockLLM by default).
- **Docker**:
  - Multi-stage build; base uses `python:3.11-slim`.
  - Copy repo, install dependencies, expose `7860` for Gradio.
- **Hugging Face Spaces**:
  - `huggingface_space/app.py` imports `demos.gradio_interface:create_app`.
  - Minimal `huggingface_space/requirements.txt` listing pinned dependencies.
  - README describing secrets configuration for API keys.

## 8. Testing & Validation
- `pytest` covering:
  - Each pattern factory instantiation with `MockLLMClient`.
  - Smart support pipeline end-to-end with mock outputs.
  - Workflow helpers (planner, router) unit tests.
  - LLM clients raising meaningful errors on missing credentials.
- `ruff`/`black` via `Makefile` lint targets.
- CI-ready instructions (GitHub Actions config optional out of scope for initial delivery but spec-ready).

## 9. Implementation Roadmap
1. Scaffold project structure, configuration files, and shared utilities.
2. Implement core abstractions (config, LLM clients, memory, tools, workflows).
3. Incrementally implement pattern modules (targeting Part One first, then subsequent parts).
4. Build demos (CLI, Gradio) after patterns share consistent interface.
5. Implement Smart Support scenario, dataset, notebook placeholder.
6. Add tests, ensure `make test` + `make demo` succeed with `MockLLMClient`.
7. Update documentation (README, pattern guides, deployment guide).
8. Final sanity checks: run lint/tests, verify Gradio app launches, ensure no TODOs.

## 10. Risks & Mitigations
- **LLM Dependencies**: Provide mock client defaults and guard external calls behind configs.
- **Complexity Across 21 Patterns**: Standardize module template and reuse workflow primitives to throttle duplication.
- **Gradio Performance**: Keep inference lightweight and limit concurrency (configurable).
- **Maintaining Consistency**: Introduce `PatternRegistry` to auto-discover patterns for CLI/UI/test alignment.

## 11. Acceptance Criteria
- Repo contains complete directory structure with implemented modules, demos, documentation per this spec.
- Running `make demo` executes a mock-backed pattern successfully.
- Gradio interface works locally with `MockLLMClient` and supports API-backed mode.
- Smart Support Triage scenario produces deterministic outputs with mock client.
- README includes quickstart, pattern map, deployment, and contribution guidance.
- No TODO markers remain in code or docs.
