# C6 pilot — NEETPrep Relative Motion Mini Q Bank

Source supplied by owner:

`https://www.neetprep.com/questions/3064-Physics/678-Motion-Plane?courseId=8&testId=2327306-Mini-Q-Bank--Motion-Plane&subtopicId=296-Relative-Motion`

Accessed: 2026-09-18

## Source role

This page is used as **external question-demand evidence** for a real Relative Motion study
session. It is not imported as curriculum authority and its questions are not promoted to
Core2/source custody merely because they appear in this pilot.

The repository stores only transient question identifiers plus short demand summaries needed
for capability mapping. It does not copy the full question bank.

## Text-visible question set

The supplied Relative Motion view exposes eight questions on the page.

### Routable with the current v1 content

The following six text-visible questions now map cleanly to the existing capability graph. Q4/Q5 became routable only after the Vector Addition/Decomposition content completion; all mappings remain transient demand evidence:

| External item | Demand summary | Primary | Secondary |
| --- | --- | --- | --- |
| Q1 | walking observer + vertical rain; relative speed magnitude | `CAP-RELATIVE-V` | `CAP-VECTOR-CHECK`, `CAP-RIGHT-TRIANGLE` |
| Q2 | boat and water velocities in the same ground frame; correct subtraction order | `CAP-RELATIVE-V` | `CAP-VECTOR-CHECK` |
| Q3 | symbolic rain/runner perpendicular relative-speed case | `CAP-RELATIVE-V` | `CAP-VECTOR-CHECK`, `CAP-RIGHT-TRIANGLE` |
| Q4 | river crossing directly opposite; component cancellation plus velocity composition | `CAP-VEC-ADD-DECOMPOSE` | `CAP-RELATIVE-V` |
| Q5 | shortest-path river crossing; perpendicular-resultant constraint plus magnitude check | `CAP-VEC-ADD-DECOMPOSE` | `CAP-RELATIVE-V`, `CAP-RIGHT-TRIANGLE` |
| Q7 | perpendicular chase/intercept; catch time from relative frame geometry | `CAP-RELATIVE-V` | `CAP-RIGHT-TRIANGLE`, `CAP-VECTOR-CHECK` |

These mappings remain `AGENT_PROPOSAL`.

Fixture:

`tests/fixtures/real_pilots/neetprep-relative-motion.worksheet.json`

## Newly routable river-crossing demand

Q4 and Q5 previously exposed a real content gap: general vector addition/decomposition and component cancellation. That gap is now represented by `CAP-VEC-ADD-DECOMPOSE` with canonical teaching and verification. The questions remain external/transient; only their capability mappings are stored.

The key learner route is:

```text
declare axes
→ represent current and swimmer as signed components
→ impose the required resultant direction
→ cancel the unwanted component
→ use relative-motion composition
→ use the Mathematics right-triangle bridge only when a magnitude is required
```

Do not copy either external question into Core2 merely because it is now routable.

## Questions still intentionally not forced into the current map

### Q6 — two projected particles

The text capture says the particle geometry/speeds are given in a figure. Without that figure,
the exact demand cannot be mapped safely. Relative horizontal motion is plausible, but the
pilot must not infer missing geometry.

Disposition:

```text
FIGURE_REQUIRED
```

### Q8 — two runners around a square track

The direction/path arrangement is provided by a figure. The text alone is insufficient to
decide whether the intended model is same-direction/opposite-direction perimeter motion or
another track relation.

Disposition:

```text
FIGURE_REQUIRED
```

## What this source tells us

This is stronger validation than a hand-picked single question.

The bank contains:

- easy direct observer-frame subtraction;
- symbolic and numerical perpendicular-component cases;
- a harder intercept case;
- river-crossing questions that require vector composition beyond the current ready content;
- figure-dependent questions where safe ingestion requires preserving the visual source.

That is exactly the behavior the v1 architecture should expose: some questions route
immediately, some reveal a content gap, and some remain unresolved until source information
is complete.

## First practical learner session

Use the six routable text-visible questions as demand evidence, while keeping Q4/Q5 behind the Vector Addition/Decomposition teaching route when learner evidence is missing or uncertain.

No learner knowledge percentage is assumed by this pilot. If the parent supplies an estimate,
the runner may use it as a starting coordinate; otherwise the study route begins
conservatively from the prerequisite chain.

The session should record only actual attempt outcomes and help used. External questions stay
transient throughout diagnosis and repair.

## Anti-drift

- Do not copy the NEETPrep question bank into canonical question records.
- Q4/Q5 are routable only because their required vector-addition/decomposition teaching now exists; do not weaken readiness checks to preserve that result.
- Do not map Q6/Q8 until the required figures are available.
- Do not treat NEETPrep difficulty percentages as learner evidence.
- Do not treat site labels such as Level 1/2/3 as our ladder coordinates.
- Do not infer academic review/source custody from successful routing.
