# Fallback-First Blueprint Plan

> Tracking issue: #54  
> Independent benchmark stream: #47 / PR #48

## Purpose

Grade9V3 is a one-learner self-study system. Strict checks are useful only if they keep the system honest without making it fragile.

This plan makes the current workflow **fallback-first**: continue every safely executable part of a worksheet, surface gaps explicitly, and reserve whole-session STOP for cases where nothing can proceed without inventing truth.

~~~text
worksheet / questions
→ map demand
→ resolve prerequisites + delivery
→ apply learner evidence if available
→ classify each demanded route item
→ EXECUTE / EXECUTE_WITH_FALLBACK / OWNER_DECISION / DEFER_ITEM
→ STOP only when no executable item remains
~~~

No new curriculum model, mastery model, or Core is introduced.

## Central invariant

> **Block the smallest affected unit, not the whole session.**

Readiness remains truthful. Execution becomes more granular.

Matrix readiness continues to answer:

- Is this matrix fully self-study-ready?
- What support/content gaps exist?
- Can it be advertised as ready?

Session execution instead answers:

- What can this learner safely do now?
- What needs a fallback?
- What needs an owner decision?
- What must be deferred?

## Execution disposition

Use one small vocabulary across the self-study path:

~~~text
EXECUTE                safe normal path
EXECUTE_WITH_FALLBACK  safe conservative path; limitation remains visible
OWNER_DECISION         safe only after explicit session-level owner choice
DEFER_ITEM             this question/capability/branch cannot proceed now
STOP                   no safe executable path remains
~~~

These are execution decisions, not academic truth or mastery states.

## Input and gap fallback matrix

| Input / condition | Default behavior | Owner option | Forbidden |
| --- | --- | --- | --- |
| Learner evidence absent | UNOBSERVED; diagnostic/quick-check start | Provide estimate/evidence | Invent mastery |
| Rough estimate absent | Neutral route | Add estimate | Require estimate |
| Rough estimate malformed/unknown | Ignore it, warn, continue neutral route | Correct it | Invalidate worksheet |
| Syllabus absent | Question demand + prerequisite closure | Add capability refs | Claim syllabus completeness |
| Prior study map absent | Continue without history | Import later | Block |
| One question mapping unresolved | Defer that question | Confirm manual mapping | Guess silently |
| Missing figure/table/data | Defer affected question | Supply source | Infer missing information |
| Underdetermined/bad item | Flag/defer item | Clarify/replace | Diagnose learner from invalid item |
| No local teaching + external provider | BRIDGE | Confirm provider | Fabricate local lesson |
| No local teaching + no provider | Defer affected branch; continue others | Supply session-only bridge | Create canonical content silently |
| Multiple local teaching locations | OWNER_DECISION or defer | Select one for session | Arbitrary global choice |
| Teaching usable but Core1A/Core1B/diagnostic incomplete | Private pilot fallback with visible limitation | Allow pilot | Relabel fully ready |
| Verification missing | Teach/repair may proceed; no DEMONSTRATED promotion | Supply fresh check | Mark mastered without verification |
| Academic/source warning | Keep visible; mechanically usable private pilot may proceed | Acknowledge | Claim reviewed/source-backed |
| Unknown prerequisite / cycle | Defer affected branch | Skip/defer branch | Fabricate prerequisite truth |
| Some worksheet items unsupported | Run supported subset | Owner may stop | Reject whole worksheet |
| No executable items | STOP | Supply missing input/content/source | Pretend progress is possible |

## Narrow owner override

Owner override is an execution mechanism only. It must never become curriculum truth or learner evidence.

Initial actions should remain small:

~~~text
CONFIRM_MAPPING
SELECT_TEACHING_LOCATION
SUPPLY_EXTERNAL_BRIDGE
ALLOW_PRIVATE_PILOT
DEFER_ITEM
~~~

Each override records:

- target;
- action;
- short reason/note;
- SESSION_ONLY scope;
- acknowledged finding(s);
- stale detection using existing request/plan digest machinery where practical.

Override must never:

- create DEMONSTRATED;
- rewrite capability/prerequisite truth;
- invent source information;
- promote candidate/unreviewed content;
- hide the warning that caused the override;
- silently persist into canonical content.

## Hard-stop rule

A blocker is justified only when continuing would require one of:

1. inventing academic truth;
2. inventing missing source/figure/data;
3. falsely attributing learner state;
4. operating on an uninterpretable request;
5. executing when every demanded route item is unavailable.

If none apply, prefer:

~~~text
fallback
→ warning
→ owner decision when useful
→ defer only affected item
~~~

## Work packages

### F0 — Baseline fallback falsifiers

No runtime changes.

Add subject-neutral tests/fixtures for:

- malformed optional estimate with otherwise valid route;
- no learner data;
- one unresolved question + one routable question;
- partially supported worksheet;
- demanded ready rung inside an otherwise incomplete matrix.

The tests should capture current over-blocking without relying on one named Physics topic.

### F1 — Contract and reporting

Freeze the execution-disposition semantics and fallback table.

Acceptance:

- every optional input has a defined fallback;
- every hard-stop condition has a written semantic reason;
- no duplicate learning model is introduced.

### F2 — Optional-input resilience

Change optional input failures from plan-invalidating findings to visible warnings/fallbacks.

Primary targets:

- study_session.resolve_estimates();
- study_start.resolve();
- worksheet_study_plan composition.

Acceptance:

- bad optional estimate does not set the session unusable;
- missing optional inputs preserve conservative defaults;
- owner warnings stay visible.

### F3 — Per-route execution gating

Stop using matrix NOT_READY as a blanket kill switch.

Derive executability from the demanded capability/rung/branch while preserving matrix readiness as truthful summary metadata.

Acceptance:

- supported route subset has a next step;
- unsupported questions/capabilities are explicitly deferred;
- matrix NOT_READY remains unchanged where appropriate;
- full-session STOP only when no executable item remains.

### F4 — Session owner override

Add a narrow session-only override input.

Acceptance:

- explicit provenance;
- warning retained;
- stale/invalid override ignored or rejected safely;
- no canonical or learner-state mutation.

### F5 — Attempt/feedback consistency

Use the same smallest-unit rule after attempts.

Acceptance:

- a blocked/unavailable question does not disable unrelated supported questions;
- a locally attributable failure can still receive local repair even if unrelated external demand exists;
- missing verification prevents mastery promotion, not teaching/repair;
- unavailable failed capability is deferred rather than fabricated.

### F6 — Benchmark rerun

After #47 completes:

- rerun all benchmark packs unchanged;
- add regression fixtures only for recurring blocker patterns;
- do not weaken benchmark expectations to fit implementation;
- record any remaining STOP and the semantic reason no fallback is safe.

## Expected module impact

Prefer changing existing composition logic over adding more modules.

Likely touched:

~~~text
Shared/tools/study_session.py
Shared/tools/study_start.py
Shared/tools/worksheet_study_plan.py
Shared/tools/session_readiness.py   # reporting/helper extraction only if needed
tests/...
~~~

Possible small schema addition only if F4 proves it necessary:

~~~text
Shared/library/session-overrides.schema.json
~~~

Do not extend package/matrix schemas merely to support this plan.

## Regression principles

- tests must be subject-neutral whenever possible;
- fallback behavior is tested separately from canonical truth;
- owner override must be tested as session-scoped;
- warnings/gaps must remain visible after fallback;
- a partial worksheet must never be promoted to fully ready;
- a deferred item must never become learner evidence;
- only independent fresh verification may support DEMONSTRATED.

## Relationship to #47

#47 remains the independent measurement stream.

This plan may proceed through F0/F1 without waiting for #47. Runtime changes F2-F5 should preserve benchmark independence. F6 begins only after the benchmark sweep is complete so recurring failure patterns can be checked against the new fallback semantics.

## Definition of done

The blueprint is resilient when:

1. missing learner/profile/syllabus/history inputs do not block;
2. bad optional owner hints degrade to neutral defaults;
3. one unavailable worksheet item does not stop supported items;
4. matrix readiness remains honest but does not substitute for route-item executability;
5. owner has a narrow, visible session escape hatch;
6. STOP means there is genuinely no safe path forward;
7. no fallback can create mastery, curriculum truth, or source authority.

> The target is not fewer checks. The target is **strict checks with graceful degradation**.