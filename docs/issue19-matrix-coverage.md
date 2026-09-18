# Issue #19 matrix coverage report

This report covers the matrices materially changed or added in the current PR #23 slice.
Counts describe canonical records on the branch; they are not learner mastery metrics.

| Matrix | Rungs | Present microtopics | Owned primary capabilities | Representative mapped questions | Unresolved / held |
| --- | ---: | ---: | ---: | ---: | --- |
| Physics — One-dimensional motion | 6 | 6 | 6 | 6 retained authored questions | Human academic review pending; no source-backed Core2 custody; donor Core2B transfer item intentionally not retained |
| Physics — Newton-law force reasoning | 5 | 5 | 5 | 1 retained authored Second-Law question | Human academic review pending; friction and third-law donor expansion intentionally deferred |
| Physics — Work / Energy / Power | 7 | 7 | 7 | 7 retained authored questions | Human academic review pending; no source-backed Core2 custody; donor Core2B transfer item intentionally not retained |
| Mathematics — Linear equations in one unknown | 3 | 3 | 3 | 1 authored question | Human academic review pending; no authorised question corpus, so source-backed Core2 remains held |

## Physics — One-dimensional motion

Rung closure:

- R1 → `MIC-PHY-KIN-DISTANCE-DISPLACEMENT`;
- R2 → `MIC-PHY-KIN-AVERAGE-RATES`;
- R3 → `MIC-PHY-KIN-ZERO-V-NONZERO-A`;
- R4G → `MIC-PHY-KIN-MOTION-GRAPHS`;
- R4 → `MIC-PHY-KIN-CONSTANT-ACCELERATION`;
- R5 → `MIC-PHY-KIN-UNIFORM-CIRCULAR-MOTION`.

Key owner-extension capabilities introduced by the migration include average rates,
motion-graph interpretation, constant-acceleration model choice and elementary uniform
circular motion. Their curriculum mappings are intentionally empty because the retained
canonical authority is authored, not a verified board binding.

Representative question pattern includes a motion-graph question whose primary
capability is graph interpretation and whose secondary capability is the distinct
zero-velocity/nonzero-acceleration concept. Prerequisite closure is left to the
capability graph rather than copied into every question.

## Physics — Newton-law force reasoning

The migration adds one explicit Second-Law rung/capability because the retained
Work/Energy derivation capability depends on it.

The important cross-topic edge is:

`CAP-WEP-ENERGY-DERIVATIONS → CAP-NLM-SECOND-LAW → CAP-NLM-FBD-BODY-OWNERSHIP`.

Friction and Newton's third law remain deferred rather than being imported for coverage
cosmetics.

## Physics — Work / Energy / Power

The matrix closes seven authored rungs. The retained quantitative/derivation capability
has two explicit prerequisite branches:

- `CAP-WEP-ENERGY-DERIVATIONS → CAP-NLM-SECOND-LAW`;
- `CAP-WEP-ENERGY-DERIVATIONS → CAP-KIN-CONSTANT-ACCELERATION`.

This is the required cross-matrix ordering mechanism. No comparison of Physics ladder
positions across matrices is used.

Representative retained questions cover supported practice/derivation/practical
reasoning with primary capability ownership and only genuine secondary capabilities.

## Mathematics — Linear equations in one unknown

Rung closure:

- R1 → `MIC-MATH-CONSTRAINT` → `CAP-MATH-SUBSTITUTE`;
- R2 → `MIC-MATH-EQUIVALENT-OPS` → `CAP-MATH-ISOLATE`;
- R3 → `MIC-MATH-EXACT-SOLUTION` → `CAP-MATH-EXACTNESS`.

Capability prerequisite closure is:

`CAP-MATH-EXACTNESS → CAP-MATH-ISOLATE → CAP-MATH-SUBSTITUTE`.

The retained authored question maps:

`Q-MATH-LINEAR-01 → primary CAP-MATH-ISOLATE + secondary CAP-MATH-EXACTNESS, CAP-MATH-SUBSTITUTE`.

Each of those capabilities has exactly one teaching microtopic and one matrix rung, so
the question can be traced to teaching without guessing.

## Current explicit gaps

This report does not claim the Issue #19 subject universe is complete. In particular:

- additional PR #9 Physics donor topics still require slice-by-slice migration review;
- Mathematics currently has only the real canonical linear-equations seed package, so
  coordinate geometry, line/slope, simultaneous-equation and geometry matrices remain
  absent until justified by actual worksheet/curriculum/extension demand;
- source-backed Core2 custody is not manufactured from authored questions;
- all materially changed learner-facing records remain CANDIDATE pending human review.
