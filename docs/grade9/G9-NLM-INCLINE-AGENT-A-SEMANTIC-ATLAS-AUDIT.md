# Agent A — NLM inclined-plane integration semantic Atlas audit

> Status: **Agent A canonical-content integration packet**
>
> Date: 2026-09-19
>
> Grade9V3 packet: `MATRIX-PHY-NLM-FIRST-LAW` / `BUCKET-PHY-NLM-FIRST-LAW`
>
> Scope: fixed inclined-plane modelling as a reusable application context for existing vector,
> FBD, Newton-II and friction capabilities.

## Capability decision

**No inclined-plane capability is created.**

That is the central academic decision of this packet.

The durable owners already exist:

```text
CAP-VEC-ANGLE-DECOMPOSITION
        representation conversion
                ↓
CAP-NLM-FBD-BODY-OWNERSHIP
        physical force inventory
                ↓
CAP-NLM-SECOND-LAW
        axis choice + signed component equations
                ↓
CAP-NLM-FRICTION / CAP-NLM-FRICTION-QUANT
        contact direction + state feasibility
```

An incline is a setting in which these reusable actions are combined. It is therefore encoded
as:

```text
CTX-PHY-NLM-INCLINED-PLANE
        application context

FAM-PHY-NLM-INCLINE-MODELLING
        stable demand / solution structure
```

Neither object participates in learner mastery or prerequisite closure.

## Why this packet now

The Terminal-1 working scope still marks school micro-demand as `MICRO_TO_CONFIRM`, so this
packet does not claim school authority from a chapter title.

However, approved ExamSIDE demand already confirms rough/smooth inclined-plane reasoning, and
the previously blocking vector-decomposition preparation is now locally available. The
remaining weakness was integration: the repository owned the component skills but had too
little canonical practice for combining them into a correct inclined-plane model.

## Two consequential setup actions

Two semantic actions are added under existing capabilities rather than promoted into new
skills.

### `NLM3-4` — force inventory versus components

Resolving a force changes its coordinate representation.

It does **not** create additional physical forces.

For example:

```text
physical interaction:
    weight mg

plane-aligned representation:
    mg sin(theta) along the plane
    mg cos(theta) perpendicular to the plane
```

A learner who writes `mg`, `mg sin(theta)` and `mg cos(theta)` as three independent
forces has a representation/ownership failure, not a trigonometry failure.

### `NLM6-4` — constraint-aligned axes

Newton II is coordinate-independent, but axis choice changes the complexity of the setup.

For a block maintained on a fixed plane, parallel/perpendicular axes expose:

```text
Sigma F_parallel = m a_parallel
Sigma F_perp     = m a_perp
a_perp = 0
```

The last line does **not** imply that total acceleration is zero. The block may accelerate
along the plane while remaining constrained perpendicular to it.

## Application-context invariants

The bounded context holds these assumptions unless an authored question changes one
explicitly:

- the plane is fixed;
- the block remains in contact when a contact equation is used;
- axes may be rotated without changing the physical interactions;
- normal reaction comes from perpendicular dynamics;
- friction comes from contact slip/tendency and state, not from a memorized page direction.

The context deliberately excludes moving wedges, rolling-body dynamics, banked curves,
three-dimensional contact geometry and a general constraint-mechanics catalogue.

## Practice inventory

The integration packet has five Core2A items:

1. smooth incline: derive `N=mg cos(theta)` and `a=g sin(theta)`;
2. static rough incline: derive the no-slip condition `tan(theta)<=mu_s`;
3. established downward sliding: derive
   `a=g[sin(theta)-mu_k cos(theta)]`;
4. horizontal push on a smooth incline: show that the applied force changes both tangential
   dynamics and the normal reaction;
5. diagnose the common error of counting weight and its components as separate forces.

These are not five new skills. They are representative integrations of the existing owners.

## Transfer inventory

The packet has five Core2B items spanning the existing transfer vocabulary.

### Representation translation

- compare plane-aligned axes with horizontal/vertical laboratory axes while preserving the same
  physics;
- diagnose weight-component double counting after the error is moved from a picture into
  component equations.

### Model choice

A static-friction item varies an uphill applied force through the value `mg sin(theta)`.
Friction must change from uphill to zero to downhill according to the no-friction slip tendency.
The learner is not allowed to use "friction on an incline points uphill" as a rule.

### Reasoning steps

- a horizontal force on a rough incline changes the normal reaction and therefore the static
  friction bound;
- smooth-versus-rough travel times over the same incline require combining the NLM acceleration
  result with constant-acceleration kinematics.

The latter directly exercises the approved rough-versus-smooth incline demand without copying
the external item.

## Important academic boundaries

### Normal reaction

`N=mg cos(theta)` is a **special case**, not a new universal formula.

With a horizontal force `P` pushing into a plane that rises to the right:

```text
N = mg cos(theta) + P sin(theta)
```

The packet therefore routes normal-reaction errors back to the actual perpendicular force
equation rather than creating a separate "normal reaction skill."

### Static friction

For a horizontal push on a rough incline, uphill positive:

```text
f_required = mg sin(theta) - P cos(theta)

static feasible iff

|f_required|
<=
mu_s [mg cos(theta) + P sin(theta)]
```

The sign of `f_required` determines the friction direction. The absolute-value comparison
determines feasibility.

### Vector ownership

The NLM packet uses `CAP-VEC-ANGLE-DECOMPOSITION`; it does not duplicate vector trigonometry
inside NLM. Vectors owns representation conversion. NLM owns what those components mean in the
chosen body's force equations.

## Deliberate exclusions

This packet does **not** add:

- an inclined-plane capability;
- a normal-force capability;
- a weight-component capability;
- a formula catalogue for every force angle;
- a moving wedge constraint;
- rolling without slipping;
- banked curves;
- multi-body wedge mechanics;
- an alternative trigonometry curriculum.

Those additions would turn a reusable context into a second mastery ontology.

## Stop condition

The fixed-incline integration is now sufficiently expressive to diagnose materially different
learner failures:

- wrong physical force inventory;
- wrong component representation;
- poor axis/setup choice;
- wrong normal-force equation;
- wrong friction direction;
- wrong static/kinetic state;
- correct mechanics but failure to connect the acceleration result to a changed kinematics
  representation.

Further incline authoring should wait for real learner evidence or a new approved demand that
cannot be expressed by these existing owners.

The next Agent-A packet should move to another remaining preparation gap rather than creating
incline-specific capability IDs.
