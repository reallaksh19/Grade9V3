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

The following four questions map cleanly to the existing Relative Motion capability family:

| External item | Demand summary | Primary | Secondary |
| --- | --- | --- | --- |
| Q1 | walking observer + vertical rain; relative speed magnitude | `CAP-RELATIVE-V` | `CAP-VECTOR-CHECK`, `CAP-RIGHT-TRIANGLE` |
| Q2 | boat and water velocities in the same ground frame; correct subtraction order | `CAP-RELATIVE-V` | `CAP-VECTOR-CHECK` |
| Q3 | symbolic rain/runner perpendicular relative-speed case | `CAP-RELATIVE-V` | `CAP-VECTOR-CHECK`, `CAP-RIGHT-TRIANGLE` |
| Q7 | perpendicular chase/intercept; catch time from relative frame geometry | `CAP-RELATIVE-V` | `CAP-RIGHT-TRIANGLE`, `CAP-VECTOR-CHECK` |

These mappings remain `AGENT_PROPOSAL`.

Fixture:

`tests/fixtures/real_pilots/neetprep-relative-motion.worksheet.json`

## Questions intentionally not forced into the current map

### Q4 — river crossing directly opposite

The learner must combine swimmer-relative-to-water and water-relative-to-ground velocities,
resolve components, and make the along-river component cancel.

The present Relative Motion matrix can express observer-relative velocity, but the durable
general vector-addition/decomposition teaching needed by this question is not yet
`SESSION_READY`.

Disposition:

```text
CONTENT_GAP
→ general vector addition / decomposition
→ component cancellation in a chosen axis system
→ then relative-motion composition
```

Do not stretch `CAP-RELATIVE-V` to pretend this entire demand is already taught.

### Q5 — shortest-path river crossing

This again requires velocity composition plus perpendicular/component geometry. It is useful
real evidence for the same vector-addition/decomposition gap exposed by Q4.

Disposition:

```text
CONTENT_GAP
→ vector addition / decomposition
→ perpendicular resultant constraint
→ right-triangle magnitude relation
```

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

Use the four routable questions first.

No learner knowledge percentage is assumed by this pilot. If the parent supplies an estimate,
the runner may use it as a starting coordinate; otherwise the study route begins
conservatively from the prerequisite chain.

The session should record only actual attempt outcomes and help used. External questions stay
transient throughout diagnosis and repair.

## Anti-drift

- Do not copy the NEETPrep question bank into canonical question records.
- Do not mark Q4/Q5 routable by weakening vector-readiness checks.
- Do not map Q6/Q8 until the required figures are available.
- Do not treat NEETPrep difficulty percentages as learner evidence.
- Do not treat site labels such as Level 1/2/3 as our ladder coordinates.
- Do not infer academic review/source custody from successful routing.


## Post-modernization routing status

The vector-foundation content repair now gives Q4/Q5 a canonical route without stretching
Relative Motion itself.

New reusable capabilities:

```text
CAP-VECTOR-SIGNED-COMPONENT
→ CAP-VEC-COMPONENT-SUM
→ CAP-VEC-RESULTANT-CONSTRAINT
```

The retained transient worksheet mapping now includes:

| External item | Primary | Secondary |
| --- | --- | --- |
| Q4 | `CAP-VEC-RESULTANT-CONSTRAINT` | `CAP-RELATIVE-V` |
| Q5 | `CAP-VEC-RESULTANT-CONSTRAINT` | `CAP-RELATIVE-V`, `CAP-RIGHT-TRIANGLE` |

This does **not** claim full arbitrary-angle trigonometric decomposition. The active content
teaches signed-component composition and an explicit resultant-component constraint. If an
item requires deriving components from an angle using sine/cosine, that remains a separate
provider/content gap rather than being hidden inside vector addition.

The external NEETPrep questions remain transient demand evidence and are not canonicalized.
