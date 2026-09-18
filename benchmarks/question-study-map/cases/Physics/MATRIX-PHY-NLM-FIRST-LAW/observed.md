# Observed behavior — Newton's first law and free-body diagrams

Baseline: `e6f9ccce4a2ecbba8764bfa5cd5e877830afa56d`  
Readiness snapshot: `SESSION_READY`  
Overall benchmark disposition: **PASS**

This pack records the frozen repository state. Synthetic falsifiers are used only where the benchmark contract permits them; no learner response, missing source information or production content is fabricated.

| Case | Status | Observed | Evidence |
| --- | --- | --- | --- |
| Direct-ready question | **PASS** | Canonical question inventory exists (7 retained questions); the representative demand has a canonical capability and teaching location. | Physics/library/phy-nlm-first-law.v1.json; Physics/matrices/phy-nlm-first-law.rungs.json |
| Prerequisite route | **PASS** | Declared prerequisite edges are explicit and can be ordered without comparing ladder_position across matrices. | Physics/library/phy-nlm-first-law.v1.json; docs/SESSION-READINESS-REPORT.md |
| Multi-capability question | **PASS** | A retained question explicitly separates primary ownership from secondary demand. | Physics/library/phy-nlm-first-law.v1.json |
| Repeated demand | **PASS** | The retained inventory contains repeated primary-capability demand that should consolidate to one teaching target. | Physics/library/phy-nlm-first-law.v1.json |
| Unknown learner | **PASS** | Unknown learner state does not alter canonical truth. For SESSION_READY, the plan may study/check/stop, but no mastery is invented. | Shared/tools/learner_evidence.py; Shared/tools/study_start.py; Shared/tools/worksheet_study_plan.py |
| Rough owner estimate | **PASS** | The owner-estimate contract selects an existing local rung/starting coordinate and leaves prerequisite checks/evidence distinct from mastery. | Shared/tools/study_start.py; tests/test_study_start.py |
| Prior learner evidence | **PASS** | The current learner-evidence contract gives direct/diagnostic observations precedence over rough estimates. | Shared/tools/learner_evidence.py; tests/test_practical_learner_evidence.py |
| External provider bridge | **NOT_APPLICABLE** | No external_provider prerequisite is declared for this matrix slice; no bridge case was manufactured. | Physics/library/phy-nlm-first-law.v1.json |
| Content gap | **NOT_APPLICABLE** | Every current matrix rung has a canonical microtopic_ref; no artificial missing-content case was created. | Physics/matrices/phy-nlm-first-law.rungs.json |
| Incomplete source | **NOT_APPLICABLE** | No genuine figure/table/source-insufficiency case is retained for this matrix benchmark; none was invented. | Physics/library/phy-nlm-first-law.v1.json |
| Feedback diagnosis | **PASS** | Every represented microtopic in this matrix slice contains misconception/diagnostic/repair data; the generic feedback contract also refuses unsupported ambiguous attribution. | Physics/library/phy-nlm-first-law.v1.json; Shared/tools/feedback.py; tests/test_feedback.py |
| Repair | **PASS** | Represented microtopics provide repair text and a teaching path; the feedback runtime can route a supported failed capability to canonical repair rather than inventing new content. | Physics/library/phy-nlm-first-law.v1.json; Shared/tools/feedback.py |
| Fresh verification | **PASS** | Represented microtopics provide exit tasks; the generic feedback contract selects a fresh same-capability question when available or an exit task fallback. | Physics/library/phy-nlm-first-law.v1.json; Shared/tools/feedback.py; tests/test_feedback.py |
| Help-dependent success | **PASS** | The shared evidence contract treats helped success conservatively and does not create independent DEMONSTRATED evidence. | Shared/tools/learner_evidence.py; tests/test_practical_learner_evidence.py |
| Independent success | **PASS** | Independent correct work may draft DEMONSTRATED evidence; review scheduling is deterministic and learner-state persistence remains explicit. | Shared/tools/feedback.py; Shared/tools/review_schedule.py; tests/test_feedback.py; tests/test_review_schedule.py |

## Gap-ledger links

No material benchmark gap recorded for this matrix in this sweep.

## Benchmark-agent boundary

No `Shared/**`, `Physics/**`, schema, learner-profile, source-custody or production-content file was changed to obtain this result.
