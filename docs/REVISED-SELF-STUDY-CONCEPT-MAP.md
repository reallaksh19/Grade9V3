# Grade9V3 — Revised Self-Study Concept Map and Core Implementation Plan

> Status: architectural intent for the post-PR18 tree.  
> Base used for this document: `architecture/final-release-authority` (PR #18 head).  
> Subject-content counterpart: GitHub Issue #19.  
> Audience: human maintainer and implementation agents.  
> This document is guidance/contract, not a source of academic truth and not a replacement for executable schemas/tests.

## 1. Goal

Build a practical self-study system for one learner.

The normal real-world starting point is usually a worksheet/question set, sometimes accompanied by a syllabus/topic, a rough parent knowledge estimate, or prior question-by-question study observations.

The system should answer:

1. What does each question actually require?
2. Which existing capabilities, microtopics and matrix rungs teach that requirement?
3. What prerequisites are required?
4. What is the sensible study order across matrices?
5. Where should this learner start?
6. When an answer is wrong, what is the smallest useful feedback?
7. What should be tried next to verify that the gap is repaired?

The objective is **not** a comprehensive corporate learning platform.

The objective is a maintainable, source-grounded system that helps one student learn independently.

---

## 2. Revised concept map

~~~mermaid
flowchart LR
    IN[Inputs<br/>Worksheet / questions<br/>Optional syllabus<br/>Optional prior study map<br/>Optional knowledge %]

    QA[Question analysis<br/>Question -> required capabilities]
    GAP[Gap detection<br/>Known capability / new gap / scope conflict]

    KG[Existing knowledge structures<br/>Capabilities<br/>Prerequisites<br/>Microtopics<br/>Matrices]
    ROUTE[Study route<br/>Prerequisite closure<br/>Cross-matrix ordering]

    LE[Optional learner evidence<br/>Current attempts > prior diagnostic > owner estimate]
    START[Starting point and emphasis]

    CORES[Existing six Cores<br/>Core1 / 1A / 1B<br/>Core2 / 2A / 2B]

    ATTEMPT[Learner attempt]
    DIAG[Diagnose first meaningful failure]
    FB[Targeted feedback<br/>hint -> stronger hint -> repair]
    VERIFY[Fresh verification question]
    OBS[Record observation]
    REVIEW[Simple review scheduling]

    IN --> QA
    QA --> GAP
    GAP --> KG
    KG --> ROUTE
    LE --> START
    ROUTE --> START
    START --> CORES
    CORES --> ATTEMPT
    ATTEMPT --> DIAG
    DIAG --> FB
    FB --> VERIFY
    VERIFY --> OBS
    OBS --> LE
    OBS --> REVIEW
    REVIEW --> ATTEMPT
~~~

### Architectural reading

The stable subject backbone is:

~~~text
matrix
  -> rung
  -> microtopic
  -> primary capability
  -> prerequisite capability graph
~~~

Questions map into that backbone through:

~~~text
question.primary_capability_ref
question.secondary_capability_refs
~~~

The new core work is deliberately thin:

~~~text
arbitrary worksheet
  -> question/capability map
  -> prerequisite closure
  -> cross-matrix study route
  -> learner routing
  -> feedback/retry loop
~~~

No seventh Core is introduced.

---

## 3. Separation of concerns

| Layer | Owns | Must not own |
|---|---|---|
| Subject content | capabilities, prerequisites, matrices, microtopics, questions, misconceptions, explanations | learner weakness/strength |
| Shared/core | schemas, mapping, prerequisite traversal, study-route planning, learner-evidence rules, feedback orchestration | topic-specific academic truth |
| Learner data | observations, current evidence, rough owner estimate, review timing | canonical curriculum truth |
| Source/review/release authority | provenance, source custody, reviewed/curated/released authority | pedagogy selection |
| Worksheet/session | transient question set and mapping to canonical capabilities | permanent curriculum structure unless promoted deliberately |

### Non-negotiable separation

A statement such as:

> "Q13 shows delta-y / delta-x is unstable"

is learner evidence.

It MUST NOT be stored in a matrix or capability definition.

A matrix says what is to be learned. Learner evidence says what happened to this learner.

---

## 4. Input model

The system should support these four common cases.

### Case A — questions only

~~~text
questions
-> derive tested capabilities
-> derive prerequisites
-> identify existing matrices/rungs
-> flag unresolved capability gaps
~~~

### Case B — questions + syllabus

~~~text
questions
-> question-derived scope

syllabus
-> syllabus scope

compare:
- covered by both
- syllabus item not exercised by worksheet
- worksheet demand outside supplied syllabus
~~~

### Case C — questions + rough parent knowledge %

The percentage is a routing hint only.

It may choose a conservative starting region/rung.

It MUST NOT prove that a prerequisite is mastered.

### Case D — questions + prior question/study map

Prior study maps are converted into learner observations linked to capabilities.

They do not alter canonical matrices.

---

## 5. Authority and evidence ordering

For learner routing, use this practical ordering:

~~~text
recent direct learner attempt
    >
prior diagnostic / prior study-map observation
    >
owner knowledge estimate
    >
unknown
~~~

This is not a psychometric mastery probability.

The minimum useful per-capability state remains:

~~~text
DEMONSTRATED
UNCERTAIN
MISSING
UNOBSERVED
~~~

A rough percentage may remain stored for human context but should stop driving routing once stronger evidence exists.

---

## 6. Question-to-study mapping

### Required mapping

Each worksheet question should resolve, where possible, to:

~~~text
question
-> primary capability
-> zero or more meaningful secondary capabilities
-> prerequisite closure
-> microtopic(s)
-> matrix/rung location(s)
~~~

### Primary capability

The central learner decision/action without which the question cannot be solved.

### Secondary capability

Another capability materially exercised by the same question.

Do not repeat every transitive prerequisite as a secondary capability.

Prerequisite closure belongs to the graph.

### Cross-matrix rule

`ladder_position` is local to a matrix.

It MUST NOT be compared across matrices.

Global study order comes from `capability.prerequisite_refs`.

---

## 7. Study-scope categories

Every capability introduced into a generated study route should be explainable by one of these reasons:

| Reason | Meaning |
|---|---|
| QUESTION_DEMAND | directly required by the supplied question set |
| PREREQUISITE | required upstream of question demand |
| SYLLABUS_REQUIREMENT | explicitly required by supplied/verified syllabus |
| DECLARED_EXTENSION | intentionally added enrichment/competition material |

If none applies, the system should flag the content rather than silently expanding scope.

---

## 8. Existing six-Core use

The six-Core architecture remains intact.

| Need | Preferred resource |
|---|---|
| quick orientation | Core1 |
| missing concept / explicit construction | Core1A |
| learner should reconstruct the concept | Core1B |
| source question custody | Core2 |
| familiar/supported application | Core2A |
| changed decision structure / transfer | Core2B |

The study router selects among existing assets. It does not redefine their academic content.

---

## 9. Feedback loop

The feedback system is the main learner-facing addition.

### Minimum loop

~~~mermaid
flowchart TD
    A[Independent attempt]
    B{Correct?}
    C[Record independent success]
    D[Identify first meaningful failure]
    E[Level 1: directional hint]
    F[Retry]
    G[Level 2: structural hint]
    H[Retry]
    I[Level 3: route to Core1B/Core1A repair]
    J[Fresh verification question]
    K[Record observation]

    A --> B
    B -- yes --> C --> J
    B -- no --> D --> E --> F
    F --> B
    D --> G
    G --> H --> B
    D --> I --> J
    J --> K
~~~

Implementation does not need probabilistic learner modelling.

The first version should identify the **first meaningful failure**, not merely whether the final numeric answer is wrong.

A minimal error-stage vocabulary is sufficient:

~~~text
CONCEPT
SETUP
EXECUTION
CARELESS
UNKNOWN
~~~

A minimal help vocabulary is sufficient:

~~~text
NONE
HINT
WORKED_EXAMPLE
SOLUTION
UNKNOWN
~~~

---

## 10. Simple review scheduling

Do not build a sophisticated scheduler initially.

Suggested first rule:

~~~text
wrong                   -> next day
correct with hint       -> ~3 days
correct independently   -> ~7 days
independent transfer    -> ~14-21 days
~~~

A failed delayed check moves the capability forward again.

This policy is intentionally replaceable after real usage.

---

# 11. Core implementation plan

The work below is the Shared/core stream. Subject content/matrix completion is owned separately under Issue #19.

## Phase 0 — Freeze the post-PR18 baseline

### Purpose

Start from the final PR #18 architecture without reopening PR #1 or rebasing the full PR #9 branch.

### Tasks

- confirm PR #18 head/merged baseline;
- identify current Shared contracts reused by the new flow;
- inventory existing capability, matrix, question, learner-profile and observation schemas;
- document any conflict between old PR #9 Shared changes and the PR #10-#18 stack;
- create a small set of golden fixtures using real worksheet-style data.

### Do not do

- no new pedagogical abstractions;
- no subject content migration;
- no learner UI;
- no feedback engine yet.

### Success

A clean implementation branch exists from the final architecture stack and the next phases can be implemented without modifying PR #9 history.

---

## Phase 1 — Worksheet -> capability -> study map

### Purpose

Make the system work from the input most often available in practice: a worksheet/question set.

### Core responsibilities

1. represent a transient worksheet/question set;
2. associate each question with primary/secondary canonical capabilities;
3. resolve each capability back to existing microtopic/matrix/rung;
4. compute prerequisite closure;
5. produce cross-matrix study order;
6. flag unresolved mappings rather than inventing curriculum.

### Expected outputs

A machine-readable study map roughly equivalent to:

~~~text
Q1 -> CAP-A -> Matrix X / R1
Q2 -> CAP-C + CAP-D -> Matrix Y / R2, Matrix X / R3
...
Study order: CAP-A -> CAP-B/C -> CAP-D/E
Unresolved: Q9 requires capability not currently modelled
~~~

### Key invariant

The mapper is an overlay. It does not copy every worksheet question into canonical subject libraries.

### Success

Given a multi-topic worksheet, the tool can produce a deterministic, inspectable question -> capability -> prerequisite -> matrix/rung map.

---

## Phase 2 — Teaching/assessment coverage audit

### Purpose

Mechanically enforce the grounding relationship between questions and teaching.

### Forward audit

For every canonical/source question capability requirement:

~~~text
question requirement
-> where is it taught or bridged?
~~~

Flag when unresolved.

### Reverse audit

For every taught capability in the generated study scope:

~~~text
why is this being taught?
~~~

It must be justified by:

- question demand;
- prerequisite;
- syllabus;
- declared extension.

### Success

A generated study route cannot silently omit a tested capability and cannot silently accumulate unrelated teaching.

---

## Phase 3 — Practical learner evidence

### Purpose

Use simple owner estimates and real observations without building a complex learner model.

### Tasks

- make rough knowledge percentage usable as a conservative bootstrap route;
- ensure percentage is not interpreted as mastery evidence;
- support importing prior question/study-map observations;
- minimally extend observation data where needed, preferably with:
  - question/session reference;
  - help level;
  - error stage;
- implement evidence precedence;
- derive current per-capability state from evidence.

### Conservative percentage rule

The exact policy should be testable and documented.

A practical starting policy is to route at or below the owner's estimated position rather than reject an estimate merely because it falls between exact ladder coordinates.

### Success

The system can start with only a rough estimate, then naturally replace that estimate with actual attempt evidence.

---

## Phase 4 — Feedback/retry runtime

### Purpose

Make the generated learning materials usable for independent study.

### Tasks

- accept a learner response and, where available, reasoning;
- evaluate answer/rubric using existing content contracts;
- identify the earliest meaningful failure that can be supported by evidence;
- map failure to relevant capability/misconception;
- select the least revealing useful hint;
- escalate support only after another attempt;
- route to Core1B/Core1A repair when necessary;
- issue a fresh verification question;
- write the resulting learner observation;
- select the next activity.

### Feedback principle

Do not respond to every wrong answer with a full solution.

Prefer:

~~~text
attempt
-> directional cue
-> retry
-> structural hint
-> retry
-> repair
-> different verification question
~~~

### Success

One representative topic can run end-to-end without a live tutor:

~~~text
attempt -> feedback -> repair -> fresh test -> updated evidence -> next step
~~~

---

## Phase 5 — Minimal review loop

### Purpose

Retest learning after time without building a scheduling platform.

### Tasks

- compute a simple next-review date from attempt outcome;
- mix due capabilities into later practice;
- record delayed performance as new evidence;
- allow failed delayed checks to route back to repair.

### Success

A capability can move through:

~~~text
learned today
-> retrieved later
-> independently verified later
~~~

with no manual tracking spreadsheet required.

---

## Phase 6 — Real-world pilot and stop condition

### Purpose

Validate the architecture against its only important user.

### Pilot material

Use at least:

- one Mathematics worksheet spanning more than one matrix;
- one Physics worksheet spanning more than one matrix;
- one prior study-map input if available.

### Observe

- wrong capability mapping;
- over-teaching;
- missing prerequisites;
- feedback that reveals too much;
- feedback that is too vague;
- careless errors causing unnecessary reteaching;
- transfer failures;
- review schedule annoyances.

### Rule

Fix demonstrated failures.

Do not add abstractions merely because a general learning platform might need them.

### Stop condition

Pause architecture work when the learner can independently:

1. receive a sensible study route from a real worksheet;
2. study appropriate Core assets;
3. get targeted feedback after mistakes;
4. retry on a fresh item;
5. have progress affect later study/review.

---

# 12. Workstream boundary with Issue #19

Issue #19 owns subject content/matrix work.

The core stream MUST NOT duplicate it.

~~~text
CORE STREAM
Shared schemas/tools
worksheet mapping
prerequisite traversal
study routing
learner evidence
feedback runtime

CONTENT STREAM (#19)
Physics/Mathematics capabilities
microtopics
matrices
questions
subject validators/representations
source-grounded academic content
~~~

If content work discovers a Shared limitation, it reports a minimal reproducible blocker.

It does not alter Shared contracts independently.

---

# 13. Anti-drift rules

1. **No new Core product.** Reuse the six existing Cores.
2. **No matrix-per-worksheet.** Matrices are durable; worksheets are transient.
3. **No rung-per-question.** Rungs are conceptual transitions.
4. **No learner state in canonical content.**
5. **No cross-matrix ordering using ladder_position.**
6. **No source claim from authored/generated questions.**
7. **No corporate-scale learner model.**
8. **No new Shared abstraction unless a concrete end-to-end case cannot be represented.**
9. **No silent scope expansion.** Every taught capability needs a reason.
10. **No full PR #9 Shared-history import after PR #18.** Selectively migrate useful subject content instead.
11. **No architecture work after pilot success without an observed learner problem.**

---

# 14. End-to-end success criteria

A successful implementation accepts:

~~~text
required:
- worksheet/question set

optional:
- syllabus/topic/subtopic
- initial knowledge %
- prior question->study map
- prior learner observations
~~~

and can produce:

- [ ] a question -> capability mapping;
- [ ] mapping from capabilities to existing matrices/rungs;
- [ ] explicit unresolved capability gaps;
- [ ] prerequisite closure;
- [ ] logical cross-matrix study order;
- [ ] conservative learner starting point;
- [ ] appropriate Core resources;
- [ ] independent learner attempt;
- [ ] targeted, non-spoiling feedback;
- [ ] fresh verification question after repair;
- [ ] updated learner evidence;
- [ ] simple delayed review recommendation.

For a representative real worksheet, a human reviewer should be able to answer without reading implementation code:

1. What is each question testing?
2. What does the learner need beforehand?
3. Where is that taught?
4. Why is this item in the study route?
5. What did the learner actually get wrong?
6. What is the next smallest useful intervention?

If those answers are clear, the system is doing its job.

---

# 15. Explicit non-goals for the first working version

Do not implement unless real usage demonstrates a need:

- Bayesian knowledge tracing;
- Item Response Theory;
- probabilistic mastery percentages;
- large multidimensional difficulty models;
- automated curriculum completion;
- generalized pedagogy-policy engines;
- proof-specific grading architecture;
- sophisticated spaced-repetition algorithms;
- enterprise-style multi-user workflows;
- new governance layers beyond the PR #10-#18 chain.

---

## Final design principle

> **Question sets reveal demand. Matrices/capabilities provide durable academic structure. Learner evidence changes routing, not truth. Feedback repairs the smallest demonstrated gap. Real usage decides what to build next.**
