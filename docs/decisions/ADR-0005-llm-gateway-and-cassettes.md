# ADR-0005: One LLM gateway, and every call recorded

Status: Accepted (2026-10-19). Built in tasks 3.2 and 3.3.

## Context
Evaluation must be reproducible by someone who did not pay for the original run, and cost must be attributable per unit of outcome rather than estimated at the end.

## Decision
`mutantlens/llm/` is the only module that imports a provider SDK. It pins model snapshots, sets temperature explicitly, validates every response against a Pydantic model, writes a cost ledger row per call, and records every call to a cassette keyed by prompt hash. Replay needs no API key.

## Consequences
- Swapping providers costs one module.
- CI and every published report run offline from cassettes at zero cost.
- Cassettes must be scrubbed of secrets before committing, and are large: store them deliberately.
