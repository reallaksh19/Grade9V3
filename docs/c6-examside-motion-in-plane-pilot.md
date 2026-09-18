# C6 real-question pilot — ExamSIDE JEE Main Motion in a Plane

Source supplied by the owner:

https://questions.examside.com/past-years/jee/jee-main/physics/motion-in-a-plane

The source page is a real external JEE Main past-question bank, not a repository-authored
worksheet and not canonical curriculum authority. At inspection time it listed Motion in a
Plane questions from 2002–2026, with 93 questions in total (74 single-correct MCQs and
19 numerical questions).

This pilot uses the source only as **real question-demand evidence**. It does not copy the
question bank into the repository, promote ExamSIDE to source custody, or treat the page's
topic label as a canonical capability model.

## Representative routable slice

The pilot fixture keeps three questions whose demand can be mapped honestly to current
canonical capabilities without inventing new subject truth:

| Pilot id | Source case | Primary capability | Secondary capability |
|---|---|---|---|
| EXAMSIDE-MIP-2026-01-21-RIVER | river/boat minimum-time and drift problem | CAP-RELATIVE-V | CAP-VECTOR-CHECK |
| EXAMSIDE-MIP-2022-06-27-RAIN | rain/runner relative-velocity problem | CAP-RELATIVE-V | CAP-VECTOR-CHECK |
| EXAMSIDE-MIP-2021-08-26-BOMB | dropped object viewed from the moving plane | CAP-RELATIVE-V | CAP-NLM-FRAME-CHOICE |

This is intentionally a small representative slice. The goal is to exercise the real
worksheet/question-set pipeline against external demand, not to transcribe all 93 questions.

## First core routing gap exposed — now resolved narrowly

The first pilot run reached `CAP-SIGNED-PAIR`: a declared Mathematics
`external_provider` prerequisite for relative motion with no local matrix/rung.

The core now represents this honestly as:

```text
CAP-SIGNED-PAIR
state: EXTERNAL_BRIDGE
action: BRIDGE
provider: Mathematics
acceptance_status: PROVIDER_REVIEW_REQUIRED
```

This does **not** mark the prerequisite demonstrated and does not fabricate a Physics
lesson. It simply stops a declared provider boundary from being misreported as an
unclassified missing-teaching error. If Mathematics later supplies a genuine canonical
teaching location, the ordinary resolved route will replace the bridge naturally.

The three-question relative-motion/reference-frame slice now produces a valid learner-facing
study route with this bridge kept explicit.

## Feedback loop exercised on a real external question

The pilot now also runs the 2026 river/boat mapping through the feedback runtime without
promoting the external question into the canonical question library.

A simulated learner response that subtracts speeds as scalars and drops direction is handled
as:

```text
real external question
→ CAP-RELATIVE-V failure
→ DIAGNOSE using the canonical relative-velocity misconception prompt
→ MISCONCEPTION_REPAIR from MIC-COMMON-INTERVAL
→ fresh verification on canonical Q-AUTHOR-REL-01
→ direct-attempt observation draft
→ next review date
```

The important boundary remains intact: the external question supplies real demand; canonical
microtopics supply repair and verification. The runtime does not invent a hint ladder for a
question that has none.

## Real gaps exposed by the same source

The page also contains question types that the current canonical subject layer cannot yet
map faithfully. These are useful C6 findings, not failures to hide.

### Projectile-motion model selection and formula structure

Many questions ask about projectile range, maximum height, time of flight, trajectory or
velocity direction. The current subject layer has 1-D constant-acceleration reasoning but
does not yet own a dedicated projectile-motion capability that explicitly combines
independent horizontal and vertical motion.

Do not map those questions to CAP-KIN-CONSTANT-ACCELERATION merely because that relation
appears somewhere in a solution. That would collapse a 2-D model-selection demand into a
1-D formula capability.

### Vector decomposition / addition

The source includes resultant-motion questions such as wind plus an object's own velocity.
The current vector package owns vector subtraction and scalar/vector distinction, but not a
general vector-addition/decomposition capability suitable for these questions.

Do not reuse CAP-VEC-SUB-ORDER or CAP-GRAPHICAL-SUBTRACT as a substitute.

### Position vector -> velocity in 2-D

The 24 Jan 2025 evening question asks for velocity magnitude/direction from a time-dependent
position vector. The current subject layer has no canonical capability for differentiating
a 2-D position vector and then reconstructing vector magnitude/direction.

### 2-D constant-acceleration component solving

The source also includes x-y constant-acceleration questions where component equations must
be solved together. The existing Grade 9/11 kinematics capability is authored around a
straight velocity-time graph and should not silently expand into a general 2-D component
solver.

### Projectile energy question

The 22 Jan 2025 evening question about kinetic-energy decrease to the highest point has a
real WEP demand, but also requires projectile/component reasoning that is not yet represented
canonically. Mapping it only to WEP would understate the question demand.

## Pilot conclusion

C6 has now moved beyond "real question-bank pilot started" for the routable slice.

For the three retained real questions, the current system can now:

1. keep the questions transient rather than canonicalizing them;
2. map them to existing capabilities;
3. compute prerequisite order across matrices;
4. surface a declared external-provider prerequisite as a visible bridge;
5. produce the learner-facing study map;
6. accept a real-question attempt outcome;
7. diagnose a known misconception without guessing;
8. route to existing canonical repair;
9. select a fresh canonical verification item;
10. draft learner evidence and a later review date.

The remaining gaps are now predominantly **subject-content gaps exposed by real demand**,
not reasons to expand the core architecture:

1. projectile-motion model selection / range-height-time structure;
2. general vector addition and decomposition;
3. 2-D position-vector → velocity and component kinematics;
4. projectile-energy combinations where WEP alone understates the demand.

Those should be added only when selected for study, and only at the smallest durable
capability/matrix granularity needed by the real questions.
