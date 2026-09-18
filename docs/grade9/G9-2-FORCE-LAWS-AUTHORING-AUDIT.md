# G9-2 Force and Laws of Motion authoring audit

> Workstream: **Grade 9 Physics only**
>
> Matrix: `MATRIX-PHY-NLM-FIRST-LAW`
>
> Result: **reuse the existing seven-rung canonical matrix, keep the frame-choice rung as an explicit question-demand extension, and remove one false cross-matrix prerequisite.**

## Authoritative scope checked

The current CBSE Academic **Class IX Science (2026-27), Standard** syllabus lists *Force and
Laws of Motion* in Unit III. Its key concepts explicitly include:

- force;
- balanced and unbalanced forces;
- friction;
- Newton's first law;
- Newton's second law;
- Newton's third law.

Its learning outcomes require learners to reason about force magnitude/direction, balanced
and unbalanced forces, friction, zero net force with constant velocity, acceleration caused
by force, Newton's first/second/third laws, calculation with the second-law expression, and
everyday applications.

Official locator:

`https://cbseacademic.nic.in/web_material/CurriculumMain27/SecPart1/ScienceSt_SecP1_2026-27.pdf`

Relevant section: **Force and Laws of Motion, PDF page 15 (document lines around 711-738 in
the extracted text).**

The same official document prescribes a Newton's Second Law practical using a trolley,
pulley and hanging masses.

This scope check controls the current authoring pass. It does **not** promote any repository
record to `PRESCRIBED`; the repository's exact curriculum-binding registry remains the
authority for that stronger claim.

## Current matrix-to-scope working sheet

`SCOPE_REASON` is planning metadata only. It is not persisted into the matrix schema.

| Rung | Canonical microtopic | Primary capability | SCOPE_REASON | Grade-9 decision |
| --- | --- | --- | --- | --- |
| R1 | `MIC-PHY-NLM-NET-ZERO-MOTION` | `CAP-NLM-NET-ZERO-MOTION` | `SYLLABUS_REQUIREMENT` | Keep; directly supports first-law / zero-net-force reasoning |
| R2 | `MIC-PHY-NLM-FORCES-SUM-ZERO` | `CAP-NLM-FORCES-SUM-ZERO` | `SYLLABUS_REQUIREMENT` | Keep; balanced/unbalanced forces require distinguishing individual forces from their net |
| R3 | `MIC-PHY-NLM-FBD-BODY-OWNERSHIP` | `CAP-NLM-FBD-BODY-OWNERSHIP` | `PREREQUISITE` | Keep; reusable representation/ownership skill for Newton II/III, not a separate syllabus claim |
| R5 | `MIC-PHY-NLM-FRICTION` | `CAP-NLM-FRICTION` | `SYLLABUS_REQUIREMENT` | Keep; friction is explicit |
| R6 | `MIC-PHY-NLM-SECOND-LAW` | `CAP-NLM-SECOND-LAW` | `SYLLABUS_REQUIREMENT` | Keep; force calculation and practical demand are explicit |
| R7 | `MIC-PHY-NLM-THIRD-LAW` | `CAP-NLM-THIRD-LAW` | `SYLLABUS_REQUIREMENT` | Keep; Newton III and applications are explicit |
| R4 | `MIC-PHY-NLM-FRAME-CHOICE` | `CAP-NLM-FRAME-CHOICE` | `QUESTION_DEMAND` / `DECLARED_EXTENSION` | Keep canonical and routable because an existing external JEE pilot requires it; do not present it as ordinary Grade-9 Standard scope |

## Why the frame-choice rung stays

The current Grade-9 Standard syllabus does not require accelerating-frame/pseudo-force
reasoning. However, the repository already has real external demand:

`EXAMSIDE-MIP-2021-08-26-BOMB`

maps `CAP-NLM-FRAME-CHOICE` as a secondary capability in the Motion-in-a-Plane pilot.

Deleting the rung merely to make the matrix look Grade-9-pure would make that existing
extension demand unroutable. The correct separation is therefore:

```text
ordinary Grade-9 Force/Laws route
→ R1/R2/R3/R5/R6/R7

explicit advanced question demand
→ may additionally route R4 frame choice
```

No curriculum authority is inferred from that question.

## Prerequisite correction

Before this pass, `CAP-NLM-NET-ZERO-MOTION` depended on
`CAP-KIN-ZERO-V-NONZERO-A`, the Motion turning-point diagnostic.

Counterfactual check:

> Can a learner understand and demonstrate “zero net force is compatible with unchanged
> velocity” without first mastering the special case “zero instantaneous velocity can
> coexist with nonzero acceleration at a turning point”?

Yes.

That turning-point distinction is useful enrichment/application, but it is not true prior
knowledge for Newton's first law. Keeping it as a prerequisite made a core Grade-9
force-law route depend on the G9-1 diagnostic extension.

The capability prerequisite and matching microtopic/teaching-step input are therefore
removed.

The **bucket-level** prerequisite on `BUCKET-PHY-KIN-1D-MOTION` remains. It records the
curriculum/content sequence for publication composition without forcing one arbitrary
Motion capability into every Newton-law study route.

## Four QA checks

### 1. Is each rung justified?

Yes: R1/R2/R5/R6/R7 are direct syllabus demand; R3 is a reusable prerequisite/representation
skill; R4 has explicit external question demand and is kept as extension only.

### 2. Does canonical teaching already exist?

Yes. All seven matrix rows already resolve to current canonical microtopics/capabilities.
No duplicate Grade-9 force-law teaching is created.

### 3. Is each row independently fail-able?

Yes. The learner can separately fail net-zero motion reasoning, force cancellation,
body ownership, friction direction, second-law force/acceleration reasoning, third-law
pairing, or the extension frame-choice decision.

### 4. Is any apparent need merely context?

Yes. Carts, swimmers, boxes, conveyor belts, horses/carts and vehicle stories reuse these
capabilities. No story-specific capability is added.

## What is deliberately not changed

- No grade/class field is added to the matrix.
- No momentum-conservation/collision capability is added just because historical Grade-9
  treatments sometimes included it.
- No frame-choice capability is relabelled as Grade-9 prescribed content.
- No source question is canonicalised merely because it supplied extension demand.
- No record is promoted beyond `CANDIDATE`.
- The existing Motion bucket prerequisite remains as publication composition context.

## G9-2 disposition

```text
current seven-rung Newton-law matrix
→ current Grade-9 Standard scope checked
→ six rows belong to the ordinary Grade-9 learning spine
→ frame-choice row retained only for explicit extension/question demand
→ false turning-point prerequisite removed
→ no missing Grade-9 Force/Laws teaching identified
→ proceed to G9-3 Gravitation after guardrails are green
```
