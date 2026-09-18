# Question → Study Map Benchmark

This benchmark suite measures whether the repository can turn mapped questions into a useful, honest, learner-facing study plan.

It is a **benchmark, not a UI template**. A result may be rendered as a table, cards, Markdown or another interface. The benchmark checks semantic decisions:

```text
question demand
→ teaching destination
→ prerequisite closure
→ learner-specific action
→ unresolved gaps / source limits
→ feedback / repair / fresh verification when an attempt exists
```

The benchmark workstream is deliberately separated from repair work.

## Benchmark agent contract

The benchmark agent may:

- add benchmark fixtures, expected outcomes and observed outcomes under `benchmarks/question-study-map/`;
- use existing repository tools to evaluate current behavior;
- record failures and ambiguities in `GAPS.md`;
- add benchmark-only helper code under this benchmark directory if needed;
- cite the exact matrix/capability/question/fixture that exposed an issue.

The benchmark agent must **not**:

- edit `Shared/` runtime or schemas;
- edit `Physics/` or `Mathematics/` curriculum/content to make a case pass;
- weaken readiness or routing rules;
- canonicalize external questions;
- infer missing figures/source information;
- turn owner percentages into mastery evidence;
- redesign the architecture while benchmarking.

If the current implementation fails a benchmark, record the failure. Do not fix it.

## Scope

Benchmark every currently mapped subtopic/matrix in the self-study v1 candidate.

Physics:

- Current electricity, Ohm's law and circuit analysis
- Fluid statics, buoyancy and Bernoulli flow
- Universal gravitation, free fall and orbital motion
- One-dimensional motion
- Magnetic fields, Lorentz force and electromagnetic induction
- Newton's first law and free-body diagrams
- Reflection and spherical mirrors
- Oscillations, simple harmonic motion and waves
- Rotational dynamics, angular momentum and rolling
- Simple machines
- Sound / propagation / wave quantities / reflection
- Thermodynamics and heat engines
- Vector addition, subtraction and orientation
- Work, energy and power
- Relative motion
- Vector representation and subtraction

Mathematics:

- One-unknown linear equations over the rationals

This scope is a snapshot of the current candidate. New matrices added later should receive a new benchmark pack rather than silently changing historical results.

## Per-subtopic benchmark pack

Each mapped subtopic should receive a directory:

```text
benchmarks/question-study-map/cases/<subject>/<matrix-id>/
  benchmark.yaml
  expected.md
  observed.md
```

The benchmark pack should use the smallest representative cases needed to exercise the subtopic. It does not need to reproduce every canonical question.

For each subtopic, cover as many of the following cases as are genuinely applicable:

1. Direct-ready question — one clear primary capability and one unambiguous teaching destination.
2. Prerequisite route — expected order follows the capability graph, not local rung numbers.
3. Multi-capability question — primary ownership stays distinct from meaningful secondary demand.
4. Repeated demand — multiple questions reuse one capability and teaching is consolidated.
5. Unknown learner — no percentage or prior evidence means no invented mastery.
6. Rough owner estimate — estimate changes starting coordinate only; never creates DEMONSTRATED evidence.
7. Prior learner evidence — direct/diagnostic evidence overrides rough estimates where available.
8. External provider bridge — bridge remains visible; unrelated external secondary capabilities must not block repair of a clearly identified local failure.
9. Content gap — missing capability/microtopic is named rather than fabricated.
10. Incomplete source — missing figure/table/data remains unresolved.
11. Feedback diagnosis — wrong attempt identifies the first meaningful failure where evidence supports it.
12. Repair — repair targets the failed capability/misconception rather than restarting the whole topic.
13. Fresh verification — uses a fresh same-capability check and does not reuse the solved external question as proof.
14. Help-dependent success — correct after help remains UNCERTAIN rather than independent mastery.
15. Independent success — independent correct work may draft DEMONSTRATED evidence and a later review.

Not every subtopic needs every case. Record `NOT_APPLICABLE` rather than inventing an artificial scenario.

## Benchmark result model

Each case records:

```yaml
benchmark_id: QSM-...
subject: Physics
matrix_id: MATRIX-...
subtopic: ...

scenario:
  description: ...
  input_kind: canonical_question | external_question | synthetic_falsifier | learner_replay
  question_refs: [...]
  learner_context: ...

expected:
  mapping: ...
  teaching_destination: ...
  prerequisite_order: ...
  learner_action: ...
  unresolved: ...
  feedback: ...
  verification: ...

forbidden:
  - ...

observed:
  status: PASS | FAIL | PARTIAL | BLOCKED_BY_SOURCE | NOT_APPLICABLE
  summary: ...
  evidence: ...
```

The benchmark must not require exact prose or exact table layout.

## Semantic benchmark criteria

A good result must be:

- **faithful** — describes what the question actually demands;
- **specific** — more precise than a chapter/topic label;
- **actionable** — learner/parent can tell what to do next;
- **personalized** — learner evidence changes the recommendation when it should;
- **honest** — content/source gaps stay explicit;
- **efficient** — repeated demands are consolidated;
- **ordered** — prerequisites drive study order;
- **readable** — internal capability IDs are not required to understand the human-facing result.

## Pass/fail philosophy

Do not use an aggregate numerical score in v1. Use `PASS`, `FAIL`, `PARTIAL`, `BLOCKED_BY_SOURCE`, or `NOT_APPLICABLE`.

## Gap recording

Every observed benchmark failure or material ambiguity must be written to `GAPS.md`.

The benchmark agent records symptoms and evidence only. It may suggest a likely layer, but must not claim a root cause unless directly proven.

Root-cause analysis and fixes are a separate phase reserved for the maintainer after the benchmark sweep is complete. See `ANALYSIS.md`.