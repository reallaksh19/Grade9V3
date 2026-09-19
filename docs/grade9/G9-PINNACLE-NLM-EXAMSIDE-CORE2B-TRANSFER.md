# Grade 9 Pinnacle NLM — ExamSIDE Core2B transfer acceptance

> Status: **owner-approved preparation-demand transfer slice**
>
> Date: 2026-09-19
>
> Primary demand corpus: `https://questions.examside.com/past-years/jee/jee-main/physics/laws-of-motion`

## Duplicate-work preflight

Before authoring this slice, the repository and pull-request history were checked for an
existing NLM Core2B / transfer / model-choice implementation.

No merged or open PR already populated `BUCKET-PHY-NLM-FIRST-LAW` with canonical
Core2B questions.

Relevant history instead showed the opposite:

- the Grade-9 NLM migration explicitly retained Core2A material while omitting the donor
  Core2B frame-choice item because the compiler did not faithfully carry the transfer
  and rubric payload;
- PR #114 deliberately stopped with Core2B blocked and added only Core2A practice;
- the current NLM matrix already described transfer demands, but the library exposed no
  NLM question to Core2B.

This pass therefore closes a real remaining gap rather than duplicating another PR.

## Why five transfer questions

One token Core2B question would make the bucket-level planner report Core2B available.
That would be structurally true but academically weak.

The smallest representative set used here covers the main changed-demand decisions
already declared by the NLM matrix:

| Transfer item | Dimension | Withheld decision |
| --- | --- | --- |
| friction state under an angled pull | `model_choice` | whether static contact is feasible or sliding has begun |
| multi-body system boundary | `reasoning_steps` | when to use the whole system and when to isolate one body |
| nonideal pulley / tension validity | `model_choice` | whether one common tension is licensed |
| verbal fixed-pulley geometry | `representation_translation` | how to construct the string-length equation and signs |
| accelerating-car frame selection | `model_choice` | whether to use an inertial description or an accelerating-frame pseudo-force convention |

A same-capability Core2A frame-choice anchor is added first so the frame transfer has
honest prior exposure lineage.

## ExamSIDE use

ExamSIDE provides the real question-demand evidence. Representative Laws-of-Motion
families include:

- blocks that may or may not move together under static friction;
- connected balls / bodies with tension and shared acceleration;
- fixed-pulley systems;
- accelerating-vehicle observer problems.

The canonical transfer questions remain Grade9V3-authored. Each stores only the
relevant ExamSIDE URL as demand provenance. External stems, figures, answers and exam
identity are not copied into the library.

## Core2B contract

Every transfer question must carry:

- an actual changed task field relative to a canonical Core2A parent;
- `transfer.dimension`, a changed-demand statement and exposure lineage;
- graduated hints;
- a full answer plus justification rubric;
- a repair reference back to the exact teaching construction.

For `model_choice` transfer, hints remain conceptual. They may not reveal the method
choice being assessed.

## Compiler defect exposed by real use

Authoring these records exposed the old reason the donor Core2B item had been omitted:
the library compiler carried hints and answer summaries but dropped seven authored
Core2B fields:

- transfer dimension;
- transfer statement;
- transfer lineage;
- rubric container;
- rubric criterion;
- rubric evidence;
- repair reference.

That is a genuine Shared delivery defect because authored assessment content disappears
between library and compiled product.

The smallest Shared repair is to carry those existing fields through
`compile_inputs._question_block` and render the transfer/rubric/repair material only
inside the answer-and-repair section, after the learner has attempted the question.

No new transfer schema, mastery model, Core, or strategy engine is introduced.

## Boundaries

This slice does not:

- open Core2B for the separate momentum-transfer bucket;
- add a new NLM capability;
- make frame choice a default Grade-9 entry rung;
- import movable/compound pulley formula catalogues;
- treat a new cover story as transfer by itself;
- expose the internal capability label to the learner in the question stem.

## Acceptance

The focused regression requires exactly five NLM Core2B questions and proves:

1. the set spans `model_choice`, `reasoning_steps` and
   `representation_translation`;
2. each item has a real Core2A parent in the same family;
3. each carries rubric, lineage and repair;
4. model-choice hints remain `CONCEPT` only;
5. ExamSIDE remains demand provenance rather than question custody;
6. the frame rung stays non-default;
7. the separate momentum-transfer bucket remains Core2B-closed;
8. the compiler no longer drops Core2B transfer payload.
