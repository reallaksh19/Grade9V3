# Question → Study Map Benchmark Gap Ledger

Baseline: `e6f9ccce4a2ecbba8764bfa5cd5e877830afa56d`

This file is the factual ledger produced by the benchmark agent. It records observed symptoms only. Root-cause analysis remains reserved for the maintainer phase.

## GAP-QSM-0001 — no retained canonical question for seven mapped matrices

- Subject: Physics
- Matrix/subtopic: `MATRIX-PHY-ELEC-CURRENT-OHM`, `MATRIX-PHY-FLUID-BERNOULLI-EQUATION`, `MATRIX-PHY-MAG-FIELD-LORENTZ`, `MATRIX-PHY-OPTICS-REFLECTION-MIRRORS`, `MATRIX-PHY-OSC-SHM-WAVES`, `MATRIX-PHY-ROT-RIGID-BODY`, `MATRIX-PHY-THERMO-FIRST-SECOND-LAW`
- Benchmark case: Direct-ready question
- Severity: MEDIUM
- Observed status: PARTIAL
- Expected: A representative retained question should allow direct question-demand → capability → teaching-location evaluation.
- Observed: Each listed package has `questions: []`. The benchmark can inspect canonical capabilities/microtopics and use a synthetic mapping falsifier, but cannot claim a retained real/canonical question-demand mapping for that subtopic.
- Reproduction: Inspect the `questions` collection in each listed `Physics/library/*.v1.json` package.
- Evidence: Each corresponding benchmark pack records `direct_mapping: PARTIAL` and names the exact package.
- Affected question/capability/microtopic refs: no retained question refs; representative mapped capability refs are recorded in the individual packs.
- Likely layer: CONTENT
- Confidence in layer guess: MEDIUM
- Cross-subtopic recurrence: CONFIRMED across 7 Physics matrices
- Benchmark-agent note: This does not prove source custody is the root cause; it only records the absence of retained question inventory for direct demand benchmarking.
- Analysis status: UNANALYSED
- Fix status: NOT_STARTED

## GAP-QSM-0002 — unresolved matrix rungs leave nine subtopics only partially teachable

- Subject: Physics
- Matrix/subtopic: 9 Physics matrices listed below
- Benchmark case: Content gap
- Severity: HIGH
- Observed status: PARTIAL
- Expected: Every rung needed for a usable subtopic route should resolve to durable canonical teaching, or the missing teaching must remain explicit and block readiness.
- Observed: The system correctly leaves the gaps explicit and keeps the matrices `NOT_READY`, but the learner cannot obtain a complete subtopic route.
- Reproduction:
  - `MATRIX-PHY-ELEC-CURRENT-OHM`: R2, R3, R5, R6, R7 have no `microtopic_ref`.
  - `MATRIX-PHY-FLUID-BERNOULLI-EQUATION`: R1, R5 have no `microtopic_ref`.
  - `MATRIX-PHY-GRAV-UNIVERSAL-LAW`: R2, R3 have no `microtopic_ref`.
  - `MATRIX-PHY-MAG-FIELD-LORENTZ`: R3, R5, R6 have no `microtopic_ref`.
  - `MATRIX-PHY-OPTICS-REFLECTION-MIRRORS`: R4, R5, R6 have no `microtopic_ref`.
  - `MATRIX-PHY-OSC-SHM-WAVES`: R2, R3, R5 have no `microtopic_ref`.
  - `MATRIX-PHY-ROT-RIGID-BODY`: R2 has no `microtopic_ref`.
  - `MATRIX-PHY-THERMO-FIRST-SECOND-LAW`: R2 has no `microtopic_ref`.
  - `MATRIX-PHY-VEC-ADD-SUB`: R1, R2, R4 have no `microtopic_ref`.
- Evidence: The frozen matrix files plus `docs/SESSION-READINESS-REPORT.md`; individual benchmark packs record the exact missing rungs.
- Affected question/capability/microtopic refs: matrix rungs above; exact represented capability refs are retained in their packs.
- Likely layer: CONTENT
- Confidence in layer guess: HIGH
- Cross-subtopic recurrence: CONFIRMED across 9 Physics matrices
- Benchmark-agent note: The benchmark does not add the missing microtopics and does not weaken readiness.
- Analysis status: UNANALYSED
- Fix status: NOT_STARTED

## GAP-QSM-0003 — vector add/sub prerequisite delivery is ambiguous

- Subject: Physics
- Matrix/subtopic: `MATRIX-PHY-VEC-ADD-SUB` / Vector addition, subtraction and orientation
- Benchmark case: Prerequisite route
- Severity: HIGH
- Observed status: PARTIAL
- Expected: `CAP-VEC-SUB-ORDER -> CAP-GRAPHICAL-SUBTRACT` should resolve to one usable prerequisite teaching destination or an explicit bridge/unresolved state.
- Observed: The current session-readiness report states that this matrix contains a prerequisite resolving to more than one canonical teaching location; the matrix remains `NOT_READY`.
- Reproduction: Inspect `CAP-VEC-SUB-ORDER.prerequisite_refs` in `Physics/library/phy-vec-add-sub.v1.json`, then compare with the readiness result in `docs/SESSION-READINESS-REPORT.md`.
- Evidence: `Physics/library/phy-vec-add-sub.v1.json`; `docs/SESSION-READINESS-REPORT.md`; vector-add/sub benchmark pack.
- Affected question/capability/microtopic refs: `CAP-VEC-SUB-ORDER`, `CAP-GRAPHICAL-SUBTRACT`, `MIC-PHY-VEC-SUB-ORDER`.
- Likely layer: UNKNOWN
- Confidence in layer guess: LOW
- Cross-subtopic recurrence: UNKNOWN
- Benchmark-agent note: Do not infer whether the defect is duplicate content, resolver semantics or intended provider structure until maintainer analysis reproduces the ambiguity.
- Analysis status: UNANALYSED
- Fix status: NOT_STARTED

## GAP-QSM-0004 — vector representation lacks reconstruction-route coverage

- Subject: Physics
- Matrix/subtopic: `MATRIX-PHY-VECTOR-REPRESENTATION` / Vector representation and subtraction
- Benchmark case: Repair
- Severity: HIGH
- Observed status: PARTIAL
- Expected: A self-study-ready repair route should be able to move from diagnosed misconception into the intended Core1B/Core1A reconstruction/teaching path for each matrix teaching microtopic.
- Observed: The three matrix teaching microtopics have teaching paths, misconceptions and exit tasks, but no `elicitation` block; the package also has zero `teaching_routes`. The readiness snapshot therefore remains `PILOT_READY`, not `SESSION_READY`.
- Reproduction: Inspect `MIC-VECTOR-VS-SCALAR`, `MIC-SIGNED-COMPONENT`, and `MIC-GRAPHICAL-SUBTRACTION` in `Physics/library/vector-representation.v1.json` and compare with `docs/SESSION-READINESS-REPORT.md`.
- Evidence: `Physics/library/vector-representation.v1.json`; `docs/SESSION-READINESS-REPORT.md`; vector-representation benchmark pack.
- Affected question/capability/microtopic refs: `MIC-VECTOR-VS-SCALAR`, `MIC-SIGNED-COMPONENT`, `MIC-GRAPHICAL-SUBTRACTION`.
- Likely layer: CONTENT
- Confidence in layer guess: HIGH
- Cross-subtopic recurrence: UNKNOWN
- Benchmark-agent note: The benchmark does not add elicitation routes or promote the matrix to ready.
- Analysis status: UNANALYSED
- Fix status: NOT_STARTED

## Sweep summary

- Matrices benchmarked: 17 / 17.
- Material gap families recorded: 4.
- Production repairs performed by benchmark agent: 0.
- `ANALYSIS.md` modified by benchmark agent: no.
