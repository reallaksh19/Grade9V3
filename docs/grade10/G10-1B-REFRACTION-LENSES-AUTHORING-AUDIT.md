# G10-1B — Refraction and spherical lenses authoring audit

> Matrix: `MATRIX-PHY-OPTICS-REFRACTION-LENSES`
>
> Result: **create one bounded local refraction/lens spine; keep human-eye and colourful-world optics out.**

## Current scope basis

The current Grade-10 discovery pass established these required actions inside
**Light — Reflection and Refraction**:

- laws of refraction and refractive index;
- spherical-lens image formation;
- lens formula, with **derivation not required**;
- magnification;
- lens power and applications;
- practical focal-length work for a convex lens;
- glass-slab ray tracing with incidence/refraction/emergence interpretation.

Current curriculum source used by the Grade-10 discovery:

`https://cbseacademic.nic.in/web_material/CurriculumMain27/SecPart1/Science_SecP1_2026-27.pdf`

Cross-check:

`https://edustud.nic.in/edu/Syllabus_2026_27/10/10_Science_SYLLABUS_2026_27_EM.pdf`

As in G10-1A, the package remains `CANDIDATE` with empty curriculum mappings. This slice
does not bypass the repository's exact curriculum-binding authority.

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
  PHY-OPTICS-REFRACTION-LENSES
```

Durable donor semantics reused:

- Snell geometry is normal-referenced;
- refractive index is physically tied to light speed;
- thin-lens ray rules must agree on one image;
- the lens equation uses the lens-specific signed relation
  `1/v - 1/u = 1/f`;
- the thin-lens/paraxial model boundary remains visible;
- magnification sign carries orientation;
- power is reciprocal focal length in metres and retains sign.

Common PR #350 was previously checked during G10-1A and did not expose a preferred
canonical-v3 optics gate. No nonexistent v3 record is claimed here.

Not imported:

- donor technical/readiness or release state;
- donor `cbse_ref` as current Grade9V3 authority;
- JEE/difficulty metadata;
- thick-lens or multi-element optics;
- human-eye correction;
- prism/dispersion/scattering;
- total-internal-reflection depth not required by this bounded current slice.

## Capability decomposition

The new local learner spine is:

```text
CAP-OPT-REFRACTION-NORMAL
→ CAP-OPT-REFRACTIVE-INDEX-SNELL
→ CAP-OPT-LENS-RAY-CONSTRUCTION
→ CAP-OPT-LENS-EQUATION
→ CAP-OPT-LENS-MAGNIFICATION
→ CAP-OPT-LENS-POWER
```

These are separated because they can fail independently:

- a learner can use the normal/bending direction but not the index/Snell relation;
- can know refraction but fail to construct a lens image;
- can draw a lens image but use mirror signs/formula;
- can locate an image but drop magnification orientation;
- can use image relations but mishandle power units/sign.

No separate capability is created for convex versus concave lens stories. They are controlled
variations of the same learner actions.

## Governed relations

G10-1B adds one Grade-10 optics gate in
`Physics/gates/foundational-relations.v1.json` and binds local copies of:

```text
REL-SNELLS-LAW
  n_1 sin(i) = n_2 sin(r)

REL-REFRACTIVE-INDEX-SPEED
  n = c/v

REL-LENS-EQUATION
  1/v - 1/u = 1/f

REL-LENS-MAGNIFICATION
  m = v/u = h_i/h_o

REL-LENS-POWER
  P = 1/f
```

The gate is an owner extension, not current curriculum authority.

## Model and representation boundaries

### Refraction

Before angle use:

```text
draw boundary normal
→ label incident/refracting media
→ compare index/speed
→ trace toward/away from normal
→ apply Snell only after those declarations
```

For a parallel-sided glass slab, the learner must treat entry and exit as two boundary
events. The emergent ray is parallel to the incident ray in the simple parallel-face model,
while lateral displacement may remain.

### Thin spherical lens

Before equation use:

```text
principal axis + optical centre + foci
→ two independent valid principal rays
→ common image / backward-extension point
→ declare Cartesian signs
→ use thin-lens equation
→ cross-check against ray geometry
```

The lens formula is **used, not derived**.

The relation is explicitly bounded to the thin-lens, paraxial/small-angle model.

### Magnification

```text
|m|  → relative size
sign → erect / inverted orientation
```

Dropping the sign is treated as information loss, not harmless simplification.

### Power

```text
signed f
→ convert f to metres
→ P = 1/f
→ report in dioptres
```

The sign distinguishes converging and diverging lens power; the magnitude tracks inverse
focal length.

## Practical reasoning retained

The current source's practical demand is represented without creating separate practical
capabilities:

- rectangular glass slab:
  normal, incident/refracted/emergent paths, two-boundary reasoning;
- convex-lens focal length:
  distant object gives an approximately parallel incident bundle and an image near the
  focal plane.

The practicals test the same underlying learner actions rather than creating story-specific
capabilities.

## Self-study closure

Every rung has:

- canonical capability + microtopic;
- teaching path;
- complete misconception → diagnostic → repair;
- fresh exit verification;
- Core1A route;
- full Core1B predict / attempt / reconstruct / boundary-test cycle.

Both Core1A and Core1B traverse the same six-rung segment.

## Deliberately not added

- no human-eye / defect-correction capability;
- no prism / dispersion / scattering capability;
- no total-internal-reflection or optical-fibre extension;
- no lens-combination formula;
- no thick-lens principal-plane model;
- no optical-instrument content;
- no wave-optics content;
- no grade/class field in the matrix;
- no new readiness state;
- no cross-repository runtime link;
- no learner evidence.

Those belong to later bounded slices or explicit later demand.

## Acceptance

G10-1B is complete when:

```text
all six refraction/lens rungs resolve to canonical microtopics
local relation expressions match gate-owned relations
normal/media semantics survive Snell use
ray construction and lens equation predict compatible image geometry
magnification keeps orientation sign
power uses metres + sign
Core1A + Core1B cover all six rungs
diagnosis + repair + fresh verification exist
MATRIX-PHY-OPTICS-REFRACTION-LENSES = SESSION_READY
human-eye / colourful-world scope has not leaked in
full repository guardrails pass
```