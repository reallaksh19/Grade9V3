# Vector foundations re-benchmark

Repair branch: `content/vector-foundations-modernization`  
Repair PR: #56  
Baseline gaps: `GAP-QSM-0002`, `GAP-QSM-0003`, `GAP-QSM-0004`

This is a focused re-benchmark of the two vector matrices after the maintainer analysis. It
does not revise the historical baseline observations in the original benchmark packs.

## Vector Representation

Before:

```text
R1 MIC-VECTOR-VS-SCALAR -> CAP-VECTOR-VS-SCALAR
R2 MIC-SIGNED-COMPONENT -> CAP-VECTOR-VS-SCALAR
=> two local teaching locations for one capability
=> ambiguity downstream
=> no Core1A/Core1B routes
=> PILOT_READY
```

After:

```text
R1 MIC-VECTOR-VS-SCALAR -> CAP-VECTOR-VS-SCALAR
R2 MIC-SIGNED-COMPONENT -> CAP-VECTOR-SIGNED-COMPONENT
R3 MIC-GRAPHICAL-SUBTRACTION -> CAP-GRAPHICAL-SUBTRACT
```

Observed repair checks:

- each of the three capabilities has exactly one teaching location;
- `CAP-VECTOR-VS-SCALAR` no longer claims signed-component competence;
- `CAP-VECTOR-SIGNED-COMPONENT` owns axis/sign transformations;
- `CAP-GRAPHICAL-SUBTRACT` depends on signed-component competence rather than the old broad capability;
- all three rungs have Core1A and Core1B route coverage;
- all three rungs have complete elicitation cycles;
- readiness is `SESSION_READY_WITH_BRIDGE`, with Mathematics bridge semantics still explicit.

Disposition:

```text
GAP-QSM-0003  RESOLVED for the observed ambiguity
GAP-QSM-0004  RESOLVED
```

The Shared ambiguity resolver was not changed.

## Vector Addition / Subtraction

The old active matrix mixed one implemented subtraction-order rung with three synthesis
skeletons, including an unrelated cross-product rung.

The active matrix is now the minimum reusable slice supported by real demand:

```text
R1 CAP-VEC-COMPONENT-SUM
   add corresponding signed components in one common axis system

R2 CAP-VEC-RESULTANT-CONSTRAINT
   impose a target resultant component and solve the required input component

R3 CAP-VEC-SUB-ORDER
   preserve subtraction operand order
```

The former cross-product synthesis rung is not silently taught. Its intent is retained as a
deferred known issue until real demand justifies a separate content slice.

Observed repair checks:

- every active rung has a canonical microtopic;
- every active rung has teaching, misconception/repair, exit verification and Core1A/Core1B coverage;
- the matrix readiness result is `SESSION_READY_WITH_BRIDGE`;
- the prerequisite route contains no ambiguous local teaching location;
- the Mathematics signed-coordinate bridge remains explicit.

Disposition:

```text
GAP-QSM-0002  PARTIALLY RESOLVED
```

Only the demand-justified Vector Add/Sub slice is completed. The other incomplete Physics
matrices remain deliberately demand-gated.

## Real demand check: NEETPrep Q4/Q5

The external questions remain transient.

They now route as:

```text
Q4
primary   CAP-VEC-RESULTANT-CONSTRAINT
secondary CAP-RELATIVE-V

Q5
primary   CAP-VEC-RESULTANT-CONSTRAINT
secondary CAP-RELATIVE-V
          CAP-RIGHT-TRIANGLE
```

The route includes:

```text
CAP-VECTOR-SIGNED-COMPONENT
→ CAP-VEC-COMPONENT-SUM
→ CAP-VEC-RESULTANT-CONSTRAINT
```

and preserves external Mathematics bridges rather than fabricating local mastery.

## Explicit remaining boundary

This repair does **not** teach arbitrary-angle trigonometric decomposition from a
magnitude-and-angle representation.

If a selected question requires sine/cosine decomposition, that remains a distinct
provider/content gap and must not be hidden inside `CAP-VEC-COMPONENT-SUM`.

## Regression evidence

The content migration exposed old ceiling-audit tests that were coupled to exact Vector
Representation prose. Those falsifiers were moved to stable synthetic fixtures, and a
separate regression now checks that the old benchmark-named Vector Representation ceiling
defect stays cleared.

The full repository guardrail passed on the repaired code before this re-benchmark note was
added. Final PR validation is recorded on PR #56.
