# Physics depiction census — measurement before design

This is the measurement checkpoint for the representation redesign. It is intentionally
committed before schema, renderer, adapter, or gate changes.

## Population and counting rule

Population: the 12 imported packets in `Physics/candidates/*.v1.json` plus the two
committed packages in `Physics/library/`: **14 packages total**.

A count below is **package incidence**: a package counts once when its authored content
explicitly teaches at least one quantity of the kind, or explicitly requires the named
primitive to make one of its authored claims visible. This avoids manufacturing quantity
records that the imported packets do not yet contain. Candidate packets remain
`packet_authority: NONE`; this document classifies what they already say and grants no
content authority.

## Quantity-kind census

| physical quantity kind | packages | incidence |
|---|---:|---|
| `SCALAR` | **14 / 14** | every surveyed package teaches a scalar quantity, scalar component, magnitude, or scalar relation |
| `POLAR_VECTOR` | **11 / 14** | electricity, fluids, gravitation, kinematics, magnetism, Newtonian mechanics, rotation, vector mechanics, work/energy, relative motion, committed vector representation |
| `AXIAL_VECTOR` | **4 / 14** | gravitation (`L`, torque), magnetism (`B`), rotation (`L`, torque, angular velocity), vector mechanics (cross-product result) |

No fourth physical quantity kind is required by the surveyed teaching surface. In
particular, the packets do not require a tensor-valued teaching object: the rotation
packet teaches fixed-axis moment of inertia as a scalar. A future tensor packet would be
new evidence and must change this census rather than being anticipated here.

## Primitive demand census

This is a conservative count of primitives needed to make claims that are already
explicit in the surveyed material. A package may need more than one primitive.

| primitive | packages waiting / using | count |
|---|---|---:|
| `TYPESET_EXPRESSION` | all 12 candidate packets + both committed packages | **14** |
| `ARROW_FIELD` | electricity, fluids, gravitation, kinematics, magnetism, Newtonian mechanics, rotation, vector mechanics, work/energy, relative motion, committed vector representation | **11** |
| `DIRECTED_PATH` | fluids (streamline), gravitation (orbit), kinematics (trajectory), optics (ray), work/energy (integration path) | **5** |
| `CARTESIAN_PLOT` | electricity (I–V characteristic), kinematics (trajectory relation), oscillations (time dependence), thermodynamics (closed P–V cycle) | **4** |
| `MARKED_AXIS` | kinematics (signed one-dimensional position/motion) | **1** |
| `NODE_NETWORK` | electricity (junctions, sources and resistors) | **1** |
| `LEVEL_COMPARISON` | work/energy (before/after scalar energy accounting) | **1** |

The count is demand, not implementation status. It does not claim that the candidate
packet has authored the scene instance needed to satisfy the demand.

## Where the proposed taxonomy was wrong

The proposed eight-item list mixed three different axes and therefore cannot be the
quantity-kind enum.

- `state` is a tuple/projection of scalar quantities. The thermodynamics packet's
  `(P, V, T)` does not become a new physical quantity category because it is viewed in
  state space.
- `field sample` is sampling/cardinality. In the magnetism packet, the sampled `B` values
  are axial vectors; in an electric-field packet sampled `E` values would be polar
  vectors.
- `path` is depiction structure. A ray, streamline, orbit or trajectory carries
  positions/directions; it is not itself a physical quantity category.
- `network node` is topology/entity structure, not a quantity.
- `conserved scalar` is `SCALAR` plus a conservation invariant. Conservation is a claim
  to check, not a new dimensional/category kind.

This matters mechanically: those five labels overlap the first three instead of
partitioning them. Counting them as peer kinds would allow the same quantity to acquire
multiple incompatible `kind` values.

## Measurement conclusion

**Measured base quantity kinds: 3. Surveyed packages: 14. Primitive families demanded:
7.** The representation design must therefore keep physical category separate from
view/topology/invariant. This document records that finding only; the schema and seam are
separate changes that follow it.
