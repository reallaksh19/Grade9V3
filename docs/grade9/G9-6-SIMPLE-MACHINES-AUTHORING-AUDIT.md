# G9-6 Simple Machines authoring audit

> Matrix: `MATRIX-PHY-SIMPLE-MACHINES`
>
> Result: **retain the existing three-rung local spine; strengthen the mechanical-advantage rung for the current Grade-9 practical/measurement demand. No new capability is needed.**

## Current scope evidence

The current CBSE Class IX Science (2026-27) Standard syllabus explicitly lists:

- simple machines and their mechanical advantage;
- pulley, inclined plane and lever;
- identifying those simple machines;
- defining and calculating mechanical advantage;
- demonstrating and explaining mechanical advantage;
- a practical for calculating the mechanical advantage of a lever using `M.A. = Load/Effort`.

This is direct current Grade-9 scope, not merely historical placement.

The authored package nevertheless remains `CANDIDATE` with empty curriculum mappings; this
audit does not bypass the repository's curriculum-binding authority.

## Donor search result

The prior Physics engineering corpus used for G9-3 through G9-5 did not provide a useful
dedicated Simple Machines engineering donor.

Therefore G9-6 does **not** invent a pseudo-donor dependency. It reuses the current local
Grade9V3 content and adapts only the missing current-source detail.

## Working-sheet classification

| Rung | Capability | SCOPE_REASON | Decision |
| --- | --- | --- | --- |
| R1 | `CAP-MACHINE-TRADEOFF` | `PREREQUISITE` | Keep the force/distance/direction work tradeoff as the conceptual guard against free-energy reasoning |
| R2 | `CAP-MACHINE-MA` | `SYLLABUS_REQUIREMENT` | Keep and strengthen: define/calculate MA plus same-state lever measurement and fair comparison |
| R3 | `CAP-MACHINE-COMPARE` | `SYLLABUS_REQUIREMENT` | Keep: identify and compare lever, pulley and inclined-plane setups |

## Smallest durable correction

The existing R2 already knew the formula and same-state condition. The current curriculum
also requires learners to demonstrate/explain mechanical advantage and includes a lever
practical.

Rather than creating a new “lever practical capability,” R2 is enriched with:

```text
identify one steady machine setting
→ measure load and effort for that same setting
→ MA = Load / Effort
→ units cancel
→ repeat under one controlled setup change
→ compare separate same-state ratios
```

This is the same learner action—mechanical advantage—not a new capability.

## What is deliberately not added

- no torque/moment equation requirement;
- no pulley-count formula catalogue;
- no velocity-ratio or efficiency formula requirement;
- no story-specific lever/pulley/incline capabilities;
- no grade field in the matrix schema;
- no cross-repository runtime/source link.

## Grade-9 completion

With G9-6 audited, the active Grade-9 Physics pass is complete:

```text
G9-1 Motion                 audited
G9-2 Force/Laws             audited
G9-3 Gravitation            donor-adapted/audited
G9-4 Work/Energy/Power      donor-adapted/audited
G9-5 Sound                  donor-adapted/audited
G9-6 Simple Machines        audited
```

Higher-grade matrices remain untouched under the Grade-9 freeze.
