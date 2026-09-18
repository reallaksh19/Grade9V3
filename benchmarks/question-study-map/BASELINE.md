# Benchmark sweep baseline

- Frozen production commit: `e6f9ccce4a2ecbba8764bfa5cd5e877830afa56d`
- Baseline event: merge of PR #48 benchmark blueprint into `main`
- Sweep branch: `benchmark/question-study-map-sweep-01`
- Guardrails on frozen commit: GitHub Actions runs `35372518922` and `35372375833`, both successful.
- Scope: the 17 matrices listed in `COVERAGE.md`.

## Freeze rule

All observed benchmark results in this sweep refer to the exact production tree above. If production changes, do not silently mix new results into this historical sweep; start a re-benchmark against the new baseline.

## Write boundary

The benchmark sweep may change only `benchmarks/question-study-map/**`. It must not repair `Shared/**`, `Physics/**`, `Mathematics/**`, schemas, learner data, source custody or production content.
