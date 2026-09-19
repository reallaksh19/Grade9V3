# Grade 9 Terminal-1 Pinnacle Physics — micro-scope plan

> Status: **planning only**
>
> Immediate school chapter boundary:
>
> ```text
> Vectors
> Motion 1 D
> Motion in 2 D
> NLM
> ```
>
> Source transcription:
> `docs/grade9/sources/TERMINAL1-PORTION-SHEET-2026-27.md`
>
> Machine-readable working sheet:
> `docs/grade9/terminal1-pinnacle-physics.micro-scope.json`

## Why this exists

The school portion sheet changes the immediate Grade-9 priority, but only at chapter level.

The repository must not convert a broad chapter title into an invented detailed syllabus.
Therefore this plan keeps **two independent axes**:

```text
SCHOOL DEMAND
CHAPTER_CONFIRMED
MICRO_TO_CONFIRM

LOCAL CAPABILITY
LOCAL_READY
LOCAL_READY_WITH_BRIDGE
LOCAL_PARTIAL
LOCAL_GAP
LOCAL_EXTENSION_AVAILABLE
```

These labels are planning language only. They are not new runtime states, matrix fields,
learner-evidence states or curriculum-authority enums.

## Vectors

### Reuse now if the school material demands it

- scalar versus vector information — `CAP-VECTOR-VS-SCALAR`;
- declared axes and signed components — `CAP-VECTOR-SIGNED-COMPONENT`;
- graphical subtraction — `CAP-GRAPHICAL-SUBTRACT`;
- component-wise addition — `CAP-VEC-COMPONENT-SUM`;
- resultant-component constraints — `CAP-VEC-RESULTANT-CONSTRAINT`;
- subtraction order — `CAP-VEC-SUB-ORDER`;
- perpendicular magnitude/right-triangle reasoning — existing Mathematics bridge.

### Local gaps to author only after school demand is confirmed

- arbitrary-angle trigonometric decomposition into x/y components;
- a durable direction-angle reconstruction action;
- unit-vector `i/j` notation, if the Pinnacle chapter actually assesses it.

The arbitrary-angle decomposition gap is the most consequential because it also gates
inclined-plane NLM and ordinary projectile setup.

## Motion 1 D

### Locally ready

- distance versus displacement;
- average speed versus average velocity;
- position-time / velocity-time graph interpretation;
- constant-acceleration model choice and equations;
- elementary uniform circular motion.

### Boundaries

- zero velocity with nonzero acceleration remains a useful retained diagnostic extension and
  is not automatically inserted into the ordinary route;
- vertical one-dimensional gravity problems appear supportable by current kinematics +
  gravitation capabilities, but should be mapped from real school questions before creating
  any new capability.

## Motion in 2 D

### Locally usable now

- vector representation/components;
- vector addition/subtraction;
- same-time relative position;
- relative velocity;
- resultant-direction/component constraints.

These existing routes still carry their declared Mathematics bridges where relevant.

### Confirmed local content gaps

The repository itself already records the following as missing durable subject content:

1. arbitrary-angle trigonometric vector decomposition;
2. independence of orthogonal x/y motions coupled by common time;
3. two-dimensional constant-acceleration component solving;
4. projectile-model selection.

If the Pinnacle chapter confirms projectile demand, the smallest durable teaching spine
should be built around those decisions. Do **not** create separate capabilities merely for
time of flight, maximum height and range unless real learner/question evidence shows that
they are independently fail-able actions.

Potential projectile applications to confirm:

- horizontal projection;
- oblique projection;
- time of flight;
- maximum height;
- horizontal range;
- velocity magnitude/direction at a later time;
- trajectory relation.

A calculus-style position-vector derivative problem remains out of scope unless the school
material explicitly demands it.

## NLM

### Locally ready

- Newton I / zero-net-force motion;
- balanced versus unbalanced force;
- one-body free-body-diagram ownership;
- friction direction from contact slip/tendency;
- Newton II signed net-force reasoning;
- Newton III interaction pairs.

The accelerating-frame/pseudo-force capability remains a non-default extension.

### Demand to confirm before authoring

- quantitative normal-reaction families beyond the existing FBD action;
- inclined-plane dynamics;
- two-body contact systems;
- tension / connected bodies;
- pulley constraints;
- coefficient-based static/kinetic friction calculations;
- momentum/impulse if the school's NLM chapter includes it.

Connected systems and pulley constraints are local gaps, but **a gap is not automatically a
school requirement**.

## Practical priority once school micro-demand arrives

```text
1. map every real school micro-demand to an existing capability
2. reuse exact matches
3. enrich only when an existing learner action is too shallow
4. create a new capability only for an independently fail-able action
5. keep story/context variations as questions, not capabilities
6. leave anything not evidenced by school material as MICRO_TO_CONFIRM
```

If the school material confirms the common Pinnacle pattern, the likely highest-value gap
order is:

```text
arbitrary-angle vector decomposition
        ↓
independent x/y motion
        ↓
2D constant-acceleration model
        ↓
projectile model selection/applications

then, only if school NLM demands them:

incline decomposition
connected-body tension
pulley constraints
quantitative friction families
```

This ordering is provisional until the chapter contents/worksheets arrive.

## Evidence still needed

Any one of these can promote micro-demand from `MICRO_TO_CONFIRM`:

- Pinnacle chapter contents/index;
- classwork/workbook pages;
- teacher revision sheet;
- Terminal-1 sample/prior paper;
- real school worksheet/question set.

The next artifact should be a **school demand → capability crosswalk**, not another framework
layer.


## Promotion protocol

When additional school material arrives, use:

`docs/grade9/TERMINAL1-PINNACLE-DEMAND-INTAKE.md`

The promotion rule is deliberately narrow:

```text
explicit school learner action
→ exact capability comparison
→ REUSE / ENRICH / AUTHOR / QUESTION_VARIATION / HOLD_UNCONFIRMED
```

No `MICRO_TO_CONFIRM` row is promoted merely because it is plausible inside a chapter title.
