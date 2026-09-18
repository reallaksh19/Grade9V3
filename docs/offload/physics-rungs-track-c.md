# Track C — Fields, waves and light

**Read `docs/OFFLOAD-PHYSICS-RUNG-RECORDS.md` first. It is the contract: the rules, the
four collisions that will break you, the worked sample, and the test run. This file is
your assignment and the parts that are yours alone.**

---

## Your load

| bucket | subtopic | author | report only |
|---|---|---|---|
| `phy-mag-field-lorentz` | Magnetic fields, Lorentz force and electromagnetic induction | **R1 R2 R3 R4 R6** | R5 |
| `phy-elec-current-ohm` | Current electricity, Ohm's law and circuit analysis | **R1 R4 R5** | R2 R3 R6 R7 |
| `phy-osc-shm-waves` | Oscillations, simple harmonic motion and waves | **R1 R3 R4** | R2 R5 |
| `phy-optics-reflection-mirrors` | Reflection and spherical mirrors | **R1 R2 R3** | R4 R5 R6 |

**14 rungs to author, 10 to report.** Measured against the one authored rung that
exists: about **2,620 lines** of JSON across four new packages and four matrix edits.

`phy-mag-field-lorentz` carries `AXIAL_VECTOR` demand, one of only four buckets in Physics.

## Your files, and nobody else's

```
Physics/library/phy-mag-field-lorentz.v1.json          create
Physics/matrices/phy-mag-field-lorentz.rungs.json      edit, only rows you authored
Physics/library/phy-elec-current-ohm.v1.json          create
Physics/matrices/phy-elec-current-ohm.rungs.json      edit, only rows you authored
Physics/library/phy-osc-shm-waves.v1.json          create
Physics/matrices/phy-osc-shm-waves.rungs.json      edit, only rows you authored
Physics/library/phy-optics-reflection-mirrors.v1.json          create
Physics/matrices/phy-optics-reflection-mirrors.rungs.json      edit, only rows you authored
```

Two other tracks are running on eight other buckets. Touching their files is a merge
conflict, not help.

**The one file all three of you will touch: `docs/architecture-manifest.json`.** It is a
generated index and it counts library packages, so adding yours moves it. Regenerate it
(`python3 Shared/tools/build_manifest.py`) and commit it — `--check` is in CI and the test
suite, so a stale one fails your branch. **When it conflicts with another track, never
hand-resolve it: take either side and re-run the generator.** It is deterministic.

## What is specific to you

Your four buckets are independent of each other and of Track A's spine, so order is
yours. You carry the **heaviest reporting load**: 10 quantitative rungs against 14
authorable, and one bucket, `phy-elec-current-ohm`, is majority-blocked (4 of 7).

**Electricity is the one to watch.** Seven rungs, three yours. Its ladder positions are
`10, 22, 34, 46, 60, 74, 88` -- the tightest spacing in Physics, which usually means the
rungs are finely split. If two of your three turn out to share one misconception and one
exit, they are one rung mislabelled as two depths, and merging them is a finding worth more
than authoring both.

**`phy-mag-field-lorentz` has five authorable rungs, the most of any bucket**, and carries
`AXIAL_VECTOR`. Magnetism is one of only two places the out-of-plane convention can be
benchmarked. If a rung turns on which way `B` points, its `controlled_variation` is the
most important block you will write.

**Optics and oscillations need no vectors at all** by the census -- `DIRECTED_PATH` for
optics, `CARTESIAN_PLOT` for oscillations. A rung reaching for vector language in either is
importing something the subtopic does not need.

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
