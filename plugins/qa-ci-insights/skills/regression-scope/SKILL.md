---
name: regression-scope
description: "Select the regression tests a change most likely needs, from the files changed in a branch or PR: name-matching test files plus tests that historically change together with those files (git co-change), ranked by score, with a bundled stdlib script. Use when the full suite is too slow, to plan manual regression for a release, or to review whether a PR touched its tests."
---

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
