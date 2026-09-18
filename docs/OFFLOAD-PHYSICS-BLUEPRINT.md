# Offload brief — the Physics blueprint core

A standalone brief. Everything needed to start is here; nothing needs to be re-derived.

---

## 1. What this repository is

A six-Core learner-material production system for Physics, Mathematics and Chemistry,
grades 9–11, aimed at CBSE and IIT-JEE. Six products per subtopic bucket:

| | |
|---|---|
| Core1 | compact orientation notes — the map of the bucket |
| Core2 | source question custody, preserved verbatim |
| Core1A | declarative teaching, construction completed and visible |
| Core1B | conceptual self-tutor — elicits the decision before revealing it |
| Core2A | supported practice with full solution breakdowns |
| Core2B | application and transfer |

A subject-neutral engine compiles a library of records into publishable products. Subject
vocabulary enters only through `<Subject>/adapter/`, and a guard refuses a subject name in
`Shared/`.

**Standing rules, non-negotiable:**

- A blueprint is never adjusted for a specific case. Fixes go in through logic that holds
  globally, and the **engineering gate outranks the blueprint**.
- **Fail closed.** A claim must be backed or must say why it is not. Silence is not
  expressible: a product that omits a required element must be distinguishable, from the
  page, from one that has it.
- **Measure, gate non-enforcing, fix the data, then enforce.** Every commit green.
- **A gate that would have passed the defect it was built to catch proves nothing.** Write
  the falsifier first and show it failing.
- **Never invent content to satisfy a gate.** An absent field is reported, never filled.

---

## 2. The problem, already measured — do not re-derive

The repo isolated **topic**. It never isolated **representation**. Drawing lives in
`<Subject>/adapter/scenes.py`, so a *geometry* is owned by whichever subject needed it first.

**The same geometry, declared under different names, built once or never:**

| Geometry | Declared as | Built |
|---|---|---|
| points over an x-y frame | `GRAPH` (Phy), `FUNCTION_PLOT` (Math), `ENERGY_PROFILE` (Chem) | once, in Physics; the other two cannot reach it |
| marked points on one axis | `NUMBER_LINE` (Math) | once, in Maths; Physics 1D motion and Chemistry pH cannot reach it |
| labelled arrows in an equal-scale frame | `VECTOR`, `VECTOR_SUBTRACTION`, `FREE_BODY_DIAGRAM` (all Phy) | twice, third pending |

**32% of each subject's scene module is pure geometry** — coordinate mapping, scale,
labels, arrowheads. Measured independently in both; the same fraction in each.

**The equation layer is already broken the same way.** `relation.mathml` is a
hand-authored string beside `relation.expression`. Nothing compares them, which is the
same "two authorities for one claim" defect the A4 gate exists to prevent, one layer down.
**2 of 5 committed relations have empty `mathml`** and `_orientation_blocks` skips them
silently, so that mathematics is typeset for no learner and no gate says so.

**Known masking bug to fix, not to work around:** `relation.expression` is marked
`[derived]` in `Shared/roles/CORE1.md`, which waives the delivery check. That marker is
what hides the empty-`mathml` case. A `[derived]` marker must require that the field it
derives *to* exists.

---

## 3. The two halves

### WHAT — topic / subtopic

Already modelled and working. A `bucket` holds `microtopics`; each microtopic has an
entry assumption, an inferential jump, a teaching path of steps, misconceptions, an
elicitation cycle and an exit task with an oracle. Gates enforce substance, authority,
step quality and A/B differentiation. **This half is not the problem.**

### HOW — representation

Owned by subjects, duplicated, and enumerated by *diagram name* rather than by anything
structural. This is the half to redesign.

---

## 4. The design question

> **How do you design a blueprint core that works across scenarios, rather than a list of
> diagram types that grows by one every time a new subtopic arrives?**

### The proposed answer, to be tested rather than assumed

**Bind WHAT to HOW through the *quantity*, not through the topic name.**

A subtopic declares the quantities it teaches. Each quantity has a **kind**. The kind
determines which depiction primitive can carry it and which invariants must hold. **The
diagram type is derived, not declared.**

This is the same move the repo already made for mathematics: the engineering gate owns the
relation, the library teaches it. Here, a quantity model owns what can be drawn, and a
subtopic says which quantities it uses.

**Candidate quantity kinds** — derive these from the twelve packets in
`Physics/candidates/`, do not accept this list as given:

| Kind | Example | Carried by |
|---|---|---|
| scalar | mass, temperature, resistance | marked axis, plot |
| polar vector | velocity, force, field strength | arrow field |
| axial vector | torque, angular momentum | arrow field **with rotation sense** |
| state | (P, V, T) point on a plane | plot, including closed cycles |
| field sample | B at several positions | arrow field over a grid |
| path | a ray, a trajectory | directed path with interaction points |
| network node | a resistor, a junction | node network |
| conserved scalar | energy before/after | level comparison |

**Candidate primitives**, all subject-neutral, all in `Shared/`:
`MARKED_AXIS`, `CARTESIAN_PLOT`, `ARROW_FIELD`, `DIRECTED_PATH`, `NODE_NETWORK`,
`LEVEL_COMPARISON`, `TYPESET_EXPRESSION`.

### What the geometry cannot know — and Physics must state

This is where the brief earns its keep. A primitive draws; it cannot know any of this:

- **Frame.** Every vector is read in a declared frame. Relative motion is the whole
  subject of one existing bucket, and a figure without a frame is unreadable.
- **Dimension.** Two different dimensions must not share one equal-scaled axis.
- **Sign convention.** Declared before use, never inferred from the data.
- **Out of plane.** A 3D vector shown on a 2D page needs an explicit into/out-of-page
  convention. Magnetism and torque both need it; nothing in the repo has it today.
- **Axial versus polar.** A torque drawn as an ordinary arrow teaches something false
  about how it behaves under reflection. The distinction is physical, not decorative.
- **Balance.** If a diagram claims equilibrium, the arrows must sum to zero — and the
  figure should check it, not assert it.
- **Conservation.** If a quantity is claimed conserved, before must equal after.
- **Category.** A scalar drawn as an arrow is an error the geometry will happily render.

The existing `VECTOR_SUBTRACTION` renderer shows the pattern to follow: it **reads its
resultant from declared data and checks it against the operands**, so the figure is an
oracle rather than an illustration. Every primitive should be able to refuse a scene that
cannot show what it exists to show.

---

## 5. What to produce

Sequence it the way this repo works — measure, gate, fix, enforce.

1. **Measure.** Across the twelve candidates in `Physics/candidates/` and the two
   committed buckets in `Physics/library/`: which quantity kinds actually occur, how
   often, and which primitive each needs. Publish the count before proposing anything.
   Expect the taxonomy above to be wrong somewhere — say where.
2. **Schema.** A quantity model on the library record. What kind, what frame, what
   convention, what dimension. All optional at schema level; absent is legal, absent and
   needed is a finding.
3. **The seam.** `Shared/depiction/` holds primitives. An adapter declares a
   *composition* — primitive plus the subject invariants — and contains no drawing code.
   Extend the topic-independence guard to refuse drawing code in an adapter; that is
   mechanically checkable exactly as subject names are.
4. **Migrate** the four existing renderers behind the seam with **composed output
   byte-identical**, proven against the previous commit, exactly as the Core1A check was
   done in R3.1.
5. **`TYPESET_EXPRESSION`** derives MathML from the gate-owned `expression` instead of
   accepting a second hand-authored copy. This is the half actively losing content today.
6. **Then** `FREE_BODY_DIAGRAM` becomes a composition rather than a new renderer, and the
   force bucket is authorable.

## 6. Exit evidence

- The quantity-kind census is committed as a number before any design lands.
- No adapter contains drawing code, enforced by the guard.
- The four existing renderers produce byte-identical output through the new seam.
- Every relation with an `expression` reaches Core1 typeset; a relation that would render
  nothing is a finding, not a silent skip.
- A planted scene that violates a physics invariant — a scalar as an arrow, forces claimed
  in balance that do not sum to zero, an out-of-plane vector with no declared convention —
  is refused, and each is a separate falsifier.
- `Shared/library/depiction.py --next` ranks the remaining primitives by what is waiting
  on them; today every count is zero, so the ranking must change as content lands.

## 7. Traps — each of these has already caught someone here

- **Do not enumerate diagram names.** That is the defect being fixed. If the design ends
  with a list that grows per subtopic, it has failed.
- **Do not let the adapter keep the geometry.** 32% is the measured duplication; if it
  does not fall, the seam is in the wrong place.
- **Do not fill an absent field.** The importer refuses to, and so must this.
- **Do not trust a marker to excuse a check.** `[derived]` already hid a live defect.
- **Do not prove a renderer against a hand-authored fixture.** Every renderer is proven by
  a scene instance compiled from a library record. This is why `FREE_BODY_DIAGRAM` is
  still unbuilt: Physics holds no force content — `force`, `newton`, `friction` and
  `normal` return zero hits across the library.
- **Watch the frozen port oracle.** `Physics/content/relative-motion-g9/` is hand-authored
  from before the library existed and pins a pre-port basis digest. Its inputs must not be
  rewritten; accept legacy shapes at the engine boundary instead, and say so in a comment.

## 8. Orientation

| | |
|---|---|
| branch | `p0-foundations` |
| plans | `docs/PLAN-R0-R2.md`, `docs/PLAN-R3-R4.md`, `docs/ROADMAP-LEARNER-READY.md` |
| engine | `Shared/publication_host/` — `drawing.py` holds today's shared primitives |
| library gates | `Shared/library/` — `depiction.py`, `authority.py`, `substance.py`, `differentiation.py`, `intake.py` |
| tools | `Shared/tools/` — `spec_conformance.py`, `spec_delivery.py`, `capability_audit.py`, `check_subjects.py`, `topic_independence_guard.py` |
| candidates | `Physics/candidates/` — twelve packets, `packet_authority: NONE`, 204 named gaps |

Run before and after every change:

```
python3 -m unittest discover -s tests -p "test_*.py"
python3 Shared/library/depiction.py --enforce
python3 Shared/tools/spec_conformance.py --enforce
python3 Shared/tools/spec_delivery.py --enforce
python3 Shared/tools/check_subjects.py
python3 Shared/tools/topic_independence_guard.py
python3 Shared/tools/capability_audit.py --enforce
python3 Shared/tools/build_manifest.py --check
python3 Shared/tools/republish.py
```

251 tests pass today and every gate is green. Keep it that way at each commit.
