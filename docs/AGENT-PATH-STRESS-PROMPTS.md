# Frozen agent-path stress prompts

> Purpose: preserve the exact human prompts used to test whether a future agent follows the
> Grade9V3 architecture rather than improvising its own routing logic.
>
> Evidence class: **system stress/regression only**. These prompts never create learner
> evidence.

The machine-readable source of truth is:

`tests/fixtures/agent_path_stress/cases.json`

The executable replay is:

`tests/test_agent_path_stress_prompts.py`

## How to use these later

For a blind stress test:

1. copy one **Prompt** below exactly;
2. give only that prompt to the agent working in the repository;
3. do not provide the expected path in advance;
4. after the agent responds/acts, compare its decisions with the matching expected path;
5. judge semantic routing, not prose similarity.

A pass means the agent used repository truth and the intended decision boundaries. It does
not require identical wording.

The most important invariant is:

```text
owner knowledge %
    ↓
starting coordinate only
    ↓
prerequisites remain unproven
    ↓
CORE1A / CORE1B keep full rung depth
    ↓
practice support comes from purpose
```

A percentage must never become a mastery claim or a percentage reduction in teaching depth.

---

## APSTRESS-REL-60-TEACH

### Prompt

> Prepare CORE1A and CORE1B for Physics — Relative Motion. Student knowledge estimate: 60%.
> Use it only to select the starting rung and check prerequisites. Use the current canonical
> matrix/library; do not treat the percentage as mastery evidence.

### Expected path

```text
resolve current Relative Motion matrix
→ owner estimate 60
→ conservative floor = R3 at ladder_position 55
→ prerequisite check = CAP-SIGNED-PAIR
→ learner route = READY_WITH_CHECKS
→ CORE1A and CORE1B use the same canonical segment
→ no learner evidence is written
```

Fail the stress test if the agent:

- says the learner has mastered 60%;
- starts at a made-up 60-position rung;
- shortens every explanation to the "remaining 40%";
- assumes the Mathematics prerequisite is mastered;
- chooses separate conceptual targets for CORE1A and CORE1B.

---

## APSTRESS-REL-0-FOUNDATION

### Prompt

> Prepare CORE1A and CORE1B for Physics — Relative Motion. Student knowledge estimate: 0%.
> Use it only as the starting-rung estimate; do not infer that any capability is mastered.

### Expected path

```text
owner estimate 0
→ below first declared coordinate
→ conservative floor policy starts at R1
→ no prerequisite mastery is invented
→ no rung below R1 is invented
```

A 0% estimate is not evidence that the learner is `MISSING` every capability.

---

## APSTRESS-REL-100-TEACH

### Prompt

> Prepare CORE1A and CORE1B for Physics — Relative Motion. Student knowledge estimate: 100%.
> Start from the highest conservative matrix coordinate but still check prerequisites; 100%
> is not proof of mastery.

### Expected path

```text
owner estimate 100
→ highest declared coordinate not above estimate = R5 at 85
→ prerequisite checks:
     CAP-SIGNED-PAIR
     CAP-SAME-TIME
     CAP-RELATIVE-V
→ READY_WITH_CHECKS
```

Fail if 100% silently turns every prerequisite into `DEMONSTRATED`.

This case is intentionally paired with the 0% case so both extremes exercise the same
owner-estimate rule.

---

## APSTRESS-G9-NLM-70-PRACTICE

### Prompt

> Prepare CORE1A, CORE1B and CORE2A for Physics — Newton's first law and free-body diagrams.
> Student knowledge estimate: 70%. CORE2A purpose: PRACTICE. Use the percentage only for
> starting-rung selection, and do not invent a source basis if one was not supplied.

### Expected path

```text
resolve current Grade-9 NLM matrix
→ owner estimate 70
→ R3
→ learner route READY
→ CORE1A / CORE1B same target segment

CORE2A purpose PRACTICE
→ support = medium
→ support is NOT derived from 70%

no source supplied
→ SOURCE_BASIS remains explicit owner input
→ do not invent source custody
```

This case checks that learner placement and practice support remain two different decisions.

---

## APSTRESS-G9-WEP-80-TRANSFER

### Prompt

> Prepare CORE1A, CORE1B, CORE2A and CORE2B for Physics — Work, energy and power. Student
> knowledge estimate: 80%. CORE2A purpose: REVISION. CORE2B purpose: COMPETITION. Use the
> estimate only to choose the initial rung; preserve prerequisite checks and report missing
> source basis instead of guessing.

### Expected path

```text
owner estimate 80
→ R4 at 80
→ prerequisite checks:
     CAP-WEP-WORK-DIRECTION
     CAP-WEP-NET-WORK-SIGN
     CAP-WEP-POTENTIAL-ELIGIBILITY

CORE2A REVISION
→ support = low

CORE2B COMPETITION
→ support = minimum
→ transfer semantics retained

source basis absent
→ SOURCE_BASIS remains explicit
→ no fabricated custody / practice source
```

Fail if the agent uses 80% to choose low/minimum support. The support levels come from the
declared purposes, not from learner placement.

Also fail if CORE2B becomes merely "CORE2A with fewer hints". The transfer decision
structure must remain distinct.

---

## What future agents are being tested for

These cases are designed to expose drift in a future agent even if all code tests still
pass.

The agent should independently recover the following path from the repository:

```text
human prompt
→ resolve subject/subtopic to current matrix
→ inspect current canonical library
→ interpret XX% as OWNER_ESTIMATE
→ conservative floor rung
→ prerequisite checks/bridges
→ same Core1A/Core1B segment
→ practice purpose selects support
→ source custody remains explicit
→ unresolved facts remain owner/agent actions
→ no fabricated learner evidence
```

The agent should **not** need this document to answer the prompt. This document is the
answer key for the person running the stress test.

## Updating the frozen cases

Do not rewrite an old expected path merely because implementation drift made a test fail.

A changed expectation requires a deliberate architecture decision with the same discipline
used elsewhere:

```text
observed reason the old invariant is wrong
→ smallest contract change
→ updated stress case
→ regression proving the new behavior
```

If only content/rung coordinates change legitimately, create a new suite version rather than
silently erasing the historical case. The current suite id is:

`AGENT-PATH-STRESS-V1`


## Command-line replay

The repository also includes a convenience runner:

`tools/run_agent_path_stress.py`

Use it to retrieve a blind prompt without seeing the answer key:

```bash
python3 tools/run_agent_path_stress.py \
  --case APSTRESS-REL-60-TEACH \
  --prompt-only
```

Give that output to the agent being tested.

After the agent has acted, replay the saved machine projection:

```bash
python3 tools/run_agent_path_stress.py \
  --case APSTRESS-REL-60-TEACH \
  --enforce
```

To check every frozen case against current repository truth:

```bash
python3 tools/run_agent_path_stress.py --all --enforce
```

A machine `PASS` means the current planner still resolves the prompt according to the
frozen architecture path. For cases that declare `selected_segment`, the runner also checks
the execution-packet teaching segment, so retained non-default extension rungs cannot silently
re-enter the ordinary route. It does **not** by itself prove that an external agent followed
that path. For an agent audit, inspect the agent's response/PR and compare its actual
decisions against the matching frozen case, especially the `must_not` conditions.

A useful later instruction is:

> Run frozen stress case `APSTRESS-REL-60-TEACH` blind. Execute it from current repository
> truth. After the work is complete, compare the path actually taken against the saved
> expected path and report every deviation. Do not reveal the answer key before execution.


---

## APSTRESS-G9-GRAV-60-TEACH

### Prompt

> Prepare CORE1A and CORE1B for Physics — Universal gravitation, free fall and orbital
> motion. Student knowledge estimate: 60%. Use the estimate only to select the starting
> rung; preserve prerequisite checks across the current Grade-9 gravitation chain and do
> not pull extension-only orbit/energy content into the ordinary teaching route.

### Expected path

```text
resolve current Grade-9 Gravitation matrix
→ owner estimate 60
→ conservative floor = R3W at ladder_position 58
→ prerequisite checks:
     CAP-PHY-GRAV-R1
     CAP-PHY-GRAV-INVERSE-SQUARE
     CAP-NLM-FBD-BODY-OWNERSHIP
     CAP-NLM-SECOND-LAW
     CAP-PHY-GRAV-FREE-FALL-G
→ READY_WITH_CHECKS
→ CORE1A / CORE1B use the same canonical target segment
→ R4/R5 remain extension-only for ordinary Grade-9 routing
```

This case checks a cross-matrix prerequisite without broadening the Gravitation bucket. The
Newton-II dependency remains a prerequisite check; it is not copied into the Gravitation
matrix as duplicate teaching.

Fail the stress test if the agent:

- treats 60% as mastery evidence;
- skips Newton II because its capability is owned by another matrix;
- jumps from the 60% estimate into the R4/R5 orbit/energy extension route;
- creates different conceptual targets for CORE1A and CORE1B.


---

## APSTRESS-G9-WEP-95-DERIVATION

### Prompt

> Prepare CORE1A and CORE1B for Physics — Work, energy and power. Student knowledge
> estimate: 95%. Use the estimate only to select the starting rung. Preserve all
> prerequisite checks needed by the Grade-9 energy-derivation rung, keep the
> constant-acceleration/near-Earth model conditions explicit, and do not turn the
> derivation into a calculus or variable-force treatment.

### Expected path

```text
resolve current Grade-9 Work / Energy / Power matrix
→ owner estimate 95
→ conservative floor = R5D at ladder_position 95
→ prerequisite checks:
     CAP-WEP-WORK-DIRECTION
     CAP-NLM-FBD-BODY-OWNERSHIP
     CAP-NLM-SECOND-LAW
     CAP-KIN-DISTANCE-DISPLACEMENT
     CAP-KIN-AVERAGE-RATES
     CAP-KIN-MOTION-GRAPHS
     CAP-KIN-CONSTANT-ACCELERATION
→ READY_WITH_CHECKS
→ CORE1A / CORE1B use the same canonical target segment
→ keep the algebraic derivation inside its stated model conditions
```

This case is the post-G9-4 checkpoint. It specifically tests the donor-adapted boundary from
PR #79: useful system/model validity is retained, but Grade-9 algebra is not silently
promoted into a universal variable-force derivation.

Fail if the agent treats 95% as mastery, skips the Newton-II/kinematics prerequisite chain,
or broadens the route into calculus/variable-force integration.

---

## APSTRESS-G9-SOUND-95-REFLECTION

### Prompt

> Prepare CORE1A and CORE1B for Physics — Production, propagation, wave quantities and
> reflection. Student knowledge estimate: 95%. Use the estimate only to select the starting
> rung and preserve prerequisite checks. For reflected-sound reasoning, trace the full
> outward-and-return path and do not hard-code one universal echo threshold; keep
> Doppler/interference and other excluded acoustics out of the Grade-9 route.

### Expected path

```text
resolve current Grade-9 Sound matrix
→ owner estimate 95
→ conservative floor = R5 at ladder_position 95
→ prerequisite checks:
     CAP-SOUND-SOURCE-MEDIUM
     CAP-SOUND-LONGITUDINAL
     CAP-SOUND-WAVE-QUANTITIES
→ READY_WITH_CHECKS
→ CORE1A / CORE1B use the same canonical target segment
→ reflected path remains round trip
→ no universal echo threshold is invented
→ excluded higher-depth acoustics stay out
```

This is the post-G9-5 checkpoint after PR #80. It preserves the useful reflected-sound and
echolocation invariant while explicitly rejecting the donor-specific universal-threshold
shortcut.

Fail if the agent treats 95% as mastery, omits the prerequisite chain, halves/doubles the
wrong echo path, invents one universal echo threshold, or imports Doppler/interference,
standing-wave formulae or decibel logarithms into the Grade-9 route.


---

## APSTRESS-G9-SIMPLE-MACHINES-90

### Prompt

> Prepare CORE1A and CORE1B for Physics — Simple machines. Student knowledge estimate:
> 90%. Use the estimate only to select the starting rung and preserve prerequisite checks.
> Keep mechanical advantage tied to same-state load/effort measurements and the ideal
> force-distance tradeoff; do not import torque equations, pulley-count formulae,
> efficiency catalogues, or story-specific machine capabilities.

### Expected path

```text
resolve current Grade-9 Simple Machines matrix
→ owner estimate 90
→ conservative floor = R3 at ladder_position 90
→ prerequisite checks:
     CAP-WEP-WORK-DIRECTION
     CAP-MACHINE-TRADEOFF
     CAP-MACHINE-MA
→ READY_WITH_CHECKS
→ CORE1A / CORE1B use the same canonical target segment
→ same-state load/effort semantics remain intact
→ fixed-pulley counterexample prevents "all machines reduce force"
→ no undeclared higher-depth machine formulae are imported
```

This is the post-G9-6 checkpoint. It protects the smallest durable decision from PR #82:
Simple Machines remains a three-capability Grade-9 spine rather than splitting into
story-specific lever/pulley/incline capabilities.

Fail if the agent treats 90% as mastery, loses the cross-topic Work/Energy prerequisite,
mixes measurements from different machine states, assumes all useful machines multiply
force, or imports torque/pulley/efficiency formula catalogues into the Grade-9 route.



---

## APSTRESS-G9-MOTION-70-DEFAULT

### Prompt

> Prepare CORE1A and CORE1B for Physics — One-dimensional motion. Student knowledge
> estimate: 70%. Use the estimate only to select the starting rung and preserve prerequisite
> checks. Keep the zero-velocity/non-zero-acceleration diagnostic extension out of the
> ordinary default route unless it is explicitly demanded; continue through the required
> graph, constant-acceleration and elementary uniform-circular-motion rungs without pulling
> Grade-10/11 projectile or general 2D kinematics into this Grade-9 path.

### Expected path

```text
resolve current Grade-9 Motion matrix
→ owner estimate 70
→ non-default diagnostic R3 is not an automatic coordinate
→ conservative default floor = R2 at ladder_position 45
→ prerequisite check:
     CAP-KIN-DISTANCE-DISPLACEMENT
→ READY_WITH_CHECKS
→ selected ordinary teaching segment:
     R2
     R4G
     R4
     R5
→ R3 remains available only for explicit diagnostic/question/owner demand
→ CORE1A / CORE1B use the same selected segment
```

This is the post-#88 Grade-9 Motion checkpoint. It tests the distinction between retaining a
useful diagnostic capability and silently treating it as ordinary curriculum progression.

Fail if the agent uses the 70% estimate to select R3, appends R3 to the default teaching
segment, treats the percentage as mastery, skips the R1 prerequisite check, or broadens the
Grade-9 Motion route into projectile/general two-dimensional kinematics.

---

## APSTRESS-G10-MIRRORS-85

### Prompt

> Prepare CORE1A and CORE1B for Physics — Reflection and spherical mirrors. Student
> knowledge estimate: 85%. Use the estimate only to select the starting rung and preserve
> prerequisite checks. Keep the ray construction, Cartesian sign convention, paraxial
> mirror-equation model and signed magnification mutually consistent; do not pull
> refraction, lenses, human-eye optics or later optics into this bounded Grade-10 slice.

### Expected path

```text
resolve current Grade-10 Reflection / spherical-mirror matrix
→ owner estimate 85
→ conservative floor = R6 at ladder_position 85
→ prerequisite checks:
     CAP-OPT-NORMAL-REFLECTION
     CAP-OPT-REAL-VIRTUAL-IMAGE
     CAP-OPT-SIGN-CONVENTION
     CAP-OPT-SPHERICAL-RAY-CONSTRUCTION
     CAP-OPT-MIRROR-EQUATION
→ READY_WITH_CHECKS
→ CORE1A / CORE1B use the same canonical target segment
→ signed magnification remains tied to the same mirror state
→ ray construction and mirror equation must agree inside the paraxial model
→ later optics remain outside G10-1A
```

This is the first frozen Grade-10 checkpoint after G10-1A. It protects the concrete
integration boundary that the first production slice established: the mirror formula is not
a detached algebra trick, and magnification is not an unsigned size factor.

Fail if the agent treats 85% as mastery, skips the prerequisite chain, assigns signs from
labels rather than coordinates, drops magnification sign, treats the mirror equation as an
exact wide-aperture law, or broadens the slice into refraction/lenses/human-eye optics.
