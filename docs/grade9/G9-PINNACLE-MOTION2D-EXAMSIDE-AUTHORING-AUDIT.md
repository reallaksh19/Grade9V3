# Grade 9 Pinnacle Motion in 2 D — ExamSIDE authoring audit

> Status: **owner-approved question-demand slice**
>
> Date: 2026-09-19
>
> School authority remains separate: the Pinnacle portion sheet confirms the chapter label
> `Motion in 2 D`; ExamSIDE is used here because the owner explicitly approved it as a
> reliable external source for worksheet/question demand.

## Reliable question-demand source

ExamSIDE Motion in a Plane:

`https://questions.examside.com/past-years/jee/jee-main/physics/motion-in-a-plane`

At inspection time the page exposed JEE Main PYQs spanning 2002–2026 and multiple concrete
families: projectile range/height/time, horizontal launch, later-time projectile velocity,
relative motion, vector-resultant demand and x-y constant acceleration.

The first authoring slice uses four representative source cases only:

| Source case | Durable learner demand |
| --- | --- |
| 2023-04-11 projectile velocity after time | angle decomposition + projectile component model |
| 2023-02-01 horizontal projectile from cliff | independent x/y motion + projectile model |
| 2020-09-04 x-y constant acceleration | component-wise constant acceleration with one common time |
| 2026-04-08 equal-range/different-flight-time projectiles | projectile model and component reasoning |

Question text is not copied into canonical content. The fixture stores concise demand summaries
and source URLs.

## Capability response

The smallest durable spine is:

```text
CAP-VEC-ANGLE-DECOMPOSITION
        ↓
CAP-KIN-2D-INDEPENDENT-COMPONENTS
        ↓
CAP-KIN-2D-CONSTANT-ACCELERATION
        ↓
CAP-KIN-PROJECTILE-MODEL
```

The first capability lives in the existing vector-operation matrix. The remaining three live
in the new `MATRIX-PHY-KIN-2D-MOTION`.

## Deliberate reuse

- signed-axis reading is reused from `CAP-VECTOR-SIGNED-COMPONENT`;
- sine/cosine projection is represented as `CAP-TRIG-RATIO-BRIDGE` with Mathematics
  provider review still visible;
- one-dimensional constant-acceleration model reasoning is reused through
  `CAP-KIN-CONSTANT-ACCELERATION`;
- right-triangle magnitude checking remains an existing bridge;
- relative-motion capabilities are not duplicated.

## What is not a separate capability

The following stay applications/controlled variations of the projectile model:

- horizontal launch;
- oblique launch;
- time of flight;
- maximum height;
- horizontal range;
- later-time speed/direction.

A separate capability should be added only if future real-question or learner evidence shows a
new independently fail-able decision.

## First-slice exclusions

- calculus-based position-vector differentiation;
- trajectory-equation derivation;
- drag;
- variable gravity;
- inclined-target projectile geometry;
- dot/cross product.

## Evidence boundary

ExamSIDE can now authorize local question-demand content because the owner approved it as
reliable. It still does not mutate the school evidence field:

```text
school_micro_demand = MICRO_TO_CONFIRM
external_question_demand = CONFIRMED_EXAMSIDE
```

That distinction prevents external JEE breadth from being misreported as a Pinnacle-issued
syllabus while still allowing real questions to drive useful Grade-9 Pinnacle preparation.
