# Pedagogical Schema Matrix: Subtopic 2 — Vector Representation and Subtraction (`BUCKET-VECTOR-REPRESENTATION`)

**Repository:** `reallaksh19/Grade9V3`  
**Working Source of Truth:** Head of Pull Request #1 (`p0-foundations`, commit `916169a`)  
**Scope:** `BUCKET-VECTOR-REPRESENTATION` (Vector representation and subtraction)  
**Execution Phase:** **Phase A: Strict Extraction Only**  
**Architectural Mode:** Strict Source Extraction & Multi-Authority Divergence Accounting (Values populated if and only if backed by repository evidence; all unbacked fields marked `*_AUTHOR_REQUIRED`; cross-layer authority divergences made explicit; zero new pedagogical authoring)

---

## 1. Scope and Authority Inventory

This extraction matrix governs `BUCKET-VECTOR-REPRESENTATION`, the prerequisite foundation bucket authored alongside `BUCKET-RELATIVE-MOTION` in PR #1. The extraction method, representation-bridge architecture, and gap taxonomy are derived directly from the approved Pilot 1 oracle (`docs/PEDAGOGICAL-SCHEMA-MATRIX-PHYSICS-SUBTOPIC-1.md` in PR #2).

Every source asset relevant to this bucket is classified according to repository authority boundaries without promoting status through prose:

| Source File / Asset | Authority Classification | Scope / Role in Subtopic 2 | Status & Unresolved Gaps |
| :--- | :--- | :--- | :--- |
| **`Physics/gates/curriculum-bindings.v1.json`** | **Governed / Authoritative** | Curriculum scope authority. Declares `bindings: []`. | Grade 9 2D vector representation gates fail closed as `OWNER_EXTENSION` (`CURRICULUM_BINDING_GAP`). Authority: `HELD_INSUFFICIENT_AUTHORITY`. |
| **`Physics/gates/motion-vectors.v1.json`** | **Governed / Authoritative** | 3 relevant engineering gates: `PHY-VEC-SCALAR-VECTOR`, `PHY-VEC-AXIS-CONVENTION`, `PHY-VEC-SUBTRACTION`. Defines canonical concepts, relations, symbols, validity conditions, reasoning sequences, misconceptions, and representations (`REP-VEC-SINGLE`, `REP-AXIS-CONVENTION`, `REP-SUB-CONSTRUCTION`). | Mature at `ENGINEERING` level. Author-created: *"No independent scientific or pedagogical review has occurred."* |
| **`Physics/adapter/CoreContracts.json`** | **Governed / Authoritative** | Subject adapter specification: validators (`SPEED_FROM_COMPONENTS`), representation kinds (`VECTOR`, `VECTOR_SUBTRACTION`). | Does not define teaching content. Implemented representation kinds are authoritative. |
| **`Physics/library/vector-representation.v1.json`** | **Library Candidate** (`status: CANDIDATE`) | 1 bucket (`BUCKET-VECTOR-REPRESENTATION`), 4 narrow microtopics (`MIC-VECTOR-VS-SCALAR`, `MIC-SIGNED-COMPONENT`, `MIC-GRAPHICAL-SUBTRACTION`, `MIC-FRAME-QUALIFICATION-BOUNDARY`), 1 relation (`REL-VECTOR-SUBTRACTION`), 2 representations (`REP-VECTOR-COMPONENT`, `REP-VECTOR-SUBTRACTION-CONSTRUCTION`), 9 data atoms, 4 capabilities. | `bucket.conventions[]` absent (`CONVENTION_GAP`); `elicitation: null` across all 4 microtopics (`CORE1B_COVERAGE_GAP`); `ISS-VEC-EXIT-DATA` held in `MIC-SIGNED-COMPONENT` (`DATA_GAP`). |
| **`CAP-SIGNED-PAIR-BRIDGE`** | **External-Provider Capability Candidate** | Prerequisite capability: Read signed coordinates and subtract coordinate values preserving sign. | `external_provider: Mathematics`, `acceptance_status: PROVIDER_REVIEW_REQUIRED`. Physics authored draft; not Mathematics-reviewed (`EXTERNAL_PROVIDER_REVIEW_REQUIRED`). |
| **`CAP-RIGHT-TRIANGLE-BRIDGE`** | **External-Provider Capability Candidate** | Prerequisite capability: Obtain hypotenuse length from two perpendicular leg lengths via $\sqrt{\text{leg}_1^2 + \text{leg}_2^2}$. | `external_provider: Mathematics`, `acceptance_status: PROVIDER_REVIEW_REQUIRED`. Physics authored draft; not Mathematics-reviewed (`EXTERNAL_PROVIDER_REVIEW_REQUIRED`). |
| **`SRC-AUTHOR-VEC`** | **Authored Source** (`status: CANDIDATE`) | V3B vector-representation design seed. | Author-created project draft; no official exam provenance claimed. |
| **`SRC-MATH-BRIDGE-CANDIDATE`** | **Authored Source** (`status: CANDIDATE`) | Author-drafted Mathematics bridge note (signed coordinates, right-triangle magnitude). | Author-created bridge draft; not a Mathematics-provider-reviewed artifact (`EXTERNAL_PROVIDER_REVIEW_REQUIRED`). |
| **`SRC-NCERT-PLANE`** | **Curriculum Candidate** (`status: CANDIDATE`) | NCERT Motion in a Plane (keph103.pdf, Chapter 3). | Motivates graphical vector addition/subtraction. Exact claim-level reconciliation pending. |
| **`SRC-PHET`** | **Activity Source Candidate** (`status: CANDIDATE`) | PhET Vector Addition simulation landing page. | Candidate visual exploration; simulation not executed in repository. |
| **`Physics/content/relative-motion-g9/`** | **Published Frozen Evidence** | Frozen publication artifacts compiled from baseline run. | Subtopic 2 assets were compiled as prerequisites for relative motion; no standalone Subtopic 2 baseline exists. |

---

## 2. Pedagogical Schema Definition & Schema Provenance

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
    They are not normative package-schema fields unless separately promoted.
```

Each microtopic is governed by a 13-field cognitive specification contract organizing evidence from `Physics/adapter/CoreContracts.json`, `Physics/gates/motion-vectors.v1.json`, `Shared/roles/CORE*.md`, and `Physics/library/vector-representation.v1.json`.

**Governing Extraction Rule**: If repository evidence supports a field, the source-backed value is recorded. If repository evidence does not support a field, it **must** be marked with its explicit failure-closed gap token (`*_AUTHOR_REQUIRED`). When multiple repository layers declare conflicting or divergent representations, the matrix **must expose both authorities** rather than collapsing them.

1. **`microtopic_id`**: Canonical repository identifier.
2. **`microtopic_name`**: Concise concept title.
3. **`authority`**: Explicit repository source files, gates, validator references, and unbacked elements.
4. **`entry_capability`**: Pre-existing skills and concepts strictly required before this microtopic. External-provider dependencies preserve provider and review status.
5. **`target_aha`**: The singular conceptual shift or cognitive leap the learner must make (pedagogical overlay).
6. **`controlled_experience`**: The cognitive vary / hold / notice structure. Extracted only from source counterexamples, diagnostics, or teaching paths; if synthesis is required, marked `CONTROLLED_EXPERIENCE_SYNTHESIS_AUTHOR_REQUIRED`; if absent, marked `CONTROLLED_EXPERIENCE_AUTHOR_REQUIRED`. Pure conceptual experiment, independent of delivery media.
7. **`representation_bridge`**: Dual-authority representation contract capturing pedagogical need, engineering gate declaration, library declaration, and alignment status (`ALIGNED`, `GATE_REPRESENTATION_UNBOUND`, `CROSS_LAYER_REPRESENTATION_DIVERGENCE`, `REPRESENTATION_BRIDGE_AUTHOR_REQUIRED`).
8. **`misconceptions`**: Plausible incorrect mental models, diagnostic triggers, and repair strategies.
9. **`boundary_or_check`**: Extreme conditions, limiting cases, and mathematical/physical checks.
10. **`assessment_evidence`**: Concrete observable student work proving mastery.
11. **`governing_convention`**: Governed coordinate system and sign rules. If missing from `bucket.conventions[]`, marked `CONVENTION_AUTHOR_REQUIRED`.
12. **`scope`**: Permitted versus prohibited physical scenarios.
13. **`intrinsic_depth`**: Intrinsic difficulty badge (`MEDIUM`/`HARD`) and source justification.

---

## 3. Four Canonical Pedagogical Contracts (`BUCKET-VECTOR-REPRESENTATION`)

### `MIC-VECTOR-VS-SCALAR`: Magnitude, vector and signed component

```yaml
microtopic_id: MIC-VECTOR-VS-SCALAR
microtopic_name: Magnitude, vector and signed component

authority:
  status: LIBRARY_CANDIDATE_WITH_ENGINEERING_GATE
  source_refs:
    - Physics/library/vector-representation.v1.json#microtopics[0]
    - Physics/gates/motion-vectors.v1.json#gates[PHY-VEC-SCALAR-VECTOR]
    - Shared/roles/CORE1A.md
  unsupported_fields:
    - bucket.conventions[] (absent in library JSON; CONVENTION_AUTHOR_REQUIRED)
    - elicitation (null in library JSON; CORE1B_COVERAGE_GAP)

entry_capability:
  - capability_ref: CAP-SIGNED-PAIR-BRIDGE
    provider: Mathematics
    acceptance_status: PROVIDER_REVIEW_REQUIRED
    action: "Read signed coordinates on an axis and subtract two coordinate values, keeping the sign."
  - capability_ref: CAP-RIGHT-TRIANGLE-BRIDGE
    provider: Mathematics
    acceptance_status: PROVIDER_REVIEW_REQUIRED
    action: "Obtain the hypotenuse length from two perpendicular leg lengths."
  - assumption: "Signed coordinate subtraction on one axis is available or bridged."

target_aha:
  - See a nonnegative speed/magnitude and a pair of signed components as two different descriptions of one physical vector, not two separate quantities.

controlled_experience:
  status: SOURCE_EXTRACTED_FROM_GATE_COUNTEREXAMPLES
  cognitive_experiment:
    experience_1_orientation_vs_magnitude:
      prompt: "Two vectors, (3,4) and (4,3) m/s, have the same magnitude. Do they point the same way?"
      hold_constant: Nonnegative magnitude (|v| = 5 m/s).
      vary: Component assignment across perpendicular axes ((3,4) vs (4,3)).
      learner_should_notice: "Both magnitudes agree (5 m/s), yet comparing signed components shows the vectors point in different directions; equal magnitude does not mean equal vector."
      source_basis: vector-representation.v1.json#misconceptions[0] & gate PHY-VEC-SCALAR-VECTOR#misconceptions[0]
    experience_2_negative_component_sign:
      prompt: "If the y-component is -4 m/s, is the speed negative?"
      hold_constant: Vector magnitude (|v| = 4 m/s).
      vary: Component sign (positive vs negative y-direction).
      learner_should_notice: "A velocity of (0,-4) m/s has speed 4 m/s, not -4 m/s. The signed component carries direction, while the magnitude is taken nonnegative after squaring."
      source_basis: vector-representation.v1.json#misconceptions[1] & gate PHY-VEC-SCALAR-VECTOR#misconceptions[1]
  note: "Two discrete cognitive comparisons exist in source evidence; synthesizing them into a single multi-variable experience is CONTROLLED_EXPERIENCE_SYNTHESIS_AUTHOR_REQUIRED."

representation_bridge:
  pedagogical_need:
    "Show a single vector's signed components against declared perpendicular axes and connect them to its nonnegative magnitude."
  engineering_gate:
    representation_ref: REP-VEC-SINGLE
    kind: VECTOR
    required_labels: ["declared frame and axis directions", "axis units", "vector symbol", "signed component readout"]
    verification: "Read the endpoint coordinates off the drawn axes and confirm they reproduce the stated signed components; confirm equal coordinate scale on both axes."
    relation_bindings: ["REL-VEC-MAGNITUDE"]
    concept_bindings: ["CON-VEC-COMPONENT-SIGNED", "CON-VEC-TWO-DESCRIPTIONS"]
  library:
    representation_refs:
      - REP-VECTOR-COMPONENT
    kind: VECTOR
    required_elements: ["Named common frame/axes", "Labelled vector with tail at the origin and arrowhead at the endpoint", "Signed component readout along each axis"]
    relation_bindings: ["REL-VECTOR-SUBTRACTION"]
  alignment_status: CROSS_LAYER_REPRESENTATION_DIVERGENCE
  architectural_note: "Gate PHY-VEC-SCALAR-VECTOR mandates REP-VEC-SINGLE bound to REL-VEC-MAGNITUDE, while candidate library binds REP-VECTOR-COMPONENT to REL-VECTOR-SUBTRACTION. Both are of kind VECTOR but differ in ID and relation bindings."

misconceptions:
  - wrong_idea: "The magnitude and the vector are the same thing, so stating '5 m/s' fully answers a direction question."
    counterexample: "(3,4) m/s and (4,3) m/s both have magnitude 5 m/s but point in different directions."
    diagnostic: "Two vectors, (3,4) and (4,3) m/s, have the same magnitude. Do they point the same way?"
    repair: "Recompute both magnitudes (both 5 m/s) then compare the signed components directly; equal magnitude does not mean equal vector."
  - wrong_idea: "A negative component means the object is slow or the quantity is 'negative speed'."
    counterexample: "A velocity of (0,-4) m/s has speed 4 m/s, not -4 m/s."
    diagnostic: "If the y-component is -4 m/s, is the speed negative?"
    repair: "Separate the signed component (direction information) from the magnitude (always taken nonnegative after squaring)."

boundary_or_check:
  limiting_case: "Zero vector (0,0) m/s has magnitude 0 m/s and no assigned direction."
  invariance_check: "Magnitude is invariant under reversing both components: |(-vx, -vy)| = |(vx, vy)|."
  sign_erasure_check: "Squaring erases sign; recovering direction requires the original signed pair, not the magnitude."

assessment_evidence:
  observable_task: "A vector has components (-3, 4) m/s. State its magnitude and describe its direction in words."
  model_response: "Magnitude 5 m/s; the vector points into the quadrant that is left (negative x) and up (positive y)."
  check_step: "Reversing both signs, (3,-4), would give the same magnitude but the opposite direction."
  oracle: "SPEED_FROM_COMPONENTS (bindings: vx=DAT-W-X, vy=DAT-W-Y; verified by CHECKED_BY_AUTHOR)."

governing_convention:
  status: CONVENTION_AUTHOR_REQUIRED
  note: "bucket.conventions[] absent on BUCKET-VECTOR-REPRESENTATION. Gate requires declared frame and perpendicular axes before reading components."

scope:
  include:
    - 2D Cartesian plane with perpendicular axes.
    - Constant velocities / displacements.
    - Nonnegative scalar magnitude via right-triangle relation.
  exclude:
    - 3D vectors.
    - Oblique (non-perpendicular) coordinate axes.
    - Relativistic composition.

intrinsic_depth:
  badge: MEDIUM
  basis: "The distinction is easy to state and easy to blur under time pressure, once negative components appear." (vector-representation.v1.json line 178)
```

---

### `MIC-SIGNED-COMPONENT`: Choosing axes and keeping components signed

```yaml
microtopic_id: MIC-SIGNED-COMPONENT
microtopic_name: Choosing axes and keeping components signed

authority:
  status: LIBRARY_CANDIDATE_WITH_ENGINEERING_GATE
  source_refs:
    - Physics/library/vector-representation.v1.json#microtopics[1]
    - Physics/gates/motion-vectors.v1.json#gates[PHY-VEC-AXIS-CONVENTION]
    - Shared/roles/CORE1A.md
  unsupported_fields:
    - bucket.conventions[] (absent in library JSON; CONVENTION_AUTHOR_REQUIRED)
    - elicitation (null in library JSON; CORE1B_COVERAGE_GAP)
    - exit_task data atoms (held under ISS-VEC-EXIT-DATA; DATA_GAP)

entry_capability:
  - Can identify a vector's components once axes are declared (MIC-VECTOR-VS-SCALAR / CAP-VECTOR-VS-SCALAR).

target_aha:
  - Recognise that the axis choice is a free, declared decision, but once declared, every component's sign is fixed by it — not by the physical 'niceness' of the described motion.

controlled_experience:
  status: SOURCE_EXTRACTED_FROM_TEACHING_PATH
  cognitive_experiment:
    vary: Declared positive direction of an axis (e.g. +x East vs +x West).
    hold_constant: Physical vector and spatial motion (w = (3,4) m/s East/North).
    learner_should_notice: "w = (3,4) m/s under east/north-positive becomes (-3,4) m/s if x is redeclared west-positive. Reversing a declared axis negates components measured along it, but the physical vector and its calculated magnitude (5 m/s) remain unchanged."
  source_basis: vector-representation.v1.json#teaching_path[SC-2, SC-3] & gate PHY-VEC-AXIS-CONVENTION#reasoning_sequence

representation_bridge:
  pedagogical_need:
    "Show how re-declaring axis directions alters component signs on the coordinate readout while preserving vector length and direction."
  engineering_gate:
    representation_ref: REP-AXIS-CONVENTION
    kind: VECTOR
    required_labels: ["declared positive directions for both axes", "axis units", "vector symbol", "explicit sign for each component"]
    verification: "Confirm that re-declaring an axis flips the corresponding component sign on the drawing, and that the Pythagorean hypotenuse length is unchanged."
    relation_bindings: ["REL-AXIS-REVERSAL"]
    concept_bindings: ["CON-AXIS-FREE-CHOICE", "CON-AXIS-BINDING"]
  library:
    representation_refs:
      - REP-VECTOR-COMPONENT
    kind: VECTOR
    scene_instance: SI-VECTOR-COMPONENTS (scene: symbol w, components (3,4) m/s, unit m/s)
  alignment_status: CROSS_LAYER_REPRESENTATION_DIVERGENCE
  architectural_note: "Gate PHY-VEC-AXIS-CONVENTION specifies REP-AXIS-CONVENTION (requiring explicit axis re-declaration verification), whereas candidate library reuses REP-VECTOR-COMPONENT."

misconceptions:
  - wrong_idea: "A component should be made positive because the object is 'moving forward'."
    counterexample: "With east declared positive, an object moving west has a negative x component however natural its motion feels."
    diagnostic: "If east is declared positive and the object moves west, is the x-component positive or negative?"
    repair: "The sign follows the declared axis only; 'forward' is not itself an axis direction unless it was declared as one."

boundary_or_check:
  reversal_check: "Reversing a declared axis direction negates every component along that axis: w_x' = -w_x."
  magnitude_invariance: "Magnitude is convention-independent: sqrt(vx^2 + vy^2) = sqrt((-vx)^2 + vy^2)."
  perpendicularity_check: "Axes remain strictly perpendicular and non-rotating under re-declaration."

assessment_evidence:
  observable_task: "Under 'north positive, east positive', a vector is (5,-2) m/s. State it again under 'south positive, east positive', and explain why the magnitude does not change."
  model_response: "(5, 2) m/s under the new convention; magnitude stays sqrt(25+4) both times."
  check_step: "Re-declare the axis back to original convention and confirm (5,-2) is recovered."
  gap: "Component values (5,-2) and (5,2) are not declared as data atom records in library; validator cannot be bound (ISS-VEC-EXIT-DATA; DATA_GAP)."

governing_convention:
  status: CONVENTION_AUTHOR_REQUIRED
  note: "bucket.conventions[] absent. Axis choice is free but must be explicitly declared before reading components."

scope:
  include:
    - Cartesian axes in a plane.
    - Discrete 180-degree axis direction reversals.
    - Component sign mapping under axis flip.
  exclude:
    - Oblique axes.
    - Continuous axis rotations (Euler angles).
    - Rotating frames.

intrinsic_depth:
  badge: MEDIUM
  basis: "Axis choice feels arbitrary to a new learner, so students often silently drop or flip a sign when the story changes." (vector-representation.v1.json line 253)
```

---

### `MIC-GRAPHICAL-SUBTRACTION`: Subtraction as addition of the reversed vector

```yaml
microtopic_id: MIC-GRAPHICAL-SUBTRACTION
microtopic_name: Subtraction as addition of the reversed vector

authority:
  status: LIBRARY_CANDIDATE_WITH_ENGINEERING_GATE
  source_refs:
    - Physics/library/vector-representation.v1.json#microtopics[2]
    - Physics/gates/motion-vectors.v1.json#gates[PHY-VEC-SUBTRACTION]
    - Shared/roles/CORE1A.md
  unsupported_fields:
    - bucket.conventions[] (absent in library JSON; CONVENTION_AUTHOR_REQUIRED)
    - elicitation (null in library JSON; CORE1B_COVERAGE_GAP)

entry_capability:
  - Can read signed components and knows a vector's magnitude is not its direction (MIC-VECTOR-VS-SCALAR / CAP-VECTOR-VS-SCALAR).
  - Can choose and maintain axes (MIC-SIGNED-COMPONENT).
  - External right-triangle bridge: CAP-RIGHT-TRIANGLE-BRIDGE (PROVIDER_REVIEW_REQUIRED).

target_aha:
  - See P - Q as P + (-Q): reverse Q's arrowhead without changing its length, then apply tail-to-head addition.

controlled_experience:
  status: SOURCE_EXTRACTED_FROM_GATE_COUNTEREXAMPLES
  cognitive_experiment:
    experience_1_operand_order:
      prompt: "For P=(6,0) m/s and Q=(0,8) m/s, construct P - Q vs Q - P."
      hold_constant: Vectors P and Q in the declared frame.
      vary: Operand subtraction order (P - Q vs Q - P).
      learner_should_notice: "P - Q yields (6,-8) m/s, while Q - P yields (-6,8) m/s. Connecting the arrowheads arbitrarily hides observer/subtraction order and produces opposite vectors."
      source_basis: gate PHY-VEC-SUBTRACTION#misconceptions[0] & vector-representation.v1.json#misconceptions[0]
    experience_2_reversal_magnitude:
      prompt: "Does reversing an arrow from (0,8) to (0,-8) m/s change its length?"
      hold_constant: Vector magnitude (8 m/s).
      vary: Arrowhead orientation (Q vs -Q).
      learner_should_notice: "Reversing an arrow only negates the signed components; squaring components makes sign irrelevant to length, so magnitude is unchanged."
      source_basis: gate PHY-VEC-SUBTRACTION#misconceptions[1] & vector-representation.v1.json#misconceptions[1]
  note: "Two discrete cognitive checks exist in source; full continuous multi-vector synthesis is CONTROLLED_EXPERIENCE_SYNTHESIS_AUTHOR_REQUIRED."

representation_bridge:
  pedagogical_need:
    "Show why subtracting Q means adding the reversed -Q, tail-to-head, distinct from the direct component-subtraction shortcut."
  engineering_gate:
    representation_ref: REP-SUB-CONSTRUCTION
    kind: VECTOR
    required_labels: ["declared frame", "labelled P, Q and the resultant", "common length scale", "axis units"]
    verification: "Compare the drawn resultant's components against the direct component subtraction; both routes must agree."
    relation_bindings: ["REL-VEC-SUBTRACTION"]
    concept_bindings: ["CON-SUB-AS-ADD-OPPOSITE", "CON-SUB-FREE-TRANSLATION"]
  library:
    representation_refs:
      - REP-VECTOR-SUBTRACTION-CONSTRUCTION
    kind: VECTOR_SUBTRACTION
    required_elements: ["Named common frame", "Labelled P, Q and -Q", "Tail-to-head construction of P + (-Q)", "Resultant labelled P-Q, with tail/head and scale"]
    scene_instance: SI-VECTOR-SUBTRACTION (kind: VECTOR_SUBTRACTION, P=(6,0), Q=(0,8), P-Q=(6,-8))
  alignment_status: CROSS_LAYER_REPRESENTATION_DIVERGENCE
  architectural_note: "Gate PHY-VEC-SUBTRACTION specifies REP-SUB-CONSTRUCTION of kind VECTOR, while candidate library specifies REP-VECTOR-SUBTRACTION-CONSTRUCTION of kind VECTOR_SUBTRACTION (explicitly requiring the intermediate -Q reversed arrow)."

misconceptions:
  - wrong_idea: "Vector subtraction means drawing both vectors from the same origin and connecting their two tips in whichever order looks right."
    counterexample: "For P=(6,0) and Q=(0,8) m/s the two tip-joining orders give (6,-8) and (-6,8) m/s, which are opposite vectors."
    diagnostic: "Which endpoint does the subtraction arrow start from: the tip of P or the tip of Q?"
    repair: "Perform the explicit reverse-then-add construction (GS-1 to GS-3); the two-tips shortcut hides the observer order and is easy to reverse by mistake."
  - wrong_idea: "Reversing a vector changes its magnitude."
    counterexample: "(0,8) m/s and (0,-8) m/s both have magnitude 8 m/s."
    diagnostic: "Does an arrow get longer or shorter when you flip it end for end?"
    repair: "Reversal only negates the signed components; the right-triangle bridge uses their squares, so the magnitude is unchanged."

boundary_or_check:
  self_subtraction_zero: "P - P = 0 for any vector P."
  antisymmetry_check: "Q - P = -(P - Q); reversing operand order negates the resultant."
  component_reconciliation: "Graphical tail-to-head resultant must match component subtraction: (P-Q)x = Px - Qx, (P-Q)y = Py - Qy."

assessment_evidence:
  observable_task: "In a common east/north frame, P = (6,0) m/s and Q = (0,8) m/s. Construct P - Q graphically and state the resultant's components and magnitude."
  model_response: "P - Q = (6,-8) m/s, magnitude 10 m/s."
  check_step: "Direct component subtraction (6-0, 0-8) = (6,-8) m/s matches graphical resultant."
  oracle: "SPEED_FROM_COMPONENTS (bindings: vx=DAT-PQ-X, vy=DAT-PQ-Y; verified by CHECKED_BY_AUTHOR)."

governing_convention:
  status: CONVENTION_AUTHOR_REQUIRED
  note: "bucket.conventions[] absent. Free vectors may be translated without rotation for tail-to-head addition."

scope:
  include:
    - 2D graphical vector subtraction via additive inverse (reverse and add).
    - Free translation of vectors without rotation.
    - Reconciliation between graphical resultant and component subtraction.
  exclude:
    - Parallelogram subtraction shortcut without explicit reversal step.
    - Vector division or cross products.

intrinsic_depth:
  badge: MEDIUM
  basis: "Component/magnitude confusion and axis-convention slips are common but each individually correctable with explicit construction." (vector-representation.v1.json line 29)
```

---

### `MIC-FRAME-QUALIFICATION-BOUNDARY`: When simple relation needs frame qualification

```yaml
microtopic_id: MIC-FRAME-QUALIFICATION-BOUNDARY
microtopic_name: When the simple v_A/B = v_A - v_B relation needs frame qualification (research-boundary note)

authority:
  status: LIBRARY_CANDIDATE_ONLY
  source_refs:
    - Physics/library/vector-representation.v1.json#microtopics[3]
    - Shared/roles/CORE1A.md
  unsupported_fields:
    - engineering_gate (none exists; this is an author-created model-boundary stress extension)
    - bucket.conventions[] (absent in library JSON; CONVENTION_AUTHOR_REQUIRED)
    - elicitation (null in library JSON; CORE1B_COVERAGE_GAP)
    - representations (representation_refs: []; REPRESENTATION_BRIDGE_AUTHOR_REQUIRED)

entry_capability:
  - Has completed MIC-GEOMETRIC-CHECK and accepts v_A/B = v_A - v_B for translating, nonrotating frames.

target_aha:
  - Recognise that the simple subtraction relation assumes both frames are nonrotating and non-relativistic; naming when it needs qualification is itself the (bounded) research task, not deriving the replacement mathematics.

controlled_experience:
  status: CONTROLLED_EXPERIENCE_AUTHOR_REQUIRED
  note: "The source teaching path (FB-1 to FB-3) is purely DECLARE: it restates conditions, names failure regimes, and declares non-assessment status. No vary/hold/notice experiment exists in repository evidence."

representation_bridge:
  pedagogical_need:
    "Demarcate the validity boundary where simple linear vector subtraction ceases to apply."
  engineering_gate:
    representation_ref: null
    status: NO_GATE_EXISTS
  library:
    representation_refs: []
  alignment_status: REPRESENTATION_BRIDGE_AUTHOR_REQUIRED
  architectural_note: "Neither the engineering gate layer nor the library candidate contains a representation for this boundary note. It is text-only research-boundary material."

misconceptions:
  - wrong_idea: "Since the school formula is 'wrong' in general, it should not be taught or trusted at all."
    counterexample: "A model's stated domain of validity is what makes it correct within that domain; the Grade 9 translating-frame case is exactly where the taught relation applies."
    diagnostic: "Does a merry-go-round or a near-light-speed spacecraft appear anywhere in the Grade 9 assessment scope?"
    repair: "A model's stated domain of validity is what makes it correct within that domain; the Grade 9 translating-frame case is exactly where the taught relation applies."

boundary_or_check:
  condition_1: "Parallel, nonrotating axes (fails in rotating frames; requires Coriolis/centrifugal terms)."
  condition_2: "Classical speeds v << c (fails near speed of light; requires relativistic velocity addition)."
  scope_check: "Explicit non-assessment status: excluded from Grade 9 exam claims."

assessment_evidence:
  observable_task: "Name (without deriving) one situation where v_A/B = v_A - v_B would need an additional term, and state whether that situation is in the Grade 9 assessment scope."
  model_response: "A rotating reference frame (e.g. observations made from a spinning platform) needs an additional Coriolis-type term; this is outside the Grade 9 assessment scope."
  oracle: "No numeric claim. Asserts two named boundary regimes; verified by CHECKED_BY_AUTHOR."

governing_convention:
  status: CONVENTION_AUTHOR_REQUIRED
  note: "bucket.conventions[] absent. Governed by declared classical domain of validity."

scope:
  include:
    - Naming without deriving the two regimes of failure (rotating frames, relativistic speeds).
    - Explaining the concept of a model's domain of validity.
  exclude:
    - Derivation of Coriolis acceleration or centrifugal fictitious forces.
    - Relativistic velocity addition formulas (Lorentz boosts).
    - Grade 9 assessment claims (explicitly non-assessed).

intrinsic_depth:
  badge: HARD
  basis: "Not a Grade 9 assessment badge: this is a RESEARCH-depth boundary note, included only to show where the taught relation stops applying." (vector-representation.v1.json line 416)
```

---

## 4. CORE1 Matrix (Compact Orientation Map)

| Microtopic | Named Objects / Quantities | Essential Convention | Governing Relation | Meaning in Words | Validity Conditions | Compact Anchor | Hard Transition | Scope / Exclusion | Representation Alignment | Authority / Gaps |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`MIC-VECTOR-VS-SCALAR`** | $\vec{v}$: Vector ($\text{m/s}$)<br>$v_x, v_y$: Signed components ($\text{m/s}$)<br>$\|\vec{v}\|$: Magnitude ($\text{m/s}$) | **`CONVENTION_AUTHOR_REQUIRED`**<br>*(Local scenes cite East/North; bucket convention absent)* | $\|\vec{v}\| = \sqrt{v_x^2 + v_y^2}$<br>(`REL-VEC-MAGNITUDE`) | Magnitude and signed components are two descriptions of one vector; magnitude is nonnegative; components carry direction. | Declared perpendicular axes; same frame and unit; classical speeds. | $\vec{w} = (3,4)\text{ m/s} \implies \|\vec{w}\| = 5\text{ m/s}$ (`DAT-W-X`, `DAT-W-Y`). | Distinguishing scalar magnitude from vector quantity when negative components appear. | **In:** 2D Cartesian plane, perpendicular axes.<br>**Out:** 3D, oblique axes, relativistic addition. | Gate: `REP-VEC-SINGLE`<br>Library: `REP-VECTOR-COMPONENT`<br>(**`CROSS_LAYER_REPRESENTATION_DIVERGENCE`**) | `LIBRARY_CANDIDATE`. Gate `PHY-VEC-SCALAR-VECTOR`. *Gaps:* `CONVENTION_GAP`, `EXTERNAL_PROVIDER_REVIEW_REQUIRED`. |
| **`MIC-SIGNED-COMPONENT`** | $\vec{w}$: Vector ($\text{m/s}$)<br>$w_x, w_y$: Components under Conv 1<br>$w_x', w_y'$: Components under Conv 2 | **`CONVENTION_AUTHOR_REQUIRED`**<br>*(Axis declaration is free; component signs fixed by it)* | $w_x' = -w_x$ under $+x$ flip<br>(`REL-AXIS-REVERSAL`) | Axis choice is a free declared decision, but once chosen, every component sign is fixed by it. | Declared axes remain perpendicular and non-rotating. | $(3,4)\text{ m/s}$ (E/N) $\to (-3,4)\text{ m/s}$ (W/N); magnitude stays $5\text{ m/s}$. | Accepting that motion "forward" can have negative component if axis points backward. | **In:** Discrete Cartesian axis reversals.<br>**Out:** Continuous rotations, rotating frames. | Gate: `REP-AXIS-CONVENTION`<br>Library: `REP-VECTOR-COMPONENT`<br>(**`CROSS_LAYER_REPRESENTATION_DIVERGENCE`**) | `LIBRARY_CANDIDATE`. Gate `PHY-VEC-AXIS-CONVENTION`. *Gaps:* `CONVENTION_GAP`, `DATA_GAP` (`ISS-VEC-EXIT-DATA`). |
| **`MIC-GRAPHICAL-SUBTRACTION`** | $\vec{P}$: Minuend ($\text{m/s}$)<br>$\vec{Q}$: Subtrahend ($\text{m/s}$)<br>$-\vec{Q}$: Reversed vector<br>$\vec{P}-\vec{Q}$: Resultant | **`CONVENTION_AUTHOR_REQUIRED`**<br>*(Free vector translation without rotation; tail-to-head)* | $\vec{P} - \vec{Q} = \vec{P} + (-\vec{Q})$<br>(`REL-VECTOR-SUBTRACTION`) | Subtracting a vector means adding its reverse; reverse $Q$ then add tail-to-head to $P$. | Same declared axes; free vectors translate without rotation. | $\vec{P}=(6,0)$, $\vec{Q}=(0,8) \implies \vec{P}-\vec{Q}=(6,-8)\text{ m/s}$, $\|\vec{P}-\vec{Q}\|=10\text{ m/s}$. | Replacing the "connect two tips" shortcut with explicit reversal and addition. | **In:** 2D reverse-then-add construction.<br>**Out:** Parallelogram shortcut without reversal. | Gate: `REP-SUB-CONSTRUCTION`<br>Library: `REP-VECTOR-SUBTRACTION-CONSTRUCTION`<br>(**`CROSS_LAYER_REPRESENTATION_DIVERGENCE`**) | `LIBRARY_CANDIDATE`. Gate `PHY-VEC-SUBTRACTION`. Validator `SPEED_FROM_COMPONENTS`. *Gap:* `CONVENTION_GAP`. |
| **`MIC-FRAME-QUALIFICATION-BOUNDARY`** | $\vec{v}_{A/B}$: Relative velocity ($\text{m/s}$)<br>Failure regimes: rotating frames, $v \approx c$ | **`CONVENTION_AUTHOR_REQUIRED`**<br>*(Translating classical frame boundary)* | Domain of validity for $\vec{v}_{A/B} = \vec{v}_A - \vec{v}_B$ | Simple vector subtraction applies to translating classical frames; rotating frames require Coriolis terms. | Nonrotating, non-relativistic translating frames; non-assessment note. | Named regimes (spinning platform, $v \to c$). No numeric claim. | Recognizing that physical models have bounded validity regimes. | **In:** Naming boundary conditions.<br>**Out:** Graduate derivations, Grade 9 exam claims. | Gate: None<br>Library: `[]`<br>(**`REPRESENTATION_BRIDGE_AUTHOR_REQUIRED`**) | `LIBRARY_CANDIDATE` (Author note). No gate. *Gaps:* `CONVENTION_GAP`, `REPRESENTATION_BRIDGE_AUTHOR_REQUIRED`. |

---

## 5. CORE1A Matrix (Declarative Detailed Teaching)

| Microtopic | Entry Capability | Target Inferential Jump | Controlled Experience (Vary / Hold / Notice) | Completed Teaching Construction (Steps & Roles) | Why-Valid Obligations | Representation Bridge (Gate vs Library) | Misconception & Diagnostic | Repair | Independent Check | Exit Evidence | Authority / Gaps |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`MIC-VECTOR-VS-SCALAR`** | `CAP-SIGNED-PAIR-BRIDGE` & `CAP-RIGHT-TRIANGLE-BRIDGE` (`PROVIDER_REVIEW_REQUIRED`). | Nonnegative magnitude and signed component pair are two descriptions of one vector. | **Exp 1:** Hold $\|v\|=5\text{ m/s}$; vary $(3,4)$ vs $(4,3)$; notice directions differ.<br>**Exp 2:** Hold $\|v\|=4$; vary sign; notice $(0,-4)$ has speed $+4\text{ m/s}$. | **VS-1 (DECLARE):** Name frame and axes.<br>**VS-2 (TRANSFORM):** Read signed components.<br>**VS-3 (TRANSFORM):** Apply right-triangle bridge.<br>**VS-4 (VERIFY):** State magnitude nonnegative, keep components for direction. | Component sign requires declared direction; sign is axis reading; legs form right triangle; squaring erases sign. | Gate specifies `REP-VEC-SINGLE` (`VECTOR`); Library specifies `REP-VECTOR-COMPONENT` (`VECTOR`).<br>(**`CROSS_LAYER_REPRESENTATION_DIVERGENCE`**) | **Wrong:** Magnitude is vector; stating 5 m/s answers direction.<br>**Diag:** "Do (3,4) and (4,3) point same way?" | Recompute both magnitudes (5 m/s) then compare components directly. | Reversing both signs gives same magnitude but opposite direction. | Vector $(-3,4)\text{ m/s} \implies$ magnitude $5\text{ m/s}$, direction left & up. Verified by `SPEED_FROM_COMPONENTS`. | Library candidate; gate `PHY-VEC-SCALAR-VECTOR`. *Gaps:* `CONVENTION_GAP`, `EXTERNAL_PROVIDER_REVIEW_REQUIRED`. |
| **`MIC-SIGNED-COMPONENT`** | `MIC-VECTOR-VS-SCALAR` (`CAP-VECTOR-VS-SCALAR`). | Axis choice is free, but once chosen, signs are fixed by it — not by motion "niceness". | **Vary:** Declared axis direction (+x East vs West).<br>**Hold:** Physical vector ($w$).<br>**Notice:** Component flips sign ($(3,4) \to (-3,4)$), magnitude ($5\text{ m/s}$) invariant. | **SC-1 (DECLARE):** Declare positive directions explicitly.<br>**SC-2 (TRANSFORM):** Re-express vector under reversed axis.<br>**SC-3 (VERIFY):** Confirm magnitude is unchanged. | Sign is meaningful only relative to declared axis; reversing direction negates components; squaring removes sign. | Gate specifies `REP-AXIS-CONVENTION` (`VECTOR`); Library reuses `REP-VECTOR-COMPONENT` (`VECTOR`, `SI-VECTOR-COMPONENTS`).<br>(**`CROSS_LAYER_REPRESENTATION_DIVERGENCE`**) | **Wrong:** Make component positive because moving forward.<br>**Diag:** "If east is positive and object moves west, is x positive or negative?" | Sign follows declared axis only; 'forward' is not an axis unless declared. | Re-declare axis back to original convention and recover $(5,-2)\text{ m/s}$. | Under N/E positive, vector is $(5,-2)$; under S/E positive, $(5,2)\text{ m/s}$, magnitude invariant. | Library candidate; gate `PHY-VEC-AXIS-CONVENTION`. *Gaps:* `CONVENTION_GAP`, `DATA_GAP` (`ISS-VEC-EXIT-DATA`). |
| **`MIC-GRAPHICAL-SUBTRACTION`** | `MIC-VECTOR-VS-SCALAR` & `MIC-SIGNED-COMPONENT`; `CAP-RIGHT-TRIANGLE-BRIDGE`. | See $P - Q$ as $P + (-Q)$: reverse $Q$, then add tail-to-head. | **Exp 1:** Hold $P, Q$; vary $P-Q$ vs $Q-P$; notice $(6,-8)$ vs $(-6,8)$ are opposite.<br>**Exp 2:** Hold magnitude; vary orientation; notice length unchanged. | **GS-1 (TRANSFORM):** Reverse $Q \to -Q$.<br>**GS-2 (TRANSFORM):** Translate $-Q$ to head of $P$.<br>**GS-3 (TRANSFORM):** Draw resultant from tail of $P$ to head of $-Q$.<br>**GS-4 (VERIFY):** Reconcile with direct component subtraction. | Vector negation flips signs; free vectors translate without rotation; tail-to-head gives sum; graphical and algebraic routes must agree. | Gate specifies `REP-SUB-CONSTRUCTION` (`VECTOR`); Library specifies `REP-VECTOR-SUBTRACTION-CONSTRUCTION` (`VECTOR_SUBTRACTION`).<br>(**`CROSS_LAYER_REPRESENTATION_DIVERGENCE`**) | **Wrong:** Connect two tips in whichever order looks right.<br>**Diag:** "Which endpoint does subtraction arrow start from: tip of P or Q?" | Perform explicit reverse-then-add construction; two-tips shortcut hides order. | Direct component subtraction $(6-0, 0-8) = (6,-8)\text{ m/s}$ matches graphical resultant. | $P=(6,0), Q=(0,8) \implies P-Q=(6,-8)\text{ m/s}$, magnitude $10\text{ m/s}$. Verified by `SPEED_FROM_COMPONENTS`. | Library candidate; gate `PHY-VEC-SUBTRACTION`. *Gap:* `CONVENTION_GAP`. |
| **`MIC-FRAME-QUALIFICATION-BOUNDARY`** | `MIC-GEOMETRIC-CHECK` (from relative motion). | Simple subtraction assumes nonrotating, non-relativistic frames; naming failure regimes is the bounded task. | **`CONTROLLED_EXPERIENCE_AUTHOR_REQUIRED`**<br>*(Source contains no cognitive experiment; teaching path is purely declarative)* | **FB-1 (DECLARE):** Restate parallel nonrotating axes and classical speed conditions.<br>**FB-2 (DECLARE):** Name rotating frames and relativistic speeds as failure regimes.<br>**FB-3 (DECLARE):** State explicit non-assessment status for Grade 9. | Conditions were declared when relation was derived; naming failure regime is defensible research claim; research depth is segregated from exam scope. | Neither layer provides a representation.<br>(**`REPRESENTATION_BRIDGE_AUTHOR_REQUIRED`**) | **Wrong:** Since school formula is "wrong" in general, don't trust it.<br>**Diag:** "Does merry-go-round or relativistic craft appear in Grade 9 scope?" | Model domain of validity is what makes it correct; translating-frame case is where relation applies. | Excluded-topics list already names rotating frames and Coriolis terms as out of scope. | Name situation where additional term is needed (rotating frame) and state it is outside exam scope. | Library candidate (Author note). No gate. *Gaps:* `CONVENTION_GAP`, `CONTROLLED_EXPERIENCE_AUTHOR_REQUIRED`, `REPRESENTATION_BRIDGE_AUTHOR_REQUIRED`. |

---

## 6. CORE1B Source-State Matrix (Strict Extraction Only)

In accordance with Phase A extraction constraints, the actual `elicitation` field in `Physics/library/vector-representation.v1.json` is inspected and recorded exactly as it exists. **No elicitation routes, sample prompts, or candidate questions are invented here.**

| Microtopic | Source State | Status | Required Coverage (from Core1A) | Predict Status | Attempt Status | Reconstruct Status | Diagnose Status | Repair Status | Boundary Test Status | Closure Status |
| :--- | :---: | :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`MIC-VECTOR-VS-SCALAR`** | `null` | **`CORE1B_AUTHOR_REQUIRED`** | Must elicit: distinguishing magnitude from signed components; predicting orientation from signs before magnitude calculation; checking sign reversal invariance. | `AUTHOR_REQUIRED` | `AUTHOR_REQUIRED` | `AUTHOR_REQUIRED` | `AUTHOR_REQUIRED` | `AUTHOR_REQUIRED` | `AUTHOR_REQUIRED` | `AUTHOR_REQUIRED` |
| **`MIC-SIGNED-COMPONENT`** | `null` | **`CORE1B_AUTHOR_REQUIRED`** | Must elicit: declaring positive axes; predicting component sign change under axis flip; verifying magnitude invariance under convention change. | `AUTHOR_REQUIRED` | `AUTHOR_REQUIRED` | `AUTHOR_REQUIRED` | `AUTHOR_REQUIRED` | `AUTHOR_REQUIRED` | `AUTHOR_REQUIRED` | `AUTHOR_REQUIRED` |
| **`MIC-GRAPHICAL-SUBTRACTION`** | `null` | **`CORE1B_AUTHOR_REQUIRED`** | Must elicit: reversing subtrahend vector; translating tail-to-head; predicting operand order reversal ($P-Q$ vs $Q-P$); reconciling with component difference. | `AUTHOR_REQUIRED` | `AUTHOR_REQUIRED` | `AUTHOR_REQUIRED` | `AUTHOR_REQUIRED` | `AUTHOR_REQUIRED` | `AUTHOR_REQUIRED` | `AUTHOR_REQUIRED` |
| **`MIC-FRAME-QUALIFICATION-BOUNDARY`** | `null` | **`CORE1B_AUTHOR_REQUIRED`** | Must elicit: identifying validity boundaries of simple model; recognizing non-rotating classical constraints; distinguishing model limits from exam scope. | `AUTHOR_REQUIRED` | `AUTHOR_REQUIRED` | `AUTHOR_REQUIRED` | `AUTHOR_REQUIRED` | `AUTHOR_REQUIRED` | `AUTHOR_REQUIRED` | `AUTHOR_REQUIRED` |

---

## 7. Representation-Alignment Matrix

| Microtopic | Gate Representation | Library Representation | Alignment Status | Reviewer Action Needed |
| :--- | :--- | :--- | :--- | :--- |
| **`MIC-VECTOR-VS-SCALAR`** | `REP-VEC-SINGLE`<br>(`kind: VECTOR`, gate `PHY-VEC-SCALAR-VECTOR`, bound to `REL-VEC-MAGNITUDE`) | `REP-VECTOR-COMPONENT`<br>(`kind: VECTOR`, library `vector-representation.v1.json`, bound to `REL-VECTOR-SUBTRACTION`) | **`CROSS_LAYER_REPRESENTATION_DIVERGENCE`** | Resolve naming and relation binding divergence between gate specification and candidate library before learner asset rendering. |
| **`MIC-SIGNED-COMPONENT`** | `REP-AXIS-CONVENTION`<br>(`kind: VECTOR`, gate `PHY-VEC-AXIS-CONVENTION`, bound to `REL-AXIS-REVERSAL`) | `REP-VECTOR-COMPONENT`<br>(`kind: VECTOR`, reused with scene `SI-VECTOR-COMPONENTS`) | **`CROSS_LAYER_REPRESENTATION_DIVERGENCE`** | Determine whether axis-convention re-declaration requires its own distinct representation contract (`REP-AXIS-CONVENTION`) or can share `REP-VECTOR-COMPONENT`. |
| **`MIC-GRAPHICAL-SUBTRACTION`** | `REP-SUB-CONSTRUCTION`<br>(`kind: VECTOR`, gate `PHY-VEC-SUBTRACTION`, bound to `REL-VEC-SUBTRACTION`) | `REP-VECTOR-SUBTRACTION-CONSTRUCTION`<br>(`kind: VECTOR_SUBTRACTION`, scene `SI-VECTOR-SUBTRACTION`) | **`CROSS_LAYER_REPRESENTATION_DIVERGENCE`** | Reconcile representation kind divergence (`VECTOR` vs `VECTOR_SUBTRACTION`) and ensure intermediate $-Q$ reversed vector is formally required. |
| **`MIC-FRAME-QUALIFICATION-BOUNDARY`** | None (`status: NO_GATE_EXISTS`) | `[]` (`representation_refs: []`) | **`REPRESENTATION_BRIDGE_AUTHOR_REQUIRED`** | Author a representation bridge (or formally declare this research-boundary note text-only without graphical depiction). |

---

## 8. Cross-Core Correspondence Matrix

| Microtopic | Core1 supported? | Core1A supported? | Core1B source state | Same intrinsic coverage possible? | Blocking Gaps |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **`MIC-VECTOR-VS-SCALAR`** | YES | YES | `null` | YES (Core1A provides complete 4-step construction to govern Core1B authoring) | `CONVENTION_GAP`, `CORE1B_AUTHOR_REQUIRED`, `EXTERNAL_PROVIDER_REVIEW_REQUIRED`. |
| **`MIC-SIGNED-COMPONENT`** | YES | YES | `null` | YES (Core1A provides complete 3-step re-declaration path) | `CONVENTION_GAP`, `CORE1B_AUTHOR_REQUIRED`, `DATA_GAP` (`ISS-VEC-EXIT-DATA`). |
| **`MIC-GRAPHICAL-SUBTRACTION`** | YES | YES | `null` | YES (Core1A provides complete reverse-translate-add-reconcile construction) | `CONVENTION_GAP`, `CORE1B_AUTHOR_REQUIRED`. |
| **`MIC-FRAME-QUALIFICATION-BOUNDARY`** | YES | YES | `null` | YES (Core1A provides 3-step boundary declaration) | `CONVENTION_GAP`, `CORE1B_AUTHOR_REQUIRED`, `REPRESENTATION_BRIDGE_AUTHOR_REQUIRED`. |

---

## 9. Phase-B Authoring Backlog

Phase B must not be executed until Phase A extraction passes review. The following backlog items represent the exact work required from a pedagogical authoring agent:

1. **Author Core1B Elicitation Routes for all 4 Microtopics (`CORE1B_AUTHOR_REQUIRED`)**:
   - **`MIC-VECTOR-VS-SCALAR`**: Author `predict` (prompt predicting direction from signed components without computing magnitude; defensible answer), `attempt` (rubric closure separating magnitude from components), `reconstruct` route, `diagnose` (magnitude mistaken for direction), `repair`, and `boundary_test` (both components negated). Must preserve Core1A coverage (`VS-1` to `VS-4`).
   - **`MIC-SIGNED-COMPONENT`**: Author `predict` (predicting sign change under axis reversal), `attempt` (rubric closure confirming magnitude invariance), `reconstruct` route, `diagnose` ("forward motion must be positive"), `repair`, and `boundary_test`. Must preserve Core1A coverage (`SC-1` to `SC-3`).
   - **`MIC-GRAPHICAL-SUBTRACTION`**: Author `predict` (predicting operand reversal $P-Q$ vs $Q-P$), `attempt` (rubric closure requiring explicit $-Q$ reversal step), `reconstruct` route, `diagnose` (two-tips shortcut), `repair`, and `boundary_test` ($P-P=0$). Must preserve Core1A coverage (`GS-1` to `GS-4`).
   - **`MIC-FRAME-QUALIFICATION-BOUNDARY`**: Author qualitative boundary elicitation distinguishing model domain from failure regimes. Must preserve non-assessment constraint (`FB-1` to `FB-3`).
2. **Author Representation Bridge for `MIC-FRAME-QUALIFICATION-BOUNDARY` (`REPRESENTATION_BRIDGE_AUTHOR_REQUIRED`)**:
   - Decide whether to author a boundary diagram or certify that this research-boundary note is text-only.
3. **Declare Bucket Conventions (`CONVENTION_GAP`)**:
   - Author formal `bucket.conventions[]` on `BUCKET-VECTOR-REPRESENTATION` declaring positive Cartesian directions ($+x$ right/east, $+y$ up/north) and frame origin.
4. **Obtain Mathematics Provider Review (`EXTERNAL_PROVIDER_REVIEW_REQUIRED`)**:
   - Route `CAP-SIGNED-PAIR-BRIDGE` and `CAP-RIGHT-TRIANGLE-BRIDGE` to Mathematics provider for formal acceptance.
5. **Add Exit Task Data Records (`DATA_GAP`)**:
   - Declare data atoms for components $(5,-2)$ and $(5,2)\text{ m/s}$ in `relative-motion.v1.json#data[]` to bind the magnitude validator to `MIC-SIGNED-COMPONENT` (`ISS-VEC-EXIT-DATA`).
