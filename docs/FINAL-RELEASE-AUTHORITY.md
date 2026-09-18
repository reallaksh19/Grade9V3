# Final learner-release authority

A publication is build output. A release is an authority claim over that output.

The publication engine therefore continues to write:

`release_authorized: false`

inside every publication manifest. No build process may grant learner release.

Release authority exists only as an external receipt under `Releases/receipts/`.

## Release chain

```text
authoring request
  ↓
fresh plan
  ↓
fresh execution packet
  ↓
current source custody
  ↓
current digest-backed review authority
  ↓
verified publication bytes + provenance
  ↓
external learner-release receipt
```

## What a release receipt binds

A successful receipt records:

- exact authoring-request digest;
- fresh planner digest and READY_FOR_RELEASE state;
- exact execution-packet digest;
- publication manifest digest and basis digest;
- digest of the complete manifest file table;
- learner-visible page/figure hashes;
- publication provenance digest and LIBRARY basis;
- exact learner-route value and digest;
- source-receipt id/digest when the request uses source-backed products;
- every learner-facing microtopic/question used by the publication, with its current record digest;
- every promotion receipt discovered from those review chains;
- every authoring-run receipt discovered through those promotion receipts.

The releaser does not supply the review/authoring receipt list. It is discovered from validated record authority so evidence cannot be omitted selectively.

## Publication immutability

Granting release does not modify the publication directory.

The publication manifest remains machine-non-authoritative. The release receipt references it by digest.

Changing any built artifact changes the manifest verification or manifest digest and invalidates the release receipt.

## Recomputable authority

A stored receipt is not trusted because it exists.

`verify_receipt()` reconstructs the release request from the receipt and recomputes:

- current request digest;
- current planner state;
- current execution packet;
- current publication verification;
- current publication provenance;
- current library records used by the run;
- current review/curation authority;
- current source receipt;
- current learner route.

The recomputed receipt must be byte-for-byte equivalent at the JSON-digest level.

Any upstream change produces `RELEASE_RECEIPT_STALE` or a more specific blocking finding.

## Learner-facing review closure

For every record named by the publication basis, learner-facing collections are closed:

- `microtopics`
- `questions`

Each must currently be REVIEWED or CURATED through the digest-bound promotion authority from PR #17.

A raw status edit cannot satisfy release.

## Product closure

The Core set in the frozen publication must exactly equal the set the fresh planner currently marks READY for the pinned request.

This prevents releasing an old five-Core publication after the request, source state, learner route, or library now requires a different product set.

## Source closure

When the fresh plan uses a source receipt, release records its id and immutable digest.

If source custody changes, the planner/packet/receipt chain changes and the release becomes stale.

## Provenance closure

Learner release requires `basis = LIBRARY`.

`AUTHORED_OUTSIDE_THE_LIBRARY` remains a legitimate engineering/demo publication state but cannot receive learner-release authority.

All publication-provenance findings, including stale omitted microtopics, block release even where the general provenance audit only reports them.

## Bypass prevention

A publication manifest with `release_authorized: true` is itself a CI failure.

Release can be represented only by a valid external receipt.

## Commands

Evaluate a release request without writing:

```text
python3 Shared/tools/release_authority.py --request /path/to/release-request.json
```

Issue the immutable receipt:

```text
python3 Shared/tools/release_authority.py --request /path/to/release-request.json --write
```

Verify an existing receipt:

```text
python3 Shared/tools/release_authority.py --receipt Releases/receipts/<id>.json --enforce
```

Audit all committed release receipts and manifest bypasses:

```text
python3 Shared/tools/release_authority.py --audit --enforce
```

Behavioral falsifiers live in `tests/test_release_authority.py`.
