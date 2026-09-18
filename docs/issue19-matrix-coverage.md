# Issue #19 matrix coverage report

This report covers the matrices materially changed or added in the current PR #23 slice.
Counts describe canonical records on the branch; they are not learner mastery metrics.

| Matrix | Rungs | Present microtopics | Owned primary capabilities | Representative mapped questions | Unresolved / held |
| --- | ---: | ---: | ---: | ---: | --- |
| Physics — One-dimensional motion | 6 | 6 | 6 | 6 retained authored questions | Human academic review pending; no source-backed Core2 custody; donor Core2B transfer item intentionally not retained |
| Physics — Newton-law force reasoning | 7 | 7 | 7 | 7 retained authored Core2A questions | Human academic review pending; donor Core2B frame-choice transfer item intentionally not retained |
| Physics — Work / Energy / Power | 7 | 7 | 7 | 7 retained authored questions | Human academic review pending; no source-backed Core2 custody; donor Core2B transfer item intentionally not retained |
| Physics — Gravitation | 5 | 3 canonical + 2 synthesis gaps | 3 | 1 retained authored Core2A question | R2 inverse-square and R3 free-fall acceleration remain synthesis/un-authored canonical gaps; donor Core2B item not retained |
| Physics — Vector addition/subtraction | 4 | 1 canonical + 3 synthesis gaps | 1 | 1 retained authored Core2A question | R1/R2/R4 remain synthesis gaps; donor Core2B item not retained |
| Physics — Vector representation | 3 | 3 present rungs (4 package microtopics) | 4 | 1 retained authored Core2A question | Human academic review pending; donor Core2B item not retained |
| Physics — Sound | 5 | 5 | 5 | 5 retained authored questions | Human academic review pending; heritage/curriculum-specific row held pending authoritative binding; no source-backed Core2 custody |
| Physics — Simple Machines | 3 | 3 | 3 | 2 retained authored questions | Human academic review pending; no source-backed Core2 custody |
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

The completed matrix now contains seven authored rungs:

- net-zero-motion reasoning;
- zero force sum;
- free-body force ownership;
- friction from relative slip tendency;
- Newton's Second Law;
- Newton's third-law interaction pairs;
- observer-frame choice.

Friction, Second Law and third law all depend explicitly on
`CAP-NLM-FBD-BODY-OWNERSHIP`, so each appears after the FBD rung in this matrix.

The important cross-topic edge remains:

`CAP-WEP-ENERGY-DERIVATIONS → CAP-NLM-SECOND-LAW → CAP-NLM-FBD-BODY-OWNERSHIP`.

## Physics — Work / Energy / Power

The matrix closes seven authored rungs. The retained quantitative/derivation capability
has two explicit prerequisite branches:

- `CAP-WEP-ENERGY-DERIVATIONS → CAP-NLM-SECOND-LAW`;
- `CAP-WEP-ENERGY-DERIVATIONS → CAP-KIN-CONSTANT-ACCELERATION`.

This is the required cross-matrix ordering mechanism. No comparison of Physics ladder
positions across matrices is used.

Representative retained questions cover supported practice/derivation/practical
reasoning with primary capability ownership and only genuine secondary capabilities.

## Physics — Gravitation and vector practice-only coverage

These matrices were not rewritten. PR #9 supplied one retained authored Core2A anchor
per matrix, and each anchor traces to already-existing canonical teaching:

- Gravitation: `Q-PHY-GRAV-2A-01 → CAP-PHY-GRAV-R1 → MIC-PHY-GRAV-R1 → R1`;
- Vector add/sub: `Q-PHY-VECOPS-2A-01 → CAP-VEC-SUB-ORDER → MIC-PHY-VEC-SUB-ORDER → R3`;
- Vector representation: `Q-PHY-VECREP-2A-01 → CAP-VECTOR-VS-SCALAR → MIC-VECTOR-VS-SCALAR → R1`.

The coverage report deliberately keeps existing synthesis gaps visible. In particular,
Gravitation R2/R3 and Vector add/sub R1/R2/R4 have no canonical microtopic record yet;
the practice migration does not manufacture one.

## Physics — Sound

Rung closure:

- R1 → `MIC-PHY-SOUND-SOURCE-MEDIUM` → `CAP-SOUND-SOURCE-MEDIUM`;
- R2 → `MIC-PHY-SOUND-LONGITUDINAL` → `CAP-SOUND-LONGITUDINAL`;
- R3 → `MIC-PHY-SOUND-WAVE-QUANTITIES` → `CAP-SOUND-WAVE-QUANTITIES`;
- R4 → `MIC-PHY-SOUND-PERCEPTION` → `CAP-SOUND-PERCEPTION`;
- R5 → `MIC-PHY-SOUND-REFLECTION` → `CAP-SOUND-REFLECTION`.

The donor heritage row was not migrated because its curriculum-specific authority was
not canonical. The gap is visible in the package scope rather than being replaced with
synthetic authority.

## Physics — Simple Machines

Rung closure:

- R1 → `MIC-PHY-MACHINE-TRADEOFF` → `CAP-MACHINE-TRADEOFF`;
- R2 → `MIC-PHY-MACHINE-MA` → `CAP-MACHINE-MA`;
- R3 → `MIC-PHY-MACHINE-COMPARE` → `CAP-MACHINE-COMPARE`.

The cross-matrix prerequisite is explicit:

`CAP-MACHINE-TRADEOFF → CAP-WEP-GRADE9-QUANT`.

No ladder position is compared with the WEP matrix.

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
