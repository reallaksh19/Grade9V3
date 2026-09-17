# Pedagogical Schema Matrix: Pilot 1 — Relative Motion in a Plane (Physics Subtopic 1)

**Repository:** `reallaksh19/Grade9V3`  
**Working Source of Truth:** Head of Pull Request #1 (`p0-foundations`, commit `916169a`)  
**Scope:** Pilot 1 — `BUCKET-RELATIVE-MOTION` (*Relative velocity in a plane*)  
**Architectural Mode:** Strict Source Extraction & Multi-Authority Divergence Accounting (Values populated if and only if backed by repository evidence; all gaps marked `*_AUTHOR_REQUIRED`; cross-layer authority divergences made explicit)

---

## 1. Physics Source and Authority Inventory

Every Physics asset present in PR #1 is inventoried and classified according to repository authority boundaries:

| Source File / Directory | Authority Classification | Supported Microtopics / Assets | Missing Fields / Major Gaps |
| :--- | :--- | :--- | :--- |
| **`Physics/adapter/CoreContracts.json`** | **Governed / Authoritative** | Subject adapter specification: 6 learner products, semantic equation fields, 5 validators (`SPEED_FROM_COMPONENTS`, `CONSTANT_ACCELERATION_*`, `APEX_STATE`), 3 implemented representations (`VECTOR`, `VECTOR_SUBTRACTION`, `GRAPH`), curriculum failure-closed rules. | Does not define teaching content or microtopics. `FREE_BODY_DIAGRAM`, `RAY_DIAGRAM`, `CIRCUIT_SCHEMATIC` are `PROPOSED` only. |
| **`Physics/gates/curriculum-bindings.v1.json`** | **Governed / Authoritative** | Exact curriculum scope authority. Declares `bindings: []` deliberately; all Grade 9 2D vector/relative motion gates fail closed as `OWNER_EXTENSION`. | No binding exists for CBSE Grade 9 2D relative motion (`CURRICULUM_BINDING_GAP`). Authority status remains `HELD_INSUFFICIENT_AUTHORITY` / `OWNER_EXTENSION`. |
| **`Physics/gates/motion-vectors.v1.json`** | **Governed / Authoritative** | 6 engineering gates: `PHY-VEC-SCALAR-VECTOR`, `PHY-VEC-AXIS-CONVENTION`, `PHY-VEC-SUBTRACTION`, `PHY-REL-POSITION`, `PHY-REL-VELOCITY`, `PHY-REL-OBSERVER-REVERSAL`. Defines canonical concepts, relations, symbols, validity conditions, reasoning sequences, misconceptions, representations, and difficulty. | Mature at `ENGINEERING` level; author-created, explicit notice: *"No independent scientific or pedagogical review has occurred."* |
| **`Physics/library/relative-motion.v1.json`** | **Library Candidate** (`status: CANDIDATE`) | 1 bucket (`BUCKET-RELATIVE-MOTION`), 3 narrow microtopics (`MIC-SAME-TIME`, `MIC-COMMON-INTERVAL`, `MIC-GEOMETRIC-CHECK`), 2 relations (`REL-RELATIVE-POSITION`, `REL-RELATIVE-VELOCITY`), 1 representation (`REP-REL-VECTOR`), 9 data atoms, full Core1A teaching paths, and full Core1B elicitations. | `bucket.conventions[]` absent (`CONVENTION_GAP`); `representation_refs: []` in `MIC-SAME-TIME` despite gate ownership (`GATE_REPRESENTATION_UNBOUND`); exit coordinates in `MIC-SAME-TIME` held under `ISS-REL-EXIT-DATA` (`DATA_COORDINATE_GAP`). |
| **`Physics/library/vector-representation.v1.json`** | **Library Candidate** (`status: CANDIDATE`) | 1 bucket (`BUCKET-VECTOR-REPRESENTATION`), 4 narrow microtopics (`MIC-VECTOR-VS-SCALAR`, `MIC-SIGNED-COMPONENT`, `MIC-GRAPHICAL-SUBTRACTION`, `MIC-FRAME-QUALIFICATION-BOUNDARY`), 1 relation (`REL-VECTOR-SUBTRACTION`), 2 representations (`REP-VECTOR-COMPONENT`, `REP-VECTOR-SUBTRACTION-CONSTRUCTION`), 9 data atoms. | `elicitation` is completely `null` across all 4 microtopics (`CORE1B_COVERAGE_GAP`); `bucket.conventions[]` absent (`CONVENTION_GAP`). |
| **`Physics/content/relative-motion-g9/`** | **Published Frozen Evidence** | Executable baseline (`baseline.json`), compilation plan (`plan.json`), source atoms (`source.json`), and compiled publication artifacts (`CORE1A.html`, `CORE1B.html`, `CORE2A.html`, `CORE2B.html`, `evidence.json`, `manifest.json` with digest `e27cbd27...`). | `CORE1.html` not generated (was not in `selected_cores` of baseline); questions carry authored provenance rather than official exam citation. |
| **`Physics/candidates/*.v1.json`** *(12 files)* | **Candidate Discovery Packets** (`packet_authority: NONE`) | 12 broad imported SIL candidate packets (e.g., `PHY-KIN-1D-MOTION`, `PHY-VEC-ADD-SUB`, `PHY-NLM-FIRST-LAW`, etc.). | Zero relations, zero representations, zero data, zero questions, zero capabilities. 204 named gaps recorded in companion `*.gaps.json` files. |

---

## 2. Census of Repository Physics Material (PR #1 Total)

To maintain strict semantic discipline and prevent unpromoted discovery packets from being treated as semantic objects, the PR #1 inventory is separated into **Supported Narrow Microtopics** and **Candidate Discovery Packets**.

### 2.1 Supported Narrow Microtopics (7 Microtopics across 2 Library Candidate Buckets)

These 7 narrow microtopics represent the total set of conceptual units in PR #1 that have authored definitions, teaching steps, and relations in candidate libraries:

| # | Microtopic ID | Library File | Bucket ID | Title | Library Representation | Engineering Gate Representation | Representation Alignment Status | Elicitation Status |
| :- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 1 | **`MIC-SAME-TIME`** | `relative-motion.v1.json` | `BUCKET-RELATIVE-MOTION` | Position measured from the other object | `[]` | `REP-REL-POSITION` (in `PHY-REL-POSITION`) | **`GATE_REPRESENTATION_UNBOUND`** | Complete (`predict`, `attempt`, `reconstruct`, `boundary_test`) |
| 2 | **`MIC-COMMON-INTERVAL`** | `relative-motion.v1.json` | `BUCKET-RELATIVE-MOTION` | From relative position to relative velocity | `["REP-REL-VECTOR"]` (`VECTOR_SUBTRACTION`) | `REP-RELV-RESULTANT` (`VECTOR`, in `PHY-REL-VELOCITY`) | **`CROSS_LAYER_REPRESENTATION_DIVERGENCE`** | Complete (`predict`, `attempt`, `reconstruct`, `boundary_test`) |
| 3 | **`MIC-GEOMETRIC-CHECK`** | `relative-motion.v1.json` | `BUCKET-RELATIVE-MOTION` | Check direction, magnitude and observer reversal | `["REP-REL-VECTOR"]` (`VECTOR_SUBTRACTION`) | `REP-REV-PAIR` (`VECTOR`, in `PHY-REL-OBSERVER-REVERSAL`) | **`CROSS_LAYER_REPRESENTATION_DIVERGENCE`** | Complete (`predict`, `attempt`, `reconstruct`, `boundary_test`) |
| 4 | **`MIC-VECTOR-VS-SCALAR`** | `vector-representation.v1.json` | `BUCKET-VECTOR-REPRESENTATION` | Magnitude, vector and signed component | `["REP-VECTOR-COMPONENT"]` | `REP-VEC-SINGLE` (in `PHY-VEC-SCALAR-VECTOR`) | **`CROSS_LAYER_REPRESENTATION_DIVERGENCE`** | `null` (`CORE1B_COVERAGE_GAP`) |
| 5 | **`MIC-SIGNED-COMPONENT`** | `vector-representation.v1.json` | `BUCKET-VECTOR-REPRESENTATION` | Choosing axes and keeping components signed | `["REP-VECTOR-COMPONENT"]` | `REP-AXIS-CONVENTION` (in `PHY-VEC-AXIS-CONVENTION`) | **`CROSS_LAYER_REPRESENTATION_DIVERGENCE`** | `null` (`CORE1B_COVERAGE_GAP`) |
| 6 | **`MIC-GRAPHICAL-SUBTRACTION`** | `vector-representation.v1.json` | `BUCKET-VECTOR-REPRESENTATION` | Subtraction as addition of the reversed vector | `["REP-VECTOR-SUBTRACTION-CONSTRUCTION"]` | `REP-SUB-CONSTRUCTION` (in `PHY-VEC-SUBTRACTION`) | **`CROSS_LAYER_REPRESENTATION_DIVERGENCE`** | `null` (`CORE1B_COVERAGE_GAP`) |
| 7 | **`MIC-FRAME-QUALIFICATION-BOUNDARY`** | `vector-representation.v1.json` | `BUCKET-VECTOR-REPRESENTATION` | When simple $v_{A/B} = v_A - v_B$ needs frame qualification | `[]` | None | **`REPRESENTATION_BRIDGE_AUTHOR_REQUIRED`** | `null` (`CORE1B_COVERAGE_GAP`) |

### 2.2 Candidate Discovery Packet Census (12 Packets — `packet_authority: NONE`)

These broad imported SIL packets contain coarse topic descriptions and gap manifests. They do **not** define narrow microtopics, relations, representations, data atoms, or question families. They are recorded here for completeness and remain a future-authoring backlog:

| # | Candidate Packet ID | Candidate File | Import Mode | Authority | Relations | Representations | Data Atoms | Questions | Named Gaps |
| :- | :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| 1 | **`PHY-KIN-1D-MOTION`** | `phy-kin-1d-motion.v1.json` | `DIGEST_PINNED_CANDIDATE_SOURCE_ONLY` | `NONE` | 0 | 0 | 0 | 0 | 17 |
| 2 | **`PHY-VEC-ADD-SUB`** | `phy-vec-add-sub.v1.json` | `DIGEST_PINNED_CANDIDATE_SOURCE_ONLY` | `NONE` | 0 | 0 | 0 | 0 | 17 |
| 3 | **`PHY-NLM-FIRST-LAW`** | `phy-nlm-first-law.v1.json` | `DIGEST_PINNED_CANDIDATE_SOURCE_ONLY` | `NONE` | 0 | 0 | 0 | 0 | 17 |
| 4 | **`PHY-WORK-ENERGY-POWER`** | `phy-work-energy-power.v1.json` | `DIGEST_PINNED_CANDIDATE_SOURCE_ONLY` | `NONE` | 0 | 0 | 0 | 0 | 17 |
| 5 | **`PHY-GRAV-UNIVERSAL-LAW`** | `phy-grav-universal-law.v1.json` | `DIGEST_PINNED_CANDIDATE_SOURCE_ONLY` | `NONE` | 0 | 0 | 0 | 0 | 17 |
| 6 | **`PHY-FLUID-BERNOULLI-EQUATION`** | `phy-fluid-bernoulli-equation.v1.json` | `DIGEST_PINNED_CANDIDATE_SOURCE_ONLY` | `NONE` | 0 | 0 | 0 | 0 | 17 |
| 7 | **`PHY-OSC-SHM-WAVES`** | `phy-osc-shm-waves.v1.json` | `DIGEST_PINNED_CANDIDATE_SOURCE_ONLY` | `NONE` | 0 | 0 | 0 | 0 | 17 |
| 8 | **`PHY-THERMO-FIRST-SECOND-LAW`** | `phy-thermo-first-second-law.v1.json` | `DIGEST_PINNED_CANDIDATE_SOURCE_ONLY` | `NONE` | 0 | 0 | 0 | 0 | 17 |
| 9 | **`PHY-ELEC-CURRENT-OHM`** | `phy-elec-current-ohm.v1.json` | `DIGEST_PINNED_CANDIDATE_SOURCE_ONLY` | `NONE` | 0 | 0 | 0 | 0 | 17 |
| 10 | **`PHY-MAG-FIELD-LORENTZ`** | `phy-mag-field-lorentz.v1.json` | `DIGEST_PINNED_CANDIDATE_SOURCE_ONLY` | `NONE` | 0 | 0 | 0 | 0 | 17 |
| 11 | **`PHY-OPTICS-REFLECTION-MIRRORS`** | `phy-optics-reflection-mirrors.v1.json` | `DIGEST_PINNED_CANDIDATE_SOURCE_ONLY` | `NONE` | 0 | 0 | 0 | 0 | 17 |
| 12 | **`PHY-ROT-RIGID-BODY`** | `phy-rot-rigid-body.v1.json` | `DIGEST_PINNED_CANDIDATE_SOURCE_ONLY` | `NONE` | 0 | 0 | 0 | 0 | 17 |

---

## 3. Scope and Execution Plan: Pilot 1 (Relative Motion)

To establish an indisputable, verified oracle pattern before scaling across the rest of Physics, this document executes **Pilot 1: Relative Motion (`BUCKET-RELATIVE-MOTION`)**, covering:
- **`MIC-SAME-TIME`**: *Position measured from the other object*
- **`MIC-COMMON-INTERVAL`**: *From relative position to relative velocity*
- **`MIC-GEOMETRIC-CHECK`**: *Check direction, magnitude and observer reversal*

### Justification for Subtopic 1 First
1. **End-to-End Grounding Across Governance & Publication**: `BUCKET-RELATIVE-MOTION` is the only topic in PR #1 with compiled publication HTML, evidence digests (`evidence.json`, `manifest.json`), active subject validators, and mature engineering gates.
2. **Complete Core1B Source Data**: Unlike `BUCKET-VECTOR-REPRESENTATION` (where `elicitation` is completely `null`), `relative-motion.v1.json` provides fully authored predictions, rubrics, reconstruction routes, and boundary tests for all three microtopics.
3. **Oracle Function**: Establishing the exact extraction and representation-divergence accounting on Subtopic 1 proves the method and provides the governing standard for authoring agents addressing Subtopic 2 and future topics.

---

## 4. Pedagogical Schema Definition & Schema Provenance

```yaml
schema_provenance:
  status: AUTHORING_ANALYSIS_OVERLAY
  repository_fields: source-extracted
  pedagogical_fields:
    - target_aha
    - controlled_experience
    - representation_bridge
  note: >
    These fields organize repository evidence for pedagogical review.
    They are not yet normative package-schema fields.
```

Each microtopic is governed by a 13-field cognitive specification contract organizing evidence from `Physics/adapter/CoreContracts.json`, `Physics/gates/motion-vectors.v1.json`, and `Shared/roles/CORE*.md`.

**Governing Extraction Rule**: If repository evidence supports a field, the source-backed value is recorded. If repository evidence does not support a field, it **must** be marked with its explicit failure-closed gap token (`*_AUTHOR_REQUIRED`). When multiple repository layers declare conflicting or divergent representations, the matrix **must expose both authorities** rather than collapsing them.

1. **`microtopic_id`**: Canonical repository identifier.
2. **`microtopic_name`**: Concise concept title.
3. **`authority`**: Explicit repository source files, gates, validator references, and unbacked elements.
4. **`entry_capability`**: Pre-existing skills and concepts strictly required before this microtopic.
5. **`target_aha`**: The singular conceptual shift or cognitive leap the learner must make.
6. **`controlled_experience`**: The cognitive vary / hold / notice structure (pure conceptual experiment, independent of delivery media: static diagram, text, or animation).
7. **`representation_bridge`**: Dual-authority representation contract capturing pedagogical need, engineering gate declaration, library declaration, and alignment status (`ALIGNED`, `GATE_REPRESENTATION_UNBOUND`, `CROSS_LAYER_REPRESENTATION_DIVERGENCE`, `REPRESENTATION_BRIDGE_AUTHOR_REQUIRED`).
8. **`misconceptions`**: Plausible incorrect mental models, diagnostic triggers, and repair strategies.
9. **`boundary_or_check`**: Extreme conditions, limiting cases, and mathematical/physical checks.
10. **`assessment_evidence`**: Concrete observable student work proving mastery.
11. **`governing_convention`**: Governed coordinate system and sign rules. If missing from `bucket.conventions[]`, marked `CONVENTION_AUTHOR_REQUIRED`.
12. **`scope`**: Permitted versus prohibited physical scenarios.
13. **`intrinsic_depth`**: Intrinsic difficulty badge (`MEDIUM`/`HARD`) and source justification.

---

## 5. Canonical Microtopic Contracts for Pilot 1 (`BUCKET-RELATIVE-MOTION`)

### `MIC-SAME-TIME`: Position measured from the other object

```yaml
microtopic_id: MIC-SAME-TIME
microtopic_name: Position measured from the other object

authority:
  status: LIBRARY_CANDIDATE_WITH_ENGINEERING_GATE
  source_refs:
    - Physics/library/relative-motion.v1.json#microtopics[0]
    - Physics/gates/motion-vectors.v1.json#gates[PHY-REL-POSITION]
    - Shared/roles/CORE1A.md
  unsupported_fields:
    - bucket.conventions[] (absent in library JSON; CONVENTION_AUTHOR_REQUIRED)
    - data.atom_binding_for_exit_task (held under ISS-REL-EXIT-DATA; DATA_COORDINATE_GAP)

entry_capability:
  - Signed coordinate-pair arithmetic is available or bridged (CAP-SIGNED-PAIR).
  - Prerequisites: Vector subtraction (PHY-VEC-SUBTRACTION).

target_aha:
  - Replace two independent positions measured from an arbitrary origin by the single physical displacement from B to A (r_A/B = r_A - r_B).

controlled_experience:
  status: SOURCE_EXTRACTED_FROM_ELICITATION
  cognitive_experiment:
    vary: Observer perspective (measuring A relative to B versus B relative to A).
    hold_constant: Simultaneous object positions r_A and r_B relative to common origin O.
    learner_should_notice: The relative displacement arrow reverses direction (180 deg) and both components invert their signs, while the spatial separation distance (magnitude) remains strictly identical.
  source_basis: relative-motion.v1.json#elicitation.boundary_test ("What has changed, and what has not? (-4,3) m vs (4,-3) m")

representation_bridge:
  pedagogical_need:
    "Connect common-origin positions to displacement from B to A."
  engineering_gate:
    representation_ref: REP-REL-POSITION
    kind: VECTOR
    required_meaning: "Both object positions and the displacement from B to A in declared frame with axis units."
    verification: "Add the drawn relative position to B's position and confirm A's position is recovered."
    relation_bindings: ["REL-RELATIVE-POSITION"]
    concept_bindings: ["CON-REL-SAME-INSTANT", "CON-REL-PATH-IDENTITY"]
  library:
    representation_refs: []
  alignment_status: GATE_REPRESENTATION_UNBOUND
  architectural_note: "The engineering gate PHY-REL-POSITION explicitly defines REP-REL-POSITION, but the candidate library relative-motion.v1.json leaves representation_refs: [] unbound. This is a binding gap across repository layers, not a missing representation."

misconceptions:
  - wrong_idea: "Subtract whichever coordinate appears first in the question."
    counterexample: "With A at (7,2) m and B at (3,5) m, r_A/B is (4,-3) m pointing southeast, but r_B/A is (-4,3) m pointing northwest: order reverses the vector direction."
    diagnostic: "Which displacement carries you from B to A?"
    repair: "Draw origin -> B -> A and reconstruct r_A = r_B + r_A/B before subtracting."

boundary_or_check:
  limiting_case: When r_A = r_B, relative position r_A/B = (0,0) m (coincident objects).
  reversal_test: r_B/A = -(r_A/B); reversing observer negates every component.
  algebraic_check: Add r_A/B back to r_B; recover r_A.

assessment_evidence:
  observable_task: "At one instant A is at (7,2) m and B at (3,5) m. Give A relative to B and explain the signs."
  model_response: "(4,-3) m: 4 m east and 3 m south from B. Negative north component means south."
  check_step: "Add (4,-3) m to B=(3,5) m; recover A=(7,2) m."
  gap: Coordinates (7,2) and (3,5) lack declared data atom IDs (ISS-REL-EXIT-DATA; required before machine-verifying/promoting this numeric exit claim).

governing_convention:
  status: CONVENTION_AUTHOR_REQUIRED
  note: "bucket.conventions[] is absent on BUCKET-RELATIVE-MOTION. While scenes mention local east/north and gate PHY-VEC-AXIS-CONVENTION mentions standard Cartesian +x=east, +y=north, no governed bucket convention is declared."

scope:
  include:
    - Same-instant positions.
    - Parallel, non-rotating Cartesian axes.
    - Classical kinematics.
  exclude:
    - Positions recorded at different instants.
    - Rotating reference frames.
    - Relativistic position transformations.

intrinsic_depth:
  badge: HARD
  basis: "Observer order and common time are easily hidden by a memorized formula." (motion-vectors.v1.json line 286)
```

---

### `MIC-COMMON-INTERVAL`: From relative position to relative velocity

```yaml
microtopic_id: MIC-COMMON-INTERVAL
microtopic_name: From relative position to relative velocity

authority:
  status: LIBRARY_CANDIDATE_WITH_ENGINEERING_GATE
  source_refs:
    - Physics/library/relative-motion.v1.json#microtopics[1]
    - Physics/gates/motion-vectors.v1.json#gates[PHY-REL-VELOCITY]
    - Physics/adapter/CoreContracts.json#validator_catalogue[SPEED_FROM_COMPONENTS]
  unsupported_fields:
    - bucket.conventions[] (absent in library JSON; CONVENTION_AUTHOR_REQUIRED)
    - instantaneous_calculus_form (source restricts scope to constant velocity finite differences)

entry_capability:
  - Can construct same-time relative position (MIC-SAME-TIME).
  - Can interpret displacement over elapsed time interval.

target_aha:
  - Subtract two same-time relative position equations at t1 and t2 before dividing by a single, shared time interval (Delta t) to obtain relative velocity.

controlled_experience:
  status: SOURCE_EXTRACTED_FROM_ELICITATION
  cognitive_experiment:
    experience_1_perpendicular_prediction:
      prompt: "A walks east at 3 m/s and B walks north at 4 m/s. Predict the speed of A as seen by B, and say whether you can get it by subtracting 3 from 4."
      hold_constant: Individual object speeds (|v_A| = 3 m/s East, |v_B| = 4 m/s North).
      vary: Relative orientation of velocity vectors (orthogonal vs collinear).
      learner_should_notice: "5 m/s, and no. The two motions are at right angles, so nothing cancels; subtracting the speeds throws away the directions that decide the answer."
      source_basis: relative-motion.v1.json#elicitation.predict
    experience_2_same_direction_boundary:
      prompt: "A and B both walk east, A at 5 m/s and B at 5 m/s. What is v_A/B, and what does B see?"
      hold_constant: Both velocities identical (5 m/s East).
      vary: Ground motion state vs relative separation change.
      learner_should_notice: "(0,0) m/s. B sees A holding still, at a fixed distance, even though both are moving quickly over the ground."
      source_basis: relative-motion.v1.json#elicitation.boundary_test

representation_bridge:
  pedagogical_need:
    "Depict relative velocity as a resultant vector arising from subtracting common-frame velocities over a shared interval."
  engineering_gate:
    representation_ref: REP-RELV-RESULTANT
    kind: VECTOR
    required_meaning: "Declared frame, resultant labelled as the relative velocity, axis units, common length scale."
    verification: "Confirm the drawn resultant's components equal the component-wise difference, and that a same-interval position change reproduces it."
    relation_bindings: ["REL-RELATIVE-VELOCITY"]
    concept_bindings: ["CON-RELV-COMMON-INTERVAL", "CON-RELV-VECTOR-DIFFERENCE"]
  library:
    representation_refs:
      - REP-REL-VECTOR
    kind: VECTOR_SUBTRACTION
    required_meaning: "Tail-to-head construction of v_A + (-v_B); labelled v_A, v_B, -v_B and resultant v_A/B."
  alignment_status: CROSS_LAYER_REPRESENTATION_DIVERGENCE
  architectural_note: "The engineering gate PHY-REL-VELOCITY specifies REP-RELV-RESULTANT of kind VECTOR (focusing on the relative velocity as a single resultant vector), whereas the candidate library specifies REP-REL-VECTOR of kind VECTOR_SUBTRACTION (focusing on the graphical subtraction construction v_A + (-v_B)). Both authorities are preserved."

misconceptions:
  - wrong_idea: "Subtracting the two speeds always gives relative speed."
    counterexample: "A moving east at 6 m/s and B moving north at 8 m/s have speeds 6 and 8 m/s, yet relative speed is 10 m/s, not 2 m/s."
    diagnostic: "If one object moves east and the other north, do their directions disappear?"
    repair: "Compute signed vector components first, then take the magnitude if requested."

boundary_or_check:
  limiting_case: "When v_A = v_B, relative velocity v_A/B = (0,0) m/s (separation vector remains strictly constant even if ground speed is high)."
  dimensional_check: "[L T^-1], units m/s for each component."
  shared_interval_check: "If observation intervals differ (Delta t_A != Delta t_B), the quotient does not represent the change in simultaneous separation."

assessment_evidence:
  observable_task: "Why must both displacement changes be divided by the same time interval in this derivation?"
  closure: RUBRIC (relative-motion.v1.json#elicitation.attempt.rubric)

governing_convention:
  status: CONVENTION_AUTHOR_REQUIRED
  note: "bucket.conventions[] absent. Shared time parameter t is enforced by gate PHY-REL-VELOCITY."

scope:
  include:
    - Same observation times and one common interval Delta t.
    - Parallel, non-rotating Cartesian axes.
    - Constant velocity kinematics.
  exclude:
    - Non-constant velocity / acceleration dynamics (instantaneous limit withheld).
    - Relativistic velocity addition.

intrinsic_depth:
  badge: HARD
  basis: "The student must connect two same-time position statements to one common interval rather than memorize a subtraction rule." (motion-vectors.v1.json line 348)
```

---

### `MIC-GEOMETRIC-CHECK`: Check direction, magnitude and observer reversal

```yaml
microtopic_id: MIC-GEOMETRIC-CHECK
microtopic_name: Check direction, magnitude and observer reversal

authority:
  status: LIBRARY_CANDIDATE_WITH_ENGINEERING_GATE
  source_refs:
    - Physics/library/relative-motion.v1.json#microtopics[2]
    - Physics/gates/motion-vectors.v1.json#gates[PHY-REL-OBSERVER-REVERSAL]
    - Physics/adapter/CoreContracts.json#representation_kinds[VECTOR_SUBTRACTION]
  unsupported_fields:
    - bucket.conventions[] (absent in library JSON; CONVENTION_AUTHOR_REQUIRED)
    - automated_compass_oracle (CoreContracts has no validator parsing compass strings; AUTOMATED_VERIFICATION_GAP / ORACLE_GAP)

entry_capability:
  - Can subtract velocity components algebraically (MIC-COMMON-INTERVAL).
  - Can perform graphical vector subtraction by reversal and tail-to-head addition (MIC-GRAPHICAL-SUBTRACTION).

target_aha:
  - Reconcile algebraic component subtraction with geometric reversal of the observer vector; recognise that observer reversal negates direction but preserves magnitude identically.

controlled_experience:
  status: SOURCE_EXTRACTED_FROM_ELICITATION
  cognitive_experiment:
    vary: Choice of which object vector is reversed in the geometric construction (-v_B versus -v_A).
    hold_constant: Ground velocities v_A and v_B.
    learner_should_notice: Reversing the observer turns the resultant arrow exactly 180 deg (v_B/A = -v_A/B), but the arrow's length and calculated speed remain invariant.
  source_basis: relative-motion.v1.json#elicitation.reconstruct.route (Step 3: "reverse which arrow you turned around, and redraw") & gate PHY-REL-OBSERVER-REVERSAL

representation_bridge:
  pedagogical_need:
    "Show that swapping the observer reverses the relative vector by 180 degrees while leaving magnitude invariant."
  engineering_gate:
    representation_ref: REP-REV-PAIR
    kind: VECTOR
    required_labels: ["declared frame", "named observer for the drawn vector", "axis units"]
    verification: "Add the two relative vectors and confirm the sum is exactly zero."
    relation_bindings: ["REL-OBSERVER-REVERSAL"]
    concept_bindings: ["CON-REV-ANTISYMMETRY", "CON-REV-MAGNITUDE-INVARIANT"]
  library:
    representation_refs:
      - REP-REL-VECTOR
    kind: VECTOR_SUBTRACTION
    scene_instance: SI-REL-VELOCITY-CONSTRUCTION (scene ID: SCN-REL-COMPUTE)
  alignment_status: CROSS_LAYER_REPRESENTATION_DIVERGENCE
  architectural_note: "The engineering gate PHY-REL-OBSERVER-REVERSAL mandates REP-REV-PAIR of kind VECTOR (requiring both relative vectors with named observers to verify zero sum), whereas the candidate library reuses REP-REL-VECTOR of kind VECTOR_SUBTRACTION. Both authorities are recorded."

misconceptions:
  - wrong_idea: "A correct length is enough for a correct vector answer."
    counterexample: "If v_A/B is (6,-8) m/s pointing southeast, an answer of (6,8) m/s has the same magnitude 10 m/s but points northeast, describing a completely different observation."
    diagnostic: "Would the same arrow reversed describe the same observer statement?"
    repair: "Name the observer, label both components and inspect the direction before taking a magnitude."

boundary_or_check:
  limiting_case: "v_A/B + v_B/A = 0 (sum of mutually observed relative velocities is zero vector)."
  magnitude_invariance: "|v_A/B| = |v_B/A|; squaring components removes negative signs."
  reversal_consistency: "Swapping observer swaps subtraction order, negating every component."
  head_on_boundary: "Two cars approach at 20 m/s each -> relative speed 40 m/s; reversing observer points the other way along the line and leaves 40 m/s unchanged." (elicitation.boundary_test)

assessment_evidence:
  observable_task: "If v_A/B points southeast, what direction does v_B/A point, and what happens to its magnitude?"
  model_response: "Northwest, with the same magnitude. Swapping subtraction order negates every component, which reverses direction by 180 deg while leaving magnitude unchanged."
  check_step: "Adding v_A/B and v_B/A gives (0,0) m/s."
  closure_status: COMPLETE (human/model closure fully defined via prompt, defensible answer, rubric, and boundary test)
  automated_verification: AUTOMATED_VERIFICATION_GAP (no automated compass validator in adapter)

governing_convention:
  status: CONVENTION_AUTHOR_REQUIRED
  note: "bucket.conventions[] absent. Scene SI-REL-VELOCITY-CONSTRUCTION specifies 'One common east/north frame, east positive along x, north positive along y', but bucket-level declaration is missing."

scope:
  include:
    - Geometric vector reversal and tail-to-head addition.
    - Component-level antisymmetry checks.
    - Magnitude invariance under observer swap.
  exclude:
    - Rotating frames.
    - Accelerating frames and fictitious forces.

intrinsic_depth:
  badge: HARD
  basis: "Correct arithmetic can conceal an incorrect vector construction or frame interpretation." (motion-vectors.v1.json line 398)
```

---

## 6. Multi-Core Pedagogical Projections (Pilot 1: Relative Motion)

### 6.1 CORE1 Matrix (Compact Orientation Map)

| Microtopic | Named Objects / Quantities | Essential Convention | Governing Relationship | Meaning in Words | Validity Conditions | Compact Anchor | Hard Transition Pointer | Scope / Exclusion | Representation Alignment | Authority / Gaps |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`MIC-SAME-TIME`** | $\vec{r}_A$: Position of A ($m$)<br>$\vec{r}_B$: Position of B ($m$)<br>$\vec{r}_{A/B}$: Displacement of A from B ($m$) | **`CONVENTION_AUTHOR_REQUIRED`**<br>*(Scene uses local East/North; bucket.conventions[] absent)* | $\vec{r}_{A/B} = \vec{r}_A - \vec{r}_B$ | The displacement from B to A is what remains after subtracting the position of B. | Both positions taken at the exact same instant; non-rotating axes; classical frame. | With A at $(7,2)\text{ m}$, B at $(3,5)\text{ m}$: $\vec{r}_{A/B} = (4,-3)\text{ m}$. | Transition from origin-based coordinates to observer-based displacement. | **In:** 2D Cartesian plane, same instant.<br>**Out:** Different instants, rotating axes. | Gate: `REP-REL-POSITION`<br>Library: `[]`<br>(**`GATE_REPRESENTATION_UNBOUND`**) | `LIBRARY_CANDIDATE`. Grounded in gate `PHY-REL-POSITION`. *Gaps:* `CONVENTION_GAP`, `GATE_REPRESENTATION_UNBOUND`. |
| **`MIC-COMMON-INTERVAL`** | $\vec{v}_A$: Velocity of A ($\text{m/s}$)<br>$\vec{v}_B$: Velocity of B ($\text{m/s}$)<br>$\vec{v}_{A/B}$: Velocity of A relative to B ($\text{m/s}$)<br>$\Delta t$: Elapsed time ($s$) | **`CONVENTION_AUTHOR_REQUIRED`**<br>*(Shared time $t$ enforced by gate; bucket convention absent)* | $\vec{v}_{A/B} = \vec{v}_A - \vec{v}_B$ | For constant velocities, relative position changes at the vector difference of common-frame velocities. | Same observation times; one common interval; parallel non-rotating axes; classical speeds. | $v_A = (6,0)\text{ m/s}$, $v_B = (0,8)\text{ m/s}$ $\implies v_{A/B} = (6,-8)\text{ m/s}$, speed $= 10\text{ m/s}$. | Justifying why division by a *shared* time interval is mandatory rather than subtracting speeds. | **In:** Constant velocities, finite intervals.<br>**Out:** Relativistic speeds, instantaneous calculus limits. | Gate: `REP-RELV-RESULTANT`<br>Library: `REP-REL-VECTOR`<br>(**`CROSS_LAYER_REPRESENTATION_DIVERGENCE`**) | `LIBRARY_CANDIDATE`. Grounded in gate `PHY-REL-VELOCITY`. Validator `SPEED_FROM_COMPONENTS`. *Gap:* `CONVENTION_GAP`. |
| **`MIC-GEOMETRIC-CHECK`** | $\vec{v}_{A/B}$: Velocity of A rel B ($\text{m/s}$)<br>$\vec{v}_{B/A}$: Velocity of B rel A ($\text{m/s}$) | **`CONVENTION_AUTHOR_REQUIRED`**<br>*(Tail-to-head addition & reversal defined in gate; bucket convention absent)* | $\vec{v}_{B/A} = -(\vec{v}_{A/B})$ | Swapping which object is the observer negates every component of the relative velocity vector. | Both evaluated in same frame at same instant; classical velocities. | $v_{A/B} = (6,-8)\text{ m/s}$ (SE) $\implies v_{B/A} = (-6,8)\text{ m/s}$ (NW), both speed $10\text{ m/s}$. | Separating vector direction (negated) from scalar magnitude (invariant). | **In:** Graphical reversal and component antisymmetry.<br>**Out:** Accelerating observers, Coriolis effects. | Gate: `REP-REV-PAIR`<br>Library: `REP-REL-VECTOR`<br>(**`CROSS_LAYER_REPRESENTATION_DIVERGENCE`**) | `LIBRARY_CANDIDATE`. Grounded in gate `PHY-REL-OBSERVER-REVERSAL`. *Gaps:* `CONVENTION_GAP`, `AUTOMATED_VERIFICATION_GAP`. |

---

### 6.2 CORE1A Matrix (Declarative Detailed Teaching)

| Microtopic | Entry Capability | Target Inferential Jump | Controlled Experience (Vary / Hold / Notice) | Completed Teaching Construction (Steps & Roles) | Why-Valid Obligations | Representation Bridge (Gate vs Library) | Misconception & Diagnostic | Repair | Independent Check | Exit Evidence | Authority / Gaps |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`MIC-SAME-TIME`** | `CAP-SIGNED-PAIR`: Signed coordinate-pair arithmetic. | Replace two origin positions by the displacement from B to A. | **Vary:** Observer choice (A rel B vs B rel A).<br>**Hold:** Positions $\vec{r}_A, \vec{r}_B$.<br>**Notice:** Arrow flips $180^\circ$, signs invert, length invariant. *(boundary_test)* | **Step 1 (TRANSFORM):** Follow path $O \to B \to A$ yielding $\vec{r}_A = \vec{r}_B + \vec{r}_{A/B}$.<br>**Step 2 (TRANSFORM):** Subtract $\vec{r}_B$ from both sides: $\vec{r}_{A/B} = \vec{r}_A - \vec{r}_B$. | Displacements add along consecutive paths; subtracting identical vector preserves equality. | Gate requires `REP-REL-POSITION` (`VECTOR`); Library has `representation_refs: []`.<br>(**`GATE_REPRESENTATION_UNBOUND`**) | **Wrong:** Subtract whichever coordinate is written first.<br>**Diag:** "Which displacement carries you from B to A?" | Draw path $O \to B \to A$, write $\vec{r}_A = \vec{r}_B + \vec{r}_{A/B}$, then isolate $\vec{r}_{A/B}$. | Add $\vec{r}_{A/B}$ to $\vec{r}_B$ to recover $\vec{r}_A$. | At one instant A is at $(7,2)$ and B at $(3,5)$. Give A rel B and explain signs $\to (4,-3)\text{ m}$. | Library candidate; gate `PHY-REL-POSITION`. *Gaps:* `GATE_REPRESENTATION_UNBOUND`, `CONVENTION_GAP`, `DATA_COORDINATE_GAP` (`ISS-REL-EXIT-DATA`). |
| **`MIC-COMMON-INTERVAL`** | `MIC-SAME-TIME`: Can construct relative position. | Subtract two relative-position equations before dividing by a common time interval. | **Exp 1 (predict):** Speeds $3\text{ E}, 4\text{ N}\text{ m/s}$; scalar diff $4 - 3 \ne 1\text{ m/s}$ vs vector diff $v_{A/B}=(3,-4)$, $|v|=5\text{ m/s}$.<br>**Exp 2 (boundary):** Speeds $5\text{ E}, 5\text{ E}\text{ m/s}$; $v_{A/B}=(0,0)\text{ m/s}$. | **Step 1 (DECLARE):** Write relative position at $t_1$ and $t_2$.<br>**Step 2 (TRANSFORM):** Group displacement changes: $\Delta \vec{r}_{A/B} = \Delta \vec{r}_A - \Delta \vec{r}_B$.<br>**Step 3 (TRANSFORM):** Divide each term by common $\Delta t$.<br>**Step 4 (DECLARE):** Equate average to constant velocity: $\vec{v}_{A/B} = \vec{v}_A - \vec{v}_B$. | Same relation applies at both instants; subtraction distributes; quotient over non-zero interval yields average velocity. | Gate specifies `REP-RELV-RESULTANT` (`VECTOR`); Library specifies `REP-REL-VECTOR` (`VECTOR_SUBTRACTION`).<br>(**`CROSS_LAYER_REPRESENTATION_DIVERGENCE`**) | **Wrong:** Subtracting speeds gives relative speed.<br>**Diag:** "If one moves east and other north, do directions disappear?" | Compute signed vector components first, then take magnitude if requested. | For equal velocity vectors ($\vec{v}_A = \vec{v}_B$), separation must remain constant. | Explain why both displacement changes must be divided by the same time interval in the derivation. | Library candidate; gate `PHY-REL-VELOCITY`. Validated by `SPEED_FROM_COMPONENTS`. *Gap:* `CONVENTION_GAP`. |
| **`MIC-GEOMETRIC-CHECK`** | `MIC-COMMON-INTERVAL` & `MIC-GRAPHICAL-SUBTRACTION`. | Reconcile algebraic subtraction with reversal of observer vector in geometric construction. | **Vary:** Which observer arrow is reversed ($-\vec{v}_B$ vs $-\vec{v}_A$).<br>**Hold:** Ground velocities $\vec{v}_A, \vec{v}_B$.<br>**Notice:** Resultant reverses direction by $180^\circ$ but magnitude is unchanged. *(reconstruct)* | **Step 1 (TRANSFORM):** Reverse $\vec{v}_B \to -\vec{v}_B$.<br>**Step 2 (TRANSFORM):** Add $\vec{v}_A$ and $-\vec{v}_B$ tail-to-head.<br>**Step 3 (VERIFY):** Compare components and reverse observer order: $\vec{v}_{B/A} = -(\vec{v}_{A/B})$. | Subtraction is addition of opposite vector; free vectors translate without rotation; opposite vectors have equal lengths. | Gate mandates `REP-REV-PAIR` (`VECTOR`); Library reuses `REP-REL-VECTOR` (`VECTOR_SUBTRACTION`, `SI-REL-VELOCITY-CONSTRUCTION`).<br>(**`CROSS_LAYER_REPRESENTATION_DIVERGENCE`**) | **Wrong:** Correct length is enough for vector answer.<br>**Diag:** "Would the same arrow reversed describe same observation?" | Name observer, label both components and inspect direction before taking magnitude. | Vector sum $\vec{v}_{A/B} + \vec{v}_{B/A} = \vec{0}$. | If $\vec{v}_{A/B}$ points SE, what direction does $\vec{v}_{B/A}$ point and what happens to its magnitude? | Library candidate; gate `PHY-REL-OBSERVER-REVERSAL`. *Gaps:* `CONVENTION_GAP`, `AUTOMATED_VERIFICATION_GAP`. |

---

### 6.3 CORE1B Matrix (Conceptual Reconstruction & Self-Tutor)

| Microtopic | Target Understanding | 1. Predict (Prompt & Defensible Answer) | 2. Attempt (Produces & Rubric Closure) | 3. Reconstruct Route (Guided Prompts) | 4. Diagnose (Plausible Wrong Answer) | 5. Repair (Action Following Error) | 6. Boundary Test (Prompt & Confirms) | Core1A Correspondence | Authority / Gaps |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`MIC-SAME-TIME`** | Displacement from B to A is independent of origin and reverses when observer swaps. | **Prompt:** A is at $(7,2)\text{ m}$ and B at $(3,5)\text{ m}$, both measured from the same origin. Before subtracting anything, predict which way you would walk to get from B to A — east or west, north or south?<br>**Answer:** East and south. A is further east than B and lower on the north axis, so the walk is east and south whatever the arithmetic turns out to be. | **Produces:** Sketch of origin, B, and A with arrow from B to A, and the two signs expected for components.<br>**Closure (Rubric):** Tail at B; signs read off sketch before subtraction. Accepted/Rejected criteria declared. | **Route:**<br>1. Trace finger $O \to B \to A$. Which two moves does question ask about?<br>2. Write trip as one journey: $\vec{r}_A = \vec{r}_B + \vec{r}_{A/B}$.<br>3. Isolate $\vec{r}_{A/B}$ by subtracting $\vec{r}_B$ from both sides.<br>4. Reconcile arithmetic $(4,-3)\text{ m}$ with initial directional prediction. | **Wrong:** Subtract whichever coordinate appears first in prompt, ignoring observer tail. | Redraw path from observer tail to target head; reconstruct vector sum before subtracting. | **Prompt:** Now give B relative to A for same positions. What changed and what did not?<br>**Answer:** $(-4,3)\text{ m}$; components negated, magnitude unchanged.<br>**Confirms:** Order is carried by vector, not first written number. | Matches Core1A derivation steps; establishes qualitative check before calculation. | Library candidate; fully populated in `relative-motion.v1.json#elicitation`. *Gaps:* `GATE_REPRESENTATION_UNBOUND`, `DATA_COORDINATE_GAP`. |
| **`MIC-COMMON-INTERVAL`** | Relative velocity requires subtracting components over shared interval, not subtracting speeds. | **Prompt:** A moves east at $3\text{ m/s}$, B north at $4\text{ m/s}$. Predict relative speed and say if $4 - 3$ gives it.<br>**Answer:** $5\text{ m/s}$, and no. Motions are at right angles; subtracting speeds throws away direction. | **Produces:** Relative velocity as signed components, then magnitude, explicitly distinguishing velocity from speed.<br>**Closure (Rubric):** Axis-by-axis subtraction before magnitude; labels velocity vs speed. | **Route:**<br>1. Write relative position at start and end of 1 second.<br>2. Subtract the two positions.<br>3. Divide by shared interval $\Delta t = 1\text{ s}$.<br>4. Re-evaluate components vs initial prediction. | **Wrong:** $4 - 3 = 1\text{ m/s}$ (scalar speed subtraction fallacy). | Recompute signed components in declared frame, then take vector magnitude $\sqrt{v_x^2 + v_y^2}$. | **Prompt:** A and B both walk east at $5\text{ m/s}$. What is $\vec{v}_{A/B}$ and what does B see?<br>**Answer:** $(0,0)\text{ m/s}$. B sees A stationary at fixed distance.<br>**Confirms:** Relative velocity is about separation changing, not ground motion. | Matches Core1A derivation steps; bridges to vector subtraction representation. | Library candidate; fully populated in `relative-motion.v1.json#elicitation`. *Divergence:* `CROSS_LAYER_REPRESENTATION_DIVERGENCE`. |
| **`MIC-GEOMETRIC-CHECK`** | Reversing observer reverses vector direction by $180^\circ$ while keeping magnitude invariant. | **Prompt:** $\vec{v}_{A/B}$ is SE at $5\text{ m/s}$. Predict $\vec{v}_{B/A}$ direction and size without calculation.<br>**Answer:** Northwest at $5\text{ m/s}$. Swapping observer reverses arrow, leaving length alone. | **Produces:** Both arrows drawn on one sketch, with observer named beside each and lengths compared.<br>**Closure (Rubric):** Observer named on each arrow; lengths stated equal without recalculating. | **Route:**<br>1. Draw $\vec{v}_A$ and $\vec{v}_B$ from common point.<br>2. Reverse $\vec{v}_B$ and add tail-to-head.<br>3. Reverse observer: redraw by reversing $\vec{v}_A$.<br>4. Verify resultant arrows are opposite and equal length. | **Wrong:** Offering scalar magnitude alone ($5\text{ m/s}$) as the complete relative velocity answer. | State the observer explicitly, assign signed components, and verify heading on coordinate grid. | **Prompt:** Two cars approach head-on at $20\text{ m/s}$ each. What is magnitude of relative velocity, and does reversing observer change it?<br>**Answer:** $40\text{ m/s}$; reversing observer points opposite way, magnitude invariant.<br>**Confirms:** Reversal leaves magnitude alone. | Matches Core1A graphical check; enforces observer labeling. | Library candidate; fully populated in `relative-motion.v1.json#elicitation`. *Gap:* `AUTOMATED_VERIFICATION_GAP` (compass oracle). |

---

## 7. Cross-Core Correspondence Matrix

| Microtopic | Core1 Role | Core1A Role | Core1B Role | A/B Differentiated? | Coverage Complete? | Authority Sufficient? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`MIC-SAME-TIME`** | Compact map: naming $\vec{r}_A, \vec{r}_B, \vec{r}_{A/B}$, governing equation, same-time validity condition, anchor values. | Declarative instruction: reveals completed $O \to B \to A$ path proof, why-valid justifications, and diagnostic. | Conceptual self-tutor: learner predicts walk direction first (East & South), sketches arrow, traces finger route, then calculates and tests reversal. | **PASS** | **PASS** | **CANDIDATE** (Grounded in engineering gate `PHY-REL-POSITION`; curriculum binding held as `OWNER_EXTENSION`). |
| **`MIC-COMMON-INTERVAL`** | Compact map: naming velocities, shared interval relation $\vec{v}_{A/B} = \vec{v}_A - \vec{v}_B$, constant velocity condition. | Declarative instruction: reveals 4-step derivation grouping displacement changes over shared $\Delta t$. | Conceptual self-tutor: learner predicts right-angle outcome first, calculates components, boundary tests zero-velocity limit. | **PASS** | **PASS** | **CANDIDATE** (Grounded in engineering gate `PHY-REL-VELOCITY`; verified by `SPEED_FROM_COMPONENTS`). |
| **`MIC-GEOMETRIC-CHECK`** | Compact map: antisymmetry relation $\vec{v}_{B/A} = -(\vec{v}_{A/B})$, graphical reversal convention. | Declarative instruction: reveals vector reversal and tail-to-head geometric construction (`SCN-REL-COMPUTE`). | Conceptual self-tutor: learner predicts opposite vector, draws both arrows with named observers, checks cancellation. | **PASS** | **PASS** | **CANDIDATE** (Grounded in engineering gate `PHY-REL-OBSERVER-REVERSAL`; scene instance verified in publication). |

---

## 8. Failure-Closed Gap Report & Architectural Divergences

The following gaps and divergences are strictly recorded to ensure architectural transparency before authoring agents are dispatched:

1. **`CURRICULUM_BINDING_GAP` (Curriculum Scope Authority)**:
   - `Physics/gates/curriculum-bindings.v1.json` declares `bindings: []`. Sources exist in the repository (`SRC-CBSE-ADV`, `SRC-CBSE-STD`), but no official binding is authorized.
   - *Status*: Content fails closed as `OWNER_EXTENSION` (`HELD_INSUFFICIENT_AUTHORITY`).
2. **`CONVENTION_GAP` (Missing Bucket Conventions)**:
   - `Shared/roles/CORE1.md` mandates `bucket.conventions[]`, which is absent in `BUCKET-RELATIVE-MOTION` and `BUCKET-VECTOR-REPRESENTATION`.
   - *Resolution*: Marked `CONVENTION_AUTHOR_REQUIRED`. An authoring agent must formally declare coordinate frame conventions on the bucket.
3. **`GATE_REPRESENTATION_UNBOUND` (Layer Disconnect in Position)**:
   - Engineering gate `PHY-REL-POSITION` explicitly declares and specifies `REP-REL-POSITION` (kind: `VECTOR`), with verification method and concept bindings.
   - Candidate library `relative-motion.v1.json#microtopics[0]` declares `representation_refs: []`.
   - *Resolution*: This is a binding gap across layers, not a missing representation. The downstream authoring task is to formally bind `REP-REL-POSITION` to `MIC-SAME-TIME`.
4. **`CROSS_LAYER_REPRESENTATION_DIVERGENCE` (Divergent Representation Authorities)**:
   - In `MIC-COMMON-INTERVAL`: Gate `PHY-REL-VELOCITY` specifies `REP-RELV-RESULTANT` (kind: `VECTOR`), whereas candidate library specifies `REP-REL-VECTOR` (kind: `VECTOR_SUBTRACTION`).
   - In `MIC-GEOMETRIC-CHECK`: Gate `PHY-REL-OBSERVER-REVERSAL` specifies `REP-REV-PAIR` (kind: `VECTOR`, required label: named observer for drawn vector), whereas candidate library reuses `REP-REL-VECTOR` (kind: `VECTOR_SUBTRACTION`).
   - *Resolution*: Both authorities are explicitly exposed in the matrix. Architectural resolution is required to decide whether downstream publication renders single resultant vectors, full subtraction constructions, or paired observer vectors.
5. **`DATA_COORDINATE_GAP` (Ungrounded Exit Task Coordinates)**:
   - In `MIC-SAME-TIME`, coordinates $(7,2)\text{ m}$ and $(3,5)\text{ m}$ live in exit task text rather than as declared data atoms with unit and dimension (`ISS-REL-EXIT-DATA`).
   - *Resolution*: Data atoms must be formally added to `relative-motion.v1.json#data[]` before machine-verifying or promoting this numeric exit claim.
6. **`CORE1B_COVERAGE_GAP` (Missing Elicitation in Subtopic 2)**:
   - All 4 microtopics in `BUCKET-VECTOR-REPRESENTATION` have `elicitation: null`. Core1B cannot be compiled for Subtopic 2 until full predict/attempt/reconstruct/diagnose/repair/boundary routes are authored.
7. **`AUTOMATED_VERIFICATION_GAP` / `ORACLE_GAP` (Subject Validator Limitation)**:
   - In `MIC-GEOMETRIC-CHECK`, Core1B conceptual closure is complete (defensible answer, rubric, and boundary test fully defined).
   - However, the exit task response requires a compass heading ("Northwest"); no automated subject validator in `CoreContracts.json` evaluates compass strings, requiring `CHECKED_BY_AUTHOR`.
