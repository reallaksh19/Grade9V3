# Grade 9 Terminal-1 Pinnacle Physics — school-demand intake protocol

> Purpose: turn future school material into an exact micro-demand → Grade9V3 capability decision.
>
> Scope: **Grade 9 Terminal-1 Pinnacle Physics only**.
>
> This is a planning/review protocol, not a runtime schema.

## Accepted evidence

Use any of the following when supplied by the owner:

- chapter contents/index pages;
- classwork or workbook pages;
- teacher revision sheet;
- school worksheet/question set;
- sample/prior Terminal-1 paper;
- teacher-issued topic list.

The current portion sheet is already sufficient to confirm only these chapter labels:

```text
Vectors
Motion 1 D
Motion in 2 D
NLM
```

Do not infer chapter-internal microtopics from those labels alone.

## Intake unit

Review one **learner action** at a time, not one page heading at a time.

For every explicit school demand, record:

```text
source locator
→ exact learner action demanded
→ current local capability/ref, if any
→ decision
→ prerequisite impact
→ exam priority
```

A useful locator is:

```text
<uploaded file or school source> / page / exercise / question number
```

Do not copy long school text into the repository. A short demand summary plus locator is enough.

## Decision rule

For each school-demanded learner action:

### REUSE

Use when an existing local capability already expresses the same independently fail-able action.

Examples:

```text
"add two vectors in x-y components"
→ CAP-VEC-COMPONENT-SUM
→ REUSE

"draw forces acting on one selected body"
→ CAP-NLM-FBD-BODY-OWNERSHIP
→ REUSE
```

A different story, object or diagram does not create a new capability.

### ENRICH

Use when the same learner action exists locally but its canonical teaching is too shallow for the confirmed school demand.

Example pattern:

```text
existing action = choose friction direction
school demand = same action plus a durable quantitative condition missing locally
→ inspect whether the missing detail belongs in the same capability
→ ENRICH only the missing semantic detail
```

Do not use ENRICH merely because a school question is harder.

### AUTHOR

Use only when the school material demands an independently fail-able learner action that the repository does not currently own.

The current likely examples, **only if school evidence confirms them**, are:

- arbitrary-angle vector decomposition;
- independent orthogonal x/y motion;
- 2-D constant-acceleration component modelling;
- projectile model selection;
- connected-body/tension reasoning;
- pulley-constraint reasoning.

Before AUTHOR, apply the counterfactual:

> Can a learner reliably succeed at the existing capability and still fail this demanded action independently?

If no, prefer REUSE/ENRICH/question variation.

### QUESTION_VARIATION

Use when the school demand is a context/application of an existing capability.

Likely examples:

- projectile range, height and time-of-flight after the projectile model is owned;
- river, rain and swimmer stories after relative-velocity/component reasoning is owned;
- lever/pulley/incline stories when they do not introduce a new learner decision.

### HOLD_UNCONFIRMED

Use when the source is too broad, ambiguous or missing the actual learner action.

Never author from:

- a chapter title alone;
- a rough recollection of what a Pinnacle chapter "usually" contains;
- donor metadata;
- a model-generated syllabus guess.

## Chapter-specific evidence to capture

### Vectors

Look specifically for evidence of:

- vector/scalar distinction;
- graphical addition/subtraction;
- x/y components;
- angle-based resolution using trigonometry;
- resultant magnitude/direction;
- unit-vector notation;
- any dot/cross-product material.

The current high-value uncertainty is **arbitrary-angle decomposition**.

### Motion 1 D

Look for:

- graph reading;
- equations of uniformly accelerated motion;
- free fall/vertical motion;
- turning-point questions;
- uniform circular motion.

The local spine is already strong; prefer mapping real questions before adding anything.

### Motion in 2 D

Look specifically for:

- independent horizontal/vertical motion;
- horizontal projectile;
- oblique projectile;
- time of flight;
- maximum height;
- range;
- trajectory equation;
- velocity at a later time;
- relative motion;
- time-dependent position-vector differentiation.

The first four durable decisions to confirm are:

```text
vector decomposition
→ independent x/y motion
→ 2-D constant acceleration
→ projectile model selection
```

Do not make range/height/time-of-flight separate capabilities unless real evidence proves they fail independently.

### NLM

Look specifically for:

- normal reaction;
- friction coefficient/static/kinetic limits;
- incline problems;
- two contacting bodies;
- strings/tension;
- pulleys;
- connected accelerations;
- Newton III partner identification;
- momentum/impulse, if included by the school.

Do not assume these from the label "NLM".

## Promotion worksheet

When new school material arrives, produce a compact table:

| Source locator | Exact school demand | Local ref | Decision | Prerequisite impact | Priority |
| --- | --- | --- | --- | --- | --- |
| p.X / Q.Y | learner action | capability or — | REUSE / ENRICH / AUTHOR / QUESTION_VARIATION / HOLD_UNCONFIRMED | none / named prerequisite | HIGH / MEDIUM / LOW |

A row becomes actionable only when the source locator and learner action are explicit.

## Stop conditions

Stop and leave the row unpromoted when continuing would require:

- guessing what the school chapter contains;
- inventing a prerequisite;
- treating a rough owner estimate as mastery;
- importing higher-grade donor content merely because it is available;
- creating a new capability for a context-only change.

## Expected next output

After the next school pages/questions are supplied, the agent should return:

```text
confirmed micro-demand
→ exact local mapping
→ REUSE / ENRICH / AUTHOR / QUESTION_VARIATION
→ smallest prerequisite route
→ what remains unconfirmed
```

and update:

`docs/grade9/terminal1-pinnacle-physics.micro-scope.json`

Only confirmed rows should move out of `MICRO_TO_CONFIRM`.
