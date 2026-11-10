---
name: gherkin-scenarios
description: "Write clean, business-readable Gherkin (Given/When/Then) scenarios and scenario outlines from acceptance criteria or examples, then lint them with a bundled script (one When per scenario, no UI clicks in steps, no vague words). Use for BDD, Cucumber/SpecFlow/Reqnroll/behave suites, or living documentation."
---

# Gherkin scenarios

Declarative scenarios describe **behaviour**, not clicks.

## Rules
- One behaviour per scenario, one `When`.
- `Given` sets state, `When` is the action, `Then` is an observable outcome.
- Business language: "Given an unpaid invoice of 120.00 EUR", not "Given I click the Invoices tab".
- Concrete values; use `Scenario Outline` + `Examples` when only data varies.
- `Background` only for setup shared by **every** scenario of the feature.
- Name scenarios after the rule: "Late fee is not applied before the due date".

## Steps
1. Group criteria by rule; one `Feature` per capability.
2. Write scenarios, then outlines for data-driven variants (include boundaries).
3. Lint:
   ```bash
   python "${CLAUDE_SKILL_DIR}/scripts/gherkin_lint.py" path/to/features
   ```
4. Fix every finding or justify it.

## Output
`.feature` file content, then the lint result.

## Example
```gherkin
Feature: Late payment fee
  Rule: A fee applies only after the due date
    Scenario Outline: Fee depends on days overdue
      Given an unpaid invoice of <amount> EUR due on 2026-03-31
      When the fee job runs on <run_date>
      Then the late fee is <fee> EUR
      Examples:
        | amount | run_date   | fee   |
        | 100.00 | 2026-03-31 | 0.00  |
        | 100.00 | 2026-04-01 | 40.00 |
```
