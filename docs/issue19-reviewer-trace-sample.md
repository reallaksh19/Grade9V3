# Issue #19 reviewer trace sample

This document is the human-review acceptance sample for Issue #19. It is intentionally
readable without implementation code.

For each retained canonical question it answers:

1. What capability is this question primarily testing?
2. What prerequisite capability would plausibly cause failure if missing?
3. Where is the primary capability taught?

The prerequisite column uses capability edges only. Matrix `ladder_position` is never
compared across matrices.

| Question | Primary capability | Failure-relevant prerequisite(s) | Canonical teaching location |
| --- | --- | --- | --- |
| `Q-MATH-LINEAR-01` | `CAP-MATH-ISOLATE` — isolate the unknown with solution-preserving operations | `CAP-MATH-SUBSTITUTE` | Mathematics `MATRIX-MATH-LINEAR-EQUATIONS`, R2 → `MIC-MATH-EQUIVALENT-OPS` |
| `Q-PHY-KIN-2A-COV-05` | `CAP-KIN-MOTION-GRAPHS` — interpret position-time / velocity-time graph information correctly | `CAP-KIN-AVERAGE-RATES` | Physics `MATRIX-PHY-KIN-1D-MOTION`, R4G → `MIC-PHY-KIN-MOTION-GRAPHS` |
| `Q-PHY-KIN-PRACTICAL-13` | `CAP-KIN-MOTION-GRAPHS` | `CAP-KIN-AVERAGE-RATES` | Physics `MATRIX-PHY-KIN-1D-MOTION`, R4G → `MIC-PHY-KIN-MOTION-GRAPHS` |
| `Q-PHY-NLM-2A-COV-04` | `CAP-NLM-FRICTION` — infer friction direction from relative sliding / slip tendency | `CAP-NLM-FBD-BODY-OWNERSHIP` | Physics `MATRIX-PHY-NLM-FIRST-LAW`, R5 → `MIC-PHY-NLM-FRICTION` |
| `Q-PHY-NLM-PRACTICAL-12` | `CAP-NLM-SECOND-LAW` — relate signed net external force to acceleration for one chosen body | `CAP-NLM-FBD-BODY-OWNERSHIP` | Physics `MATRIX-PHY-NLM-FIRST-LAW`, R6 → `MIC-PHY-NLM-SECOND-LAW` |
| `Q-PHY-WEP-2A-DERIV-01` | `CAP-WEP-ENERGY-DERIVATIONS` — connect work/energy relations to prior mechanics rather than quote them as isolated formulas | `CAP-WEP-WORK-DIRECTION`; `CAP-NLM-SECOND-LAW`; `CAP-KIN-CONSTANT-ACCELERATION` | Physics `MATRIX-PHY-WORK-ENERGY-POWER`, R5D → `MIC-PHY-WEP-ENERGY-DERIVATIONS` |
| `Q-PHY-WEP-PRACTICAL-09` | `CAP-WEP-GRADE9-QUANT` — choose and execute the appropriate quantitative work/energy relation | `CAP-WEP-MECH-ENERGY-CONDITION`; `CAP-WEP-ENERGY-DERIVATIONS` | Physics `MATRIX-PHY-WORK-ENERGY-POWER`, R6 → `MIC-PHY-WEP-GRADE9-QUANT` |
| `Q-PHY-SOUND-2A-01` | `CAP-SOUND-WAVE-QUANTITIES` — distinguish and relate period, frequency, wavelength, amplitude and wave speed | `CAP-SOUND-LONGITUDINAL` | Physics `MATRIX-PHY-SOUND`, R3 → `MIC-PHY-SOUND-WAVE-QUANTITIES` |
| `Q-PHY-MACHINE-2A-01` | `CAP-MACHINE-MA` — calculate mechanical advantage from load and effort | `CAP-MACHINE-TRADEOFF` | Physics `MATRIX-PHY-SIMPLE-MACHINES`, R2 → `MIC-PHY-MACHINE-MA` |
| `Q-PHY-VECOPS-2A-01` | `CAP-VEC-SUB-ORDER` — preserve operand order and orientation in vector subtraction | `CAP-GRAPHICAL-SUBTRACT` | Physics `MATRIX-PHY-VEC-ADD-SUB`, R3 → `MIC-PHY-VEC-SUB-ORDER` |
| `Q-PHY-VECREP-2A-01` | `CAP-VECTOR-VS-SCALAR` — distinguish vector information from magnitude-only information | `CAP-SIGNED-PAIR-BRIDGE` | Physics `MATRIX-PHY-VECTOR-REPRESENTATION`, R1 → `MIC-VECTOR-VS-SCALAR` |

## Cross-matrix examples

The sample also demonstrates why cross-matrix study order must come from prerequisite
edges rather than rung percentages.

### Work/Energy derivation branch

```text
Q-PHY-WEP-2A-DERIV-01
  → CAP-WEP-ENERGY-DERIVATIONS
      → CAP-WEP-WORK-DIRECTION
      → CAP-NLM-SECOND-LAW
          → CAP-NLM-FBD-BODY-OWNERSHIP
      → CAP-KIN-CONSTANT-ACCELERATION
          → CAP-KIN-MOTION-GRAPHS
              → CAP-KIN-AVERAGE-RATES
                  → CAP-KIN-DISTANCE-DISPLACEMENT
```

The Newton and Kinematics matrices have independent local ladder coordinates. The
capability edges above, not those local coordinates, establish the legal study
dependencies.

### Simple Machines branch

```text
Q-PHY-MACHINE-2A-01
  → CAP-MACHINE-MA
      → CAP-MACHINE-TRADEOFF
          → CAP-WEP-WORK-DIRECTION
```

Again, the path crosses matrices solely through capability prerequisites.

## Secondary capability interpretation

Secondary capability refs are kept sparse. They name additional learner actions the
question materially requires; they are not a copy of prerequisite closure.

Examples:

- `Q-PHY-KIN-2A-COV-05` has primary `CAP-KIN-MOTION-GRAPHS` and meaningful
  secondary `CAP-KIN-ZERO-V-NONZERO-A`.
- `Q-PHY-NLM-PRACTICAL-12` has primary `CAP-NLM-SECOND-LAW` and meaningful
  secondary `CAP-NLM-FBD-BODY-OWNERSHIP`.
- `Q-PHY-WEP-PRACTICAL-09` has primary `CAP-WEP-GRADE9-QUANT` and secondaries
  `CAP-WEP-MECH-ENERGY-CONDITION` and `CAP-WEP-ENERGY-DERIVATIONS`.

The graph remains responsible for all deeper prerequisite closure. Prerequisite edges are intentionally minimal: a deeper derivation or related concept is not a prerequisite unless its absence would block learning or demonstrating the target capability.

## What this sample does not claim

This is a canonical question-to-teaching trace sample, not a learner diagnosis and not
a curriculum-authority claim.

It does **not** establish:

- that any CANDIDATE record is academically reviewed;
- that authored questions provide source custody;
- that a learner is weak or strong in any capability;
- that local ladder positions can be compared across matrices;
- that the Issue #19 real-worksheet acceptance has been completed.

The final real-worksheet acceptance remains separate: it requires an actual supplied or
retained worksheet whose questions span more than one matrix. No synthetic worksheet is
created merely to make that checkbox green.
