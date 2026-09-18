# Track A — Mechanics spine

**Read `docs/OFFLOAD-PHYSICS-RUNG-RECORDS.md` first. It is the contract: the rules, the
four collisions that will break you, the worked sample, and the test run. This file is
your assignment and the parts that are yours alone.**

---

## Your load

| bucket | subtopic | author | report only |
|---|---|---|---|
| `phy-vec-add-sub` | Vector addition, subtraction and orientation | **R3** | R1 R2 R4 |
| `phy-kin-1d-motion` | One-dimensional motion | **R1 R3** | R2 R4 |
| `phy-nlm-first-law` | Newton's first law and free-body diagrams | **R1 R2 R3 R4** | — |
| `phy-work-energy-power` | Work, energy and power | **R1 R2 R3 R4** | R5 |

**11 rungs to author, 6 to report.** Measured against the one authored rung that
exists: about **2,170 lines** of JSON across four new packages and four matrix edits.

`phy-vec-add-sub` carries the only `AXIAL_VECTOR` demand in your track (a cross-product result).

## Your files, and nobody else's

```
Physics/library/phy-vec-add-sub.v1.json          create
Physics/matrices/phy-vec-add-sub.rungs.json      edit, only rows you authored
Physics/library/phy-kin-1d-motion.v1.json          create
Physics/matrices/phy-kin-1d-motion.rungs.json      edit, only rows you authored
Physics/library/phy-nlm-first-law.v1.json          create
Physics/matrices/phy-nlm-first-law.rungs.json      edit, only rows you authored
Physics/library/phy-work-energy-power.v1.json          create
Physics/matrices/phy-work-energy-power.rungs.json      edit, only rows you authored
```

Two other tracks are running on eight other buckets. Touching their files is a merge
conflict, not help.

**The one file all three of you will touch: `docs/architecture-manifest.json`.** It is a
generated index and it counts library packages, so adding yours moves it. Regenerate it
(`python3 Shared/tools/build_manifest.py`) and commit it — `--check` is in CI and the test
suite, so a stale one fails your branch. **When it conflicts with another track, never
hand-resolve it: take either side and re-run the generator.** It is deterministic.

## What is specific to you

Your four buckets are the **prerequisite spine of the whole subject**: vectors feed
kinematics, kinematics feeds the laws of motion, and those feed work and energy. Two
consequences you own that the other tracks do not.

**Order matters here and nowhere else.** Author `phy-vec-add-sub` first, then
`phy-kin-1d-motion`, then `phy-nlm-first-law`, then `phy-work-energy-power`. A capability
you declare in the first is one a later bucket may legitimately name as a
`prerequisite_refs` entry. Authoring out of order means either inventing a forward
reference or leaving a real dependency unstated.

**`phy-vec-add-sub` is one rung and it is the hardest one in your track.** R3 is the only
conceptual rung in a bucket whose other three are quantitative, and the subject already
carries two capabilities with a discrimination riding inside an arithmetic prerequisite --
`CAP-SIGNED-PAIR` and `CAP-RIGHT-TRIANGLE`, both untaught. If R3 turns out to *be* one of
those two riders, that is a finding the owner is waiting for. Say so; do not resolve it,
and do not add a third.

**`phy-nlm-first-law` is the only bucket in Physics with no quantitative rungs at all.**
All four are yours. It is also what the `FREE_BODY_DIAGRAM` renderer has been blocked on
since the roadmap was written -- not by an import, by exactly this content. You are not
asked to author the renderer or any representation; you are asked to notice if a rung's
`notice` line cannot be served without one, and say so.

## Done when

```bash
python3 Shared/tools/check_subjects.py            # the one that catches a missing route
python3 Shared/tools/matrix_conformance.py --enforce
python3 Shared/tools/ceiling_audit.py --enforce
python3 Shared/tools/resolve_request.py --enforce
python3 Shared/tools/build_manifest.py            # regenerate, then commit
python3 -m unittest discover -s tests -p "test_*.py"
```

For each bucket, the brief for a rung you authored must print `## Bind to <MIC-…>` and no
longer `## STOP -- this rung has no record`. If it still says STOP, the matrix row does not
reference your record and nothing downstream can see your work.

**Report:** rungs authored per bucket; rungs you moved between the author and report
columns and why; each reported rung with the equation it would need; external sources you
wanted and did not declare; and what you could not do.

A bucket where you authored two rungs well and explained why the rest could not be done
beats one where five were constructed to fill the table. The gates cannot tell a careful
rung from a plausible one.
