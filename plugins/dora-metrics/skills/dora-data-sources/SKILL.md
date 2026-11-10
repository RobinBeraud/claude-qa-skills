---
name: dora-data-sources
description: "Find and define where each DORA metric's data comes from in the team's tools (Azure DevOps pipelines and releases, GitHub Actions and deployments API, GitLab environments, Jira, ServiceNow change and incident records) and write precise definitions of deployment, failure, restoration, change and rework so the numbers are comparable. Use before measuring DORA metrics or when two teams compute them differently."
---

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
