# Grade 9 Terminal-1 Pinnacle Physics — Motion in 2D evidence reconnaissance

> Status: **evidence reconnaissance only**
>
> School demand state: **chapter confirmed; micro-demand unconfirmed**
>
> Authoring disposition: **HOLD_UNCONFIRMED**

## Question being answered

Does current evidence justify authoring projectile/general 2D kinematics for the learner's
Pinnacle Terminal-1 Physics route?

**No, not yet.**

The owner-supplied school portion sheet confirms only the chapter label:

`Motion in 2 D`

It does not enumerate projectile motion, arbitrary-angle vector resolution, independent
component motion, 2D constant acceleration, trajectory equations, range/height/time-of-flight,
or any other chapter-internal learner action.

## Evidence classes kept separate

### 1. School evidence

Current school evidence:

- `docs/grade9/sources/TERMINAL1-PORTION-SHEET-2026-27.md`
- chapter label: `Motion in 2 D`
- authority level: **chapter boundary only**

No additional Pinnacle chapter index, workbook page, class worksheet, revision sheet, teacher
topic list, prior paper or sample question is currently present in the repository.

Therefore every Motion-2D micro row in
`docs/grade9/terminal1-pinnacle-physics.micro-scope.json` remains
`MICRO_TO_CONFIRM`.

### 2. Local Grade9V3 capability truth

Current reusable foundations include:

- `CAP-VECTOR-VS-SCALAR`
- `CAP-VECTOR-SIGNED-COMPONENT`
- `CAP-VEC-COMPONENT-SUM`
- `CAP-VEC-RESULTANT-CONSTRAINT`
- `CAP-GRAPHICAL-SUBTRACT`
- `CAP-VEC-SUB-ORDER`
- `CAP-SAME-TIME`
- `CAP-RELATIVE-V`
- `CAP-VECTOR-CHECK`
- `CAP-KIN-CONSTANT-ACCELERATION` for the existing one-dimensional model

Current repository boundaries are equally important:

- `BUCKET-PHY-VEC-ADD-SUB` explicitly excludes arbitrary-angle trigonometric
  decomposition when components are not already supplied;
- `BUCKET-PHY-KIN-1D-MOTION` explicitly excludes general 2D vector decomposition and
  projectile motion;
- there is no canonical learner capability for independence of orthogonal component motions
  coupled by one time variable;
- there is no canonical general 2D constant-acceleration solver;
- there is no canonical projectile-model-selection capability.

These are **local capability gaps**. They are not automatically Pinnacle school requirements.

### 3. External real-question evidence

The existing external pilot:

`docs/c6-examside-motion-in-plane-pilot.md`

uses a real ExamSIDE JEE Main Motion-in-a-Plane question bank as **question-demand evidence**,
not school or curriculum authority.

Its retained routable slice proves that current canonical content can already handle real
relative-motion/reference-frame demand through:

```text
vector/component foundations
→ CAP-SAME-TIME
→ CAP-RELATIVE-V
→ CAP-VECTOR-CHECK
→ optional explicit frame support
```

The same external source also exposes real question types that cannot be mapped honestly to
the present canonical layer without under-stating their demand:

- projectile model selection and range/height/time structure;
- arbitrary-angle vector decomposition;
- 2D component constant-acceleration solving;
- velocity magnitude/direction reconstruction after component evolution;
- projectile + WEP combinations where WEP alone is not the full demand.

This external evidence confirms that the suspected local gaps are genuine **subject-content
gaps under real 2D question demand**.

It still does **not** prove that Pinnacle Terminal-1 assesses those gaps.

## Current Motion-2D decision table

| Learner action | School micro-demand | Local state | Evidence-supported decision |
| --- | --- | --- | --- |
| vector representation / signed components | `MICRO_TO_CONFIRM` | ready with bridge | reuse if school demand appears |
| component addition/subtraction | `MICRO_TO_CONFIRM` | ready with bridge | reuse if demanded |
| relative position / relative velocity | `MICRO_TO_CONFIRM` | ready with bridge | reuse if demanded |
| arbitrary-angle vector decomposition | `MICRO_TO_CONFIRM` | local gap | **HOLD_UNCONFIRMED** |
| independent x/y component motion | `MICRO_TO_CONFIRM` | local gap | **HOLD_UNCONFIRMED** |
| 2D constant acceleration | `MICRO_TO_CONFIRM` | local gap | **HOLD_UNCONFIRMED** |
| horizontal projectile model | `MICRO_TO_CONFIRM` | local gap | **HOLD_UNCONFIRMED** |
| oblique projectile model | `MICRO_TO_CONFIRM` | local gap | **HOLD_UNCONFIRMED** |
| range / maximum height / time of flight | `MICRO_TO_CONFIRM` | application-family gap | **HOLD_UNCONFIRMED** |
| later-time velocity magnitude/direction | `MICRO_TO_CONFIRM` | local gap | **HOLD_UNCONFIRMED** |
| trajectory equation | `MICRO_TO_CONFIRM` | local gap | **HOLD_UNCONFIRMED** |
| position-vector differentiation | `MICRO_TO_CONFIRM` | local gap | defer unless explicitly demanded |

## Smallest durable authoring spine if school evidence confirms ordinary projectile work

If a real Pinnacle source confirms projectile-style demand, the first authoring proposal should
start from learner actions, not formula names:

```text
arbitrary-angle vector resolution
        ↓
independent orthogonal component motion
        ↓
2D constant acceleration with one common time variable
        ↓
projectile model selection
        ↓
question variations / applications
```

Range, maximum height, time of flight, horizontal launch and oblique launch should initially be
treated as controlled applications of that spine, not separate capabilities, unless real learner
evidence proves that they fail independently.

## What would authorize authoring

Any one of the following, with an explicit source locator, can move a row out of
`MICRO_TO_CONFIRM`:

- Pinnacle Motion-in-2D chapter contents/index;
- class workbook/classwork page;
- teacher revision list;
- school worksheet/question set;
- sample or prior Terminal-1 paper;
- teacher-issued topic list.

The next confirmed source should be processed through:

`docs/grade9/TERMINAL1-PINNACLE-DEMAND-INTAKE.md`

## Decision now

```text
Motion in 2 D chapter = CONFIRMED
projectile/general-2D micro-demand = NOT CONFIRMED
local capability gap = REAL
authoring authorization = NO
next action = obtain/map school micro-evidence
```

This is intentionally a stronger evidence boundary than either extreme:

- it does not pretend Grade9V3 already teaches general 2D/projectile motion;
- it also does not manufacture school scope merely because external question banks and
  Physics knowledge show that the content is plausible.


## Owner source decision — 2026-09-19

The owner explicitly approved ExamSIDE as a reliable source for worksheet/question demand.

That changes the authoring disposition:

```text
Pinnacle chapter label                confirmed
Pinnacle chapter-internal micro-scope still school-unconfirmed
ExamSIDE real question demand         trusted for selected worksheet intake
local 2D/projectile gaps              authoring may proceed when a selected ExamSIDE item needs them
```

Selected first-slice evidence:

- JEE Main 2023-04-11 evening: oblique projectile velocity after time;
- JEE Main 2023-02-01 morning: horizontal projectile from a cliff;
- JEE Main 2020-09-04 morning: x-y constant acceleration with component acceleration;
- JEE Main 2026-04-08 evening: equal-range projectiles with different flight times.

The bounded local response is:

```text
CAP-VEC-ANGLE-DECOMPOSITION
        ↓
CAP-KIN-2D-INDEPENDENT-COMPONENTS
        ↓
CAP-KIN-2D-CONSTANT-ACCELERATION
        ↓
CAP-KIN-PROJECTILE-MODEL
```

Range, height, time of flight and horizontal/oblique launch are initially handled as question variations of this spine. Calculus-style position-vector differentiation and trajectory-equation derivation remain outside this first slice.
