# Grade9V3

Self-study learner-material production system for **Physics, Mathematics and Chemistry**, **CBSE grades 9–11** (with explicit IIT-JEE tier classification where applicable).

Six learner products per subtopic bucket:

| Product | Purpose |
|---|---|
| Core1 | Compact basic notes / semantic orientation |
| Core2 | Source questions with ladder hints, source identity and answers |
| Core1A | Declarative detailed teaching, by intrinsic subtopic difficulty |
| Core1B | Open-ended conceptual reconstruction (self-tutor) |
| Core2A | Purpose-adjusted practice with complete solution breakdowns |
| Core2B | Supported application and transfer |

## Shape

```
Shared/            subject-neutral engine — no subject, topic or gate identifier may be hardcoded here
  roles/           the six Core role specifications
  gates/           technical engineering gate schema + validator        (P2)
  library/         microtopic library engine: intake, promotion, resolver (P3)
  publication_host/ composition, closure, storage, audit, figures        (P1)
  tools/           guardrails and generators
Physics/ Mathematics/ Chemistry/
  adapter/         subject contract: validator families, representation vocabulary,
                   equation semantic fields, curriculum bindings
  gates/           subject gate data, grades 9–11
  library/         microtopic packages
  content/         authored runs and published products
tools/             topic library browser, run builder, portal            (P4)
docs/              program plan and architecture
```

The governing rule: **subject and topic variation is governed data, never a branch in engine code.** `Shared/` is checked for this automatically — see `Shared/tools/topic_independence_guard.py`.

## Running it

```sh
# compile one bucket from its library into publication inputs
python3 Shared/library/compile_inputs.py Mathematics/library/*.json \
  --bucket BUCKET-LINEAR-EQUATION --subject Mathematics \
  --topic-id MATH-LINEQ-G9 --title "Linear equations in one unknown" --out /tmp/lineq

# publish through that subject's adapter
python3 Mathematics/run.py publish --plan /tmp/lineq/plan.json \
  --baseline /tmp/lineq/baseline.json --source-root /tmp/lineq --out /tmp/lineq/publication

python3 -m unittest discover -s tests -p "test_*.py"   # full suite
python3 Shared/tools/topic_independence_guard.py       # engine carries no subject
python3 Shared/tools/build_manifest.py                 # regenerates the manifest and tools/data.js
```

A committed publication pins a snapshot of the engine that produced it, and the suite re-verifies that snapshot. So **after changing anything under `Shared/` or `Physics/adapter/`, republish the committed run** — the composed pages should come back byte-identical, and if they do not, that is a real change to learner-facing output and needs saying out loud:

```sh
R=Physics/content/relative-motion-g9
python3 Physics/run.py publish --plan $R/inputs/plan.json --baseline $R/inputs/baseline.json \
  --source-root $R/inputs --out /tmp/regen && rm -rf $R/publication && cp -r /tmp/regen $R/publication
```

`tools/index.html` opens over `file://` with no build step.

## Status

Two subjects publish end-to-end: Physics (relative motion, frozen as the port oracle) and Mathematics (linear equations, compiled from its library on demand). Chemistry has a contract but no library yet.

See [docs/PROGRAM-PLAN.md](docs/PROGRAM-PLAN.md) for the phased plan and what is proven versus proposed. **Nothing here claims independent academic review, learner release or curriculum authority** — machine checks establish structure, custody and supported computation, not that an explanation teaches.

## Provenance

Architecture derives from the V3B work in `reallaksh19/Common` (draft PR #364, branch `draft/core-relay-architecture-review-20260913`), with adaptations from the parallel tracks in that repository: PR #350/#383 (Physics engineering gates, curriculum-scope binding, authority delegation) and PR #395 (Mathematics observability, subtopic intelligence library, topic-independence guarding). Those tracks are referenced and adapted, never copied wholesale.
