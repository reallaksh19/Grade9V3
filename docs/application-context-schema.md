# Application context schema boundary

The library now has a first-class way to say **where an existing capability is being used**
without pretending that the story setting is itself a new capability.

This distinction exists to prevent capability proliferation such as creating a new mastery id
for every familiar application setting.

## Three different things

```text
capability
    what the learner can do

question family
    the stable demand/solution structure being exercised

application context
    the situation in which that demand is presented
```

Only capabilities participate in learner mastery state and prerequisite closure.

Question families and questions may reference one or more application contexts through
`context_refs`.

## Schema

A package may declare:

```json
{
  "application_contexts": [
    {
      "id": "CTX-...",
      "version": "0.1.0",
      "status": "CANDIDATE",
      "source_refs": [],
      "evidence_refs": [],
      "extensions": {},
      "title": "...",
      "description": "...",
      "invariants": [],
      "variation_dimensions": [
        {
          "name": "...",
          "description": "..."
        }
      ],
      "task_objectives": [],
      "scope_limits": []
    }
  ]
}
```

`question_family.context_refs` and `question.context_refs` point to those records.

The new collection is optional so existing canonical packages do not need cosmetic edits.

## Hard boundary

An application context may **not** appear in any `prerequisite_refs`.

The resolver fails with:

```text
APPLICATION_CONTEXT_USED_AS_PREREQUISITE
```

if a context is inserted into prerequisite topology.

That rule is structural, not subject-specific.

## When a new capability is justified

A context change alone does not justify a capability.

A new capability is justified only when the learner must perform a reusable action or make a
reusable distinction with its own success criterion and evidence state.

Examples of evidence that may justify a new capability later:

- two questions share a failure that cannot be diagnosed by the existing capability set;
- the repair required for that failure is reusable across more than one surface context;
- learner evidence needs to distinguish possession of that skill from possession of the
  underlying capability.

Until then, keep the application as a context/question-family variation.

## Routing consequence

The routing graph remains:

```text
question
→ capability demand
→ prerequisite capability closure
→ teaching / bridge resolution
```

Context metadata may help select or explain questions, but it never inserts a node into that
graph and never creates learner state.

This keeps canonical skill truth separate from the situations used to exercise it.
