# Agent A — Motion in 2D / Motion in a Plane semantic Atlas audit

> Status: **Agent A canonical-content packet**
>
> Date: 2026-09-19
>
> Grade9V3 packet: `MATRIX-PHY-KIN-2D-MOTION` / `BUCKET-PHY-KIN-2D-MOTION`
>
> External semantic reference inspected: Common PR #350 at commit
> `9c7d363d2ae2866ac829ae6b8039eeb8c1abc2c0`.

## Ownership boundary

This packet changes only subject-owned academic meaning:

- `Physics/library/phy-kin-2d-motion.v1.json`;
- `Physics/matrices/phy-kin-2d-motion.rungs.json`;
- subject-focused tests and this audit.

It does not change Shared schemas, planners, routing vocabularies, the Topic Atlas JavaScript,
or learner state.

## APP preflight

The current Topic Atlas application work is on `feat/nlm-topic-atlas`. Its projected data
does not yet contain `MATRIX-PHY-KIN-2D-MOTION`, `CAP-KIN-PROJECTILE-MODEL`, or the
Motion-in-2D packet.

The app contract was still useful: Level-2 semantic leaves are the canonical
`microtopic.teaching_path[]` steps, and diagnostic repair targets are expected to name
those stable step IDs.

Because Motion in 2D was not yet present in the app projection, Common PR #350 was used as
the fallback semantic reference requested by the owner.

## What Common PR #350 contributed

The useful reference is the Motion-in-a-Plane concept decomposition, especially:

| Common PR #350 concept | Grade9V3 ownership decision |
| --- | --- |
| `M2D_FOUNDATION` | existing R1 / `CAP-KIN-2D-INDEPENDENT-COMPONENTS` |
| `PROJECTILE_COMPONENT_CLOCK` | existing R1/R3 shared-clock semantics |
| `PROJECTILE_APEX` | R3 semantic leaf `K2D3-4` |
| `PROJECTILE_SAME_HEIGHT` | R3 semantic leaf `K2D3-5` |
| `PROJECTILE_HORIZONTAL_LAUNCH` | R3 semantic leaf `K2D3-6` |
| `PROJECTILE_TRAJECTORY` | **not imported**; trajectory-equation derivation remains outside this packet |
| `PROJECTILE_OUTFIELDER` | **not imported**; observer/relative-motion reasoning belongs to the existing relative-motion graph |
| `RELATIVE_MOTION_FOUNDATION` | **not duplicated**; already owned by the relative-motion package |

The Common repository is an authoring reference here, not curriculum authority and not
question custody. ExamSIDE remains the owner-approved real-question demand source for the
current Pinnacle preparation slice.

## Why the matrix remains three rungs

The prior three durable capabilities are still academically coherent:

1. represent one plane event as signed perpendicular components with one clock;
2. apply constant-acceleration kinematics component by component when valid;
3. select and use the gravity-only projectile specialization.

Common PR #350 supplies evidence that **multiple independently observable failures were
hidden inside R3**, but it does not require new capabilities for range, maximum height,
time of flight, horizontal launch or oblique launch.

Those are therefore exposed as stable semantic leaves and assessment families under the
existing projectile capability instead of becoming near-duplicate capabilities.

## Semantic leaves added or sharpened

### R1 — independent components

- `K2D1-1` — declare one frame, origin, axes and time origin;
- `K2D1-2` — encode signed component state;
- `K2D1-3` — separate axis histories while preserving one clock;
- `K2D1-4` — recombine only simultaneous components.

### R2 — 2D constant acceleration

- `K2D2-1` — validate constant acceleration **per axis**;
- `K2D2-2` — apply the 1D relations separately to x and y;
- `K2D2-3` — carry an event time found on one axis to the other axis.

### R3 — projectile model

- `K2D3-1` — select gravity-only free flight;
- `K2D3-2` — evolve horizontal and vertical components with one clock;
- `K2D3-3` — translate the requested event into a component condition;
- `K2D3-4` — apex: `v_y=0`, while `v_x` and downward acceleration remain;
- `K2D3-5` — same-height return: `Delta y=0`, with shortcut boundary explicit;
- `K2D3-6` — horizontal/unequal-height launch: obtain time from vertical motion;
- `K2D3-7` — reconstruct speed/direction/displacement from simultaneous components.

These are semantic leaves, not new learner-state dimensions.

## Canonical misconception coverage

The packet now explicitly diagnoses:

- two clocks for one event;
- combining x and y values from different instants;
- using acceleration magnitude as both component accelerations;
- treating one constant acceleration component as permission to use constant-a equations on
  both axes;
- horizontal force required to sustain horizontal projectile velocity;
- horizontal launch meaning vertical velocity stays zero;
- whole velocity or acceleration becoming zero at the apex;
- same-height shortcuts used for unequal-height landing;
- same height implying identical velocity vectors;
- horizontal speed controlling fall time.

## Practice and transfer inventory

One canonical family now owns five Core2A items and five Core2B items.

Core2A covers:

- shared-clock component state;
- componentwise constant acceleration;
- apex state;
- horizontal launch from height;
- same-height landing.

Core2B spans three declared transfer dimensions:

- `representation_translation` — verbal motion → signed x/y state;
- `model_choice` — per-axis constant-a validity and projectile-model validity;
- `reasoning_steps` — unequal-height impact and equal-height state comparison.

Model-choice hints are conceptual only; they do not hand over the assessed model choice.

All ten questions are Grade9V3 `AUTHORED` candidates. ExamSIDE/Common material supplies
demand/decomposition evidence only; no external question wording or exam identity is
copied into canonical question custody.

## Boundaries retained

This packet deliberately does **not** add:

- a separate capability for range;
- a separate capability for maximum height;
- a separate capability for time of flight;
- a separate horizontal-projectile capability;
- a separate oblique-projectile capability;
- trajectory-equation derivation;
- inclined-plane projectile geometry;
- moving-launcher frame conversion;
- river/rain relative-motion catalogues;
- circular-motion content;
- drag or variable gravity.

If later real learner evidence shows that one of the new semantic leaves fails repeatedly
and independently while the parent capability otherwise holds, that is evidence to revisit
capability granularity. It is not assumed in advance.
