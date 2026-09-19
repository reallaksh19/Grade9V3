# Grade 9 Pinnacle NLM — ExamSIDE demand reconnaissance

> Status: **owner-approved preparation-demand reconnaissance**
>
> Date: 2026-09-19
>
> Primary source:
> `https://questions.examside.com/past-years/jee/jee-main/physics/laws-of-motion`
>
> Specific owner-supplied item:
> `https://questions.examside.com/past-years/jee/question/pa-machine-gun-fires-a-bullet-of-mass-m-with-a-velocity-of-comedk-physics-units-and-measurements-k8pkjfk78zobjtd5`
>
> Authority: `docs/grade9/PINNACLE-EXAMSIDE-PREPARATION-AUTHORITY.md`

## Source snapshot

The inspected ExamSIDE JEE Main Laws of Motion page reports 153 questions across 113 papers
from 2002–2026.

Visible recent questions repeatedly demand more than the current qualitative NLM foundation.
Representative families include:

- friction on inclined planes;
- static-friction threshold / maximum common acceleration;
- blocks in contact;
- multiple blocks joined by ideal strings;
- pulley/string tension;
- equilibrium under several forces;
- applied force on an incline;
- accelerating-observer / hanging-bob reasoning;
- retarding force using Newton II plus kinematics;
- connected-body constraints;
- momentum-transfer / recoil style force.

The owner-supplied machine-gun item explicitly uses force as the rate of momentum carried away
by fired bullets. That is a real question-demand signal for the momentum-rate form of Newton II,
not merely a different story for `F = ma`.

## Current local NLM spine

The current canonical bucket already owns:

- `CAP-NLM-NET-ZERO-MOTION`;
- `CAP-NLM-FORCES-SUM-ZERO`;
- `CAP-NLM-FBD-BODY-OWNERSHIP`;
- `CAP-NLM-SECOND-LAW`;
- `CAP-NLM-FRICTION`;
- `CAP-NLM-THIRD-LAW`;
- `CAP-NLM-FRAME-CHOICE` as a retained explicit-demand extension.

This is a strong conceptual foundation. The main gap is not "Newton's laws" in general; it is
the quantitative and constraint reasoning repeatedly required by the approved question bank.

## Demand-family crosswalk

| ExamSIDE demand family | Existing local support | Decision |
| --- | --- | --- |
| Choose one body, draw forces, apply signed net-force equation | FBD ownership + Newton II | **REUSE** |
| Balanced/equilibrium force reasoning | net-zero + force-sum reasoning | **REUSE** |
| Basic friction direction | `CAP-NLM-FRICTION` | **REUSE** |
| Quantitative friction magnitude / limiting condition | current friction capability is primarily directional/qualitative | **ENRICH / AUTHOR candidate** |
| Static vs sliding friction decision under a threshold | local coverage too shallow for repeated quantitative JEE demand | **AUTHOR candidate** |
| Inclined-plane force components | FBD + vector decomposition available across repository | **REUSE WITH BRIDGE** |
| Two blocks in contact with common acceleration | Newton II exists; common-acceleration system constraint not durable locally | **AUTHOR candidate** |
| Ideal-string equal-tension reasoning | no durable local capability | **AUTHOR candidate** |
| Ideal pulley / connected acceleration constraint | no durable local capability | **AUTHOR candidate** |
| Large chain / many-body moving-boundary systems | no local capability | **DEFER after first connected-body slice** |
| Accelerating observer / hanging bob | `CAP-NLM-FRAME-CHOICE` | **REUSE AS EXPLICIT EXTENSION** |
| Bullet retarding force with known deceleration | Newton II + existing kinematics | **REUSE** |
| Momentum-flow / machine-gun recoil-force reasoning | current Newton-II capability does not own `F = dp/dt` / mass-flow reasoning | **AUTHOR explicit-demand extension candidate** |
| Collision/momentum-conservation algebra | excluded by current bucket unless demanded | **Do not import automatically** |

## Smallest high-value NLM production spine

Do not create one capability for every block/pulley/incline story.

The first useful expansion should be:

```text
existing body-specific FBD
        ↓
quantitative contact/friction condition
        ↓
connected bodies share a constrained acceleration
        ↓
ideal string transmits a tension constraint
        ↓
ideal pulley changes direction while preserving the declared string constraint
```

This spine explains a large fraction of the visible approved NLM demand without creating a
catalogue of apparatus-specific skills.

### Candidate A — quantitative friction condition

Suggested learner action:

> Determine whether static friction can satisfy the required contact-force demand; otherwise
> use the appropriate sliding-friction model, with the normal reaction obtained from the same
> free-body diagram.

Do not encode "friction = mu N" as an unconditional identity.

The teaching must distinguish:

```text
static friction
→ adjusts up to its limiting value

limiting static friction
→ equality only at impending slip

kinetic/sliding friction
→ model used after relative sliding is established
```

This is the biggest gap exposed repeatedly by the inspected question bank.

### Candidate B — connected-body common acceleration

Suggested learner action:

> Decide which bodies are constrained to share an acceleration magnitude/direction, write
> one Newton-II equation per selected body or one system equation when appropriate, and
> maintain one consistent sign convention.

This should not be named after "two blocks", "three blocks", "train", or "cart".

### Candidate C — ideal string / tension constraint

Suggested learner action:

> Under explicitly ideal string assumptions, use the string to relate the connected bodies'
> kinematics and tension, while keeping tension forces assigned to the correct body-specific
> FBDs.

Do not imply equal tension when the rope/pulley model is not ideal.

### Candidate D — pulley constraint

Suggested learner action:

> Convert fixed string length into the required relation between connected displacements,
> velocities or accelerations for a bounded ideal-pulley configuration.

The first slice should cover only ordinary single-string fixed-pulley arrangements needed by
representative current demand.

Do not begin with compound/movable pulley catalogues.

### Candidate E — momentum-transfer force extension

The supplied machine-gun item exposes a distinct demand:

> Relate the external force/recoil to momentum transferred per unit time.

A bounded extension may teach:

```text
F_external = rate of change of momentum
```

and, for discrete identical ejecta,

```text
force magnitude
= (number ejected per unit time)
  × (momentum change per item)
```

This should be an explicit question-demand extension, not inserted into the ordinary Grade-9
default NLM route merely because one approved question uses it.

It is also distinct from full collision/momentum-conservation algebra.

## Priority order

### Priority 1 — quantitative friction

Reason:

- repeated visible ExamSIDE demand;
- builds directly on existing FBD/force ownership;
- immediately supports incline, stacked-block and threshold questions;
- relatively small content addition.

### Priority 2 — connected-body + ideal string constraint

Reason:

- repeated block/string/pulley demand;
- durable across many stories;
- closes a genuine structural gap rather than adding isolated formulas.

### Priority 3 — bounded pulley relation

Reason:

- useful once connected-body and ideal-string invariants exist;
- should be kept narrower than a full pulley taxonomy.

### Priority 4 — momentum-rate extension

Reason:

- explicit owner-supplied real question evidence;
- conceptually valuable;
- does not need to block the ordinary NLM preparation route.

## What should remain non-default

The existing observer-frame/pseudo-force capability should stay non-default.

ExamSIDE contains accelerating-observer style demand, so it is legitimate preparation content
when a question calls for it. That does not justify making it an automatic prerequisite of
ordinary NLM questions.

Similarly, the momentum-rate extension should be reachable by question demand without becoming
a default rung required for every learner.

## What not to build in the first NLM expansion

Do not simultaneously add:

- arbitrary multi-pulley catalogues;
- movable-pulley formula patterns;
- wedge-on-wedge systems;
- variable-mass rocket equation;
- full impulse/collision curriculum;
- rigid-body torque/rotation;
- every possible friction optimization problem as its own capability.

Those may be genuine later demands, but they are not required to close the first high-value gap.

## Recommended next production PR

The next bounded production PR should focus on:

```text
quantitative friction
+
connected-body common acceleration
+
ideal string tension constraint
```

with pulley geometry included only where needed to demonstrate the string constraint.

Required regression boundaries:

- current FBD/body-ownership prerequisite remains explicit;
- `CAP-NLM-FRAME-CHOICE` remains non-default;
- no story-specific block/pulley capability explosion;
- ideal-rope/pulley assumptions must be stated;
- static friction is not always set equal to its maximum;
- external ExamSIDE questions remain transient demand, not canonical question custody.

After that slice is proven and session-ready, evaluate whether a separate small
momentum-transfer-force extension is warranted from the supplied machine-gun item.

## Stop condition

Stop NLM authoring after the bounded friction + connected-body + string slice is mechanically
session-ready and stress-frozen.

Further breadth should be triggered by:

- learner evidence;
- additional approved ExamSIDE families that cannot be expressed by the new spine;
- later JEE preparation staging.
