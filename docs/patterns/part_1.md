# Part One — Foundational Patterns

## Chapter 1: Prompt Chaining
- **Intent**: Sequence prompts to decompose complex tasks into manageable steps.
- **Highlights in repo**: `patterns.prompt_chaining` demonstrates a three-step refinement pipeline (draft → critique → polish).
- **Try it**: `python -m demos.run_pattern --pattern prompt_chaining --mock`

## Chapter 2: Routing
- **Intent**: Direct requests to specialized agents/toolchains based on intent.
- **Highlights**: Workflow router inspects request metadata and dispatches to domain experts.
- **Try it**: `python -m demos.run_pattern --pattern routing --mock --input "Pricing question about enterprise tier"`

## Chapter 3: Parallelization
- **Intent**: Execute multiple sub-tasks concurrently and aggregate outcomes.
- **Highlights**: ThreadPool-backed executor with deterministic mock fan-out responses.

## Chapter 4: Reflection
- **Intent**: Self-evaluate outputs and iterate toward higher quality.
- **Highlights**: Critique loop with configurable max iterations & acceptance criteria.

## Chapter 5: Tool Use
- **Intent**: Combine LLM reasoning with external tool invocations.
- **Highlights**: Calculator, FAQ search stub, and structured tool registry.

## Chapter 6: Planning
- **Intent**: Generate and follow explicit plans for multi-step problems.
- **Highlights**: Plan generator + executor; integrates with prompt chain for validation.

## Chapter 7: Multi-Agent
- **Intent**: Coordinate specialized agents through turn-based communication.
- **Highlights**: Architect/Implementer pair demonstrating spec-to-code translation.
