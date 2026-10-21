# ADR-0001: Measure before you generate

Status: Accepted (2026-10-19). Ratified at the end of Stage 2, before Stage 3 (the first LLM stage) is planned in detail.

## Context
The obvious build order is to write the generation loop first and measure later. Every comparable hobby project does this, and most report results only on toy modules or in mock mode.

## Decision
The mutation engine is finished and made CI-fast before any LLM code exists. The baseline corpus and its scores are committed before the first prompt is written.

## Consequences
- Any later claim about the generation loop is a delta against a committed, reproducible control.
- There is a useful tool before any LLM stage, with no model dependency at all, which is the project's insurance.
- It feels slow at the start. That is the cost, and it is accepted.
