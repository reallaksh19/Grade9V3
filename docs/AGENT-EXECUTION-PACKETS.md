# Agent execution packets

Planning answers **what is known and what is still missing**. An execution packet answers
**what a third agent may do next without re-deciding the architecture**.

The packet is intentionally not learner-facing content. It is a pinned work contract.

## Lifecycle

Three transitions are separate:

1. **AUTHORING** — candidate material may be created once structural findings, owner
   decisions and agent-owned prerequisite actions are resolved.
2. **BUILD** — requested products may be compiled only when the library/compiler actually
   supports them.
3. **RELEASE** — learner release requires build readiness plus mechanical academic
   reviewability and human academic review.

This prevents a circular rule in which content would have to be reviewed before it could be
authored.

## Partial execution

A six-Core request is not all-or-nothing.

If Core1 is ready while Core2 awaits a verified source-inspection receipt and Core1A/Core1B
await learner routing, the execution packet marks Core1 runnable and keeps the other work
orders waiting.
An unrelated hold does not freeze every Core.

Each work order carries:

- the current product state;
- the action the agent is authorised to take;
- the exact blockers;
- the role-spec path and SHA-256;
- the role's parsed required fields;
- the canonical target bucket/segment/question inventory;
- a write scope;
- the authority boundary.

## Allowed actions

`BUILD_FROM_CANONICAL`
: Compose product output from existing canonical records. Do not rewrite curriculum truth.

`AUTHOR_CANDIDATE_QUESTION`
: Only for Core2A/Core2B when authored supplements are explicitly allowed. The result must
  remain `CANDIDATE` with `AUTHORED` origin.

`HOLD_SOURCE_CUSTODY`
: Core2 has no authorised source corpus. Core2 is custody and therefore cannot be filled by
  generation.

`HOLD_ARCHITECTURE_ASSET`
: A governing canonical asset is missing. A product author may not invent curriculum
  authority to make the build pass.

`WAIT`
: A named owner or agent input must be resolved first.

`WITHHELD`
: The declared purpose intentionally excludes the product.

## Packet pins

Every packet pins:

- the canonical request digest;
- the matrix digest;
- a digest of the subject library files;
- the verified source-receipt digest, when source-backed products are requested;
- each Core role-spec SHA-256.

`verify()` recompiles the current plan and rejects the packet if any of those inputs or the
per-Core action/state/blocker tuple changed. A stale packet cannot silently keep authoring
against an old architecture.

## Source boundary

Core2 remains source custody. An authored practice candidate may help Core2A/Core2B only
when the owner explicitly permits authored supplements; that candidate does not become
Core2 by being useful.

The six-Core Relative Motion planning fixture therefore remains partial until its supplied
source is inspected. No source sufficiency is invented by this layer.

## Learner boundary

Core1A, Core1B, Core2A and Core2B are learner-routed products. A practice-only request must
still provide learner capability evidence or an explicit owner routing decision/waiver.

A percentage is a coordinate/owner decision, never evidence that prerequisites are held.

## Acceptance

The CI gate runs:

```text
python3 Shared/tools/compile_execution_packet.py --audit --enforce
```

The executable falsifiers are in `tests/test_execution_packet.py`.
