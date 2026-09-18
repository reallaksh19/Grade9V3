# Capability delivery across subject/provider boundaries

Prerequisite topology and capability delivery answer different questions.

- **Prerequisite topology:** what must be known before a target capability?
- **Delivery resolution:** where can that required capability be taught or verified?

A capability with no local matrix rung is therefore not automatically missing. If its
canonical record declares an external provider, the route keeps it as an explicit bridge.

## Delivery states

| State | Meaning |
|---|---|
| `LOCAL` | exactly one canonical local teaching location exists |
| `EXTERNAL_BRIDGE` | no local location exists and the capability declares an external provider |
| `UNRESOLVED` | no local location and no external provider exist |
| `AMBIGUOUS` | more than one canonical teaching location exists |

The Shared resolver is `Shared/tools/capability_delivery.py`. Subject-specific callers
must not reimplement these semantics.

## Route validity versus readiness

A route may be structurally valid while still requiring an external bridge.

```text
valid = no unknown capability / cycle / unresolved delivery / ambiguity
ready = valid and no unsatisfied external bridge remains
```

For compatibility, `passed` currently means structural validity. Callers that intend to
start learner execution must inspect `ready`.

An external bridge is reported in `blockers`, not `findings`. A missing capability with
no provider remains a finding and makes the route invalid.

## Learner evidence

The learner-facing planner resolves bridge need without mutating canonical subject truth:

- external capability + `DEMONSTRATED` prerequisite → `SKIP`;
- external capability + `DEMONSTRATED` direct worksheet demand → `QUICK_CHECK`;
- external capability + `UNCERTAIN` or `MISSING` → `BRIDGE`;
- external capability + no evidence → `BRIDGE`, with the provider asked to verify first
  rather than teach more than necessary.

Owner estimates remain local matrix-start hints only and never satisfy an external bridge.

## Boundary rule

This mechanism must not create local copies such as `*-BRIDGE`, `*-LOCAL` or
`*-PREREQ` merely to make routing convenient. One skill should keep one capability
identity. A consuming subject may depend on it; the owning/provider subject supplies or
verifies it.

The current `external_provider` and `acceptance_status` fields are sufficient for this
routing distinction. A provider-capability registry should be added only if a real case
shows that naming the provider subject is insufficient to locate the supplied material.
