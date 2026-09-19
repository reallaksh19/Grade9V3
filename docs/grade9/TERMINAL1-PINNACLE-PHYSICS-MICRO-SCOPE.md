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

### Question-demand extension now locally authored

Owner approval on 2026-09-19 accepts ExamSIDE past-year questions as a reliable external question-demand source. Selected Motion-in-a-Plane questions now justify `CAP-VEC-ANGLE-DECOMPOSITION`, backed by an explicit Mathematics trigonometric-ratio bridge.

Still unconfirmed for Pinnacle school scope:

- a separate inverse-trig direction-angle reconstruction capability;
- unit-vector `i/j` notation, unless school material or a selected reliable question requires it.

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

### Owner-approved external question-demand slice

ExamSIDE JEE Main Motion-in-a-Plane PYQs are now accepted by the owner as a reliable question-demand source. A selected worksheet slice has therefore justified and closed the first durable local gaps:

1. `CAP-VEC-ANGLE-DECOMPOSITION`;
2. `CAP-KIN-2D-INDEPENDENT-COMPONENTS`;
3. `CAP-KIN-2D-CONSTANT-ACCELERATION`;
4. `CAP-KIN-PROJECTILE-MODEL`.

This changes **local capability state**, not Pinnacle school authority: the chapter-internal school rows stay `MICRO_TO_CONFIRM` until school-issued evidence confirms them.

Range, maximum height, time of flight, horizontal launch and oblique launch remain applications/question variations of the projectile model unless learner evidence proves a separate capability is needed.

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


## Motion-in-2D evidence reconnaissance

The current evidence decision for Motion in 2D is recorded in:

`docs/grade9/TERMINAL1-PINNACLE-MOTION2D-RECON.md`

The existing ExamSIDE Motion-in-a-Plane source is now owner-approved as a **reliable external question-demand source**. It can authorize bounded capability authoring and worksheet mapping for selected real questions. It is still not Pinnacle school-issued authority, so `school_micro_demand` remains separate and may stay `MICRO_TO_CONFIRM`.

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
