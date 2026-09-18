# Grade9V3 — Concept Report

> Scope: current repository architecture, the merged PR #1 foundation, the architecture/self-study work from PR #9 onward, the current self-study v1 integration, the independent benchmark workstream in Issue #47 / PR #48, and the evidence-gated future road plan in PR #49.
>
> Purpose: explain the whole system as one coherent concept for a human maintainer, parent, reviewer, or future implementation agent.
>
> This report is descriptive. It does not introduce a new architecture.

## 1. Executive summary

Grade9V3 is a personal self-study system for one learner in CBSE Grades 9–11, initially focused on Physics and Mathematics, with Chemistry structurally anticipated by the shared engine.

The system is not primarily a question generator, a tutoring chatbot, a curriculum database, or a test-preparation application. Its central purpose is narrower and more useful:

> Given real questions the learner needs to face, determine what those questions demand, connect that demand to durable academic knowledge already represented in the repository, identify the prerequisites, decide where this learner should start, deliver the smallest appropriate teaching/practice support, diagnose mistakes without prematurely revealing answers, verify repair on fresh work, and retain only evidence that was actually demonstrated.

The repository therefore separates several things that ordinary tutoring systems often collapse:

- **academic truth** — capabilities, prerequisites, microtopics, matrices, question families and subject representations;
- **learner products** — the six existing Core products;
- **source and review authority** — where material came from, whether custody is established, who reviewed it, and whether it is authorised for release;
- **worksheet/session demand** — transient external questions that reveal what a learner is being asked to do;
- **learner evidence** — what this particular learner has or has not demonstrated;
- **runtime orchestration** — mapping, routing, readiness, feedback and review;
- **benchmark evidence** — evidence about whether Grade9V3 itself behaves correctly.

The architecture deliberately prevents one category of evidence from impersonating another.

A worksheet may reveal demand, but it does not automatically become curriculum authority.

A rough parent estimate may choose a starting region, but it does not prove mastery.

A source URL may identify material, but downloading it does not prove exact source custody.

A benchmark failure may prove a weakness in Grade9V3, but it says nothing about the learner.

A story context such as river crossing may classify an application, but it is not automatically a new capability.

The result is a system that is more conservative than a typical AI tutor but is also much harder to fool into claiming knowledge, authority, readiness or learner mastery that it does not possess.

---

## 2. The problem Grade9V3 is solving

The real-world input is usually not a clean curriculum specification.

It is more often:

~~~text
school worksheet
past-paper question
coaching question bank
topic request
parent estimate
old study notes
previous learner mistakes
~~~

A conventional tutoring workflow tends to jump immediately from the visible topic label to an explanation:

~~~text
question says "relative motion"
→ teach relative motion
~~~

Grade9V3 asks more precise questions first:

1. What learner action does this question actually require?
2. Which reusable capability represents that action?
3. What other capabilities are materially exercised?
4. What prerequisites must already be available?
5. Where is each capability actually taught?
6. Is the teaching local, provided externally, unresolved, or ambiguous?
7. Is the corresponding matrix ready for an independent self-study session?
8. What evidence already exists for this learner?
9. What is the smallest useful intervention?
10. What fresh work would show that the gap is repaired?

This changes the system from a topic-based content browser into a capability-driven self-study route.

---

## 3. The architectural lineage

### 3.1 PR #1 — the foundational publication and knowledge architecture

PR #1 established the fundamental repository shape.

Its most important contribution was not one Physics topic. It was the separation of:

~~~text
Shared engine
subject adapters
subject gates
canonical libraries
six learner products
publication outputs
~~~

The governing engineering idea is:

> Subject and topic variation belongs in governed data, not in subject-specific branches inside Shared runtime code.

That is why Physics and Mathematics can behave differently where academic semantics require it while still using the same publication host.

Examples already encoded in the architecture include:

- Physics numerical comparison with a tolerance;
- Mathematics exact rational equality;
- Chemistry contracts designed around exact element-count structures.

The Shared layer therefore owns orchestration and contracts, while subject adapters own subject-specific representation and checking semantics.

PR #1 also established the six learner products:

| Product | Role |
| --- | --- |
| Core1 | compact orientation / basic notes |
| Core1A | explicit detailed teaching |
| Core1B | conceptual reconstruction / self-tutor elicitation |
| Core2 | source-backed questions with source identity, hints and answers |
| Core2A | supported/familiar practice with solution breakdown |
| Core2B | application and transfer |

This six-Core model remains intact throughout the later work. The self-study architecture does not introduce a seventh Core.

### 3.2 PR #9 and the planner/compiler agreement problem

PR #9 addressed a foundational consistency issue: the planning layer must not say a product is ready when the compiler cannot actually build it.

This matters because Grade9V3 treats readiness as a claim that must survive mechanical falsification.

For practice products, the planner therefore has to look at the actual question exposure owned by the relevant bucket/capability slice rather than simply assuming that package membership implies usable practice.

This theme becomes a recurring architectural rule:

> Planning, buildability, learner reachability, academic authority and runtime readiness are related but distinct claims.

### 3.3 PRs #10–#18 — governed agent authoring and authority

The next architectural chain made agent-assisted development possible without allowing an agent to promote its own assertions into authority.

The flow evolved into:

~~~text
owner request
→ plan
→ required owner decisions
→ execution packet
→ source custody
→ constrained authoring work order
→ authoring receipt
→ independent review
→ curation
→ final release receipt
~~~

The important idea is not the number of receipts. It is the separation of authority.

An agent can author a candidate.

That does not make the candidate reviewed.

A reviewed record is not automatically curated.

A built publication is not automatically authorised for learner release.

The repository therefore distinguishes:

~~~text
AUTHORING
BUILD
REVIEW
CURATION
RELEASE
~~~

instead of representing them with one editable status field.

Source custody follows the same principle.

The system explicitly rejects the shortcut:

~~~text
"I inspected the source"
→ therefore source is sufficient
~~~

Instead, the architecture introduced verified source receipts and a deterministic acquisition/ingestion pipeline.

Conceptually:

~~~text
source bytes
→ content-addressed acquisition
→ explicit custody manifest
→ candidate ingestion
→ canonical validation
→ source receipt
~~~

And it preserves this distinction:

~~~text
download succeeded
!= transcription is exact
!= source custody is sufficient
!= academic content is reviewed
~~~

These PRs are mainly development/governance infrastructure, but they are essential to the academic concept because the learner-facing system is supposed to be source-grounded rather than merely fluent.

### 3.4 PR #20 — worksheet-driven self-study becomes the explicit product direction

PR #20 documented the revised concept map after the release-authority foundation.

The project goal became explicit:

> Build a practical self-study system for one learner.

The normal starting object changed from an authoring request to a real worksheet/question set.

That produces the central self-study flow:

~~~text
arbitrary worksheet
→ question/capability map
→ prerequisite closure
→ cross-matrix route
→ learner routing
→ feedback/retry
~~~

The architecture remains intentionally thin around the six existing learner products.

### 3.5 PRs #22–#27 — the C0–C5 self-study core

The self-study runtime was then implemented incrementally.

#### C0/C1 — worksheet mapping

A transient worksheet contract allows arbitrary questions to be mapped onto canonical capabilities without forcing those questions into the permanent academic library.

Each question may identify:

~~~text
one primary capability
zero or more meaningful secondary capabilities
~~~

The system then resolves those capabilities back to their canonical microtopics and matrix/rung teaching locations.

Unknown, missing and ambiguous mappings remain explicit.

#### C2 — prerequisite and cross-matrix routing

The prerequisite graph, not matrix rung numbers, determines global order.

This is essential because ladder positions are local to one matrix.

Grade9V3 therefore rejects:

~~~text
Matrix A R4 < Matrix B R6
therefore teach A before B
~~~

as meaningless.

Instead:

~~~text
CAP-B prerequisite_refs CAP-A
→ teach/verify CAP-A before CAP-B
~~~

The route also records why each capability entered the study scope:

- QUESTION_DEMAND
- PREREQUISITE
- SYLLABUS_REQUIREMENT
- DECLARED_EXTENSION

This prevents silent scope expansion.

#### C3 — practical learner evidence

The project deliberately avoided a corporate-scale mastery model.

Learner evidence remains interpretable and conservative.

The practical state space is:

~~~text
DEMONSTRATED
UNCERTAIN
MISSING
UNOBSERVED
~~~

Evidence precedence favours actual learner behaviour over rough estimates.

In practical terms:

~~~text
direct learner attempt
>
prior diagnostic / prior study observation
>
rough owner estimate
>
unknown
~~~

A parent estimate is useful because it can avoid starting every topic from rung one.

But it is never converted into demonstrated mastery.

#### C4 — feedback and retry

The feedback runtime is designed to preserve learner effort.

The default logic is:

~~~text
independent attempt
→ diagnose first supported meaningful failure
→ least revealing useful hint
→ retry
→ stronger structural help if needed
→ repair
→ fresh verification
~~~

It does not guess a failed capability when a multi-capability failure is ambiguous.

For arbitrary worksheet questions, it also does not fabricate a hint ladder merely because the question is present.

It may instead use the canonical misconception/repair structure associated with the mapped capability.

#### C5 — simple delayed review

Review scheduling is intentionally small and deterministic:

~~~text
incorrect             → +1 day
correct with hint     → +3 days
correct independently → +7 days
independent transfer  → +14 days
~~~

This is a reminder/retrieval policy, not a mastery algorithm.

### 3.6 PRs #28–#33 — making the architecture practical for one family

The next set of changes reduced friction rather than increasing theory.

Examples include:

- decoupling tests from subject-migration timing;
- permitting feedback on transient worksheet questions;
- making rough knowledge percentage useful as a starting coordinate;
- importing prior study-map observations without guessing;
- applying separate rough estimates to different subtopics/matrices;
- compiling the internal route into a learner/parent-facing study map.

The result is important conceptually:

> The repository does not require the parent to think in internal capability IDs before the system becomes useful.

Internal truth remains canonical, but the output can say what to study and why in human terms.

### 3.7 PRs #34–#40 — real external questions expose the missing runtime semantics

The ExamSIDE Motion-in-a-Plane pilot tested the architecture against real external questions.

This exposed a crucial distinction.

A prerequisite can be absent locally for two very different reasons:

~~~text
A. the repository has no way to supply it
B. another declared provider owns it
~~~

Treating both as NO_TEACHING_LOCATION was wrong.

That led to the shared capability-delivery resolver:

~~~text
LOCAL
EXTERNAL_BRIDGE
UNRESOLVED
AMBIGUOUS
~~~

This resolver now provides one meaning of capability delivery across mapping, route planning, study-scope audit, start routing, learner-facing plans, readiness and the practical session runner.

The same pilot also demonstrated that a structurally valid route is not always executable for a particular learner.

Hence the session-readiness layer.

The statuses are:

~~~text
SESSION_READY
SESSION_READY_WITH_BRIDGE
PILOT_READY
NOT_READY
~~~

A route can therefore be:

~~~text
valid = true
ready = false
first action = BRIDGE
~~~

without contradiction.

### 3.8 PR #41 — self-study v1 consolidation

PR #41 merged the practical self-study flow into one integration candidate and is now merged to main.

Its vertical slice is:

~~~text
real worksheet/question set
→ transient capability map
→ canonical delivery resolution
→ prerequisite closure
→ rough starting estimate
→ prior learner evidence
→ learner-facing study map
→ session-readiness gate
→ attempt outcome
→ diagnosis / safe hint / repair
→ fresh verification
→ observation draft
→ delayed review date
~~~

PR #41 is the best single expression of the current product concept.

It intentionally does not add:

- a new mastery model;
- a universal grader;
- hidden learner-state persistence;
- a full scheduler;
- a second curriculum model.

### 3.9 PRs #42, #43, #45 and #46 — readiness, broader pilot evidence and ontology correction

PR #42 records a practical readiness snapshot.

At that snapshot:

Physics:
- 5 matrices are SESSION_READY;
- 1 is SESSION_READY_WITH_BRIDGE;
- 1 is PILOT_READY;
- 9 are NOT_READY.

Mathematics:
- the represented one-unknown linear-equations matrix is SESSION_READY.

The current safe v1 Physics whitelist in that report is:

- one-dimensional motion;
- Newton's first law / free-body diagrams;
- simple machines;
- sound;
- work / energy / power;
- relative motion with a Mathematics bridge.

PR #43 brought a second external Relative Motion question bank into the pilot as demand evidence without promoting it into canonical curriculum/source custody.

PR #45 fixed a narrow feedback edge case:

> An unrelated external secondary capability should not block repair of a clearly identified local failure.

But the system still stops when:

- the failed capability itself is external;
- the failed capability cannot be safely attributed;
- local delivery is unresolved or ambiguous.

PR #46 introduced one of the most important ontology clarifications.

It separates:

~~~text
capability
= what the learner can do

question family
= stable demand / solution structure

application context
= where the demand is presented
~~~

Only capabilities participate in mastery/evidence state and prerequisite closure.

This prevents story settings from proliferating into fake skills.

For example, river/boat, rain/runner and aircraft/wind can be different contexts around reusable relative-motion/vector capabilities without requiring a separate mastery ID for each story.

### 3.10 Repository numbering note

The GitHub API currently returns no pull request numbered #8 in this repository.

The relevant architectural sequence after merged PR #1 therefore resumes at PR #9.

---

## 4. The current conceptual architecture

The system is easiest to understand as seven cooperating layers.

### Layer 1 — canonical academic structure

This layer answers:

> What exists academically independent of this learner and this worksheet?

It includes:

- capabilities;
- prerequisite references;
- success criteria;
- microtopics;
- matrices and local rung order;
- question families;
- application contexts;
- canonical questions;
- misconceptions;
- diagnostics;
- repairs;
- exit tasks;
- subject representations and gates.

The durable academic backbone is:

~~~text
matrix
→ rung
→ microtopic
→ primary capability
→ prerequisite capability graph
~~~

A capability is a reusable learner action or distinction.

A matrix is a structured progression of teaching locations.

A rung is not one question.

A matrix is not one worksheet.

An application context is not a capability.

### Layer 2 — the six learner products

The six Cores are delivery products over the canonical academic layer.

They are not six independent curricula.

They express different pedagogical purposes around the same underlying truth.

~~~text
Core1  → orientation
Core1A → explicit teaching
Core1B → reconstruction
Core2  → source-backed question custody
Core2A → supported practice
Core2B → application / transfer
~~~

The self-study router selects among these products.

It does not redefine them.

### Layer 3 — source, authoring and release authority

This layer answers:

> Why should the repository trust the material and what authority does it have?

It tracks:

- source acquisition;
- source custody;
- authoring provenance;
- work-order scope;
- authoring receipts;
- independent review;
- curation;
- final release authority.

This layer prevents generated material from silently claiming source status or reviewed authority.

### Layer 4 — worksheet/session demand

This layer is deliberately transient.

It answers:

> What do the questions in front of the learner demand?

A worksheet question may map to canonical capability IDs.

It may be:

- a school question;
- a past-paper question;
- an external question-bank item;
- a manually mapped problem;
- an agent-proposed mapping.

The worksheet is evidence of demand.

It is not automatically:

- curriculum authority;
- canonical content;
- source custody;
- a new matrix;
- a new capability.

### Layer 5 — learner evidence

This layer answers:

> What has this learner actually demonstrated?

It includes:

- direct attempts;
- diagnostic observations;
- imported prior study observations;
- help used;
- error stage;
- learner state;
- rough parent estimates as low-authority routing hints;
- review timing.

Learner evidence never modifies canonical academic truth.

A statement such as:

~~~text
"Q13 shows slope roles are unstable"
~~~

belongs in learner evidence, not inside the definition of slope.

### Layer 6 — runtime orchestration

This layer connects the previous layers.

It includes:

- question-to-capability mapping;
- canonical teaching-location resolution;
- capability delivery classification;
- prerequisite closure;
- scope audit;
- cross-matrix ordering;
- learner start routing;
- learner-facing study-plan generation;
- session readiness;
- feedback;
- fresh verification;
- observation drafting;
- review scheduling.

The runtime should add as little new truth as possible.

Its job is to compose existing truth safely.

### Layer 7 — independent system benchmark

Issue #47 / PR #48 adds a separate evidence domain:

> How well does Grade9V3 itself perform across the mapped subtopics?

The benchmark is not part of the learner loop.

It tests semantic behaviour across all 17 currently mapped matrices.

Its agent may measure and record.

It may not repair production code/content while measuring.

This produces:

~~~text
benchmark cases
→ observed result
→ PASS / FAIL / PARTIAL / BLOCKED_BY_SOURCE / NOT_APPLICABLE
→ gap ledger
→ maintainer handoff
~~~

Only after the complete sweep does the maintainer:

~~~text
read gaps together
→ find recurring causes
→ classify the real layer
→ choose smallest durable repair
→ fix in separate PR
→ rerun benchmark suite
~~~

This separation is central to keeping the benchmark independent.

---

## 5. The three major flows

Grade9V3 now has three separate but connected flows.

### 5.1 Academic production flow

This is the authoring/governance flow.

~~~text
source / owner request
→ plan
→ source custody
→ constrained authoring
→ candidate records
→ review
→ curation
→ build
→ release authority
~~~

Its purpose is to protect canonical material and learner-facing publications.

### 5.2 Learner self-study flow

This is the everyday personal-use flow.

~~~text
real worksheet/question set
→ question demand
→ canonical capabilities
→ delivery + prerequisites
→ study route
→ learner evidence overlay
→ session readiness
→ six-Core study
→ independent attempt
→ diagnosis
→ hint / repair
→ fresh verification
→ observation draft
→ delayed review
↺
~~~

Its purpose is to help one learner become increasingly independent.

### 5.3 System validation and repair flow

This is the Issue #47 / PR #48 workstream.

~~~text
current system
→ independent benchmark agent
→ benchmark every mapped matrix
→ record observed gaps
→ no fixes
→ handoff
→ maintainer reverse-engineering
→ smallest durable repair
→ separate repair PR
→ complete benchmark rerun
↺
~~~

Its purpose is to improve Grade9V3 without allowing the benchmark to mark its own homework.

---

## 6. One complete learner-session example

Relative Motion is currently the clearest vertical slice.

A real external question may demand:

~~~text
CAP-RELATIVE-V
+ vector checking
+ signed-coordinate arithmetic
~~~

The system does not automatically make that external question canonical.

Instead:

### Step 1 — map the question

The transient worksheet record identifies the primary and secondary capabilities.

### Step 2 — resolve delivery

The delivery resolver may find:

~~~text
CAP-RELATIVE-V → LOCAL
CAP-VECTOR-CHECK → LOCAL
CAP-SIGNED-PAIR → EXTERNAL_BRIDGE to Mathematics
~~~

### Step 3 — compute prerequisites and route

The prerequisite graph determines what must come before what.

No cross-matrix rung-number comparison is used.

### Step 4 — overlay learner evidence

If the learner already independently demonstrated the signed-coordinate prerequisite, the bridge can be skipped.

If no such evidence exists, familiarity is not enough.

The first action remains BRIDGE.

A rough parent estimate for Relative Motion may still select a local starting region, but it does not erase the bridge.

### Step 5 — readiness

The route may be structurally valid but not ready for execution:

~~~text
valid = true
ready = false
first action = BRIDGE
~~~

Once the prerequisite is genuinely satisfied:

~~~text
ready = true
~~~

and the local session can continue.

### Step 6 — independent attempt

The learner sees the question without a solution being revealed.

### Step 7 — evaluate conservatively

A human or approved evaluator supplies the outcome for free-form work.

The runner does not pretend to be a universal grader.

### Step 8 — diagnose

If the learner's work clearly shows the Relative Motion failure, local diagnosis proceeds.

If the failed capability is unclear, the runtime does not guess.

### Step 9 — repair

A confirmed misconception routes to canonical repair content.

### Step 10 — fresh verification

The learner is checked on a different same-capability item or exit task.

Seeing or repairing the original question does not itself prove mastery.

### Step 11 — observation draft

The runtime returns evidence for review.

It does not silently persist learner state.

### Step 12 — review timing

The simple deterministic rule schedules the next check.

This is the intended end-to-end experience.

---

## 7. Why the architecture is suitable for one learner

A commercial learning platform might need:

- population calibration;
- large-scale psychometrics;
- item response models;
- probabilistic knowledge tracing;
- complex scheduler optimisation;
- multi-tenant permissions;
- generalized curriculum import;
- broad automated grading.

Grade9V3 does not need those things to achieve its purpose.

For one learner, interpretability and restraint are more valuable.

The father should be able to answer:

- Why did the system choose this lesson?
- What question created this demand?
- Which prerequisite caused this ordering?
- Why is this bridge required?
- What evidence says this skill is demonstrated?
- Why did the feedback repair this concept?
- Why is this subtopic blocked?
- What exactly should happen next?

The current architecture supports those questions with inspectable records rather than hidden scoring models.

---

## 8. The key academic principles embedded in the design

### 8.1 Teach capabilities, not chapter labels

A question may superficially belong to one chapter but fail because of a reusable prerequisite elsewhere.

The capability graph exposes that.

### 8.2 Prerequisite order is semantic

Matrix coordinates organise one local progression.

They do not define global prerequisite order.

### 8.3 External questions reveal demand

They are valuable precisely because they test whether the canonical model can explain real exam questions.

But they remain transient until deliberately promoted under the repository's source/review rules.

### 8.4 Direct performance outranks estimates

The learner's actual independent attempt is more informative than an approximate percentage.

### 8.5 Help changes the meaning of success

A correct answer after substantial assistance is not treated as equivalent to an independent correct answer.

### 8.6 Repair the first supported meaningful failure

A wrong final number is not enough information.

The system tries to identify where the reasoning first meaningfully broke.

But it does not invent a diagnosis when the evidence is ambiguous.

### 8.7 Verification must be fresh

The goal is not to make the learner reproduce a solution just seen.

Repair should be followed by a new check of the same capability.

### 8.8 Context is not mastery

The same capability can appear in several stories.

Application contexts classify those stories without polluting the prerequisite/mastery graph.

### 8.9 Readiness is a claim, not a feeling

A matrix is not made SESSION_READY merely because it has a file or several rungs.

Teaching, reconstruction, diagnosis, repair, verification and prerequisite delivery must be sufficiently represented.

### 8.10 Real use decides future architecture

The project explicitly rejects speculative platform expansion.

---

## 9. Separation-of-concerns table

| Layer | Owns | Must not silently become |
| --- | --- | --- |
| Canonical subject content | capabilities, prerequisites, microtopics, matrices, question families, misconceptions, teaching | learner-specific state |
| Six Cores | learner-facing forms of canonical content | a second curriculum |
| Source/review authority | custody, provenance, review, curation, release | pedagogy or mastery |
| Worksheet/session | transient real-question demand | permanent curriculum/source authority |
| Learner evidence | what this learner demonstrated, help, error observations, review timing | canonical academic truth |
| Shared runtime | mapping, routing, readiness, feedback orchestration | topic-specific academic truth |
| Application context | reusable situation/setting metadata | capability or prerequisite |
| Benchmark evidence | what happened when Grade9V3 was tested | learner evidence or production fix |

---

## 10. Current readiness and known gaps

The readiness snapshot associated with the self-study candidate reports the following practical state.

### Physics — SESSION_READY

- One-dimensional motion
- Newton's first law and free-body diagrams
- Simple machines
- Sound
- Work, energy and power

### Physics — SESSION_READY_WITH_BRIDGE

- Relative motion

The bridge is signed-coordinate arithmetic supplied by Mathematics.

### Physics — PILOT_READY

- Vector representation and subtraction

The teaching exists, but Core1A/Core1B route coverage remains incomplete.

### Physics — NOT_READY

- Current electricity, Ohm's law and circuit analysis
- Fluid statics, buoyancy and Bernoulli flow
- Universal gravitation, free fall and orbital motion
- Magnetic fields, Lorentz force and electromagnetic induction
- Reflection and spherical mirrors
- Oscillations, simple harmonic motion and waves
- Rotational dynamics, angular momentum and rolling
- Thermodynamics and heat engines
- Vector addition, subtraction and orientation

### Mathematics

The currently represented one-unknown linear-equations matrix is SESSION_READY.

This is not a claim that the Mathematics syllabus is complete.

### High-value visible content gaps

Vector addition/decomposition is a particularly important current gap for later Motion-in-a-Plane work.

Gravitation also retains matrix rungs without canonical microtopics.

The architecture's intended response is not to weaken readiness.

It is to fill the smallest durable academic gap when real question demand or the benchmark justifies doing so.

---

## 11. The independent benchmark strategy — Issue #47 / PR #48

The benchmark exists because one successful Relative Motion pilot is not enough to prove the routing model behaves well across the repository.

The benchmark covers all 17 currently mapped matrices:

- 16 Physics matrices;
- 1 Mathematics matrix.

For each subtopic, the benchmark may test applicable situations such as:

- direct mapping;
- prerequisite routing;
- multi-capability questions;
- repeated demand;
- unknown learner;
- rough parent estimate;
- prior evidence;
- external bridge;
- content gap;
- incomplete source/figure;
- feedback diagnosis;
- repair;
- fresh verification;
- help-dependent success;
- independent success.

It must not manufacture irrelevant cases.

Non-applicable cases are explicitly NOT_APPLICABLE.

The benchmark agent's production write boundary is intentionally narrow.

It writes benchmark artifacts only.

It does not edit:

- Shared runtime;
- Physics content;
- Mathematics content;
- schemas;
- learner profiles;
- source custody;
- production academic records.

Every meaningful failure is recorded in the gap ledger with observed facts and remains UNANALYSED.

The maintainer then sees all gaps together.

That sequencing matters because several apparent content failures may share one routing defect, or several runtime symptoms may come from one missing canonical capability.

The preferred repair process is therefore:

~~~text
many observations
→ pattern
→ reproduced root cause
→ smallest durable repair
→ regression/falsifier
→ full benchmark rerun
~~~

rather than:

~~~text
one failure
→ one patch
→ next failure
→ another patch
~~~

---

## 12. The future road plan — PR #49

The future road plan is deliberately a parking lot of evidence-gated ideas.

It is not a commitment to add features.

Each idea has:

- a trigger;
- the smallest likely change;
- an explicit instruction not to build a larger subsystem unless evidence requires it.

The current future candidates are described below.

### 12.1 Method-selection / discrimination practice

Potential trigger:

> The learner can execute individual methods when named but struggles to choose the method in mixed unlabelled questions.

Likely smallest response:

> Add/tag a small class of method-selection questions using existing capabilities and question infrastructure.

Do not create a new Core or a strategy-selection platform.

### 12.2 Progressive removal of support

Potential trigger:

> Correct performance remains dependent on hints or immediate worked examples.

Likely smallest response:

~~~text
guided attempt
→ lighter help
→ independent attempt
→ delayed independent check
~~~

Use current evidence/help fields first.

### 12.3 Lightweight Study / Test / Past-paper modes

Potential trigger:

> Study performance is good but mixed/timed exam performance is materially worse.

Likely smallest response:

> Reuse the same session runner with stricter assistance policies.

Do not create a separate exam architecture.

### 12.4 Exam-response completeness

Potential trigger:

> The learner understands the idea but repeatedly loses marks because required reasoning, terminology, units or conditions are omitted.

Likely smallest response:

> Where reliable rubric/mark-scheme evidence exists, distinguish conceptual correctness from exam-credit completeness.

Do not build a universal essay/free-response grader.

### 12.5 Review-policy tuning

Potential trigger:

> Real use shows the 1/3/7/14 schedule is consistently inappropriate.

Likely smallest response:

> Adjust the deterministic rule.

Do not introduce a sophisticated forgetting model by default.

### 12.6 Lightweight question-demand progression

Potential trigger:

> Routine questions are consistently passed while unfamiliar/composite questions fail, and current metadata cannot explain the difference.

Likely smallest response:

> Add a few useful demand labels such as routine, multi-step, mixed-capability, unfamiliar/transfer.

Prefer question metadata over fake capability levels.

### 12.7 Optional confidence capture

Potential trigger:

> Wrong-and-confident behaviour repeatedly requires a different repair from wrong-and-unsure behaviour.

Likely smallest response:

> Capture a coarse confidence signal on selected items.

Confidence remains evidence context, not mastery.

### 12.8 Parent-facing session summary

Potential trigger:

> The father repeatedly has to inspect raw internal output to understand what happened.

Likely smallest response:

> Generate a short view over existing evidence: attempted, demonstrated, uncertain, repaired, due next, blocked.

Do not create another state store.

---

## 13. Explicit non-goals

Unless real evidence becomes overwhelming, the project should not become:

- a Bayesian knowledge-tracing platform;
- an Item Response Theory system;
- a probabilistic mastery dashboard;
- an enterprise multi-user product;
- a universal curriculum import engine;
- a universal free-form grading system;
- a sophisticated adaptive scheduler;
- an automatic external-question canonicalizer;
- a system with a new capability for every exam story;
- a system with learner state embedded in canonical content;
- a system where benchmark results are treated as learner data.

The project is allowed to remain small.

---

## 14. Anti-drift rules that define the concept

The most important rules, collected in one place, are:

1. **No new Core unless the existing six genuinely cannot represent an observed need.**
2. **No matrix per worksheet.**
3. **No rung per question.**
4. **No learner state in canonical academic content.**
5. **No global cross-matrix ordering from local ladder positions.**
6. **No source authority from authored/generated questions.**
7. **No mastery claim from a rough percentage.**
8. **No invented mapping, failed capability, missing figure or source information.**
9. **No application context in prerequisite topology.**
10. **No automatic promotion of external worksheet questions into canonical content.**
11. **No silent learner-state persistence from the feedback runner.**
12. **No weakening readiness merely to increase the number of usable matrices.**
13. **No benchmark agent fixes while the benchmark is still measuring.**
14. **No local patch before recurring benchmark symptoms are considered together.**
15. **No new Shared abstraction unless a concrete end-to-end case cannot be represented.**
16. **No architecture work after successful real use unless a demonstrated problem requires it.**

---

## 15. What success should look like for the learner

The system succeeds when the learner can increasingly do the following without intervention:

1. receive a sensible route from a real worksheet;
2. start at an appropriate point rather than restarting the whole topic;
3. see prerequisites that genuinely matter;
4. satisfy or verify external bridges when required;
5. use appropriate six-Core materials;
6. attempt questions before being shown solutions;
7. receive targeted, non-spoiling help after a real mistake;
8. repair the actual gap rather than repeating an entire chapter;
9. pass a fresh verification question independently;
10. retain the capability on later review;
11. eventually select the right method in mixed work without being told the topic;
12. perform under real exam constraints if/when that becomes an observed need.

The long-term success metric is therefore not how much architecture exists.

It is how little scaffolding the learner eventually needs.

---

## 16. What success should look like for the maintainer/father

The parent should not need to operate the repository as an educational software company.

A successful system should make these questions easy to answer:

~~~text
What is this question testing?
What must be known first?
Where is that taught?
Is the teaching actually ready?
What does she already know?
Where should she start?
What went wrong?
What is the smallest repair?
What should she try next?
When should it be checked again?
Is this a learner problem or a system/content problem?
~~~

If answering these questions requires reading internal code, the view layer should improve.

If answering them requires inventing new state, the architecture should not be expanded until real evidence shows the existing model is insufficient.

---

## 17. The complete concept in one map

~~~mermaid
flowchart TB
    subgraph FOUNDATION["Canonical academic + authority foundation"]
        CAP["Capabilities + prerequisite graph"]
        MAT["Matrices / rungs / microtopics"]
        QF["Question families + application contexts"]
        SIX["Six Cores"]
        SRC["Sources / custody / review / release authority"]
        CAP --> MAT
        MAT --> SIX
        QF --> CAP
        SRC --> SIX
    end

    subgraph LEARNER["Personal self-study loop"]
        IN["Real worksheet / questions"]
        MAP["Transient question → capability map"]
        DEL["Capability delivery
LOCAL / EXTERNAL_BRIDGE /
UNRESOLVED / AMBIGUOUS"]
        ROUTE["Prerequisite closure + study route"]
        EVID["Learner evidence
attempts > prior diagnostics > estimate"]
        START["Starting action
QUICK_CHECK / START_HERE /
STUDY / BRIDGE / SKIP"]
        READY["Session readiness"]
        STUDY["Six-Core study"]
        ATT["Independent attempt"]
        FB["Supported diagnosis
hint / repair"]
        VER["Fresh verification"]
        OBS["Observation draft"]
        REV["1 / 3 / 7 / 14 review"]

        IN --> MAP --> DEL --> ROUTE
        EVID --> START
        ROUTE --> START --> READY --> STUDY --> ATT --> FB --> VER --> OBS --> REV --> ATT
        OBS --> EVID
    end

    FOUNDATION --> MAP
    FOUNDATION --> DEL
    FOUNDATION --> READY
    FOUNDATION --> STUDY

    subgraph BENCH["Independent Grade9V3 benchmark loop"]
        B1["Benchmark 17 mapped matrices"]
        B2["Observe only"]
        B3["PASS / FAIL / PARTIAL /
BLOCKED / N/A"]
        B4["GAPS.md
UNANALYSED"]
        B5["Maintainer clusters symptoms
and reproduces causes"]
        B6["Smallest durable repair
separate PR"]
        B7["Rerun complete benchmark"]
        B1 --> B2 --> B3 --> B4 --> B5 --> B6 --> B7 --> B1
    end

    FOUNDATION --> B1
~~~

The learner loop and benchmark loop touch the same academic system but produce different evidence.

That distinction should remain permanent.

---

## 18. Near-term operational sequence

Assuming the current ready/draft work is merged as intended, the next sensible operating sequence is:

~~~text
1. preserve current architecture
2. complete the independent 17-matrix benchmark
3. run genuine learner sessions on ready matrices
4. collect benchmark gaps separately from learner observations
5. inspect benchmark gaps together
6. reproduce recurring causes
7. repair the smallest correct layer
8. rerun the complete benchmark
9. continue real learner use
10. promote future-road ideas only when triggered
~~~

This sequence intentionally places observation before invention.

---

## 19. Final interpretation

Grade9V3 has evolved into three coordinated systems:

### A. A governed academic-content system

It answers:

> What is the academic truth, where did it come from, and what authority does it have?

### B. A personal self-study system

It answers:

> Given this learner and these real questions, what should happen next?

### C. An independent system-quality loop

It answers:

> When Grade9V3 is tested across its mapped academic surface, where does the system itself fail?

The strength of the design is the boundaries between these systems.

The future direction should therefore not be to add more machinery by default.

It should be to preserve those boundaries while improving only what live learner evidence and independent benchmark evidence show to be weak.

The core principle is:

> **Question sets reveal demand. Canonical capabilities and matrices hold durable academic structure. Source/review machinery controls authority. Learner evidence changes routing, not truth. Feedback repairs the smallest supported gap. Benchmark evidence improves the system, not the learner model. Real use decides what deserves to be built next.**
