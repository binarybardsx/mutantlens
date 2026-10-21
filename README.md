# mutantlens

**Does your test suite actually catch bugs?**

mutantlens seeds small faults into your code and counts how many your tests notice. Line coverage tells you which lines ran; mutation score tells you which bugs would have been caught. They are not the same number, and the gap is usually large.

> Status: **pre-alpha**, building in public.

## Two things in one repository

1. **The tool.** A CLI and GitHub Action that assesses the code in a pull request, fast enough to run on every PR. Scoped to the diff, with per-mutant test selection and caching.
2. **The experiment.** A corpus harness that runs the same engine across many repositories and variants to answer one question: *does feeding surviving mutants back to an LLM actually produce better tests than asking once?* Existing evidence disagrees with itself, and the answer is reported either way.

## How it works

Scope the diff, seed faults, run only the tests whose coverage touches each fault, and report what survived. Where tests are missing, a model proposes new ones — and a proposed test is accepted only if it kills a fault that survived before. Coverage is reported and never enforced.

See [docs/architecture.md](docs/architecture.md) and [docs/roadmap.md](docs/roadmap.md).

## Quickstart

Not yet. The first release comes once the tool is useful without an LLM.

## Licence

Apache-2.0 (add the standard text to `LICENSE` before the first public commit). Deliberately permissive: the previous leading tool in this space was AGPL-3.0 and unmaintained, which blocked the teams most likely to want it.
