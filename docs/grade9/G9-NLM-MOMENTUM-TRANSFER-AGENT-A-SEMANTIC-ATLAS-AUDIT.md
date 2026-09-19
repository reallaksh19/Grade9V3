# Agent A — NLM momentum-transfer force semantic Atlas audit

> Status: **Agent A canonical-content packet**
>
> Date: 2026-09-19
>
> Grade9V3 packet: `MATRIX-PHY-NLM-MOMENTUM-TRANSFER` /
> `BUCKET-PHY-NLM-MOMENTUM-TRANSFER`
>
> Scope: the explicit-demand, non-default discrete momentum-transfer force extension justified
> by the owner-approved ExamSIDE machine-gun demand.

## Ownership boundary

This packet changes subject-owned academic meaning only:

- `Physics/library/phy-nlm-momentum-transfer.v1.json`;
- `Physics/matrices/phy-nlm-momentum-transfer.rungs.json`;
- subject-focused tests and this audit.

It does not broaden the default NLM capability, change Shared routing, add learner-state
semantics, or turn momentum/impulse into a general Grade-9 chapter.

The extension remains `default_entry_eligible: false`.

## Durable capability decision

The existing single capability remains the correct permanent owner:

```text
CAP-NLM-MOMENTUM-TRANSFER-RATE
```

It owns this bounded learner action:

```text
one inertial frame + sign convention
        ↓
per-item signed momentum change
        ↓
repeated-event rate
        ↓
average force on the item stream
        ↓
opposite launcher recoil
        ↓
balancing holding force when held fixed
```

No additional capability is introduced for machine guns, recoil stories, event-rate conversion,
zero-transfer cases, support reactions, or average-versus-instantaneous interpretation.

## Stable semantic actions

The six semantic leaves are:

- `NLM-MTR-1` — declare one inertial frame and positive direction;
- `NLM-MTR-2` — compute `Delta p_item = m(v_out-v_in)` for one fixed-mass item;
- `NLM-MTR-3` — convert repeated identical changes into an average rate,
  `F_avg = R Delta p_item`;
- `NLM-MTR-4` — distinguish stream force, launcher recoil and external holding force by body;
- `NLM-MTR-5` — verify dimensions and signed directions;
- `NLM-MTR-6` — interpret `R Delta p_item` as an **average repeated-event force**, not as
  the instantaneous or peak force during every moment of an individual launch.

The sixth leaf is a consequential diagnostic boundary. A learner who computes the correct
average but treats it as a constant instantaneous force needs interpretation/representation
repair, not more practice multiplying rate by momentum.

## Misconception coverage

The packet now separates:

- final momentum from final-minus-initial momentum change;
- stream force from launcher recoil;
- recoil from the external holding force;
- bounded discrete-event momentum transfer from rocket/continuously varying-mass dynamics;
- average repeated-event force from an instantaneous or peak force pulse.

The important zero-transfer boundary is also explicit: a nonzero item stream can carry
substantial momentum while producing **zero force from this interaction** if the device does
not change each item's signed momentum.

## Practice inventory

The extension now has five Core2A items:

1. nonzero entry and exit velocities in the same direction;
2. from-rest numerical launcher/recoil/holding-force calculation;
3. finite event count over a time interval converted into a rate;
4. a physical leftward ejection represented in a right-positive coordinate system;
5. average-force calculation followed by an explicit average-versus-instantaneous boundary.

These are all authored Grade9V3 items. The approved ExamSIDE item remains preparation-demand
evidence rather than copied question custody.

## Transfer inventory

The extension now has five Core2B items spanning the existing transfer vocabulary:

- **model choice** — average holding force remains determinable even when projectile
  acceleration time is unavailable, so a direct per-projectile `F=ma` route is not the only
  valid representation;
- **representation translation** — a finite test log and gram mass must be converted into
  event-rate/SI quantities;
- **reasoning steps** — distinguish support-on-launcher from launcher-on-support after the
  stream recoil is already known;
- **model choice** — reject `Rmv_out` when entry and exit momentum are identical;
- **model choice** — accept a pulsed sensor trace as compatible with the same correctly
  calculated average force.

Model-choice hints remain conceptual only.

## Academic boundary

The packet deliberately retains this distinction:

```text
known from repeated-event data:
    average momentum-transfer force

not known without extra temporal data:
    instantaneous force waveform
    peak force
    launch interaction duration
```

This prevents the compact rate relation from claiming more time resolution than the evidence
supports.

Likewise:

```text
Delta p_item = 0
    ↓
F_avg = R Delta p_item = 0
```

even when `R` and the item's carried momentum are nonzero.

## Boundaries retained

This packet deliberately does **not** add:

- collision taxonomy;
- coefficient of restitution;
- impulse-integral instruction;
- force-time integration;
- general momentum-conservation curriculum;
- rocket equation;
- continuous variable-mass dynamics;
- center-of-mass collision methods;
- an instantaneous-force or peak-force capability.

Those are different academic demands and should appear only if later evidence warrants them.

## Stop condition

The explicit momentum-transfer extension is now fine enough to distinguish the consequential
learner failures supported by current evidence:

- wrong momentum state comparison;
- wrong event-rate representation;
- wrong body/force role;
- wrong sign;
- wrong average-versus-instantaneous interpretation;
- wrong model-family expansion into rocket/collision mechanics.

Further momentum decomposition should wait for real learner evidence or a separately approved
question family that cannot be expressed by this bounded capability.

The next Agent-A packet should return to the remaining incomplete Grade-9 Physics preparation
areas rather than expanding momentum breadth.
