# Benchmark coverage tracker

Baseline: `e6f9ccce4a2ecbba8764bfa5cd5e877830afa56d` (frozen after PR #48 merge)

The benchmark agent updates only the benchmark status and links to case directories. Do not edit matrix/content/runtime files as part of this workstream.

| Done | Subject | Matrix | Subtopic | Rungs | Benchmark pack | Gaps logged |
| --- | --- | --- | --- | ---: | --- | --- |
| [x] | Physics | `MATRIX-PHY-ELEC-CURRENT-OHM` | Current electricity, Ohm's law and circuit analysis | 7 | [pack](cases/Physics/MATRIX-PHY-ELEC-CURRENT-OHM/) | GAP-QSM-0001, GAP-QSM-0002 |
| [x] | Physics | `MATRIX-PHY-FLUID-BERNOULLI-EQUATION` | Fluid statics, buoyancy and Bernoulli flow | 5 | [pack](cases/Physics/MATRIX-PHY-FLUID-BERNOULLI-EQUATION/) | GAP-QSM-0001, GAP-QSM-0002 |
| [x] | Physics | `MATRIX-PHY-GRAV-UNIVERSAL-LAW` | Universal gravitation, free fall and orbital motion | 5 | [pack](cases/Physics/MATRIX-PHY-GRAV-UNIVERSAL-LAW/) | GAP-QSM-0002 |
| [x] | Physics | `MATRIX-PHY-KIN-1D-MOTION` | One-dimensional motion | 6 | [pack](cases/Physics/MATRIX-PHY-KIN-1D-MOTION/) | — |
| [x] | Physics | `MATRIX-PHY-MAG-FIELD-LORENTZ` | Magnetic fields, Lorentz force and electromagnetic induction | 6 | [pack](cases/Physics/MATRIX-PHY-MAG-FIELD-LORENTZ/) | GAP-QSM-0001, GAP-QSM-0002 |
| [x] | Physics | `MATRIX-PHY-NLM-FIRST-LAW` | Newton's first law and free-body diagrams | 7 | [pack](cases/Physics/MATRIX-PHY-NLM-FIRST-LAW/) | — |
| [x] | Physics | `MATRIX-PHY-OPTICS-REFLECTION-MIRRORS` | Reflection and spherical mirrors | 6 | [pack](cases/Physics/MATRIX-PHY-OPTICS-REFLECTION-MIRRORS/) | GAP-QSM-0001, GAP-QSM-0002 |
| [x] | Physics | `MATRIX-PHY-OSC-SHM-WAVES` | Oscillations, simple harmonic motion and waves | 5 | [pack](cases/Physics/MATRIX-PHY-OSC-SHM-WAVES/) | GAP-QSM-0001, GAP-QSM-0002 |
| [x] | Physics | `MATRIX-PHY-ROT-RIGID-BODY` | Rotational dynamics, angular momentum and rolling | 5 | [pack](cases/Physics/MATRIX-PHY-ROT-RIGID-BODY/) | GAP-QSM-0001, GAP-QSM-0002 |
| [x] | Physics | `MATRIX-PHY-SIMPLE-MACHINES` | Simple machines | 3 | [pack](cases/Physics/MATRIX-PHY-SIMPLE-MACHINES/) | — |
| [x] | Physics | `MATRIX-PHY-SOUND` | Production, propagation, wave quantities and reflection | 5 | [pack](cases/Physics/MATRIX-PHY-SOUND/) | — |
| [x] | Physics | `MATRIX-PHY-THERMO-FIRST-SECOND-LAW` | Thermodynamics and heat engines | 5 | [pack](cases/Physics/MATRIX-PHY-THERMO-FIRST-SECOND-LAW/) | GAP-QSM-0001, GAP-QSM-0002 |
| [x] | Physics | `MATRIX-PHY-VEC-ADD-SUB` | Vector addition, subtraction and orientation | 4 | [pack](cases/Physics/MATRIX-PHY-VEC-ADD-SUB/) | GAP-QSM-0002, GAP-QSM-0003 |
| [x] | Physics | `MATRIX-PHY-WORK-ENERGY-POWER` | Work, energy and power | 7 | [pack](cases/Physics/MATRIX-PHY-WORK-ENERGY-POWER/) | — |
| [x] | Physics | `MATRIX-PHY-RELATIVE-MOTION` | Relative motion | 4 | [pack](cases/Physics/MATRIX-PHY-RELATIVE-MOTION/) | — |
| [x] | Physics | `MATRIX-PHY-VECTOR-REPRESENTATION` | Vector representation and subtraction | 3 | [pack](cases/Physics/MATRIX-PHY-VECTOR-REPRESENTATION/) | GAP-QSM-0004 |
| [x] | Mathematics | `MATRIX-MATH-LINEAR-EQUATIONS` | One-unknown linear equations over the rationals | 3 | [pack](cases/Mathematics/MATRIX-MATH-LINEAR-EQUATIONS/) | — |

## Completion rule

This sweep has a benchmark pack for all 17 baseline matrices. Each pack records expected and observed behavior, marks non-applicable cases explicitly, and links every material PARTIAL/FAIL/BLOCKED_BY_SOURCE finding to `GAPS.md`.

No repair is included in the benchmark sweep. `ANALYSIS.md` remains reserved for the maintainer phase.
