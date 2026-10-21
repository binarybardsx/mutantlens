# Roadmap

Built top-down, **one stage at a time**. Stage 0 is a throwaway spike that runs the whole idea end to end. Each later stage replaces crude parts with proper ones, in the order the previous stage showed they hurt. Every task ends with something you can run and see.

Stages 0 and 1 are **firm**. Stages 2 to 5 are **provisional**: their shape is a best guess, and each is re-planned using what the previous stage taught before it starts.

| Stage | Tasks | Gate (all true before the next stage starts) | Plan |
|---|---|---|---|
| 0. The idea, crudely | 0.1 to 0.3 | `assess` on a toy prints a score; a weak suite with 100% line coverage scores clearly below a strong one; a ranked list of what is wrong with the crude version is in the surprises log | Firm |
| 1. Make the score trustworthy | 1.1 to 1.10 | Byte-exact apply; distinct outcomes; sandbox blocks escapes; recorded runs with provenance; three real projects measured; agreement with an established engine explained; ADR-0002 closed; `spike/` deleted. **Publish article 1 after 1.9** | Firm |
| 2. Make it CI-fast | 2.1 to 2.8 | A representative PR assessed within a stated time budget; before-and-after table across a 15 to 20 repo corpus with B0 baselines. **Publish article 2 after 2.8** | Provisional |
| 3. Add the LLM | 3.1 to 3.12 | One-shot and guided variants replay from cassettes at zero cost; the gate rejects a coverage-raising test that kills nothing; equivalence detector measured on 100+ labelled survivors. Checkpoint at 3.7 | Provisional |
| 4. The experiment | 4.1 to 4.7 | Paired tests, confidence intervals, cost per killed mutant, seen versus unseen code split. **Publish article 3 after 4.7** | Provisional |
| 5. Release | 5.1 to 5.6 | Clean install from PyPI; action green on an external repo; every article number traces to a committed report | Provisional |

**Stopping points.** After Stage 2 there is a useful CI tool with no LLM in it. After Stage 4 there is a result. Both are publishable alone. Publish as you go; do not wait for the end.

**Measure before you generate** still holds: no LLM task starts until the tool is useful and validated without one (ADR-0001). The only model contact before the gateway exists is the throwaway spike in 3.1, whose job is to show you how generated tests fail.

**Try it, see it fail, then read.** The concept behind a task is easier to absorb after you have hit the problem it solves. Ask for the full concept brief after the first attempt if you prefer.
