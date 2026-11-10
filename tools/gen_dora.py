from _gen import write_plugin

PLUGIN = "dora-metrics"
DESC = "Measure and improve software delivery performance with the five DORA metrics (deployment frequency, change lead time, failed deployment recovery time, change fail rate, deployment rework rate): calculator script, data sources per tool, quick check, capability-based improvement plan and a monthly review that resists gaming."

S = {}

S["dora-metrics-calculator"] = ("""Compute the five DORA software delivery metrics from CSV exports with a bundled stdlib script: deployment frequency, change lead time, change fail rate, failed deployment recovery time and deployment rework rate, per week or month, with medians and counts. Use when a team wants its DORA metrics from deployment logs, pipeline runs, releases or change records (Azure DevOps, GitHub, GitLab, ServiceNow).""", r"""
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
""")

S["dora-data-sources"] = ("""Find and define where each DORA metric's data comes from in the team's tools (Azure DevOps pipelines and releases, GitHub Actions and deployments API, GitLab environments, Jira, ServiceNow change and incident records) and write precise definitions of deployment, failure, restoration, change and rework so the numbers are comparable. Use before measuring DORA metrics or when two teams compute them differently.""", r"""
# DORA data sources and definitions

## Decide the definitions first (write them down)
| Term | Decide |
|---|---|
| Deployment | A production deployment of a releasable change, per service. Count config/flag changes? |
| Change | Commit, PR or work item: what starts the lead-time clock (first commit is the usual choice) |
| Failure | Deployment that degrades service and needs remediation (rollback, hotfix, patch, incident) |
| Restoration | Service restored for users, not root cause fixed |
| Rework | Unplanned deployment to fix a defect in a previous deployment |

## Where to get data
| Tool | Deployments | Lead time | Failures / restore |
|---|---|---|---|
| Azure DevOps | Pipeline runs of the prod stage / Release deployments (REST `_apis/pipelines`, `release/deployments`) | Commit dates of the run's changes, PR `creationDate` | Linked bugs/incidents, rollback runs |
| GitHub | Deployments API or workflow runs on the prod environment | Commits/PRs in the deployment | Issues labelled incident, reverted PRs |
| GitLab | Environments + deployments API; built-in DORA analytics (Ultimate) | MR merge to deploy | Incidents (issues of type incident) |
| ServiceNow | Change requests (implemented, failed) | Change created to implemented (proxy) | Incident open/resolve, linked change |
| Jira | Releases / deployment info | Issue in progress to released | Incident issues |

## Output
Definitions table signed off by the team, extraction queries or API calls per metric, and the CSV layout for `dora-metrics-calculator`.
""")

S["dora-quick-check"] = ("""Run a quick, survey-based DORA estimate when no tooling data exists: ask the team the four classic questions (deployment frequency, lead time, change fail rate, recovery time) with the official answer ranges, collect answers per person, show spread and consensus, and turn disagreements into discussion. Use for a first assessment, a workshop, or to compare perception with measured data.""", r"""
# DORA quick check

## Questions
Use the exact wording and answer ranges of the current quick check at dora.dev (they evolve with each report), for the primary application or service:
1. **Deployment frequency**: how often do you deploy to production?
2. **Change lead time**: how long from code committed to code running in production?
3. **Change fail rate**: what share of deployments cause a failure that needs remediation?
4. **Failed deployment recovery time**: how long to restore service after a failed deployment?
5. **Deployment rework rate**: what share of deployments are unplanned, to fix a defect in production?

## Steps
1. Ask each person individually (anonymous form).
2. Show the distribution per question; a wide spread means people do not share the same view of the system.
3. Discuss the spread first, the answer second.
4. Plan to replace the estimate with measured data (`dora-data-sources`).

## Output
Answer distribution per question, the consensus estimate, the disagreements worth discussing, and next steps.
""")

S["dora-capabilities-plan"] = ("""Build an improvement plan from the DORA research capabilities (technical: CI, trunk-based development, test automation, deployment automation, loosely coupled architecture, database change management, monitoring; process: small batches, WIP limits, visual management, streamlined change approval; culture: generative culture, learning, psychological safety): find the constraint and run experiments. Use after measuring DORA metrics, when a team asks how to improve them.""", r"""
# DORA capabilities improvement plan

Metrics show *where*; capabilities show *how*. Improve one constraint at a time.

## Steps
1. Start from the metrics: which one is the weakest relative to the team's goal?
2. Map likely capabilities:
   | Weak metric | Capabilities to look at first |
   |---|---|
   | Deployment frequency | Deployment automation, small batches, streamlined change approval, trunk-based development |
   | Change lead time | CI, test automation, code review time, WIP limits, loosely coupled architecture |
   | Change fail rate / rework | Test automation, shift-left testing, code review quality, database change management, small batches |
   | Recovery time | Monitoring and observability, rollback/feature flags, proactive failure notification, incident practice |
3. Assess each candidate capability 1-5 with evidence; pick **one** constraint.
4. Write 1-3 experiments: hypothesis, change, metric expected to move, time box (4-8 weeks).
5. Review results with `dora-metrics-review`; keep, adapt or drop.

## Output
Capability assessment table, the chosen constraint with rationale, and experiment cards.
""")

S["dora-metrics-review"] = ("""Facilitate a monthly DORA metrics review that leads to learning instead of gaming: trends with context, throughput and instability read together, outliers explained by the team, one improvement experiment, and guardrails against misuse (no team rankings, no individual targets). Includes how to read DORA alongside AI coding adoption. Use for monthly team or department delivery reviews.""", r"""
# DORA metrics review (45 min)

## Agenda
1. **Trends (10 min)**: the five metrics over 6-12 months, throughput and instability **side by side**. Faster with more failures is not progress.
2. **Outliers (10 min)**: the team explains spikes (holidays, migration, incident, process change). Write the explanation on the chart.
3. **Experiment check (10 min)**: did last month's experiment move its metric? Keep, adapt, drop.
4. **Next experiment (10 min)**: one, from `dora-capabilities-plan`.
5. **Close (5 min)**: what we tell stakeholders.

## Guardrails
- Metrics belong to the team. No ranking of teams, no individual targets, no bonuses on DORA numbers (Goodhart's law).
- Look at all five together; a single metric can always be gamed.
- Small samples: say "n = 6 deployments" next to the percentage.

## Reading AI coding adoption
The DORA 2024 report found higher AI adoption associated with slightly *lower* delivery throughput and stability on average, while individuals reported higher productivity. When AI tools ramp up, watch change lead time **and** change fail rate and rework rate together, plus review time on PRs: more code is not more delivery if verification becomes the bottleneck.

## Output
Review notes template, the charts to prepare, and the experiment card.
""")

write_plugin(PLUGIN, DESC, S, ["dora", "devops", "delivery-performance", "metrics"])
