# Testing

## Non-negotiables

- **No live network in any test.** No API key is needed to run the suite. Model calls go through cassettes; the default test provider is a deterministic fake.
- **No test writes outside a temp directory.**
- **Tests ship in the same PR as the code.**
- **Never delete or skip a test to get CI green.** Fix it or explain in the PR why the test was wrong.

## Layers

| Layer | What it covers | Notes |
|---|---|---|
| Unit | Pure logic: operators, hashing, scoping, selection, budgets | Fast, no containers |
| Property | Invariants that must hold for any input | See below |
| Golden | Mutant sets and reports for fixed fixture modules | Snapshot files reviewed by eye on change |
| Sandbox | That isolation actually isolates | Must run in CI, not just locally |
| Integration | CLI end to end on a fixture repository | Cassettes only |

## Properties worth asserting

- Apply then revert a mutant leaves the file byte-identical.
- A mutant's content hash is stable across runs and unaffected by unrelated edits to the file.
- Test selection never misses a killing test: on a fixture, selected-subset results equal full-suite results.
- A budgeted run with a fixed seed is reproducible, including which mutants it skipped.
- The acceptance gate rejects any test that kills nothing, however much coverage it adds.

## Sandbox tests that must exist

A generated test that opens a socket, that loops forever, that allocates unbounded memory, and that tries to write to the source tree. Each must produce a typed outcome, not an exception and not a hang.

## What is not tested

Model output quality. That is measured by the experiment harness, not asserted in the suite. Do not write a test that asserts a model produced a good test.
