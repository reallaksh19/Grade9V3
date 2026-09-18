# G9-3 Gravitation authoring audit

> Workstream: **Grade 9 Physics only**
>
> Matrix: `MATRIX-PHY-GRAV-UNIVERSAL-LAW`
>
> Result: **reuse and adapt the repository owner's richer prior Physics engineering semantics; fill only the current Grade-9 gravitation slice and keep higher-depth field/orbit material out of the ordinary route.**

## Adaptation method

This pass does not start Gravitation from a blank page.

Prior internal Physics engineering records were inspected for:

- source/receiver force ownership;
- centre-to-centre geometry;
- point-mass / external-spherical model scope;
- inverse-square force scaling;
- local gravitational field/acceleration as force per unit test mass;
- test-mass independence;
- the distinction between universal `G` and local `g`;
- representation failures;
- misconceptions;
- limiting/model-validity checks.

Those semantics were **copied and adapted into the local Grade9V3 records**.

No Common gate ID, source path, readiness state or runtime dependency is retained in the
Grade9V3 package. The local package is self-contained.

Advanced donor material such as multi-source field superposition was deliberately not copied
into the current Grade-9 core.

## Current-source boundary

The current Grade-9 workstream requires acceleration due to gravity and the relationship
between mass and weight using universal gravitation and the laws of motion.

Accordingly this pass implements the smallest durable learner-capability chain:

```text
mutual attractive interaction
        ↓
universal-law model scope + inverse-square scaling
        ↓
local g / ideal free-fall mass independence
        ├── also uses Newton II
        ↓
mass versus weight
```

Energy/escape and orbital-angular-momentum records already in the repository remain
extension-only.

Pressure, buoyancy and Bernoulli are not pulled into this package.

## Working-sheet classification

`SCOPE_REASON` remains planning-only.

| Rung | Canonical microtopic | SCOPE_REASON | Grade-9 treatment |
| --- | --- | --- | --- |
| R1 | `MIC-PHY-GRAV-R1` | `SYLLABUS_REQUIREMENT` | Adapted: persistent mutual attraction, body ownership and geometry independent of motion/page orientation |
| R2 | `MIC-PHY-GRAV-INVERSE-SQUARE` | `SYLLABUS_REQUIREMENT` | Adapted: model-scope check, centre distance, mass factors, inverse-square distance factor, limiting check |
| R3 | `MIC-PHY-GRAV-FREE-FALL-G` | `SYLLABUS_REQUIREMENT` | Adapted: local g as force per unit mass, test-mass independence, local-not-universal g |
| R3W | `MIC-PHY-GRAV-MASS-WEIGHT` | `SYLLABUS_REQUIREMENT` | Adapted: mass kept separate from local gravitational force W = m g |
| R4 | `MIC-PHY-GRAV-R4` | `DECLARED_EXTENSION` | Retained; not default Grade-9 core |
| R5 | `MIC-PHY-GRAV-R5` | `DECLARED_EXTENSION` | Retained; not default Grade-9 core |

## Why R1 was enriched rather than replaced

The previous local R1 already owned the mutual-interaction idea.

The donor material added durable missing semantics:

- gravity persists when an object is supported, rising or falling;
- force direction follows source-receiver geometry, not velocity;
- equal-and-opposite interaction forces act on different bodies;
- diagram rotation must rotate the physical force direction with the geometry.

These are the **same learner action**, so the existing capability was enriched rather than
creating new capabilities named after supported books, upward projectiles, or diagram
orientation.

## Why R2 was enriched

R2 already owned inverse-square scaling.

The donor material supplied the model conditions the local draft needed:

- identify source and receiver;
- state point-mass or valid external-spherical scope;
- use centre-to-centre separation;
- keep mass scaling linear and distance scaling inverse-square;
- keep attractive direction independent of velocity;
- verify the large-distance trend.

This remains one coherent learner action: apply and validate the simple Newtonian universal-law
model.

## Why R3 is local-g/free-fall rather than the whole donor field topic

The prior engineering corpus contains a much broader gravitational-field treatment, including
radial-field representations and multi-source vector superposition.

Current Grade-9 scope does not justify importing that whole gate.

The adapted R3 therefore keeps only:

- `g = F_grav / m_test` conceptually;
- external-source `g ∝ M/r^2`;
- the Newton-II test-mass cancellation;
- equal ideal free-fall acceleration for different test masses at one location;
- the fact that the familiar near-Earth value of g is local, not universal.

Multi-source field superposition is **DEFER**.

## Why mass/weight remains a separate rung

A learner can understand test-mass independence of free-fall acceleration while still
believing mass changes when a scale reading/weight changes.

Conversely, a learner can use `W = m g` without understanding the force-per-unit-mass logic
behind local g.

Those are independently fail-able actions, so `R3W` remains separate.

## Prerequisite closure

```text
CAP-PHY-GRAV-R1
        ↓
CAP-PHY-GRAV-INVERSE-SQUARE
        ↓
CAP-PHY-GRAV-FREE-FALL-G
        ├── CAP-NLM-SECOND-LAW
        ↓
CAP-PHY-GRAV-MASS-WEIGHT
```

No whole Newton-law or vector bucket is pulled into the gravitation bucket merely because the
donor engineering model was deeper.

## Deliberately not copied

- multi-source gravitational-field superposition;
- universal use of a near-Earth numerical value for g;
- inside-source field modelling;
- advanced orbit mechanics;
- donor release/readiness claims;
- donor curriculum authority;
- donor difficulty engineering vectors.

## Question inventory

No canonical source question is manufactured.

Each adapted core microtopic has a fresh local exit task. Source-backed Core2 custody remains a
separate authority problem.

## Authority boundary

- local records remain `CANDIDATE`;
- curriculum mappings remain empty;
- all runtime/source references remain local to Grade9V3;
- no grade/class field is added to the matrix schema;
- prior internal engineering material supplies Physics semantics, not Grade9V3 release authority.

## G9-3 disposition

```text
existing local Gravitation matrix
        +
richer prior internal Physics engineering
        ↓
copy/adapt reusable semantics
        ↓
R1 enrich force geometry and persistence
R2 enrich model scope + inverse-square checks
R3 local g / free-fall mass independence
R3W mass versus weight
        ↓
exclude field superposition / broad fluids / orbit from Grade-9 core
        ↓
run readiness + regressions + guardrails
```
