# Benchmark coverage tracker

Baseline: `integration/self-study-v1-candidate`

The benchmark agent updates only the benchmark status and links to case directories. Do not edit matrix/content/runtime files as part of this workstream.

| Done | Subject | Matrix | Subtopic | Rungs | Benchmark pack | Gaps logged |
| --- | --- | --- | --- | ---: | --- | --- |
| [ ] | Physics | `MATRIX-PHY-ELEC-CURRENT-OHM` | Current electricity, Ohm's law and circuit analysis | 7 | TODO | TODO |
| [ ] | Physics | `MATRIX-PHY-FLUID-BERNOULLI-EQUATION` | Fluid statics, buoyancy and Bernoulli flow | 5 | TODO | TODO |
| [ ] | Physics | `MATRIX-PHY-GRAV-UNIVERSAL-LAW` | Universal gravitation, free fall and orbital motion | 5 | TODO | TODO |
| [ ] | Physics | `MATRIX-PHY-KIN-1D-MOTION` | One-dimensional motion | 6 | TODO | TODO |
| [ ] | Physics | `MATRIX-PHY-MAG-FIELD-LORENTZ` | Magnetic fields, Lorentz force and electromagnetic induction | 6 | TODO | TODO |
| [ ] | Physics | `MATRIX-PHY-NLM-FIRST-LAW` | Newton's first law and free-body diagrams | 7 | TODO | TODO |
| [ ] | Physics | `MATRIX-PHY-OPTICS-REFLECTION-MIRRORS` | Reflection and spherical mirrors | 6 | TODO | TODO |
| [ ] | Physics | `MATRIX-PHY-OSC-SHM-WAVES` | Oscillations, simple harmonic motion and waves | 5 | TODO | TODO |
| [ ] | Physics | `MATRIX-PHY-ROT-RIGID-BODY` | Rotational dynamics, angular momentum and rolling | 5 | TODO | TODO |
| [ ] | Physics | `MATRIX-PHY-SIMPLE-MACHINES` | Simple machines | 3 | TODO | TODO |
| [ ] | Physics | `MATRIX-PHY-SOUND` | Production, propagation, wave quantities and reflection | 5 | TODO | TODO |
| [ ] | Physics | `MATRIX-PHY-THERMO-FIRST-SECOND-LAW` | Thermodynamics and heat engines | 5 | TODO | TODO |
| [ ] | Physics | `MATRIX-PHY-VEC-ADD-SUB` | Vector addition, subtraction and orientation | 4 | TODO | TODO |
| [ ] | Physics | `MATRIX-PHY-WORK-ENERGY-POWER` | Work, energy and power | 7 | TODO | TODO |
| [ ] | Physics | `MATRIX-PHY-RELATIVE-MOTION` | Relative motion | 4 | TODO | TODO |
| [ ] | Physics | `MATRIX-PHY-VECTOR-REPRESENTATION` | Vector representation and subtraction | 3 | TODO | TODO |
| [ ] | Mathematics | `MATRIX-MATH-LINEAR-EQUATIONS` | One-unknown linear equations over the rationals | 3 | TODO | TODO |

## Completion rule

The sweep is complete only when every row above has:

- a benchmark pack under `cases/<subject>/<matrix-id>/`;
- expected and observed behavior recorded;
- applicable benchmark dimensions marked PASS/FAIL/PARTIAL/BLOCKED_BY_SOURCE/NOT_APPLICABLE;
- every material FAIL/PARTIAL/BLOCKED_BY_SOURCE linked to `GAPS.md`;
- no repairs mixed into the benchmark PR.