# Issue #19 subject-content migration note

This note records the subject-content work on PR #23. The branch is stacked directly on
PR #18 by explicit owner override recorded on Issue #19. PR #9 is treated only as a
subject-content donor; no PR #9 Shared-layer history is merged.

## Migrated from PR #9

### Physics — one-dimensional motion

Migrated the useful authored quantitative/model-choice slice around the existing
one-dimensional-motion conceptual spine:

- average speed and average velocity from total distance/displacement and total time;
- motion-graph interpretation;
- constant-acceleration model selection and relations;
- elementary uniform circular motion;
- representative authored Core2A questions and their primary/meaningful-secondary
  capability mappings;
- supporting Physics relations, data, representation/question-family records needed by
  those retained questions.

The resulting matrix closes every present rung to a canonical microtopic and capability.

### Physics — Newton second-law prerequisite slice

Migrated only the prerequisite needed by the retained Work/Energy/Power derivation chain:

- `CAP-NLM-SECOND-LAW`;
- its microtopic and matrix rung;
- the Newton-second-law relation and required mass/acceleration data;
- one representative authored practice question.

This is intentionally a narrow prerequisite migration, not a wholesale import of the
PR #9 Newton-law package.

### Physics — Newton friction and third-law completion

Completed the remaining useful Newton-law donor slice:

- `CAP-NLM-FRICTION` and `MIC-PHY-NLM-FRICTION`;
- `CAP-NLM-THIRD-LAW` and `MIC-PHY-NLM-THIRD-LAW`;
- retained authored Core2A questions for net-zero motion, force-sum reasoning, FBD
  ownership, friction, Second Law, third law and the practical-style Second-Law task;
- donor Core2B frame-choice question remains intentionally omitted because its
  transfer/rubric payload is not faithfully delivered by the current compiler.

The donor friction rung was **not** copied at position 60 because its prerequisite
`CAP-NLM-FBD-BODY-OWNERSHIP` is taught at position 70 on the post-#18 matrix. The
completed post-#18 order is therefore:

`20 net-zero → 45 force-sum → 70 FBD ownership → 78 friction → 86 Second Law → 94 third law → 100 frame choice`.

These positions are local to the Newton matrix only; cross-matrix order still comes
from capability prerequisites.

### Physics — Work / Energy / Power

Migrated the useful authored quantitative/model-choice slice around the existing
work-energy conceptual spine:

- average and instantaneous power;
- kinetic/potential-energy derivation capability;
- quantitative work/energy relation selection;
- representative authored Core2A questions and meaningful capability mappings;
- the relations/data/question-family records required by those retained questions.

The derivation capability carries explicit cross-topic prerequisites into Newton's
Second Law and constant-acceleration kinematics. No cross-matrix ordering is inferred
from ladder positions.

### Physics — Sound

Migrated the scientifically useful authored Sound spine while deliberately holding the
donor's curriculum-specific heritage row:

- sound production by vibration and the role of a material medium;
- longitudinal propagation with particle motion separated from disturbance propagation;
- period/frequency/wavelength/amplitude/speed graph reasoning;
- pitch/loudness/audible-range reasoning;
- reflected-sound timing, echo, reverberation and echolocation;
- five retained authored Core2A questions;
- wave-speed, frequency-period and echo-distance validator support.

The PR #9 Gol Gumbaz/C. V. Raman heritage capability, microtopic, question and matrix
row were **not** migrated because their justification depended on the donor's
`SRC-CBSE-STD` curriculum claim, which is not canonical in that package. This remains
an explicit source-held gap rather than being relabelled as generic authored coverage.

### Physics — Simple Machines

Migrated the authored effort/load tradeoff, mechanical-advantage and machine-comparison
spine:

- three capabilities/microtopics/rungs;
- explicit minimal prerequisite `CAP-MACHINE-TRADEOFF → CAP-WEP-WORK-DIRECTION`;
- mechanical-advantage and ideal work-tradeoff relations;
- two retained authored Core2A questions;
- executable mechanical-advantage validation.

This material is carried as owner extension because the donor's verified curriculum
mapping again relied on a non-canonical `SRC-CBSE-STD` binding.

### Physics — Gravitation and vector practice anchors

The post-#18 branch already carried the relevant canonical Gravitation and vector
capabilities/microtopics, so PR #9 contributed practice rather than new conceptual truth.

Retained Core2A anchors:

- `Q-PHY-GRAV-2A-01` → `CAP-PHY-GRAV-R1` → `MIC-PHY-GRAV-R1`;
- `Q-PHY-VECOPS-2A-01` → `CAP-VEC-SUB-ORDER` → `MIC-PHY-VEC-SUB-ORDER`;
- `Q-PHY-VECREP-2A-01` → `CAP-VECTOR-VS-SCALAR` → `MIC-VECTOR-VS-SCALAR`.

Their donor Core2B companions were intentionally not retained because the current
compiler does not faithfully deliver the donor transfer/rubric payload. Relative Motion
had only a donor Core2B addition, so no new Relative Motion question was imported.

No conceptual rung, capability, curriculum mapping or source authority was added for
these practice-only migrations.

## Mathematics added from current canonical content

PR #9 contains no Mathematics matrix donor for the existing linear-equations package.
The Mathematics work therefore indexes the existing post-#18 canonical package rather
than importing new mathematics.

Added:

- `Mathematics/matrices/linear-equations.rungs.json`;
- exactly three rungs, one for each existing canonical microtopic:
  - equation as a constraint tested by substitution;
  - reversible operations preserving the solution set;
  - exact rational solution versus decimal approximation;
- rung order derived from the existing capability prerequisite chain;
- matrix-only vocabulary ceilings and controlled variation derived from the package's
  existing teaching, diagnostic and boundary examples;
- no new Mathematics capability, relation, question or curriculum claim.

## Intentionally not migrated from PR #9 in this slice

The following PR #9 content is deliberately not imported merely because it exists:

- PR #9 Shared/library, Shared/tools, Shared/roles or other framework changes;
- higher-grade PR #9 deltas in electricity, fluids, magnetism, optics, SHM/waves,
  rigid-body rotation and thermodynamics; their existing post-#18 canonical matrices
  remain untouched in this Grade 9-focused slice unless a real worksheet/source later
  justifies migration;
- PR #9 curriculum mappings that rely on `SRC-CBSE-STD` where the canonical package
  does not itself carry verified source authority;
- donor Core2B question records whose transfer/rubric payloads cannot currently survive
  the post-#18 compiler unchanged;
- any source-custody claim derived from authored questions.

These remain explicit pending work, not fabricated coverage.

## Changes required by post-#18 contracts

The donor content was adapted rather than copied mechanically:

1. **Authority**
   New quantitative Physics material remains `CANDIDATE` and is labelled
   `OWNER_EXTENSION`; unsupported donor curriculum mappings were removed.

2. **Matrix provenance**
   Touched learner-facing Physics rungs backed only by authored canonical resources are
   classified `AUTHORED`, not `SOURCE`.

3. **Gate schema**
   PR #9 gate-relation `validator_refs` are not legal in the post-#18 gate schema.
   Relation authority remains in `Physics/gates/`; executable validator support is
   declared in `Physics/adapter/CoreContracts.json` and implemented in
   `Physics/adapter/validator.py`. Donor falsifiers that tried to mutate the removed
   `validator_refs` field were replaced by executable post-#18 falsifiers that remove a
   Physics-required symbol unit and must raise `SYMBOL_FIELD_MISSING`; validator
   implementation itself is checked separately by the Issue #19 Physics tests.

4. **Compiler delivery**
   Donor Core2B transfer/rubric records that the current compiler cannot faithfully
   deliver were not retained as canonical questions in this slice. Rubric-form answers
   on retained practice questions were represented as compiler-supported model
   responses while preserving the authored reasoning/check content.

5. **Frozen publication runtime**
   Physics publication runtime snapshots were regenerated after the subject adapter
   changed. The repository's republisher confirmed no learner-visible HTML or figure
   changes.

6. **Review state**
   No record was edited to REVIEWED or CURATED. New and materially changed content
   remains CANDIDATE and subject to the repository's digest-bound review/promotion flow.

## Subject-level falsifiers

- `tests/test_issue19_physics_content.py`
  - matrix → microtopic → capability closure;
  - prerequisite resolution and acyclicity;
  - explicit cross-topic prerequisite edges;
  - sparse question mappings and ownership;
  - truthful authored/owner-extension authority;
  - gate/validator implementation;
  - teaching-route closure.

- `tests/test_issue19_mathematics_content.py`
  - matrix closure to the three existing microtopics;
  - explicit capability chain and acyclicity;
  - question → capability → teaching-rung traceability;
  - primary-capability bucket ownership;
  - authored/owner-extension provenance;
  - no learner-specific state in the matrix.

This note describes the current PR #23 slice. Additional Physics donor topics can be
added as separate coherent slices on the same stack after the current guardrails are
green.


## Post-migration prerequisite minimality audit

A human academic pass was added after the structural migration. The audit applies the
Issue #19 rule that a prerequisite must be **true prior knowledge**, not merely useful
sequencing or deeper enrichment.

The resulting corrections keep the graph from over-routing a self-study learner:

- motion-graph interpretation requires average-rate reasoning, while constant-acceleration
  derivation requires motion-graph interpretation;
- uniform circular motion is no longer forced through the unrelated
  zero-velocity/non-zero-acceleration turning-point concept;
- free-body force ownership is treated as a foundational capability rather than requiring
  prior equilibrium/force-sum reasoning;
- work-direction reasoning is foundational inside the WEP spine;
- average power depends on work reasoning, not mechanical-energy conservation;
- routine Grade 9 WEP calculation does not require prior derivation of the energy formulae;
- the energy-derivation branch keeps only the work, Newton-II and constant-acceleration
  capabilities actually used in the derivation;
- simple-machine tradeoff depends on work-direction reasoning rather than the entire
  Grade 9 WEP quantitative/derivation chain.

The detailed counterfactual audit is recorded in
`docs/issue19-prerequisite-audit.md`.
