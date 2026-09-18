# Master offload prompt — author one subtopic's rung records

**Twelve independent tasks, one bucket each. Each agent creates one new library package and
edits one matrix file. Nothing else.**

Paste this whole document to each agent and add one line: *"Your bucket is N."*

---

## 0 · Why 61 rungs have no record

Physics has 14 matrices, 68 rungs, and **7 rungs with a record**. The gap is not neglect:

- The **matrices** are a map — what to teach, in what order, with what vocabulary ceiling.
  Twelve agents filled them in one pass because the schema, the gate and the compiled
  brief already existed.
- The **records** are the territory — the actual teaching. Until `author_brief.py` existed
  there was no contract telling an agent how to produce one the gates would admit, so
  nobody could be handed the job. There is one now, and it has been walked end to end:
  `MIC-MEASURED-FROM` was refused six times and then admitted.

So this is the job that was waiting for its instructions.

### Yes, it is a database — with one qualification that decides your whole task

It is a database with **referential integrity enforced upstream**, so rows are not freely
insertable:

```
engineering gate registry   owns the equations
        ↓ gate_relation_ref
library relation            a bound copy, never a different one
        ↓ relation_refs
microtopic                  the teaching
        ↓ microtopic_ref
matrix rung                 the map
```

A library relation that binds no gate entry is refused: `GATE_RELATION_UNKNOWN`. **Physics
declares 6 gate relations, all for two already-authored buckets, and none for yours.**

That splits your rungs in two, and the split is the first thing you decide:

| | |
|---|---|
| a rung that states a **distinction** | needs no relation. **Author it now.** |
| a rung that states an **equation** | needs a gate relation that does not exist. **Stop and report it.** |

39 of the 61 are conceptual. Those are the deliverable. The other 22 are blocked on
registry work that is not yours and not offloadable — writing an equation into a library
without an upstream owner is exactly the invention every gate here exists to prevent.

---

## 1 · Your assignment

One bucket. Author its **conceptual** rungs; report its quantitative ones.

| # | bucket_id | no record | conceptual — **yours** | quantitative — report only |
|---:|---|---:|---|---|
| 1 | `BUCKET-PHY-ELEC-CURRENT-OHM` | 7 | R1 R4 R5 | R2 R3 R6 R7 |
| 2 | `BUCKET-PHY-FLUID-BERNOULLI-EQUATION` | 5 | R2 R3 R4 | R1 R5 |
| 3 | `BUCKET-PHY-GRAV-UNIVERSAL-LAW` | 5 | R1 R4 R5 | R2 R3 |
| 4 | `BUCKET-PHY-KIN-1D-MOTION` | 4 | R1 R3 | R2 R4 |
| 5 | `BUCKET-PHY-MAG-FIELD-LORENTZ` | 6 | R1 R2 R3 R4 R6 | R5 |
| 6 | `BUCKET-PHY-NLM-FIRST-LAW` | 4 | R1 R2 R3 R4 | — |
| 7 | `BUCKET-PHY-OPTICS-REFLECTION-MIRRORS` | 6 | R1 R2 R3 | R4 R5 R6 |
| 8 | `BUCKET-PHY-OSC-SHM-WAVES` | 5 | R1 R3 R4 | R2 R5 |
| 9 | `BUCKET-PHY-ROT-RIGID-BODY` | 5 | R1 R3 R4 R5 | R2 |
| 10 | `BUCKET-PHY-THERMO-FIRST-SECOND-LAW` | 5 | R1 R3 R4 R5 | R2 |
| 11 | `BUCKET-PHY-VEC-ADD-SUB` | 4 | R3 | R1 R2 R4 |
| 12 | `BUCKET-PHY-WORK-ENERGY-POWER` | 5 | R1 R2 R3 R4 | R5 |

**The conceptual/quantitative column is a keyword heuristic, not authority.** It was
computed from each rung's own text. You decide per rung, and the gate decides whether you
were right. Moving a rung from one column to the other is a legitimate finding — say so in
your report.

**Your files:**

```
Physics/library/<your-slug>.v1.json      the package you create
Physics/matrices/<your-slug>.rungs.json  the matrix, edited only where you authored a rung
```

Your source material is `Physics/candidates/<your-slug>.v1.json` — candidate input under
`packet_authority: NONE`. It is not truth and you may not promote it; it is a place to
look.

---

## 2 · Four collisions that will break you on the first run

Measured by probing the machinery with exactly the package you are about to write. Every
one of these is invisible until twelve agents hit it at once.

**1 · Resource ids are global.** `SRC-CBSE-ADV` declared in two packages is
`LIBRARY_DUPLICATE_ID` — and it raises rather than reporting, so you get a traceback.
Declare your own, suffixed with your slug: `SRC-AUTHOR-NLM`. **Do not re-declare an
external curriculum document a peer already declares.** If your rung needs one, name the
gap in your report and cite your own authored source instead — twelve copies of the CBSE
syllabus under twelve ids is a worse outcome than a named gap.

**2 · Teaching-path step ids are global too.** `RP0-1` used in two microtopics is
`LIBRARY_NESTED_ID_COLLISION`. Namespace every step by its microtopic: `NLM-R1-1`,
`NLM-R1-2`.

**3 · A bucket that supports no product is refused.** `LIBRARY_SUPPORTS_NO_PRODUCT`. A
package with capabilities and microtopics and nothing else is admitted by `intake.py` and
then rejected by the subject sweep. You need **teaching routes** claiming `CORE1A` and
`CORE1B` for your microtopics. This is the single most likely way to lose a run: intake
goes green and you think you are done.

**4 · A bucket with a drawable representation must name its canonical figure.**
`BUCKET_PRIMARY_REPRESENTATION_UNDECLARED`. If you author no representation, omit
`primary_representation_ref` entirely — do not set it to `null`.

---

## 3 · What to do

Dependency-ordered. Each step is checkable before the next.

**Step 1 — read your rung's compiled brief. It is the contract, not a suggestion.**

```
python3 Shared/tools/author_brief.py --subject Physics \
        --bucket <YOUR_BUCKET> --rung R1 --core CORE1A
```

Because the rung has no record, it emits the **rung-authoring** contract: produce a
capability, then the microtopic, then the product — in that order, and never the product
first. It also prints your rung's **vocabulary ceiling**, its **must-contain** list, its
**misconception** and its **controlled variation**. Those came from the matrix and they
bind you.

**Step 2 — one capability per rung, asserting one thing.**
`success_criterion` states a single thing. Two capabilities already in this subject carry a
**discrimination riding inside a procedural prerequisite** — taught by nothing, assessed by
nothing, and they look covered because the words are there. Do not add a third; if your
rung needs both, that is two capabilities.

**Step 3 — the microtopic.** `entry_assumptions`, `inferential_jump`, `teaching_path` with
`why_valid` on every step, the misconception's three parts, `exit_task` with an oracle.

- A step's `output` must **show the changed state**, not describe it. *"two counts of four
  for one chair"* is refused; `door -> chair: 4 paces.  window -> chair: 4 paces.` passes.
- `relation_refs: []` is legal and is what a conceptual rung carries.
- A qualitative exit uses `oracle.no_numeric_claim`, saying why the answer asserts no
  computed value. Silence is not an option; there is a field for every honest answer.

**Step 4 — the `elicitation` block**, which is what makes Core1B a tutor rather than
Core1A with prompts. Four parts, and the schema names them: `predict`, `attempt`,
`reconstruct`, `boundary_test`. `reconstruct.route` is a list of **asks** — a route made of
statements is `teaching_path` under another key, which is exactly how this product once
became the declarative one. A `RUBRIC` closure needs `accepted` and `rejected`.

**Step 5 — teaching routes** claiming `CORE1A` and `CORE1B` for your microtopics. See
collision 3.

**Step 6 — the matrix row.** For each rung you authored, set `provenance: SOURCE`, add
`microtopic_ref`, and **delete `aha`, `learner_owns`, `misconception` and `closure`** — the
record owns them now, and a second copy is a second authority. Keep `ceiling`,
`must_contain` and `controlled_variation`: no record can hold those.

**Step 7 — run §5 and fix until green.**

---

## 4 · The sample — the one rung that exists

`MIC-MEASURED-FROM`, in `Physics/library/relative-motion.v1.json`. It is the entry rung of
relative motion, it is conceptual, and it passed every gate. Read the whole record; this is
its shape.

```jsonc
"inferential_jump": "\"Where is it?\" has no answer until you say measured from what. Position is a relation, not a property of the object.",
"teaching_path": [
  { "id": "RP0-1", "role": "TRANSFORM",
    "action": "Count paces from the door to the chair: four. Now count from the window to the same chair: four again.",
    "why_valid": "Both counts are honest measurements of the same chair, made without moving it, so neither can be dismissed as a mistake.",
    "output": "door -> chair: 4 paces.  window -> chair: 4 paces." }
],
"relation_refs": [],            // conceptual rung: no equation, and this is legal
"exit_task": {
  "oracle": { "no_numeric_claim": "The answer asserts no computed value. It decides whether two descriptions are distinguishable, and the learner's own check is whether a second person can act on what was said." }
}
```

Note what it does **not** do. Its rung's ceiling forbids *frame, axis, axes, component,
vector, coordinate* — and the record uses none of them, anywhere a learner reads. It talks
about paces, doors and windows instead. That is the ceiling working, and
`ceiling_audit.py` now reads your record, not just your matrix row.

---

## 5 · Test run

In order. Each proves something different; a later one passing does not imply an earlier one did.

```bash
# 0 · baseline, before you write anything
python3 Shared/tools/check_subjects.py                      # expect pass
python3 -m unittest discover -s tests -p "test_*.py"        # expect 348 tests OK

# 1 · your package is admissible
python3 Shared/library/intake.py Physics/library/<your-slug>.v1.json

# 2 · THE ONE THAT CATCHES COLLISION 3 -- do not skip because step 1 was green
python3 Shared/tools/check_subjects.py

# 3 · your matrix still agrees with your records
python3 Shared/tools/matrix_conformance.py --enforce
python3 Shared/tools/ceiling_audit.py --enforce

# 4 · the rung is reachable and the plan changed
python3 Shared/tools/author_brief.py --subject Physics --bucket <YOUR_BUCKET> \
        --rung <a rung you authored> --core CORE1A
python3 Shared/tools/resolve_request.py --enforce

# 5 · you broke nothing shared
python3 -m unittest discover -s tests -p "test_*.py"
python3 Shared/tools/capability_collisions.py               # expect the known 4 over 2 stems
python3 Shared/tools/build_manifest.py --check
```

**Read the step-4 brief.** A rung you authored must now print `## Bind to <MIC-…>` instead
of `## STOP -- this rung has no record`. If it still says STOP, the matrix row does not
reference your record and nothing downstream can see your work.

| finding | what you did |
|---|---|
| `NAMED_WITHOUT_DEMONSTRATING` | a step's `output` describes an outcome instead of showing it |
| `ELICITATION` | a `RUBRIC` closure with no `accepted` / `rejected`, or a route of statements |
| `LIBRARY_DUPLICATE_ID` · `LIBRARY_NESTED_ID_COLLISION` | collisions 1 and 2 |
| `LIBRARY_SUPPORTS_NO_PRODUCT` | collision 3: no teaching route |
| `GATE_RELATION_UNKNOWN` | you authored a relation. That rung was quantitative — stop and report it |
| `MATRIX_RESTATES_THE_RECORD` | you left `aha` on a row whose record now owns it |
| `CEILING_WORD_IN_THE_AUTHORED_EXPLANATION` | your teaching uses a word its rung's ceiling forbids |
| `SUBSTANCE_*` | a field duplicates a peer's, is templated, or restates its own type name |

---

## 6 · What is expected

**Deliverable:** one new package and one edited matrix, committed on `p0-foundations`,
with §5 green.

| | your minimum |
|---|---|
| conceptual rungs authored | **every one in your row**, or a reason per rung |
| capabilities | one per rung, one assertion each |
| teaching routes | `CORE1A` and `CORE1B` over your microtopics |
| matrix rows converted | every rung you authored |
| quantitative rungs | **reported, never authored** |

**Report five numbers and one list:** rungs authored; rungs you moved between the two
columns and why; quantitative rungs blocked on the registry, with the equation each would
need; external sources you wanted and did not declare; and everything you could not do.

**The honest-failure clause, and it is not a formality.** A bucket where you authored two
rungs well and explained why the other three could not be done beats one where five rungs
were constructed to fill the table. The gates cannot tell a careful rung from a plausible
one — that is what review is for, and inventing teaching to reach a count is the single
failure this repository exists to prevent.

**Report, never fix, anything outside your two files.** A finding naming another bucket, a
schema, or a gate goes in your report. Do not touch it.

---

## 7 · Orientation

| | |
|---|---|
| branch | `p0-foundations` |
| the record model | `Shared/library/package.schema.json` |
| the worked rung | `MIC-MEASURED-FROM` in `Physics/library/relative-motion.v1.json` |
| your binding contract | `author_brief.py`, per rung — compiled, never written by hand |
| what the candidates are and are not | `Physics/candidates/README.md` |
| the matrix layer you are completing | `docs/OFFLOAD-MASTER-PHYSICS-MATRICES.md` |
| what the stress test found | `docs/STRESS-PHYSICS.md` |
