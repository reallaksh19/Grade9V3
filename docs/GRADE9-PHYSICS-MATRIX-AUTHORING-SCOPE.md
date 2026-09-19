# Grade 9 Physics matrix authoring scope

> Status: **current production authoring scope**
>
> Sequence: **Grade 9 → Grade 10 → Grade 11**.
>
> Current freeze: **author Grade 9 only**. Do not broaden the current task into the older
> mixed Physics-topic batch.

## Active learner-specific Grade-9 reconciliation

The ordinary Grade-9 authoring pass is complete. The current owner direction is to keep the
active workstream on **Grade 9** until the Pinnacle Terminal-1 school demand is reconciled.

Use these existing planning artifacts as the source of truth for that reconciliation:

- `docs/grade9/sources/TERMINAL1-PORTION-SHEET-2026-27.md`
- `docs/grade9/TERMINAL1-PINNACLE-PHYSICS-MICRO-SCOPE.md`
- `docs/grade9/terminal1-pinnacle-physics.micro-scope.json`

The portion sheet confirms chapter labels, not their detailed micro-scope. Therefore do not
bulk-author projectile motion, trig vector resolution, connected-body mechanics, incline
systems, pulley constraints or quantitative friction families until school material confirms
the exact learner action.

Keep school-demand evidence and repository readiness separate. A local gap is not automatically
a school requirement, and a confirmed school chapter is not automatically evidence for every
plausible subtopic inside it.

### Current investigation order

```text
1. Motion in 2 D
   confirm whether projectile/component-motion teaching is actually assessed

2. Vectors
   confirm arbitrary-angle decomposition, direction recovery, graphical addition
   and/or unit-vector notation

3. NLM
   confirm whether assessment extends beyond the current one-body Newton/FBD/friction
   spine into inclines, tension, multi-block or pulley systems

4. Motion 1 D
   mainly inspect exam-specific vertical-motion/problem-family demand
```

Until that evidence arrives, the next artifact is a **school question/subtopic → existing
capability → reuse/enrich/new-capability/question-variation crosswalk**, not another framework
layer.

## Why this scope exists

Grade9V3 now has enough architecture, benchmark coverage and session behavior to make broad
ontology-building counterproductive. The current job is narrower:

```text
real Grade-9 demand
→ current canonical capability/microtopic
→ existing matrix/rung where possible
→ honest gap when missing
→ smallest justified authoring change
```

The matrix remains a pedagogical ladder. It is **not** a curriculum authority.

Do not add `grade`, `grade_level`, `class`, `syllabus_status`, or a similar field to
`Shared/library/matrix.schema.json`. Curriculum/grade claims belong in the existing source,
curriculum-mapping, supplied-syllabus and route-scope layers.

## Donor adaptation rule

Before fresh Physics authoring, search the repository owner's prior `reallaksh19/Common`
Physics PRs from the mature engineering period (PR #350 onward).

The rule is **copy with adaptation, never cross-repository linking**:

```text
prior internal Physics record
        ↓ inspect
extract reusable physics semantics
        ↓
compare with current Grade9V3 capability
        ↓
copy/adapt only the useful delta into Grade9V3
        ↓
local Grade9V3 source_refs / tests / readiness
```

Do **not** put Common paths, Common gate IDs, Common readiness state, or cross-repository
references into Grade9V3 runtime records. Donor PR/commit identifiers may be kept only in
working/audit notes when traceability is useful.

Do not inherit donor curriculum authority. Current Grade9V3 scope still uses
`SYLLABUS_REQUIREMENT | QUESTION_DEMAND | PREREQUISITE | DECLARED_EXTENSION | DEFER`.

The target architecture wins when granularity differs: one broad donor gate may map to
several independently fail-able Grade9V3 capabilities, and advanced donor material may be
discarded or kept extension-only.

## Grade-9 authoring progress

| Slice | Status | Evidence |
| --- | --- | --- |
| G9-1 Motion | **AUDITED** | `docs/grade9/G9-1-MOTION-AUTHORING-AUDIT.md`; existing six-rung spine reused, broad Vector Add/Sub bucket prerequisite removed |
| G9-2 Force and Laws of Motion | **AUDITED** | `docs/grade9/G9-2-FORCE-LAWS-AUTHORING-AUDIT.md`; existing seven-rung matrix reused, frame choice bounded to extension demand, false turning-point prerequisite removed |
| G9-3 Gravitation | **DONOR-ADAPTED / AUDITED** | `docs/grade9/G9-3-GRAVITATION-AUTHORING-AUDIT.md`; force/model-scope/local-g semantics copied and adapted locally; energy/orbit retained as extensions |
| G9-4 Work, Energy and Power | **DONOR-ADAPTED / AUDITED** | `docs/grade9/G9-4-WORK-ENERGY-POWER-AUTHORING-AUDIT.md`; existing seven-rung spine retained, system-boundary and conditional-conservation semantics strengthened |
| G9-5 Sound | **DONOR-ADAPTED / AUDITED** | `docs/grade9/G9-5-SOUND-AUTHORING-AUDIT.md`; existing five-rung spine retained, longitudinal representation and echo-model boundaries strengthened |
| G9-6 Simple Machines | **AUDITED / COMPLETE** | `docs/grade9/G9-6-SIMPLE-MACHINES-AUTHORING-AUDIT.md`; three-rung spine retained, same-state MA measurement/practical semantics strengthened |

## Grade-9 pass status

**COMPLETE.** G9-1 through G9-6 are audited and merged; Grade 10 remains outside the active freeze.

All six active Grade-9 production slices have now been audited. The freeze remains in force:
do not begin Grade 10 in the same authoring PR.

## Current Grade-9 Physics production order


Work in this order.

| Priority | Production slice | Repository matrix / treatment | Current rule |
| --- | --- | --- | --- |
| G9-1 | Motion | `MATRIX-PHY-KIN-1D-MOTION` | Core Grade-9 authoring target |
| G9-2 | Force and Laws of Motion | `MATRIX-PHY-NLM-FIRST-LAW` | Core Grade-9 authoring target |
| G9-3 | Gravitation | `MATRIX-PHY-GRAV-UNIVERSAL-LAW` | Core Grade-9 authoring target |
| G9-4 | Work, Energy and Power | `MATRIX-PHY-WORK-ENERGY-POWER` | Core Grade-9 authoring target |
| G9-5 | Sound | `MATRIX-PHY-SOUND` | Core Grade-9 authoring target |
| G9-6 | Simple Machines | `MATRIX-PHY-SIMPLE-MACHINES` | Current Standard syllabus scope confirmed; detailed matrix audit remains sequenced after G9-5 |
| support only | Vector representation / addition | `MATRIX-PHY-VECTOR-REPRESENTATION`, `MATRIX-PHY-VEC-ADD-SUB` | Include only as prerequisite, advanced-question demand or declared extension |
| extension only | Relative motion | `MATRIX-PHY-RELATIVE-MOTION` | Question-demand / declared-extension route, not ordinary Grade-9 scope by default |
| defer | Rotation, thermodynamics, SHM/waves, electricity, magnetism, optics, broad fluids/Bernoulli | existing matrices remain in repository | Do not author in this Grade-9 pass unless a verified current Grade-9 source or real worksheet demand justifies the exact slice |

Existing higher-grade or broader matrices are **not deleted**. They are simply outside the
current authoring queue.

### Gravitation boundary

If a verified Grade-9 source requires mass/weight, free fall, pressure, buoyancy or a related
slice, map that exact learner demand into the existing capability structure or author the
smallest missing canonical record.

Do **not** import the whole `MATRIX-PHY-FLUID-BERNOULLI-EQUATION` matrix into Grade-9
authoring merely because pressure/buoyancy is adjacent to gravitation in one curriculum
presentation.

## Authoring working sheet

Use one planning-only column:

```text
SCOPE_REASON
```

Allowed working values:

```text
SYLLABUS_REQUIREMENT
QUESTION_DEMAND
PREREQUISITE
DECLARED_EXTENSION
DEFER
```

`DEFER` is authoring shorthand only. It is not a new runtime enum and must not be added to
Shared contracts.

Example:

| Proposed rung / capability | SCOPE_REASON | Canonical record? | Matrix action |
| --- | --- | --- | --- |
| distance vs displacement | `SYLLABUS_REQUIREMENT` | search current library | reference existing record if present |
| acceleration | `SYLLABUS_REQUIREMENT` | search current library | reference or expose an honest gap |
| vector component addition | `PREREQUISITE` / `QUESTION_DEMAND` | likely existing | include only when demanded |
| relative-velocity boat problem | `DECLARED_EXTENSION` | existing route | keep outside ordinary Grade-9 scope |
| torque / angular momentum | `DEFER` | higher-grade content | do not author in this pass |

## Per-rung procedure

For **every** proposed Grade-9 rung:

1. Search the current `Physics/library/`.
2. Identify the learner action the rung is supposed to represent.
3. If an appropriate canonical microtopic already exists:
   - reference its `microtopic_ref`;
   - use truthful current provenance under the existing matrix contract;
   - do not duplicate the microtopic's teaching, misconception, repair or exit task.
4. If no canonical microtopic exists:
   - represent the gap honestly using the existing matrix provenance/gap semantics;
   - do not create canonical teaching merely to make the matrix look complete.
5. Check prerequisite refs before creating a new capability.
6. Do not pull Grade-10/11 content downward just because it connects neatly.

The historical broad-offload assumption that most units have no canonical content is no
longer valid.

## Four QA questions outside the JSON

Before accepting any Grade-9 rung, answer:

```text
1. Is this justified by Grade-9 syllabus, actual question demand, a real prerequisite,
   or an explicit extension?

2. Does a canonical microtopic/capability already teach this learner action?

3. Is this one independently fail-able learner capability with an observable success criterion?

4. Is this genuinely a new learner action, or merely the same capability in another context?
```

If question 4 says “context only”, reuse the capability.

Do not create context-named capabilities such as:

```text
falling-stone capability
moon capability
lift capability
boat capability
pulley-story capability
```

when the reusable learner action is unchanged.

## Required matrix shape

Keep the finalized matrix contract unchanged:

```text
matrix
├── matrix_id
├── subject
├── bucket_id
├── topic
├── subtopic
│
├── rungs[]
│   ├── rung
│   ├── ladder_position
│   ├── provenance
│   ├── microtopic_ref        when canonical
│   ├── ceiling[]
│   ├── must_contain[]
│   └── controlled_variation[]
│
├── family
│   ├── invariant_demand
│   ├── difficult_move
│   ├── independent_check
│   └── support_ladder
│       ├── low
│       ├── medium
│       └── high
│
└── transfer[]
    ├── dimension
    ├── changed_demand
    ├── information_not_handed_over
    └── repair_to
```

Do not add learner/session state to this structure.

## Scope authority

The current Grade-9 queue is an **authoring-workstream decision**, not a claim that every
listed matrix is prescribed by every current CBSE/NCERT Grade-9 pathway.

Where curriculum sources are in transition or multiple pathways exist:

```text
verified curriculum/source binding
→ curriculum-backed scope

real worksheet/question
→ QUESTION_DEMAND

true dependency
→ PREREQUISITE

deliberate enrichment
→ DECLARED_EXTENSION

none of the above
→ DEFER
```

Do not silently convert provisional, advanced, extension or historical material into
ordinary Grade-9 syllabus truth.

## Source notes for this freeze

Use authoritative source custody before making exact curriculum claims.

Current external references motivating the cautious boundary include:

- NCERT Class IX Science textbook material;
- NCERT Secondary Stage / Grade 9 syllabus material;
- CBSE Academic 2026-27 curriculum, which separately lists Class IX `Science` and
  `Science at Advanced Level`.

These references justify **checking scope explicitly**. They do not by themselves authorize a
matrix record or promote canonical content.

## Completion condition for the Grade-9 pass

The Grade-9 authoring pass is complete when:

- G9-1 through G9-5 have internally coherent matrices against current canonical content;
- G9-6 is either explicitly bound to a verified source/demand or remains provisional;
- prerequisite/extension vector content is only as deep as real Grade-9 work requires;
- relative motion remains a visible extension/question-demand path;
- deferred higher-grade matrices have not been expanded for completeness;
- all changed matrices pass existing conformance/readiness/guardrail checks;
- missing teaching remains visible rather than fabricated.

Only then open the **Grade-10** authoring pass. Grade 11 follows Grade 10.

## Anti-drift

```text
No schema change for grade.
No one-rung-per-question.
No one-capability-per-story context.
No higher-grade pull-down for elegance.
No broad Physics completion target.
No canonical teaching invented for matrix completeness.
No source claim without source custody.
No learner state in matrices.
```

The target is not broad Physics coverage.

The target is:

> **Build the smallest durable Grade-9 Physics learning map that makes real Grade-9
> questions explainable, teachable and diagnosable, then move to Grade 10.**
