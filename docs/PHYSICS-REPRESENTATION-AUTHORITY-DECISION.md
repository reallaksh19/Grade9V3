# Physics Representation Authority Decision — Analysis Pass

**Repository:** `reallaksh19/Grade9V3`  
**Dispatch base:** `4c450979369bffc850f4c6ffdf7afa1fcc89c98c`  
**Branch:** `physics-representation-authority-analysis-v2`  
**Mode:** analysis / decision artifact only — no production representation mutation  
**Scope:** current Vector Foundation and Relative Motion representation divergences

---

## 1. Decision question

Phase A correctly preserved the differences between Physics gate representations and candidate-library representations rather than choosing one layer silently. The next question is not "which ID wins?" It is:

> What semantic relationship exists between each gate representation and each library representation, and what architecture is required before those relationships can be enforced rather than inferred by reviewers?

The gate registry is upstream technical authority for subject representations. The library is the executable teaching layer and may realize those representations, but it must not silently replace or weaken gate semantics.

This pass therefore classifies each current divergence and identifies the smallest safe integration order. It does **not** rename, merge, bind, split, or author production representations.

---

## 2. Authority layers inspected

### Upstream technical authority

- `Shared/gates/gate.schema.json`
- `Physics/gates/motion-vectors.v1.json`

The gate schema explicitly describes the registry as upstream technical authority for what the subject matter requires before teaching is authored, including representations.

### Subject depiction capability

- `Physics/adapter/CoreContracts.json`
- `Physics/adapter/scenes.py`

The current implemented Physics scene kinds are:

- `VECTOR`
- `VECTOR_SUBTRACTION`
- `GRAPH`

`VECTOR` renders **one vector from the origin against axes**.

`VECTOR_SUBTRACTION` renders the explicit reverse-and-tail-to-head construction. Its implementation explicitly states that using `VECTOR` for that construction would hide the reversal the figure exists to show.

### Candidate teaching realization

- `Physics/library/vector-representation.v1.json`
- `Physics/library/relative-motion.v1.json`

### Existing shared representation audit

- `Shared/library/depiction.py`

This audit currently proves that a library representation uses a subject-declared representation kind and that picture/word/symbol correspondence is internally backed by library relations. It does **not** bind a library representation to the gate representation it realizes.

---

## 3. Structural finding: representation authority has no explicit gate → library lineage

Relations already have explicit upstream lineage:

```text
library relation
    gate_relation_ref
        ↓
gate relation
```

The package schema documents this as subject truth being owned by the gate registry while the library holds a compiler-reachable copy.

Representations have no equivalent field.

A library representation currently contains:

```text
id
kind
purpose
required_elements
relation_refs
read_order
instance_constraints
...
```

but no:

```text
gate_representation_ref
```

or equivalent.

Consequently, the current system can prove:

```text
library representation kind exists in subject adapter
library correspondence points to library relation symbols
```

but cannot prove:

```text
this library representation is the realization of this gate representation
```

or:

```text
its kind and relation custody agree with that upstream representation
```

This is the primary architectural gap. It explains why the repository can be green while Phase A still reports representation divergences.

**Decision:** do not repair representation IDs one by one before introducing explicit gate-to-library representation lineage. Otherwise the next divergence can recur with no mechanical falsifier.

---

## 4. Divergence classification

### 4.1 `MIC-VECTOR-VS-SCALAR`

```text
Gate:
  REP-VEC-SINGLE
  kind: VECTOR
  relation binding: REL-VEC-MAGNITUDE

Library:
  REP-VECTOR-COMPONENT
  kind: VECTOR
  relation_refs: REL-VECTOR-SUBTRACTION
```

**Classification:** `LIKELY_REALIZATION_WITH_WRONG_RELATION_CUSTODY`

The visual purpose substantially overlaps: one vector, declared axes, signed components, magnitude/direction distinction. The kinds also agree.

However, the gate representation is explicitly bound to the vector-magnitude relation while the library representation is bound to vector subtraction. That is not a harmless ID difference. It changes which mathematical symbols the correspondence layer treats as authoritative.

The library representation's current correspondence also names symbol `P` while its concrete scene draws symbol `w`. The existing depiction validator accepts this because `P` exists in the bound subtraction relation, but that is precisely the wrong relation for the scene's conceptual purpose.

**Decision:** do not call this pair aligned yet. The likely end state is a library single-vector realization explicitly bound to `REP-VEC-SINGLE` and to a compiler-reachable library copy of gate relation `REL-VEC-MAGNITUDE`.

---

### 4.2 `MIC-SIGNED-COMPONENT`

```text
Gate:
  REP-AXIS-CONVENTION
  kind: VECTOR
  relation binding: REL-AXIS-REVERSAL

Library:
  REP-VECTOR-COMPONENT
  kind: VECTOR
  relation_refs: REL-VECTOR-SUBTRACTION
```

**Classification:** `INSUFFICIENT_REALIZATION`

The gate representation is about comparing the **same physical vector under a changed axis declaration**. Its verification explicitly requires re-declaring an axis and checking that the relevant component changes sign while magnitude remains invariant.

The current library representation holds one single-vector scene only. It has neither a library copy of `REL-AXIS-REVERSAL` nor a representation structure that explicitly pairs the before/after declarations.

Reusing the single-vector representation ID for this microtopic therefore hides the distinguishing representation demand.

**Decision:** this needs a dedicated library realization rather than silently treating `REP-VECTOR-COMPONENT` as equivalent to `REP-AXIS-CONVENTION`.

A drawable realization is also coupled to the existing re-declared-component data gap (`ISS-VEC-EXIT-DATA`) unless the representation is designed without inventing transformed data.

---

### 4.3 `MIC-GRAPHICAL-SUBTRACTION`

```text
Gate:
  REP-SUB-CONSTRUCTION
  kind: VECTOR
  relation binding: REL-VEC-SUBTRACTION

Library:
  REP-VECTOR-SUBTRACTION-CONSTRUCTION
  kind: VECTOR_SUBTRACTION
  relation_refs: REL-VECTOR-SUBTRACTION
```

**Classification:** `SAME_SEMANTIC_CONSTRUCTION / GATE_KIND_TOO_GENERIC`

The semantic construction agrees strongly across layers:

```text
reverse Q
preserve its magnitude
translate without rotation
tail-to-head addition
draw/resultant
reconcile with component subtraction
```

The relation custody also agrees through the existing library relation's `gate_relation_ref`.

The kind does not agree. The subject adapter contains a specialized implemented `VECTOR_SUBTRACTION` kind specifically because a generic `VECTOR` scene renders one vector only and would hide the reverse-and-tail-to-head construction.

Therefore this is not evidence that the library invented an unnecessary specialized kind. It is evidence that the gate representation's `kind: VECTOR` is too weak for the representation contract the gate itself describes.

**Decision:** after explicit representation lineage exists, the gate representation should be reviewed for migration to `kind: VECTOR_SUBTRACTION`. Do not downgrade the library realization to `VECTOR`.

---

### 4.4 `MIC-SAME-TIME`

```text
Gate:
  REP-REL-POSITION
  kind: VECTOR
  relation binding: REL-RELATIVE-POSITION

Library microtopic:
  representation_refs: []
```

**Classification:** `MISSING_LIBRARY_REALIZATION`

The gate requires a declared-frame diagram containing both object positions and the displacement from B to A. No library representation is currently bound to this microtopic.

This cannot be fixed by pointing the microtopic at `REP-REL-VECTOR`, because that representation depicts velocity subtraction, not same-instant position geometry.

A concrete scene is also coupled to the existing Relative Motion position-data/oracle gap (`ISS-REL-EXIT-DATA`) if it is to be data-bound rather than hand-waved.

**Decision:** author a dedicated library realization of `REP-REL-POSITION` only after the representation-lineage mechanism exists and the required position data decision is made.

---

### 4.5 `MIC-COMMON-INTERVAL`

```text
Gate:
  REP-RELV-RESULTANT
  kind: VECTOR
  relation binding: REL-RELATIVE-VELOCITY

Library:
  REP-REL-VECTOR
  kind: VECTOR_SUBTRACTION
  relation_refs: REL-RELATIVE-VELOCITY
```

**Classification:** `DISTINCT_REPRESENTATION_VIEWS_OF_THE_SAME_RELATION`

The gate representation asks for a resultant relative-velocity vector in the declared frame and checks its components against the vector difference / same-interval position change.

The library representation instead shows the full subtraction construction by reversing `v_B` and adding it to `v_A`.

Both concern `REL-RELATIVE-VELOCITY`, but they are not representation-identical:

```text
REP-RELV-RESULTANT
    = resultant/readout view

REP-REL-VECTOR
    = construction/reverse-and-add view
```

The fact that the richer construction contains a resultant does not establish that a representation of one kind may automatically satisfy a gate representation of another kind. No refinement/subtyping policy exists in the subject contract.

**Decision:** preserve both views. Do not merge them. Add a dedicated library `VECTOR` realization for the gate resultant view, while retaining the subtraction construction where the teaching requires it.

The existing velocity data (`DAT-VAB-X`, `DAT-VAB-Y`) are sufficient for a single-resultant `VECTOR` scene, so this realization is not blocked on new numeric data.

---

### 4.6 `MIC-GEOMETRIC-CHECK`

```text
Gate:
  REP-REV-PAIR
  kind: VECTOR
  relation binding: REL-OBSERVER-REVERSAL

Library:
  REP-REL-VECTOR
  kind: VECTOR_SUBTRACTION
  relation_refs: REL-RELATIVE-VELOCITY
```

**Classification:** `MISSING_REQUIRED_VIEW + SUBJECT_KIND_EXPRESSIVENESS_GAP`

The gate's representation is specifically about the pair:

```text
v_A/B
v_B/A
```

with named observer order and verification that the two vectors sum to zero.

The current library representation shows one subtraction construction. It does not show the observer-reversal pair as the gate requires.

More importantly, the current implemented `VECTOR` renderer draws exactly one vector from the origin. A single `VECTOR` scene therefore cannot directly realize `REP-REV-PAIR` as named. Two independent scene instances are not mechanically guaranteed to be presented or verified as one paired representation.

**Decision:** do not fake this with the existing `VECTOR` renderer. Before authoring the library realization, decide whether Physics needs a new explicit representation kind such as `VECTOR_PAIR`, or an equally explicit paired-scene contract. This is a subject-adapter decision, not a library shortcut.

---

## 5. Corrected representation topology

The current representation state should therefore be understood as:

```text
VECTOR FOUNDATION

REP-VEC-SINGLE (gate, VECTOR)
  ↳ likely library single-vector realization
     but wrong relation custody today

REP-AXIS-CONVENTION (gate, VECTOR)
  ↳ dedicated library realization missing
  ↳ before/after convention data/scene decision required

REP-SUB-CONSTRUCTION (gate, currently VECTOR)
  ↳ REP-VECTOR-SUBTRACTION-CONSTRUCTION
     kind VECTOR_SUBTRACTION
     semantic construction matches
  ↳ gate kind should be reviewed, not library downgraded


RELATIVE MOTION

REP-REL-POSITION (gate, VECTOR)
  ↳ library realization missing

REP-RELV-RESULTANT (gate, VECTOR)
  ↳ dedicated resultant realization missing
  ↳ REP-REL-VECTOR is a different construction view

REP-REV-PAIR (gate, VECTOR)
  ↳ paired realization missing
  ↳ current VECTOR renderer cannot directly express the named pair
```

---

## 6. Shared architecture required before production reconciliation

### 6.1 Add explicit gate representation lineage

The library representation schema needs an explicit upstream binding analogous to `relation.gate_relation_ref`.

Preferred shape:

```yaml
gate_representation_ref: REP-...
```

A **one-library-representation → one-gate-representation** rule is preferred over a many-to-many list for the current architecture. If one microtopic needs multiple views, it should reference multiple library representations. This keeps each realization independently auditable and prevents one overly broad library record from pretending to satisfy several distinct gate contracts.

A representation with no gate counterpart should have to declare an explicit authority state rather than silently floating outside gate custody.

### 6.2 Add an authority validator

The validator should fail closed on at least:

```text
GATE_REPRESENTATION_REF_UNKNOWN
GATE_REPRESENTATION_KIND_MISMATCH
GATE_REPRESENTATION_RELATION_UNBOUND
GATE_REPRESENTATION_DUPLICATE_REALIZATION   # if 1:1 is enforced
```

For relation custody, a gate representation's `relation_bindings[]` should be satisfied by library relations whose `gate_relation_ref` names those gate relations.

Do **not** attempt free-text equality between gate `required_labels[]` and library `required_elements[]`; those are different layers of authoring. The explicit lineage plus kind/relation checks creates the minimum mechanical custody without pretending semantic prose can be safely compared lexically.

### 6.3 No representation-kind subtyping by inference

Until the subject adapter explicitly defines a refinement relation, treat:

```text
VECTOR != VECTOR_SUBTRACTION
```

A richer-looking figure is not automatically a valid realization of a simpler kind, and a generic kind is not automatically sufficient for a specialized construction.

---

## 7. Integration dependency order

The safe order is:

```text
1. representation lineage in shared package schema
2. authority validator + falsifier tests
3. correct the clear gate-kind mismatch for subtraction
4. split / bind Vector Foundation library representations
5. author missing Relative Motion resultant realization
6. resolve data dependency for axis-convention / relative-position scenes
7. decide paired-vector representation kind for observer reversal
8. only then mark Phase-A representation divergences resolved
```

This order prevents a library patch from inventing authority while the system still has no way to record which gate representation it claims to realize.

---

## 8. What can proceed independently

The oracle/data work can proceed in parallel because two missing realizations depend on data already tracked as separate gaps:

- re-declared component data for the axis-convention comparison;
- position data for the relative-position scene.

However, data work must not choose representation architecture on its own.

The Mathematics-provider review can also proceed independently; it does not control gate/library representation lineage.

---

## 9. Falsifiers for the eventual integration

Do not accept the representation integration unless all of the following become machine-checkable:

```text
Every library representation used by these two buckets either:
  - binds one known gate representation, or
  - carries an explicit reviewed exception state.

Every bound gate representation kind agrees with the library realization kind.

Every gate relation binding is reachable through a library relation whose
  gate_relation_ref identifies that gate relation.

MIC-VECTOR-VS-SCALAR no longer uses subtraction relation custody to explain
  magnitude/component correspondence.

MIC-SIGNED-COMPONENT has an axis-reversal realization rather than silently
  reusing a single static component scene.

MIC-GRAPHICAL-SUBTRACTION preserves the specialized reverse-and-add depiction;
  it is not downgraded to a one-vector scene.

MIC-SAME-TIME has an explicit relative-position realization or remains visibly
  blocked; no unrelated velocity representation is substituted.

MIC-COMMON-INTERVAL distinguishes resultant view from subtraction-construction
  view rather than merging them by ID.

MIC-GEOMETRIC-CHECK does not claim REP-REV-PAIR is fulfilled by a renderer that
  can only draw one vector.
```

---

## 10. Analysis result

```yaml
representation_authority:
  status: ARCHITECTURE_DECISION_REQUIRED_BEFORE_LIBRARY_RECONCILIATION

  primary_gap:
    code: GATE_LIBRARY_REPRESENTATION_LINEAGE_MISSING
    effect: >
      Gate representations are upstream authority, but library representations
      cannot currently declare which gate representation they realize.

  clear_gate_correction:
    representation: REP-SUB-CONSTRUCTION
    current_kind: VECTOR
    reviewed_target_kind: VECTOR_SUBTRACTION
    status: APPLY_ONLY_AFTER_LINEAGE_GATE_EXISTS

  missing_realizations:
    - REP-AXIS-CONVENTION
    - REP-REL-POSITION
    - REP-RELV-RESULTANT
    - REP-REV-PAIR

  existing_library_views_to_preserve:
    - REP-VECTOR-COMPONENT
    - REP-VECTOR-SUBTRACTION-CONSTRUCTION
    - REP-REL-VECTOR

  new_subject_kind_decision_required:
    - observer-reversal paired-vector view
```

**Completion claim for this pass:** the existing representation divergences are classified and their dependency order is explicit. No representation divergence is declared resolved by this analysis artifact.