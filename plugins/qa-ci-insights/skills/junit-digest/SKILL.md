---
name: junit-digest
description: "Summarise one or many JUnit/xUnit XML test reports into a short digest: totals, failures grouped by error message, slowest tests and suites, skipped tests, using a bundled stdlib script. Use after a CI run, before a release meeting, or when a report is too long to read."
---

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
