# ADR-0007: SQLite and Parquet, no server

Status: Accepted (2026-10-19). Built in task 1.7.

## Context
The tool runs on a laptop or a CI runner. The experiment runs on one machine over a corpus. Neither needs a database server, and requiring one would reduce adoption to near zero.

## Decision
SQLite for the run store and cost ledger, Parquet for exported result tables, DuckDB for analysis. File-based, zero operational surface.

## Consequences
- Corpus analysis is a SQL query rather than a bespoke script.
- Concurrency is bounded by SQLite's writer model; the orchestrator writes, workers return results.
- If the corpus ever outgrows one machine, revisit. It will not during the planned stages.
