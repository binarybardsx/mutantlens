# ADR-0006: Apache-2.0, permissive on purpose

Status: Accepted (2026-10-19).

## Context
The leading open-source AI test-generation tool in this space reached 5.7k stars under AGPL-3.0 and was marked unmaintained in June 2025. AGPL blocks adoption at exactly the companies most likely to want this.

## Decision
Apache-2.0 for code. Corpus definitions and result data under CC-BY-4.0. Do not read or copy from any AGPL-licensed tool in this space; build clean and say so in the README.

## Consequences
- No AGPL code may enter the repository, and dependency licences are checked before adoption.
- The permissive licence is itself a differentiator worth stating.
