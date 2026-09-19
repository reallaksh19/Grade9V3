# G9-5 Sound authoring audit

> Matrix: `MATRIX-PHY-SOUND`
>
> Result: **retain the existing five-rung Grade9V3 spine and copy/adapt only the durable acoustics invariants missing or under-specified locally.**

## Donor-first finding

The prior acoustics engineering record is much broader in authority metadata but not broader in learner actions than the current Grade9V3 Sound package.

Therefore no new capability is added.

Useful donor semantics copied and adapted locally:

- sound is mechanical and requires a material medium;
- compression = locally higher density/pressure and rarefaction = lower density/pressure;
- local particle oscillation is parallel to propagation in the simple longitudinal-fluid model;
- `v=fλ` belongs to one wave in one medium/state;
- reflected-sound ranging uses the full outward-and-return path;
- forgetting the factor of two is a primary echo-calculation failure.

## Deliberate rejection of donor wording

The donor also encoded a fixed “minimum echo distance” based on a memorized 0.1 s delay and one air sound speed.

That is **not** copied into Grade9V3 as a universal law.

Grade9V3 keeps the durable invariant:

```text
round-trip path = v * delay
one-way range = v * delay / 2
```

and treats whether a reflected return is heard as a distinct echo versus reverberation as condition-dependent.

This is a concrete example of copy-with-adaptation rather than schema/claim transplantation.

## Capability mapping

```text
source vibration + medium → CAP-SOUND-SOURCE-MEDIUM
longitudinal pattern       → CAP-SOUND-LONGITUDINAL
wave quantities            → CAP-SOUND-WAVE-QUANTITIES
pitch/loudness/hearing     → CAP-SOUND-PERCEPTION
reflection/ranging         → CAP-SOUND-REFLECTION
```

No donor gate ID is retained in runtime records.

## Scope filtering

Not copied:

- a universal hard echo threshold;
- acoustic impedance;
- standing-wave/interference formulae;
- Doppler effect;
- logarithmic decibel models;
- donor readiness/release claims;
- donor curriculum authority.

## G9-5 disposition

```text
existing five-rung Sound matrix
+ prior acoustics engineering
→ enrich representation/model invariants
→ reject over-specific echo threshold
→ no new capability
→ readiness/regression/guardrails
→ G9-6 next
```
