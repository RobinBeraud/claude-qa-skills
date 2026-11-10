---
name: mutation-report-digest
description: "Summarise a mutation testing report (Stryker mutation-testing-report-schema JSON, used by StrykerJS, Stryker.NET and Stryker4s, or PIT mutations.xml) with a bundled stdlib script: score per file, survivors and no-coverage mutants grouped by file and mutator, worst files first. Use after a mutation run, or when a report is too big to read."
---

# Mutation report digest

## Run
```bash
python "${CLAUDE_SKILL_DIR}/scripts/mutation_report.py" reports/mutation/mutation.json --top 15
python "${CLAUDE_SKILL_DIR}/scripts/mutation_report.py" target/pit-reports/mutations.xml
```

## What you get
- Overall mutation score = killed / (killed + survived + no coverage + timeout counted as killed), with counts per status.
- Per file: score, survivors, no-coverage mutants; sorted by number of survivors.
- Survivors by mutator type (e.g. `EqualityOperator`, `ConditionalBoundary`, `ArithmeticOperator`): shows which kind of assertion the suite lacks.
- The first survivors with file:line and the mutated code, ready for triage.

## Then
Continue with `surviving-mutant-triage` on the worst files. Do not chase 100 %: aim at the critical files.
