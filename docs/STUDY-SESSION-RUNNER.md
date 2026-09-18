# Practical study-session runner

`Shared/tools/study_session.py` is a thin orchestration layer over the existing core.
It does not create new curriculum truth, grade free-form answers, or silently update learner
state.

The intended loop is:

```text
worksheet capability map
→ session-readiness check
→ rough starting estimate / existing learner evidence
→ ordered study route
→ worksheet attempt
→ diagnosis / repair / fresh verification
→ observation draft
→ review date
```

## First supported pilot: Relative Motion

Relative Motion is currently `SESSION_READY_WITH_BRIDGE`.

The local Relative Motion matrix has teaching, Core1A/Core1B reconstruction, misconception
diagnosis/repair, and exit verification on all four rungs. Signed-coordinate arithmetic is
kept visible as a Mathematics bridge rather than assumed mastered.

A rough parent estimate can use the subtopic name directly:

```bash
python3 Shared/tools/study_session.py plan \
  --map tests/fixtures/study_session/relative-motion.worksheet.json \
  --estimate "Relative motion=60" \
  --readable
```

The estimate chooses where to try first inside the matrix. It never marks earlier
capabilities demonstrated.

## Validity versus execution readiness

The plan now keeps two different ideas separate:

- `valid=true`: the worksheet route and capability delivery graph are structurally sound;
- `ready=true`: the plan is valid and every external-provider prerequisite needed for this
  learner is already satisfied.

A Relative Motion plan can therefore be valid while still returning `ready=false` and a
Mathematics bridge as the first action. If learner evidence already demonstrates that
prerequisite, the same route becomes ready and the bridge is skipped.

All prerequisite delivery decisions use the shared `capability_delivery` resolver rather
than reimplementing bridge logic in the session layer.

## Record one attempt

The runner does not decide whether a free-form answer is correct. A human or another
approved evaluator supplies the outcome.

Example: the learner ignored direction in a relative-velocity question.

```bash
python3 Shared/tools/study_session.py attempt \
  --map tests/fixtures/study_session/relative-motion.worksheet.json \
  --question SCHOOL-REL-Q1 \
  --result INCORRECT \
  --failed-capability CAP-RELATIVE-V \
  --error-stage CONCEPT \
  --response-summary "Subtracted the speeds as scalars and ignored direction." \
  --when 2026-09-18 \
  --readable
```

For a transient worksheet question there is no invented hint ladder. The runtime diagnoses
from the canonical microtopic. If a misconception is then confirmed, pass its index:

```bash
python3 Shared/tools/study_session.py attempt \
  --map tests/fixtures/study_session/relative-motion.worksheet.json \
  --question SCHOOL-REL-Q1 \
  --result INCORRECT \
  --failed-capability CAP-RELATIVE-V \
  --error-stage CONCEPT \
  --misconception-index 0 \
  --when 2026-09-18 \
  --readable
```

The result may include a canonical repair, a fresh verification question or exit task, an
observation draft, and a review date.

## Safety / anti-drift rules

- `NOT_READY` teaching matrices block the session rather than being filled with invented
  teaching.
- `PILOT_READY` remains visibly weaker than `SESSION_READY`.
- External worksheet questions remain transient demand; they are not automatically promoted
  to Core2/source custody.
- External-provider prerequisites remain explicit bridges.
- Rough percentages are routing hints, never mastery evidence.
- Attempt evaluation is supplied by the caller.
- Observation drafts are returned but never written automatically.
- Academic/source warnings remain visible to the parent even when a private pilot is
  mechanically executable.

## What comes next

Use the runner on a real Relative Motion worksheet before broadening it. The next core
change should be justified by an observed problem in that session: wrong starting point,
bad diagnosis, over-revealing help, unsuitable verification, or awkward evidence capture.
