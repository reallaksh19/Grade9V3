# Authoring run receipts

Execution packets say what a third agent may do. This layer enforces what it actually did.

An agent does not write directly to the canonical library or arbitrary repository paths.
It submits one authoring proposal against one runnable work order.

## Modes

### CANDIDATE_RECORDS_ONLY

Used by `AUTHOR_CANDIDATE_QUESTION` work orders.

The executor requires:

- an existing target package inside `<subject>/library/`;
- only collections named by the work order;
- only new record ids;
- `status = CANDIDATE`;
- `origin = AUTHORED`;
- an AUTHORED canonical origin resource;
- bucket-owned primary capability;
- exposure to the work-order Core;
- a merged package that passes the normal intake gate.

For Core2B, two extra transfer proofs are mandatory:

- `adaptation.parent_ref` points at a real canonical question and `changed_fields` names fields whose values actually differ;
- `transfer` states the changed demand dimension and `builds_on` lineage, including the parent question.

Changing only metadata is not transfer.

### PRODUCT_OUTPUT_ONLY

Used by `BUILD_FROM_CANONICAL` work orders.

The executor rejects all library writes. Product artifacts may be written only below:

`publication/drafts/<run_id>/<core>/`

Path traversal outside that root is rejected.

## Staleness

Every proposal pins the request digest and execution-packet digest.

Before validating the proposal, the executor re-verifies the packet against the current request,
library, matrix, role contracts and source receipt. A stale packet or stale proposal fails.

## Authoring run receipt

A successful validation produces a receipt containing:

- request and packet digests;
- Core and authoring action;
- work-order digest;
- exact write scope;
- target package digest before and after, when applicable;
- ids/status/origin/digests of newly added records;
- output artifact paths, byte counts and digests;
- acceptance commands inherited from the packet;
- a statement that scope/schema validation is not academic approval.

By default validation is dry-run only.

`--write` applies the validated package/artifacts and stores the receipt under
`publication/authoring-runs/` unless another receipt path is explicitly supplied.

## What this does not permit

- promotion to REVIEWED or CURATED;
- mutation of existing canonical records;
- authored content becoming Core2 custody;
- Core2B transfer by relabelling same-family practice;
- product output writing into the library;
- writes from WAIT/HOLD/WITHHELD work orders.

## CI

CI runs:

`python3 Shared/tools/execute_authoring_run.py --audit --enforce`

This proves every runnable write-scope/action pair emitted by committed author-request fixtures
is supported by the executor. Behavioral falsifiers live in `tests/test_authoring_run.py`.
