# Session readiness report

Date: 2026-09-18  
Audit base: `integration/self-study-v1-candidate`  
Base commit audited: `bbf9f00f3232224e609405f9029c7d843a685b0c`

This report is generated from the existing `Shared/tools/session_readiness.py` rules. It is
a practical **self-study executability** report, not an academic-review or source-custody
claim.

A matrix can be mechanically session-ready while still carrying explicit academic/source
warnings. Conversely, a matrix with all named rungs is not session-ready if teaching,
diagnosis, repair or verification support is incomplete.

## Summary

### Physics

| Status | Count |
| --- | ---: |
| `SESSION_READY` | 5 |
| `SESSION_READY_WITH_BRIDGE` | 1 |
| `PILOT_READY` | 1 |
| `NOT_READY` | 9 |

### Mathematics

| Status | Count |
| --- | ---: |
| `SESSION_READY` | 1 |
| `SESSION_READY_WITH_BRIDGE` | 0 |
| `PILOT_READY` | 0 |
| `NOT_READY` | 0 |

The Mathematics count reflects only the one matrix currently represented in this candidate;
it is **not** a claim that the Mathematics syllabus is complete.

## Physics status by matrix

### SESSION_READY

- One-dimensional motion
- Newton's first law and free-body diagrams
- Simple machines
- Production, propagation, wave quantities and reflection
- Work, energy and power

### SESSION_READY_WITH_BRIDGE

- Relative motion
  - explicit prerequisite bridge: signed-coordinate capability → Mathematics
  - provider acceptance remains visible rather than assumed

### PILOT_READY

- Vector representation and subtraction

The vector-representation matrix has teaching records but lacks complete Core1A/Core1B route
coverage for its three current teaching microtopics:

- `MIC-VECTOR-VS-SCALAR`
- `MIC-SIGNED-COMPONENT`
- `MIC-GRAPHICAL-SUBTRACTION`

The audit also reports thin primary-practice/source custody and pending academic review. Those
are warnings rather than structural blockers for a private pilot, but the missing Core1A /
Core1B routing keeps the matrix below `SESSION_READY`.

### NOT_READY

- Current electricity, Ohm's law and circuit analysis
- Fluid statics, buoyancy and Bernoulli flow
- Universal gravitation, free fall and orbital motion
- Magnetic fields, Lorentz force and electromagnetic induction
- Reflection and spherical mirrors
- Oscillations, simple harmonic motion and waves
- Rotational dynamics, angular momentum and rolling
- Thermodynamics and heat engines
- Vector addition, subtraction and orientation

These should not be enabled in the practical session runner merely because a matrix file
exists.

## High-value blocker detail

### Vector addition, subtraction and orientation — NOT_READY

Current matrix state:

- `R3 / CAP-VEC-SUB-ORDER` is ready.
- Three other rungs have no canonical `microtopic_ref` yet.
- The audit also detects a prerequisite that resolves to more than one canonical teaching
  location.

This is the clearest high-ROI content gap for later Motion-in-a-Plane work. The fix belongs
in the subject-content stream: author the smallest reusable vector-addition/decomposition
microtopics/capabilities and remove the prerequisite-location ambiguity. Do not weaken the
readiness rule and do not add one capability per exam question.

### Universal gravitation — NOT_READY

Current matrix state:

- `R1 / CAP-PHY-GRAV-R1` is ready.
- `R4 / CAP-PHY-GRAV-R4` is ready.
- `R5 / CAP-PHY-GRAV-R5` is ready.
- two matrix rungs still lack canonical microtopics.

The correct response is to fill those two durable teaching gaps if/when real worksheet
demand justifies the subtopic, not to mark the partial matrix ready.

## Mathematics

### SESSION_READY

- One-unknown linear equations over the rationals

This is the only Mathematics matrix currently audited in this candidate. Coordinate
geometry, slope/line equations, simultaneous equations and broader geometry are not silently
counted as ready; they are simply not represented as completed matrices here.

## Practical whitelist for v1

The current v1 runner may safely begin with this whitelist:

```text
Physics
  One-dimensional motion
  Newton's first law / free-body diagrams
  Simple machines
  Sound
  Work / energy / power
  Relative motion          [with Mathematics bridge]

Mathematics
  One-unknown linear equations
```

Vector representation remains useful for controlled pilot work but should stay visibly
`PILOT_READY` until its Core1A/Core1B route coverage is completed.

## Immediate use

Relative Motion remains the preferred first real learner session because it is the only
subtopic currently validated through all of:

```text
session readiness
→ rough owner estimate
→ prerequisite bridge
→ learner-facing route
→ retained real external question
→ diagnosis
→ repair
→ fresh verification
→ observation draft
→ review date
```

## Anti-drift decisions

- Do not convert `PILOT_READY` to `SESSION_READY` by weakening checks.
- Do not mark partial matrices ready to increase coverage counts.
- Do not infer syllabus completeness from the number of ready matrices.
- Do not add teaching content solely to eliminate a bridge warning.
- Do not treat authored/candidate practice as source-custody evidence.
- Expand content only from real question demand, genuine prerequisites, explicit syllabus
  scope or deliberate owner-approved extension.

## Next content priority

If the next real worksheet stays within Relative Motion, no subject expansion is needed.

If Motion in a Plane becomes the next target, the first subject-content priority is:

```text
general vector addition / decomposition
→ resolve current vector matrix gaps
→ projectile model selection
→ minimum reusable component-kinematics chain
```

The core architecture does not need another subsystem for this work.
