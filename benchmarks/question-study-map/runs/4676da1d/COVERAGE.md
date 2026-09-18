# Full Question → Study Map re-benchmark after PR #57

Baseline: `4676da1dc4b595ab88ad0f6a7aed24d3040a9040`

The original benchmark packs under `benchmarks/question-study-map/cases/**` remain unchanged. This run reapplies the same semantic case family to all 17 matrices after the Vector Representation modernization.

Baseline guardrails: **PASS** — GitHub Actions run `35376387928`.

| Done | Subject | Matrix | Readiness | Rerun | Change |
| --- | --- | --- | --- | --- | --- |
| [x] | Physics | `MATRIX-PHY-ELEC-CURRENT-OHM` | `NOT_READY` | **PARTIAL** | No material semantic change |
| [x] | Physics | `MATRIX-PHY-FLUID-BERNOULLI-EQUATION` | `NOT_READY` | **PARTIAL** | No material semantic change |
| [x] | Physics | `MATRIX-PHY-GRAV-UNIVERSAL-LAW` | `NOT_READY` | **PARTIAL** | No material semantic change |
| [x] | Physics | `MATRIX-PHY-KIN-1D-MOTION` | `SESSION_READY` | **PASS** | No material semantic change |
| [x] | Physics | `MATRIX-PHY-MAG-FIELD-LORENTZ` | `NOT_READY` | **PARTIAL** | No material semantic change |
| [x] | Physics | `MATRIX-PHY-NLM-FIRST-LAW` | `SESSION_READY` | **PASS** | No material semantic change |
| [x] | Physics | `MATRIX-PHY-OPTICS-REFLECTION-MIRRORS` | `NOT_READY` | **PARTIAL** | No material semantic change |
| [x] | Physics | `MATRIX-PHY-OSC-SHM-WAVES` | `NOT_READY` | **PARTIAL** | No material semantic change |
| [x] | Physics | `MATRIX-PHY-ROT-RIGID-BODY` | `NOT_READY` | **PARTIAL** | No material semantic change |
| [x] | Physics | `MATRIX-PHY-SIMPLE-MACHINES` | `SESSION_READY` | **PASS** | No material semantic change |
| [x] | Physics | `MATRIX-PHY-SOUND` | `SESSION_READY` | **PASS** | No material semantic change |
| [x] | Physics | `MATRIX-PHY-THERMO-FIRST-SECOND-LAW` | `NOT_READY` | **PARTIAL** | No material semantic change |
| [x] | Physics | `MATRIX-PHY-VEC-ADD-SUB` | `NOT_READY` | **PARTIAL** | GAP-QSM-0003 resolved; GAP-QSM-0002 still keeps matrix NOT_READY |
| [x] | Physics | `MATRIX-PHY-WORK-ENERGY-POWER` | `SESSION_READY` | **PASS** | No material semantic change |
| [x] | Physics | `MATRIX-PHY-RELATIVE-MOTION` | `SESSION_READY_WITH_BRIDGE` | **PASS** | No material semantic change |
| [x] | Physics | `MATRIX-PHY-VECTOR-REPRESENTATION` | `SESSION_READY_WITH_BRIDGE` | **PASS** | GAP-QSM-0004 resolved; PILOT_READY → SESSION_READY_WITH_BRIDGE |
| [x] | Mathematics | `MATRIX-MATH-LINEAR-EQUATIONS` | `SESSION_READY` | **PASS** | No material semantic change |

## Result

- Matrices rerun: **17 / 17**.
- New regressions observed: **0**.
- `GAP-QSM-0003`: **verified resolved**.
- `GAP-QSM-0004`: **verified resolved**.
- `GAP-QSM-0001`: persists as demand-gated question-inventory backlog.
- `GAP-QSM-0002`: persists as demand-gated incomplete teaching-rung backlog.
- Next justified repair remains Vector Addition/Decomposition, based on the already-recorded real NEETPrep river-crossing demand.
