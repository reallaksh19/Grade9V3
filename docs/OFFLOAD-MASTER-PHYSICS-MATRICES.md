# Master offload prompt — one Physics subtopic matrix per agent

**Thirteen independent tasks. Each agent writes exactly one new file and edits nothing
else. Measured: they share no files, not even the manifest.**

Paste this whole document to each agent and add one line: *"Your unit is N."*

---

## 0 · What you are building, and why it is a separate layer

A **subtopic matrix** is the human-authored half of the production pipeline: the ladder of
rungs for one subtopic, each rung's vocabulary ceiling and controlled experience, the
question family, and the transfer rows.

```
Physics/matrices/<slug>.rungs.json     <- the one file you create
Shared/library/matrix.schema.json      <- what it must conform to
Shared/tools/matrix_conformance.py     <- the gate that reads it
Shared/tools/author_brief.py           <- the only consumer
```

It exists because of what the repository could not answer. Asked to *"create Core1A for
Motion in 2D › relative motion at knowledge 20%"*, the engine had every gate it needed to
refuse bad content and nothing that could say **which rung 20% means**, **what words the
explanation may not use**, or **what the learner must notice**. Those are not properties of
the compiler. They are properties of the subtopic, and this file is where they live.

Two hard consequences, and breaking either is the failure this layer was built to prevent:

**The matrix never reaches a learner.** It feeds the authoring brief and never the product
compiler. A claim you write here is read by the next author, not published. So a matrix
that is wrong misleads an author; a matrix that is *authoritative* would publish unchecked
teaching, which is why it may not restate any record.

**`ladder_position` is a curriculum coordinate, never a learner estimate.** Teaching depth
is intrinsic and may not shrink because a learner is thought to know more. A percentage
*selects* an entry rung on the teaching side; it *routes support* on the practice side.
These are two different readings of one number and the brief performs both — see §4.

### Never offloaded

Learner data. `Learners/profiles/` is owner-written. An agent may write a profile only
with `provenance: SYNTHETIC_TEST`, and `learner_evidence.py` refuses to route one:
`SYNTHETIC_PROFILE_ROUTED`. Do not touch that directory for this task.

---

## 1 · The subtopics — detailed list

Thirteen units. Unit 0 is already committed and is your reference standard, not an
assignment.

Columns: the bucket the matrix is for; the topic it sits in; the source material you may
read; and the representation demand this subtopic already has, taken from
`docs/MEASURE-PHYSICS-DEPICTION-CENSUS.md`. Every unit demands `SCALAR` and
`TYPESET_EXPRESSION`, so those are not repeated.

| # | bucket_id | topic | source | also demands |
|---:|---|---|---|---|
| **0** | `BUCKET-RELATIVE-MOTION` | Motion in two dimensions | **committed library** | `POLAR_VECTOR` · `ARROW_FIELD` |
| **1** | `BUCKET-VECTOR-REPRESENTATION` | Motion in two dimensions | **committed library** | `POLAR_VECTOR` · `ARROW_FIELD` |
| 2 | `BUCKET-PHY-NLM-FIRST-LAW` | Laws of Motion | `phy-nlm-first-law.v1` | `POLAR_VECTOR` · `ARROW_FIELD` |
| 3 | `BUCKET-PHY-KIN-1D-MOTION` | Motion | `phy-kin-1d-motion.v1` | `POLAR_VECTOR` · `ARROW_FIELD` · `DIRECTED_PATH` · `CARTESIAN_PLOT` · `MARKED_AXIS` |
| 4 | `BUCKET-PHY-VEC-ADD-SUB` | Vectors / Motion in a Plane | `phy-vec-add-sub.v1` | `POLAR_VECTOR` · **`AXIAL_VECTOR`** · `ARROW_FIELD` |
| 5 | `BUCKET-PHY-WORK-ENERGY-POWER` | Work and Energy | `phy-work-energy-power.v1` | `POLAR_VECTOR` · `ARROW_FIELD` · `DIRECTED_PATH` · `LEVEL_COMPARISON` |
| 6 | `BUCKET-PHY-GRAV-UNIVERSAL-LAW` | Gravitation | `phy-grav-universal-law.v1` | `POLAR_VECTOR` · **`AXIAL_VECTOR`** · `ARROW_FIELD` · `DIRECTED_PATH` |
| 7 | `BUCKET-PHY-ROT-RIGID-BODY` | System of Particles and Rotational Motion | `phy-rot-rigid-body.v1` | `POLAR_VECTOR` · **`AXIAL_VECTOR`** · `ARROW_FIELD` |
| 8 | `BUCKET-PHY-OSC-SHM-WAVES` | Oscillations | `phy-osc-shm-waves.v1` | `CARTESIAN_PLOT` |
| 9 | `BUCKET-PHY-FLUID-BERNOULLI-EQUATION` | Mechanical Properties of Fluids | `phy-fluid-bernoulli-equation.v1` | `POLAR_VECTOR` · `ARROW_FIELD` · `DIRECTED_PATH` |
| 10 | `BUCKET-PHY-THERMO-FIRST-SECOND-LAW` | Thermodynamics | `phy-thermo-first-second-law.v1` | `CARTESIAN_PLOT` |
| 11 | `BUCKET-PHY-ELEC-CURRENT-OHM` | Electricity | `phy-elec-current-ohm.v1` | `POLAR_VECTOR` · `ARROW_FIELD` · `CARTESIAN_PLOT` · `NODE_NETWORK` |
| 12 | `BUCKET-PHY-MAG-FIELD-LORENTZ` | Magnetic Effects of Electric Current | `phy-mag-field-lorentz.v1` | `POLAR_VECTOR` · **`AXIAL_VECTOR`** · `ARROW_FIELD` |
| 13 | `BUCKET-PHY-OPTICS-REFLECTION-MIRRORS` | Light - Reflection and Refraction | `phy-optics-reflection-mirrors.v1` | `DIRECTED_PATH` |

Candidate sources are `Physics/candidates/<slug>.v1.json` with their gaps beside them in
`<slug>.v1.gaps.json`. Committed sources are `Physics/library/<slug>.v1.json`.

### The one thing that differs between unit 1 and units 2–13

`matrix_conformance.py` reads whether a rung exists from **`<Subject>/library/` only**.
Candidates are `packet_authority: NONE` — source, not subject truth — so the library does
not hold them.

- **Units 2–13:** no library record exists for your subtopic. Every rung row is
  `SYNTHESIS` or `ABSENT`. A row claiming `SOURCE` or `AUTHORED` fails
  `PROVENANCE_DISAGREES_WITH_LIBRARY`, and that gate is correct — claiming a record exists
  does not make one.
- **Unit 1:** four records exist and your rows must reference them by
  `microtopic_ref` with `provenance: SOURCE`, carrying **no** `aha`, `learner_owns`,
  `misconception` or `closure`, because the record owns those:

  | microtopic_ref | teaches |
  |---|---|
  | `MIC-VECTOR-VS-SCALAR` | magnitude, vector and signed component as different descriptions |
  | `MIC-SIGNED-COMPONENT` | the axis choice is free and declared; after that every component is signed |
  | `MIC-GRAPHICAL-SUBTRACTION` | `P − Q` as `P + (−Q)`: reverse without rescaling, then tail-to-head |
  | `MIC-FRAME-QUALIFICATION-BOUNDARY` | when the simple subtraction needs frame qualification (non-assessment) |

  Unit 1 is the highest-value unit for one measured reason. `MIC-VECTOR-VS-SCALAR`
  explains a vector using seven terms — frame, axes, perpendicular, component, magnitude,
  right-triangle, vector — that its own `entry_assumptions` never declare, and **every gate
  in the repository passes it**. Writing that rung's ceiling is the first time that defect
  becomes nameable. Do not edit the microtopic; write the ceiling that indicts it.

---

## 2 · What to do

Work in this order. Each step is checkable before the next, and the order is enforced by
dependency rather than instruction.

**Step 1 — read, and write down the jumps before writing any JSON.**
Read your source packet (or the committed package for unit 1) and
`docs/BENCHMARK-MATRIX-PHYSICS-RELATIVE-MOTION.md` end to end. Then list, in prose, the
distinct **inferential jumps** this subtopic needs. One jump per rung.

A rung is **one inferential jump**: a microtopic plus a verified position in a prerequisite
chain. Three criteria decide whether a candidate is one rung:

- **irreducible** — it cannot be split into two claims a learner could hold separately
- **one misconception** — there is a single wrong idea it is the job of this rung to kill
- **one observable exit** — one thing a learner can be asked to do that shows they have it

If a candidate has two misconceptions, it is two rungs. If you cannot state its exit as an
observable action, it is not a rung yet and you do not know what it is.

**Step 2 — order them, and leave the holes visible.**
Assign `ladder_position` 0–100, strictly ascending. Positions are spacing, not scores: the
gap between 20 and 55 in unit 0 records that a rung is missing there.

**A missing rung is a row, not an omission.** Write it with `provenance: ABSENT` and an
`aha` that names the hole. Note that unit 0 does **not** do this — it names `R2` in the
benchmark's prose and skips it in the file, which is why nothing can see that hole
mechanically. Do the better thing; the schema's own wording asks for it.

**Step 3 — per rung, write what no record can hold.**
Every rung, source-backed or not, gets these three. They have no schema home in the
library, which is exactly why the matrix exists:

- `ceiling[]` — words the explanation may **not** use, because each presupposes what this
  rung teaches. A scope boundary excludes *content*; a ceiling excludes *vocabulary*, and
  they are different fences. This is the highest-value field in the file.
- `must_contain[]` — what the explanation must contain to be this rung at all.
- `controlled_variation[]` — phased. Per phase: what you **vary**, what you **hold**, what
  the learner should **notice**. Phased because an experience whose invariant changes
  partway cannot be described by one hold. Phase 1 shows the invariance; a later phase
  breaks it.

**Step 4 — per rung with no record, write the four the record would have owned.**
`aha`, `learner_owns[]`, `misconception{wrong_idea, diagnostic_prompt, repair}`, `closure`.
Mark the row `SYNTHESIS`. If you cannot construct all four honestly, mark it `ABSENT` and
carry only `aha`. That is a legal, tested answer — see §3.

**Step 5 — the question family, and what support hands over.**
`family{invariant_demand, difficult_move, independent_check}`. One family for the subtopic:
what every instance demands, which single move is actually hard, and the check that
confirms an answer without re-deriving it.

Then `family.support_ladder[]` — one row per support level (`high`, `medium`, `low`,
optionally `minimum`), each saying what is **handed over** at that level. The engine holds
the thresholds and nothing else: what support means is a property of your subtopic, and
until you write it the brief prints `AUTHOR_REQUIRED` and names the missing row.

Every row is the **same product**. Removing help does not create transfer — the decision
structure is unchanged across the whole ladder. And no row may hand over the
`invariant_demand` itself: that removes the decision, and what is left is transcription.
`SUPPORT_HANDS_OVER_THE_DEMAND` refuses it.

`difficult_move` is where most matrices go wrong. In unit 0 it is *"deciding the
subtraction order from the words 'A relative to B'"* — a **reading** decision, not
arithmetic. Name the move that fails, not the longest step.

**Step 6 — the transfer rows.**
One row per changed demand. `dimension` must be one of the four this subject already
declares — `model_choice`, `representation_translation`, `reasoning_steps`, `novelty` — and
a fifth spelling of these four is refused by name.

Per row: `changed_demand`, `information_not_handed_over`, `repair_to` (a rung of *your*
ladder).

`information_not_handed_over` is the load-bearing field. It is what makes collapse
mechanical: if a Core2B hint hands over that row's withheld information, the task has
silently become Core2A with a label. It must be **narrower** than `changed_demand` — if
they are the same sentence the row says nothing a hint could violate.

**Step 7 — run §6, fix, commit.**

---

## 3 · Best practices

**Never invent to satisfy a gate.** Every gate here is built so that the honest answer is
available. `ABSENT` exists so you can say *"there is a rung here and I could not construct
it"* without fabricating a misconception for it. A matrix whose rows are all `SYNTHESIS`
because `ABSENT` felt like failure is worse than one with four honest holes.

**Reference, never copy.** Where a record exists it owns its jump, entry state,
misconception and exit task. A matrix restating them is a second authority for one claim
and the two will drift. `MATRIX_RESTATES_THE_RECORD` refuses it.

**The library decides.** A row may claim `SOURCE` for a rung nobody authored, and the gate
resolves that disagreement against the library every time. Never in the other direction.

**A ceiling is not a style note.** It is a list of words, and the test is mechanical: does
the word presuppose the thing this rung teaches? "Frame" at a rung teaching that position
is relative does — you cannot use it to explain what it is. "Metre" does not.

**Hold must be true throughout its phase.** `PHASE_HOLDS_NOTHING` catches an empty hold; no
gate catches a false one. A phase whose invariant breaks halfway is two phases.

**One misconception per rung, with all three parts.** Wrong idea, the diagnostic that
separates it from the right idea, and the repair. A repair with no diagnostic behind it is
the defect the twelve candidate packets already carry — their misconception cues are
repairs with nothing that would detect the wrong idea. Do not reproduce it.

**Do not read the other twelve units.** Everything you need is your source packet, the
benchmark, and the schema. Touching a neighbour's file is a merge conflict, not help.

**Do not edit any record, gate, schema or test.** If you believe the schema cannot express
what your subtopic needs, that is a finding to report, not a change to make. A field added
to serve one subtopic is the blueprint being bent to a case, which is the one thing this
architecture forbids.

---

## 4 · Sample — the committed unit 0, verbatim

`Physics/matrices/relative-motion.rungs.json` passes every gate today. These are the two
row shapes and both bottom blocks, copied from it.

**A rung with no record** — carries the four the record would have owned, plus the three no
record can hold:

```json
{
  "rung": "R1",
  "ladder_position": 20,
  "provenance": "SYNTHESIS",
  "aha": "\"Where is it?\" has no answer until you say measured from what. Position is a relation, not a property of the object.",
  "learner_owns": ["Can say where a thing is by pointing or counting paces."],
  "ceiling": ["frame", "axis", "axes", "component", "vector", "coordinate"],
  "must_contain": [
    "Two situations carrying the same number that are not the same situation.",
    "The direction said in words before any symbol or drawing appears."
  ],
  "misconception": {
    "wrong_idea": "Position is a property the object carries with it.",
    "diagnostic_prompt": "Two people give different answers for where the same chair is. Can both be right?",
    "repair": "Say what you measured from, then give the number; the number alone is not the answer."
  },
  "closure": "Given two descriptions with identical numbers, say whether they describe the same thing, and why.",
  "controlled_variation": [
    {
      "phase": 1,
      "vary": "who is doing the measuring",
      "hold": "the two objects, fixed in the room",
      "notice": "the answer to \"where is A\" changes while nothing physical has moved"
    }
  ]
}
```

**A rung with a record** — references it and carries nothing the record owns. Note the two
phases: phase 1 shows the invariance, phase 2 breaks it.

```json
{
  "rung": "R5",
  "ladder_position": 85,
  "provenance": "SOURCE",
  "microtopic_ref": "MIC-GEOMETRIC-CHECK",
  "must_contain": ["The reversed vector drawn from the head of the first, not the origin."],
  "controlled_variation": [
    {"phase": 1, "vary": "which object is the observer", "hold": "the pair of motions",
     "notice": "the arrow flips; the length does not"},
    {"phase": 2, "vary": "to head-on approach", "hold": "both speeds at 20 m/s",
     "notice": "the answer is 40 -- larger than anything present"}
  ]
}
```

**The family and one transfer row:**

```json
"family": {
  "invariant_demand": "Identify the observer, subtract in that order, keep both signs, and take a magnitude only if the question asked for one.",
  "difficult_move": "Deciding the subtraction order from the words \"A relative to B\", which is a reading decision rather than arithmetic.",
  "independent_check": "Add the answer to the observer's velocity; it must return A's.",
  "support_ladder": [
    {"level": "high",   "handed_over": "The observer is named, the axes are declared, and the subtraction order is stated."},
    {"level": "medium", "handed_over": "The observer is named and the axes are declared."},
    {"level": "low",    "handed_over": "The situation only."}
  ]
},
"transfer": [
  {
    "dimension": "model_choice",
    "changed_demand": "Two objects on a rotating platform: decide whether the relation applies.",
    "information_not_handed_over": "that a validity condition of the relation fails here",
    "repair_to": "R5"
  }
]
```

### What your file consumes it for

This is the whole point of the layer, so run it and read the output before you write
anything:

```
python3 Shared/tools/author_brief.py --subject Physics \
        --bucket BUCKET-RELATIVE-MOTION --knowledge 20 --core CORE1A
```

It resolves `20%` against the ladder — `R1=20, R3=55, R4=70, R5=85` → `R1` — then, because
`R1` has no record, refuses to emit a product brief at all and emits the **rung-authoring**
contract instead. Authoring a product against an absent rung is how an existing rung gets
diluted to serve a lower ladder position.

Every field you write appears in that output. A field that never reaches the brief is
decoration; a wrong field is an instruction to the next author.

---

## 5 · What is expected

**Deliverable:** one new file, `Physics/matrices/<slug>.rungs.json`, committed on branch
`p0-foundations`, with the checks in §6 green.

**A complete matrix, measured against unit 0:**

| | unit 0 | your minimum |
|---|---:|---|
| rungs | 4 rows, 2 further holes named in prose | **≥ 3 rows, every hole a row** |
| rungs carrying a `ceiling` | 4 / 4 | **every rung** |
| rungs carrying `controlled_variation` | 4 / 4 | **every rung** |
| rungs carrying ≥ 2 phases | 1 | **≥ 1** |
| `family` | complete | complete |
| `family.support_ladder` rows | 3 | **≥ 2, distinct levels** |
| `transfer` rows | 4, one per dimension | **≥ 2, distinct dimensions** |

**What counts as success, precisely.** A matrix with three rungs where every row is honest
beats eight rows where four were constructed to fill the table. If your source genuinely
does not support a rung, the row says `ABSENT` and names the hole — that is the
deliverable, not the failure.

**Report four numbers and one list:** rungs written; of those, how many `SYNTHESIS` and how
many `ABSENT`; transfer rows; and **the list of things you could not do and why**. That
last list is the part the owner reads.

**Report, never fix, anything outside your file.** If a gate finding names a record, a
schema or another unit, write it in your report. Do not touch it.

---

## 6 · Test run

In order. Each proves something different, and a later one passing does not imply an
earlier one did.

```bash
# 0 · baseline, before you write anything — so you know what was already red
python3 Shared/tools/matrix_conformance.py            # expect findings 0
python3 -m unittest discover -s tests -p "test_*.py"  # expect 299 tests OK

# 1 · your file conforms, and the ladder, phases and transfer rows hold together
python3 Shared/tools/matrix_conformance.py --enforce

# 2 · it is usable: the brief compiles and is not empty
python3 Shared/tools/author_brief.py --subject Physics --bucket <YOUR_BUCKET> \
        --knowledge 20 --core CORE1A
python3 Shared/tools/author_brief.py --subject Physics --bucket <YOUR_BUCKET> \
        --knowledge 80 --core CORE2B

# 3 · you broke nothing shared
python3 -m unittest discover -s tests -p "test_*.py"
python3 Shared/tools/check_subjects.py
python3 Shared/tools/build_manifest.py --check
python3 Shared/tools/capability_collisions.py         # expect the known 4 / 2 stems
```

**Read the step-2 output, do not just check the exit code.** The brief is the deliverable's
real consumer. Three things to look for in it:

1. Every rung you wrote is resolvable — the two `--knowledge` values land on different
   rungs, and each named rung prints its ceiling, its must-contain list and its phases.
2. No brief prints `## Rung X: (from the record)` for a rung you marked `SYNTHESIS` or
   `ABSENT`. That line means the row names nothing and the gate now refuses it —
   `RUNG_NAMES_NO_JUMP`.
3. `--core CORE2B` reads the percentage as a **routing input**, not a ladder position, and
   prints your family, your support ladder row for that level, and every transfer row with
   what it withholds. Missing any of them, it prints `AUTHOR_REQUIRED` or `STOP` and names
   what to write. A `STOP` is a finished, honest brief only if the matching row genuinely
   cannot be written; otherwise it is your remaining work.

**Findings you should expect to see, and what each means:**

| finding | what you did |
|---|---|
| `MATRIX_STRUCTURE` | the file does not match the schema; the path in `where` is the field |
| `RUNG_NAMES_NO_JUMP` | a row with a position and nothing else; a hole must be *visible* |
| `SYNTHESIS_INCOMPLETE` | claimed construction, carried no entry state / misconception / closure — mark it `ABSENT` instead |
| `MATRIX_RESTATES_THE_RECORD` | copied a jump or misconception a microtopic owns |
| `PROVENANCE_DISAGREES_WITH_LIBRARY` | claimed `SOURCE`/`AUTHORED` for a record the library does not hold — for units 2–13 this means you claimed a candidate as subject truth |
| `PROVENANCE_CLAIMS_A_RECORD_WITH_NO_REF` | claimed `SOURCE`/`AUTHORED` and named no microtopic |
| `LADDER_OUT_OF_ORDER` · `LADDER_POSITION_REUSED` · `RUNG_LABEL_REUSED` | the ladder is not a ladder |
| `PHASE_HOLDS_NOTHING` | an experience with no invariant cannot show one |
| `TRANSFER_DIMENSION_UNDECLARED` | a fifth spelling of the four dimensions |
| `TRANSFER_REPAIRS_TO_NO_RUNG` | `repair_to` names a rung your ladder does not have |
| `WITHHELD_RESTATES_THE_DEMAND` | withheld information is not narrower than the demand, so no hint could violate it |
| `SUPPORT_LEVEL_REUSED` | two `support_ladder` rows describe the same level |
| `SUPPORT_HANDS_OVER_THE_DEMAND` | support hands over the invariant demand; the collapse from the support side |

---

## 7 · Benchmarks

### The reference standard

`docs/BENCHMARK-MATRIX-PHYSICS-RELATIVE-MOTION.md`. Every matrix is measured against it
for **completeness, provenance honesty and falsifiability — not for length**. Read its
Part 7, "Gaps carried forward": the benchmark's own honest summary is *"4 rungs
source-backed, 2 absent; Core2B entirely unauthored"*. That is what an honest matrix looks
like.

### The fourteen falsifiers

Counted honestly: **three** are enforced by `matrix_conformance.py` (11, 12, and half of
8 — an *empty* hold is refused, a *false* one is not). Two belong to the product compiler.
**Nine are yours to check by reading**, and a matrix that cannot fail them is not a
benchmark. The gates do not make this file correct; they only keep it from being
structurally impossible.

**Ladder** — by reading:
1. Rung *N*'s `learner_owns` contains rung *N−1*'s `aha`. Fails → the rungs are unordered, not graded.
2. Two rungs sharing `learner_owns` **and** `aha` are one microtopic mislabelled as two depths.
3. Every term in an explanation is in `learner_owns`, introduced by this rung, or named by a lower one. Fails → the explanation assumes its own conclusion.
4. No term from a rung's own `ceiling` appears in its explanation.

**Teaching pair** — 5–6 belong to the products, not the matrix; 7–8 are yours:

7. Every misconception is producible by some phase of `notice`. A misconception no experience exposes is unaddressed.
8. `hold` is true throughout the phase it describes.

**Practice pair** — by reading:
9. Every `transfer` row's `changed_demand` changes the **decision structure**. Removing hints does not create transfer.
10. No `transfer` row's `hold` contains the decision structure. If it does, it is Core2A.
11. `information_not_handed_over` is narrower than `changed_demand` — enforced as `WITHHELD_RESTATES_THE_DEMAND`.
12. Every `transfer` row has a `repair_to` naming a specific rung — enforced.

**Representation** — by reading, against the census:

13. Every phase's `notice` implies a depiction, and the quantity kinds it needs are among the three the census measured: `SCALAR`, `POLAR_VECTOR`, `AXIAL_VECTOR`. If your `notice` needs a fourth, that is new evidence and a finding to report — not a kind to coin.
14. Your subtopic's row in §1 lists the primitives it already demands. If your ladder needs one that is not listed, say so; if it needs none of them, say that too.

**Units 4, 6, 7 and 12 carry the only `AXIAL_VECTOR` demand in Physics.** Unit 0 cannot be
the benchmark for the out-of-plane convention, because no rung in relative motion needs
one. Rotation and magnetism must be. If your unit is one of these four, the rung where an
axial quantity first appears is the most important row in your file.

### Numbers to hold

| | |
|---|---:|
| tests, before and after | **299**, green |
| gates green | **11** |
| `matrix_conformance` findings across all matrices | **0** |
| matrices committed today | 1 of 14 |
| `capability_collisions` findings, unchanged by you | **4** over 2 capability stems |
| files you and your twelve peers share | **0** — verified, the manifest does not move |

### The two capability forks, and why you must not add a third

`capability_collisions.py` reports two records whose `success_criterion` asserts two
things, a **conceptual** clause riding inside a **procedural** prerequisite:

```
CAP-SIGNED-PAIR      "Preserve east/north signs and distinguish a point from a displacement."
CAP-RIGHT-TRIANGLE   "Use the right-triangle relation with nonnegative lengths and
                      distinguish magnitude from signed component."
```

Both riders are untaught and unassessed, and both look covered because the words are
there. A rung hiding inside a delegation is a rung nobody authored. If a rung you are
writing turns out to be one of those two riders, **say so in your report** — that is a
finding the owner is waiting for. Do not resolve it, and do not add a third.

---

## 8 · Orientation

| | |
|---|---|
| branch | `p0-foundations` |
| the schema you conform to | `Shared/library/matrix.schema.json` |
| the gate that reads you | `Shared/tools/matrix_conformance.py` |
| the only consumer | `Shared/tools/author_brief.py` |
| the reference standard | `docs/BENCHMARK-MATRIX-PHYSICS-RELATIVE-MOTION.md` |
| representation demand, measured | `docs/MEASURE-PHYSICS-DEPICTION-CENSUS.md` |
| what the candidates are and are not | `Physics/candidates/README.md` |
| the parallel offload on the same packets | `docs/OFFLOAD-B1-CANDIDATE-GAPS.md` |
| why the axis differs per layer | the benchmark's "How to read it", decision 1 |
| what a percentage may and may not do | `docs/ROADMAP-LEARNER-READY.md` §R5 |

`docs/OFFLOAD-B1-CANDIDATE-GAPS.md` is a different task on the same twelve packets:
closing their named gaps *inside* `Physics/candidates/`. If both run at once, the B1 agent
edits the packet and you create the matrix — no shared file. Neither may promote anything
into `Physics/library/`; the subject sweep refuses it: `CANDIDATE_IN_LIBRARY`.
