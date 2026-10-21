# Documentation map

A small `CLAUDE.md` is always loaded; everything else is read on demand. Point Claude Code at one file per task, never the whole folder.

| Information | Lives in | Loaded |
|---|---|---|
| Hard rules, commands, conventions | `CLAUDE.md` | always |
| Components, interfaces, data flow | `docs/architecture.md` | when a task touches an interface |
| Stages and the current gate | `docs/roadmap.md` | when planning or closing a stage |
| Why we decided something | `docs/decisions/ADR-*.md` | only when questioning or changing a decision |
| What a component is and its interface | `docs/components/Cxx-*.md` | when the task names one |
| What every run must record | `docs/metrics.md` | any task that writes to the run store |
| How to work with Claude Code here | `docs/development-workflow.md` | when starting, or when a task feels wrong |
| How to test | `docs/testing.md` | when writing tests |
| Running decisions, dated | `docs/decision-log.md` | append at each decision |
| What surprised us | `docs/surprises-log.md` | append whenever reality disagreed |
| Which task is next | `mutantlens-tasks.xlsx` (outside the repo) | the one task row |

Rule of thumb: if it changes when a task finishes, it does not belong in `CLAUDE.md`. If it must never be violated, it does.

Component notes are written in the task that needs them, not before. Only C02 (mutation core) exists so far.
