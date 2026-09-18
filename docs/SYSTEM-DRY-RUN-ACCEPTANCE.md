# System dry-run acceptance

> Status: **COMPLETE for current no-learner-input workflow**
>
> Evidence class: synthetic/system evidence only. This document does not create learner
> evidence and does not change the empirical acceptance status.

## Decision

The repository may continue architecture, content, matrix and worksheet-routing work without
waiting for an interactive learner session.

For the current workflow, system confidence comes from:

- architectural regression;
- exhaustive synthetic feedback/session scanners;
- real-source worksheet routing;
- the Q4 end-to-end dry run;
- canonical diagnosis/repair/verification checks;
- explicit evidence-boundary tests.

Actual learner evidence remains a separate optional empirical lane. If it becomes available
later, it may be reviewed and persisted under the existing `LIVE_LEARNER` contract. Its
absence is not a blocker for unrelated system or content work.

No new runtime execution state, matrix field, learner state or acceptance enum is introduced
by this decision.

## Accepted system path

The concrete end-to-end case is the real-source Relative Motion item:

```text
NEETPREP-MQB-REL-Q4
        ↓
worksheet capability mapping
        ↓
prerequisite closure
        ↓
session readiness / explicit bridge
        ↓
evaluated attempt signature
        ↓
diagnose / retry / repair
        ↓
fresh verification
        ↓
UNREVIEWED_SESSION_DRAFT
        ↓
NOT_WRITTEN
```

The system dry run covers these high-likelihood branches:

1. independent correct;
2. correct after help and fresh verification;
3. clear concept/setup failure;
4. execution/careless failure;
5. ambiguous/undecidable failure;
6. persistent/repair path;
7. explicit local prerequisite failure;
8. explicit external-prerequisite failure requiring `OWNER_DECISION`.

The first Q4 dry run also falsified a real integration defect: an explicitly supported
prerequisite failure was previously discarded because feedback accepted only direct
primary/secondary question capabilities. PR #72 repaired this generically by allowing
explicit attribution to canonical prerequisite closure without copying prerequisites into
worksheet mappings or widening ambiguous diagnosis.

## Evidence retained

Relevant merged evidence:

- PR #66 — exhaustive feedback-policy scanner;
- PR #67 — study-session orchestration scanner;
- PR #68 — high-likelihood learner scenarios and matrix contract;
- PR #72 — real-source Q4 dry run plus prerequisite-attribution repair.

PR #72 final validation:

```text
651 tests
OK

generated architecture manifest  PASS
JSON checks                      PASS
full guardrails                  PASS
```

## Boundary with empirical evidence

System evidence and learner evidence answer different questions.

```text
SYSTEM / DRY-RUN EVIDENCE
Does the machinery route safely and according to the blueprint?
→ may be synthetic
→ may use planted falsifiers
→ may proceed without student input

EMPIRICAL LEARNER EVIDENCE
What did this actual learner demonstrate?
→ requires reviewed actual learner work
→ provenance = LIVE_LEARNER
→ cannot be manufactured by a dry run
```

The empirical tool may therefore continue to report:

```text
PENDING_REAL_EVIDENCE
```

while the system dry-run workstream is complete.

That is not a contradiction. `PENDING_REAL_EVIDENCE` means only that no reviewed live learner
attempt has been retained.

## Future rule

Do not create more synthetic architecture merely because learner evidence is unavailable.

Continue normal work unless one of these produces a concrete defect:

```text
real worksheet demand
system dry-run failure
benchmark regression
later live learner evidence
```

If live evidence becomes available later, reopen or create an empirical review task and keep
the observation in the learner-evidence lane. Do not retroactively relabel synthetic dry-run
outputs as learner evidence.
