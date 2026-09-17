# Physics Convention Authority Decision — Analysis Pass

**Repository:** `reallaksh19/Grade9V3`  
**Dispatch base:** `a014740632a4305dcd1b7546b2b7036921f1b50b`  
**Branch:** `physics-convention-authority-analysis`  
**Mode:** analysis / decision artifact only — no production library mutation  
**Scope:** `BUCKET-VECTOR-REPRESENTATION` and `BUCKET-RELATIVE-MOTION`

---

## 1. Decision question

Resolve the current `CONVENTION_GAP` without promoting local examples into bucket-wide truth.

The repository schema gives `bucket.conventions[]` one narrow job: hold whatever must be fixed before the bucket's quantities can be read. Core1 and Core1A both require that field, and Core1A requires declared conventions before any dependent quantity is used.

This analysis therefore separates three different kinds of statement:

```yaml
convention_authority:
  bucket_invariants:
    # Stable interpretive rules that apply throughout the bucket.

  declaration_obligations:
    # Information that must be declared in each instance before quantities are read.

  instance_choices:
    # Choices an author or learner may make locally and which must not be frozen globally.
```

It also separates conventions from model/validity conditions. A statement can be required for a relation to be valid without being a convention.

---

## 2. Authority hierarchy used

This pass uses only the frozen repository state at the dispatch base.

Highest relevant structural authority:

- `Shared/library/package.schema.json`
- `Shared/roles/CORE1.md`
- `Shared/roles/CORE1A.md`

Physics semantic authority used for candidate convention wording:

- `Physics/gates/motion-vectors.v1.json` (`maturity: ENGINEERING`, author-created, no independent scientific/pedagogical review)
- `Physics/adapter/CoreContracts.json`

Candidate-library evidence used to test whether a statement is global or local:

- `Physics/library/vector-representation.v1.json`
- `Physics/library/relative-motion.v1.json`

The candidate libraries do not gain higher authority because they contain learner-facing examples.

---

## 3. Structural finding

`bucket.conventions[]` is optional in the package schema but required by both Core1 and Core1A role contracts.

The schema defines each convention as exactly:

```yaml
- id:
  statement:
```

and describes the collection as the material that must be fixed before bucket quantities can be read.

Therefore the current absence of `bucket.conventions[]` is a real role-contract gap, not merely documentation debt.

However, the field must not be used as a dumping ground for every relation condition, model regime, unit, or representation constraint already housed elsewhere.

---

## 4. Vector Foundation — authority analysis

Target bucket:

`BUCKET-VECTOR-REPRESENTATION`

### 4.1 What the engineering gates establish

The gates repeatedly establish all of the following:

1. A signed component has meaning only relative to a declared positive axis direction.
2. The positive direction of each axis is a free declaration, not a property of the physical situation.
3. Once an axis direction is declared, it fixes the sign of components measured along that axis.
4. Vectors compared or combined by the authored relations must be expressed in the same declared frame / axes and compatible units.
5. The repository explicitly rejects the idea that one axis convention is physically correct while another is wrong.

### 4.2 What the candidate library establishes

The library repeatedly uses local examples such as:

- east-positive x / north-positive y,
- later reversal of x to west-positive,
- common east/north scenes for subtraction.

The question-family contract explicitly says the axis convention is initially stated and later may be inferred or chosen by the learner. It also permits changing the axis convention within declared assumptions.

Therefore `east-positive x / north-positive y` is an **instance choice**, not a bucket invariant.

### 4.3 Proposed convention set

**DECISION: recommend two bucket conventions for integration.**

```yaml
conventions:
  - id: CONV-VEC-AXIS-DECLARATION
    statement: >
      Before any signed component is read, the frame and the positive direction
      of each axis for that instance are declared. Component signs are read
      relative to those declared positive directions.

  - id: CONV-VEC-COMMON-COMPONENT-BASIS
    statement: >
      Vectors whose components are compared, added, or subtracted within one
      instance are interpreted in the same declared axes and compatible units.
```

### 4.4 Why these are bucket conventions

`CONV-VEC-AXIS-DECLARATION` fixes the sign-reading rule while preserving the gate's explicit freedom to choose the positive directions locally.

`CONV-VEC-COMMON-COMPONENT-BASIS` fixes the common interpretive basis required before a component comparison or subtraction is meaningful. It does not choose a compass orientation.

### 4.5 Statements that must NOT be promoted into the bucket conventions

Do not add any of the following as global conventions:

- `+x = east`
- `+y = north`
- "forward is positive"
- a fixed compass direction for either axis
- one axis convention is preferred or physically correct

These contradict or over-constrain `PHY-VEC-AXIS-CONVENTION`, which explicitly treats positive direction as a free declaration.

### 4.6 Statements that stay outside `bucket.conventions[]`

Keep these in their current semantic homes:

- axes perpendicular for the magnitude relation → relation condition
- axes parallel / non-rotating for subtraction construction → relation / gate validity condition
- classical / non-relativistic regime → model validity / package extension
- equal coordinate scale → representation requirement
- exact unit such as `m/s` → symbol/datum/representation unit fields
- zero vector has no assigned direction → representation / relation boundary condition

Reason: these are not arbitrary interpretive conventions that must be declared before every quantity is read. They are model, relation, representation, or unit constraints with existing homes.

---

## 5. Relative Motion — authority analysis

Target bucket:

`BUCKET-RELATIVE-MOTION`

### 5.1 What the engineering gates and library establish

The repository consistently establishes:

1. Source positions / velocities are expressed in a named common frame.
2. Signed components require declared axis directions exactly as in the vector-foundation prerequisite.
3. `A/B` means the quantity of A relative to B; B is the reference / observer and the subtraction order is A minus B.
4. Swapping the order changes the relative vector's direction / sign.
5. Same-instant positions, one common interval, parallel non-rotating axes, and classical-speed assumptions are validity conditions for the specific relations.

Local examples frequently use east/north axes, but the gates do not make east/north globally mandatory.

### 5.2 Proposed convention set

**DECISION: recommend two bucket conventions for integration.**

```yaml
conventions:
  - id: CONV-REL-COMMON-FRAME-DECLARATION
    statement: >
      Before relative position or relative velocity components are read, the
      common frame and the positive direction of each axis for that instance
      are declared; all compared source quantities use that same declared
      component basis.

  - id: CONV-REL-OBSERVER-ORDER
    statement: >
      The notation A/B means "A relative to B": B is the reference or observer,
      and the ordered relative quantity is formed from A minus B. Reversing the
      order names the opposite relative vector.
```

### 5.3 Why observer order is a convention

`A/B` is notation whose interpretation must be fixed before the learner can read `r_A/B` or `v_A/B` correctly. The underlying subtraction relation is scientific content; the slash notation and which object is named as reference are an interpretive convention layered on top of that relation.

The convention therefore states the notation/order rule but does not replace the relation definitions or their derivations.

### 5.4 Statements that must NOT be promoted into the bucket conventions

Do not add:

- `+x = east`
- `+y = north`
- a fixed compass orientation
- "B is always the observer" without the `A/B` qualifier
- "subtract the second thing written in the prose question" as a rule

The observer/reference is determined by the ordered notation / quantity being asked for, not by prose position.

### 5.5 Statements that stay outside `bucket.conventions[]`

Keep these as relation/model conditions:

- positions must be evaluated at the same instant
- relative-velocity derivation uses one shared non-zero interval
- axes must be parallel and non-rotating for the simple model
- finite-interval average is not automatically instantaneous velocity
- classical / non-relativistic model
- rotating-frame cases require additional treatment

These statements govern whether a relation is valid. They are not arbitrary declarations whose value can be chosen locally.

---

## 6. Cross-bucket relationship

`BUCKET-RELATIVE-MOTION` depends on `BUCKET-VECTOR-REPRESENTATION`, but the current package schema has no convention-reference mechanism.

Therefore the Relative Motion bucket cannot rely on an implicit inheritance that the library cannot represent.

The recommended integration duplicates the minimal axis/frame declaration obligation in the Relative Motion bucket while keeping the semantics consistent with the vector-foundation convention.

This is intentional duplication of a role-required declaration, not duplication of scientific relations.

A future schema may support convention references or inherited bucket contracts, but introducing that mechanism is outside this task.

---

## 7. Unit decision

**DECISION: do not create a bucket convention that globally fixes `m/s`.**

Rationale:

- units already have explicit structured homes in Physics symbol records, data atoms, validators, and representation scenes;
- the convention schema is for what must be fixed before quantities can be read, not for duplicating every unit declaration;
- the authored examples currently use `m/s`, but promoting that example pattern into a separate convention adds redundant authority and creates drift risk.

The existing Core1 requirement that units be visible remains satisfied by the existing unit-bearing fields when Core1 is compiled.

---

## 8. Model-regime decision

Both candidate packages carry:

`physics:model_regime: CLASSICAL_PARALLEL_NONROTATING_AXES`

**DECISION: do not copy this string into `bucket.conventions[]`.**

Its components are already expressed as relation/gate validity conditions. Treating model regime as a convention would blur two categories:

- a convention is something declared so a quantity can be interpreted;
- a validity condition is something that must be true for a relation/model to apply.

The distinction should remain explicit.

---

## 9. Proposed integration patch shape

No production patch is made in this analysis branch.

If approved, the authority integration patch should add only `conventions` arrays to the two bucket objects, using the exact candidate wording below unless review changes it.

### `BUCKET-VECTOR-REPRESENTATION`

```json
"conventions": [
  {
    "id": "CONV-VEC-AXIS-DECLARATION",
    "statement": "Before any signed component is read, the frame and the positive direction of each axis for that instance are declared. Component signs are read relative to those declared positive directions."
  },
  {
    "id": "CONV-VEC-COMMON-COMPONENT-BASIS",
    "statement": "Vectors whose components are compared, added, or subtracted within one instance are interpreted in the same declared axes and compatible units."
  }
]
```

### `BUCKET-RELATIVE-MOTION`

```json
"conventions": [
  {
    "id": "CONV-REL-COMMON-FRAME-DECLARATION",
    "statement": "Before relative position or relative velocity components are read, the common frame and the positive direction of each axis for that instance are declared; all compared source quantities use that same declared component basis."
  },
  {
    "id": "CONV-REL-OBSERVER-ORDER",
    "statement": "The notation A/B means 'A relative to B': B is the reference or observer, and the ordered relative quantity is formed from A minus B. Reversing the order names the opposite relative vector."
  }
]
```

---

## 10. Falsifiers before integration

Reject or revise this decision if any of the following is shown from repository evidence:

1. A bucket convention fixes east/north globally despite the axis gate declaring positive direction a free choice.
2. A convention duplicates a relation condition such as same-time, common-interval, or non-rotating-axis validity merely to fill the field.
3. The observer-order wording conflicts with any existing `r_A/B` or `v_A/B` relation meaning.
4. A convention makes a local scene's coordinate choice normative for every instance.
5. The integration changes any relation, representation, capability, data atom, microtopic, elicitation, question family, curriculum mapping, or provider-review status.
6. Adding the conventions is described as independent scientific review or curriculum acceptance.
7. Core1/Core1A are called globally complete solely because `CONVENTION_GAP` is resolved; other known gaps must remain independently visible.

---

## 11. Authority status of this decision

```yaml
decision_status: READY_FOR_REVIEW
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