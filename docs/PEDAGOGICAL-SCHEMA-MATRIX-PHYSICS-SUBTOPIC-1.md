# Pedagogical Schema Matrix: Pilot 1 — Relative Motion in a Plane (Physics Subtopic 1)

**Repository:** `reallaksh19/Grade9V3`  
**Working Source of Truth:** Head of Pull Request #1 (`p0-foundations`, commit `916169a`)  
**Scope:** Pilot 1 instructional slice inside `BUCKET-RELATIVE-MOTION`  
**Architectural Mode:** Strict Source Extraction & Multi-Authority Divergence Accounting

---

## 1. Source and Authority Inventory

Every Physics asset used here is classified according to repository authority boundaries. Semantic bucket ownership is derived from each microtopic's `bucket_id`; physical file location is not treated as ownership.

| Source File / Directory | Authority Classification | Supported Assets | Missing Fields / Major Gaps |
| :--- | :--- | :--- | :--- |
| **`Physics/adapter/CoreContracts.json`** | **Governed / Authoritative** | Subject adapter; validators and implemented representation kinds (`VECTOR`, `VECTOR_SUBTRACTION`, `GRAPH`). | Does not define teaching content or bucket membership. |
| **`Physics/gates/curriculum-bindings.v1.json`** | **Governed / Authoritative** | Curriculum scope authority; `bindings: []`. | Grade 9 2D relative motion fails closed as `OWNER_EXTENSION` (`CURRICULUM_BINDING_GAP`). |
| **`Physics/gates/motion-vectors.v1.json`** | **Governed / Authoritative** | Relative-motion gates `PHY-REL-POSITION`, `PHY-REL-VELOCITY`, `PHY-REL-OBSERVER-REVERSAL`, plus vector-foundation gates. | Engineering maturity only; no independent scientific/pedagogical review. |
| **`Physics/library/relative-motion.v1.json`** | **Library Candidate** (`status: CANDIDATE`) | Physically stores the 3 instructional Relative Motion microtopics: `MIC-SAME-TIME`, `MIC-COMMON-INTERVAL`, `MIC-GEOMETRIC-CHECK`; includes Core1A teaching paths and authored Core1B elicitation. | `bucket.conventions[]` absent (`CONVENTION_GAP`); `MIC-SAME-TIME.representation_refs: []` despite gate representation (`GATE_REPRESENTATION_UNBOUND`); `ISS-REL-EXIT-DATA` holds exit coordinates. |
| **`Physics/library/vector-representation.v1.json`** | **Library Candidate** (`status: CANDIDATE`) | Physically stores 3 vector-foundation microtopics **plus** `MIC-FRAME-QUALIFICATION-BOUNDARY`, whose own `bucket_id` is `BUCKET-RELATIVE-MOTION`. | The boundary microtopic is a Relative Motion research-boundary member even though stored in this file; its `elicitation` key is absent. |
| **`Physics/content/relative-motion-g9/`** | **Published Frozen Evidence** | Baseline, plan, source atoms, compiled Core1A/Core1B/Core2A/Core2B artifacts, evidence and manifest. | Core1 was not selected for that baseline; authored questions are not official-exam provenance. |
| **`Physics/candidates/*.v1.json`** *(12 files)* | **Candidate Discovery Packets** (`packet_authority: NONE`) | Broad imported discovery packets. | No authored narrow relations/representations/data/questions/capabilities; remain quarantined from authored-microtopic census. |

---

## 2. Corrected Physics Topology

There are **7 authored narrow Physics microtopics** across two semantic buckets. File location does not determine bucket ownership.

```text
BUCKET-VECTOR-REPRESENTATION
├── MIC-VECTOR-VS-SCALAR
├── MIC-SIGNED-COMPONENT
└── MIC-GRAPHICAL-SUBTRACTION

BUCKET-RELATIVE-MOTION
├── MIC-SAME-TIME
├── MIC-COMMON-INTERVAL
├── MIC-GEOMETRIC-CHECK
└── MIC-FRAME-QUALIFICATION-BOUNDARY
```

The Relative Motion bucket is intentionally split by pedagogical role:

```yaml
bucket_membership:
  bucket_id: BUCKET-RELATIVE-MOTION
  instructional_microtopics:
    - MIC-SAME-TIME
    - MIC-COMMON-INTERVAL
    - MIC-GEOMETRIC-CHECK
  research_boundary_microtopics:
    - MIC-FRAME-QUALIFICATION-BOUNDARY
```

### 2.1 Authored Narrow Microtopic Census

| # | Microtopic ID | Physical Library File | Semantic Bucket | Role | Library Representation | Gate Representation | Core1B Source State |
| :- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | `MIC-SAME-TIME` | `relative-motion.v1.json` | `BUCKET-RELATIVE-MOTION` | Instructional | `[]` | `REP-REL-POSITION` | `PRESENT` |
| 2 | `MIC-COMMON-INTERVAL` | `relative-motion.v1.json` | `BUCKET-RELATIVE-MOTION` | Instructional | `REP-REL-VECTOR` | `REP-RELV-RESULTANT` | `PRESENT` |
| 3 | `MIC-GEOMETRIC-CHECK` | `relative-motion.v1.json` | `BUCKET-RELATIVE-MOTION` | Instructional | `REP-REL-VECTOR` | `REP-REV-PAIR` | `PRESENT` |
| 4 | `MIC-FRAME-QUALIFICATION-BOUNDARY` | `vector-representation.v1.json` | `BUCKET-RELATIVE-MOTION` | **Research boundary** | `[]` | None | **`ABSENT`** |
| 5 | `MIC-VECTOR-VS-SCALAR` | `vector-representation.v1.json` | `BUCKET-VECTOR-REPRESENTATION` | Instructional | `REP-VECTOR-COMPONENT` | `REP-VEC-SINGLE` | **`ABSENT`** |
| 6 | `MIC-SIGNED-COMPONENT` | `vector-representation.v1.json` | `BUCKET-VECTOR-REPRESENTATION` | Instructional | `REP-VECTOR-COMPONENT` | `REP-AXIS-CONVENTION` | **`ABSENT`** |
| 7 | `MIC-GRAPHICAL-SUBTRACTION` | `vector-representation.v1.json` | `BUCKET-VECTOR-REPRESENTATION` | Instructional | `REP-VECTOR-SUBTRACTION-CONSTRUCTION` | `REP-SUB-CONSTRUCTION` | **`ABSENT`** |

For the four records physically stored in `vector-representation.v1.json`, `elicitation` is represented as `ABSENT` because the key is not present. It is not represented as `null`.

### 2.2 Candidate Discovery Packets

The 12 `packet_authority: NONE` discovery packets remain outside the authored narrow-microtopic census. Their presence does not promote them into bucket members.

---

## 3. Pilot 1 Scope

Pilot 1 is a coherent **three-microtopic instructional slice** of `BUCKET-RELATIVE-MOTION`; it is not the entire semantic bucket.

```yaml
pilot_1:
  bucket_id: BUCKET-RELATIVE-MOTION
  instructional_scope:
    - MIC-SAME-TIME
    - MIC-COMMON-INTERVAL
    - MIC-GEOMETRIC-CHECK
  acknowledged_bucket_member_outside_instructional_slice:
    - MIC-FRAME-QUALIFICATION-BOUNDARY
```

The research-boundary member is kept separate because it is non-assessment material with a different pedagogical function. Pilot 1 does not silently promote it into an ordinary lesson.

---

## 4. Schema Provenance

```yaml
schema_provenance:
  status: AUTHORING_ANALYSIS_OVERLAY
  repository_fields: SOURCE_EXTRACTED
  pedagogical_fields:
    - target_aha
    - controlled_experience
    - representation_bridge
  note: >
    Overlay fields organize repository evidence for review and are not
    normative package fields unless separately promoted.
```

Custody rules:

1. `microtopic.bucket_id` controls semantic ownership.
2. Missing keys are recorded as `ABSENT`; explicit null values would be recorded separately if present.
3. Source content presence and role-contract completeness are separate dimensions.
4. Gate/library representation divergences remain explicit rather than being collapsed.
5. Pilot scope can be narrower than bucket membership when the excluded member has a distinct research-boundary role.

---

## 5. Pilot 1 Instructional Contracts

### 5.1 `MIC-SAME-TIME` — Position measured from the other object

```yaml
microtopic_id: MIC-SAME-TIME
bucket_id: BUCKET-RELATIVE-MOTION
role: INSTRUCTIONAL
source_refs:
  - Physics/library/relative-motion.v1.json#microtopics[MIC-SAME-TIME]
  - Physics/gates/motion-vectors.v1.json#gates[PHY-REL-POSITION]

target_aha:
  value: >
    Replace two origin-referenced positions with the displacement from the observer object
    to the observed object: r_A/B = r_A - r_B.

representation_bridge:
  engineering_gate:
    representation_ref: REP-REL-POSITION
    kind: VECTOR
  library:
    representation_refs: []
  alignment_status: GATE_REPRESENTATION_UNBOUND

governing_convention:
  source_state: ABSENT_AT_BUCKET_LEVEL
  status: CONVENTION_AUTHOR_REQUIRED

core1b:
  source_state: PRESENT
  authored_routes:
    - predict
    - attempt
    - reconstruct
    - boundary_test

known_gaps:
  - CONVENTION_GAP
  - GATE_REPRESENTATION_UNBOUND
  - DATA_COORDINATE_GAP  # ISS-REL-EXIT-DATA
```

### 5.2 `MIC-COMMON-INTERVAL` — From relative position to relative velocity

```yaml
microtopic_id: MIC-COMMON-INTERVAL
bucket_id: BUCKET-RELATIVE-MOTION
role: INSTRUCTIONAL
source_refs:
  - Physics/library/relative-motion.v1.json#microtopics[MIC-COMMON-INTERVAL]
  - Physics/gates/motion-vectors.v1.json#gates[PHY-REL-VELOCITY]

target_aha:
  value: >
    Subtract two same-time relative-position equations and divide by one shared
    nonzero observation interval to obtain v_A/B = v_A - v_B for the candidate's constant-velocity scope.

representation_bridge:
  engineering_gate:
    representation_ref: REP-RELV-RESULTANT
    kind: VECTOR
  library:
    representation_refs: [REP-REL-VECTOR]
    kind: VECTOR_SUBTRACTION
  alignment_status: CROSS_LAYER_REPRESENTATION_DIVERGENCE

governing_convention:
  source_state: ABSENT_AT_BUCKET_LEVEL
  status: CONVENTION_AUTHOR_REQUIRED

core1b:
  source_state: PRESENT
  authored_routes:
    - predict
    - attempt
    - reconstruct
    - boundary_test

known_gaps:
  - CONVENTION_GAP
```

### 5.3 `MIC-GEOMETRIC-CHECK` — Direction, magnitude and observer reversal

```yaml
microtopic_id: MIC-GEOMETRIC-CHECK
bucket_id: BUCKET-RELATIVE-MOTION
role: INSTRUCTIONAL
source_refs:
  - Physics/library/relative-motion.v1.json#microtopics[MIC-GEOMETRIC-CHECK]
  - Physics/gates/motion-vectors.v1.json#gates[PHY-REL-OBSERVER-REVERSAL]

target_aha:
  value: >
    Swapping the observer reverses the relative-velocity vector while preserving
    its magnitude: v_B/A = -v_A/B.

representation_bridge:
  engineering_gate:
    representation_ref: REP-REV-PAIR
    kind: VECTOR
  library:
    representation_refs: [REP-REL-VECTOR]
    kind: VECTOR_SUBTRACTION
  alignment_status: CROSS_LAYER_REPRESENTATION_DIVERGENCE

governing_convention:
  source_state: ABSENT_AT_BUCKET_LEVEL
  status: CONVENTION_AUTHOR_REQUIRED

core1b:
  source_state: PRESENT
  authored_routes:
    - predict
    - attempt
    - reconstruct
    - boundary_test

known_gaps:
  - CONVENTION_GAP
  - AUTOMATED_VERIFICATION_GAP  # no compass-string validator in adapter
```

---

## 6. Core1 / Core1A / Core1B Correspondence for the Instructional Slice

Source content presence and role completeness are separated explicitly.

| Microtopic | Core1 Source Content | Core1 Role Contract | Core1A Source Content | Core1A Role Contract | Core1B Source State | Blocking Gaps |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| `MIC-SAME-TIME` | `PRESENT` | **`INCOMPLETE`** | `PRESENT` | **`INCOMPLETE`** | `PRESENT` | `CONVENTION_GAP`, `GATE_REPRESENTATION_UNBOUND`, `DATA_COORDINATE_GAP` |
| `MIC-COMMON-INTERVAL` | `PRESENT` | **`INCOMPLETE`** | `PRESENT` | **`INCOMPLETE`** | `PRESENT` | `CONVENTION_GAP` |
| `MIC-GEOMETRIC-CHECK` | `PRESENT` | **`INCOMPLETE`** | `PRESENT` | **`INCOMPLETE`** | `PRESENT` | `CONVENTION_GAP`, `AUTOMATED_VERIFICATION_GAP` |

The role-contract incompleteness comes from missing bucket-level conventions; it does not mean the instructional source content or Core1B elicitation is absent.

---

## 7. Representation Alignment

| Microtopic | Gate Representation | Library Representation | Status |
| :--- | :--- | :--- | :--- |
| `MIC-SAME-TIME` | `REP-REL-POSITION` (`VECTOR`) | `[]` | `GATE_REPRESENTATION_UNBOUND` |
| `MIC-COMMON-INTERVAL` | `REP-RELV-RESULTANT` (`VECTOR`) | `REP-REL-VECTOR` (`VECTOR_SUBTRACTION`) | `CROSS_LAYER_REPRESENTATION_DIVERGENCE` |
| `MIC-GEOMETRIC-CHECK` | `REP-REV-PAIR` (`VECTOR`) | `REP-REL-VECTOR` (`VECTOR_SUBTRACTION`) | `CROSS_LAYER_REPRESENTATION_DIVERGENCE` |

No representation authority is silently replaced by another.

---

## 8. Research-Boundary Member — Separate Contract

`MIC-FRAME-QUALIFICATION-BOUNDARY` is a semantic member of `BUCKET-RELATIVE-MOTION`, but it is not part of the Pilot 1 instructional slice.

```yaml
microtopic_id: MIC-FRAME-QUALIFICATION-BOUNDARY
bucket_id: BUCKET-RELATIVE-MOTION
role: RESEARCH_BOUNDARY
physical_file: Physics/library/vector-representation.v1.json
primary_capability_ref: CAP-VECTOR-CHECK
relation_refs:
  - REL-RELATIVE-VELOCITY
prerequisite_refs:
  - MIC-GEOMETRIC-CHECK
assessment_scope: NON_ASSESSMENT_BOUNDARY_NOTE
elicitation:
  source_state: ABSENT
  phase_b_decision: DEFERRED_PENDING_EXPLICIT_PEDAGOGICAL_CONTRACT
```

The future authoring question is not assumed to have the same answer as for the three vector-foundation instructional microtopics. Before Phase B authors Core1B for this boundary note, reviewers must decide whether a non-assessment boundary note needs Core1B and what elicitation depth is appropriate.

---

## 9. Phase A Falsifier / Audit

The audit derives semantic membership across both library files and checks key presence directly.

```python
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

vector_file_by_id = {
    m["id"]: m
    for m in vector_representation_data["microtopics"]
}

for microtopic_id in {
    "MIC-VECTOR-VS-SCALAR",
    "MIC-SIGNED-COMPONENT",
    "MIC-GRAPHICAL-SUBTRACTION",
    "MIC-FRAME-QUALIFICATION-BOUNDARY",
}:
    assert "elicitation" not in vector_file_by_id[microtopic_id]
```

This falsifier would fail if file location were again mistaken for semantic ownership or if an absent `elicitation` key were again reported as explicit `null`.

---

## 10. Phase A Result

The corrected Physics topology is:

```text
VECTOR FOUNDATION
  BUCKET-VECTOR-REPRESENTATION
  3 instructional microtopics
  -> Core1B source state ABSENT; authoring required

RELATIVE MOTION INSTRUCTIONAL SLICE
  BUCKET-RELATIVE-MOTION
  3 instructional microtopics
  -> Core1B already authored

RELATIVE MOTION RESEARCH BOUNDARY
  BUCKET-RELATIVE-MOTION
  1 research-boundary microtopic
  -> Core1B decision deferred to a separate pedagogical contract
```

Total authored narrow Physics microtopics: **7 = 3 vector-foundation + 3 Relative Motion instructional + 1 Relative Motion research-boundary**. The 12 authority-`NONE` discovery packets remain quarantined.
