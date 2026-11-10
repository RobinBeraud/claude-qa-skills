---
name: repro-minimizer
description: "Shrink a failing scenario to the smallest reproduction: fewer steps, smaller data, fewer settings, by delta-debugging style halving, and identify the trigger condition. Use when a bug only appears in long sessions, big imports, specific customer data or complex configurations, before handing it to a developer."
---

# Repro minimizer

## Steps
1. Confirm the full reproduction works reliably (at least 3/3). If not, record the rate and look for timing or data dependencies first.
2. **Halve the input**: remove half of the steps, rows, files or settings; keep the half that still fails. Repeat (delta debugging).
3. **Vary one thing at a time** at the end: each remaining value -> neutral value. Note which change makes the bug disappear: that is the trigger.
4. **Generalize**: does it fail with other values of the same kind (other customer, other month, other browser)?
5. Write the minimal steps and the trigger in one sentence.

## Output
```
Original: 37 steps, 12,000-row import, tenant X
Minimal:  3 steps, 2-row import
Trigger:  a line amount with 3 decimals followed by a credit note line
Still fails on: other tenants, Chrome and Firefox
```
plus the minimal data file content.
