from _gen import write_plugin

PLUGIN = "qa-ci-insights"
DESC = "Make CI signals trustworthy: find flaky tests across runs, digest JUnit reports, pick the regression tests a change really needs from git history, triage CI failures by cause, and target coverage gaps by risk."

S = {}

S["flaky-test-hunter"] = ("""Find flaky tests by comparing JUnit XML reports from several CI runs of the same code: pass/fail flips, flip rate, failure messages, and a quarantine shortlist, using a bundled stdlib script; then diagnose likely causes (timing, order, shared data, environment). Use when CI is red then green on retry, or the team stopped trusting the pipeline.""", r"""
# Flaky test hunter

## Collect
Download the JUnit XML of 5-20 runs (same commit ideally, or a recent range) into one folder, one sub-folder or file per run, named so they sort chronologically.

## Run
```bash
python "${CLAUDE_SKILL_DIR}/scripts/flaky_tests.py" runs/ --min-runs 3 --format md
```
It lists every test that both passed and failed, with runs, failures, flips (status changes between consecutive runs), flip rate, and the most frequent failure message.

## Diagnose each flaky test
| Clue | Likely cause | Fix |
|---|---|---|
| Timeout / "element not found" | Missing wait condition, slow env | Wait on state, not time |
| Fails only in full suite | Order dependence, shared data | Isolate data, reset state |
| Fails around midnight / month-end | Clock / time zone | Freeze the clock |
| Different message each time | Race condition in the product | Log a product bug |
| Only on one agent | Environment | Fix the agent image |

## Output
Script table, then per test: cause hypothesis, evidence, fix, and whether to **quarantine** (tag + ticket + owner + deadline), never silently skip.
""")

S["junit-digest"] = ("""Summarise one or many JUnit/xUnit XML test reports into a short digest: totals, failures grouped by error message, slowest tests and suites, skipped tests, using a bundled stdlib script. Use after a CI run, before a release meeting, or when a report is too long to read.""", r"""
# JUnit digest

## Run
```bash
python "${CLAUDE_SKILL_DIR}/scripts/junit_digest.py" reports/ --top 10
```
Accepts files or folders (JUnit, pytest `--junitxml`, Maven Surefire, Playwright/Jest junit reporters).

## What you get
- Totals: tests, passed, failed, errors, skipped, duration.
- Failures **grouped by normalised message** (numbers and ids stripped), so 40 failures with one root cause read as one line.
- Slowest tests and slowest suites.
- Skipped tests count (skips pile up silently).

## Then
Add a 3-line human summary: is the build releasable, the main failure cluster and its probable cause, and what to look at first.
""")

S["regression-scope"] = ("""Select the regression tests a change most likely needs, from the files changed in a branch or PR: name-matching test files plus tests that historically change together with those files (git co-change), ranked by score, with a bundled stdlib script. Use when the full suite is too slow, to plan manual regression for a release, or to review whether a PR touched its tests.""", r"""
# Regression scope

## Run (inside the repository)
```bash
python "${CLAUDE_SKILL_DIR}/scripts/co_change.py" --base origin/main --head HEAD --history 1500 --top 30
```
- Changed files come from `git diff --name-only base...head`.
- For each changed source file, the script ranks test files by: same name stem (`invoice.py` <-> `test_invoice.py`, `Invoice.cs` <-> `InvoiceTests.cs`) and co-change frequency in the last N commits.

## Then
1. Group the ranked tests by area; add manual regression checks for areas without automated tests.
2. Flag changed source files with **no related test at all**: that is the real risk.
3. Propose: must-run tests, should-run tests, and the full suite only if a shared component (auth, database layer, money calculation) changed.

## Caveat
Co-change is a heuristic from history: new code has no history, and generated or bulk commits add noise (the script ignores commits touching more than 50 files).
""")

S["ci-failure-triage"] = ("""Triage a failed CI pipeline from its logs: classify each failure as product bug, test bug, flaky test, environment/infrastructure or dependency issue, find the first real error in long logs, and propose the next action and owner. Use when a pipeline is red and someone asks what broke and whose it is.""", r"""
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
""")

S["coverage-gap-analysis"] = ("""Read a code coverage report (Cobertura, JaCoCo, lcov, coverage.py) together with risk signals (business-critical modules, recent bugs, churn) and recommend where new tests pay off most, instead of chasing a global percentage. Use when someone asks to raise coverage, before refactoring, or to review test effort.""", r"""
# Coverage gap analysis

## Steps
1. Parse the coverage report per file/package (line and branch coverage).
2. Add risk signals per file: business criticality (money, permissions, legal), churn (`git log --since=6.months --format= --name-only | sort | uniq -c`), bug history, complexity.
3. Score = risk x (1 - branch coverage). Rank.
4. For the top files, list the **uncovered branches that matter** (error paths, rounding, permission checks), not just uncovered lines.
5. Recommend the test level for each (unit, API, characterization).

## Output
| File | Branch cov. | Churn | Criticality | Score | What to test |
and a short note: global % targets reward easy tests; risk-weighted gaps do not.
""")

write_plugin(PLUGIN, DESC, S, ["ci", "flaky-tests", "junit", "regression"])
