---
name: release-readiness
description: "Produce a go/no-go release readiness report from test results, open bugs, story status and known risks: what was tested, what was not, open defects by severity, risks with mitigation, and a clear recommendation with conditions. Use before a release or deployment decision, a release review meeting, or a customer go-live."
---

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
