# Physics donor adaptation policy

> Applies to Grade-9 Physics authoring now, then Grade 10 and Grade 11 in sequence.

## Rule

Search the repository owner's mature prior Physics engineering work **before** creating new
Physics teaching.

The donor is a research/engineering corpus, not a runtime dependency.

```text
SEARCH
→ COMPARE
→ COPY
→ ADAPT
→ LOCALISE
→ TEST
```

Do not create cross-repository `source_refs`, prerequisite links, runtime lookups, or release
dependencies.

Once adapted, Grade9V3 must be able to stand on its own.

## What may be copied and adapted

Useful donor material includes:

- canonical physics concepts;
- equations and symbol semantics;
- model conditions and validity limits;
- representation invariants;
- reasoning sequences;
- transformations;
- misconceptions and counterexamples;
- repair logic;
- verification/limiting cases;
- problem-family invariants;
- transfer dimensions and falsifiers.

Map these into the existing Grade9V3 structures rather than importing a second schema.

## What must not be inherited

Do not import donor:

- release/readiness claims;
- old curriculum inclusion as current authority;
- learner state;
- difficulty vectors merely because they exist;
- JEE/CBSE labels as route authority;
- broad-gate granularity when Grade9V3 needs smaller independently fail-able capabilities;
- advanced content that current Grade-9 scope does not justify.

## Target mapping

```text
donor concept / model condition
→ inferential_jump / teaching_path / why_valid

donor reasoning sequence
→ Core1A teaching_path and Core1B elicitation route

donor misconception
→ misconception + diagnostic_prompt + repair

donor representation invariant
→ matrix must_contain / controlled_variation / teaching step

donor verification / falsifier
→ exit_task check / targeted regression test

donor problem family / transfer dimension
→ question_family / matrix transfer

donor advanced material
→ DECLARED_EXTENSION or DEFER
```

## Capability decision

Before adding a new capability:

1. same learner action already exists → reuse it;
2. same action but donor has richer semantics → enrich the existing record;
3. story/context changed only → reuse capability and change context;
4. representation changed but success criterion is the same → normally reuse;
5. independently fail-able learner action with a distinct success criterion → candidate new capability;
6. donor depth exceeds current grade scope → extension or defer.

## Curriculum boundary

Donor curriculum metadata is historical evidence only.

Current Grade9V3 scope decisions remain:

```text
SYLLABUS_REQUIREMENT
QUESTION_DEMAND
PREREQUISITE
DECLARED_EXTENSION
DEFER
```

A donor record can improve the Physics without deciding whether the learner should study it
in the current Grade-9 pass.

## Verification

Every donor-adapted topic must still pass the normal Grade9V3 checks:

- schema/conformance;
- capability and prerequisite resolution;
- Core1A/Core1B self-study closure;
- misconception → diagnosis → repair → fresh verification;
- session readiness;
- targeted regressions;
- repository guardrails.

The donor reduces reinvention. It does not bypass Grade9V3 acceptance.
