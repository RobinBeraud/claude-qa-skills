---
name: bug-triage
description: "Triage a batch of incoming bugs or a bug backlog export: detect likely duplicates, missing information, misfiled components, severity inconsistencies and stale items, then propose a ranked action list. Use for weekly bug triage meetings, after a bug bash, or when a backlog has grown out of control."
---

# Bug triage

## Input
A list or export (CSV/JSON) with at least id, title, description, state, created date; ideally severity, priority, area, assignee, last update.

## Steps
1. **Normalise** titles (lowercase, strip ids and versions) and group near-duplicates by shared key terms and same area; list them as *candidate* duplicates with the reason.
2. **Completeness**: flag reports missing steps, expected/actual, environment or evidence; draft the question to ask the reporter.
3. **Severity sanity**: data loss, security, money or legal impact must not be "low"; cosmetic issues must not be "critical".
4. **Staleness**: open > 180 days with no activity -> propose close or re-validate.
5. **Clusters**: areas with many bugs this period -> hint for root-cause analysis.
6. **Rank** what to fix first: severity x frequency x customer impact.

## Output
1. Proposed decisions table: `id | proposal (fix now / schedule / need info / duplicate of X / close) | reason`.
2. Duplicate groups.
3. Hot spots by area with counts.
Decisions are proposals: the triage meeting decides.
