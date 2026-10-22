# Surprises log

Every time reality contradicted expectation. These entries are the most interesting paragraphs in the eventual write-ups and are impossible to reconstruct later.

Write the entry the day it happens, in one or two sentences. No polish.

## Format

```
## YYYY-MM-DD - <what surprised you>
Expected: <what you thought>
Observed: <what happened>
Consequence: <what changed because of it>
```

## Entries

Task 0.3 entries, ranked by how badly each can make the score wrong (worst first).

## 2026-10-21 - 1. A crash or a hang counts as a kill
Expected: only a failing assertion would count as killed.
Observed: tested with fake mutants. Code that raises `ZeroDivisionError` shows as `killed`. An infinite loop shows as `killed (timeout)`. Both look the same as a test that really noticed the bug. A slow machine could also hit the 10 second limit and fake a kill.
Consequence: the score can be too high with no warning. Stage 1 task 1.5 must give killed, survived, timeout, suite error and build error their own outcomes.

## 2026-10-21 - 2. Some mutants can never be killed
Expected: the strong suite would kill everything.
Observed: 5 of 14 survive even the strong suite (`x <= lo`, `x >= hi`, and the three `a < 0` style changes). They change no behaviour, so no test can catch them. The strong suite's 64% is close to its real ceiling.
Consequence: a low score may not mean weak tests. Tasks 3.10 and 3.11 need to find these, and the report should say how many survivors are probably unkillable.

## 2026-10-21 - 3. Mutated code runs with no protection
Expected: fine for a toy.
Observed: each mutant runs as a normal process with network access and write access to the machine. It is only safe because the code is our own `toy/` file.
Consequence: this must never run on other people's code until the sandbox exists. Task 1.6.

## 2026-10-21 - 4. Only comparisons are mutated
Expected: comparisons would be a good start.
Observed: the score says nothing about arithmetic, boolean logic, return values or deleted lines. A suite could score well and still miss those bugs.
Consequence: the number is narrow. Task 1.4 adds the other operators.

## 2026-10-21 - 5. Diffs go through `ast.unparse`, and mutants have no stable name
Expected: diffs would match the file.
Observed: comments and formatting are lost, brackets appear (`and (b + c > a)`), and the line number in a mutant's label does not match the line number in its diff hunk. Mutants are numbered by position, so the numbers change when code is edited.
Consequence: a diff cannot be applied back to the real file, and results cannot be compared between runs. Tasks 1.3 (apply) and 1.7 (stable ids).

## 2026-10-21 - 6. It is slow
Expected: fine.
Observed: every mutant copies the whole folder and starts a new pytest process. That is fine for 14 mutants and far too slow for a real project.
Consequence: Stage 2 (test selection, caching, parallel runs).

## 2026-10-21 - 7. A flaky test would look like a kill
Expected: tests are stable.
Observed: a mutant is called killed after one failing run. There is no second run to check.
Consequence: a random failure gives a fake kill. Stage 1 should rerun a failure before calling it killed.

## 2026-10-22 - Type-blind operators produce mutants that crash instead of failing
Expected: every operator would produce plausible bugs a test could catch.
Observed: `arithmetic_replace` turns `+` into `-` without knowing the types. On strings that raises `TypeError` (confirmed: `'a' - 'b'`). `return_replace` can also break callers that use the result. Run over `mutantlens/` itself the tool lists 109 mutants in 18 files, so such mutants are common.
Consequence: with today's runner these crashes would count as kills (entry 1 above), inflating the score. Task 1.5 must separate a crash from a failing assertion before any score is trusted.
