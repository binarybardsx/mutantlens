# mutantlens: instructions for Claude Code

mutantlens measures whether a test suite actually catches bugs. It seeds small faults (mutants) into source code and counts how many the tests notice. An LLM loop then proposes tests for the faults nobody caught, and every proposed test must earn its place by killing a fault that previously survived.

> **Name:** the project, package and CLI are `mutantlens`. Do not introduce another name.

Read this file fully, then read ONLY the task row you were given and the component note it names, if one exists. Do not read the whole repo.

## Where things are
- Task list: `mutantlens-tasks.xlsx` (Tasks sheet), kept outside the repo. The row is pasted into your prompt. Tasks are identified by ID, e.g. `1.5`.
- Component notes: `docs/components/Cxx-*.md`, written only when a task needs one. Architecture: `docs/architecture.md`. Decisions: `docs/decisions/`.
- Stages and the current stage's gate: `docs/roadmap.md`. Workflow: `docs/development-workflow.md`. Testing: `docs/testing.md`.
- What every run must record: `docs/metrics.md`. Index of all docs: `docs/index.md`.

## Hard rules (a violation means stop and ask)

1. **One stage at a time, one task at a time.** A stage is a small set of tasks that ends in something runnable you can see; each task is one component or one measurement. Work only on the task ID you were given and touch only the files it needs. Do not plan or build tasks for a later stage. If you notice other work, write it in the PR description and move on.
2. **Interface before implementation.** Propose the types and signatures first and stop for approval. No implementation in the same turn as a new interface.
3. **Measure before you generate.** No LLM code, no prompts and no model dependencies before Stage 3 (task 3.1 is the first). If an earlier task seems to need a model, the task is wrong: stop and say so.
4. **The verifier decides, never the model and never you.** A test is accepted only when the mutation runner reports it killed a mutant that previously survived. Never accept a test because it looks correct, raises coverage, or the model said it was good.
5. **Coverage is reported, never enforced.** No code path may gate on coverage delta.
6. **All generated or mutated code runs in the sandbox** (`mutantlens/sandbox/`, built in task 1.6): never execute a model-written test or a mutated module outside it. Until 1.6 is done, mutated code may run unsandboxed ONLY on fixtures under `tests/fixtures/` or `toy/` in this repo, never on external code. The sandbox has no network, a read-only source mount, memory and CPU caps and a hard timeout.
7. **One LLM gateway.** Only `mutantlens/llm/` imports a provider SDK. Everything else takes a client interface. Pin model snapshots, set temperature explicitly, validate every response against a Pydantic model. The one exception is the throwaway `spike/ask.py` in task 3.1.
8. **Determinism is a feature.** Every run records its seed. Every model call goes through cassette record/replay. Tests never touch the live network and never need an API key.
9. **Types grow with the task that first needs them.** Add only the fields the current task uses; no up-front contracts. Types live in `mutantlens/contracts/`, one small module each. After the first tagged release they are frozen: a change then needs a decision-log entry, a schema-snapshot update and its own task.
10. **Never spend money without being asked.** Do not run paid model calls, corpus runs or evaluations. Print the exact command for the human to run, with an estimate of what it will cost.
11. **No new dependency** without stating why, checking its licence is permissive, and checking it is maintained.
12. **No scope creep.** No speculative abstraction, no refactor, no rename, no "while I'm here" cleanup, no code for a future task.

**`spike/` is throwaway** (Stage 0 and task 3.1): exempt from rules 2, 14 and 15 and from ruff and pyright, never imported by `mutantlens/`. Stage 0 code is deleted at task 1.10; `spike/ask.py` is deleted once the gateway (3.2) replaces it. Keep it small and ugly; the point is to see the idea run and see where it hurts.
13. **Record provenance on every run once the run store exists.** Config hash, tool git SHA, target repo SHA, model snapshot, seed, budgets. A result that cannot be traced to these did not happen.
14. **Tests ship with the code,** including the edge case the task's concept brief warned about. Never delete or skip a test to get green.
15. **Docs stay in sync** in the same pull request: the component note if there is one, `docs/architecture.md` if an interface moved, an ADR if a decision changed.
16. **When a mistake repeats, add a rule here** rather than fixing it again.

## Commands

```bash
uv sync                      # install
uv run ruff check . && uv run ruff format --check .
uv run pyright
uv run pytest                # must pass with no network and no API key
uv run mutantlens assess <path>    # the tool
uv run mutantlens report <run-id>  # render a run
```

## Conventions
- Python 3.12+, full type annotations, Pydantic v2 at every module boundary.
- Pure functions in the core; IO at the edges. The mutation core does not touch the network or the clock.
- Errors are values at boundaries: no uncaught exception escapes the CLI. Every failure becomes a typed outcome that lands in the run store.
- Structured logging only. Never log an API key, never log full source files.
- Mutants are identified by content hash, never by index or line number alone.

## Out of scope unless the task says so
Multi-language support, a web UI, a hosted service, multi-agent orchestration, fine-tuning, and anything in a later stage than the task you were given. Python only until the Python numbers are published.

## What does NOT belong in this file
Component details, API shapes, long examples, the task list, history. Those live in `docs/` and are read on demand.
