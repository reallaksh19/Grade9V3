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
- explicit prerequisite `CAP-MACHINE-TRADEOFF → CAP-WEP-GRADE9-QUANT`;
- mechanical-advantage and ideal work-tradeoff relations;
- two retained authored Core2A questions;
- executable mechanical-advantage validation.

This material is carried as owner extension because the donor's verified curriculum
mapping again relied on a non-canonical `SRC-CBSE-STD` binding.

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
- friction and Newton's third-law donor material;
- additional vector/other Physics donor content not yet reviewed as the next coherent
  slice;
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
   `Physics/adapter/validator.py`.

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
