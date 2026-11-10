---
name: test-case-export
description: "Convert test cases written in Markdown or JSON into import-ready CSV for Azure DevOps Test Plans or Jira Xray (steps with action and expected result), with a bundled stdlib script. Use when test cases designed with Claude must land in the team's test management tool without retyping."
---

# Test case export

## Input format (JSON)
```json
[{"title": "Late fee applied the day after due date",
  "priority": 2, "area": "Billing\\Invoices",
  "steps": [{"action": "Create an unpaid invoice of 100 EUR due 2026-03-31", "expected": "Invoice is saved, status Unpaid"},
            {"action": "Run the fee job on 2026-04-01", "expected": "A late fee of 40 EUR is added"}]}]
```
Markdown is also accepted: a `## Title` heading per test, then a table `| Action | Expected |`.

## Commands
```bash
python "${CLAUDE_SKILL_DIR}/scripts/export_test_cases.py" cases.json --target azure > azure_import.csv
python "${CLAUDE_SKILL_DIR}/scripts/export_test_cases.py" cases.md   --target xray  > xray_import.csv
```

## Notes
- Azure DevOps: the CSV uses the columns `ID, Work Item Type, Title, Test Step, Step Action, Step Expected, Priority, Area Path`; import it from *Test Plans > Import test cases from CSV*. Leave `ID` empty for new items.
- Xray: one row per step with a shared `Test ID`; map columns in the Xray CSV importer.
- Check the column names against your project's process template before a large import; import 2 cases first.
