---
name: escaped-defect-rca
description: "Run a blameless root-cause analysis of a defect that reached production: timeline, how it was introduced, why each test layer and review missed it, contributing factors, and concrete prevention actions (a test, a check, a process change) with owners. Use after a production incident or a customer-reported bug worth learning from."
---

# Escaped defect analysis

## Steps
1. **Facts**: what customers saw, since when, how many affected, how it was detected (customer, monitoring, support).
2. **Timeline**: change that introduced it (commit/PR), reviews, test runs, deployment, detection, fix.
3. **Why it escaped**, layer by layer: requirement (was the case known?), unit, API, E2E, exploratory, code review, monitoring. For each: would a reasonable check here have caught it? Why not?
4. **Contributing factors**: time pressure, missing test data, environment gaps, AI-generated code accepted without reading, unclear ownership. No names, no blame.
5. **Actions**: at most 3, each concrete, owned and dated: e.g. "add a property test on VAT rounding", "add monitoring on export errors", "add the case to the refinement checklist".
6. **Detection**: how to find this class of bug faster next time.

## Output
Incident summary, timeline table, "where it could have been caught" table, actions table (`action | owner | due | done when`).
