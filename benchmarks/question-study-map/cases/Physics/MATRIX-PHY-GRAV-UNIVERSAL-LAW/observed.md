# Observed behavior — Universal gravitation, free fall and orbital motion

Baseline: `e6f9ccce4a2ecbba8764bfa5cd5e877830afa56d`  
Readiness snapshot: `NOT_READY`  
Overall benchmark disposition: **PARTIAL**

This pack records the frozen repository state. Synthetic falsifiers are used only where the benchmark contract permits them; no learner response, missing source information or production content is fabricated.

| Case | Status | Observed | Evidence |
| --- | --- | --- | --- |
| Direct-ready question | **PASS** | Canonical question inventory exists (1 retained question); the representative demand has a canonical capability and teaching location. | Physics/library/phy-grav-universal-law.v1.json; Physics/matrices/phy-grav-universal-law.rungs.json |
| Prerequisite route | **NOT_APPLICABLE** | No prerequisite edge exists in the current represented capability slice; no artificial prerequisite case was created. | Physics/library/phy-grav-universal-law.v1.json |
| Multi-capability question | **NOT_APPLICABLE** | No retained question in this package provides a genuine multi-capability case; none was manufactured. | Physics/library/phy-grav-universal-law.v1.json |
| Repeated demand | **NOT_APPLICABLE** | No genuine repeated-primary question pair exists in the retained inventory; none was manufactured. | Physics/library/phy-grav-universal-law.v1.json |
| Unknown learner | **PASS** | Unknown learner state does not alter canonical truth. For NOT_READY, the plan may study/check/stop, but no mastery is invented. | Shared/tools/learner_evidence.py; Shared/tools/study_start.py; Shared/tools/worksheet_study_plan.py |
| Rough owner estimate | **PASS** | The owner-estimate contract selects an existing local rung/starting coordinate and leaves prerequisite checks/evidence distinct from mastery. | Shared/tools/study_start.py; tests/test_study_start.py |
| Prior learner evidence | **PASS** | The current learner-evidence contract gives direct/diagnostic observations precedence over rough estimates. | Shared/tools/learner_evidence.py; tests/test_practical_learner_evidence.py |
| External provider bridge | **NOT_APPLICABLE** | No external_provider prerequisite is declared for this matrix slice; no bridge case was manufactured. | Physics/library/phy-grav-universal-law.v1.json |
| Content gap | **PARTIAL** | 2 of 5 matrix rungs lack canonical microtopic_ref (R2, R3). The current readiness status is NOT_READY; the gap remains visible instead of being fabricated away. | Physics/matrices/phy-grav-universal-law.rungs.json; docs/SESSION-READINESS-REPORT.md |
| Incomplete source | **NOT_APPLICABLE** | No genuine figure/table/source-insufficiency case is retained for this matrix benchmark; none was invented. | Physics/library/phy-grav-universal-law.v1.json |
| Feedback diagnosis | **PASS** | Every represented microtopic in this matrix slice contains misconception/diagnostic/repair data; the generic feedback contract also refuses unsupported ambiguous attribution. | Physics/library/phy-grav-universal-law.v1.json; Shared/tools/feedback.py; tests/test_feedback.py |
| Repair | **PASS** | Represented microtopics provide repair text and a teaching path; the feedback runtime can route a supported failed capability to canonical repair rather than inventing new content. | Physics/library/phy-grav-universal-law.v1.json; Shared/tools/feedback.py |
| Fresh verification | **PASS** | Represented microtopics provide exit tasks; the generic feedback contract selects a fresh same-capability question when available or an exit task fallback. | Physics/library/phy-grav-universal-law.v1.json; Shared/tools/feedback.py; tests/test_feedback.py |
| Help-dependent success | **PASS** | The shared evidence contract treats helped success conservatively and does not create independent DEMONSTRATED evidence. | Shared/tools/learner_evidence.py; tests/test_practical_learner_evidence.py |
| Independent success | **PASS** | Independent correct work may draft DEMONSTRATED evidence; review scheduling is deterministic and learner-state persistence remains explicit. | Shared/tools/feedback.py; Shared/tools/review_schedule.py; tests/test_feedback.py; tests/test_review_schedule.py |

## Gap-ledger links

- `GAP-QSM-0002`

## Benchmark-agent boundary

No `Shared/**`, `Physics/**`, schema, learner-profile, source-custody or production-content file was changed to obtain this result.
