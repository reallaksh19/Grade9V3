# Issue #19 real-worksheet acceptance status

Issue #19 requires one **real worksheet** whose questions span more than one
subtopic/matrix, followed by a manual demonstration of:

```text
question
→ primary / meaningful secondary capability
→ prerequisite closure
→ canonical microtopic / matrix rung
```

This acceptance is currently **BLOCKED BY MISSING INPUT**, not by subject architecture.

## Search performed

On 2026-09-18 the implementation checked both available places a retained worksheet
could legitimately exist without inventing one:

1. the Issue #19 branch repository tree, including names matching worksheet, question
   set/bank, paper, exam, sample paper, assessment and similar terms;
2. the current project/conversation file surface.

Result:

- the repository holds no retained worksheet/question-set/sample-paper asset;
- the project file surface contains the prior architecture transcript and the screenshot
  supplied for product-context discussion, not a worksheet/question paper.

Issue #19 already records the same repository-side finding in its earlier execution
classification comment.

## What qualifies

A future input may satisfy this acceptance when it is a real supplied or retained
worksheet/question set and:

- contains identifiable questions;
- spans at least two existing matrices/subtopics;
- preserves enough source identity to distinguish the actual questions from authored
  substitutes;
- can be mapped question-by-question without altering canonical learner-independent
  content merely to force a match.

The worksheet does **not** have to be source-custody material for Core2 in order to test
the mapping workflow. But its identity and wording must be real enough that the mapping
demonstration is about the supplied worksheet, not an invented proxy.

## What must not be used as a substitute

The acceptance must remain blocked rather than being satisfied with:

- a synthetic worksheet authored solely for this checkbox;
- a list assembled from canonical library questions and relabelled as a worksheet;
- a donor PR question collection with no evidence it was the real worksheet being
  analysed;
- a single-matrix practice set;
- learner-specific observations masquerading as curriculum content.

## What is already proven without the worksheet

The branch already proves the underlying subject-content machinery independently:

- matrix → microtopic closure for present canonical rungs;
- microtopic → primary-capability closure;
- prerequisite resolution and cycle freedom;
- cross-matrix dependencies through capability edges rather than ladder positions;
- representative authored question ownership by primary capability;
- sparse meaningful secondary capability mapping;
- an 11-question reviewer-facing trace sample across Physics and Mathematics;
- truthful OWNER_EXTENSION/AUTHORED/CANDIDATE authority where source-backed authority is
  absent;
- generated-artifact reproducibility and full repository guardrails.

The reviewer sample lives at:

`docs/issue19-reviewer-trace-sample.md`

## Unblock condition

The only action needed to complete this acceptance is to supply or retain one real
multi-topic worksheet/question set. At that point the implementation should:

1. preserve the worksheet/question identifiers;
2. map every selected question to one primary and only meaningful secondary
   capabilities;
3. compute prerequisite closure from the canonical graph;
4. trace the primary/secondary capabilities to existing teaching microtopics/rungs;
5. report any genuinely unmapped demand as a gap rather than creating a capability for
   audit cosmetics;
6. add the resulting manual trace to this document or a worksheet-specific companion
   report.

Until such an input exists, this criterion remains deliberately open.
