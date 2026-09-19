# Grade-9 Physics authoring pass — completion record

The sequential Grade-9 Physics authoring pass is complete. G9-6 merged after clean push and
pull-request guardrails, closing the Grade-9-only authoring freeze.

## Completed slices

| Slice | Matrix | Disposition |
| --- | --- | --- |
| G9-1 Motion | `MATRIX-PHY-KIN-1D-MOTION` | audited; reused existing canonical spine |
| G9-2 Force and Laws of Motion | `MATRIX-PHY-NLM-FIRST-LAW` | audited; removed false capability prerequisite |
| G9-3 Gravitation | `MATRIX-PHY-GRAV-UNIVERSAL-LAW` | copied/adapted prior Physics semantics into local Grade9V3 records |
| G9-4 Work, Energy and Power | `MATRIX-PHY-WORK-ENERGY-POWER` | donor-adapted; strengthened system-boundary and conditional conservation |
| G9-5 Sound | `MATRIX-PHY-SOUND` | donor-adapted; strengthened longitudinal/echo model boundaries |
| G9-6 Simple Machines | `MATRIX-PHY-SIMPLE-MACHINES` | current-source audit; strengthened same-state MA practical reasoning |

## Boundaries preserved

- matrices remain pedagogical structures, not curriculum authority;
- no grade/class field was added to the matrix schema;
- no donor repository is a runtime dependency;
- learner state remains outside canonical content;
- relative motion remains extension/question-demand;
- vector material is prerequisite/question-demand only;
- higher-grade/broader Physics matrices were not expanded for completeness.

## Next workstream

Do **not** mix Grade 10 into this PR. A later Grade-10 pass should begin from current `main`,
repeat the donor-first copy/adapt procedure, and establish its own current-source scope before
authoring.
