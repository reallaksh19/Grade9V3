# Pedagogical Schema Matrix: Subtopic 2 — Vector Representation and Subtraction (`BUCKET-VECTOR-REPRESENTATION`)

**Repository:** `reallaksh19/Grade9V3`  
**Working Source of Truth:** Head of Pull Request #1 (`p0-foundations`, commit `916169a`)  
**Scope:** semantic members of `BUCKET-VECTOR-REPRESENTATION`, derived from `microtopic.bucket_id`  
**Execution Phase:** **Phase A: Strict Extraction Only**  
**Architectural Mode:** Strict Source Extraction & Multi-Authority Divergence Accounting. Values are recorded only when backed by repository evidence; analytical synthesis is explicitly marked; no Core1B prompts are authored in this phase.

---

## 1. Semantic Scope and Authority Inventory

**Conceptual ownership is determined by `microtopic.bucket_id`, not by the file that physically stores a microtopic.**

The source file `Physics/library/vector-representation.v1.json` physically contains four microtopic records, but only three are owned by `BUCKET-VECTOR-REPRESENTATION`. The fourth record, `MIC-FRAME-QUALIFICATION-BOUNDARY`, declares `bucket_id: "BUCKET-RELATIVE-MOTION"` and is therefore a Relative Motion research-boundary microtopic.

```yaml
bucket_membership:
  BUCKET-VECTOR-REPRESENTATION:
    instructional_microtopics:
      - MIC-VECTOR-VS-SCALAR
      - MIC-SIGNED-COMPONENT
      - MIC-GRAPHICAL-SUBTRACTION

  BUCKET-RELATIVE-MOTION:
    research_boundary_microtopics:
      - MIC-FRAME-QUALIFICATION-BOUNDARY
```

| Source File / Asset | Authority Classification | Scope / Role in Subtopic 2 | Status & Unresolved Gaps |
| :--- | :--- | :--- | :--- |
| **`Physics/gates/curriculum-bindings.v1.json`** | **Governed / Authoritative** | Curriculum scope authority; declares `bindings: []`. | Grade 9 2D vector representation gates fail closed as `OWNER_EXTENSION` (`CURRICULUM_BINDING_GAP`). |
| **`Physics/gates/motion-vectors.v1.json`** | **Governed / Authoritative** | Three vector-foundation gates: `PHY-VEC-SCALAR-VECTOR`, `PHY-VEC-AXIS-CONVENTION`, `PHY-VEC-SUBTRACTION`. | Mature at `ENGINEERING` level; author-created and not independently reviewed. |
| **`Physics/adapter/CoreContracts.json`** | **Governed / Authoritative** | Subject adapter: validators and implemented representation kinds (`VECTOR`, `VECTOR_SUBTRACTION`). | Does not itself define teaching content. |
| **`Physics/library/vector-representation.v1.json`** | **Library Candidate** (`status: CANDIDATE`) | Physically stores 4 microtopic records. Semantic ownership is 3 vector-foundation members plus 1 Relative Motion research-boundary member. | `BUCKET-VECTOR-REPRESENTATION.conventions[]` absent (`CONVENTION_GAP`); the three vector-owned microtopics have no `elicitation` key (`CORE1B_AUTHOR_REQUIRED`); `ISS-VEC-EXIT-DATA` affects `MIC-SIGNED-COMPONENT`. |
| **`CAP-SIGNED-PAIR-BRIDGE`** | **External-Provider Capability Candidate** | Signed-coordinate prerequisite. | `external_provider: Mathematics`; `acceptance_status: PROVIDER_REVIEW_REQUIRED`. |
| **`CAP-RIGHT-TRIANGLE-BRIDGE`** | **External-Provider Capability Candidate** | Right-triangle magnitude prerequisite. | `external_provider: Mathematics`; `acceptance_status: PROVIDER_REVIEW_REQUIRED`. |
| **`SRC-AUTHOR-VEC`** | **Authored Source** (`status: CANDIDATE`) | V3B vector-representation design seed. | Author-created project draft; no official exam provenance claimed. |
| **`SRC-NCERT-PLANE`** | **Curriculum Candidate** (`status: CANDIDATE`) | Motivates graphical vector addition/subtraction. | Exact claim-level reconciliation pending. |
| **`SRC-PHET`** | **Activity Source Candidate** (`status: CANDIDATE`) | Candidate visual exploration route. | Simulation not executed as repository evidence. |

### Out of Scope for this Subtopic

`MIC-FRAME-QUALIFICATION-BOUNDARY` is **not** a fourth vector-representation contract. It belongs to `BUCKET-RELATIVE-MOTION`, references `REL-RELATIVE-VELOCITY`, depends on `MIC-GEOMETRIC-CHECK`, and must be handled as a distinct research-boundary contract. Its future Core1B treatment is intentionally **not decided by this Phase A vector-foundation matrix**.

---

## 2. Schema Provenance and Extraction Discipline

```yaml
schema_provenance:
  status: AUTHORING_ANALYSIS_OVERLAY
  repository_fields: SOURCE_EXTRACTED
  pedagogical_fields:
    - target_aha
    - controlled_experience
    - representation_bridge
  rule: >
    A pedagogical overlay may organize source evidence, but any analytical
    construction not literally present in source must be marked author-required.
```

The matrix uses the following custody rules:

1. `microtopic.bucket_id` is the semantic ownership field.
2. Missing keys and explicit JSON `null` are different source states.
3. `bucket.conventions[]` absence makes the Core1/Core1A role contract incomplete even when source content is present.
4. Core1B's obligation to carry Core1A coverage does not prove an elicitation design has been authored or shown feasible.
5. A vary/hold/notice construction is marked `CONTROLLED_EXPERIENCE_SYNTHESIS_AUTHOR_REQUIRED` whenever it requires analytical combination or transformation of source facts.
6. Scope claims must be traceable to the microtopic/library/gate record or be marked author-required.

---

## 3. Canonical Vector-Foundation Contracts

### 3.1 `MIC-VECTOR-VS-SCALAR` — Magnitude, vector and signed component

```yaml
microtopic_id: MIC-VECTOR-VS-SCALAR
bucket_id: BUCKET-VECTOR-REPRESENTATION
source_refs:
  - Physics/library/vector-representation.v1.json#microtopics[MIC-VECTOR-VS-SCALAR]
  - Physics/gates/motion-vectors.v1.json#gates[PHY-VEC-SCALAR-VECTOR]

source_support:
  inferential_jump: PRESENT
  teaching_path: PRESENT
  misconceptions: PRESENT
  exit_task: PRESENT
  bucket_conventions: ABSENT
  elicitation_key: ABSENT

entry_capability:
  - capability_ref: CAP-SIGNED-PAIR-BRIDGE
    provider: Mathematics
    acceptance_status: PROVIDER_REVIEW_REQUIRED
  - capability_ref: CAP-RIGHT-TRIANGLE-BRIDGE
    provider: Mathematics
    acceptance_status: PROVIDER_REVIEW_REQUIRED

target_aha:
  status: SOURCE_BACKED_PEDAGOGICAL_OVERLAY
  value: >
    A nonnegative magnitude and a pair of signed components are different
    descriptions of one physical vector; the magnitude alone does not preserve direction.

controlled_experience:
  experience_1_orientation_vs_magnitude:
    status: SOURCE_EXTRACTED
    source_basis: >
      Source misconception/diagnostic compares (3,4) and (4,3) m/s, which have
      equal magnitude but different directions.
    prompt: "Two vectors, (3,4) and (4,3) m/s, have the same magnitude. Do they point the same way?"
  experience_2_negative_component_sign:
    status: CONTROLLED_EXPERIENCE_SYNTHESIS_AUTHOR_REQUIRED
    source_basis: >
      Source provides the negative-component counterexample (0,-4) m/s with speed 4 m/s.
      Converting that evidence into a positive-vs-negative vary/hold experiment is analytical synthesis.
    raw_counterexample: "A velocity of (0,-4) m/s has speed 4 m/s, not -4 m/s."

representation_bridge:
  engineering_gate:
    representation_ref: REP-VEC-SINGLE
    kind: VECTOR
    relation_bindings: [REL-VEC-MAGNITUDE]
  library:
    representation_refs: [REP-VECTOR-COMPONENT]
    kind: VECTOR
    relation_bindings: [REL-VECTOR-SUBTRACTION]
  alignment_status: CROSS_LAYER_REPRESENTATION_DIVERGENCE

governing_convention:
  source_state: ABSENT
  status: CONVENTION_AUTHOR_REQUIRED

scope:
  source_backed_include:
    - 2D Cartesian plane with perpendicular declared axes.
    - Nonnegative magnitude derived from signed perpendicular components.
  author_required_or_removed:
    - "Constant velocities / displacements"  # removed from asserted scope: not directly supported by this microtopic/gate evidence

core1b:
  source_state: ABSENT
  status: CORE1B_AUTHOR_REQUIRED
  required_coverage: SAME_AS_CORE1A
  elicitation_design: NOT_AUTHORED
```

### 3.2 `MIC-SIGNED-COMPONENT` — Choosing axes and keeping components signed

```yaml
microtopic_id: MIC-SIGNED-COMPONENT
bucket_id: BUCKET-VECTOR-REPRESENTATION
source_refs:
  - Physics/library/vector-representation.v1.json#microtopics[MIC-SIGNED-COMPONENT]
  - Physics/gates/motion-vectors.v1.json#gates[PHY-VEC-AXIS-CONVENTION]

source_support:
  inferential_jump: PRESENT
  teaching_path: PRESENT
  misconceptions: PRESENT
  exit_task: PRESENT
  bucket_conventions: ABSENT
  elicitation_key: ABSENT
  exit_task_data_atoms: HELD_BY_ISS-VEC-EXIT-DATA

target_aha:
  status: SOURCE_BACKED_PEDAGOGICAL_OVERLAY
  value: >
    Axis choice is a declared decision; once declared, each component sign is fixed by that choice.

controlled_experience:
  status: CONTROLLED_EXPERIENCE_SYNTHESIS_AUTHOR_REQUIRED
  source_basis: vector-representation.v1.json teaching steps SC-2 and SC-3
  note: >
    The source directly contains axis re-declaration and magnitude-invariance steps.
    Packaging them as a single vary/hold/notice experiment is analytical synthesis.

representation_bridge:
  engineering_gate:
    representation_ref: REP-AXIS-CONVENTION
    kind: VECTOR
    relation_bindings: [REL-AXIS-REVERSAL]
  library:
    representation_refs: [REP-VECTOR-COMPONENT]
    kind: VECTOR
  alignment_status: CROSS_LAYER_REPRESENTATION_DIVERGENCE

governing_convention:
  source_state: ABSENT
  status: CONVENTION_AUTHOR_REQUIRED

scope:
  source_backed_include:
    - Cartesian axes in a plane.
    - Re-declaration of axis direction and consequent component-sign change.
    - Magnitude invariance under sign reversal of a component caused by axis re-declaration.
  source_backed_exclude:
    - Oblique axes.
    - Rotating frames.

core1b:
  source_state: ABSENT
  status: CORE1B_AUTHOR_REQUIRED
  required_coverage: SAME_AS_CORE1A
  elicitation_design: NOT_AUTHORED
```

### 3.3 `MIC-GRAPHICAL-SUBTRACTION` — Subtraction as addition of the reversed vector

```yaml
microtopic_id: MIC-GRAPHICAL-SUBTRACTION
bucket_id: BUCKET-VECTOR-REPRESENTATION
source_refs:
  - Physics/library/vector-representation.v1.json#microtopics[MIC-GRAPHICAL-SUBTRACTION]
  - Physics/gates/motion-vectors.v1.json#gates[PHY-VEC-SUBTRACTION]

source_support:
  inferential_jump: PRESENT
  teaching_path: PRESENT
  misconceptions: PRESENT
  exit_task: PRESENT
  bucket_conventions: ABSENT
  elicitation_key: ABSENT

target_aha:
  status: SOURCE_BACKED_PEDAGOGICAL_OVERLAY
  value: "P - Q is P + (-Q): reverse Q without changing its length, then add tail-to-head."

controlled_experience:
  status: CONTROLLED_EXPERIENCE_SYNTHESIS_AUTHOR_REQUIRED
  source_basis: >
    Gate/library misconceptions and checks supply operand-order and reversal evidence.
    A unified vary/hold/notice experiment is an analytical construction, not a literal source field.

representation_bridge:
  engineering_gate:
    representation_ref: REP-SUB-CONSTRUCTION
    kind: VECTOR
    relation_bindings: [REL-VEC-SUBTRACTION]
  library:
    representation_refs: [REP-VECTOR-SUBTRACTION-CONSTRUCTION]
    kind: VECTOR_SUBTRACTION
  alignment_status: CROSS_LAYER_REPRESENTATION_DIVERGENCE

governing_convention:
  source_state: ABSENT
  status: CONVENTION_AUTHOR_REQUIRED

scope:
  source_backed_include:
    - 2D graphical vector subtraction as addition of the reversed vector.
    - Translation of a free vector without rotation for tail-to-head construction.
    - Reconciliation with signed-component subtraction.
  source_backed_exclude:
    - Vector division or cross products.

core1b:
  source_state: ABSENT
  status: CORE1B_AUTHOR_REQUIRED
  required_coverage: SAME_AS_CORE1A
  elicitation_design: NOT_AUTHORED
```

---

## 4. Core1 / Core1A Role-Completeness Matrix

Source content and role-contract completeness are intentionally separate dimensions.

| Microtopic | Core1 Source Content | Core1 Role Contract | Core1A Source Content | Core1A Role Contract | Blocking Gap |
| :--- | :---: | :---: | :---: | :---: | :--- |
| `MIC-VECTOR-VS-SCALAR` | `PRESENT` | **`INCOMPLETE`** | `PRESENT` | **`INCOMPLETE`** | `CONVENTION_GAP`; external Mathematics provider review also pending. |
| `MIC-SIGNED-COMPONENT` | `PRESENT` | **`INCOMPLETE`** | `PRESENT` | **`INCOMPLETE`** | `CONVENTION_GAP`; `DATA_GAP` on exit-task atoms. |
| `MIC-GRAPHICAL-SUBTRACTION` | `PRESENT` | **`INCOMPLETE`** | `PRESENT` | **`INCOMPLETE`** | `CONVENTION_GAP`. |

The `INCOMPLETE` status is structural: `bucket.conventions[]` is required by the Core1/Core1A role contract and is absent from the candidate bucket. It does not erase the source teaching content that is already present.

---

## 5. Core1B Source-State Matrix — Strict Extraction Only

The candidate microtopic records are inspected by key presence. For all three vector-owned microtopics, the `elicitation` key is **absent**. This is not represented as JSON `null`.

| Microtopic | Source State | Status | Required Coverage | Elicitation Design |
| :--- | :---: | :---: | :---: | :---: |
| `MIC-VECTOR-VS-SCALAR` | **`ABSENT`** | **`CORE1B_AUTHOR_REQUIRED`** | `SAME_AS_CORE1A` | `NOT_AUTHORED` |
| `MIC-SIGNED-COMPONENT` | **`ABSENT`** | **`CORE1B_AUTHOR_REQUIRED`** | `SAME_AS_CORE1A` | `NOT_AUTHORED` |
| `MIC-GRAPHICAL-SUBTRACTION` | **`ABSENT`** | **`CORE1B_AUTHOR_REQUIRED`** | `SAME_AS_CORE1A` | `NOT_AUTHORED` |

No Phase A claim is made that a particular Core1B elicitation design is feasible. Phase B must author and review that design.

---

## 6. Representation Alignment

| Microtopic | Gate Representation | Library Representation | Alignment Status |
| :--- | :--- | :--- | :--- |
| `MIC-VECTOR-VS-SCALAR` | `REP-VEC-SINGLE` (`VECTOR`) | `REP-VECTOR-COMPONENT` (`VECTOR`) | `CROSS_LAYER_REPRESENTATION_DIVERGENCE` |
| `MIC-SIGNED-COMPONENT` | `REP-AXIS-CONVENTION` (`VECTOR`) | `REP-VECTOR-COMPONENT` (`VECTOR`) | `CROSS_LAYER_REPRESENTATION_DIVERGENCE` |
| `MIC-GRAPHICAL-SUBTRACTION` | `REP-SUB-CONSTRUCTION` (`VECTOR`) | `REP-VECTOR-SUBTRACTION-CONSTRUCTION` (`VECTOR_SUBTRACTION`) | `CROSS_LAYER_REPRESENTATION_DIVERGENCE` |

These divergences remain explicit; no representation authority is collapsed into the other.

---

## 7. Phase-B Backlog — Vector Foundation Only

Phase B remains blocked until this Phase A correction is reviewed. When Phase B begins, the vector-foundation backlog is:

1. Author Core1B elicitation designs for the three vector-owned instructional microtopics, preserving `required_coverage: SAME_AS_CORE1A` without assuming feasibility in advance.
2. Declare `BUCKET-VECTOR-REPRESENTATION.conventions[]` so Core1/Core1A role contracts can become complete.
3. Obtain Mathematics-provider review for `CAP-SIGNED-PAIR-BRIDGE` and `CAP-RIGHT-TRIANGLE-BRIDGE`.
4. Resolve `ISS-VEC-EXIT-DATA` for the `MIC-SIGNED-COMPONENT` exit-task atoms.
5. Reconcile, or deliberately preserve with documented custody, the gate/library representation divergences.

### Explicitly Separate Decision

`MIC-FRAME-QUALIFICATION-BOUNDARY` is **not** included in the vector-foundation Core1B authoring batch. Before any Phase B work on that research-boundary microtopic, define its pedagogical role contract separately, including whether a non-assessment research-boundary note needs Core1B at all and, if so, what elicitation depth is appropriate.

---

## 8. Phase A Falsifier / Audit

The audit derives semantic membership across library files. It must not assume that physical file location implies bucket ownership.

```python
# Loaded from candidate library JSON files.
all_microtopics = [
    *relative_motion_data["microtopics"],
    *vector_representation_data["microtopics"],
]

def members(bucket_id):
    return {
        m["id"]
        for m in all_microtopics
        if m["bucket_id"] == bucket_id
    }

assert members("BUCKET-VECTOR-REPRESENTATION") == {
    "MIC-VECTOR-VS-SCALAR",
    "MIC-SIGNED-COMPONENT",
    "MIC-GRAPHICAL-SUBTRACTION",
}

assert members("BUCKET-RELATIVE-MOTION") == {
    "MIC-SAME-TIME",
    "MIC-COMMON-INTERVAL",
    "MIC-GEOMETRIC-CHECK",
    "MIC-FRAME-QUALIFICATION-BOUNDARY",
}

vector_target_microtopics = [
    m
    for m in all_microtopics
    if m["bucket_id"] == "BUCKET-VECTOR-REPRESENTATION"
]

for m in vector_target_microtopics:
    assert "elicitation" not in m
```

The audit intentionally distinguishes an absent key from an explicit `null` value.

---

## 9. Phase A Result

Physics source topology after correction:

```text
VECTOR FOUNDATION — BUCKET-VECTOR-REPRESENTATION
  3 instructional microtopics
  -> Core1/Core1A source content present
  -> Core1/Core1A role contract incomplete on CONVENTION_GAP
  -> Core1B source state ABSENT; authoring required

RELATIVE MOTION — BUCKET-RELATIVE-MOTION
  3 instructional microtopics
  -> Core1B already authored in relative-motion.v1.json

RELATIVE MOTION RESEARCH BOUNDARY — BUCKET-RELATIVE-MOTION
  1 research-boundary microtopic
  -> stored physically in vector-representation.v1.json
  -> future Core1B treatment requires an explicit separate pedagogical decision
```

Total authored narrow Physics microtopics remain **7**: **3 vector-foundation + 3 Relative Motion instructional + 1 Relative Motion research-boundary**. The 12 authority-`NONE` discovery packets remain quarantined from this authored-microtopic census.
