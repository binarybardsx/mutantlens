# What every run records

Build this up from the run-store task (1.7) onward: add each field in the task that first produces it. Provenance fields go in with the store itself, since adding them later means re-running everything, which is how projects lose their numbers.

## Levels

| Level | Fields |
|---|---|
| Run | run id, config hash, tool git SHA, target repo + SHA, variant, seed, model snapshot, budgets, started at, duration |
| Target | module, unit, lines of code, existing line coverage, baseline mutation score, mutants generated, survivors before |
| Mutant | content hash, operator, source span, outcome (killed / survived / timeout / suite error / build error), tests selected, tests run, execution ms, cache hit |
| Model call | prompt hash, context strategy, context tokens, output tokens, latency ms, cost, structured output valid, attempt number |
| Candidate test | validation outcome (parse error / import error / fails on clean / flaky / network attempt / accepted), mutants killed, rejection reason |
| Phase timing | ms in coverage capture, mutant generation, test execution, model wait, validation |

## The three derived metrics

Each must be answerable with one SQL statement:

1. **Mutation score delta** — before and after, per target and per run.
2. **Cost per killed mutant** — the headline number for every comparison.
3. **Wall clock per assessed pull request** — the number that decides whether anyone adopts the tool.

## Rules

- No number is reported without the config hash that produced it.
- No comparison is reported from a single seed.
- Cost is recorded at the call, never estimated afterwards.
