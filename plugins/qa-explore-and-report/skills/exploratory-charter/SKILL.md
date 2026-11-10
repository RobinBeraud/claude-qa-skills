---
name: exploratory-charter
description: "Create focused exploratory testing charters (\"Explore <target> with <resources> to discover <information>\") using the SFDIPOT product elements and Whittaker's testing tours, with time-boxes and a session sheet. Use when planning exploratory testing of a feature, a release or a risky area, or when scripted tests feel blind."
---

# Exploratory testing charters

## Charter format (Elisabeth Hendrickson)
> **Explore** *target* **with** *resources / techniques* **to discover** *information*.

## Steps
1. Model the target with **SFDIPOT**: Structure (components, files), Function (what it does), Data (inputs, outputs, states), Interfaces (UI, API, imports/exports), Platform (browsers, OS, infra), Operations (how real users use it, at month-end, at scale), Time (dates, time zones, concurrency, timeouts).
2. For each risky element, write a charter. Pick a **tour** when useful:
   - *Money tour*: the features sales demos. *Landmark*: jump between key features in odd orders.
   - *Bad-data / saboteur*: hostile input, interrupted operations. *Back alley*: least-used features.
   - *Supermodel*: look only at the UI. *Couch potato*: do the minimum, accept every default.
   - *Obsessive-compulsive*: repeat actions, double submit. *Garbage collector*: visit every screen once.
3. Time-box each session (45-90 min), name a tester, list the test data needed.
4. Order charters by risk.

## Output
| # | Charter | Tour / technique | Time-box | Data needed | Risk |
plus a blank session sheet:
```
CHARTER:  TESTER:  START:  DURATION:
SETUP %  TEST %  BUG INVESTIGATION %
NOTES:
BUGS:
ISSUES / QUESTIONS:
```
