# Grade-10 Physics discovery and donor crosswalk

> Status: **DISCOVERY COMPLETE — no Grade-10 production content authored in this PR**
>
> Base: `main@766fff7488e976be8cd2f7603a62108390c4b4c9`
>
> Sequence: **Grade 9 complete → Grade 10 discovery → bounded Grade-10 production slices → Grade 11 later**

This document starts the Grade-10 Physics workstream from current `main` without reopening the
completed Grade-9 pass and without bulk-importing the old mixed-topic Physics matrices.

The governing rule remains:

```text
CURRENT Grade9V3
+ current Grade-10 source scope
+ pinned prior Physics engineering
        ↓
capability-level semantic comparison
        ↓
REUSE / ENRICH / candidate new independently-failable capability
        ↓
local teaching + diagnosis + repair + verification
        ↓
targeted readiness / regression
```

Not:

```text
Common Grade-10-looking gate
→ copy its schema / readiness / curriculum authority
```

and not:

```text
existing higher-grade Grade9V3 matrix
→ assume it is already a current Grade-10 route
```

## 1. Current Grade-10 scope basis

Current 2026–27 Class X Science places the Physics work in:

```text
Unit III  Natural Phenomena      12 marks
Unit IV   Effects of Current     13 marks
```

Current-source references used for this discovery:

- CBSE Academic current curriculum target:
  `https://cbseacademic.nic.in/web_material/CurriculumMain27/SecPart1/Science_SecP1_2026-27.pdf`
- Directorate of Education, GNCT Delhi, Class X Science annual syllabus 2026–27
  (which points to the same CBSE Academic curriculum):
  `https://edustud.nic.in/edu/Syllabus_2026_27/10/10_Science_SYLLABUS_2026_27_EM.pdf`

The current Grade-10 Physics scope identified from that source is:

### G10-1 — Light: Reflection and Refraction

- reflection by curved surfaces;
- spherical-mirror image formation;
- centre of curvature, principal axis, principal focus, focal length;
- mirror formula (**derivation not required**);
- magnification and applications of spherical mirrors;
- laws of refraction and refractive index;
- spherical-lens image formation;
- lens formula (**derivation not required**);
- magnification, power and applications of lenses;
- practical focal-length work for a concave mirror and convex lens;
- glass-slab ray tracing with incidence/refraction/emergence interpretation.

### G10-2 — The Human Eye and the Colourful World

- functioning of the eye lens;
- defects of vision and correction;
- refraction through a prism;
- dispersion;
- scattering and daily-life applications;
- current source explicitly excludes colour of the Sun at sunrise/sunset;
- prism ray-tracing practical.

### G10-3 — Electricity

- electric current and potential difference;
- Ohm's law;
- resistance and resistivity;
- factors affecting conductor resistance;
- series and parallel resistor combinations;
- heating effect and applications;
- electric power and the relations among P, V, I and R;
- V–I/resistance practical;
- series/parallel equivalent-resistance practical.

### G10-4 — Magnetic Effects of Electric Current

Ordinary current scope:

- magnetic field and field lines;
- field due to a current-carrying conductor;
- field due to a current-carrying coil/solenoid;
- force on a current-carrying conductor;
- Fleming's Left-Hand Rule;
- DC and AC;
- frequency of AC;
- advantage of AC over DC;
- domestic electric circuits.

Current source marks the following as **formative-only rather than year-end summative**:

```text
motor
electromagnetic induction
electric generator
```

For Grade9V3 authoring, those should stay visibly separated from the ordinary summative
route. Use `DECLARED_EXTENSION` or `DEFER` in planning rather than inventing a new runtime
scope enum.

## 2. Donor snapshot

The Grade-9 donor-adaptation policy remains authoritative for method.

Pinned discovery donor:

```text
repository: reallaksh19/Common
PR: #383
role: breadth/discovery + first-pass semantic donor
head SHA: e92481f6e03a8bb49a55f568b03cba7c12fb942a
source:
  Grade 9/V2/Physics/Blueprint/policy/
  physics-technical-engineering-gates.v1.json
```

Preferred deeper semantic donor when an applicable canonical v3 record exists:

```text
repository: reallaksh19/Common
PR: #350
role: preferred canonical-v3 semantic donor where applicable
current head observed for this discovery:
  9c7d363d2ae2866ac829ae6b8039eeb8c1abc2c0
```

PR #383 donor records relevant to current Grade 10:

```text
PHY-OPTICS-REFLECTION-MIRRORS
PHY-OPTICS-REFRACTION-LENSES
PHY-OPTICS-HUMAN-EYE
PHY-OPTICS-DISPERSION-SCATTERING
PHY-ELEC-CURRENT-OHM
PHY-ELEC-POWER-JOULE
PHY-MAG-FIELD-LORENTZ
PHY-MAG-INDUCTION-FARADAY
```

Their `cbse_ref`, `technical_readiness`, difficulty, release and source-scope metadata are
**historical donor metadata only**. They do not establish Grade9V3 current curriculum or
release authority.

Before production authoring for any one slice, inspect the corresponding #350 canonical-v3
records when available and record the exact donor path/commit used.

## 3. Local reality before Grade-10 authoring

Grade9V3 already contains broader Physics matrices from earlier work. They are useful starting
material, not proof of current Grade-10 completion.

### Existing optics

`MATRIX-PHY-OPTICS-REFLECTION-MIRRORS`

Current canonical library owns only:

```text
CAP-OPT-NORMAL-REFLECTION
CAP-OPT-REAL-VIRTUAL-IMAGE
CAP-OPT-SIGN-CONVENTION
```

The matrix has six rungs, but R4–R6 are still synthesis rows without canonical
`microtopic_ref` ownership. The current local package therefore does **not** yet close the
Grade-10 mirror route, and no local refraction/lens, human-eye or dispersion/scattering
canonical package currently exists.

### Existing electricity

`MATRIX-PHY-ELEC-CURRENT-OHM`

Current canonical library owns only:

```text
CAP-ELEC-CURRENT-CONSERVATION
CAP-ELEC-OHMIC-MODEL-TEST
```

The seven-rung matrix is much broader than those two current canonical records. Potential
difference, resistance/resistivity, series/parallel combination, heating/power and practical
measurement closure still need capability-level reconciliation rather than blanket acceptance
of the old synthesis rows.

### Existing magnetism

`MATRIX-PHY-MAG-FIELD-LORENTZ`

Current canonical library owns:

```text
CAP-MAG-FIELD-DIRECTION
CAP-MAG-FLUX-ORIENTATION
CAP-MAG-REDIRECT-NOT-SPEED
```

Only part of this is naturally useful for current Grade 10. The current Grade-10 route needs
field patterns from current-carrying conductors/coils/solenoids, force-direction reasoning,
AC/DC and domestic-circuit understanding. Flux-orientation and charged-particle redirection
must not be pulled into the ordinary Grade-10 route merely because they already exist locally.

Likewise, the donor's quantitative Lorentz-force and Faraday/Lenz engineering may be richer
than the current Grade-10 summative demand. Reuse only what the current learner action needs.

## 4. Donor-to-local crosswalk

| Grade-10 production area | Current local state | Pinned donor #383 | Initial treatment |
| --- | --- | --- | --- |
| Reflection / spherical mirrors | partial local matrix + 3 canonical capabilities | `PHY-OPTICS-REFLECTION-MIRRORS` | **ENRICH existing**; close mirror ray/image/formula/application/practical semantics without changing bucket identity unless a real ownership conflict appears |
| Refraction / spherical lenses | no dedicated local canonical package | `PHY-OPTICS-REFRACTION-LENSES` | **NO_LOCAL_EQUIVALENT → candidate new capability family/bucket**; keep lens and refraction learner actions distinct where independently fail-able |
| Human eye / correction | no local canonical package | `PHY-OPTICS-HUMAN-EYE` | **NO_LOCAL_EQUIVALENT → candidate new capability family** |
| Prism / dispersion / scattering | no local canonical package | `PHY-OPTICS-DISPERSION-SCATTERING` | **NO_LOCAL_EQUIVALENT → candidate new capability family**; honour current exclusion of sunrise/sunset colour |
| Current / potential / Ohm / resistance | local matrix, canonical coverage incomplete | `PHY-ELEC-CURRENT-OHM` | **ENRICH existing**; reuse current conservation and Ohmic-model testing, add only independently fail-able missing learner actions |
| Series/parallel + resistivity + practical V–I | synthesis rows but no canonical closure | `PHY-ELEC-CURRENT-OHM` | **ENRICH existing**; do not call old synthesis readiness subject authority |
| Heating + electric power | not canonically closed locally | `PHY-ELEC-POWER-JOULE` | **ENRICH / candidate separate capability** after learner-action test; keep safety/domestic claims current-source bounded |
| Magnetic field direction | local `CAP-MAG-FIELD-DIRECTION` exists | `PHY-MAG-FIELD-LORENTZ` | **REUSE + ENRICH** for conductor/coil/solenoid field representations |
| Force on current-carrying conductor | no current Grade-10-specific canonical action | `PHY-MAG-FIELD-LORENTZ` | **ENRICH / candidate new capability**; Grade-10 success criterion is direction/model reasoning, not automatic advanced Lorentz algebra |
| DC / AC / domestic circuits | no clear local canonical owner | donor material only partially overlaps | **CONTENT GAP**; author current-source-bounded local capability/teaching as needed |
| Motor / induction / generator | existing local matrix/donor contain richer material | `PHY-MAG-INDUCTION-FARADAY` | **FORMATIVE-ONLY → DECLARED_EXTENSION or DEFER**; do not place in ordinary year-end route |

## 5. Anti-duplication decisions

Before any new Grade-10 capability:

```text
same learner action already local?
→ REUSE

same action, donor adds model condition / representation / misconception / verification?
→ ENRICH

new story only?
→ context, not capability

new representation but same success criterion?
→ normally same capability

independently fail-able learner action with a separate success criterion?
→ candidate new capability

donor sophistication beyond current summative scope?
→ DECLARED_EXTENSION / DEFER
```

This is especially important in optics and magnetism, where the donor has broad engineering
gates and the target system needs smaller learner actions.

## 6. Grade-10 production order

Use bounded slices, not one broad "Grade 10 Physics" PR.

```text
G10-1A  Reflection and spherical mirrors
        close the existing local matrix/library gap first

G10-1B  Refraction and spherical lenses
        create/adapt only the missing local capability structure

G10-2A  Human eye and corrective optics

G10-2B  Prism, dispersion and scattering

G10-3A  Current, potential difference, Ohm model, resistance/resistivity

G10-3B  Series/parallel networks + V–I/equivalent-resistance practical reasoning

G10-3C  Heating effect + electric power

G10-4A  Magnetic fields from current, conductor/coil/solenoid

G10-4B  Force on current-carrying conductor + Fleming left-hand rule

G10-4C  DC/AC + domestic circuits

G10-4X  Motor / electromagnetic induction / generator
        formative-only extension/defer; not ordinary summative route
```

The exact A/B/C split may collapse when two rows prove to be one learner action. Do not
create capability boundaries merely to preserve this planning list.

## 7. First bounded production slice

The first production PR should be:

```text
G10-1A — Reflection and spherical mirrors
```

Why:

- current source clearly requires it;
- Grade9V3 already has a partial local matrix and canonical package;
- the gap is concrete and bounded;
- donor semantics are mature enough to reduce reinvention;
- the local missing closure is visible: matrix R4–R6 currently lack canonical microtopic
  ownership;
- it provides a clean test of the Grade-9 donor-adaptation method at Grade 10 without first
  creating a new bucket.

G10-1A should compare, field by field:

```text
learner action
success criterion
prerequisite closure
mirror geometry / ray representation
Cartesian sign convention
mirror formula and magnification
model conditions
applications
misconceptions
diagnostic / repair
fresh verification
practical focal-length reasoning
problem families
transfer
falsifiers
provenance
```

Do not import donor paraxial/engineering depth beyond what is needed to explain the model's
validity safely at this grade.

## 8. Validation policy for Grade 10

For a bounded content-only adaptation:

```text
full repository guardrails
+ topic schema/conformance
+ prerequisite resolution
+ Core1A/Core1B closure
+ diagnosis/repair/fresh verification
+ topic session readiness
+ direct dependent routes
+ topic-specific donor falsifiers
```

Do **not** mechanically rerun every matrix benchmark unless shared routing, delivery,
feedback, evidence, matrix-contract or session semantics change.

After each completed Grade-10 slice, add one frozen blind agent-path stress checkpoint only
when it protects a meaningful boundary exposed by that slice.

## 9. Explicit non-goals

This discovery does not authorize:

- a Grade-10 matrix schema change;
- a grade/class field in matrices;
- a new readiness enum;
- donor runtime links;
- import of #383 readiness/curriculum metadata;
- bulk completion of all old Physics synthesis rows;
- Grade-11 authoring;
- JEE-depth pull-down;
- automatic summative inclusion of motor/induction/generator;
- reopening completed Grade-9 slices without a concrete regression.

## 10. Discovery disposition

```text
Grade 9 production / stress lane    COMPLETE
Grade 10 current-source scope       ESTABLISHED FOR PLANNING
Grade 10 donor crosswalk            ESTABLISHED
Grade 10 production content         NOT STARTED IN THIS DOCUMENT
first bounded production slice      G10-1A REFLECTION / SPHERICAL MIRRORS
architecture changes                NONE JUSTIFIED
```
