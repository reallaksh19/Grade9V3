# Agent A — NLM friction semantic Atlas audit

> Status: **Agent A canonical-content packet**
>
> Date: 2026-09-19
>
> Grade9V3 packet: `MATRIX-PHY-NLM-FIRST-LAW` / `BUCKET-PHY-NLM-FIRST-LAW`
>
> Scope: the friction rungs only — qualitative contact friction (R5) and bounded quantitative
> static/kinetic friction (R8).

## Ownership boundary

This packet changes only subject-owned academic meaning:

- `Physics/library/phy-nlm-first-law.v1.json`;
- `Physics/matrices/phy-nlm-first-law.rungs.json`;
- subject-focused tests and this audit.

It does not change Shared schemas, routing, learner state, Topic Atlas JavaScript, the
diagnostic vocabulary, or Core-selection semantics.

Connected-body, ideal-string and pulley capabilities remain separate canonical owners. They
may appear as secondary context in a friction question, but this packet does not rewrite them.

## Why friction is the next packet

Motion in 2D and vector decomposition already have Agent-A semantic packets. Friction had
sound canonical concepts but comparatively thin action-specific practice and transfer coverage.

The existing durable split is academically useful and is retained:

```text
CAP-NLM-FRICTION
    qualitative contact-level existence/direction
        ↓
CAP-NLM-FRICTION-QUANT
    normal reaction → no-slip demand → static feasibility → kinetic branch
```

No new friction capability is introduced.

## Stable semantic leaves

### R5 — qualitative contact friction

- `NLM5-1` — choose the body and named contact before assigning friction;
- `NLM5-2` — infer relative sliding or slip tendency if friction were absent;
- `NLM5-3` — use a counterexample to reject "friction always opposes velocity";
- `NLM5-4` — allow zero friction when no tangential contact force is required.

The fourth leaf is important because "rough contact" and "nonzero friction" are not equivalent.
It is still a semantic action under the existing capability, not a second mastery skill.

### R8 — quantitative static/kinetic friction

- `NLM8-1` — obtain the actual normal reaction from the perpendicular dynamics;
- `NLM8-2` — solve the friction required by a provisional no-slip state;
- `NLM8-3` — compare that demand with `mu_s N`;
- `NLM8-4` — use limiting-static equality only at impending slip and kinetic friction only
  after sliding is established.

This keeps the important learner failures separate without turning normal reaction, limiting
friction and kinetic friction into independent permanent capabilities.

## Misconception coverage

The friction packet now distinguishes these routes explicitly:

- friction always points opposite the object's velocity;
- rough surfaces in contact must always exert nonzero friction;
- friction always equals `mu N`;
- the normal force is always `mg`;
- the presence of `mu_s` or `mu_k` tells the learner which contact-state model to use.

Those errors require different repair prompts even though they live under only two durable
capabilities.

## Practice and transfer inventory

The friction slice now has five Core2A items and five Core2B items when filtered by primary
friction capability.

Core2A covers:

- conveyor-belt friction direction;
- zero-friction rough contact;
- sub-limit static friction as a responsive force;
- established-sliding kinetic friction;
- a stacked-block no-slip threshold.

Core2B covers:

- unknown contact-state selection under an angled pull;
- shoe/ground friction as a changed representation/context;
- deciding that moving rough contact can still require zero friction;
- an angled push that changes the normal reaction and the static threshold;
- moving the applied force to the other body in a stacked-block system.

The transfer set uses `representation_translation`, `model_choice`, and `reasoning_steps`.
Model-choice hints remain conceptual only and do not hand over the assessed branch.

All questions remain Grade9V3 `AUTHORED` candidates. Existing ExamSIDE references remain
preparation-demand provenance where applicable; no external question wording is copied into
canonical custody.

## Matrix sharpening

R5 now requires an explicit zero-friction rough-contact case.

R8 now requires a genuine contact-state decision and an example where the normal reaction must
be solved rather than assumed. Controlled variation also makes these two boundaries visible.

## Boundaries retained

This packet deliberately does **not** add:

- a zero-friction capability;
- a normal-reaction capability;
- separate static-friction and kinetic-friction capabilities;
- rolling-resistance or drag models;
- an inclined-plane catalogue;
- a coefficient/formula taxonomy;
- connected-body, string or pulley re-authoring;
- learner-specific mastery fields.

A connected-body problem may be used as a transfer context when friction is the primary
decision. The connected-body capability remains a secondary prerequisite/context owner rather
than being absorbed into friction.

## Stop condition

The friction decomposition is now sufficiently fine for the present evidence:

- concept-level direction/existence failures route to R5 leaves;
- magnitude/state-selection failures route to R8 leaves;
- the practice inventory distinguishes routine repair from changed-demand transfer.

Further atomisation should wait for real learner evidence showing another independently
repeating friction failure that changes the study response.

The next Agent-A packet should therefore move to **NLM connected systems / ideal-string
constraints**, not add more friction IDs.
