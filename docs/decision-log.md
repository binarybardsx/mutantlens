# Decision log

One dated entry per choice that had alternatives. Substantial or irreversible decisions get a full ADR in `docs/decisions/`; everything else lives here.

This file is article material. Write the entry when you make the decision, not afterwards.

## Format

```
## YYYY-MM-DD - <decision>
Task: <id>
Chose: <what>
Over: <alternatives>
Because: <reason, with the constraint that decided it>
Revisit if: <what would change this>
```

## Entries

## 2026-10-19 - Measure before generate
Task: planning
Chose: Finish and validate the mutation engine and make it CI-fast before any LLM code.
Over: Building the generation loop first and measuring later.
Because: Without a validated baseline, no later claim about the loop means anything. Also gives a useful tool that does not depend on a model.
Revisit if: The baseline turns out to be trivial to produce, freeing time to parallelise.

## 2026-10-20 - One feature at a time, one component per task
Task: planning
Chose: Plan and build a single small runnable feature at a time. Inside it, each task is one component, starting with a CLI stub so the path exists from the start. Types are added by the task that first needs them.
Over: A 46-task plan across seven milestones with an up-front contracts task.
Because: Interfaces written before any code ran would have been guesses. Planning only the current feature lets each one use what the last taught.
Revisit if: Rework between features becomes the main cost.

## 2026-10-20 - Stages: top-down vertical slices, firm for two stages, provisional after
Task: planning
Chose: Build top-down. Stage 0 is a throwaway end-to-end spike on a toy; later stages replace its parts with proper ones in the order the spike showed they hurt. A throwaway spike also precedes any LLM work (3.1). All stages are listed in the task list, but only Stages 0 and 1 are firm; Stages 2 to 5 are provisional and are re-planned when the previous stage ends.
Over: Bottom-up layers (contracts, config, store, sandbox) built before anything runs, and a single feature planned at a time with nothing visible beyond it.
Because: Intuition comes from seeing the idea work and then seeing it fail. Listing the later stages keeps the destination and the three article points visible, while marking them provisional avoids pretending the detail is known. Refines the entry above (one feature at a time), whose vocabulary of features A to N is replaced by stages.
Revisit if: Rework between stages becomes the main cost, or the provisional stages keep changing shape.

## 2026-10-21 - Build backend and CLI library for the scaffold
Task: 1.1
Chose: hatchling as the build backend, and argparse from the standard library for the CLI.
Over: uv_build or setuptools for the backend; click or typer for the CLI.
Because: hatchling is MIT-licensed, maintained and widely used. argparse adds no dependency, and the CLI is only a few commands (rule 11).
Revisit if: The CLI grows enough subcommands that argparse becomes awkward to maintain.

## 2026-10-21 - Maintenance check of Python mutation engines
Task: 1.2
Chose: Keep ADR-0002 as Proposed and build the mutation core on libcst 1.9.0.
Over: Wrapping mutmut, cosmic-ray or mutpy.
Because: Checked on 2026-10-21. mutmut 3.8.0 (Sep 2026, Python 3.13, 74 open issues) and cosmic-ray 8.7.0 (Aug 2026, Python 3.13, 52 open issues) are both active. mutpy's last release is 0.6.1 from Nov 2019, so it is dead. libcst 1.9.0 (Jul 2026) supports Python 3.13. I did not study mutmut's or cosmic-ray's library APIs in depth, so I have not shown that neither offers per-mutant control.
Revisit if: Task 1.10 finds an engine with a clean per-mutant library API, or libcst stops being maintained.

## 2026-10-21 - Mutant spans are character offsets
Task: 1.2
Chose: `Span` holds half-open character offsets into the source string.
Over: Line and column pairs, or byte offsets.
Because: `apply` (task 1.3) takes and returns a string, so it can cut at those numbers directly. Line and column can be derived later for reports.
Revisit if: A consumer needs byte offsets, for example to edit files read as bytes.

## 2026-10-22 - A mutant carries the hash of its whole source file
Task: 1.3
Chose: `Mutant.source_hash` is the SHA-256 of the full source text, and `apply` refuses a mutant whose hash does not match the source it is given.
Over: Checking only that `source[span]` still equals `original`; storing a line number.
Because: A span is only true for the exact source it came from. An edit earlier in the file shifts every later span, and the text at a shifted span can still look right by accident. A whole-source hash catches every such case with one check.
Revisit if: Task 1.7 needs a mutant id that survives unrelated edits. That id is a separate hash and does not replace this one.
