# G9-4 Work, Energy and Power authoring audit

> Matrix: `MATRIX-PHY-WORK-ENERGY-POWER`
>
> Result: **retain the existing seven-rung Grade9V3 spine and copy/adapt the durable missing semantics from the owner's prior Work/Energy engineering corpus.**

## Donor-first finding

The local Grade9V3 package was already strong: it had signed work, net-work/kinetic-energy change, potential-energy eligibility, conditional mechanical-energy conservation, power, derivations and quantitative closure.

The prior engineering corpus did **not** justify new learner capabilities. Its important reusable delta was:

- declare one analysed object/system and interval before work/energy calculation;
- keep force/displacement geometry attached to the same body/event;
- treat the constant-force work expression as a scoped model;
- declare a system boundary and energy stores/transfers before conservation;
- distinguish total-energy conservation from conditional mechanical-energy conservation;
- show dissipation/transfer explicitly instead of saying energy is destroyed;
- keep frame and potential-energy reference consistent;
- verify units, sign, model validity and limiting cases.

Those semantics are copied and adapted locally. No donor runtime/source link is retained.

## Capability decision

No new capability was added.

The donor's broad Work/Energy gates map cleanly onto the existing local capabilities:

```text
work geometry            → CAP-WEP-WORK-DIRECTION
net work / ΔK            → CAP-WEP-NET-WORK-SIGN
potential eligibility    → CAP-WEP-POTENTIAL-ELIGIBILITY
system/conservation test → CAP-WEP-MECH-ENERGY-CONDITION
power                    → CAP-WEP-POWER-RATES
derivation               → CAP-WEP-ENERGY-DERIVATIONS
quantitative closure     → CAP-WEP-GRADE9-QUANT
```

## Main adaptation

R4 is strengthened from “check for friction” into the reusable model-choice sequence:

```text
declare physical system + states
→ inventory K/U stores and transfers
→ identify non-conservative/dissipative transfer
→ use Δ(K+U) accounting when transfer exists
→ simplify to K_i + U_i = K_f + U_f only when extra transfer is zero
→ verify reference/sign/units
```

This preserves the critical distinction:

```text
energy is conserved
≠
mechanical K+U is always constant
```

## Scope filtering

Not copied into the Grade-9 core:

- variable-force integration;
- spring/elastic energy formulae;
- Noether/Lagrangian or microscopic dissipation models;
- donor release/readiness claims;
- donor historical curriculum authority.

## Authority boundary

All records remain local Grade9V3 `CANDIDATE` records with local `source_refs`.
The donor supplied reusable Physics semantics only.

## G9-4 disposition

```text
existing seven-rung WEP matrix
+ richer prior internal engineering
→ enrich existing capabilities/microtopics
→ no duplicate capability
→ no higher-grade pull-down
→ readiness/regression/guardrails
→ G9-5 next
```
