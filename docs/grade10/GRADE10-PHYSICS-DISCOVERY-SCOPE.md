# Grade-10 Physics discovery scope

> Status: **DISCOVERY ONLY — no Grade-10 production authoring is authorized by this file**
>
> Sequence boundary: Grade 9 is complete on current `main`; Grade 10 starts from a fresh
> current-source and donor comparison. Grade 11 remains out of scope.

## Why this pass exists

Grade9V3 already contains several broader Physics matrices that happen to overlap future
Grade-10 material. Their presence is not curriculum authority and must not be treated as
proof that Grade 10 is already authored.

The Grade-10 pass therefore starts with:

```text
current official scope evidence
        +
current Grade9V3 matrix/library state
        +
pinned prior Physics engineering donors
        ↓
capability-level crosswalk
        ↓
smallest Grade-10 production slice
```

Not:

```text
existing matrix exists
→ declare it Grade 10
```

and not:

```text
Common has a Grade-10 gate
→ import the gate/schema/readiness claim
```

## Current-source evidence status

Current-year authority must be re-established for Grade 10 independently of the completed
Grade-9 pass.

Evidence available during this discovery pass:

1. CBSE Academics currently exposes the 2026-27 curriculum release on its academic site.
2. The official 2026-27 Class-X Science reading material includes the Magnetic Effects of
   Electric Current unit.
3. The official CBSE Science Learning Standards document identifies the Class-X Physics
   chapter families as:
   - Light — Reflection and Refraction;
   - The Human Eye and the Colourful World;
   - Electricity;
   - Magnetic Effects of Electric Current.
4. The 2025-26 official Science syllabus is a useful near-current comparator for the detailed
   topic list, but it is **not** promoted here as 2026-27 authority.

References inspected:

- https://cbseacademic.nic.in/
- https://cbseacademic.nic.in/web_material/CurriculumMain27/SecPart1/Science_SecP1IX_2026-27_RM.pdf
- https://www.cbseacademic.nic.in/cbe/documents/Learning_Standards_Science.pdf
- https://cbseacademic.nic.in/web_material/CurriculumMain26/Sec/Science_Sec_2025-26.pdf

### Source-binding consequence

This document may establish **candidate Grade-10 production areas**.

It may not yet bind an exact 2026-27 syllabus claim into canonical content. Before the first
Grade-10 production PR, capture/inspect the exact current Science scope source used for that
slice and record its custody according to the existing source workflow.

If the current source differs from the historical/near-current comparator, current source
wins.

## Current local Grade9V3 state

### Optics — reflection and spherical mirrors

Local matrix:

`MATRIX-PHY-OPTICS-REFLECTION-MIRRORS`

Current matrix rungs:

```text
R1  reflection measured from the normal              mapped
R2  real versus virtual image geometry               mapped
R3  sign convention                                  mapped
R4  spherical-mirror principal-ray construction      matrix-only
R5  mirror equation                                  matrix-only
R6  mirror magnification                             matrix-only
```

Current benchmark snapshot: `NOT_READY`.

The existing package has canonical teaching for only the first three capabilities. R4-R6
have matrix design but no resolving canonical microtopic in the package.

This is an authentic Grade-10 candidate because the existing local structure already
matches the reflection/mirror learner journey closely. It should be **enriched**, not
replaced wholesale.

### Electricity

Local matrix:

`MATRIX-PHY-ELEC-CURRENT-OHM`

Current matrix rungs:

```text
R1  current / steady charge-flow continuity          mapped
R2  drift/current-density microscopic model          matrix-only
R3  potential difference / energy per charge         matrix-only
R4  test an ohmic constant-resistance model          mapped
R5  series/parallel circuit structure                matrix-only
R6  electric power                                   matrix-only
R7  Kirchhoff-style node/loop equations              matrix-only
```

Current benchmark snapshot: `NOT_READY`.

The current matrix is broader than a safe Grade-10 assumption. In particular, the
microscopic drift/current-density rung and Kirchhoff loop-equation rung must not enter the
ordinary Grade-10 route merely because they already exist.

The Grade-10 pass should reuse the matrix where the learner action matches current scope,
fill missing canonical teaching only when source-backed, and explicitly keep higher-depth
material outside the ordinary route.

### Magnetic effects

Local matrix:

`MATRIX-PHY-MAG-FIELD-LORENTZ`

Current matrix rungs:

```text
R1  magnetic-field direction / page conventions      mapped
R2  magnetic-flux orientation                        mapped
R3  charged-particle v × B force                     matrix-only
R4  perpendicular magnetic force redirects speed     mapped
R5  induction / flux-change direction                matrix-only
R6  motional-emf geometry                            matrix-only
```

Current benchmark snapshot: `NOT_READY`.

This local matrix also spans beyond a safe Grade-10 assumption. A Grade-10 route may need
field direction, field around current, force on a current-carrying conductor, motor and
induction reasoning, while charged-particle Lorentz dynamics, quantitative flux formalism
or motional-emf formulae may be later-depth material unless the current source explicitly
requires them.

Do not treat the existing matrix ordering as the Grade-10 curriculum sequence.

### Missing local Grade-10 areas

No dedicated current matrix/library was found for:

- refraction through lenses as a Grade-10 learner spine;
- human-eye accommodation/vision defects;
- dispersion/scattering as a learner spine.

Their absence is a discovery result, not immediate permission to create three new buckets.
Create new local capability structure only after the current-source slice is bound and the
anti-duplication test is applied.

## Grade-10 discovery boundary

For this pass, the candidate Physics scope is:

```text
G10-A  Light: reflection / spherical mirrors
G10-B  Light: refraction / spherical lenses
G10-C  Human eye / vision correction / dispersion-scattering
G10-D  Electricity
G10-E  Magnetic effects of electric current
```

These labels are **working discovery areas**, not runtime enum values or matrix-schema
fields.

## What remains unchanged

Grade-10 work must preserve the existing architecture boundaries:

- matrix = pedagogical design, not curriculum authority;
- canonical library = teaching/repair/verification;
- learner/session evidence remains separate;
- rough owner percentage = starting coordinate only;
- prerequisite closure may cross matrices but does not create fake mastery;
- donor material is copied/adapted locally, never a runtime dependency;
- no new readiness state is required;
- no grade/class field is required in the matrix schema;
- ordinary Grade-10 scope must not pull Grade-11/JEE depth down simply because the donor
  contains it.

## Provisional production order

The smallest defensible first production slice is:

```text
G10-1  Light — Reflection and spherical mirrors
```

Reason:

- a local matrix already exists;
- half of its learner spine already has canonical teaching;
- the missing R4-R6 content is visible and bounded;
- the donor corpus contains a direct semantic counterpart;
- it allows the Grade-10 copy/adapt method to be proven before creating new lens/eye
  structures.

After G10-1, re-evaluate rather than mechanically committing the entire discovery list.

## Exit condition for discovery

Discovery is complete when:

```text
current-source authority status is explicit
donor snapshots are pinned
existing local overlap is identified
higher-depth pull-down risks are explicit
missing local areas are named without pre-authoring them
first bounded production slice is chosen
no architecture expansion is introduced
```
