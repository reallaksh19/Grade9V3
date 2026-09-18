# Offload brief — close the named gaps on one imported candidate

**Twelve independent tasks, one per packet. Run them in parallel; they share no files.**

Everything needed is here. Do not read the other eleven.

---

## Your packet

```
Physics/candidates/<packet>.v1.json         the imported candidate
Physics/candidates/<packet>.v1.gaps.json    what the source had no field for
```

Pick one packet name and work only on those two files. A second agent is working on
another packet in the same directory; touching its files is a merge conflict, not help.

## What these are

Twelve packets from a parallel Physics track, imported under the C5 contract:
`DIGEST_PINNED_CANDIDATE_SOURCE_ONLY`, `packet_authority: NONE`. Each pins the digest of
the packet it came from. Measured, across all twelve:

| | |
|---|---:|
| microtopics | 12 |
| relations · representations · data · questions · capabilities | **0** |

One microtopic per packet and nothing else, with **204 named gaps**: 144
`SIL_FIELD_ABSENT`, 36 `IMPORTER_INFERRED`, 24 `TTU_CANDIDATE_NOT_PROMOTED`.

Your job is to draft what the source has no field for, **marked as a draft**. Not to
promote anything.

---

## The three rules, in order of how badly breaking them ends

**1 · Never invent to satisfy a gate.** The importer refuses to, and so do you. A
packet's TTU scaffolds are candidate input under the C5 mapping, not exit tasks; its
misconception cues are repairs with no diagnostic prompt behind them. Writing the missing
halves produces exactly the plausible-looking teaching this library exists to keep out.
Where you cannot source it, the field stays absent and the gap stays named.

**2 · Everything you write carries `AUTHOR_REQUIRED`.** You are drafting for review. A
gap you close must cite the source field it came from. A gap you cannot close stays in
the gaps file with a sharper reason than it had.

**3 · The file stays in `Physics/candidates/`.** Never move it to `Physics/library/`.
`packet_authority: NONE` means it is source, not subject truth, and the subject sweep
refuses a candidate found in a library: `CANDIDATE_IN_LIBRARY`. Promotion is an owner
decision after review.

---

## What the library will demand, so you can see the shape

These are the gates a record must eventually pass. You are not required to reach them —
you are required not to fake them.

| Gate | Refuses |
|---|---|
| `intake.py` | a microtopic with no entry assumption, no inferential jump, a step that asserts without justifying, a misconception missing any of its three parts, an exit task with no oracle |
| `substance.py` | a field whose text duplicates a peer's, is templated across records, or restates its own type name |
| `authority.py` | a relation restating gate-owned `expression`, or dropping a validity condition |
| `depiction.py` | a representation whose `kind` the subject contract does not declare |
| `capability_collisions.py` | a `success_criterion` asserting two things — in particular a **discrimination** riding inside a procedural prerequisite. Two already exist in this subject and both are untaught. Do not add a third. |

## Two traps specific to this task

**The `IMPORTER_INFERRED` gaps are not yours to confirm.** The importer guessed a step
role from an atom kind. A guess you agree with is still a guess; mark it reviewed, do not
promote it to fact.

**A `success_criterion` asserts one thing.** `CAP-SIGNED-PAIR` reads *"preserve east/north
signs **and distinguish a point from a displacement**"* — a conceptual rung riding inside
an arithmetic prerequisite, taught by nothing and assessed by nothing, and it looks
covered because the words are there. If your packet needs both, that is two capabilities.

---

## Done when

```
python3 Shared/library/intake.py Physics/candidates/<packet>.v1.json
python3 Shared/tools/check_subjects.py
python3 Shared/tools/capability_collisions.py
python3 -m unittest discover -s tests -p "test_*.py"
```

- the suite is green and `check_subjects` passes — your file must not break either
- `intake.py` reports **fewer findings than before**, and every one it still reports is
  named in the gaps file with a reason
- the gaps file accounts for every gap you did not close
- `packet_authority` is still `NONE` and `packet_digest` is unchanged
- no field you wrote lacks `AUTHOR_REQUIRED`

Report three numbers: gaps closed, gaps sharpened, gaps untouched and why. A packet where
you closed nothing but explained all seventeen precisely is a **successful** run — the
source genuinely may not carry that content, and saying so is the deliverable.

---

## Orientation

| | |
|---|---|
| branch | `p0-foundations` |
| the record model | `Shared/library/package.schema.json` |
| why the importer refuses to fill | `Shared/library/import_sil.py` docstring |
| what the candidates are and are not | `Physics/candidates/README.md` |
| the standard for marking synthesis | `docs/BENCHMARK-MATRIX-PHYSICS-RELATIVE-MOTION.md`, provenance legend |
