# Pedagogical Schema Matrix: Physics Subtopic 1 (Relative Motion in a Plane)

**Repository:** `reallaksh19/Grade9V3`  
**Working Source of Truth:** Head of Pull Request #1 (`p0-foundations`, commit `916169a`)  
**Scope:** Subtopic 1 First — `BUCKET-RELATIVE-MOTION` (*Relative velocity in a plane*)

---

## 1. Physics Source and Authority Inventory

Every Physics asset present in PR #1 is inventoried and classified according to repository authority boundaries:

| Source File / Directory | Authority Classification | Supported Microtopics / Assets | Missing Fields / Major Gaps |
| :--- | :--- | :--- | :--- |
| **`Physics/adapter/CoreContracts.json`** | **Governed / Authoritative** | Subject adapter specification: 6 learner products, semantic equation fields, 5 validators (`SPEED_FROM_COMPONENTS`, `CONSTANT_ACCELERATION_*`, `APEX_STATE`), 3 implemented representations (`VECTOR`, `VECTOR_SUBTRACTION`, `GRAPH`), curriculum failure-closed rules. | Does not define teaching content or microtopics. `FREE_BODY_DIAGRAM`, `RAY_DIAGRAM`, `CIRCUIT_SCHEMATIC` are `PROPOSED` only. |
| **`Physics/gates/curriculum-bindings.v1.json`** | **Governed / Authoritative** | Exact curriculum scope authority. Declares `bindings: []` deliberately; all Grade 9 2D vector/relative motion gates fail closed as `OWNER_EXTENSION`. | No binding exists for CBSE Grade 9 2D relative motion. Authority status remains `HELD_INSUFFICIENT_AUTHORITY` / `OWNER_EXTENSION`. |
| **`Physics/gates/motion-vectors.v1.json`** | **Governed / Authoritative** | 6 engineering gates: `PHY-VEC-SCALAR-VECTOR`, `PHY-VEC-AXIS-CONVENTION`, `PHY-VEC-SUBTRACTION`, `PHY-REL-POSITION`, `PHY-REL-VELOCITY`, `PHY-REL-OBSERVER-REVERSAL`. Defines canonical concepts, relations, symbols, validity conditions, reasoning sequences, misconceptions, and difficulty. | Mature at `ENGINEERING` level; author-created, explicit notice: *"No independent scientific or pedagogical review has occurred."* |
| **`Physics/library/relative-motion.v1.json`** | **Library Candidate** (`status: CANDIDATE`) | 1 bucket (`BUCKET-RELATIVE-MOTION`), 3 microtopics (`MIC-SAME-TIME`, `MIC-COMMON-INTERVAL`, `MIC-GEOMETRIC-CHECK`), 2 relations, 1 representation (`REP-REL-VECTOR`), 9 data atoms, full Core1A teaching paths, and full Core1B elicitations. | `bucket.conventions[]` absent; `controlled_experience` not explicitly structured in schema; exit task coordinates in `MIC-SAME-TIME` held under `ISS-REL-EXIT-DATA`. |
| **`Physics/library/vector-representation.v1.json`** | **Library Candidate** (`status: CANDIDATE`) | 1 bucket (`BUCKET-VECTOR-REPRESENTATION`), 4 microtopics (`MIC-VECTOR-VS-SCALAR`, `MIC-SIGNED-COMPONENT`, `MIC-GRAPHICAL-SUBTRACTION`, `MIC-FRAME-QUALIFICATION-BOUNDARY`), 1 relation, 2 representations, 9 data atoms. | `elicitation` is completely `null` across all 4 microtopics (`CORE1B_COVERAGE_GAP`); `bucket.conventions[]` absent. |
| **`Physics/content/relative-motion-g9/`** | **Published Frozen Evidence** | Executable baseline (`baseline.json`), compilation plan (`plan.json`), source atoms (`source.json`), and compiled publication artifacts (`CORE1A.html`, `CORE1B.html`, `CORE2A.html`, `CORE2B.html`, `evidence.json`, `manifest.json` with digest `e27cbd27...`). | `CORE1.html` not generated (was not in `selected_cores` of baseline); questions carry authored provenance rather than official exam citation. |
| **`Physics/candidates/*.v1.json`** *(12 files)* | **Imported Source-Only Candidate** (`packet_authority: NONE`) | 12 broad imported SIL candidate packets (e.g., `phy-kin-1d-motion`, `phy-vec-add-sub`, `phy-nlm-first-law`, `phy-work-energy-power`, etc.). | Zero relations, zero representations, zero data, zero questions, zero capabilities. 204 named gaps recorded in companion `*.gaps.json` files. |

---

## 2. Narrow-Microtopic Census (PR #1 Total)

Broad chapter titles are rejected as matrix rows. Below is the census of all distinct microtopic units present in PR #1:

### A. Library Package: `relative-motion.v1.json` (`BUCKET-RELATIVE-MOTION`) — *Evaluated First*
1. **`MIC-SAME-TIME`**: Position measured from the other object at the same instant ($r_{A/B} = r_A - r_B$).
2. **`MIC-COMMON-INTERVAL`**: From relative position to relative velocity over a shared time interval ($v_{A/B} = v_A - v_B$).
3. **`MIC-GEOMETRIC-CHECK`**: Check direction, magnitude, and observer reversal ($v_{B/A} = -v_{A/B}$).

### B. Library Package: `vector-representation.v1.json` (`BUCKET-VECTOR-REPRESENTATION`)
4. **`MIC-VECTOR-VS-SCALAR`**: Magnitude, vector, and signed component as dual descriptions of one physical entity.
5. **`MIC-SIGNED-COMPONENT`**: Choosing axes freely; once declared, fixing every sign by the chosen axis.
6. **`MIC-GRAPHICAL-SUBTRACTION`**: Vector subtraction as addition of the reversed vector ($P - Q = P + (-Q)$).
7. **`MIC-FRAME-QUALIFICATION-BOUNDARY`**: Research boundary: limits of Galilean velocity subtraction in rotating or non-inertial frames.

### C. Imported Candidate Packets (`Physics/candidates/`, Authority: `NONE`)
*Note: Each carries only 1 broad unconstructed topic label with 0 relations, 0 representations, and 0 data atoms.*
8. `MIC-PHY-KIN-1D-MOTION` *(Candidate packet only; 17 named gaps)*
9. `MIC-PHY-VEC-ADD-SUB` *(Candidate packet only; 17 named gaps)*
10. `MIC-PHY-NLM-FIRST-LAW` *(Candidate packet only; 17 named gaps)*
11. `MIC-PHY-WORK-ENERGY-POWER` *(Candidate packet only; 17 named gaps)*
12. `MIC-PHY-GRAV-UNIVERSAL-LAW` *(Candidate packet only; 17 named gaps)*
13. `MIC-PHY-FLUID-BERNOULLI-EQUATION` *(Candidate packet only; 17 named gaps)*
14. `MIC-PHY-OSC-SHM-WAVES` *(Candidate packet only; 17 named gaps)*
15. `MIC-PHY-THERMO-FIRST-SECOND-LAW` *(Candidate packet only; 17 named gaps)*
16. `MIC-PHY-ELEC-CURRENT-OHM` *(Candidate packet only; 17 named gaps)*
17. `MIC-PHY-MAG-FIELD-LORENTZ` *(Candidate packet only; 17 named gaps)*
18. `MIC-PHY-OPTICS-REFLECTION-MIRRORS` *(Candidate packet only; 17 named gaps)*
19. `MIC-PHY-ROT-RIGID-BODY` *(Candidate packet only; 17 named gaps)*

---

## 3. Canonical Pedagogical Schema Contracts: Subtopic 1 (`BUCKET-RELATIVE-MOTION`)

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
    - bucket.conventions (absent in library JSON; required by CORE1.md)
    - data.atom_binding_for_exit_task (held under ISS-REL-EXIT-DATA)

entry_capability:
  - Signed coordinate-pair arithmetic is available or bridged (CAP-SIGNED-PAIR).
  - Prerequisites: Vector subtraction (PHY-VEC-SUBTRACTION).

target_aha:
  - Replace two independent positions measured from an arbitrary origin by the single physical displacement from B to A (r_A/B = r_A - r_B).

controlled_experience:
  vary: Observer perspective (measuring A relative to B versus B relative to A).
  hold_constant: Simultaneous object positions r_A and r_B relative to common origin O.
  learner_should_notice: The relative displacement arrow reverses direction (180 deg) and both components invert their signs, while the spatial separation distance (magnitude) remains strictly identical.
  source_basis: relative-motion.v1.json#elicitation.boundary_test & gate PHY-REL-POSITION#misconceptions[0]

connections:
  - Common-origin positions r_A, r_B <-> Relative displacement r_A/B.
  - Continuous vector path (Origin -> B -> A) <-> Triangle addition r_A = r_B + r_A/B <-> Algebraic subtraction r_A/B = r_A - r_B.
  - Graphical representation: REP-REL-POSITION (VECTOR kind, requires declared frame, both positions, displacement from B to A, axis units).

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
    - instantaneous_calculus_form (source restricts scope to constant velocity finite differences)

entry_capability:
  - Can construct same-time relative position (MIC-SAME-TIME).
  - Can interpret displacement over elapsed time interval.

target_aha:
  - Subtract two same-time relative position equations at t1 and t2 before dividing by a single, shared time interval (Delta t) to obtain relative velocity.

controlled_experience:
  vary: The relative orientation of velocity vectors (parallel vs. perpendicular motion).
  hold_constant: Individual object speeds (|v_A| = 3 m/s, |v_B| = 4 m/s).
  learner_should_notice: Relative speed is NOT the difference of speeds (4 - 3 != 1 m/s). Components must be subtracted axis by axis over a shared time interval; perpendicular vectors yield sqrt(3^2 + (-4)^2) = 5 m/s.
  source_basis: relative-motion.v1.json#elicitation.predict & gate PHY-REL-VELOCITY#misconceptions[0]

connections:
  - Relative displacement change Delta r_A/B <-> Difference of individual displacements (Delta r_A - Delta r_B).
  - Division by common interval Delta t <-> Relative velocity v_A/B = v_A - v_B.
  - Graphical representation: REP-RELV-RESULTANT (requires declared frame, resultant labelled as relative velocity, common length scale).

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
  model_response: "The relation compares how the simultaneous separation changes over one shared interval. Different intervals describe different displacement changes and do not form this comparison."
  check_step: "For equal constant velocity vectors, separation must remain constant over all Delta t."

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
    - automated_compass_oracle (noted in library oracle: no validator parses compass strings)

entry_capability:
  - Can subtract velocity components algebraically (MIC-COMMON-INTERVAL).
  - Can perform graphical vector subtraction by reversal and tail-to-head addition (MIC-GRAPHICAL-SUBTRACTION).

target_aha:
  - Reconcile algebraic component subtraction with geometric reversal of the observer vector; recognise that observer reversal negates direction but preserves magnitude identically.

controlled_experience:
  vary: Choice of which object vector is reversed in the geometric construction (-v_B versus -v_A).
  hold_constant: Ground velocities v_A and v_B.
  learner_should_notice: Reversing the observer turns the resultant arrow exactly 180 deg (v_B/A = -v_A/B), but the arrow's length and calculated speed remain invariant.
  source_basis: relative-motion.v1.json#elicitation.reconstruct.route & gate PHY-REL-OBSERVER-REVERSAL

connections:
  - Algebraic subtraction v_A/B = v_A - v_B <-> Graphical addition of opposite vector v_A + (-v_B).
  - Vector antisymmetry v_B/A = -(v_A/B) <-> Magnitude invariance |v_B/A| = |v_A/B|.
  - Graphical representation: REP-REL-VECTOR (kind: VECTOR_SUBTRACTION; scene instance SCN-REL-COMPUTE).

misconceptions:
  - wrong_idea: "A correct length is enough for a correct vector answer."
    counterexample: "If v_A/B is (6,-8) m/s pointing southeast, an answer of (6,8) m/s has the same magnitude 10 m/s but points northeast, describing a completely different observation."
    diagnostic: "Would the same arrow reversed describe the same observer statement?"
    repair: "Name the observer, label both components and inspect the direction before taking a magnitude."

boundary_or_check:
  limiting_case: "v_A/B + v_B/A = 0 (sum of mutually observed relative velocities is zero vector)."
  magnitude_invariance: "|v_A/B| = |v_B/A|; squaring components removes negative signs."
  reversal_consistency: "Swapping observer swaps subtraction order, negating every component."

assessment_evidence:
  observable_task: "If v_A/B points southeast, what direction does v_B/A point, and what happens to its magnitude?"
  model_response: "Northwest, with the same magnitude. Swapping subtraction order negates every component, which reverses direction by 180 deg while leaving magnitude unchanged."
  check_step: "Adding v_A/B and v_B/A gives (0,0) m/s."

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

## 4. CORE1 Matrix (Compact Orientation Map)

| Microtopic | Named Objects / Quantities | Essential Convention | Governing Relationship | Meaning in Words | Validity Conditions | Compact Anchor | Hard Transition Pointer | Scope / Exclusion | Authority / Gaps |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`MIC-SAME-TIME`** | $\vec{r}_A$: Position of A ($m$)<br>$\vec{r}_B$: Position of B ($m$)<br>$\vec{r}_{A/B}$: Displacement of A from B ($m$) | Declared origin $O$; parallel Cartesian axes; $+x$ East, $+y$ North. | $\vec{r}_{A/B} = \vec{r}_A - \vec{r}_B$ | The displacement from B to A is what remains after subtracting the position of B. | Both positions taken at the exact same instant; non-rotating axes; classical frame. | With A at $(7,2)\text{ m}$, B at $(3,5)\text{ m}$: $\vec{r}_{A/B} = (4,-3)\text{ m}$. | Transition from origin-based coordinates to observer-based displacement. | **In:** 2D Cartesian plane, same instant.<br>**Out:** Different instants, rotating axes. | `LIBRARY_CANDIDATE`. Grounded in gate `PHY-REL-POSITION`. *Gap:* `bucket.conventions[]` absent in library JSON. |
| **`MIC-COMMON-INTERVAL`** | $\vec{v}_A$: Velocity of A ($\text{m/s}$)<br>$\vec{v}_B$: Velocity of B ($\text{m/s}$)<br>$\vec{v}_{A/B}$: Velocity of A relative to B ($\text{m/s}$)<br>$\Delta t$: Elapsed time ($s$) | Shared time parameter $t$; same time interval $\Delta t$ for both motions. | $\vec{v}_{A/B} = \vec{v}_A - \vec{v}_B$ | For constant velocities, relative position changes at the vector difference of common-frame velocities. | Same observation times; one common interval; parallel non-rotating axes; classical speeds. | $v_A = (6,0)\text{ m/s}$, $v_B = (0,8)\text{ m/s}$ $\implies v_{A/B} = (6,-8)\text{ m/s}$, speed $= 10\text{ m/s}$. | Justifying why division by a *shared* time interval is mandatory rather than subtracting speeds. | **In:** Constant velocities, finite intervals.<br>**Out:** Relativistic speeds, instantaneous calculus limits. | `LIBRARY_CANDIDATE`. Grounded in gate `PHY-REL-VELOCITY`. Validator implemented in adapter. |
| **`MIC-GEOMETRIC-CHECK`** | $\vec{v}_{A/B}$: Velocity of A rel B ($\text{m/s}$)<br>$\vec{v}_{B/A}$: Velocity of B rel A ($\text{m/s}$) | Tail-to-head vector addition; vector reversal ($-\vec{v}$). | $\vec{v}_{B/A} = -(\vec{v}_{A/B})$ | Swapping which object is the observer negates every component of the relative velocity vector. | Both evaluated in same frame at same instant; classical velocities. | $v_{A/B} = (6,-8)\text{ m/s}$ (SE) $\implies v_{B/A} = (-6,8)\text{ m/s}$ (NW), both speed $10\text{ m/s}$. | Separating vector direction (negated) from scalar magnitude (invariant). | **In:** Graphical reversal and component antisymmetry.<br>**Out:** Accelerating observers, Coriolis effects. | `LIBRARY_CANDIDATE`. Grounded in gate `PHY-REL-OBSERVER-REVERSAL`. Representation `REP-REL-VECTOR`. |

---

## 5. CORE1A Matrix (Declarative Detailed Teaching)

| Microtopic | Entry Capability | Target Inferential Jump | Controlled Experience (Vary / Hold / Notice) | Completed Teaching Construction (Steps & Roles) | Why-Valid Obligations | Required Representation Bridge | Misconception & Diagnostic | Repair | Independent Check | Exit Evidence | Authority / Gaps |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`MIC-SAME-TIME`** | `CAP-SIGNED-PAIR`: Signed coordinate-pair arithmetic. | Replace two origin positions by the displacement from B to A. | **Vary:** Observer choice (A rel B vs B rel A).<br>**Hold:** Positions $\vec{r}_A, \vec{r}_B$.<br>**Notice:** Arrow flips $180^\circ$, signs invert, length is invariant. | **Step 1 (TRANSFORM):** Follow path $O \to B \to A$ yielding $\vec{r}_A = \vec{r}_B + \vec{r}_{A/B}$.<br>**Step 2 (TRANSFORM):** Subtract $\vec{r}_B$ from both sides: $\vec{r}_{A/B} = \vec{r}_A - \vec{r}_B$. | Displacements add along consecutive paths; subtracting identical vector preserves equality. | Diagram showing $O$, $\vec{r}_A$, $\vec{r}_B$, and directed vector from $B$ to $A$ (`REP-REL-POSITION`). | **Wrong:** Subtract whichever coordinate is written first.<br>**Diag:** "Which displacement carries you from B to A?" | Draw path $O \to B \to A$, write $\vec{r}_A = \vec{r}_B + \vec{r}_{A/B}$, then isolate $\vec{r}_{A/B}$. | Add $\vec{r}_{A/B}$ to $\vec{r}_B$ to recover $\vec{r}_A$. | At one instant A is at $(7,2)$ and B at $(3,5)$. Give A rel B and explain signs $\to (4,-3)\text{ m}$. | Library candidate; gate `PHY-REL-POSITION`. *Gap:* Coordinates in exit task lack data atom ID (`ISS-REL-EXIT-DATA`). |
| **`MIC-COMMON-INTERVAL`** | `MIC-SAME-TIME`: Can construct relative position. | Subtract two relative-position equations before dividing by a common time interval. | **Vary:** Velocity orientation (parallel vs orthogonal).<br>**Hold:** Individual speeds ($3, 4\text{ m/s}$).<br>**Notice:** Relative speed is not scalar difference; components must be subtracted over shared $\Delta t$. | **Step 1 (DECLARE):** Write relative position at $t_1$ and $t_2$.<br>**Step 2 (TRANSFORM):** Group displacement changes: $\Delta \vec{r}_{A/B} = \Delta \vec{r}_A - \Delta \vec{r}_B$.<br>**Step 3 (TRANSFORM):** Divide each term by common $\Delta t$.<br>**Step 4 (DECLARE):** Equate average to constant velocity: $\vec{v}_{A/B} = \vec{v}_A - \vec{v}_B$. | Same relation applies at both instants; subtraction distributes; quotient over non-zero interval yields average velocity. | Resultant vector diagram (`REP-RELV-RESULTANT`) showing $\vec{v}_A$, $\vec{v}_B$, and $\vec{v}_{A/B}$. | **Wrong:** Subtracting speeds gives relative speed.<br>**Diag:** "If one moves east and other north, do directions disappear?" | Compute signed vector components first, then take magnitude if requested. | For equal velocity vectors ($\vec{v}_A = \vec{v}_B$), separation must remain constant. | Explain why both displacement changes must be divided by the same time interval in the derivation. | Library candidate; gate `PHY-REL-VELOCITY`. Validated by `SPEED_FROM_COMPONENTS`. |
| **`MIC-GEOMETRIC-CHECK`** | `MIC-COMMON-INTERVAL` & `MIC-GRAPHICAL-SUBTRACTION`. | Reconcile algebraic subtraction with reversal of observer vector in geometric construction. | **Vary:** Which observer arrow is reversed ($-\vec{v}_B$ vs $-\vec{v}_A$).<br>**Hold:** Ground velocities $\vec{v}_A, \vec{v}_B$.<br>**Notice:** Resultant reverses direction by $180^\circ$ but magnitude is unchanged. | **Step 1 (TRANSFORM):** Reverse $\vec{v}_B \to -\vec{v}_B$.<br>**Step 2 (TRANSFORM):** Add $\vec{v}_A$ and $-\vec{v}_B$ tail-to-head.<br>**Step 3 (VERIFY):** Compare components and reverse observer order: $\vec{v}_{B/A} = -(\vec{v}_{A/B})$. | Subtraction is addition of opposite vector; free vectors translate without rotation; opposite vectors have equal lengths. | Scene instance `SCN-REL-COMPUTE` on `REP-REL-VECTOR` (kind: `VECTOR_SUBTRACTION`). | **Wrong:** Correct length is enough for vector answer.<br>**Diag:** "Would the same arrow reversed describe same observation?" | Name observer, label both components and inspect direction before taking magnitude. | Vector sum $\vec{v}_{A/B} + \vec{v}_{B/A} = \vec{0}$. | If $\vec{v}_{A/B}$ points SE, what direction does $\vec{v}_{B/A}$ point and what happens to its magnitude? | Library candidate; gate `PHY-REL-OBSERVER-REVERSAL`. Scene instance compiled and verified. |

---

## 6. CORE1B Matrix (Conceptual Reconstruction & Self-Tutor)

| Microtopic | Target Understanding | 1. Predict (Prompt & Defensible Answer) | 2. Attempt (Produces & Rubric Closure) | 3. Reconstruct Route (Guided Prompts) | 4. Diagnose (Plausible Wrong Answer) | 5. Repair (Action Following Error) | 6. Boundary Test (Prompt & Confirms) | Core1A Correspondence | Authority / Gaps |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`MIC-SAME-TIME`** | Displacement from B to A is independent of origin and reverses when observer swaps. | **Prompt:** A is at $(7,2)$ and B at $(3,5)$. Predict walk direction from B to A without subtracting.<br>**Answer:** East and South. A is further east and lower north than B. | **Produces:** Sketch of $O, B, A$ with arrow from $B$ to $A$ and predicted component signs.<br>**Closure (Rubric):** Tail at B; signs read off sketch before subtraction. Accepted/Rejected examples declared. | **Route:**<br>1. Trace finger $O \to B \to A$.<br>2. Write trip as one journey: $\vec{r}_A = \vec{r}_B + \vec{r}_{A/B}$.<br>3. Isolate $\vec{r}_{A/B}$ by subtracting $\vec{r}_B$.<br>4. Compare signs with initial prediction. | **Wrong:** Subtract whichever coordinate appears first in prompt, ignoring observer tail. | Redraw path from observer tail to target head; reconstruct vector sum before subtracting. | **Prompt:** Give B relative to A for same positions. What changed and what did not?<br>**Answer:** $(-4,3)\text{ m}$; components negated, magnitude unchanged.<br>**Confirms:** Order is carried by vector, not first written number. | Exact 1:1 match with Core1A `MIC-SAME-TIME` construction. | Library candidate; fully populated in `relative-motion.v1.json#elicitation`. |
| **`MIC-COMMON-INTERVAL`** | Relative velocity requires subtracting components over shared interval, not subtracting speeds. | **Prompt:** A moves east at $3\text{ m/s}$, B north at $4\text{ m/s}$. Predict relative speed and say if $4 - 3$ gives it.<br>**Answer:** $5\text{ m/s}$, and no. Motions are at right angles; subtracting speeds throws away direction. | **Produces:** Relative velocity as signed components, then magnitude, explicitly distinguishing velocity from speed.<br>**Closure (Rubric):** Axis-by-axis subtraction before magnitude; labels velocity vs speed. | **Route:**<br>1. Write relative position at start and end of 1 second.<br>2. Subtract the two positions.<br>3. Divide by shared interval $\Delta t = 1\text{ s}$.<br>4. Re-evaluate components vs initial prediction. | **Wrong:** $4 - 3 = 1\text{ m/s}$ (scalar speed subtraction fallacy). | Recompute signed components in declared frame, then take vector magnitude $\sqrt{v_x^2 + v_y^2}$. | **Prompt:** A and B both walk east at $5\text{ m/s}$. What is $\vec{v}_{A/B}$ and what does B see?<br>**Answer:** $(0,0)\text{ m/s}$. B sees A stationary at fixed distance.<br>**Confirms:** Relative velocity is about separation changing, not ground motion. | Exact 1:1 match with Core1A `MIC-COMMON-INTERVAL` derivation. | Library candidate; fully populated in `relative-motion.v1.json#elicitation`. |
| **`MIC-GEOMETRIC-CHECK`** | Reversing observer reverses vector direction by $180^\circ$ while keeping magnitude invariant. | **Prompt:** $\vec{v}_{A/B}$ is SE at $5\text{ m/s}$. Predict $\vec{v}_{B/A}$ direction and size without calculation.<br>**Answer:** Northwest at $5\text{ m/s}$. Swapping observer reverses arrow, leaving length alone. | **Produces:** Both arrows drawn on one sketch, with observer named beside each and lengths compared.<br>**Closure (Rubric):** Observer named on each arrow; lengths stated equal without recalculating. | **Route:**<br>1. Draw $\vec{v}_A$ and $\vec{v}_B$ from common point.<br>2. Reverse $\vec{v}_B$ and add tail-to-head.<br>3. Reverse observer: redraw by reversing $\vec{v}_A$.<br>4. Verify resultant arrows are opposite and equal length. | **Wrong:** Offering scalar magnitude alone ($5\text{ m/s}$) as the complete relative velocity answer. | State the observer explicitly, assign signed components, and verify heading on coordinate grid. | **Prompt:** What does $\vec{v}_{A/B} + \vec{v}_{B/A}$ equal geometrically and numerically?<br>**Answer:** $\vec{0}$; two equal and opposite vectors cancel.<br>**Confirms:** Complete antisymmetry of observer reversal. | Exact 1:1 match with Core1A `MIC-GEOMETRIC-CHECK` graphical check. | Library candidate; fully populated in `relative-motion.v1.json#elicitation`. |

---

## 7. Cross-Core Correspondence Matrix

| Microtopic | Core1 Role | Core1A Role | Core1B Role | A/B Differentiated? | Coverage Complete? | Authority Sufficient? |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`MIC-SAME-TIME`** | Compact map: naming $\vec{r}_A, \vec{r}_B, \vec{r}_{A/B}$, governing equation, same-time validity condition, anchor values. | Declarative instruction: reveals completed $O \to B \to A$ path proof, why-valid justifications, and diagnostic. | Conceptual self-tutor: learner predicts walk direction first, sketches arrow, traces finger route, boundary tests reversal. | **PASS** | **PASS** | **CANDIDATE** (Grounded in engineering gate `PHY-REL-POSITION`; curriculum binding held as `OWNER_EXTENSION`). |
| **`MIC-COMMON-INTERVAL`** | Compact map: naming velocities, shared interval relation $\vec{v}_{A/B} = \vec{v}_A - \vec{v}_B$, constant velocity condition. | Declarative instruction: reveals 4-step derivation grouping displacement changes over shared $\Delta t$. | Conceptual self-tutor: learner predicts right-angle outcome first, calculates components, boundary tests zero-velocity limit. | **PASS** | **PASS** | **CANDIDATE** (Grounded in engineering gate `PHY-REL-VELOCITY`; verified by `SPEED_FROM_COMPONENTS`). |
| **`MIC-GEOMETRIC-CHECK`** | Compact map: antisymmetry relation $\vec{v}_{B/A} = -(\vec{v}_{A/B})$, graphical reversal convention. | Declarative instruction: reveals vector reversal and tail-to-head geometric construction (`SCN-REL-COMPUTE`). | Conceptual self-tutor: learner predicts opposite vector, draws both arrows with named observers, checks cancellation. | **PASS** | **PASS** | **CANDIDATE** (Grounded in engineering gate `PHY-REL-OBSERVER-REVERSAL`; scene instance verified in publication). |

---

## 8. Gap Report

1. **`AUTHORITY_GAP`**: `Physics/gates/curriculum-bindings.v1.json` declares `bindings: []`. CBSE Grade 9 2D relative motion gates fail closed as `OWNER_EXTENSION` (`HELD_INSUFFICIENT_AUTHORITY`).
2. **`SOURCE_GAP`**: In `MIC-SAME-TIME`, coordinates $(7,2)\text{ m}$ and $(3,5)\text{ m}$ live in exit task text rather than as declared data atoms with unit and dimension (`ISS-REL-EXIT-DATA`).
3. **`CONTROLLED_EXPERIENCE_GAP`**: `package.schema.json` lacks an explicit `controlled_experience` field; cognitive experiments were derived from `boundary_test`, `predict`, and gate counterexamples.
4. **`REPRESENTATION_BRIDGE_GAP`**: `Shared/roles/CORE1.md` mandates `bucket.conventions[]`, which is absent in `relative-motion.v1.json`.
5. **`CLOSURE_GAP`**: `MIC-GEOMETRIC-CHECK` exit answer requires a compass direction ("Northwest"); no subject validator returns compass directions, so closure relies on `CHECKED_BY_AUTHOR`.
