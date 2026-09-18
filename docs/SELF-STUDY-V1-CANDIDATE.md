# Self-study v1 integration candidate

This branch is the consolidation point for the practical one-learner workflow.

It combines the implemented core path, current Issue #19 subject content, the Relative Motion
session-readiness audit, the thin study-session runner, the retained real-question C6 pilot,
and the revised concept/implementation notes.

## Intended vertical slice

```text
real worksheet/question set
→ transient question-to-capability mapping
→ prerequisite closure across matrices
→ explicit external-provider bridges
→ rough subtopic starting estimate
→ learner-facing study plan
→ attempt outcome supplied by evaluator
→ diagnose / repair / fresh verification
→ observation draft
→ simple delayed review date
```

## Deliberate boundaries

- Worksheet questions do not become curriculum authority automatically.
- Rough percentages are routing hints, never mastery evidence.
- Cross-matrix order comes from capability prerequisites, not rung numbers.
- `NOT_READY` matrices block self-study rather than receiving fabricated teaching.
- External-provider prerequisites remain explicit bridges.
- Free-form grading is outside the runner; the caller supplies the evaluated outcome.
- Learner observations are returned as drafts and are never persisted silently.
- Academic review/source-custody warnings remain distinct from private-family pilot readiness.
- No BKT/IRT, adaptive scheduler platform, or new mastery model is introduced.

## First usable subtopic

Relative Motion is the first validated session target. It is currently
`SESSION_READY_WITH_BRIDGE` because signed-coordinate arithmetic is owned by Mathematics
and remains visibly bridged.

The retained ExamSIDE Relative Motion question slice has been used to validate the complete
route and feedback loop without canonicalizing those external questions.

## Next decision point

After this branch is mechanically green, the next meaningful input is one actual learner
session. Future core changes should be justified by observed problems such as:

- starting too high or too low;
- wrong capability diagnosis;
- help that reveals too much;
- repair that misses the misconception;
- fresh verification that checks the wrong capability;
- awkward or insufficient learner-evidence capture.

Do not extend the architecture merely to increase feature coverage.
