# Agent A — Motion 1D vertical-gravity integration semantic Atlas audit

> Status: **Agent A canonical-content integration packet**
>
> Date: 2026-09-19
>
> Grade9V3 packet: `MATRIX-PHY-KIN-1D-MOTION` / `BUCKET-PHY-KIN-1D-MOTION`
>
> Scope: bounded vertical one-dimensional motion under locally constant gravity.

## Capability decision

**No vertical-motion capability is created.**

The repository already owns the durable academic actions:

```text
CAP-PHY-GRAV-FREE-FALL-G
    local gravitational acceleration / free-fall meaning
                ↓
CAP-KIN-CONSTANT-ACCELERATION
    signed constant-a model and equations
                ↓
CAP-KIN-ZERO-V-NONZERO-A
    turning-point distinction

with:
CAP-KIN-DISTANCE-DISPLACEMENT
CAP-KIN-MOTION-GRAPHS
```

The missing preparation was the integration of these owners under one consistent vertical
coordinate model.

The packet therefore introduces:

```text
CTX-PHY-KIN-VERTICAL-GRAVITY
        application context

FAM-PHY-KIN-VERTICAL-GRAVITY
        stable demand / solution structure
```

Neither becomes learner mastery state or a prerequisite node.

## Why this packet now

The owner-approved ExamSIDE Motion-in-a-Straight-Line reconnaissance explicitly identifies
vertical motion under gravity and turning-point reasoning as preparation demand.

That reconnaissance also states that the current Motion-1D capability spine is structurally
strong and does **not** justify a new production capability.

The correct repair is therefore to make the existing cross-capability route explicit and
practisable.

## Two consequential semantic actions

### `KIN4-6` — signed local gravity

For a bounded region where local `g` is treated as constant:

```text
g > 0  = magnitude

choose +up:
    a = -g

choose +down:
    a = +g
```

The acceleration sign belongs to the coordinate representation and the physical downward
direction of gravity. It does not flip merely because the object changes from rising to
falling.

This action also preserves the Gravitation boundary: the familiar constant local `g` is a
bounded approximation, not a claim that one numerical value of `g` applies everywhere.

### `KIN3-4` — apex event condition

At a vertical turning point:

```text
v = 0
a != 0
```

The zero velocity is an instantaneous event condition. The gravitational acceleration remains
downward through the event.

A learner who sets both `v=0` and `a=0` has a conceptual turning-point failure, not an
algebra error.

## Practice inventory

The packet adds five Core2A items:

1. upward launch: derive `t_top=u/g` and `H=u^2/(2g)`;
2. release from height with +up: future impact time and negative impact velocity;
3. return to launch level: distinguish zero displacement from nonzero distance and recover
   return velocity `-u`;
4. repeat free fall with +down to make coordinate dependence explicit;
5. apex witness: positive velocity -> zero -> negative velocity while acceleration remains
   `-g` under +up.

These are representative uses of existing capabilities, not new permanent skills.

## Transfer inventory

The packet adds five Core2B items.

### Representation translation

The same upward throw is solved with +down instead of +up. Directed quantities change sign,
while physical top time and maximum height do not.

A second item translates the flight into a velocity-time graph: one straight line of slope
`-g`, crossing zero at the apex and continuing through the descent.

### Reasoning steps

A balcony launch changes the origin and creates two algebraic time roots. The learner must keep
the signed gravity model fixed and select the root corresponding to the future impact.

An intermediate-height item uses `v^2` to show that the ball has equal speed but opposite
velocity on ascent and descent.

### Model choice

A diagnostic item presents the common rule:

```text
rising  -> a=-g
falling -> a=+g
```

while keeping +up fixed. The learner must reject that switch because neither the axis nor the
physical gravity direction changed.

The model-choice hint remains conceptual.

## Stable academic boundaries

### Gravity magnitude versus signed acceleration

`g` is used as a positive local magnitude in this packet. The signed acceleration is produced
only after the axis is declared.

### Velocity direction versus acceleration direction

For +up:

```text
ascent:   v > 0, a = -g
apex:     v = 0, a = -g
descent:  v < 0, a = -g
```

This is one continuous constant-acceleration model, not three separate phases requiring three
gravity signs.

### Displacement versus distance

A return to the launch point has:

```text
whole-trip displacement = 0
whole-trip distance > 0
```

The constant-acceleration equations use signed displacement; path-length questions require the
separate distance concept.

### Same height versus same velocity

At one intermediate height visited twice:

```text
same position
same speed magnitude
opposite velocity signs
```

The squared-velocity relation determines a magnitude before motion direction supplies the sign.

## Deliberate exclusions

This packet does **not** add:

- a vertical-motion capability;
- a free-fall-sign capability;
- air resistance or terminal velocity;
- large-altitude varying-`g` motion;
- calculus/variable-acceleration methods;
- two-dimensional projectile motion;
- a universal claim that `g=9.8 m/s^2` everywhere.

Those are different models or depths.

## School-scope boundary

The machine-readable Terminal-1 sheet may now state that local vertical-motion preparation is
`LOCAL_READY_WITH_BRIDGE`.

It must still retain:

```text
school_micro_demand = MICRO_TO_CONFIRM
```

because the chapter title does not prove that this specific microtopic is on the learner's
school assessment.

## Stop condition

The vertical-gravity route is now fine enough to distinguish the consequential failures
supported by current evidence:

- wrong axis/sign setup;
- acceleration-sign flip at direction reversal;
- apex `v=0 -> a=0` misconception;
- displacement/distance confusion;
- wrong algebraic event/root interpretation;
- equation/graph representation mismatch.

Further vertical-motion decomposition should wait for learner evidence or a separately approved
demand family that cannot be expressed by these existing owners.
