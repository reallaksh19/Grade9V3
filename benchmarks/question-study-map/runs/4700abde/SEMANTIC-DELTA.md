# Semantic delta checked in this rerun

Baseline: `4700abdefecefd6211488a527594dabba8797e89`

The content benchmark already established question mapping, prerequisite routing, bridges, diagnosis, repair and verification behavior. PRs #60–#62 changed **execution policy**, so this rerun checks those changes against the existing benchmark cases rather than inventing a second benchmark framework.

## 1. Incomplete matrix is not automatically a whole-session stop

Expected:

```text
matrix = NOT_READY
demanded rung = represented + safe teaching path
→ EXECUTE_WITH_FALLBACK
```

Observed contract evidence:
- `tests/test_study_session.py::test_not_ready_matrix_can_execute_usable_demanded_rungs_with_fallback`

Result: **PASS**.

## 2. Missing teaching is not treated as usable fallback

Expected:

```text
demanded rung = NEEDS_SUPPORT
but microtopic/capability/teaching path absent
→ OWNER_DECISION
```

Observed contract evidence:
- `READINESS_MICROTOPIC_MISSING`
- `READINESS_CAPABILITY_MISSING`
- `READINESS_TEACHING_PATH_MISSING`
- `test_missing_teaching_path_requires_owner_decision_even_when_rung_is_needs_support`

Result: **PASS**.

## 3. Dependency safety

Expected:

```text
prerequisite A → OWNER_DECISION
dependent B
→ B also OWNER_DECISION
unrelated C
→ may continue
```

Observed contract evidence:
- `test_owner_decision_propagates_to_dependents_but_not_unrelated_branch`

Result: **PASS**.

## 4. Fallback teaching does not manufacture mastery

Expected:

```text
independent correct attempt
+ no canonical fresh verification
→ observation draft UNCERTAIN
not DEMONSTRATED
```

Observed contract evidence:
- `STUDY_SESSION_VERIFICATION_UNAVAILABLE`
- `test_independent_correct_attempt_without_verification_stays_uncertain`

Result: **PASS**.

## 5. Existing benchmark invariants stay intact

The fallback policy does not change:

- canonical capability ownership;
- prerequisite topology;
- matrix readiness labels;
- external bridge visibility;
- source custody;
- learner evidence precedence;
- external question transience.

Result: **PASS**.
