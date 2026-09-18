# Track B — Extended mechanics and matter

**Read `docs/OFFLOAD-PHYSICS-RUNG-RECORDS.md` first. It is the contract: the rules, the
four collisions that will break you, the worked sample, and the test run. This file is
your assignment and the parts that are yours alone.**

---

## Your load

| bucket | subtopic | author | report only |
|---|---|---|---|
| `phy-rot-rigid-body` | Rotational dynamics, angular momentum and rolling | **R1 R3 R4 R5** | R2 |
| `phy-grav-universal-law` | Universal gravitation, free fall and orbital motion | **R1 R4 R5** | R2 R3 |
| `phy-fluid-bernoulli-equation` | Fluid statics, buoyancy and Bernoulli flow | **R2 R3 R4** | R1 R5 |
| `phy-thermo-first-second-law` | Thermodynamics and heat engines | **R1 R3 R4 R5** | R2 |

**14 rungs to author, 6 to report.** Measured against the one authored rung that
exists: about **2,620 lines** of JSON across four new packages and four matrix edits.

Rotation and gravitation both carry `AXIAL_VECTOR` demand -- two of the four in Physics.

## Your files, and nobody else's

```
Physics/library/phy-rot-rigid-body.v1.json          create
Physics/matrices/phy-rot-rigid-body.rungs.json      edit, only rows you authored
Physics/library/phy-grav-universal-law.v1.json          create
Physics/matrices/phy-grav-universal-law.rungs.json      edit, only rows you authored
Physics/library/phy-fluid-bernoulli-equation.v1.json          create
Physics/matrices/phy-fluid-bernoulli-equation.rungs.json      edit, only rows you authored
Physics/library/phy-thermo-first-second-law.v1.json          create
Physics/matrices/phy-thermo-first-second-law.rungs.json      edit, only rows you authored
```

Two other tracks are running on eight other buckets. Touching their files is a merge
conflict, not help.

**The one file all three of you will touch: `docs/architecture-manifest.json`.** It is a
generated index and it counts library packages, so adding yours moves it. Regenerate it
(`python3 Shared/tools/build_manifest.py`) and commit it — `--check` is in CI and the test
suite, so a stale one fails your branch. **When it conflicts with another track, never
hand-resolve it: take either side and re-run the generator.** It is deterministic.

## What is specific to you

Your four buckets all **build on Track A's spine** and none of them feed each other, so
you can author them in any order. Pick the one you understand best first: your first bucket
is where you will hit the four collisions in §2 of the master, and it is cheaper to hit
them once on familiar physics.

**Two of your four carry `AXIAL_VECTOR` demand** -- rotation and gravitation both teach
angular momentum and torque. Rotation is, with magnetism, one of only two places in Physics
where the out-of-plane convention can be benchmarked at all; relative motion cannot do it,
because no rung there needs one. If a rung of yours turns on which way an axial quantity
points, that rung's `controlled_variation` is the most important block in your track.

**`phy-thermo-first-second-law` is the odd one out.** Its census demand is
`CARTESIAN_PLOT` and `SCALAR` only -- no vectors anywhere. A rung there that reaches for
vector language is importing something the subtopic does not need, and its ceiling should
probably say so.

**Fluids: R1 is quantitative and R2-R4 are not.** That is unusual -- most buckets start
conceptual. Check it: if R1 really is the entry rung and really needs an equation, then
your bucket has no authorable entry, and the first thing a learner meets is blocked. That
is worth reporting explicitly rather than quietly starting at R2.

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
