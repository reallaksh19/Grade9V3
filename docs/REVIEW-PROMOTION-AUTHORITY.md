# Review and promotion authority

`REVIEWED` and `CURATED` are evidence claims. They are not labels an agent may assign by editing JSON.

This layer binds promotion to exact record digests and external receipts.

## Lifecycle

```text
authoring-run receipt
   ↓
exact CANDIDATE record digest
   ↓
independent review
   ↓
REVIEWED promotion receipt
   ↓
exact REVIEWED record digest
   ↓
curation acceptance
   ↓
CURATED promotion receipt
```

Only adjacent transitions are legal:

- `CANDIDATE -> REVIEWED`
- `REVIEWED -> CURATED`

Stage skipping fails.

## First review

A `CANDIDATE -> REVIEWED` request must pin the authoring-run receipt that created the record.

The review authority verifies:

- the authoring receipt itself conforms to the run-receipt contract;
- its digest matches the pinned digest;
- it lists the target record among `changed_records`;
- the authored record digest equals the current candidate digest;
- the reviewer is not the authoring actor;
- originals were inspected;
- review result is PASS;
- the promotion changes only `status`;
- the resulting package still passes intake;
- the promoted record does not outrank any dependency.

## Curation

`REVIEWED -> CURATED` must pin the prior REVIEWED promotion receipt.

The authority verifies that the current reviewed digest exactly matches the prior receipt, that the prior review chain is still valid, and that the original author is not self-curating the record.

## Hidden edits are impossible

A promotion receipt stores both the before and after record digest.

For REVIEWED, the verifier reconstructs the candidate record by changing only `status` back to `CANDIDATE`. For CURATED it reconstructs the reviewed record by changing only `status` back to `REVIEWED`.

If that reconstructed digest does not equal the receipt's before digest, the promotion contains an unreviewed content edit and fails.

Therefore promotion is status-only. Content edits require a new authoring/review cycle.

## Review authority at release time

Academic release no longer trusts `record.status` alone.

A microtopic marked `REVIEWED` or `CURATED` counts as reviewed only when a valid current-stage promotion receipt matches the exact current record digest.

A hand edit such as:

```json
{"status":"REVIEWED"}
```

without a matching receipt becomes `UNBACKED_REVIEWED`, and learner release remains blocked.

## Review authority at source-sufficiency time

Source-question coverage applies the same rule.

A question marked `REVIEWED`/`CURATED` contributes to `SUFFICIENT` source coverage only if its promotion receipt chain verifies. A raw status edit cannot manufacture Core2/Core2A/Core2B custody coverage.

## Staleness

Changing any reviewed record after review changes its digest.

The previous review receipt then becomes stale automatically. The effective stage is no longer review-backed until the changed candidate goes through a new review cycle.

Unrelated changes elsewhere in the package do not invalidate the record-level review authority.

## Legacy promotion helper

`Shared.library.promote.promote()` no longer performs upward promotion.

Any direct `CANDIDATE -> REVIEWED` or `REVIEWED -> CURATED` call fails with
`DIGEST_BOUND_REVIEW_AUTHORITY_REQUIRED`. The helper retains demotion and dependency
maturity auditing only.

This removes a parallel promotion path that could otherwise bypass authoring receipts and
record-digest checks.

## Storage

Promotion receipts are stored under:

`Reviews/receipts/`

They remain outside canonical records so package schemas do not grow hidden lifecycle fields and review evidence cannot be silently rewritten as teaching content.

## Commands

Validate a promotion:

```text
python3 Shared/tools/review_authority.py --request /path/to/promotion-request.json
```

Validate and apply:

```text
python3 Shared/tools/review_authority.py --request /path/to/promotion-request.json --write
```

Audit committed current-stage review receipts:

```text
python3 Shared/tools/review_authority.py --audit --enforce
```

Behavioral falsifiers live in `tests/test_review_authority.py`.
