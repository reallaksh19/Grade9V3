# Core2B — supported application and transfer

Read [the shared role invariants](README.md) first.

## Purpose

Assess whether the learner can carry the bucket's reasoning into a situation that demands a decision they have not been handed — a different model, a different representation, a different context, or a higher reasoning load.

## What makes a Core2B task

A task belongs here only if it changes a **specified** dimension of demand relative to prior exposure. State which one:

| Dimension | The learner must now |
|---|---|
| Model choice | Decide which relation or model applies, rather than being told |
| Representation | Choose or translate the representation before calculating |
| Context | Map an unfamiliar situation onto a known structure |
| Reasoning load | Chain steps that were previously separated |

**A cover story is not a dimension.** The same question with different numbers, or the same structure with a different object in it, is same-family practice and belongs in Core2A. Declaring it `NEW_TRANSFER` does not make it transfer; the exposure audit exists precisely to dispute that claim, and a flagged pair is resolved by a reviewer, not by the author's own label.

## Required content

- **Graduated help** that supports without collapsing the demand — help that hands over the model choice defeats the task.
- **Full answer and rubric**, including what a good justification contains, not only the final result.
- **A repair route** for the predictable failure, pointing back to the specific Core1A/Core1B construction that addresses it.
- **An explicit statement of the changed demand** relative to prior exposure, so the reviewer can check the transfer claim.
- **Exposure lineage**: what the learner has already seen that this builds on.

## Practice routing

Same inputs as [Core2A](CORE2A.md) — scoped capability evidence or an explicit owner waiver — with the same prohibitions on manufactured diagnosis. Transfer tasks in particular must not be routed to a learner on the assumption that a high aggregate estimate implies the prerequisites are in place.

## What Core2B must not do

- Introduce new scientific content under a transfer label. A task requiring a model the learner was never taught is a coverage gap, not a transfer assessment.
- Depend on a live tutor for closure.
- Treat low measured similarity as evidence of genuine transfer. Similarity is a screening signal; transfer is a claim about demand, and it is established by review.

## What this role requires the library to hold

The prose above is the authority for *meaning*. The block below is the authority for
*presence*: every path in it must resolve to a field the package schema can hold. It
cannot check the reverse — that everything the prose requires appears in the block.

```requires
question.transfer.dimension              state which dimension of demand changes
question.transfer.statement              an explicit statement of the changed demand
question.transfer.builds_on[]            exposure lineage: what the learner has already seen
question.hints[]                         graduated help that supports without collapsing the demand
question.hints[].reveals                 help that hands over the model choice defeats the task
question.answer.summary                  full answer
question.answer.rubric[]                 and rubric
question.answer.rubric[].criterion       what a good justification contains
question.answer.rubric[].evidence_of     not only the final result
question.repair_ref                      a repair route pointing back to the Core1A/Core1B construction
question.origin                          a task requiring an untaught model is a coverage gap
```
