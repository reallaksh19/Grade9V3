# G10-1B — Refraction and spherical lenses authoring audit

> Matrix: `MATRIX-PHY-OPTICS-REFRACTION-LENSES`
>
> Result: **create the missing local Grade-10 refraction/lens family; reuse general image
> geometry; do not broaden into human-eye or prism/dispersion/scattering work.**

## Current scope basis

The current 2026–27 Class X Science scope places the following inside **Light — Reflection
and Refraction**:

- refraction and the laws of refraction;
- refractive index;
- refraction by spherical lenses and image formation;
- lens formula, with **derivation not required**;
- magnification;
- power and applications of lenses;
- practical tracing through a rectangular glass slab with incidence/refraction/emergence
  interpretation;
- practical estimation of convex-lens focal length from a distant object.

Current curriculum source:

`https://cbseacademic.nic.in/web_material/CurriculumMain27/SecPart1/Science_SecP1_2026-27.pdf`

The package remains `CANDIDATE` with empty curriculum mappings. Scope evidence does not
bypass the repository's exact curriculum-binding authority.

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

The donor contributed durable semantic checks:

- one ordered media pair must govern refraction angle, index and speed ratios;
- the thin-lens equation uses `1/v - 1/u = 1/f`, not the mirror plus-form;
- lens formula use is bounded by a thin-lens/paraxial model;
- power uses focal length in metres and retains sign;
- independent principal rays must agree on one image point.

Common PR #350 was inspected at
`9c7d363d2ae2866ac829ae6b8039eeb8c1abc2c0`. Its discovery catalog still marks
`PHY-OPTICS-REFRACTION-LENSES` as `MIGRATION_REQUIRED` with no canonical-v3 gate IDs.
No nonexistent preferred-v3 record is claimed.

Not imported:

- donor technical-readiness or release state;
- donor `cbse_ref` as current Grade9V3 authority;
- donor JEE tier or difficulty;
- lens-maker formula, total internal reflection or optical fibres;
- thick-lens principal planes or aberration treatment;
- human-eye correction, prism/dispersion/scattering or optical instruments.

## Capability-level decomposition

| Rung | Learner action | Treatment |
| --- | --- | --- |
| R1 | normal-referenced laws of refraction | **NEW local capability** |
| R2 | relative refractive index across angle/speed ratios | **NEW local capability + relation** |
| R3 | rectangular glass-slab trace and i/r/e interpretation | **NEW local practical capability** |
| R4 | thin spherical-lens principal-ray image construction | **NEW local capability**, reusing `CAP-OPT-REAL-VIRTUAL-IMAGE` |
| R5 | Cartesian lens sign convention | **NEW local lens-specific capability** |
| R6 | signed thin-lens equation | **NEW local capability + relation** |
| R7 | signed lens magnification | **NEW local capability + relation** |
| R8 | signed lens power and bounded applications | **NEW local capability + relation** |
| R9 | convex-lens distant-object focal-length practical | **NEW local practical capability** |

No separate capabilities are created merely for convex versus concave lens stories. Those
are controlled variations of the same ray/sign/formula learner actions.

## Reuse boundary

`CAP-OPT-REAL-VIRTUAL-IMAGE` from G10-1A already expresses the general distinction between
actual light-path intersection and backward-extension intersection. G10-1B uses it as an
upstream prerequisite for lens ray construction rather than cloning an equivalent lens-only
capability.

The G10-1A mirror sign capability is *not* reused because its action is explicitly
mirror-pole-specific. G10-1B therefore owns a separate optical-centre lens-sign action.

## Governed relations

The local gate owns and the package binds exact copies of:

```text
REL-REFRACTIVE-INDEX
  n_21 = n_2/n_1 = sin(i)/sin(r) = v_1/v_2

REL-LENS-EQUATION
  1/v - 1/u = 1/f

REL-LENS-MAGNIFICATION
  m = v/u = h_i/h_o

REL-LENS-POWER
  P = 1/f
```

The refraction ratio keeps one media order. The angle-ratio form is not used at exact normal
incidence where it becomes `0/0`.

The lens equation is used, not derived, and is explicitly treated as a thin-lens/paraxial
model. Power requires `f` in metres, yielding dioptres.

## Practical closure

### Rectangular glass slab

The learner must:

```text
draw normal at entry
→ refract into glass
→ draw normal at exit
→ refract back into air
→ measure/interpret i, r, e
→ distinguish parallel emergence from collinearity
```

### Convex lens focal length

The learner must:

```text
choose a safe distant object
→ align lens and screen
→ focus a sharp real image
→ measure optical-centre-to-screen distance
→ repeat
→ explain why this estimates f rather than proving an exact infinity-object value
```

No direct-Sun viewing is required or encouraged.

## Self-study closure

Every rung has:

- a non-empty teaching path;
- misconception → diagnostic → repair;
- fresh exit verification;
- full Core1B predict/attempt/reconstruct/boundary-test elicitation.

Both Core1A and Core1B traverse the same nine-rung local segment. Cross-bucket reuse of
general real/virtual image geometry remains explicit in prerequisite closure.

## Deliberately not added

- no human-eye functioning/defect/correction capability;
- no prism, dispersion or scattering capability;
- no total internal reflection or optical-fibre teaching;
- no lens-maker relation;
- no lens-combination or microscope/telescope route;
- no advanced aberration calculation;
- no new matrix schema, readiness enum or grade field;
- no Common runtime link;
- no learner evidence.

## Acceptance

G10-1B is complete when:

```text
all nine refraction/lens rungs resolve to canonical microtopics
gate-owned relation copies match exactly
CAP-OPT-REAL-VIRTUAL-IMAGE is reused rather than duplicated
Core1A + Core1B cover all nine rungs
diagnosis + repair + fresh verification exist
MATRIX-PHY-OPTICS-REFRACTION-LENSES = SESSION_READY
human-eye and prism/dispersion/scattering scope has not leaked into the slice
full repository guardrails pass
```
