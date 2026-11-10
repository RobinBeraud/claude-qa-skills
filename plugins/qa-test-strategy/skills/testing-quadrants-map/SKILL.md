---
name: testing-quadrants-map
description: "Map a team's current and missing testing activities onto the Agile Testing Quadrants (Brian Marick, Lisa Crispin and Janet Gregory): technology- vs business-facing, supporting the team vs critiquing the product, then spot the empty quadrants and propose actions. Use when building or reviewing a test strategy, onboarding a QA, or when testing is only UI checks or only unit tests."
---

# Agile testing quadrants map

| | Supporting the team | Critiquing the product |
|---|---|---|
| **Business-facing** | **Q2**: examples, story tests, prototypes, BDD scenarios | **Q3**: exploratory testing, usability, UAT, demos, alpha/beta |
| **Technology-facing** | **Q1**: unit, component, integration tests | **Q4**: performance, load, security, accessibility, resilience ("-ility" testing) |

## Steps
1. Interview or read: list what the team actually does today, with frequency and automation level.
2. Place each activity in a quadrant; note tools and owners.
3. Find **empty or thin quadrants**. Typical gaps: Q3 done only by the PO at the end, Q4 only after an incident, Q2 replaced by UI scripts.
4. For each gap, one concrete next step and the skill to use (e.g. Q3 -> `exploratory-charter`, Q4 -> `performance-test-k6`, `accessibility-audit`).

## Output
The filled 2x2 table, the gaps, and 3-5 prioritised actions.
