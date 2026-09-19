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

## Post-completion routing guard

The authoring completion claim means the **ordinary Grade-9 route**, not every retained
extension capability. Rungs retained only for explicit diagnostic/advanced/question demand
are marked `default_entry_eligible: false`: generic learner profiles and rough owner estimates
do not select them and default teaching segments do not append them. The canonical extension
records remain available when an owner explicitly routes to that extension.

This routing flag is operational only. It is not curriculum authority and does not replace the
scope/source decisions in the topic audits.

## Subsequent workstream

Grade-10 discovery subsequently began from current `main` in PR #85 using the same donor-first,
current-source-bounded method. This post-completion Grade-9 routing correction does not broaden
Grade-9 content and should remain independent of Grade-10 production slices.


## Frozen stress closure

Each of the six Grade-9 production slices now has at least one saved agent-path checkpoint:

```text
Motion                 APSTRESS-G9-MOTION-70-DEFAULT
Force / Laws           APSTRESS-G9-NLM-70-PRACTICE
Gravitation            APSTRESS-G9-GRAV-60-TEACH
Work / Energy / Power  APSTRESS-G9-WEP-95-DERIVATION
Sound                  APSTRESS-G9-SOUND-95-REFLECTION
Simple Machines        APSTRESS-G9-SIMPLE-MACHINES-90
```

The runner checks the owner-estimate route and, where declared, the execution-packet teaching
segment. This matters after the post-completion extension-routing correction: retained
diagnostic/advanced rungs may remain canonical without becoming automatic learner coordinates
or default teaching suffixes.

This is system regression evidence only. It does not create learner mastery evidence and does
not reopen the Grade-9 authoring pass.
