# First live learner session — Physics Relative Motion Q4

> Status: **session packet only — no learner evidence recorded yet**
>
> This adapts the earlier Mathematics-style real-session procedure to the current Physics case.
> It does not change curriculum/runtime behavior and it does not pre-label any learner misconception.

## Purpose

Run one actual learner episode against the owner-supplied NEETPrep Relative Motion Q4 and
retain only what the learner really does.

Use the original external Q4 from the source page. Do **not** copy or rewrite the external
question into canonical content just for this session.

Repository mapping:

```text
question
NEETPREP-MQB-REL-Q4

primary
CAP-VEC-RESULTANT-CONSTRAINT

secondary
CAP-RELATIVE-V
```

The relevant reusable learning chain is:

```text
CAP-VECTOR-SIGNED-COMPONENT
        ↓
CAP-VEC-COMPONENT-SUM
        ↓
CAP-VEC-RESULTANT-CONSTRAINT
        +
CAP-RELATIVE-V
```

Any Mathematics bridge needed for signed-coordinate handling remains explicit. No bridge is
converted into Physics mastery merely because the learner can continue the session.

---

## 1. Before the learner sees help

Session reference:

```text
SESSION-REAL-PHY-REL-Q4-01
```

Record:

- date/time;
- learner's original written work or a clear photo;
- final answer exactly as given;
- any diagram, axis declaration, component equation, or verbal explanation;
- whether any help was used before submission.

Do not supply:

- the relevant capability names;
- the required component equation;
- a worked vector diagram;
- the cancellation condition;
- a hint about which quantity should be zero.

The first attempt should be genuinely cold.

If the parent wants to provide a rough topic estimate before the session, record it separately.
It is routing input only and must not be converted into mastery evidence.

---

## 2. Cold attempt

Present the original NEETPrep Q4.

Instruction to learner:

> Solve it in your normal exam style. Show enough working that another person can follow how
> you decided the direction/components. Ask for help only if you genuinely need it.

Capture the attempt before discussing it.

### What matters in Physics that was less visible in the Mathematics case

Do not record only the numerical/final answer.

Also preserve, if present:

- chosen positive directions;
- vector or velocity labels;
- component signs;
- a sketch;
- the equation used to combine velocities;
- the condition used to represent "directly opposite";
- units and physical interpretation.

Those details are what allow a supported diagnosis instead of guessing from a final number.

---

## 3. Evaluate the attempt only after submission

The primary question is:

> Did the learner translate the required **resultant direction** into a component constraint
> and solve the compensating input component correctly?

Possible evidence patterns are:

### A. Signed-component representation failure

Use only if the work actually shows a sign/axis problem.

Capability:

`CAP-VECTOR-SIGNED-COMPONENT`

Examples of observable evidence:

- positive direction is changed mid-solution;
- a westward/upstream component is written with the wrong sign after axes were declared;
- the learner treats signed components as unsigned speeds.

### B. Vector component-sum failure

Use only if the work actually shows incorrect vector composition.

Capability:

`CAP-VEC-COMPONENT-SUM`

Examples of observable evidence:

- magnitudes are added instead of corresponding components;
- x and y contributions are mixed;
- one vector contribution is omitted from the resultant.

### C. Resultant-constraint failure

This is the primary Q4 capability.

Capability:

`CAP-VEC-RESULTANT-CONSTRAINT`

Examples of observable evidence:

- the learner makes the swimmer's along-river component zero instead of the **resultant**
  along-river component;
- the learner never converts "directly opposite" into a zero-resultant-component condition;
- the compensating component has the wrong sign despite otherwise correct component addition.

### D. Relative-velocity/frame failure

Use only when the work shows the frame composition itself is wrong.

Capability:

`CAP-RELATIVE-V`

Examples of observable evidence:

- swimmer-relative-water and water-relative-ground velocities are combined in the wrong frame;
- the learner uses an observer subtraction/composition relation inconsistent with the stated
  quantities.

### E. Ambiguous failure

If the written work does not establish which capability failed:

```text
result = UNCERTAIN
failed capability = not assigned
→ ask one discriminating question
→ do not guess
```

A wrong final answer by itself is not enough to choose A/B/C/D.

---

## 4. Least-help feedback ladder

Use the smallest intervention that can reveal or repair the first supported failure.

### Hint 1 — identify the physical constraint

Ask:

> If the learner must arrive directly opposite, what must be true about the **along-river
> component of the ground-relative resultant velocity**?

Do not give the equation yet.

### Hint 2 — expose the component equation

If needed, ask:

> Write only the along-river component relation:
> swimmer contribution + current contribution = ground-result contribution.
> What value must the ground-result component have for "directly opposite"?

### Repair — canonical concept

If the failure is confirmed as `CAP-VEC-RESULTANT-CONSTRAINT`, use the existing canonical
repair principle:

> Apply the condition to the **resultant**, not to each input vector. Opposite signed
> components can cancel while the individual vectors remain angled.

Do not restart the whole Relative Motion topic unless the learner's work shows a wider gap.

### Stronger support

Only if the learner still cannot proceed, return to the prerequisite actually failing:

```text
signed components
or
component-wise vector addition
or
relative-velocity composition
```

Record the help level actually used.

---

## 5. Fresh verification

Repair of the original Q4 is not enough evidence by itself.

Use the canonical fresh verification already attached to
`CAP-VEC-RESULTANT-CONSTRAINT`:

> In one frame, a current contributes +3 along the x-axis. Choose the swimmer's x-component
> so the combined velocity has x-component 0, and state the equation you used.

Expected reasoning is structurally:

```text
0 = swimmer_x + 3
→ swimmer_x = -3
```

This is a capability check, not another copy of the river-crossing question.

The learner should attempt this fresh item **without help** after the repair if possible.

---

## 6. Evidence interpretation

Do not convert every successful endpoint into `DEMONSTRATED`.

Use the actual sequence.

### Independent cold Q4 correct

Record the direct attempt faithfully.

A fresh verification should still be retained for empirical acceptance because the purpose of
this episode is to show that the reusable capability, not just one external item, is available.

### Cold Q4 incorrect, then repaired

The original attempt may support `MISSING` or `UNCERTAIN` depending on how clearly the
failure is attributable.

A later correct answer after a hint/repair does not erase the original evidence.

### Fresh verification correct independently

After human review, this can support a new direct observation for
`CAP-VEC-RESULTANT-CONSTRAINT` with independence recorded as `NONE` help for that fresh
verification.

### Fresh verification needs help or remains wrong

Keep the capability below demonstrated state. Record the actual help and result.

### No canonical fresh verification

Not expected for this capability, but the general repository rule still applies:

```text
independent correctness
+ no canonical fresh verification
→ UNCERTAIN
not DEMONSTRATED
```

---

## 7. Capture sheet

Fill this from the real session only.

```text
Session:
SESSION-REAL-PHY-REL-Q4-01

Question:
NEETPREP-MQB-REL-Q4

Cold attempt
------------
Final answer:
<actual learner answer>

Working/reasoning:
<verbatim summary or retained image reference>

Diagram / axes / components:
<what the learner actually wrote>

Help before submission:
NONE / HINT / WORKED_EXAMPLE / SOLUTION

Evaluator result:
CORRECT / INCORRECT / UNDECIDABLE

First supported failure:
<capability ref, or AMBIGUOUS>

Error stage:
CONCEPT / SETUP / EXECUTION / CARELESS / UNKNOWN

Feedback actually used:
<none / exact hint / repair>

Fresh verification
------------------
Learner response:
<actual response>

Help used:
NONE / HINT / WORKED_EXAMPLE / SOLUTION

Verification result:
CORRECT / INCORRECT / UNDECIDABLE

Review decision
---------------
Observation to persist:
YES / NO

Capability:
<capability ref>

State:
DEMONSTRATED / UNCERTAIN / MISSING

Provenance:
LIVE_LEARNER

Evidence kind:
DIRECT_ATTEMPT
```

---

## 8. What should be sent back for review

After the session, provide:

1. the learner's cold Q4 answer;
2. the actual written working or a clear photo;
3. any help used before/after the first submission;
4. the fresh-verification response;
5. anything the learner said that materially explains the reasoning.

Do **not** summarize the learner as "weak at vectors" or similar before the work is reviewed.
Send the evidence first.

---

## 9. Acceptance boundary

This session is evidence about the learner.

If it instead exposes a system defect, keep the two workstreams separate:

```text
live learner/session observation
        ↓
record in empirical acceptance

system defect
        ↓
separate repair PR
        ↓
smallest durable fix
        ↓
full benchmark rerun if shared semantics changed
        ↓
rebase acceptance branch
```

Do not repair production architecture inside the learner-evidence PR.

---

## Stop condition

The session packet is complete when the real cold attempt and fresh verification have been
captured.

Until that happens:

```text
empirical status = PENDING_REAL_EVIDENCE
```
