# Full Question → Study Map re-benchmark after session-only owner resolution

Baseline: `a6842190f4b9835c654ec110a5875c33ae8ca220`

This rerun follows PR #64, which allows a parent to resolve an existing `OWNER_DECISION` for the current session through one of two narrow choices:

```text
CAPABILITY=LOCATION:MATRIX_ID:RUNG
CAPABILITY=EXTERNAL:PROVIDER
```

The change is runtime-only. It does not change canonical delivery, matrix readiness, learner evidence, source custody, or benchmark expectations.

Baseline guardrails: **PASS** — GitHub Actions run `35379234710`.

| Done | Subject | Matrix | Readiness | Rerun |
| --- | --- | --- | --- | --- |
| [x] | Physics | `MATRIX-PHY-ELEC-CURRENT-OHM` | `NOT_READY` | **PARTIAL** |
| [x] | Physics | `MATRIX-PHY-FLUID-BERNOULLI-EQUATION` | `NOT_READY` | **PARTIAL** |
| [x] | Physics | `MATRIX-PHY-GRAV-UNIVERSAL-LAW` | `NOT_READY` | **PARTIAL** |
| [x] | Physics | `MATRIX-PHY-KIN-1D-MOTION` | `SESSION_READY` | **PASS** |
| [x] | Physics | `MATRIX-PHY-MAG-FIELD-LORENTZ` | `NOT_READY` | **PARTIAL** |
| [x] | Physics | `MATRIX-PHY-NLM-FIRST-LAW` | `SESSION_READY` | **PASS** |
| [x] | Physics | `MATRIX-PHY-OPTICS-REFLECTION-MIRRORS` | `NOT_READY` | **PARTIAL** |
| [x] | Physics | `MATRIX-PHY-OSC-SHM-WAVES` | `NOT_READY` | **PARTIAL** |
| [x] | Physics | `MATRIX-PHY-ROT-RIGID-BODY` | `NOT_READY` | **PARTIAL** |
| [x] | Physics | `MATRIX-PHY-SIMPLE-MACHINES` | `SESSION_READY` | **PASS** |
| [x] | Physics | `MATRIX-PHY-SOUND` | `SESSION_READY` | **PASS** |
| [x] | Physics | `MATRIX-PHY-THERMO-FIRST-SECOND-LAW` | `NOT_READY` | **PARTIAL** |
| [x] | Physics | `MATRIX-PHY-VEC-ADD-SUB` | `SESSION_READY_WITH_BRIDGE` | **PASS** |
| [x] | Physics | `MATRIX-PHY-WORK-ENERGY-POWER` | `SESSION_READY` | **PASS** |
| [x] | Physics | `MATRIX-PHY-RELATIVE-MOTION` | `SESSION_READY_WITH_BRIDGE` | **PASS** |
| [x] | Physics | `MATRIX-PHY-VECTOR-REPRESENTATION` | `SESSION_READY_WITH_BRIDGE` | **PASS** |
| [x] | Mathematics | `MATRIX-MATH-LINEAR-EQUATIONS` | `SESSION_READY` | **PASS** |

## Owner-resolution invariants checked

- `LOCATION` may select only a location already offered by the canonical route.
- `EXTERNAL` creates only a session-scoped provider label; it does not create canonical provider truth.
- An owner choice cannot jump over an unresolved prerequisite dependency.
- Applied owner choices remain visible and force `EXECUTE_WITH_FALLBACK`.
- The original canonical finding remains inspectable as owner-resolved history.
- Malformed/duplicate/unknown/unnecessary owner choices are warnings, not silent mutations.
- No owner choice creates learner mastery evidence.
- The #62 verification boundary remains intact: without canonical fresh verification, independent correctness stays `UNCERTAIN`.

## Result

- Matrices rerun: **17 / 17**.
- New benchmark gap families: **0**.
- Mapping/content regressions observed: **0**.
- Readiness changes caused by #64: **0**.
- `GAP-QSM-0001`: persists as demand-gated question-inventory backlog.
- `GAP-QSM-0002`: persists across the eight incomplete Physics matrices.
- `GAP-QSM-0003` and `GAP-QSM-0004`: remain resolved.
- Session-only owner resolution is compatible with the existing benchmark separation and evidence boundaries.
