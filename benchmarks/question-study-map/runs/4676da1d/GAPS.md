# Gap status after full rerun

Baseline: `4676da1dc4b595ab88ad0f6a7aed24d3040a9040`

## Persisting

### GAP-QSM-0001 — question inventory backlog

**PERSISTS.** Seven dormant Physics matrices still lack retained canonical question inventory. No blanket question creation is justified.

### GAP-QSM-0002 — incomplete teaching-rung backlog

**PERSISTS.** Nine Physics matrices still contain unresolved teaching rungs. In the current priority slice, Vector Add/Sub still lacks canonical teaching at R1, R2 and R4 and correctly remains `NOT_READY`.

## Verified resolved

### GAP-QSM-0003 — Vector Add/Sub prerequisite ambiguity

**RESOLVED.** The chain now resolves through distinct capability ownership:
`CAP-VEC-SUB-ORDER → CAP-GRAPHICAL-SUBTRACT → CAP-VECTOR-SIGNED-COMPONENT`.
The readiness regression explicitly confirms no `READINESS_PREREQUISITE_AMBIGUOUS` finding.

### GAP-QSM-0004 — Vector Representation reconstruction coverage

**RESOLVED.** The three matrix teaching rungs now have Core1A and Core1B route coverage plus complete elicitation, and the matrix is `SESSION_READY_WITH_BRIDGE`.

## Boundary

This rerun changes benchmark evidence only. No production repair is mixed into this branch.
