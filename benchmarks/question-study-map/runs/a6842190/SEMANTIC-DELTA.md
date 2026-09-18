# Semantic delta checked after PR #64

Baseline: `a6842190f4b9835c654ec110a5875c33ae8ca220`

## Session-only location selection

Expected:

```text
canonical route offers multiple locations
+ owner selects one offered location
→ selected location used for this session
→ EXECUTE_WITH_FALLBACK
→ canonical ambiguity remains unchanged
```

Contract evidence: `tests/test_study_session.py::test_owner_can_select_one_offered_location_for_session_only`.

Result: **PASS**.

## Session-only external bridge

Expected:

```text
canonical delivery unresolved
+ owner explicitly chooses EXTERNAL:provider
→ BRIDGE for this session only
→ provider is not written into the canonical capability
→ EXECUTE_WITH_FALLBACK
```

Contract evidence: `tests/test_study_session.py::test_owner_can_supply_session_external_bridge_without_mutating_canonical_route`.

Result: **PASS**.

## Dependency safety remains stronger than owner convenience

Expected: an owner resolution may address the target capability but may not bypass a still-unresolved prerequisite dependency.

Observed: #64 retains prerequisite dependency checks before owner resolution of the dependent route.

Result: **PASS**.

## Evidence boundary

Owner resolution changes execution only. It does not create `DEMONSTRATED` evidence, and #62 still caps an independent correct attempt at `UNCERTAIN` when canonical fresh verification is unavailable.

Result: **PASS**.
