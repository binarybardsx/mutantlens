# ADR-0004: All generated and mutated code runs in a sandbox

Status: Accepted (2026-10-19). Built in task 1.6. Until then, mutated code runs unsandboxed only on repo-owned fixtures.

## Context
This system executes code a language model wrote, against code it also mutated, on a developer machine or a CI runner. A comparable project states plainly that its safety screening is "a denylist, not a sandbox". A denylist is not a security control.

## Decision
Every execution of test code — generated or existing, mutated or clean — happens inside a container with no network, a read-only source mount, a writable tmpfs, memory and CPU limits and a hard timeout. Violations become typed outcomes, never exceptions.

## Consequences
- A container runtime is a hard dependency for running the tool.
- Slightly slower per-run startup, mitigated by batching mutants per container.
- Sandbox escape attempts are a test category that must run in CI (see `docs/testing.md`).
