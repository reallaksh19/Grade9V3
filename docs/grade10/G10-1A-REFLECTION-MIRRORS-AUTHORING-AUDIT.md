# G10-1A — Reflection and spherical mirrors authoring audit

> Matrix: `MATRIX-PHY-OPTICS-REFLECTION-MIRRORS`
>
> Result: **reuse R1–R3; close R4–R6 locally; do not broaden into refraction/lenses.**

## Current scope basis

The current 2026–27 Class X Science scope places the following inside **Light — Reflection
and Refraction**:

- reflection by curved surfaces;
- spherical-mirror image formation;
- centre of curvature, principal axis, principal focus and focal length;
- mirror formula, with **derivation not required**;
- magnification;
- applications of spherical mirrors;
- practical determination of focal length of a concave mirror.

Current curriculum source:

`https://cbseacademic.nic.in/web_material/CurriculumMain27/SecPart1/Science_SecP1_2026-27.pdf`

Cross-check used during discovery:

`https://edustud.nic.in/edu/Syllabus_2026_27/10/10_Science_SYLLABUS_2026_27_EM.pdf`

The package remains `CANDIDATE` with empty curriculum mappings. This audit records current
scope demand but does not bypass the repository's exact curriculum-binding authority.

## Donor evidence

Pinned discovery donor:

```text
repo: reallaksh19/Common
PR: #383
head: e92481f6e03a8bb49a55f568b03cba7c12fb942a
path:
  Grade 9/V2/Physics/Blueprint/policy/
  physics-technical-engineering-gates.v1.json
subtopic:
  PHY-OPTICS-REFLECTION-MIRRORS
```

The donor contributed durable semantic checks:

- one spherical-mirror geometry must govern every principal ray;
- signed mirror quantities need one declared Cartesian convention;
- the mirror equation is bounded by the paraxial/small-angle model;
- magnification sign carries orientation;
- a ray construction is an independent check against sign/algebra mistakes.

Common PR #350 was inspected at head
`9c7d363d2ae2866ac829ae6b8039eeb8c1abc2c0`. Its current canonical-v3 engineering-gate
set does not contain an optics mirror gate, so no nonexistent "preferred v3" record is
claimed here.

Not imported:

- donor technical-readiness or release state;
- donor `cbse_ref` as current Grade9V3 authority;
- donor difficulty/JEE metadata;
- a new donor schema;
- advanced aberration treatment;
- lens/refraction content.

## Capability-level reconciliation

| Rung | Current local state before G10-1A | Decision |
| --- | --- | --- |
| R1 normal-referenced reflection | canonical | **REUSE** |
| R2 real/virtual image geometry | canonical | **REUSE** |
| R3 Cartesian optical signs | canonical | **REUSE** |
| R4 spherical-mirror principal rays | matrix synthesis only | **ENRICH → local canonical capability/microtopic** |
| R5 signed mirror equation | matrix synthesis only | **ENRICH → local canonical capability/microtopic + governed relation** |
| R6 signed magnification | matrix synthesis only | **ENRICH → local canonical capability/microtopic + governed relation** |

No extra capability was created for concave versus convex mirrors. They are controlled
variations of the same learner actions.

## Local canonical closure

G10-1A adds:

```text
CAP-OPT-SPHERICAL-RAY-CONSTRUCTION
  → MIC-OPT-SPHERICAL-RAY-CONSTRUCTION

CAP-OPT-MIRROR-EQUATION
  → MIC-OPT-MIRROR-EQUATION
  → REL-MIRROR-EQUATION

CAP-OPT-MIRROR-MAGNIFICATION
  → MIC-OPT-MIRROR-MAGNIFICATION
  → REL-MIRROR-MAGNIFICATION
```

Prerequisite chain:

```text
CAP-OPT-NORMAL-REFLECTION
→ CAP-OPT-REAL-VIRTUAL-IMAGE
→ CAP-OPT-SIGN-CONVENTION
→ CAP-OPT-SPHERICAL-RAY-CONSTRUCTION
→ CAP-OPT-MIRROR-EQUATION
→ CAP-OPT-MIRROR-MAGNIFICATION
```

The two relations are owned in
`Physics/gates/foundational-relations.v1.json` and copied into the library through
`gate_relation_ref`.

## Formula boundary

The local route deliberately distinguishes **formula use** from **formula derivation**.

For the current Grade-10 slice:

```text
declare signs
→ use 1/v + 1/u = 1/f
→ rearrange for the requested unknown
→ compare with ray geometry
→ state the paraxial/small-angle model condition
```

No derivation of the mirror formula is made a learner requirement.

## Matrix/library boundary

R4–R6 previously carried temporary synthesis teaching fields because no canonical
microtopic existed.

After canonical closure, the matrix retains only its design job:

```text
microtopic_ref
ladder_position
must_contain
ceiling
controlled_variation
```

The duplicated `aha`, `learner_owns`, `misconception` and `closure` fields are removed
from those rungs.

## Self-study closure

Each new microtopic carries:

- a teaching path;
- misconception → diagnostic prompt → repair;
- fresh exit verification;
- a full Core1B predict/attempt/reconstruct/boundary-test cycle.

Both Core1A and Core1B routes traverse the same six-rung mirror segment.

## Deliberately not added

- no lens/refraction capability;
- no human-eye capability;
- no dispersion/scattering capability;
- no formula derivation requirement;
- no f = R/2 relation merely to make the package look richer;
- no advanced spherical-aberration calculation;
- no grade/class field in the matrix;
- no new readiness state;
- no Common runtime/source link;
- no learner evidence.

Those belong to later bounded slices or to explicit future demand.

## Acceptance

G10-1A is complete when:

```text
all six mirror rungs resolve to canonical microtopics
relation copies match gate-owned expressions
Core1A + Core1B cover all six rungs
diagnosis + repair + fresh verification exist
MATRIX-PHY-OPTICS-REFLECTION-MIRRORS = SESSION_READY
refraction/lens scope has not leaked into this slice
full repository guardrails pass
```
