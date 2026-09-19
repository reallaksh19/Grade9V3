# Grade 9 Pinnacle Motion 1 D — ExamSIDE demand reconnaissance

> Status: **owner-approved preparation-demand reconnaissance**
>
> Date: 2026-09-19
>
> Source: `https://questions.examside.com/past-years/jee/jee-main/physics/motion-in-a-straight-line`
>
> Authority: `docs/grade9/PINNACLE-EXAMSIDE-PREPARATION-AUTHORITY.md`

## Source snapshot

The inspected ExamSIDE JEE Main Motion in a Straight Line page reports 123 questions across
107 papers from 2002–2026.

Visible recent questions repeatedly exercise:

- distance versus displacement;
- average speed and average velocity under unequal distance/time partitions;
- position-time and velocity-time graph interpretation;
- signed one-dimensional relative velocity;
- constant-acceleration stopping/braking;
- vertical motion under gravity;
- turning-point reasoning;
- multi-stage motion;
- equations involving displacement/velocity as functions of time;
- some higher-depth variable-acceleration/calculus-style demand.

This source is used as preparation-demand evidence. It is not relabelled as Pinnacle-issued
micro-syllabus evidence.

## Crosswalk against current Grade9V3

| ExamSIDE demand family | Current local representation | Decision |
| --- | --- | --- |
| Distance versus displacement | `CAP-KIN-DISTANCE-DISPLACEMENT` | **REUSE** |
| Average speed versus average velocity | `CAP-KIN-AVERAGE-RATES` | **REUSE** |
| Position-time / velocity-time graph interpretation | `CAP-KIN-MOTION-GRAPHS` | **REUSE** |
| Uniformly accelerated straight-line motion | `CAP-KIN-CONSTANT-ACCELERATION` | **REUSE** |
| Braking/stopping-distance questions | constant-acceleration model + sign convention | **QUESTION_VARIATION** |
| Vertical 1-D motion under gravity | `CAP-KIN-CONSTANT-ACCELERATION` + `CAP-PHY-GRAV-FREE-FALL-G` | **ENRICH / bridge route** |
| Zero instantaneous velocity at a turning point with nonzero acceleration | `CAP-KIN-ZERO-V-NONZERO-A` | **REUSE AS DEMAND-BACKED EXTENSION** |
| Straight-line relative velocity | existing relative-motion capability family | **REUSE CROSS-BUCKET** |
| Multi-stage train/car motion | current rate/graph/constant-acceleration capabilities | **QUESTION_VARIATION / composite use** |
| Position/velocity functions requiring differentiation or `a=v,dv/dx` | outside current Grade-9 depth | **EXCLUDE_AT_CURRENT_DEPTH** |
| Elementary uniform circular motion | not part of the inspected straight-line demand family | **NO NEW EXAMSIDE CLAIM** |

## Academic conclusion

The current Grade9V3 Motion-1D spine is already structurally strong.

Unlike Motion-2D and NLM, this reconnaissance does **not** justify a new production capability
spine.

The main high-value action is to improve/verify routing and question variation around two
areas:

1. vertical one-dimensional motion under gravity with a consistent sign convention;
2. turning-point questions where instantaneous velocity is zero but acceleration is not.

Both can reuse existing capabilities.

## Recommended smallest follow-up

Do not create a new Motion-1D matrix or a new capability merely because ExamSIDE has many
questions.

Instead:

```text
approved ExamSIDE demand
→ transient representative question mappings
→ current Motion-1D / Gravitation / Relative-Motion capabilities
→ verify prerequisite order and fresh-question coverage
```

If a real question exposes a missing learner action after that mapping, author only that gap.

### Vertical-motion route

Use:

```text
declare + direction
→ apply signed constant acceleration
→ gravity bridge/model
→ interpret zero velocity at apex without setting acceleration to zero
```

The existing `CAP-KIN-ZERO-V-NONZERO-A` should remain a real demand-backed diagnostic/extension
rather than being forced into every ordinary straight-line session.

### Relative-motion route

Do not duplicate straight-line relative velocity inside the Motion-1D matrix.

Use the existing relative-motion capability family when the question's difficult move is
observer-relative velocity rather than ordinary one-body kinematics.

## Boundaries

Do not pull into the current Grade-9 Motion-1D slice:

- calculus differentiation/integration;
- general variable-acceleration differential equations;
- `a=v,dv/dx` as a default technique;
- higher-depth function analysis merely because the PYQ page contains it.

These are valid JEE demands at later depth, but they are not repairs of the current Grade-9
preparation route.

## Micro-scope consequences

The following may now be marked as owner-approved ExamSIDE preparation demand while leaving
`school_micro_demand = MICRO_TO_CONFIRM`:

- distance versus displacement;
- average speed versus average velocity;
- motion graphs;
- constant-acceleration model/equations;
- vertical one-dimensional gravity motion;
- zero-velocity/nonzero-acceleration turning-point reasoning.

No ExamSIDE preparation claim is added here for elementary uniform circular motion from the
Motion-in-a-Straight-Line page.

## Agent-A vertical-gravity closure

The bounded vertical-motion follow-up is now represented without a new capability. The local
route reuses `CAP-KIN-CONSTANT-ACCELERATION`, `CAP-PHY-GRAV-FREE-FALL-G` and
`CAP-KIN-ZERO-V-NONZERO-A`, with a dedicated application context and practice family.

The added preparation distinguishes:

- the magnitude `g>0` from the signed acceleration chosen by the coordinate axis;
- velocity reversal from acceleration reversal;
- the apex condition `v=0` from the false conclusion `a=0`;
- signed displacement from total distance;
- algebraic roots from the future physical event;
- equation and velocity-time-graph representations of the same constant-g motion.

This changes **local preparation readiness only**. It does not promote the school micro-demand
beyond `MICRO_TO_CONFIRM`.

## Stop condition

Stop after representative straight-line ExamSIDE questions map cleanly through the existing
capabilities.

No new Motion-1D production capability should be authored unless later mapping or learner
evidence reveals a specific independently fail-able gap.
