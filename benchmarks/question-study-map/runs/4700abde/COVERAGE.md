# Full Question → Study Map re-benchmark after fallback/mastery boundary

Baseline: `4700abdefecefd6211488a527594dabba8797e89`

This rerun follows merged PRs #60, #61 and #62. It preserves the historical benchmark packs and re-evaluates all 17 mapped matrices against the existing semantic family, with the new fallback behavior checked inside the existing content-gap, prerequisite-route, rough-estimate and independent-success cases.

Baseline guardrails: **PASS** — GitHub Actions run `35378713205`.

| Done | Subject | Matrix | Readiness | Rerun | Material change |
| --- | --- | --- | --- | --- | --- |
| [x] | Physics | `MATRIX-PHY-ELEC-CURRENT-OHM` | `NOT_READY` | **PARTIAL** | Content gap persists; represented usable rungs can now execute only via bounded fallback |
| [x] | Physics | `MATRIX-PHY-FLUID-BERNOULLI-EQUATION` | `NOT_READY` | **PARTIAL** | Content gap persists; represented usable rungs can now execute only via bounded fallback |
| [x] | Physics | `MATRIX-PHY-GRAV-UNIVERSAL-LAW` | `NOT_READY` | **PARTIAL** | Content gap persists; represented usable rungs can now execute only via bounded fallback |
| [x] | Physics | `MATRIX-PHY-KIN-1D-MOTION` | `SESSION_READY` | **PASS** | No mapping/content regression |
| [x] | Physics | `MATRIX-PHY-MAG-FIELD-LORENTZ` | `NOT_READY` | **PARTIAL** | Content gap persists; represented usable rungs can now execute only via bounded fallback |
| [x] | Physics | `MATRIX-PHY-NLM-FIRST-LAW` | `SESSION_READY` | **PASS** | No mapping/content regression |
| [x] | Physics | `MATRIX-PHY-OPTICS-REFLECTION-MIRRORS` | `NOT_READY` | **PARTIAL** | Content gap persists; represented usable rungs can now execute only via bounded fallback |
| [x] | Physics | `MATRIX-PHY-OSC-SHM-WAVES` | `NOT_READY` | **PARTIAL** | Content gap persists; represented usable rungs can now execute only via bounded fallback |
| [x] | Physics | `MATRIX-PHY-ROT-RIGID-BODY` | `NOT_READY` | **PARTIAL** | Content gap persists; represented usable rungs can now execute only via bounded fallback |
| [x] | Physics | `MATRIX-PHY-SIMPLE-MACHINES` | `SESSION_READY` | **PASS** | No mapping/content regression |
| [x] | Physics | `MATRIX-PHY-SOUND` | `SESSION_READY` | **PASS** | No mapping/content regression |
| [x] | Physics | `MATRIX-PHY-THERMO-FIRST-SECOND-LAW` | `NOT_READY` | **PARTIAL** | Content gap persists; represented usable rungs can now execute only via bounded fallback |
| [x] | Physics | `MATRIX-PHY-VEC-ADD-SUB` | `SESSION_READY_WITH_BRIDGE` | **PASS** | Now READY_WITH_BRIDGE after #56; real Q4/Q5 demand routable |
| [x] | Physics | `MATRIX-PHY-WORK-ENERGY-POWER` | `SESSION_READY` | **PASS** | No mapping/content regression |
| [x] | Physics | `MATRIX-PHY-RELATIVE-MOTION` | `SESSION_READY_WITH_BRIDGE` | **PASS** | No mapping/content regression |
| [x] | Physics | `MATRIX-PHY-VECTOR-REPRESENTATION` | `SESSION_READY_WITH_BRIDGE` | **PASS** | READY_WITH_BRIDGE repair remains stable |
| [x] | Mathematics | `MATRIX-MATH-LINEAR-EQUATIONS` | `SESSION_READY` | **PASS** | No mapping/content regression |

## Cross-cutting runtime checks

The full rerun treats the merged fallback work as a semantic change, not as a readiness rewrite:

- invalid/optional rough estimates warn and fall back; they do not create mastery;
- a usable demanded rung inside an incomplete matrix may continue as `EXECUTE_WITH_FALLBACK`;
- missing microtopic/capability/teaching path requires `OWNER_DECISION`;
- `OWNER_DECISION` propagates through prerequisite dependencies, while unrelated worksheet branches may still execute;
- independent correctness without canonical fresh verification is capped at `UNCERTAIN` rather than `DEMONSTRATED`;
- matrix readiness labels remain unchanged/truthful.

## Result

- Matrices rerun: **17 / 17**.
- New benchmark gap families: **0**.
- New mapping/content regressions observed: **0**.
- `GAP-QSM-0001`: persists in seven dormant Physics matrices as demand-gated question-inventory backlog.
- `GAP-QSM-0002`: persists in eight incomplete Physics matrices; the Vector Add/Sub slice is no longer part of this backlog after #56.
- `GAP-QSM-0003`: remains resolved.
- `GAP-QSM-0004`: remains resolved.
- The fallback/runtime changes pass the existing benchmark philosophy without weakening readiness or learner-evidence boundaries.
