---
name: test-pyramid-assessment
description: "Measure the real shape of a repository's test suite with a bundled stdlib script: count test files and test cases classified as unit, integration/API or end-to-end from paths, names and imports, compare it to a healthy pyramid (or trophy), and recommend where to move effort. Use when someone claims the suite is too slow, too flaky or top-heavy, or before writing a test strategy."
---

# Test pyramid assessment

## Run (from the repository root)
```bash
python "${CLAUDE_SKILL_DIR}/scripts/pyramid_scan.py" . --format md
```
The script walks the repo (skipping `node_modules`, `.git`, build folders), finds test files for Python, JS/TS, Java/Kotlin, C#, Go and PHP, counts test cases, and classifies each file:
- **e2e**: Playwright, Cypress, Selenium, WebDriver, Appium imports, or `e2e/` paths
- **integration/api**: HTTP clients, test containers, databases, `integration/`, `api/` paths
- **unit**: everything else that looks like a test

## Interpret
- A healthy suite usually has most cases at unit level and few E2E; a "testing trophy" (more integration) is fine for thin-logic apps.
- **Ice-cream cone** (mostly E2E/manual): slow, flaky; push logic checks down to unit/API.
- **No integration level**: units pass but wiring breaks; add API/contract tests.
- Heuristic classification: check a sample of files before concluding.

## Output
Counts per level (files and cases), the shape diagnosis, and 3 recommendations with the skills to apply.
