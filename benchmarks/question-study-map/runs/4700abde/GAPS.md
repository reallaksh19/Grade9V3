# Gap status — post fallback-first full rerun

Baseline: `4700abdefecefd6211488a527594dabba8797e89`

This file records benchmark observations only. It does not perform new root-cause analysis or production repair.

## GAP-QSM-0001 — retained question inventory backlog

**PERSISTS.**

Seven dormant Physics matrices still lack retained canonical question inventory for a direct real/canonical question-demand benchmark. The fallback-first runtime does not change this content/evidence backlog.

Disposition: demand-gated; no blanket question manufacture.

## GAP-QSM-0002 — incomplete subject-content migration

**PERSISTS, narrowed.**

Eight Physics matrices remain `NOT_READY` because durable teaching rungs are still incomplete:

- Current electricity / Ohm's law
- Fluid statics / buoyancy / Bernoulli
- Universal gravitation
- Magnetic fields / Lorentz force / induction
- Reflection / spherical mirrors
- Oscillations / SHM / waves
- Rotational dynamics
- Thermodynamics / heat engines

Vector Add/Sub is no longer in this backlog after PR #56.

The new runtime behavior does not hide these gaps. It only changes execution granularity:

- represented demanded rung with safe teaching → `EXECUTE_WITH_FALLBACK`;
- missing/ambiguous demanded teaching → `OWNER_DECISION`;
- dependent capability cannot leap over that owner decision.

Disposition: demand-gated content backlog; no blanket fill.

## GAP-QSM-0003 — Vector Representation capability ambiguity

**REMAINS RESOLVED.**

Distinct capability ownership continues to prevent the previous duplicate teaching-location ambiguity.

## GAP-QSM-0004 — Vector Representation reconstruction coverage

**REMAINS RESOLVED.**

Core1A/Core1B reconstruction and verification support remains available for the active vector-representation rungs.

## New gap check after PRs #60–#62

**No new benchmark gap family recorded.**

The new runtime semantics are conservative at both execution and evidence boundaries. In particular, a correct attempt without a canonical fresh-verification path is retained as `UNCERTAIN`, not promoted to `DEMONSTRATED`.

## Benchmark-agent boundary

No `Shared/**`, `Physics/**`, `Mathematics/**`, schema, learner-profile, source-custody or production-content file is changed by this rerun.
