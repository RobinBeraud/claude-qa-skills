from _gen import write_plugin

PLUGIN = "qa-release"
DESC = "Ship with evidence: go/no-go release readiness reports, post-deployment smoke plans, quality flow metrics from Azure DevOps or Jira exports, and blameless root-cause analysis of escaped defects."

S = {}

S["release-readiness"] = ("""Produce a go/no-go release readiness report from test results, open bugs, story status and known risks: what was tested, what was not, open defects by severity, risks with mitigation, and a clear recommendation with conditions. Use before a release or deployment decision, a release review meeting, or a customer go-live.""", r"""
# Release readiness

## Inputs
Release scope (stories/epics), test execution results (automated + manual), open bugs export, known risks, exit criteria from the test plan.

## Steps
1. **Scope status**: stories done / not done / partially tested.
2. **Execution**: pass/fail/blocked/not run per area; flag "not run" honestly.
3. **Open defects** by severity, with the ones that block the exit criteria named.
4. **Risk review**: each high risk from the test plan -> covered? residual risk? mitigation (feature flag, monitoring, rollback plan, support briefing).
5. **Exit criteria check**: met / not met, one line each.
6. **Recommendation**: GO, GO WITH CONDITIONS (list them, each with an owner), or NO-GO (what would change the answer).

## Output (one page)
```
RELEASE: x.y  DATE:  RECOMMENDATION: GO WITH CONDITIONS
Scope:        18/20 stories done, 2 deferred (list)
Testing:      312 automated pass, 4 fail (known, non-blocking), 23 manual pass, 2 blocked (env)
Open bugs:    0 blocker, 1 critical (#123, workaround documented), 6 major
Not tested:   ...
Risks:        ...
Conditions:   ...
```
The recommendation belongs to the team and product owner; this report gives them the facts.
""")

S["post-deploy-smoke"] = ("""Design a short post-deployment smoke and verification plan: the 10-20 checks that prove a deployment is healthy in minutes (critical journeys, integrations, background jobs, monitoring signals) with owners, expected results and a rollback trigger. Use before a deployment window, a hotfix, or a migration go-live.""", r"""
# Post-deployment smoke plan

## Steps
1. List the **critical journeys** (log in, the 3 money-making flows, the most used screen) and pick one read-only or reversible check per journey.
2. Add **integrations**: payment, e-invoicing platform, identity provider, e-mail, exports to third parties.
3. Add **background work**: scheduled jobs, queues draining, batch outputs.
4. Add **signals**: error rate, latency, logs for new exceptions, business counters (orders, invoices created) compared with the same hour last week.
5. Define the **rollback trigger** in numbers (e.g. error rate > 2 % for 10 min, any data corruption, login failure).
6. Order by speed: automated checks first, then manual ones; total under 30 minutes.

## Output
| # | Check | How (automated / manual, command or URL) | Expected | Owner | Max time |
plus the rollback trigger and who decides. Never use real customer actions that cannot be undone (payments, outgoing invoices) as smoke tests.
""")

S["qa-flow-metrics"] = ("""Compute quality flow metrics from a work-item export (Azure DevOps or Jira CSV): bugs created vs closed per month, open bug backlog, median time to fix, escape rate to production, reopen rate and aging, with a bundled stdlib script, then interpret trends without vanity metrics. Use for quality reviews, retrospectives, or to check whether AI-assisted development changed defect trends.""", r"""
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
""")

S["escaped-defect-rca"] = ("""Run a blameless root-cause analysis of a defect that reached production: timeline, how it was introduced, why each test layer and review missed it, contributing factors, and concrete prevention actions (a test, a check, a process change) with owners. Use after a production incident or a customer-reported bug worth learning from.""", r"""
# Escaped defect analysis

## Steps
1. **Facts**: what customers saw, since when, how many affected, how it was detected (customer, monitoring, support).
2. **Timeline**: change that introduced it (commit/PR), reviews, test runs, deployment, detection, fix.
3. **Why it escaped**, layer by layer: requirement (was the case known?), unit, API, E2E, exploratory, code review, monitoring. For each: would a reasonable check here have caught it? Why not?
4. **Contributing factors**: time pressure, missing test data, environment gaps, AI-generated code accepted without reading, unclear ownership. No names, no blame.
5. **Actions**: at most 3, each concrete, owned and dated: e.g. "add a property test on VAT rounding", "add monitoring on export errors", "add the case to the refinement checklist".
6. **Detection**: how to find this class of bug faster next time.

## Output
Incident summary, timeline table, "where it could have been caught" table, actions table (`action | owner | due | done when`).
""")

write_plugin(PLUGIN, DESC, S, ["release", "metrics", "rca", "strategy"])
