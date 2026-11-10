---
name: mutation-score-gate
description: "Add a pragmatic mutation-testing quality gate to CI: incremental mutation on changed files only (Stryker --incremental / since, PIT with scmMutationCoverage or history), a threshold on the changed code rather than the whole repo, time limits, and a clear report in the pull request. Use when the team wants mutation testing in the pipeline without slowing every build."
---

# Mutation score gate

## Design
- **Changed code only**: mutate files touched by the PR (`stryker run --since=main`, `--incremental`, PIT `scmMutationCoverage` or `withHistory`). Full runs stay nightly.
- **Threshold on changed code**, e.g. break below 70 % for files in critical packages, warn elsewhere. Start low, raise gradually.
- **Time box**: cap the job (e.g. 15 min); if exceeded, warn instead of failing.
- **Report in the PR**: score, survivors with file:line (the `mutation-report-digest` output fits a PR comment).

## Example (StrykerJS, GitHub Actions)
```yaml
- run: npx stryker run --incremental --since=origin/main --thresholds.break 70
```
## Rules
- Exclude generated code and tests from mutation.
- Equivalent mutants are ignored with a documented reason, never by lowering the threshold globally.

## Output
Pipeline snippet for the team's CI (GitHub Actions, Azure Pipelines or GitLab CI), threshold policy, and the rollout plan (warn for 2 weeks, then break).
