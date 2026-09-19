# Graphical Cognitive Deconstruction Route (GCDR) — Blueprint v1.0

## Status

This is a **parallel support-route contract**, not a second curriculum taxonomy.

Canonical authority remains:

```text
capability → matrix rung → microtopic → teaching_path semantic leaf
                                      │
                                      ├─ normal route
                                      └─ GCDR activity
```

A GCDR activity must return evidence to the same semantic leaf/capability it supports.

## When to recommend the route

Recommend a GCDR when the concept itself is intrinsically difficult — counterintuitive, hidden-mechanism, relational, constraint-based, multi-representation, reference-frame/system-boundary sensitive — **or** when learner evidence shows very low knowledge, a persistent misconception, repeated failure, failure after normal repair, or failed reconstruction.

Do not auto-route from one wrong answer. Missing prerequisites divert to prerequisite recovery first.

## One explorer, one cognitive target

Every explorer declares:

- **target failure** — the learner model being replaced;
- **target operation** — the reasoning operation the learner must acquire;
- **core invariant** — what survives valid variation;
- **boundary** — where the invariant/shortcut stops applying.

Do not combine several hard concepts simply because they share a chapter.

## Mandatory cognitive sequence

```text
CONTEXT
  ↓
PREDICT
  ↓
MANIPULATE
  ↓
OBSERVE
  ↓
CONTRADICT
  ↓
GRAPHICAL DECONSTRUCTION
  ↓
MATHEMATICAL RECONSTRUCTION
  ↓
INVARIANT DISCOVERY
  ↓
BOUNDARY STRESS
  ↓
SCAFFOLD FADE
  ↓
FRESH TRANSFER
```

The final equation is a compression of the visible mechanism, not the opening move.

## Three graphical depths

### G1 — Phenomenon
Show what physically happens: objects, motion, contacts, geometry, trajectory, reference frame, or system boundary.

### G2 — Mechanism
Expose what is normally invisible: force/velocity components, relative motion, rope segments, event markers, constraints, interaction pairs, system boundaries, or causal dependencies.

### G3 — Mathematical structure
Convert the mechanism into signed quantities, equations, a derived relation, and the invariant.

## Coordinated representations

Use multiple views only when they perform different reasoning jobs. A typical ensemble is:

```text
physical scene
    ├─ vector/FBD view
    ├─ graph
    ├─ state table
    └─ equation
```

All views must share one underlying state. A view may not silently use a different time, frame, sign convention, or system boundary.

## Counterfactual requirement

Where useful, let the learner impose the tempting wrong model and observe the contradiction.

Examples:

- force `T = mg` and see that the predicted acceleration becomes zero;
- force `Δy = 0` and see that it solves a real but wrong event;
- remove ground friction and see that internal horse–cart forces cannot accelerate the combined centre of mass.

Feedback must answer both **why the correct model works** and **why the tempting model cannot**.

## Progressive disclosure

Learner mode should not expose the invariant, full derivation, all overlays, and diagnostic answer before prediction.

Preferred reveal order:

```text
physical scene → prediction → relevant overlay → causal relation
→ equation → invariant → boundary
```

A teacher/debug mode may expose all layers simultaneously.

## Scaffold fading

Full graphical success is not mastery.

```text
full labels/values/hints
  ↓
partial labels
  ↓
learner supplies signs/relations
  ↓
physical scene only
  ↓
fresh task without explorer
```

## 3-Audit Universal Quality Gate

### Audit 1 — Canonical Truth & Scope
Before implementation, verify:

- exact capability and semantic leaf;
- assumptions and sign/frame/system conventions;
- primitive vs derived quantities;
- hold/vary/notice structure;
- invariant and conditional claims;
- boundary/limit cases;
- prerequisites.

No visual may be more authoritative than the canonical academic records.

### Audit 2 — Graphical Cognitive Deconstruction
This is the hardest gate.

Ask:

- What is invisible in the ordinary explanation?
- What can the learner manipulate?
- Which prediction must be elicited before reveal?
- What observation contradicts the wrong model?
- Which mechanism must become visible?
- Which representations must remain synchronized?
- How does the equation emerge from the visual mechanism?
- Which boundary case breaks an overgeneralized shortcut?

**Fail Audit 2** if a paragraph + equation + decorative animation would provide essentially the same learning experience.

### Audit 3 — Reconstruction & Transfer
The learner must demonstrate:

1. canonical reconstruction;
2. representation transfer;
3. boundary recognition;
4. fresh transfer without the explorer.

A multiple-choice score alone is insufficient exit evidence.

## Entry and exit contracts

Every GCDR activity is machine-bound through `resource.extensions.topic_atlas.gcdr_contract`.

The contract declares route triggers, cognitive target, interaction sequence, graphical mechanism, boundary stress, and exit evidence.

Conformance states:

- `DESIGN_BOUND` — blueprint metadata exists;
- `IMPLEMENTATION_PARTIAL` — some required interaction behaviours exist, but not all;
- `CERTIFIED` — every implementation-evidence flag is true and CI validates structural/referential integrity.

`CERTIFIED` does **not** imply human scientific or pedagogical approval; those remain separate review authorities.

## Minimum Definition of Done for certification

- prediction occurs before answer reveal;
- meaningful direct manipulation exists;
- at least two synchronized representations add distinct reasoning value;
- the wrong model produces an observable contradiction;
- a causal chain is explicit;
- mathematics is reconstructed from the visual mechanism;
- the learner discovers/tests an invariant;
- a boundary case breaks a shortcut;
- scaffolds fade;
- fresh transfer succeeds without the explorer;
- the exit rejoins the same semantic leaf.

## Reference implementation lessons

The pulley explorer is a useful benchmark because it coordinates a physical rig, manipulable parameters, prediction, rope-geometry accounting, FBDs, dynamic/static comparison, and diagnostic checks. The reusable principle is not its exact layout; it is the sequence **predict → manipulate → reveal mechanism → reconstruct → stress boundary → verify transfer**.

The blueprint deliberately improves on reference-dashboard behaviour by preventing answer leakage before prediction and by requiring scaffold fade plus fresh transfer before certification.
