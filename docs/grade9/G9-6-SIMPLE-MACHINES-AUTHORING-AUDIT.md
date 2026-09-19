# G9-6 Simple Machines authoring audit

> Matrix: `MATRIX-PHY-SIMPLE-MACHINES`
>
> Result: **retain the existing three-rung local Grade9V3 spine; no suitable dedicated mature donor record exists, so do not force a donor dependency or invent a replacement.**

## Donor-first search result

The mature prior Physics corpus was searched for simple machines, mechanical advantage, levers, pulleys and inclined planes.

No dedicated reusable Physics engineering record comparable to the Gravitation, Work/Energy or Sound donors was found.

The donor-adaptation policy therefore resolves to:

```text
search donor
→ no useful dedicated donor
→ use current Grade9V3 canonical content
→ compare against current Grade-9 scope
→ repair only real local gaps
```

No cross-repository link is created.

## Current local capability spine

| Rung | Capability | SCOPE_REASON | Decision |
| --- | --- | --- | --- |
| R1 | `CAP-MACHINE-TRADEOFF` | `PREREQUISITE` / curriculum-derived support | Keep; connects Work/Energy to machine behavior and blocks free-energy reasoning |
| R2 | `CAP-MACHINE-MA` | `SYLLABUS_REQUIREMENT` | Keep; mechanical advantage is the direct quantitative learner action |
| R3 | `CAP-MACHINE-COMPARE` | `SYLLABUS_REQUIREMENT` | Keep; lever/pulley/inclined-plane setups are compared through one reusable input-output framework |

The existing decomposition is sufficient. No lever-story, pulley-story or ramp-story capability is added.

## Smallest correction

The existing R1 already owned the ideal force-distance work tradeoff. The missing durable boundary was that learners can overgeneralize:

```text
ideal input work = useful output work
```

into a claim about every real machine.

R1 is therefore strengthened to distinguish:

```text
ideal lossless model
→ F_effort d_effort = F_load d_load

real lossy machine
→ input work may exceed useful output work
→ losses transfer energy to other stores
→ no free energy
```

No efficiency formula is introduced in this Grade-9 pass.

## Deliberately not added

- torque/moment equations;
- pulley-count formula catalogues;
- velocity-ratio formulae;
- efficiency formulae;
- device-specific capabilities;
- higher-grade mechanics;
- donor metadata or donor release authority.

## Authority boundary

The package remains local and `CANDIDATE`; exact curriculum authority remains outside the matrix/package itself.

## G9-6 disposition

```text
donor search
→ no useful dedicated donor
→ retain local 3-rung spine
→ strengthen ideal-vs-real model boundary
→ readiness/regression/guardrails
→ Grade-9 Physics authoring pass complete
```
