# Grade-10 Physics donor crosswalk

> Status: planning/audit artifact only.
>
> Target architecture remains Grade9V3. Donor files supply reusable Physics semantics, not
> runtime dependencies, curriculum authority, learner state or release/readiness authority.

## Pinned donor snapshot

### Common PR #350 — canonical Physics line

- role: preferred semantic/architecture donor where a canonical gate already exists;
- state at discovery: OPEN;
- pinned head SHA: `9c7d363d2ae2866ac829ae6b8039eeb8c1abc2c0`;
- repository: `reallaksh19/Common`.

This is not a promise that the open PR will remain unchanged. Refresh the pin before using
new donor bytes in a production PR.

### Common PR #383 — 43-subtopic breadth/discovery registry

- role: Grade 9–11 discovery catalogue and first-pass semantic donor;
- state at discovery: OPEN;
- pinned head SHA: `e92481f6e03a8bb49a55f568b03cba7c12fb942a`;
- registry path:
  `Grade 9/V2/Physics/Blueprint/policy/physics-technical-engineering-gates.v1.json`;
- registry blob SHA observed in this pass:
  `89b009c31c79ad4b2009577220705d2711eadc4b`.

Do not inherit its `technical_readiness`, `jee_tier` or historical `cbse_ref` as current
Grade9V3 authority.

### Common PR #402 — observability/SIL programme

- role: discovery/observability history and rich subject-intelligence evidence;
- state at discovery: CLOSED, not merged;
- pinned head SHA: `efd5d47df8daa3de5996d8419652dd76cb08dc89`.

Use only when it adds concrete reusable semantics. Do not treat the closed programme as
release authority.

## Grade-10 donor inventory from PR #383

At the pinned #383 head, the registry contains eight records labelled Grade 10:

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

These names are donor discovery identifiers only.

## Capability-level crosswalk

| Donor | Current Grade9V3 | Initial treatment | Main caution |
| --- | --- | --- | --- |
| `PHY-OPTICS-REFLECTION-MIRRORS` | `MATRIX-PHY-OPTICS-REFLECTION-MIRRORS` + partial library | **ENRICH** | Keep local learner-capability decomposition; fill R4-R6 only from current scope + useful donor semantics |
| `PHY-OPTICS-REFRACTION-LENSES` | no dedicated local learner spine found | **NO_LOCAL_EQUIVALENT / candidate new slice** | Do not create until current source binds the required lens actions |
| `PHY-OPTICS-HUMAN-EYE` | no dedicated local learner spine found | **NO_LOCAL_EQUIVALENT / candidate new slice** | Do not let the donor's chapter mapping substitute for current authority |
| `PHY-OPTICS-DISPERSION-SCATTERING` | no dedicated local learner spine found | **NO_LOCAL_EQUIVALENT / candidate new slice** | Keep daily-life/qualitative scope separate from unnecessary wave-optics depth |
| `PHY-ELEC-CURRENT-OHM` | `MATRIX-PHY-ELEC-CURRENT-OHM` + partial library | **ENRICH + NARROW ordinary route** | Existing R2 microscopic drift/current-density and R7 Kirchhoff depth must not be pulled down automatically |
| `PHY-ELEC-POWER-JOULE` | power appears as matrix R6; no canonical microtopic | **ENRICH existing electricity bucket first** | Heating/power may be independently fail-able capabilities, but do not create a second matrix just because the donor has a separate gate |
| `PHY-MAG-FIELD-LORENTZ` | `MATRIX-PHY-MAG-FIELD-LORENTZ` + partial library | **ENRICH + NARROW ordinary route** | Current local flux/charged-particle content is broader than a safe Grade-10 assumption |
| `PHY-MAG-INDUCTION-FARADAY` | induction ideas appear in matrix R5/R6; no canonical microtopic | **ENRICH existing magnetism bucket first** | Preserve qualitative induction/current-direction learning before importing full Faraday/Lenz/motional-emf formalism |

## Anti-duplication test for Grade 10

For every donor action:

```text
same learner action already local?
→ REUSE

same action, donor has stronger model condition / misconception / verification?
→ ENRICH

new story/context only?
→ REUSE capability

new representation, same success criterion?
→ usually REUSE

independently fail-able learner action with a distinct success criterion?
→ candidate NEW CAPABILITY

donor sophistication exceeds current Grade-10 source?
→ DEFER / DECLARED_EXTENSION
```

## Donor-to-local translation

Useful donor material may map into existing Grade9V3 structures as follows:

```text
canonical concept / model condition
→ inferential_jump / teaching_path / why_valid

reasoning sequence
→ teaching_path / Core1B elicitation

misconception
→ misconception + diagnostic_prompt + repair

representation invariant
→ must_contain / controlled_variation / teaching step

verification / falsifier
→ exit_task check / targeted regression

problem family / transfer
→ question_family / matrix transfer
```

Do not import donor release checklists, technical-readiness values, JEE tiers, schema
machinery or old curriculum declarations simply because they are present.

## First production slice — handoff

The discovery pass recommends one bounded next slice:

```text
G10-1  Reflection and spherical mirrors
```

The production agent should:

1. bind the current Grade-10 source for the reflection/mirror slice;
2. inspect the current local matrix and library first;
3. inspect the pinned donor record(s);
4. compare R1-R6 at the learner-action level;
5. preserve R1-R3 unless a concrete semantic defect is demonstrated;
6. author/adapt only the missing durable R4-R6 teaching/repair/verification required by
   current Grade-10 scope;
7. keep lens/human-eye/electricity/magnetism out of the same PR;
8. add one targeted post-slice stress checkpoint only after the production route is real;
9. run repository guardrails and the topic-relevant readiness/benchmark checks.

No shared architecture change is justified by this discovery.
