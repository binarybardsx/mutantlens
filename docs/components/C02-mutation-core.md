# C02: Mutation core

Status: Draft
Owner tasks: 1.2 (find mutants, one operator), 1.3 (apply), 1.4 (the remaining operators)
Depends on: nothing

## Purpose
Enumerate mutants for a scope, apply one to a working copy, and revert it exactly. Nothing else. It does not decide which mutants to run, in what order, or against which tests — that is the runner's job (ADR-0002).

## Interface
```
find_mutants(source: str) -> list[Mutant]        # 1.2 (built)
apply(source: str, mutant: Mutant) -> str          # 1.3
# revert(): not built until a task needs it. Mutants are applied to a copy.
```
Pure functions over strings. The core never touches the filesystem, the network or the clock.

`Mutant` (in `mutantlens/contracts/mutant.py`) has four fields so far: `operator`, `span`, `original`, `replacement`. `Span` is a half-open range of character offsets into the source string. Mutants come back in source order. Source that does not parse raises `libcst.ParserSyntaxError`; the caller turns that into a typed outcome.

## Starter operator set
Task 1.2 has ONE operator: comparison boundary (> to >=, < to <=, >= to >, <= to <). The rest arrive in task 1.4, one at a time. The full candidate list, chosen from the survey literature, not invented: comparison operator replacement, arithmetic operator replacement, boolean operator replacement, constant replacement (including the off-by-one and empty-collection cases), conditional negation, and return-value replacement. Each operator has an id that appears in results, so per-operator usefulness is measurable later.

## Behaviour
1. Enumeration is deterministic: the same source and operator set produce the same mutants in the same order.
2. A mutant's span is exact, derived from libcst position metadata.
3. `apply` changes exactly one token at the mutant's span; everything else, including comments, whitespace and line endings, is byte-identical. It refuses a mutant whose source hash does not match.
4. Enumeration never produces a mutant that fails to parse. If an operator would produce invalid syntax, it is skipped and counted.
5. Operators never mutate inside test files, string literals used as docstrings, or `__all__`.

## What it must never do
Write to disk. Run tests. Call a model. Decide anything about scheduling or budgets.

## Tests
Property: applying a mutant changes exactly one token. Property: every enumerated mutant parses. Golden: the mutant set for two fixture modules, reviewed on change. Determinism: two enumerations are equal.

## Validation
Task 1.10: compare the mutant set against an established engine on at least three real modules. Every difference explained as an operator-set or scoping difference. Committed as a short report.

## Open questions
Whether to suppress equivalent-prone operators up front, as Google's work on mutant suppression suggests, or to measure first and suppress later. Decide in Stage 3 (task 3.10), with data.
