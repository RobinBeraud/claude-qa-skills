---
name: coverage-gap-analysis
description: "Read a code coverage report (Cobertura, JaCoCo, lcov, coverage.py) together with risk signals (business-critical modules, recent bugs, churn) and recommend where new tests pay off most, instead of chasing a global percentage. Use when someone asks to raise coverage, before refactoring, or to review test effort."
---

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
