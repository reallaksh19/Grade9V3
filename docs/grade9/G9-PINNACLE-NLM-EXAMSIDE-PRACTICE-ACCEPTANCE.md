# Grade 9 Pinnacle NLM — ExamSIDE practice acceptance

> Status: **owner-approved preparation-demand acceptance slice**
>
> Date: 2026-09-19
>
> Primary source: `https://questions.examside.com/past-years/jee/jee-main/physics/laws-of-motion`
>
> Authority: `docs/grade9/PINNACLE-EXAMSIDE-PREPARATION-AUTHORITY.md`

## Why this slice exists

The inspected ExamSIDE JEE Main Laws of Motion page currently exposes 153 questions from
113 papers across 2002–2026.

The goal here is not to import that question bank.

The goal is to use representative real question demand to answer a narrower engineering
question:

> Do the current Grade9V3 NLM capabilities have enough canonical Core2A practice, and can
> real ExamSIDE questions route through the existing graph without chapter-label guessing?

## Inspected demand cases

The acceptance fixture keeps only IDs, URLs and concise demand summaries. It does not copy
ExamSIDE stems, figures, answers or solutions.

| Inspected case | Durable learner action |
| --- | --- |
| 2026-01-24 stacked sliding bodies | quantitative kinetic/static-contact reasoning, body-specific FBD, Newton II |
| 2022-06-28 hanging mass + larger mass | ideal-string tension, fixed-string constraint, Newton II |
| 2021-08-26 two blocks moving together | static-friction feasibility + common acceleration |
| 2021-08-31 accelerating car with suspended bob | explicit observer-frame / pseudo-force extension |
| 2021-03-18 bullet stopping in wood | constant-acceleration kinematics first, then Newton II |
| 2021-09-01 rough versus smooth incline timing | friction plus constant-acceleration timing |
| owner-supplied machine-gun item | discrete momentum transfer per unit time |

The bullet case is deliberately important: although ExamSIDE classifies it under Laws of
Motion, the primary Grade9V3 learner action is constant-acceleration kinematics. Newton II
is secondary. Chapter placement is not allowed to dictate capability ownership.

## Practice closure added

The default NLM package now holds one authored Core2A practice question for each bounded
capability added in the previous NLM production slice:

- `CAP-NLM-FRICTION-QUANT`;
- `CAP-NLM-CONNECTED-COMMON-ACCEL`;
- `CAP-NLM-IDEAL-STRING-TENSION`;
- `CAP-NLM-SINGLE-STRING-CONSTRAINT`.

The explicit momentum-transfer package now holds one authored Core2A practice question for:

- `CAP-NLM-MOMENTUM-TRANSFER-RATE`.

These are **AUTHORED** Grade9V3 questions. ExamSIDE is recorded as the demand source that
justifies what has to be practised; the authored items do not borrow ExamSIDE exam identity,
wording or source-question custody.

## Core2B decision

This pass does **not** add a Core2B exposure.

The ExamSIDE page proves that mixed and changed-demand NLM questions exist, but a single
token transfer item would make the current bucket-level planner report Core2B ready for the
whole bucket. That would overstate the current transfer inventory.

Keep Core2B blocked until a deliberately small but representative transfer set is authored
and reviewed.

## Acceptance invariants

The focused regression must prove:

1. each newly added bounded NLM capability owns at least one Core2A question;
2. the momentum-transfer explicit extension owns one Core2A question;
3. every added practice question remains `origin = AUTHORED`;
4. ExamSIDE appears only as preparation-demand provenance, not as copied question custody;
5. the seven inspected external demand cases resolve through the current capability graph;
6. the bullet case routes primarily through kinematics and secondarily through Newton II;
7. observer-frame and momentum-transfer capabilities remain non-default;
8. ordinary NLM Core2B remains blocked because no canonical Core2B question is yet exposed.

## Stop condition

After this acceptance slice is green, do not add more NLM concepts.

Use additional ExamSIDE questions only when they expose one of:

- a real missing practice variation;
- a repeated model-selection failure;
- a missing transfer/discrimination item;
- a capability gap not already represented by the current graph.
