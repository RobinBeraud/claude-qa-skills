---
name: flaky-test-hunter
description: "Find flaky tests by comparing JUnit XML reports from several CI runs of the same code: pass/fail flips, flip rate, failure messages, and a quarantine shortlist, using a bundled stdlib script; then diagnose likely causes (timing, order, shared data, environment). Use when CI is red then green on retry, or the team stopped trusting the pipeline."
---

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
