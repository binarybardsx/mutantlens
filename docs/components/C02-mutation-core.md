# C02: Mutation core

Status: Draft
Owner tasks: 1.2 (find mutants, one operator), 1.3 (apply), 1.4 (the remaining operators, built)
Depends on: nothing

## Purpose
Enumerate mutants for a scope, apply one to a working copy, and revert it exactly. Nothing else. It does not decide which mutants to run, in what order, or against which tests — that is the runner's job (ADR-0002).

## Interface
```
find_mutants(source: str) -> list[Mutant]        # 1.2 (built), runs every operator as of 1.4
scan(source: str) -> FindResult                    # 1.4: mutants plus the skipped-invalid count
apply(source: str, mutant: Mutant) -> str          # 1.3 (built)
# revert(): not built until a task needs it. Mutants are applied to a copy.
```
Pure functions over strings. The core never touches the filesystem, the network or the clock.

`Mutant` (in `mutantlens/contracts/mutant.py`) has five fields so far: `operator`, `span`, `original`, `replacement`, `source_hash`. `source_hash` is the SHA-256 (hex, of the UTF-8 text) of the exact source the mutant was found in, from `mutantlens/mutate/hashing.py`. `Span` is a half-open range of character offsets into the source string. Mutants come back in source order. `apply` hashes the source it is given and raises `StaleMutantError` if it does not match the mutant's `source_hash`; nothing is changed in that case. Source that does not parse raises `libcst.ParserSyntaxError`; the caller turns that into a typed outcome.

## Operators
Each operator is a module in `mutantlens/mutate/operators/` with a stable id that appears in results, so per-operator usefulness is measurable later. An `Operator` has an `id` and `candidates(module, locator)`, which returns `Candidate(span, replacement)` values. `scan` turns candidates into `Mutant`s, sorts them by (span start, span end, operator id, replacement), and drops any whose mutated source does not parse. Dropped ones are counted in `FindResult.skipped_invalid`, never hidden.

| Id | Changes | Leaves alone |
|---|---|---|
| `comparison_boundary` | `>`↔`>=`, `<`↔`<=` | `==`, `!=`, `in`, `is` |
| `arithmetic_replace` | `+`↔`-`, `*`↔`/`, `//`→`/`, `%`→`*`, `**`→`*`, and the `+=` style forms | unary `-` and `+`, bitwise and shift operators, `@` |
| `logical_replace` | `and`↔`or` | `not`, `&`, `\|` |
| `constant_replace` | integer `n` to `n + 1` (one variant only), `True`↔`False`, a non-empty list, set or dict literal to an empty one | floats, strings, tuples, already-empty collections |
| `conditional_negate` | the test of `if`, `elif`, `while` and `x if c else y` becomes `not (test)` | `for` loops, comprehension filters |
| `return_replace` | `return expr` becomes `return None` | bare `return`, `return None` |

No operator changes anything inside a string, a comment or a docstring, or anything assigned to `__all__`. Strings are never mutated, so the first two hold by construction; `__all__` is skipped explicitly in `CandidateVisitor`. Tuples are left out because libcst's position for a parenthesised tuple is not yet checked.

Test files are skipped by `is_test_file(path)` in `mutantlens/mutate/scope.py`, called by the code that walks a project (`assess`), because the core only sees a string. The candidate list in the survey literature is covered; further operators are added only with evidence.

## Behaviour
1. Enumeration is deterministic: the same source and operator set produce the same mutants in the same order.
2. A mutant's span is exact, derived from libcst position metadata.
3. `apply` changes exactly one token at the mutant's span; everything else, including comments, whitespace and line endings, is byte-identical. It refuses a mutant whose source hash does not match.
4. Enumeration never produces a mutant that fails to parse. If an operator would produce invalid syntax, it is skipped and counted in `FindResult.skipped_invalid`. The check parses every mutated source once, which is quadratic in file size; fine for now, revisit in Stage 2.
5. Operators never mutate inside test files, docstrings or `__all__` (see Operators).

## What it must never do
Write to disk. Run tests. Call a model. Decide anything about scheduling or budgets.

## Tests
Property: applying a mutant changes exactly one token. Property: every enumerated mutant parses. Golden: the mutant set for two fixture modules, reviewed on change. Determinism: two enumerations are equal.

## Validation
Task 1.10: compare the mutant set against an established engine on at least three real modules. Every difference explained as an operator-set or scoping difference. Committed as a short report.

## Open questions
Whether to suppress equivalent-prone operators up front, as Google's work on mutant suppression suggests, or to measure first and suppress later. Decide in Stage 3 (task 3.10), with data.
