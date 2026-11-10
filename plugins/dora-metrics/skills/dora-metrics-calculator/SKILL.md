---
name: dora-metrics-calculator
description: "Compute the five DORA software delivery metrics from CSV exports with a bundled stdlib script: deployment frequency, change lead time, change fail rate, failed deployment recovery time and deployment rework rate, per week or month, with medians and counts. Use when a team wants its DORA metrics from deployment logs, pipeline runs, releases or change records (Azure DevOps, GitHub, GitLab, ServiceNow)."
---

# DORA metrics calculator

DORA groups five metrics: **throughput** (change lead time, deployment frequency, failed deployment recovery time) and **instability** (change fail rate, deployment rework rate).

## Input
A deployments CSV, one row per production deployment, with at least a timestamp. Optional columns, mapped with flags:
| Flag | Meaning |
|---|---|
| `--time-col` | deployment timestamp (required) |
| `--env-col` + `--env` | keep only production rows |
| `--failed-col` | truthy when the deployment caused a failure needing remediation |
| `--restored-col` | timestamp when service was restored after that failure |
| `--rework-col` | truthy when the deployment was unplanned work to fix a bug (rework) |
| `--commit-col` | first commit (or PR creation) timestamp of the change deployed |
| `--changes` + `--change-commit-col` + `--change-deploy-col` | alternative: one row per change with commit and deploy times |

## Run
```bash
python "${CLAUDE_SKILL_DIR}/scripts/dora_metrics.py" --deployments deploys.csv --time-col deployed_at \
  --env-col environment --env production --failed-col caused_incident --restored-col restored_at \
  --rework-col hotfix --commit-col first_commit_at --period month
```

## Then
- Read trends, not single months; note small samples (n < 10 deployments).
- Compare with the bands of the **latest** State of DevOps report (they change yearly); rework rate has no official bands yet.
- Pair every number with a question for the team (what happened in March?).
