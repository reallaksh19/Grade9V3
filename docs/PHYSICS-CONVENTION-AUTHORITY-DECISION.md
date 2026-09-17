# Physics Convention Authority Decision — Analysis Pass

**Repository:** `reallaksh19/Grade9V3`  
**Dispatch base:** `a014740632a4305dcd1b7546b2b7036921f1b50b`  
**Branch:** `physics-convention-authority-analysis`  
**Mode:** analysis / decision artifact only — no production library mutation  
**Scope:** `BUCKET-VECTOR-REPRESENTATION` and `BUCKET-RELATIVE-MOTION`

---

## 1. Decision question

Resolve the current `CONVENTION_GAP` without promoting local examples into bucket-wide truth.

The package schema gives `bucket.conventions[]` a narrow role: it holds what must be fixed before a bucket's quantities can be read. Core1 and Core1A both require that field, and Core1A requires conventions to be declared before dependent quantities are used.

This analysis distinguishes:

```yaml
convention_authority:
  bucket_invariants:
    # Stable interpretive rules that apply throughout the bucket.

  declaration_obligations:
    # Information that must be declared in each instance before quantities are read.

  instance_choices:
    # Choices an author or learner may make locally and which must not be frozen globally.
```

A convention is also kept distinct from a model or relation validity condition. Something may have to be true for a relation to apply without being a convention.

---

## 2. Authority hierarchy

This pass uses only the frozen repository state at the dispatch base.

Structural authority:

- `Shared/library/package.schema.json`
- `Shared/roles/CORE1.md`
- `Shared/roles/CORE1A.md`

Physics semantic authority:

- `Physics/gates/motion-vectors.v1.json`
- `Physics/adapter/CoreContracts.json`

Candidate-library evidence used to distinguish bucket-wide truth from local examples:

- `Physics/library/vector-representation.v1.json`
- `Physics/library/relative-motion.v1.json`

The engineering gates remain author-created and not independently scientifically or pedagogically reviewed. This decision does not change that status.

---

## 3. Structural finding

`bucket.conventions[]` is optional in the package schema but required by the Core1 and Core1A role contracts.

Each convention has exactly:

```yaml
- id:
  statement:
```

The schema describes the collection as what must be fixed before the bucket's quantities can be read.

Therefore the missing field is a real role-contract gap. However, it must not become a duplicate home for relation conditions, representation constraints, units, or model assumptions that already have explicit fields elsewhere.

---

## 4. `BUCKET-VECTOR-REPRESENTATION`

### 4.1 Source-backed authority

The engineering gates establish:

- a signed component has meaning only relative to a declared positive axis direction;
- the positive direction of an axis is a free declaration, not a property of the physical situation;
- once declared, the axis direction fixes the component sign;
- one convention is not physically privileged over another;
- operations on components require a shared declared component basis.

The candidate library repeatedly uses east-positive x / north-positive y as a local worked convention, and then deliberately reverses the x convention in `MIC-SIGNED-COMPONENT`. The question-family contract also permits the axis convention to be changed or later chosen by the learner.

Therefore east/north is local instance data, not bucket authority.

### 4.2 Final convention recommendation

**Decision: recommend one convention item for this bucket.**

```yaml
conventions:
  - id: CONV-VEC-AXIS-DECLARATION
    statement: >
      Before any signed component is read, the frame and the positive direction
      of each axis for that instance are declared. Every signed component used
      together in that instance is interpreted in that declared component basis.
```

This fixes the sign-reading rule and common component basis while preserving the source-backed freedom to choose the actual positive directions locally.

### 4.3 Do not promote these local choices

Do **not** add any of the following as bucket conventions:

- `+x = east`
- `+y = north`
- "forward is positive"
- one fixed compass orientation
- any claim that one axis convention is physically correct

These would contradict the gate `PHY-VEC-AXIS-CONVENTION`.

### 4.4 Keep these outside `bucket.conventions[]`

Retain the following in their current semantic homes:

- perpendicular axes for the magnitude relation → relation condition;
- parallel / non-rotating axes for the subtraction construction → relation or gate validity condition;
- classical / non-relativistic regime → model validity / package extension;
- equal coordinate scale → representation requirement;
- `m/s` and other units → symbol, datum, validator, and representation unit fields;
- zero-vector direction boundary → representation / relation boundary condition.

These are not free declarations whose values are chosen per instance.

---

## 5. `BUCKET-RELATIVE-MOTION`

### 5.1 Source-backed authority

The gates and candidate library consistently establish:

- source positions and velocities are interpreted in one named common frame;
- positive axis directions must be declared before signed components are interpreted;
- the ordered notation `A/B` means the quantity of A relative to B;
- B is the reference / observer in `A/B`, so the ordered quantity is formed from A minus B;
- reversing the order names the opposite relative vector.

They also establish several validity conditions: same-time positions, a shared interval for the finite-interval derivation, parallel non-rotating axes, and classical-speed assumptions.

Those validity conditions are not conventions.

### 5.2 Final convention recommendation

**Decision: recommend two convention items for this bucket.**

```yaml
conventions:
  - id: CONV-REL-COMMON-FRAME-DECLARATION
    statement: >
      Before relative position or relative velocity components are read, one
      common frame and the positive direction of each axis for that instance are
      declared. All source quantities compared in that instance are interpreted
      in that same declared component basis.

  - id: CONV-REL-OBSERVER-ORDER
    statement: >
      The notation A/B means "A relative to B": B is the reference or observer,
      and the ordered relative quantity is formed from A minus B. Reversing the
      order names the opposite relative vector.
```

### 5.3 Why observer order belongs here

The subtraction relation is scientific content. The slash notation and which object the notation identifies as reference are interpretive rules required before `r_A/B` or `v_A/B` can be read correctly.

The convention therefore fixes notation/order semantics without replacing the relation definitions or their derivations.

### 5.4 Do not promote these local choices

Do **not** add:

- `+x = east`
- `+y = north`
- a fixed compass orientation
- "B is always the observer" without the `A/B` qualifier
- "subtract the second thing written in the prose question"

The reference object follows the ordered quantity, not prose position.

### 5.5 Keep these as validity/model conditions

Do not move these into `bucket.conventions[]`:

- positions must be evaluated at the same instant;
- the finite-interval derivation uses one shared non-zero interval;
- axes must be parallel and non-rotating for the simple relative-motion model;
- a finite-interval average is not automatically instantaneous velocity;
- the model is classical / non-relativistic;
- rotating frames require additional treatment.

These determine when the relation is valid, not how an arbitrary sign/reference choice is declared.

---

## 6. Cross-bucket relationship

`BUCKET-RELATIVE-MOTION` depends on `BUCKET-VECTOR-REPRESENTATION`, but the current package schema has no convention-reference or inheritance field.

Therefore Relative Motion cannot rely on invisible inheritance for a role-required declaration. The recommended Relative Motion convention repeats the minimal frame/axis declaration obligation explicitly.

This is deliberate duplication of a learner-facing declaration requirement, not duplication of the underlying scientific relations.

A future convention-reference mechanism may remove that duplication, but introducing such a schema feature is outside this task.

---

## 7. Unit decision

**Decision: do not create a bucket convention fixing `m/s`.**

Units already have structured homes in symbol records, data atoms, validators, and representation scenes. Adding `m/s` again under bucket conventions would create redundant authority and drift risk.

Core1's unit requirement remains satisfied through those unit-bearing fields.

---

## 8. Model-regime decision

Both candidate packages carry:

`physics:model_regime: CLASSICAL_PARALLEL_NONROTATING_AXES`

**Decision: do not copy this into `bucket.conventions[]`.**

A convention is declared so a quantity can be interpreted. A model/validity condition must be true for a relation to apply. The repository should keep those concepts distinct.

---

## 9. Integration patch shape

No production mutation is made on this analysis branch.

If approved, the integration patch should add only the following `conventions` arrays to the two bucket records.

### Vector Foundation

```json
"conventions": [
  {
    "id": "CONV-VEC-AXIS-DECLARATION",
    "statement": "Before any signed component is read, the frame and the positive direction of each axis for that instance are declared. Every signed component used together in that instance is interpreted in that declared component basis."
  }
]
```

### Relative Motion

```json
"conventions": [
  {
    "id": "CONV-REL-COMMON-FRAME-DECLARATION",
    "statement": "Before relative position or relative velocity components are read, one common frame and the positive direction of each axis for that instance are declared. All source quantities compared in that instance are interpreted in that same declared component basis."
  },
  {
    "id": "CONV-REL-OBSERVER-ORDER",
    "statement": "The notation A/B means 'A relative to B': B is the reference or observer, and the ordered relative quantity is formed from A minus B. Reversing the order names the opposite relative vector."
  }
]
```

No other library field should change in the convention integration patch.

---

## 10. Falsifiers before integration

Reject or revise this decision if any of the following is shown from repository evidence:

1. A proposed convention fixes east/north globally despite the axis gate declaring positive direction a free choice.
2. A convention duplicates same-time, common-interval, non-rotating-axis, or other model validity conditions merely to fill the field.
3. The observer-order wording conflicts with an existing `r_A/B` or `v_A/B` meaning.
4. A local representation scene is treated as global bucket authority.
5. The integration changes a relation, representation, capability, datum, microtopic, elicitation, question family, curriculum mapping, or provider-review status.
6. Adding conventions is described as independent scientific review or curriculum acceptance.
7. Core1/Core1A are called globally complete solely because `CONVENTION_GAP` is resolved; every other known gap must remain independently visible.

---

## 11. Decision status

```yaml
decision_status: READY_FOR_INTEGRATION_REVIEW
source_basis:
  structural:
    - Shared/library/package.schema.json
    - Shared/roles/CORE1.md
    - Shared/roles/CORE1A.md
  physics_semantics:
    - Physics/gates/motion-vectors.v1.json
    - Physics/adapter/CoreContracts.json
  candidate_examples:
    - Physics/library/vector-representation.v1.json
    - Physics/library/relative-motion.v1.json

scientific_review_status: UNCHANGED
curriculum_authority_status: UNCHANGED
representation_divergence_status: UNCHANGED
oracle_data_status: UNCHANGED
mathematics_provider_status: UNCHANGED
```

If approved and integrated, this resolves the **structural candidate-library `CONVENTION_GAP`** for these two buckets only. It does not promote either bucket beyond its existing candidate/review authority.