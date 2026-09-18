# Issue #19 prerequisite minimality audit

Issue #19 says that `prerequisite_refs` must describe **true prior knowledge**, not
"nice to know" sequencing. This pass applies that rule to the owner-extension content
migrated in PR #23.

## Counterfactual test

For each prerequisite edge, ask:

> If this prerequisite capability were missing, could a normally prepared learner still
> learn and successfully demonstrate the target capability without first mastering it?

If the answer is yes, the relationship is not kept as a prerequisite. It may still be a
useful teaching connection, enrichment route, derivation, or question-specific secondary
capability.

This is deliberately a routing test, not a claim that the removed concepts are
unimportant.

## Corrections made

### One-dimensional motion

- `CAP-KIN-MOTION-GRAPHS` now depends only on `CAP-KIN-AVERAGE-RATES`.
  The turning-point concept is an application, not prior knowledge for reading graph axes
  and interval slopes.
- `CAP-KIN-CONSTANT-ACCELERATION` now depends on
  `CAP-KIN-MOTION-GRAPHS`, because its authored success criterion explicitly derives
  the equations from a velocity-time graph.
- `CAP-KIN-UNIFORM-CIRCULAR-MOTION` has no forced turning-point prerequisite.
  Constant-speed circular motion does not require prior mastery of the
  zero-velocity/non-zero-acceleration case.

### Newton-law force reasoning

- `CAP-NLM-FBD-BODY-OWNERSHIP` is foundational and no longer depends on
  `CAP-NLM-FORCES-SUM-ZERO`.
- Friction, Newton II and Newton III continue to depend on FBD body ownership because
  their authored success criteria require assigning forces to the correct body.

### Work / Energy / Power

- `CAP-WEP-WORK-DIRECTION` is foundational inside the WEP spine and has no FBD
  prerequisite. A question that independently requires force identification can map FBD
  as a secondary capability.
- `CAP-WEP-POWER-RATES` depends on work-direction reasoning rather than the
  mechanical-energy-conservation condition.
- `CAP-WEP-GRADE9-QUANT` keeps only
  `CAP-WEP-MECH-ENERGY-CONDITION`. Using the Grade 9 work/energy relations correctly
  does not require first deriving those relations.
- `CAP-WEP-ENERGY-DERIVATIONS` depends on the capabilities actually used in its
  authored derivation route: work-direction reasoning, Newton II and constant-acceleration
  kinematics. Mechanical-energy conservation is not required to derive
  `K = 0.5 m v^2` or the controlled-lift `m g h` expression.

### Simple machines

- `CAP-MACHINE-TRADEOFF` now depends on `CAP-WEP-WORK-DIRECTION`, not the full
  `CAP-WEP-GRADE9-QUANT` capability.
- The simple-machine microtopic itself teaches the ideal force-distance work tradeoff.
  A learner therefore does not have to traverse kinetic-energy derivations, Newton II,
  and constant-acceleration kinematics before learning basic mechanical advantage.

## What was deliberately not changed

This pass does not rewrite pre-existing Gravitation/vector capability graphs or the
existing Mathematics linear-equation capability chain. Those were not introduced by
the current owner-extension migration and should change only when a real worksheet or
separate academic review demonstrates a concrete routing problem.

The audit also does not create a new prerequisite type or Shared-layer contract. The
existing graph remains sufficient; the correction is to make its edges academically
minimal.
