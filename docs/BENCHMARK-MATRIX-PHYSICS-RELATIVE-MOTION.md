# Benchmark matrix — Motion in 2D › Relative Motion

The reference artifact. Every later subtopic matrix is measured against this one for
completeness, provenance honesty and falsifiability — not for length.

## How to read it

Two architectural decisions govern the whole document, and both come from the
repository's own invariants rather than from this subtopic:

1. **The axis differs per layer.** Core1A/Core1B are indexed by **rung** — a distinct
   conceptual claim — because depth is intrinsic and may not shrink for a learner
   estimated to know more. Core2A/Core2B are indexed by **support and routing**, because
   they are the only two products permitted to read capability evidence or an owner
   waiver. A percentage is a *curriculum coordinate* on the teaching side and a *routing
   input* on the practice side. These are not the same number.
2. **One canonical truth per rung; four projections.** Core1A, Core1B, Core2A and Core2B
   are four questions asked of one node, never four schemas.

## Provenance legend

Extraction is distinguished from synthesis throughout. A cell marked `SYNTHESIS` is a
construction of this matrix and has **no record behind it yet**.

| Tag | Meaning |
|---|---|
| `SOURCE(id)` | verbatim in a committed library or gate record |
| `AUTHORED(id)` | authored into the library in this programme, record exists |
| `SYNTHESIS` | constructed here; **`AUTHOR_REQUIRED`**, no schema home today |
| `ABSENT` | no record and no content exists |

---

## Part 1 — The rung ladder (canonical truth)

| Rung | Target aha | Learner owns coming in | Capability | Provenance |
|---|---|---|---|---|
| **R1** | "Where is it?" has no answer until you say *measured from what*. Position is a **relation**, not a property of the object. | can say where a thing is by pointing or counting paces | — | `ABSENT` |
| **R2** | The trip **from B to A** is an object in its own right, and it is neither position. | R1 | — | `ABSENT` |
| **R3** | Replace two positions from an origin by the displacement from B to A. | signed coordinate-pair arithmetic, available or bridged | `CAP-SAME-TIME` | `SOURCE(MIC-SAME-TIME)` |
| **R4** | Subtract two relative-position equations **before** dividing by a common time interval. | can construct relative position and interpret displacement over time | `CAP-RELATIVE-V` | `SOURCE(MIC-COMMON-INTERVAL)` |
| **R5** | Reconcile the algebraic result with reversal of the observer vector in a geometric construction. | can subtract velocity components; magnitude needs the reviewed right-triangle bridge | `CAP-VECTOR-CHECK` | `SOURCE(MIC-GEOMETRIC-CHECK)` |
| **R6** | The simple subtraction **assumes** non-rotating, non-relativistic frames; naming when it needs qualification is the skill. | R5 | — | `SOURCE(MIC-FRAME-QUALIFICATION-BOUNDARY)`, non-assessment |

### Governing relations

| Relation | Expression | Conditions | Provenance |
|---|---|---|---|
| `REL-RELATIVE-POSITION` | `r_A/B = r_A − r_B` | same instant · parallel non-rotating axes · different instants do not define it · classical model | `SOURCE` |
| `REL-RELATIVE-VELOCITY` | `v_A/B = v_A − v_B` | same times, one common interval · parallel non-rotating axes · classical speeds · a finite-interval average is not automatically instantaneous | `SOURCE` |

**Note on R6.** Its content is already carried by the two relations' `conditions`. The
microtopic's first step says *"restate the two conditions already attached to
`REL-RELATIVE-VELOCITY`"* — attributed restatement, not a second authority. Any later
matrix that restates a relation's conditions **without** that attribution is a finding.

### Misconception, check and closure per rung

| Rung | Misconception | Diagnostic that separates it | Repair | Independent check | Provenance |
|---|---|---|---|---|---|
| R3 | subtract whichever coordinate appears first in the question | which displacement carries you from B to A? | draw origin → B → A and reconstruct `r_A = r_B + r_A/B` before subtracting | if A and B occupy one point, `r_A/B` is zero; reversing A and B reverses the vector | `SOURCE` |
| R4 | subtracting the two speeds always gives relative speed | if one object moves east and the other north, do their directions disappear? | compute signed components first, then magnitude if requested | equal velocities give zero; a stationary observer gives `v_A/B = v_A` | `SOURCE` |
| R5 | a correct length is enough for a correct vector answer | would the same arrow reversed describe the same observer statement? | name the observer, label both components, inspect direction before taking a magnitude | swapping A and B reverses direction, magnitude unchanged | `SOURCE` |

### Vocabulary ceiling — `SYNTHESIS`, no schema home

A scope boundary excludes **content**. A ceiling excludes **words**, because a word can
import the very concept being taught. This column has no field today and is the single
most important gap at the low rungs.

| Rung | May **not** use | Why |
|---|---|---|
| R1 | frame · axis · component · vector · coordinate | each presupposes that direction is already representable |
| R2 | subtract · component · magnitude | the trip must be named before it is computed |
| R3 | velocity · rate | R3 is a statement about one instant |
| R4 | magnitude-before-components | the misconception at this rung *is* reaching for magnitude early |

**Measured failure this catches:** `MIC-VECTOR-VS-SCALAR` explains a vector using seven
terms — frame, axes, perpendicular, component, magnitude, right-triangle, vector — that
its `entry_assumptions` never declare. Every gate in the repository passes it.

**Corrected, after the offloaded matrices inherited the error.** Undeclared on entry and
*belongs on the ceiling* are different tests, and putting the seven under this heading
conflated them. A rung's own output is undeclared by construction — that is what teaching
is. Only the **borrowed** terms are ceiling words:

| | |
|---|---|
| frame · axes · perpendicular · right-triangle | borrowed and never declared — **ceiling** |
| component · magnitude · vector | what this microtopic builds — **its output** |

A ceiling that forbids a rung's own output makes the rung unwritable: the repair for
"a magnitude is not a component" cannot be written without either word.
`ceiling_audit.py` enforces the distinction. The unit-1 matrix copied all seven from this
table and three had to be removed, so the error here propagated exactly once before a
gate caught it.

---

## Part 2 — Core1A and Core1B: same rung, different agency

They never differ in rung. They differ in **who makes the decision**.

| Rung | Core1A — reveal the completed construction | Core1B — elicit the decision first |
|---|---|---|
| R3 | follow origin → B → A; subtract `r_B` from both sides | `AUTHORED`: predict which way you would walk from B to A before subtracting anything |
| R4 | write relative position at `t1` and `t2`; group; divide by one `Δt` | `AUTHORED`: predict A-east-3 / B-north-4 relative speed, and whether `4 − 3` gives it |
| R5 | reverse `v_B`; add tail-to-head; compare components and reverse observer order | `AUTHORED`: predict `v_B/A` from `v_A/B` without calculating — direction and size |

### Controlled variation — `SYNTHESIS`, **phases required**

One `hold_constant` cannot describe an experience whose invariant changes partway. R5
needs two phases; so does any "see the invariance, then break it" design.

| Rung | Phase | Vary | Hold | Notice |
|---|---|---|---|---|
| R3 | 1 | the instant B is read | A's reading | a separation appears that never existed |
| R4 | 1 | the two directions to perpendicular | both speeds | nothing cancels; `4 − 3 = 1` where the answer is 5 |
| R5 | 1 | which object is the observer | the pair of motions | the arrow flips; the length does not |
| R5 | 2 | to head-on approach | both speeds at 20 | the answer is 40 — larger than anything present |

`CONTROLLED_EXPERIENCE_SYNTHESIS_AUTHOR_REQUIRED` for every row above.

---

## Part 3 — Core2A: one family, varying support

**Canonical family:** given two motions in a common frame, find one relative to the other.

| | | Provenance |
|---|---|---|
| invariant demand | identify the observer → subtract in that order → keep signs → magnitude only if asked | `SYNTHESIS` |
| difficult move | deciding the **order** from the words "A relative to B" — not the arithmetic | `AUTHORED(Q-AUTHOR-REL-01.answer.difficult_move = 0)` |
| independent check | add your answer to the observer's velocity; it must return A's | `AUTHORED` |
| worked anchor | A at (6,0), B at (0,8) m/s → `v_A/B` = (6,−8), magnitude 10 | `SOURCE(Q-AUTHOR-REL-01)` |

### Support ladder — this is where a knowledge estimate legitimately enters

It may influence only: which family to expose, how much support, whether a bridge is
required, whether transfer is routed. It may **not** infer prerequisite mastery.

| Support | Handed over | Learner supplies | Provenance |
|---|---|---|---|
| high | observer named · axes declared · order stated | arithmetic, then the check | `SYNTHESIS` |
| medium | observer named · axes declared | the order, arithmetic, check | `AUTHORED` (2 hints exist) |
| low | the situation only | observer, axes, order, arithmetic, check | `SYNTHESIS` |

**All three rows are Core2A.** Removing hints does not create transfer — the decision
structure is identical across the ladder. A matrix that presents its low-support row as
Core2B has made the error this benchmark exists to prevent.

---

## Part 4 — Core2B: one row per changed demand

Dimension values are `question_family.demand_dimensions`' own keys, so the repository has
one vocabulary rather than three spellings of four things.

| `transfer.dimension` | Changed demand | `information_not_handed_over` | Repair to | Provenance |
|---|---|---|---|---|
| `model_choice` | two objects on a **rotating** platform: decide whether the relation applies at all | that a validity condition fails | R6 | `SYNTHESIS` |
| `representation_translation` | both objects' **position-time graphs**; find relative velocity | the velocity vectors themselves | R4 | `SYNTHESIS` |
| `novelty` | boat-in-river / aircraft-in-wind: same mathematics, unfamiliar mapping | which quantity plays the observer's role | R3 | `SYNTHESIS` |
| `reasoning_steps` | chain relative velocity into **closest approach** | that separation is least when relative velocity ⊥ separation | R5 | `SYNTHESIS` |

`information_not_handed_over` is what makes collapse mechanical. If a Core2B hint hands
over the row's own withheld information, the task has become Core2A with a label.

---

## Part 5 — Representation demand, derived from `Notice`

A representation is a claim about **what a learner should notice**, so it is derived from
Part 2 and never from the topic's name.

| Rung | Notice to serve | Quantity kind | Primitive | Gate's required labels |
|---|---|---|---|---|
| R3 | a separation that never existed | `POLAR_VECTOR` | `ARROW_FIELD` | `SOURCE(REP-REL-POSITION)`: declared frame, both object positions |
| R4 | perpendicular motions do not cancel | `POLAR_VECTOR` | `ARROW_FIELD` | `SOURCE(REP-RELV-RESULTANT)`: declared frame, resultant labelled |
| R5 ph1 | the arrow flips, the length does not | `POLAR_VECTOR` | `ARROW_FIELD` | `SOURCE(REP-REV-PAIR)`: declared frame, named observer |
| R5 ph2 | 40 from two 20s | `POLAR_VECTOR` | `ARROW_FIELD` | as above |

Quantity kinds are the census's three — `SCALAR`, `POLAR_VECTOR`, `AXIAL_VECTOR`. Relative
motion needs only `POLAR_VECTOR`; **no rung here requires `AXIAL_VECTOR`**, which is why
this subtopic cannot be the benchmark for the out-of-plane convention. Rotation and
magnetism must be.

**Live divergence, unresolved.** The gate declares `REP-REL-POSITION`,
`REP-RELV-RESULTANT`, `REP-REV-PAIR` with `required_labels`; the library declares
`REP-REL-VECTOR` with `required_elements`. They do not correspond and nothing compares
them: `CROSS_LAYER_REPRESENTATION_DIVERGENCE`. The gate already states "declared frame" —
the physics invariant — and the library does not bind to it.

---

## Part 6 — Falsifiers

Mechanical. A matrix that cannot fail these is not a benchmark.

**Ladder**
1. Rung *N*'s `Learner owns` must contain rung *N−1*'s `aha`. R4 owns R3's conclusion; R5 owns R4's. Fails → the rungs are unordered, not graded.
2. Two rungs sharing `Learner owns` **and** `aha` are one microtopic mislabelled as two depths.
3. Every term used in an explanation is in `entry_assumptions`, introduced by a step of that rung, or named in a lower rung. Fails → the explanation assumes its own conclusion.
4. No term from the rung's own ceiling appears in its explanation.

**Teaching pair**
5. Every rung Core1A constructs, Core1B elicits — coverage, not a lighter product.
6. Every reveal names a prompt that precedes it and is itself readable.
7. Every listed misconception is producible by some phase of `Notice`. A misconception with no experience that exposes it is unaddressed.
8. `hold_constant` is true throughout the phase it describes.

**Practice pair**
9. Core2A rows share one decision structure; differing support does not create a new one.
10. Core2B's `hold_constant` must **not** contain the decision structure. If it does, it is Core2A.
11. No Core2B hint discloses that row's `information_not_handed_over`.
12. Every Core2B row has a `builds_on` lineage and a `repair_ref` to a specific rung.

**Representation**
13. Every figure is derived from a `Notice`, and carries a bridge binding picture to symbol to words.
14. Library `required_elements` satisfy the gate's `required_labels` for the same depiction.

**Known inert check.** The A/B gate detects collapse by looking for `ELICITED_REVEAL`
blocks. Question products have none, so falsifiers 9–11 are **not implemented** —
`differentiation.py` returns no findings for the Core2A/Core2B pair. Measured: `pair
CORE2A/CORE2B: A=1 block, B=0 blocks, B reveals=0`. Falsifier 10 is the repair.

---

## Part 7 — Gaps carried forward

| Gap | Status |
|---|---|
| **R1 and R2 do not exist** | `ABSENT`. The library's relative-motion slice is rungs 3–6 of six and is presented as the entry point. By the depth invariant these cannot be produced by teaching R3 more gently — they are different claims needing their own records. |
| Vocabulary ceiling | no schema home |
| Phased controlled variation | no schema home |
| `information_not_handed_over` | no schema home |
| Core2B content | none authored; four rows are `SYNTHESIS` |
| `CROSS_LAYER_REPRESENTATION_DIVERGENCE` | gate and library representations do not correspond; nothing compares them |
| Core2A/Core2B A/B gate | inert by construction |
| R6 Core1B | deliberately undecided — a non-assessment boundary note should not inherit the instructional elicitation contract without a decision |

**Honest summary of this matrix:** 4 rungs source-backed, 2 absent; Core1A and Core1B
authored for the 3 instructional rungs; Core2A partly authored at one support level;
Core2B entirely unauthored. The teaching spine is real. Everything that makes the
practice pair auditable is synthesis, and everything that makes the low rungs reachable
is missing.
