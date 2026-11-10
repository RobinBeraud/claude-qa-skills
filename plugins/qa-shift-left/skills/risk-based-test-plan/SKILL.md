---
name: risk-based-test-plan
description: "Build a lean, risk-based test plan for a feature, epic or release: scope, risk matrix (impact x likelihood), test approach per risk, test types, data, environments, entry and exit criteria. Use when a feature needs a plan, before a release, or when asked what to test first with limited time."
---

# Risk-based test plan

Spend test effort where failure would hurt most. One to two pages, not a 40-page template.

## Inputs
Feature description or epic, list of stories, architecture notes if any, deadline and team capacity.

## Steps
1. **Scope**: in scope, out of scope (and why), assumptions.
2. **Risk storming**: list product risks with the SFDIPOT prompts (Structure, Function, Data, Interfaces, Platform, Operations, Time). Phrase each risk as "*X* may fail when *Y*, causing *Z*".
3. **Score** each risk: impact 1-3 x likelihood 1-3. Likelihood rises with new code, complex logic, many integrations, past bugs in the area, and AI-generated code that nobody fully read.
4. **Approach per risk**: which level (unit, API, UI, exploratory, performance, security, accessibility), who, and how much.
5. **Test data and environments**: what data must exist, how to reset it, which environment, which flags.
6. **Entry / exit criteria**: concrete and measurable (e.g. "no open blocker or critical bug", "all high risks covered by at least one automated check").
7. **Schedule**: tie the high risks to the earliest moment they can be tested.

## Output
Markdown with sections 1 to 7 and a risk table:
| # | Risk | Impact | Likelihood | Score | Approach | Owner |
Sort by score, highest first.

## Pitfalls
- A risk without an approach is a wish. A test type without a risk is waste.
- Mark explicitly what will **not** be tested; silence is not a decision.
