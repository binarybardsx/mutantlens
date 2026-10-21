# Development workflow

## The loop for one task

1. **Pick the task.** The first task of the current stage whose dependencies are all Completed. One at a time.
2. **Read the concept brief** for that task before building. If you cannot say what the task teaches, do not start it.
3. **Paste into Claude Code:** the task row, and the component note it names if there is one. `CLAUDE.md` loads automatically. Nothing else.
4. **Interface first.** Claude proposes types and signatures and stops. You approve or change them.
5. **Implementation plus tests**, in one PR, only the files the task needs.
6. **Run the done check** — the exact command in the task's acceptance criteria. Code existing is not done; the command passing is done.
7. **Update the logs.** A decision-log entry if you chose between alternatives. A surprises-log entry if reality disagreed with you.
8. **Mark Completed** in the task list with the PR link.

## Who runs what

Claude Code never spends money. Any paid run — corpus runs, model comparisons, the experiment matrix — is printed as a command for you to run, with a cost estimate. CI runs on cassettes and a fake provider, so it is free and offline.

## Stage checkpoints

When a stage's last task passes: check the stage gate, add log entries, and note what surprised you. Only then re-plan the next stage, using what was learned. If the gate cannot be met, that is information about the plan. Do not continue past it.

## When a task feels wrong

Stop. A task that seems to need something from a later stage is usually a planning error, not a reason to reach forward. Fix the plan and log why.

## Commit and PR conventions

- Conventional commits (`feat:`, `fix:`, `test:`, `docs:`, `refactor:`, `chore:`).
- One task per PR, with the task ID in the title.
- The PR description shows how each acceptance criterion was met: test name, command output or committed report.
