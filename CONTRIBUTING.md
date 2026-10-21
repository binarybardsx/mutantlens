# Contributing

Thanks for looking. This project is built in public, one task at a time, from a roadmap in `docs/roadmap.md`.

## Before you open a PR

- **One task per PR.** If there is no task for what you want to do, open an issue first and we will add one.
- **Tests ship with code.** No live network, no API key required to run the suite.
- **Generated or mutated code runs only in the sandbox.** This is a hard rule, including in tests and examples.
- **Dependencies** need a permissive licence and a reason. No AGPL code enters this repository.

## Setup

```bash
uv sync --all-extras --dev
uv run pytest
```

The suite must pass with no network access and no provider key.

## What makes a good contribution here

The project's value is that its measurements are trustworthy. A change that makes the tool faster but could cause a killing test to be missed is a bad trade. If you are touching mutant identity, test selection or outcome classification, say in the PR how you convinced yourself it is still correct.

## Reporting a result

If you run mutantlens on a repository and the numbers look wrong, that is the most useful issue you can file. Include the config hash, the tool version, the target repository and commit, and the run record if you can share it.
