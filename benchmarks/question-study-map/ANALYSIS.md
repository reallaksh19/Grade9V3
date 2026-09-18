# Reverse-engineering analysis notes

Baseline benchmark sweep: `e6f9ccce4a2ecbba8764bfa5cd5e877830afa56d`  
Merged benchmark sweep: PR #52  
Analysis branch: `analysis/question-study-map-gaps`

This file contains maintainer analysis only. No production/runtime/content repair is included
in this branch.

The analysis starts from the four gap families recorded by the independent benchmark sweep
and works backwards from observed behavior to the smallest durable defect.

## Executive clustering

The four benchmark gaps collapse into three root-cause classes:

1. **Content inventory / evidence coverage**
   - GAP-QSM-0001
   - some mapped subtopics have no retained canonical question inventory.

2. **Deliberately incomplete subject-content migration**
   - GAP-QSM-0002
   - nine Physics matrices contain skeleton rungs that were never given canonical teaching
     microtopics.

3. **Legacy Vector Representation content model**
   - GAP-QSM-0003
   - GAP-QSM-0004
   - one broad capability spans two distinct matrix rungs, creating two local teaching
     locations; the same package also predates the current Core1B elicitation/teaching-route
     contract.

The benchmark does **not** currently show a general learner-evidence, feedback, scheduler or
renderer defect.

The most important conclusion is that GAP-QSM-0003 should **not** be fixed by weakening the
Shared delivery resolver. The ambiguity is useful evidence that the current capability
granularity is wrong for self-study/evidence routing.

---

## ANALYSIS-GAP-QSM-0001

- Gap: Seven mapped Physics matrices have no retained canonical question inventory for a
  direct question-demand benchmark.
- Reproduced: YES
- Cross-subtopic occurrences:
  - `MATRIX-PHY-ELEC-CURRENT-OHM`
  - `MATRIX-PHY-FLUID-BERNOULLI-EQUATION`
  - `MATRIX-PHY-MAG-FIELD-LORENTZ`
  - `MATRIX-PHY-OPTICS-REFLECTION-MIRRORS`
  - `MATRIX-PHY-OSC-SHM-WAVES`
  - `MATRIX-PHY-ROT-RIGID-BODY`
  - `MATRIX-PHY-THERMO-FIRST-SECOND-LAW`
- Confirmed layer: CONTENT / QUESTION INVENTORY
- Root cause:
  These packages were migrated primarily as capability/microtopic/matrix teaching structures.
  They currently contain no retained question records, so the benchmark cannot exercise a
  real/canonical question → capability → teaching-location path for those subtopics.
- Why this is the root cause:
  The benchmark can still inspect matrix/capability topology and can use synthetic mapping
  falsifiers. The missing artifact is specifically representative retained question demand,
  not a failure of worksheet routing or capability resolution.
- Smallest durable fix:
  **No blanket fix.** Do not create token questions merely to improve benchmark coverage.
  When a subtopic becomes active because of a real worksheet, source bank or deliberate
  study selection, retain a small representative question inventory with truthful
  provenance and normal primary/secondary capability mapping.
- Files/contracts likely affected:
  Subject `<subject>/library/*.json` question/family records only when real demand is
  selected. No Shared contract change is indicated.
- Content migration required:
  Demand-driven only. None for dormant subtopics.
- Regression benchmark:
  For an activated subtopic, at least one retained question must trace:
  `question → primary capability → prerequisite closure → canonical teaching location`
  without changing capability truth merely to fit the question.
- Risks / anti-drift constraints:
  - Do not manufacture questions to satisfy the benchmark.
  - Do not label authored practice as source custody.
  - Do not require every matrix to have a large local question bank.
  - Exit tasks may remain useful verification even when source-backed Core2 inventory is thin.
- Decision:
  Treat as an **inventory/evidence backlog**, not a core defect and not an immediate global
  repair.
- Fix PR:
  NONE YET — create per-subtopic content PR only when demand activates the subtopic.
- Re-benchmark result:
  PENDING future activated-subtopic work.

---

## ANALYSIS-GAP-QSM-0002

- Gap: Nine Physics matrices contain unresolved rungs with no canonical `microtopic_ref`.
- Reproduced: YES
- Cross-subtopic occurrences:
  - Electricity: R2, R3, R5, R6, R7
  - Fluids/Bernoulli: R1, R5
  - Gravitation: R2, R3
  - Magnetism/induction: R3, R5, R6
  - Reflection/mirrors: R4, R5, R6
  - SHM/waves: R2, R3, R5
  - Rotational dynamics: R2
  - Thermodynamics: R2
  - Vector add/sub: R1, R2, R4
- Confirmed layer: CONTENT
- Root cause:
  The Issue #19 content migration intentionally preserved several matrix skeletons whose
  durable rung intent was useful, but whose canonical teaching microtopics were not yet
  authored/migrated. The readiness layer is correctly refusing to call those matrices ready.
- Why this is the root cause:
  The missing object is explicit in each matrix: the affected rungs have no
  `microtopic_ref`. The runtime is not losing or misrouting an existing teaching record;
  the teaching record does not exist yet.
- Smallest durable fix:
  Complete only the rungs justified by real worksheet demand, genuine prerequisites,
  explicit syllabus scope or an owner-approved extension.
- Files/contracts likely affected:
  Subject library + matrix files for the selected subtopic. Shared/runtime/schema changes are
  not indicated.
- Content migration required:
  YES, but selectively.
- Regression benchmark:
  For each completed rung:
  - matrix rung resolves to one canonical microtopic;
  - microtopic resolves to one suitably granular capability;
  - prerequisite closure is acyclic and unambiguous;
  - self-study support is present at the level required by session readiness;
  - at least one real/retained question can reuse the capability where genuine demand exists.
- Risks / anti-drift constraints:
  - Do not fill all nine matrices simply to obtain green readiness counts.
  - Do not create one capability per question.
  - Do not copy syllabus chapter structure mechanically into the capability graph.
  - Do not weaken `NOT_READY` to hide missing teaching.
- Decision:
  Maintain as a **demand-driven content backlog**.
  The first justified target is Vector Addition/Decomposition because the owner-supplied
  NEETPrep Relative Motion bank already exposes this missing prerequisite in river-crossing
  questions Q4/Q5.
- Fix PR:
  FUTURE CONTENT PR — Vector Addition/Decomposition first.
- Re-benchmark result:
  PENDING.

---

## ANALYSIS-GAP-QSM-0003

- Gap: Vector add/sub prerequisite delivery is reported as ambiguous.
- Reproduced: YES, by tracing the current canonical records and Shared resolver semantics.
- Cross-subtopic occurrences:
  Confirmed on the Vector Add/Sub prerequisite closure. No evidence yet that the same defect
  occurs in another matrix.
- Confirmed layer: CONTENT MODEL / CAPABILITY GRANULARITY
- Root cause:
  `CAP-VECTOR-VS-SCALAR` currently combines two distinct learner actions:
  1. distinguish vector from scalar magnitude;
  2. read signed vector components against declared axes.

  The Vector Representation matrix teaches those as two separate rungs:
  - R1 → `MIC-VECTOR-VS-SCALAR`
  - R2 → `MIC-SIGNED-COMPONENT`

  Both microtopics declare the same primary capability,
  `CAP-VECTOR-VS-SCALAR`.

  Therefore `study_map.capability_locations(...)` correctly discovers two local teaching
  locations for one capability. The subject-neutral `capability_delivery.resolve(...)`
  classifies any capability with more than one local teaching location as `AMBIGUOUS`.

  This ambiguity then appears in the prerequisite closure for
  `CAP-VEC-SUB-ORDER`, because:
  `CAP-VEC-SUB-ORDER → CAP-GRAPHICAL-SUBTRACT → CAP-VECTOR-VS-SCALAR`.
- Why this is the root cause:
  The two locations are not duplicate files accidentally discovered by the resolver. They are
  deliberate, different matrix rungs representing different cognitive work. A single learner
  evidence key cannot cleanly say whether the learner owns only vector/scalar distinction or
  also signed-component reading.
- Smallest durable fix:
  Split the broad capability so the matrix rungs have distinct primary learner actions.

  Conceptually:
  - keep a capability for vector-vs-scalar/magnitude distinction at R1;
  - introduce a separate signed-component / declared-axis capability at R2;
  - make graphical subtraction depend on the signed-component capability (plus the
    right-triangle bridge only where magnitude is genuinely required);
  - update question/family secondary mappings only where they actually depend on the new
    capability.

  **Do not change Shared `capability_delivery.resolve` to treat multiple local locations as
  automatically valid.** That would hide genuinely duplicated/competing teaching ownership
  elsewhere and would preserve learner-evidence ambiguity.
- Files/contracts likely affected:
  - `Physics/library/vector-representation.v1.json`
  - `Physics/matrices/vector-representation.rungs.json`
  - `Physics/library/phy-vec-add-sub.v1.json`
  - affected Physics-specific tests/benchmark expectations
  No Shared resolver change should be necessary.
- Content migration required:
  YES.
- Regression benchmark:
  - each Vector Representation rung has one primary capability at the intended granularity;
  - `CAP-VEC-SUB-ORDER` prerequisite closure resolves without
    `READINESS_PREREQUISITE_AMBIGUOUS`;
  - R1 evidence does not imply R2 signed-component competence;
  - a real river-crossing/vector question can reuse the signed-component/vector-composition
    prerequisite without inventing a question-specific capability.
- Risks / anti-drift constraints:
  - Do not introduce aliases that leave the old broad capability as a second owner.
  - Do not weaken ambiguity detection globally.
  - Preserve stable meaning for existing learner observations if any exist; migrate refs
    explicitly rather than silently reinterpreting old evidence.
  - Do not conflate the Mathematics signed-pair bridge with the Physics act of reading a
    physical vector's signed components.
- Decision:
  Treat as a **content-model repair**, not a Shared runtime repair.
- Fix PR:
  FUTURE CONTENT-MODEL PR, preferably combined with GAP-QSM-0004 because both concern the
  same legacy Vector Representation package.
- Re-benchmark result:
  PENDING.

---

## ANALYSIS-GAP-QSM-0004

- Gap: Vector Representation lacks reconstruction-route coverage.
- Reproduced: YES
- Cross-subtopic occurrences:
  Current benchmark evidence identifies this package specifically; no broader Shared failure
  is established.
- Confirmed layer: CONTENT
- Root cause:
  `Physics/library/vector-representation.v1.json` predates the current self-tutor
  readiness contract. Its three matrix teaching microtopics have teaching paths,
  misconceptions and exit tasks, but:
  - the microtopics have no complete `elicitation` cycle;
  - the package has zero `teaching_routes`.

  Session readiness therefore correctly keeps the matrix at `PILOT_READY`.
- Why this is the root cause:
  The Shared readiness rule succeeds on other packages with the same runtime. The missing
  records are local to Vector Representation.
- Smallest durable fix:
  Migrate the three Vector Representation teaching rungs to the current Core1A/Core1B
  content contract:
  - Core1A route for declarative/worked teaching;
  - Core1B route with Predict → Attempt → Reconstruct → Diagnose/Repair → Boundary Test;
  - keep existing misconceptions/exit tasks and reuse them rather than authoring parallel
    truth.
- Files/contracts likely affected:
  `Physics/library/vector-representation.v1.json` and Physics-specific tests/benchmark
  expectations.
- Content migration required:
  YES.
- Regression benchmark:
  - all intended Vector Representation rungs have Core1A + Core1B coverage;
  - each Core1B microtopic has complete elicitation;
  - readiness no longer emits
    `READINESS_CORE1A_ROUTE_MISSING` / `READINESS_CORE1B_ROUTE_MISSING`;
  - repair remains targeted to the diagnosed capability;
  - fresh verification remains independent of the repaired example.
- Risks / anti-drift constraints:
  - Do not create a second teaching ontology beside existing microtopics.
  - Do not change capability truth merely to satisfy renderer/readiness wording.
  - Do not claim academic review/source custody from authoring these routes.
- Decision:
  Combine with GAP-QSM-0003 as one **Vector Representation modernization** PR so capability
  granularity and self-tutor routes are corrected together.
- Fix PR:
  FUTURE VECTOR REPRESENTATION MODERNIZATION PR.
- Re-benchmark result:
  PENDING.

---

## Fix-order decision

Do not repair in numeric gap order.

Recommended repair sequence after this analysis is reviewed:

1. **Vector Representation modernization**
   - resolves GAP-QSM-0003;
   - resolves GAP-QSM-0004;
   - establishes clean vector prerequisites for Motion in a Plane.

2. **Vector Addition/Decomposition content completion**
   - addresses the highest-value slice of GAP-QSM-0002;
   - directly supported by real NEETPrep river-crossing demand.

3. **Re-benchmark Relative Motion + Vector Representation + Vector Add/Sub**
   - ensure the learner-facing route remains honest;
   - ensure no new capability-location ambiguity appears.

4. **Leave the remaining GAP-QSM-0002 matrices demand-gated**
   - complete them only when a real worksheet/syllabus need activates them.

5. **Leave GAP-QSM-0001 as an evidence/inventory backlog**
   - add representative questions only when real demand/source custody justifies them.

## Core architecture conclusion

The benchmark sweep does not justify a new core subsystem.

One observed ambiguity that initially looked like a resolver problem is better explained by a
too-broad content capability spanning two distinct matrix rungs. The Shared ambiguity guard is
therefore protecting the architecture and should remain strict.

The next repair should be a small, explicit Physics content-model migration, followed by a
full benchmark rerun before any further repair.
