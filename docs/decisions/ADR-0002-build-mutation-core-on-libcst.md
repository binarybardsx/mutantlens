# ADR-0002: Build a small mutation core on libcst rather than wrapping an engine

Status: Proposed. The maintenance check happens at the start of task 1.2 (the mutation core); the final status is set in task 1.10 using the agreement analysis. Check the current state of mutmut, cosmic-ray and mutpy.

## Context
Existing Python mutation engines are mature, but they own the orchestration loop: they decide which mutants to generate, which tests to run, in what order and with what parallelism. This project's contribution lives precisely in that loop — diff scoping, per-mutant test selection, cross-run caching, budget enforcement, and feeding chosen survivors to a model mid-run.

`ast` discards formatting, so applying and reverting a mutation through it rewrites the file. libcst preserves formatting and gives exact byte positions, which is what makes stable mutant hashes possible.

## Decision
Write a minimal mutation core on libcst that enumerates, applies and reverts mutants, and keep orchestration in this project. Keep an adapter interface and validate the core against an established engine on at least three modules (a later validation task).

## Consequences
- Full control over selection, caching and budgets; no fighting another tool's control flow.
- We own correctness of the operators, so the agreement analysis is mandatory, not optional.
- If the check in task 1.2 finds an engine exposing a clean library API with per-mutant control, reverse this and log it.
