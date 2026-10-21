# ADR-0003: A test is accepted only if it kills a surviving mutant

Status: Accepted (2026-10-19). Enforced in task 3.8.

## Context
Coverage-gated generation is what the existing open-source tools do: keep a test if it raises coverage. Meta's published results report that 277 of 571 accepted tests would have been discarded under a line-coverage criterion, which means coverage both keeps worthless tests and throws away valuable ones.

## Decision
The only acceptance criterion is that a candidate test kills at least one mutant that survived before it. Coverage delta is recorded and reported; no code path may gate on it.

## Consequences
- Fewer accepted tests, each with a demonstrable reason to exist.
- Acceptance rate becomes a meaningful metric rather than a measure of verbosity.
- This rule is the project's thesis. If it is ever relaxed, the project has become something else.
