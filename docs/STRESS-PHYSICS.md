# Stress test — Physics

Run against the whole subject rather than the one path with a library behind it. Four
dimensions, measured; every finding below was produced by a command, not by reading code.

| | |
|---|---:|
| matrices | 14 |
| rungs | 68 |
| rungs with a record | **6** |
| library packages | 2 of 14 buckets |
| committed publications | 1 |

---

## S1 · The published page has no relationship to the library — **the finding**

Every gate in this repository governs the library: intake, substance, authority,
depiction, spec delivery, the vocabulary ceiling. The one artifact a learner can open was
checked by none of them, and not because it drifted. **It was never compiled from the
library at all.**

`Physics/content/relative-motion-g9/inputs/plan.json` carries hand-written prose in its own
id space — units `U-1A-VEC`, buckets `B-VEC`, obligations `OB-VEC-CONCEPT` — and
references zero library records:

```
MIC-MEASURED-FROM    in the frozen plan: False
MIC-SAME-TIME        in the frozen plan: False
MIC-COMMON-INTERVAL  in the frozen plan: False
MIC-GEOMETRIC-CHECK  in the frozen plan: False
```

Adding, changing or deleting any library record cannot move that page, and nothing said so.

**Why no gate caught it.** `republish.py` verifies the *frozen inputs* against the
*published bytes*, and does that correctly. Nothing compared the plan to the library the
plan was supposed to project. Two links in the chain, one checked.

**And the page is the failure the ceiling exists to prevent.** The published HTML uses
**14 distinct ceiling words** across the two ladders — `frame`, `axis`, `axes`,
`component`, `vector`, `velocity`, `perpendicular`, `right-triangle`, `quadrant`, `basis`,
`vector subtraction`, `resultant`, `free vector`. The gate that forbids them governs
records this page does not contain.

**Fix.** `publication_provenance.py`. A run declares its basis beside its inputs — outside
the digest-verified publication basis, so declaring cannot disturb what `republish`
checks (verified: the basis digest is unchanged and the publication still PASSes).

```
basis: LIBRARY                       and names the records it projects
basis: AUTHORED_OUTSIDE_THE_LIBRARY  and says why, which puts it on the board
```

Silence is the one answer not available. The existing run now declares
`AUTHORED_OUTSIDE_THE_LIBRARY` with its measured numbers. A hand-authored run is a
legitimate thing to have; pretending otherwise is how a true fact stops being written down.

`PUBLICATION_OMITS_A_MICROTOPIC_THE_LIBRARY_TEACHES` is the detector for the day a run *is*
library-based — a rung authored after the freeze, taught by the library and not by the
page. Reported, never enforced: republishing is owner work.

**`republish.py` was not in CI at all.** Now it is.

---

## S2 · The request layer holds — and was over-claiming

42 requests: 14 buckets × 3 purposes, every core. **Zero crashes**, and behaviour uniform
across all 14:

| purpose | Core2B | buckets |
|---|---|---:|
| `COMPETITION` | READY | 14 |
| `PRACTICE` | READY | 14 |
| `STARTER` | WITHHELD, with its own reason | 14 |

But twelve of those buckets have **no library records at all**, and the plan still called
Core2A and Core2B READY. Practice varies instances of what teaching established; transfer
changes the demand while holding truth already taught. Neither survives an empty ladder.

A defect in the resolver I wrote, invisible on the one bucket that has a library. Practice
is now BLOCKED where no rung has a record:

```
CORE2A=BLOCKED  CORE2B=BLOCKED   12 buckets
CORE2A=READY    CORE2B=READY      2 buckets
```

---

## S3 · A malformed matrix produced a traceback, not a finding

18 malformed boards fed to the two matrix-layer audits: **7 raised**. `matrix_conformance`
ran its semantic checks *before* schema validation, so a board whose `rungs` is a string
crashed the gate instead of reporting `MATRIX_STRUCTURE`. A stack trace names no rule, and
these are exactly the shapes thirteen parallel authors can produce.

`resolve_request` already validated structure first; the other two now match. A broken
matrix exits 1 with a named finding.

This is the second time this defect class has appeared — `check()` once raised
`AttributeError` on a wrong-typed record while promising never to raise on content. The
promise is easy to make in a docstring and only holds when something feeds the tool
garbage on purpose.

---

## S4 · What the stress test did not break

- **68 rungs, 14 matrices, 0 findings** against `matrix_conformance --enforce`.
- **Every matrix compiles a complete brief** — ceiling, phases, transfer rows, resolved
  support — at its own lowest and highest ladder positions.
- **The entry rung authored yesterday holds.** `MIC-MEASURED-FROM` respects its own
  ceiling, carries no relation, and declares `oracle.no_numeric_claim`.
- **The committed publication still verifies**, basis digest unchanged.

---

## Carried forward, reported and not enforced

| | count |
|---|---:|
| ceiling words in an authored explanation | 7 |
| ceiling words in a matrix's own learner-facing text | 4 |
| capability forks, each with an untaught discrimination | 2 stems |
| runs authored outside the library | 1 of 1 |
| rungs with no record | **62 of 68** |

Each is somebody's content decision rather than a structural defect, which is why each is
reported by name and none fails the build.
