# Reverse-engineering analysis notes

This file is intentionally reserved for the **post-benchmark analysis phase**.

The benchmark agent should not fill this file.

After all mapped subtopics have benchmark packs and the gap ledger is complete, the maintainer will analyse the findings across subtopics and determine the smallest durable fixes.

## Analysis workflow

For each gap in `GAPS.md`:

1. Reproduce the failure from the benchmark case.
2. Compare the same semantic case across other subtopics.
3. Decide whether the failure is a one-off content omission, source/input insufficiency, wrong capability/prerequisite model, learner-evidence routing problem, feedback/repair problem, renderer problem, or shared core problem.
4. Identify whether several gaps share one root cause.
5. Write the confirmed root cause with concrete evidence.
6. Choose the smallest fix location.
7. Define a regression benchmark that must pass after the fix.
8. Implement the fix in a separate PR.
9. Re-run the full benchmark suite for collateral regressions.

## Analysis record format

```markdown
## ANALYSIS-GAP-QSM-0001

- Gap:
- Reproduced: YES | NO
- Cross-subtopic occurrences:
- Confirmed layer:
- Root cause:
- Why this is the root cause:
- Smallest durable fix:
- Files/contracts likely affected:
- Content migration required:
- Regression benchmark:
- Risks / anti-drift constraints:
- Decision:
- Fix PR:
- Re-benchmark result:
```

## Clustering questions

Before fixing individual gaps, ask:

- Are several `NOT_READY` results actually one missing content pattern?
- Are multiple routing failures caused by one prerequisite-graph assumption?
- Are several human-facing problems renderer issues rather than curriculum issues?
- Are external-provider cases being treated consistently across subjects?
- Are content gaps being confused with source gaps?
- Are learner estimates incorrectly affecting evidence anywhere?
- Are feedback failures tied to missing misconception records rather than runtime logic?
- Are fresh-verification failures caused by thin question inventory rather than feedback code?

The goal is **reverse engineering from benchmark behavior back to the smallest real defect**, not patching each failing case independently.

## Current state

Awaiting complete benchmark sweep across all currently mapped matrices.