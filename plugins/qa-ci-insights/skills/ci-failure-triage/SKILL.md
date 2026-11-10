---
name: ci-failure-triage
description: "Triage a failed CI pipeline from its logs: classify each failure as product bug, test bug, flaky test, environment/infrastructure or dependency issue, find the first real error in long logs, and propose the next action and owner. Use when a pipeline is red and someone asks what broke and whose it is."
---

# CI failure triage

## Steps
1. Find the **first** error, not the last: scroll up from the failure summary to the earliest stack trace, compiler error or failed step.
2. Classify:
   | Class | Typical evidence |
   |---|---|
   | Product bug | Assertion on business value fails consistently, same commit fails locally |
   | Test bug | Test changed in the PR, wrong expectation, broken fixture |
   | Flaky | Passes on rerun, timeout, timing-dependent message (see `flaky-test-hunter`) |
   | Environment | DNS, disk full, agent offline, service unavailable, certificate expired |
   | Dependency | Package registry, new version of a transitive dependency, lockfile drift |
3. Check what changed: the PR diff, dependency updates, pipeline definition, base image.
4. Propose the next action and owner; for product bugs, draft the bug with `bug-report`.

## Output
| Job / test | First error (1 line) | Class | Evidence | Next action | Owner |
and a one-paragraph summary for the team channel.
