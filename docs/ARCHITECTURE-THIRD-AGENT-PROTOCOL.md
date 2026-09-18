# Third-agent authoring protocol

This document is the contract for an agent that enters this repository with no memory of
its implementation history. It turns a short human request into a governed plan before any
learner-facing material is authored.

The acceptance prompt is deliberately small:

```text
Create Core1, Core2, Core1A, Core1B, Core2A, Core2B.
Core2 basis: https://ncert.nic.in/textbook/pdf/keph103.pdf
Sub topic: Relative motion.
```

The architecture, not the agent's intuition, supplies everything already recorded.

## 1. Three independent readiness axes

A green schema check is not a claim that a learner can traverse the material.

- **STRUCTURE** — records, references, matrices and compiler dependencies are mechanically
  valid.
- **REACHABLE_TO_LEARN** — the declared learner state can reach the selected rung after
  prerequisite closure and any explicit bridges.
- **PRODUCT BUILDABILITY** — the library owns the assets required by the requested Core.
- **ACADEMIC_REVIEW** is reported separately. Machine checks never turn CANDIDATE content
  into reviewed physics.

The invariant exposed by the planner is:

```text
READY_TO_BUILD != REACHABLE_TO_LEARN
```

Content expansion remains blocked until structural findings are clear and the relevant
records have human review.

## 2. The capability graph is reachability authority

`ladder_position` is a curriculum coordinate. It is not evidence and it cannot contradict
the capability graph.

For every recorded rung C, every prerequisite P that is also on the same ladder must have:

```text
position(P) < position(C)
```

`Shared/tools/capability_graph.py` computes transitive prerequisite closure and
`matrix_conformance.py` enforces the order with
`LADDER_PREREQUISITE_ORDER_VIOLATION`.

A learner request for a later coordinate is checked against the same graph. Missing
same-ladder prerequisites move entry backward. Prerequisites supplied elsewhere are
returned as explicit bridges. Unknown prerequisites block execution.

A percentage therefore selects a proposed coordinate; it never proves prerequisite
mastery and never dilutes the depth of a rung.

## 3. One definition of practice ownership

Retrieval closure and question ownership are different.

`slice_for_bucket` may retrieve prerequisite capabilities because an author needs their
context. That does not make questions attached to those prerequisite capabilities the
downstream bucket's practice.

`Shared/library/practice_inventory.py` is the shared rule:

- a bucket owns capabilities taught by its own microtopics;
- a bucket owns questions whose primary capability is one of those capabilities;
- Core2A/Core2B exposure is then selected from those bucket-owned questions.

The compiler and strict request resolver both use this definition. A planted regression
proves that a question for prerequisite CAP-A cannot make a downstream CAP-B bucket
Core2A-ready.

## 4. Plan request versus execution request

There are intentionally two contracts.

### Plan-level request

`Shared/library/authoring-request.schema.json` accepts a partial human request. It may omit
learner entry and practice purposes because discovering those omissions is the planner's
job.

`Shared/tools/plan_request.py` resolves:

- subject and subtopic to a bucket;
- the canonical rung inventory;
- existence, matrix provenance, library review status and source refs on separate axes;
- prerequisite topology and learner-route requirements;
- compiler-supported products;
- bucket-owned Core2A/Core2B inventory;
- source-inspection state;
- academic-review readiness;
- owner inputs that cannot be derived;
- agent actions that must happen before the owner is asked anything else.

Planning may return WAITING states. That is not a failure.

### Execution request

`Shared/library/request.schema.json` remains strict. Execution may not guess a learner
entry or practice purpose. `resolve_request.py` additionally applies prerequisite-safe
entry and bucket-owned practice inventory before producing briefs.

`execution_handoff()` in the planner refuses execution while findings, owner inputs,
agent actions, non-ready products, or human academic review remain unresolved.

Rule:

```text
Planning may wait; execution may not guess.
```

## 5. What an agent derives and what the owner decides

The agent must derive, without asking the owner:

- bucket and canonical ladder;
- capability and prerequisite topology;
- rung existence;
- inferential jumps, misconceptions and exits already owned by records;
- vocabulary ceilings and controlled variation already owned by matrices;
- role contracts;
- current question inventory and practice exposure;
- current source custody and compiler support;
- Core relationships and blockers.

Normal owner inputs are limited to decisions that are not repository facts:

1. learner entry evidence: a profile/diagnostic, an explicit owner entry, an owner estimate,
   or an explicit unknown/waiver;
2. Core2A purpose: STARTER, PRACTICE, REVISION or COMPETITION;
3. Core2B purpose: PRACTICE, REVISION, COMPETITION or NONE;
4. only **after** supplied source inspection reports insufficient coverage: whether
   project-authored candidate questions may fill the gap.

The agent does not ask item 4 before inspecting the source.

## 6. The six Core semantics

The existing role specifications remain product authority. The orchestration contract makes
their relationship explicit:

| Core | Architectural role |
|---|---|
| Core1 | Canonical conceptual orientation/map for the selected capability family. |
| Core1A | Teacher-supported reveal/traversal of the selected canonical rung segment. |
| Core1B | Learner elicitation/reconstruction of the **same** canonical rung segment. Agency changes; the target does not. |
| Core2 | Source/question custody and canonical problem representation. |
| Core2A | Practice inside the taught capability family. Support may change; the conceptual target does not. |
| Core2B | Transfer: the decision structure changes and the learner must supply more of the model/representation/strategy. It is not Core2A with fewer hints. |

The strict resolver computes one teaching segment and projects Core1/Core1A/Core1B from that
selection; it does not independently choose different ladders for A and B.

## 7. Source basis and custody

A URL in a prompt is a request to inspect a source, not authority to claim everything in it
supports every requested product.

When a source basis is present but has not been inspected, the planner returns the agent
action `INSPECT_AND_INGEST_SOURCE_BASIS`. The agent must inspect and register coverage
before execution.

If inspection is sufficient, no supplemental-policy question is needed. If inspection is
insufficient, and only then, the planner asks for
`SUPPLEMENTAL_QUESTION_POLICY = SOURCE_ONLY | ALLOW_AUTHORED_CANDIDATES`.

Source identity, existence and review are deliberately separate:

- **existence** — whether a library record exists;
- **matrix_provenance** — how the matrix describes that row;
- **source_refs** — what the library record cites;
- **library_record_status** — CANDIDATE/REVIEWED state.

No one field is allowed to imply the others.

## 8. Academic readiness is not engineering readiness

`Shared/tools/academic_readiness.py` checks only mechanical preconditions for review:

- entry assumptions exist;
- the inferential jump exists;
- a misconception diagnostic exists;
- an observable exit exists;
- the rung has a vocabulary ceiling;
- the rung has controlled variation.

It explicitly does **not** decide whether the science is true or the explanation teaches
well. Human review status is reported separately and learner release requires both
mechanical reviewability and REVIEWED records.

CI runs the report but does not manufacture human approval.

## 9. Relative Motion is the golden path

`Requests/relative-motion-six-core.plan-request.json` is the cold-agent acceptance fixture.

From only subject, subtopic, six requested products and the NCERT source URL, the planner
must:

1. resolve `BUCKET-RELATIVE-MOTION`;
2. expose the canonical rung chain and provenance axes;
3. validate prerequisite topology;
4. report compiler/library product support;
5. report source inspection as an agent action;
6. ask only for learner entry, Core2A purpose and Core2B purpose;
7. not ask whether authored supplements are allowed before source inspection;
8. author no learner-facing content;
9. keep execution and content expansion blocked while unresolved decisions/review remain.

The executable regression is in `tests/test_architecture.py`.

## 10. The twelve-phase implementation map

1. **Freeze baseline** — this branch starts from PR #1 head; readiness axes are explicit.
2. **Capability graph authority** — transitive topology and matrix-order gate.
3. **Evidence-safe learner entry** — coordinate requests backtrack/bridge prerequisites.
4. **Unified practice ownership** — one bucket-owned question inventory.
5. **Third-agent API** — partial plan request schema and resolver.
6. **Minimal owner questions** — `required_owner_inputs` contains only non-derivable choices.
7. **Plan before execute** — WAITING is legal in planning; execution handoff fails closed.
8. **Core semantics** — six roles and A/B relationships are explicit and tested.
9. **Provenance separation** — existence, matrix provenance, source refs and review status are separate.
10. **Academic-review boundary** — mechanical reviewability is reported separately from human approval.
11. **Golden-path integration** — Relative Motion three-line prompt is an executable fixture.
12. **Controlled expansion** — `CONTENT_EXPANSION` remains BLOCKED until the earlier gates and human review permit it. The architecture does not add new curriculum merely to declare this phase complete.

## 11. What completion means

A third agent succeeds when it can enter the repository without prior conversation history,
run the plan request, and know:

- what the repository already owns;
- which six products are currently buildable;
- what must happen before source-backed practice can be claimed;
- where the learner can legally enter;
- exactly which decisions require the owner;
- why execution or expansion is blocked.

That is the boundary between a reusable architecture and an agent remembering the method.
