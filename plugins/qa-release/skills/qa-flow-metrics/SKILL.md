---
name: qa-flow-metrics
description: "Compute quality flow metrics from a work-item export (Azure DevOps or Jira CSV): bugs created vs closed per month, open bug backlog, median time to fix, escape rate to production, reopen rate and aging, with a bundled stdlib script, then interpret trends without vanity metrics. Use for quality reviews, retrospectives, or to check whether AI-assisted development changed defect trends."
---

# QA flow metrics

## Run
```bash
python "${CLAUDE_SKILL_DIR}/scripts/qa_metrics.py" export.csv \
  --type "Work Item Type" --created "Created Date" --closed "Closed Date" --state "State" \
  --severity "Severity" --found-in "Found In Environment" --prod-values "Production,PRD" \
  --as-of 2026-11-10
```
Column names are flags because every export differs; only `--created` and `--type` are required. Dates in ISO or dd/mm/yyyy.

## Metrics produced
- Per month: bugs created, closed, net flow, median days to close, escaped to production and escape rate, reopen rate (if a reopen column is given).
- Open backlog at the as-of date by severity and by age bucket (<30, 30-90, 90-180, >180 days).

## Interpret with care
- Fewer bugs created can mean fewer tests, not better code: read it next to test activity and incidents.
- A falling median time to fix with a rising backlog means easy bugs are fixed first.
- Compare the same months year over year before claiming an effect (seasonality, holidays).
- Never rank people with these numbers.
