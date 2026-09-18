# Relative Motion river/boat source audit

This note records how the owner-supplied river/boat links should be used without confusing
practice demand, explanation, scientific checking and source custody.

## Source roles

### Official / stronger scientific and assessment references

- `SRC-NCERT-EXEMPLAR-RIVER` — official NCERT exemplar question 20. It directly exercises
  river-current vector composition, a due-north launch, a direct-opposite crossing, resultant
  speed and a comparison of crossing times.
- `SRC-OPENSTAX-RELATIVE-RIVER` — independent open-textbook treatment of relative motion in
  two dimensions. It explicitly models boat-relative-water plus water-relative-ground to
  obtain boat-relative-ground velocity and includes river-crossing exercises.

These are the preferred scientific/question-demand cross-checks for learner-facing
explanations and adapted practice.

### Owner-supplied supplementary explanation

- `SRC-ANAND-RIVER-BOAT` — useful worked explanation of two different objectives:
  reaching the point directly opposite versus minimizing crossing time. It is retained as
  an explanation source only, not curriculum authority.

### Owner-supplied external practice bank

- `SRC-SCRIBD-DPP8-RIVER-BOAT` — a three-page Physicsaholics DPP mirror containing 14
  river/boat questions plus an answer key. The set spans direct crossing, minimum-time,
  drift/heading choice and harder variable-flow/accelerated-motion cases.

This source is demand evidence only. The repository retains the locator and demand
classification; it must not copy the bank into canonical content or infer scientific
authority from a user-uploaded mirror.

## What the current capability graph can support

The existing Relative Motion spine already supports the core modelling relation:

```text
same-time frame choice
→ relative velocity
→ component / direction check
```

That is enough to explain the ordinary constant-current boat/river composition case and to
diagnose common vector-direction errors.

The stronger river/boat banks also contain additional demands such as optimization by
objective, variable current and time-dependent swimmer motion. Those are **observed demand
gaps**, not permission to widen a capability silently.

Do not add a new canonical capability merely because these sources contain harder problems.
Add one only when an actual learner/session or deliberately selected worksheet needs a
distinct repair target that the current `CAP-RELATIVE-V` / `CAP-VECTOR-CHECK` pair
cannot diagnose cleanly.

## Live-pilot use

For the first Relative Motion live pilot:

1. present the selected external question with no solution material;
2. use current canonical teaching/feedback first;
3. if the learner's failure is specifically about river-crossing objective choice
   (direct-opposite versus minimum-time) rather than relative-velocity construction itself,
   record that as an observed content-gap candidate;
4. only then decide whether a dedicated moving-medium capability is justified.

This preserves the project's rule: real learner evidence should drive the next abstraction.
