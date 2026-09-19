# Pinnacle preparation authority — owner-approved ExamSIDE demand

> Status: **owner instruction**
>
> Date: 2026-09-19
>
> Scope: Grade 9 Pinnacle Physics preparation inside chapter boundaries already confirmed by
> the Pinnacle Terminal-1 portion sheet.

## Decision

The owner accepts **ExamSIDE past-year JEE question pages and individual ExamSIDE PYQs as
reliable external preparation-demand evidence** for the learner when the demand corresponds
to an active Pinnacle chapter.

This means matching ExamSIDE demand may justify:

- `REUSE`;
- `ENRICH`;
- `AUTHOR`;
- `QUESTION_VARIATION`;

without waiting for a Pinnacle worksheet to repeat the same micro-demand.

This authority is about **preparation breadth**, not about rewriting the school's own syllabus.

## Evidence domains remain separate

Keep these claims distinct:

```text
Pinnacle portion sheet
→ chapter is active

Pinnacle worksheet / classwork / revision / test
→ direct school micro-demand

owner-approved matching ExamSIDE chapter or PYQ
→ valid Pinnacle preparation micro-demand

Grade9V3 capability/matrix
→ local teaching representation
```

Therefore ExamSIDE preparation evidence must not silently change:

```text
school_micro_demand = MICRO_TO_CONFIRM
```

unless a Pinnacle-issued source actually confirms that micro-demand.

A planning/view layer may separately record:

```text
preparation_demand = CONFIRMED_EXAMSIDE
```

or retain the existing equivalent field:

```text
external_question_demand = CONFIRMED_EXAMSIDE
```

No new runtime enum is required by this owner instruction.

## Owner-approved sources supplied on 2026-09-19

### Motion in 2 D

`https://questions.examside.com/past-years/jee/jee-main/physics/motion-in-a-plane`

Use as a demand-discovery corpus for the active Pinnacle `Motion in 2 D` chapter.

### Vectors

`https://questions.examside.com/past-years/jee/jee-main/physics/vector-algebra`

Use as a demand-discovery corpus for the active Pinnacle `Vectors` chapter.

### NLM

`https://questions.examside.com/past-years/jee/jee-main/physics/laws-of-motion`

Use as a demand-discovery corpus for the active Pinnacle `NLM` chapter.

### Specific approved question evidence

`https://questions.examside.com/past-years/jee/question/pa-machine-gun-fires-a-bullet-of-mass-m-with-a-velocity-of-comedk-physics-units-and-measurements-k8pkjfk78zobjtd5`

This individual item may be used as concrete question-demand evidence. Its durable learner
action must still be mapped before any capability is added; a story/context never creates a
capability by itself.

## Demand-discovery rule

For each representative ExamSIDE question:

```text
question
→ exact learner action
→ existing capability/prerequisite mapping
→ REUSE / ENRICH / AUTHOR / QUESTION_VARIATION / EXCLUDE_AT_CURRENT_DEPTH
```

The repository should author the **smallest stable learner-action structure** that explains
the demand.

Do not mirror ExamSIDE chapter taxonomies mechanically.

## Capability creation rule

Before adding a capability, apply this counterfactual:

> Could the learner reliably perform the existing capability and still fail this new
> decision independently?

If no, prefer an existing capability, enrichment, or a question variation.

Examples of things that should normally remain applications rather than capabilities:

- different projectile launch stories after the projectile model is owned;
- different numbers or geometries using the same vector operation;
- different connected-body stories governed by the same force/constraint decision.

## Depth boundary

ExamSIDE is evidence that a demand is worthwhile for Pinnacle preparation. It does not mean
every JEE question on the page belongs at the current Grade-9 teaching depth.

A demanded item may be classified:

```text
REUSE
ENRICH
AUTHOR
QUESTION_VARIATION
EXCLUDE_AT_CURRENT_DEPTH
```

Use `EXCLUDE_AT_CURRENT_DEPTH` when the durable demand depends on material deliberately
outside the current preparation slice.

## Anti-overreach rules

Do not:

- relabel ExamSIDE evidence as Pinnacle-issued evidence;
- promote `school_micro_demand` from ExamSIDE alone;
- import every JEE subtopic because it appears on a matching chapter page;
- create a capability for every question story;
- duplicate an existing prerequisite in a new chapter matrix;
- weaken existing readiness or learner-evidence semantics;
- treat an owner estimate as evidence of mastery.

## Practical consequence

For the four confirmed Terminal-1 chapter labels, further preparation authoring no longer
needs to wait for school micro-demand **when a matching owner-approved ExamSIDE question
family already demonstrates the learner action**.

School-issued material remains valuable for emphasis and calibration, but it is no longer
the only authority that may trigger bounded Pinnacle preparation content.
