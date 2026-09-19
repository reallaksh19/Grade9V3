# Grade 9 Pinnacle Vectors — ExamSIDE demand reconnaissance

> Status: **owner-approved preparation-demand reconnaissance**
>
> Date: 2026-09-19
>
> Source: `https://questions.examside.com/past-years/jee/jee-main/physics/vector-algebra`
>
> Authority: `docs/grade9/PINNACLE-EXAMSIDE-PREPARATION-AUTHORITY.md`

## Source snapshot

The inspected ExamSIDE Vector Algebra page exposes JEE Main PYQs from 2002–2026 and reports
39 questions across 37 papers.

This document uses the page only as real question-demand evidence. It does not copy the
question bank into Grade9V3 and does not relabel ExamSIDE as Pinnacle-issued material.

## Representative demand families observed

The visible PYQs contain repeated demand for:

- resolving a vector into perpendicular components from a stated magnitude/angle;
- adding and subtracting vectors and forces;
- obtaining resultant magnitude and direction;
- using perpendicularity/angle conditions between vectors;
- unit-vector notation and finding a unit vector in a specified direction;
- projection/component of one vector along another;
- vector relations that naturally invoke dot-product reasoning;
- plane-normal / cross-product style reasoning;
- three-dimensional geometric vector displacement;
- at least one calculus-style vector-function item.

The important curriculum-engineering point is that these are not eleven new capabilities.
They collapse into a smaller number of durable learner actions.

## Crosswalk against current Grade9V3

| ExamSIDE demand family | Current local representation | Decision | Reason |
| --- | --- | --- | --- |
| Resolve magnitude + angle into signed x/y components | `CAP-VEC-ANGLE-DECOMPOSITION` + `CAP-TRIG-RATIO-BRIDGE` | **REUSE** | Already authored from real Motion-in-a-Plane demand |
| Add signed components | `CAP-VEC-COMPONENT-SUM` | **REUSE** | Same learner action |
| Subtract vectors / subtraction order | `CAP-GRAPHICAL-SUBTRACT`, `CAP-VEC-SUB-ORDER` | **REUSE** | Context does not justify another capability |
| Resultant magnitude from perpendicular components | `CAP-RIGHT-TRIANGLE-BRIDGE` / existing resultant route | **REUSE** | Existing magnitude reconstruction is sufficient for orthogonal cases |
| Resultant direction from known components | current Vector bucket explicitly excludes inverse-trig direction recovery | **ENRICH / bounded AUTHOR candidate** | This is a distinct output decision and is repeatedly demanded |
| Unit-vector i/j notation | no durable local teaching capability | **AUTHOR candidate** | Small, reusable representation skill |
| Normalize a nonzero vector to unit direction | no durable local teaching capability | **AUTHOR candidate** | Independently fail-able and directly supports later mechanics |
| General projection / component along another vector | no local dot-product projection capability | **EXCLUDE_AT_CURRENT_DEPTH for first slice** | Useful JEE demand, but not needed to close current Grade-9 mechanics route |
| General dot-product angle/perpendicularity algebra | no local capability | **EXCLUDE_AT_CURRENT_DEPTH for first slice** | Keep visible as later Vector depth |
| Cross product / normal-to-plane reasoning | no local capability | **EXCLUDE_AT_CURRENT_DEPTH** | Higher representation/algebra burden; not needed by current Terminal-1 mechanics spine |
| Three-dimensional vector geometry | current active route is 2-D | **EXCLUDE_AT_CURRENT_DEPTH** | Separate depth expansion, not a repair of the present route |
| Calculus-based vector differentiation | explicitly outside current Motion-2-D slice | **EXCLUDE_AT_CURRENT_DEPTH** | Preserve current calculus boundary |

## Smallest high-value next Vector slice

Do **not** rebuild the Vector matrix around the ExamSIDE chapter taxonomy.

The smallest useful addition is:

```text
existing signed x/y components
        ↓
recover direction angle from components
        ↓
read/write i-hat / j-hat notation
        ↓
normalize a 2-D vector to its unit direction
```

The first item may be an enrichment of the current vector-operation route if the existing
capability boundaries can express it cleanly. Unit-vector notation and normalization should
be authored only if the counterfactual confirms they are independently fail-able learner
actions.

### Proposed bounded capability decisions

Candidate 1:

```text
CAP-VEC-DIRECTION-FROM-COMPONENTS
```

Learner action:

> Given signed x/y components, recover the vector's direction using the declared quadrant and
> an inverse-trigonometric ratio, rather than returning only a magnitude.

Likely prerequisite:

```text
CAP-VECTOR-SIGNED-COMPONENT
+ right-triangle / inverse-trig Mathematics bridge
```

Do not silently pretend the current basic trig-ratio bridge already certifies inverse trig.

Candidate 2:

```text
CAP-VEC-UNIT-NOTATION
```

Learner action:

> Translate between a 2-D component pair and compact i-hat / j-hat notation without changing
> the vector.

This is representation translation, not new Physics.

Candidate 3:

```text
CAP-VEC-UNIT-DIRECTION
```

Learner action:

> Divide a nonzero vector by its magnitude to produce a dimensionless unit vector in the same
> direction and verify magnitude 1.

Prerequisites should reuse:

- signed components;
- magnitude from perpendicular components;
- unit-vector notation.

## What not to author in the same PR

Keep the next production slice bounded. Do not add simultaneously:

- general dot product;
- scalar projection formula;
- cross product;
- 3-D vector algebra;
- calculus/vector-function differentiation.

Those are genuine ExamSIDE demands, but mixing them into the first Vector repair would turn a
small preparation gap into a broad JEE Vector course.

## Micro-scope consequences

The current Terminal-1 planning file should now treat the following as externally confirmed
preparation demand:

- arbitrary-angle decomposition;
- recover vector/resultant direction from components;
- unit-vector notation / unit direction.

Their `school_micro_demand` remains `MICRO_TO_CONFIRM` unless Pinnacle-issued evidence
confirms them.

## Recommended next production PR

After this reconnaissance is accepted:

1. inspect whether inverse-trig direction recovery should enrich the current
   `BUCKET-PHY-VEC-ADD-SUB` or receive one additional rung;
2. author i/j representation and 2-D unit-direction normalization as the smallest coherent
   new learner slice;
3. retain explicit Mathematics bridges rather than hiding trig/inverse-trig prerequisites;
4. add one or two ExamSIDE-derived demand fixtures as transient mappings, not canonical
   question custody;
5. add focused tests proving dot/cross/calculus content does not leak into this slice.

## Stop condition

Stop after the bounded direction/unit-vector slice is session-ready.

Further Vector Algebra breadth should wait for either:

- direct learner evidence;
- later JEE preparation staging;
- a new owner instruction changing the depth boundary.
