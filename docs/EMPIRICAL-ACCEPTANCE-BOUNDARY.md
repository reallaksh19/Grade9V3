# Regression versus empirical learner acceptance

The repository has two evidence layers and they must not be collapsed.

## 1. Architectural regression

Architectural regression answers:

> Does the implementation still obey the repository/blueprint contracts?

It is automatic and CI-enforced. It may use synthetic fixtures and planted falsifiers.

Examples:

- prerequisite topology and delivery classification;
- schema/reference boundaries;
- learner-state routing rules;
- feedback state-machine behavior;
- blueprint-prescribed guard commands;
- absence of case-specific identifiers in Shared/core.

A green regression suite proves that the machinery behaves as specified. It does **not**
prove that the machinery helped a real learner.

## 2. Empirical learner acceptance

Empirical acceptance starts only from reviewed evidence of an actual learner session.

The observation contract therefore carries provenance:

- `LIVE_LEARNER` — reviewed observation from an actual learner session;
- `UNREVIEWED_SESSION_DRAFT` — output drafted by the runtime and not yet accepted as
  learner evidence;
- `HISTORICAL_IMPORT` — prior diagnostic/study-map evidence;
- `SYNTHETIC_TEST` — test-only evidence.

Only `LIVE_LEARNER + DIRECT_ATTEMPT` is visible to the empirical acceptance status layer.

The runtime deliberately produces `UNREVIEWED_SESSION_DRAFT`. A person must inspect the
attempt and observation before persisting it as `LIVE_LEARNER`.

## Status semantics

`Shared/tools/empirical_acceptance.py` reports:

```text
PENDING_REAL_EVIDENCE
EMPIRICAL_EVIDENCE_AVAILABLE
INVALID_EMPIRICAL_EVIDENCE
```

`PENDING_REAL_EVIDENCE` is not a CI failure. It is the honest state before a learner has
produced reviewed evidence.

`EMPIRICAL_EVIDENCE_AVAILABLE` also is not an automatic claim that the system has passed
learner acceptance. It means real evidence exists and can now be reviewed against the
product question being investigated.

`INVALID_EMPIRICAL_EVIDENCE` is structural: evidence claiming `LIVE_LEARNER` must name
the session and question that produced it. CI may fail that state because the claimed
evidence is not inspectable.

## CI boundary

CI runs both layers differently:

```text
Blueprint regression
    enforcing

Empirical learner acceptance status
    enforce evidence structure
    do not require evidence to exist
```

This prevents two opposite errors:

- synthetic regression data becoming a fake learner-success claim;
- lack of a learner session blocking unrelated architecture work.

A real learner acceptance conclusion remains a human/product decision grounded in the
retained learner episode. No test fixture can manufacture it.
