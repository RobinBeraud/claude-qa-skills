---
name: ebm-scorecard
description: "Track Evidence-Based Management measures over time with a bundled stdlib script: from a CSV of measurements (period, key value area, measure, value, direction) it computes the latest value, change vs previous period and vs baseline, an improving / worsening / flat signal per measure and a summary per key value area. Use for monthly or quarterly EBM reviews or a product value dashboard."
---

# EBM scorecard

## CSV format
```
period,kva,measure,value,direction
2026-Q1,CV,Customer satisfaction (CSAT),7.6,higher
2026-Q1,T2M,Lead time (days),21,lower
2026-Q2,CV,Customer satisfaction (CSAT),7.9,higher
2026-Q2,T2M,Lead time (days),17,lower
```
`kva` is one of CV, UV, T2M, A2I. `direction` says whether higher or lower is better.

## Run
```bash
python "${CLAUDE_SKILL_DIR}/scripts/ebm_scorecard.py" ebm.csv --threshold 5
```
`--threshold` (percent) below which a change counts as flat.

## Output and reading
- Per measure: baseline, previous, latest, change vs previous and baseline, signal.
- Per KVA: how many measures improve, worsen or stay flat.
- Then discuss with the team: which goal hypothesis do these signals support or contradict? Which experiment next (`ebm-experiment-loop`)?
