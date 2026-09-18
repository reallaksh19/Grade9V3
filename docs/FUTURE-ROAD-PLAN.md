# Grade9V3 — Future Road Plan

> Status: evidence-gated future ideas only.
>
> This is **not** a new implementation plan and does not change the current learner flow.
> The current architecture remains the authority until real learner use or the independent benchmark demonstrates a concrete limitation.

## 1. Purpose

Grade9V3 is a personal, self-paced learning system for one learner.

The current priority is to make the existing workflow reliable:

~~~text
worksheet / questions
→ capability mapping
→ prerequisite + delivery resolution
→ learner-aware study route
→ readiness gate
→ six-Core study
→ attempt
→ diagnosis / hint / repair
→ fresh verification
→ learner observation
→ delayed review
~~~

Future work should be added only when it solves a demonstrated learner or system problem.

The governing rule is:

~~~text
observed problem
→ evidence
→ classify the layer
→ smallest durable fix
→ falsifier/regression test
→ rerun the relevant benchmark
~~~

Do not add features because a general learning platform might need them.

---

## 2. Immediate road after the current PR stack

### A. Complete the independent Question → Study Map benchmark

Issue #47 / PR #48 owns the independent benchmark workstream.

The benchmark agent:

- measures all currently mapped matrices;
- records PASS / FAIL / PARTIAL / BLOCKED_BY_SOURCE / NOT_APPLICABLE;
- writes benchmark evidence only;
- records meaningful gaps in GAPS.md;
- does not modify production runtime, schemas or academic content;
- leaves root-cause analysis and repairs to the maintainer.

Benchmark evidence is evidence about **Grade9V3**, not evidence about the learner.

### B. Run real learner sessions

Use actual school/exam questions and record only what genuinely happens.

Look especially for:

- wrong question-to-capability mapping;
- missing or excessive prerequisite routing;
- unnecessary teaching;
- external bridges that are confusing or blocking;
- hints that reveal too much or too little;
- inability to diagnose the failed capability safely;
- repair that does not lead to successful fresh verification;
- review timing that is annoying or ineffective.

Do not fabricate learner outcomes to exercise the system.

### C. Analyse benchmark gaps together

After the independent sweep, read the gap ledger as a whole before fixing individual symptoms.

Look for recurring causes across subtopics, for example:

~~~text
mapping problem
content problem
source/custody problem
prerequisite topology problem
delivery/readiness problem
feedback problem
question-family/context problem
~~~

A recurring cause should normally receive one durable repair rather than several case-specific patches.

### D. Repair separately

Every repair should be a separate, reviewable change with:

~~~text
observed failure
→ proven/reproduced cause
→ smallest fix
→ falsifier test
→ benchmark rerun
~~~

Shared/core changes should not be made when a content-only repair is sufficient, and content should not be expanded to hide a Shared/core defect.

---

## 3. Future academic ideas — implement only when triggered

The following are useful possibilities, not commitments.

### 3.1 Method-selection / discrimination practice

**Trigger**

The learner can execute methods when the method is obvious or named, but performs poorly when several possible methods are mixed.

Example:

~~~text
can solve:
- Pythagoras questions
- trigonometry questions
- similarity questions

but struggles to decide which one applies in an unlabelled mixed set
~~~

**Smallest likely change**

Add or tag a small class of questions that asks the learner to identify the appropriate method before solving.

This should reuse existing capabilities and question infrastructure.

**Do not build**

- a new Core;
- a new mastery dimension;
- a general strategy-selection engine.

---

### 3.2 Progressive removal of support

**Trigger**

The learner repeatedly succeeds only after hints or immediately after seeing worked material.

**Smallest likely change**

Prefer a sequence such as:

~~~text
guided attempt
→ lighter hint
→ independent attempt
→ delayed independent check
~~~

Use existing help/evidence fields before introducing any new learner model.

**Do not build**

A numeric independence score unless real use proves the existing evidence cannot express the problem.

---

### 3.3 Lightweight test / past-paper mode

**Trigger**

The learner performs well during normal study but underperforms on mixed or timed exam work.

**Smallest likely change**

Allow the existing session runner to operate with stricter assistance rules, for example:

~~~text
STUDY
hints / repair allowed

TEST
no help until submission

PAST_PAPER
original question order / timing / marking conditions where available
~~~

This should be an orchestration mode over the existing system, not a seventh Core or a second learning architecture.

---

### 3.4 Exam-response completeness

**Trigger**

The learner understands the concept but repeatedly loses marks because the written response omits required reasoning, terminology, units, conditions or intermediate steps.

**Smallest likely change**

Where reliable mark-scheme/rubric evidence exists, distinguish:

~~~text
conceptually correct
vs
exam-credit complete
~~~

This is most likely to matter in Physics and other structured-response subjects.

**Do not build**

A universal free-response grading engine.

---

### 3.5 Review-schedule tuning

**Trigger**

Real use shows the current simple 1/3/7/14-day review policy is clearly too frequent, too sparse or poorly matched to repeated failures.

**Smallest likely change**

Adjust the small deterministic policy using observed outcomes.

Keep it understandable to the learner and parent.

**Do not build**

A sophisticated spaced-repetition or probabilistic forgetting model unless the simple policy demonstrably fails.

---

### 3.6 Lightweight question-demand progression

**Trigger**

The learner repeatedly passes routine questions but fails unfamiliar/composite questions, and the existing question metadata cannot explain or route that difference.

**Smallest likely change**

Add only the minimum useful demand labels, such as:

~~~text
routine
multi-step
mixed-capability
unfamiliar/transfer
~~~

Prefer question/family metadata over creating artificial capability levels.

**Do not build**

A large multidimensional difficulty model.

---

### 3.7 Confidence capture

**Trigger**

Repeated sessions show a meaningful difference between:

~~~text
wrong + unsure
wrong + strongly confident
~~~

and the distinction would change the repair decision.

**Smallest likely change**

Optionally capture a coarse learner confidence response for selected questions.

**Do not build**

Confidence scoring by default or treat confidence as mastery evidence.

---

### 3.8 Parent-facing session summary

**Trigger**

The father must repeatedly inspect raw internal output to understand what happened in a session.

**Smallest likely change**

Generate a short summary from existing data:

~~~text
What was attempted?
What was demonstrated?
What remains uncertain?
What was repaired?
What is due next?
What is blocked by content/source/bridge?
~~~

This should be a view over existing evidence, not a second state store.

---

## 4. Ideas that should remain out of scope unless evidence becomes overwhelming

Do not add these merely for completeness:

- Bayesian knowledge tracing;
- Item Response Theory;
- probabilistic mastery percentages;
- enterprise/multi-user account architecture;
- generalized curriculum-planning engines;
- universal automatic grading of open responses;
- sophisticated adaptive schedulers;
- new Core products;
- a matrix/rung for every worksheet or question;
- automatic promotion of external questions into canonical content;
- learner state inside canonical capabilities or matrices;
- benchmark observations inside learner state;
- case-specific capabilities created only because the story/context changed.

---

## 5. Promotion rule: when a future idea becomes real work

A future idea should move into an implementation issue only when there is concrete evidence such as:

- a repeated live-learner failure;
- a reproducible benchmark failure;
- the same symptom across multiple matrices;
- a workflow burden that repeatedly requires manual intervention.

Before implementing:

1. record the observed symptom;
2. identify whether it is learner, content, source, mapping, topology, readiness, feedback or UI/view-layer related;
3. check whether the current model already represents it;
4. choose the smallest change that solves the demonstrated problem;
5. add a falsifier/regression test;
6. rerun affected benchmark cases;
7. rerun the complete benchmark suite when the change affects shared behaviour.

If the current architecture can already represent the case, prefer better content/data or a better view over a new abstraction.

---

## 6. Evidence domains must stay separate

Keep these distinctions explicit:

| Evidence | Question answered |
|---|---|
| Learner observation | What happened to this learner? |
| Worksheet/question mapping | What does this question demand? |
| Canonical content | What is the durable academic structure? |
| Source/review evidence | What is grounded and authorised? |
| Benchmark evidence | What happened when Grade9V3 itself was tested? |

None of these should silently substitute for another.

---

## 7. Long-term success condition

The long-term goal is not to make Grade9V3 increasingly complex.

It is to make the learner increasingly independent.

A mature version should help the learner:

- start at the right place;
- understand what a difficult question requires;
- repair genuine gaps without unnecessary reteaching;
- select methods without being told the chapter;
- solve fresh questions independently;
- retain important knowledge;
- perform under real exam conditions when needed.

If the existing architecture already achieves those outcomes reliably, the correct roadmap action is **no new architecture**.

---

## Final principle

> **Use live learner evidence and independent benchmark evidence to decide what deserves to exist. Preserve the current architecture until a demonstrated failure proves that the smallest durable fix requires something more.**
