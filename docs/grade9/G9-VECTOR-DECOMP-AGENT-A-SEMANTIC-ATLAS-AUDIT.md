# Agent A — Vector decomposition / initial-velocity representation semantic Atlas audit

> Status: **Agent A canonical-content packet**
>
> Date: 2026-09-19
>
> Grade9V3 packet: `MATRIX-PHY-VEC-ADD-SUB` / `BUCKET-PHY-VEC-ADD-SUB`, R4
>
> Downstream consumer boundary checked against: `MATRIX-PHY-KIN-2D-MOTION`
>
> External semantic reference inspected: Common PR #350 at commit
> `9c7d363d2ae2866ac829ae6b8039eeb8c1abc2c0`.

## Ownership boundary

This packet changes subject-owned academic meaning only:

- `Physics/library/phy-vec-add-sub.v1.json`;
- `Physics/matrices/phy-vec-add-sub.rungs.json`;
- subject-focused tests and this audit.

It does not create a Shared learner-state type, diagnostic vocabulary, Core route,
webpage rule, or new permanent mastery skill.

The durable capability remains `CAP-VEC-ANGLE-DECOMPOSITION`. Initial velocity does
not receive a second decomposition capability merely because projectile problems consume
the resulting components.

## Why this packet exists

The previous Motion-in-2D packet deliberately accepts already-resolved `u_x,u_y`
values when it begins projectile evolution. The immediate upstream academic question is
therefore narrower than "teach more vectors":

> What exactly must the learner be able to do before Motion-in-2D may treat an initial
> velocity as a signed component state?

The answer is representation conversion, not another motion law.

Common PR #350 provides a useful boundary witness: the projectile problem-family route
contains a REPRESENT step that resolves initial velocity/displacement into components
before projectile-model selection and time evolution. Grade9V3 keeps that ordering while
retaining its own canonical capability IDs and content ownership.

## Capability decision

No new capability is added.

`CAP-VEC-ANGLE-DECOMPOSITION` already owns the durable learner action:

- start from a magnitude-angle vector;
- bind the angle to its actual reference axis;
- project onto perpendicular components;
- preserve direction through component signs;
- verify the component representation.

The packet sharpens this capability rather than introducing:

- `CAP-VEC-INITIAL-VELOCITY`;
- a projectile-specific vector-decomposition capability;
- separate capabilities for angle-from-x versus angle-from-y;
- separate quadrant capabilities.

Those distinctions change the reasoning inside one representation action, but do not
justify separate permanent mastery nodes.

## Stable semantic leaves

R4 now exposes five meaningful actions:

- `VAD-1` — decide whether decomposition is needed at all; if signed components are
  already supplied, preserve them rather than applying trigonometry again;
- `VAD-2` — identify the angle reference and therefore which component direction is
  adjacent/opposite;
- `VAD-3` — compute the perpendicular component magnitudes with the corresponding
  cosine/sine projection;
- `VAD-4` — attach signs from the declared axes and bind the pair to the vector role
  named by the problem; for initial velocity this means `u_x,u_y` at the initial
  instant;
- `VAD-5` — reconstruct magnitude/quadrant to verify that the component pair represents
  the original vector.

These are stable curriculum addresses. They are not learner mastery dimensions.

## Boundary with Motion in 2D

The academically important handoff is:

```text
magnitude + direction
        |
        v
CAP-VEC-ANGLE-DECOMPOSITION
        |
        | produces an equivalent signed vector state
        | e.g. u_x, u_y at t=0
        v
CAP-KIN-2D-INDEPENDENT-COMPONENTS
        |
        v
CAP-KIN-2D-CONSTANT-ACCELERATION
        |
        v
CAP-KIN-PROJECTILE-MODEL
```

Vector decomposition answers:

> What are the signed components of this vector in this declared frame?

It does **not** answer:

> How do those components evolve with time?

Therefore:

- `u_x=u cos(theta)`, `u_y=u sin(theta)` describes the initial velocity state for a
  launch angle measured from +x in the stated quadrant;
- whether later `v_x` remains equal to `u_x` depends on the motion model;
- whether later `v_y` changes, and how, depends on the motion model;
- projectile specialization remains downstream academic ownership.

This boundary prevents vector content from silently teaching projectile dynamics and
prevents Motion-in-2D from duplicating generic vector projection.

## Canonical misconception coverage

R4 now distinguishes four materially different wrong routes:

1. **angle-reference error** — "x always uses cosine";
2. **sign error** — treating sine/cosine output as already carrying the required
   coordinate signs;
3. **representation-choice error** — applying trigonometric decomposition even when a
   signed component pair is already supplied;
4. **state/evolution boundary error** — assuming that resolving an initial velocity into
   `u_x,u_y` proves those components remain constant later.

The fourth misconception is deliberately repaired by pointing to the boundary rather than
teaching downstream projectile equations inside the vector packet.

## Controlled variations

R4 now varies one meaningful feature at a time:

- reference angle 30° versus 60°;
- reference axis +x versus +y for the same physical vector;
- quadrant/sign while holding the component magnitudes;
- vector role (velocity, force, displacement) while preserving projection geometry;
- magnitude-angle input versus already-supplied signed components;
- generic velocity versus explicitly initial velocity.

The last two are especially important. They test whether the learner can decide when the
operation applies and where its academic ownership ends.

## Practice and transfer inventory

A new canonical family,
`FAM-PHY-VEC-ANGLE-DECOMP-PRACTICE`, contains ten Grade9V3-authored candidates:

- five Core2A practice items;
- five Core2B transfer items.

Core2A covers:

- angle measured from +x;
- angle measured from +y;
- quadrant-II signs;
- quadrant-IV signs;
- initial-velocity component state.

Core2B spans:

- `representation_translation` — verbal compass direction, force-context reuse and a
  non-default axis convention;
- `model_choice` — deciding that no magnitude-angle decomposition is needed when
  components are already supplied;
- `reasoning_steps` — proving that complementary angle descriptions of one unchanged
  vector produce the same components.

The model-choice transfer item exposes only a `CONCEPT` hint, so the hint does not hand
over the decision being assessed.

All ten items are `AUTHORED`. ExamSIDE supplies real Motion-in-a-Plane demand evidence
only. Common PR #350 is a semantic-boundary reference only. No external question wording
or exam identity is copied into canonical question custody.

## Deliberate exclusions

This packet does **not** add or absorb:

- inverse-trigonometric direction recovery from components;
- dot product;
- cross product;
- non-orthogonal basis resolution;
- later-time kinematic evolution;
- projectile event selection;
- relative-motion frame conversion;
- trajectory-equation derivation.

If later learner evidence shows a repeated, instructionally distinct failure hidden inside
one of VAD-1..VAD-5, that is evidence to reconsider the leaf decomposition. It is not a
reason to pre-emptively create another capability.
