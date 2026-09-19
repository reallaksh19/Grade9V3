# Agent A — NLM connected systems / ideal-string constraints semantic Atlas audit

> Status: **Agent A canonical-content packet**
>
> Date: 2026-09-19
>
> Grade9V3 packet: `MATRIX-PHY-NLM-FIRST-LAW` / `BUCKET-PHY-NLM-FIRST-LAW`
>
> Scope: connected-body common acceleration (R9), ideal-string tension (R10), and the
> bounded one-fixed-pulley string-length constraint (R11).

## Ownership boundary

This packet changes subject-owned academic meaning only:

- `Physics/library/phy-nlm-first-law.v1.json`;
- `Physics/matrices/phy-nlm-first-law.rungs.json`;
- subject-focused tests and this audit.

It does not change Shared schemas, routing, learner state, diagnostic vocabulary, Core
selection, or the Topic Atlas runtime.

Friction remains a separate canonical owner. It can appear as a prerequisite or secondary
context in a connected-body problem, but this packet does not reopen the friction packet.

## Durable capability decision

The existing three capabilities remain the correct permanent decomposition:

```text
active fixed-separation constraint
        ↓
CAP-NLM-CONNECTED-COMMON-ACCEL
        ↓
body / subsystem / whole-system Newton-II equations

ideal string/redirection force model
        ↓
CAP-NLM-IDEAL-STRING-TENSION
        ↓
body-specific tension arrows + one T only when licensed

fixed-pulley inextensible-string geometry
        ↓
CAP-NLM-SINGLE-STRING-CONSTRAINT
        ↓
signed displacement / velocity / acceleration relation
```

No new capability is created for contact loss, system-boundary choice, Atwood machines,
tension-versus-weight, or separating tension equality from the length constraint.

## Why the three owners must remain distinct

These three ideas often occur in one problem but they answer different questions.

**Common acceleration** is conditional on an active physical constraint that fixes relative
separation. It is withdrawn when the contact/connector can no longer enforce that condition.

**Equal tension** is a force-transmission result of the declared ideal string/redirection
model. It says nothing by itself about whether a hanging body is in equilibrium; the tension
magnitude must still satisfy that body's Newton-II equation.

**The fixed-pulley acceleration relation** is kinematic. It comes from constant string length
and the actual changing segments. Equal tension is not its proof.

That distinction is now explicit enough that diagnostics can route a learner to the failed
claim instead of treating every string/pulley error as one generic "connected bodies" mistake.

## Stable semantic leaves

### R9 — connected bodies / common acceleration

- `NLM9-1` — identify the active condition fixing relative separation;
- `NLM9-2` — use one compatible sign convention and assign the constrained acceleration;
- `NLM9-3` — write body-specific Newton-II equations with interaction forces retained;
- `NLM9-4` — cancel internal partner forces only after forming a combined system;
- `NLM9-5` — choose the system boundary for the target: whole system for shared acceleration,
  body/subsystem when an internal interaction force must be exposed.

The packet also makes explicit that equal acceleration does **not** imply equal net force:
`F_net,i = m_i a` can differ when masses differ.

### R10 — ideal-string tension

- `NLM10-1` — declare the ideal string/redirection assumptions;
- `NLM10-2` — place each string-on-body force on the correct FBD;
- `NLM10-3` — use one common tension magnitude only while the ideal assumptions hold;
- `NLM10-4` — refuse equal tension when the force-transmission model is broken;
- `NLM10-5` — solve tension from Newton II rather than replacing it automatically by
  `mg` or by another applied force.

For an upward-positive hanging body, the diagnostic relation is `T - mg = ma_y`. Thus
`T=mg` is the zero-vertical-acceleration special case, not the definition of tension.

### R11 — one fixed-pulley string constraint

- `NLM11-1` — declare one fixed-pulley geometry and coordinates;
- `NLM11-2` — build the changing string length from the geometry;
- `NLM11-3` — derive velocity/acceleration constraints from constant length;
- `NLM11-4` — translate signed results back into physical motion;
- `NLM11-5` — keep the length-derived kinematic relation separate from equal-tension
  force modelling.

The bounded result remains `a_A + a_B = 0` only for the declared one-fixed-pulley
two-changing-segment geometry and sign convention.

## Misconception coverage

The packet now distinguishes these failure routes:

- touching/connected bodies automatically share acceleration even after the constraint is lost;
- same acceleration means the same net force on each body;
- an interaction force can be cancelled from an individual-body FBD because it is internal
  to a larger possible system;
- the two end tensions cancel because they are equal;
- every rope/pulley permits one common tension;
- a hanging body's tension is always its weight;
- every pulley uses one memorized acceleration ratio;
- opposite sides of a fixed pulley have the same signed acceleration;
- equal tension is what causes the fixed-string acceleration constraint.

These errors require different repair actions despite sharing a broader Laws-of-Motion context.

## Practice and transfer inventory

When filtered by **primary capability** across R9-R11, the packet now has five Core2A and
five Core2B items.

Core2A covers:

- two-block maintained-contact acceleration/contact force;
- ideal-string two-cart acceleration and tension;
- fixed-pulley length/velocity/acceleration relation;
- maintained contact versus contact loss as a common-acceleration validity check;
- an ideal Atwood system deriving both acceleration and tension while showing
  `T\neq mg` during acceleration.

Core2B covers:

- choosing/changing the system boundary in a three-cart problem;
- rejecting equal tension after a nonideal pulley assumption is introduced;
- reconstructing a fixed-pulley length relation from a changed verbal coordinate
  representation;
- rejecting common acceleration when an ordinary contact cannot maintain separation;
- preserving the fixed-length acceleration relation while refusing equal tension after the
  force-transmission idealization is broken.

The five transfer items span the existing `reasoning_steps`, `model_choice`, and
`representation_translation` dimensions. Model-choice hints are concept-only.

## Key cross-capability boundary

The new qualitative boundary item deliberately changes only the pulley force model while
holding a fixed, taut, inextensible, no-slip string geometry.

Under that stated boundary:

```text
fixed string length still justifies:
    a_A + a_B = 0

but the packet no longer licenses:
    T_A = T_B
```

No torque equation or pulley-inertia calculation is introduced. The purpose is to test whether
the learner can keep a kinematic claim after the independent force-model claim is withdrawn.

## Matrix sharpening

R9 now requires both an active-constraint failure case and a target-driven system-boundary
choice.

R10 now requires a hanging-body case where tension differs from weight because acceleration is
nonzero.

R11 now requires explicit separation of the fixed-length acceleration constraint from the
equal-tension idealization.

Each rung has a third controlled variation exposing the corresponding learner decision.

## Boundaries retained

This packet deliberately does **not** add:

- movable or compound pulley acceleration ratios;
- a pulley-count formula catalogue;
- rotational dynamics or torque calculation;
- massive-rope dynamics;
- elastic-string dynamics;
- wedge constraints;
- a general many-body-chain formula;
- a separate Atwood capability;
- a separate tension-versus-weight capability;
- friction re-authoring.

A nonideal pulley may appear only as a **model-boundary test**: the packet can refuse an
equal-tension assertion without manufacturing the missing rotational dynamics.

## Stop condition

R9-R11 now expose the consequential learner decisions separately:

- is the constraint still active?
- which system boundary exposes the requested quantity?
- what assumptions license one common tension?
- what does Newton II actually make the tension magnitude?
- which claim comes from force transmission and which from fixed-length geometry?

Further decomposition should wait for learner evidence showing a different recurring failure
that would change the repair.

The next Agent-A packet should move to another incomplete Laws-of-Motion or Grade-9 Physics
area rather than creating more pulley/string IDs.
