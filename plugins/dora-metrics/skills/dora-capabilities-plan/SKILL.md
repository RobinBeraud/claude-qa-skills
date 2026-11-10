---
name: dora-capabilities-plan
description: "Build an improvement plan from the DORA research capabilities (technical: CI, trunk-based development, test automation, deployment automation, loosely coupled architecture, database change management, monitoring; process: small batches, WIP limits, visual management, streamlined change approval; culture: generative culture, learning, psychological safety): find the constraint and run experiments. Use after measuring DORA metrics, when a team asks how to improve them."
---

# DORA capabilities improvement plan

Metrics show *where*; capabilities show *how*. Improve one constraint at a time.

## Steps
1. Start from the metrics: which one is the weakest relative to the team's goal?
2. Map likely capabilities:
   | Weak metric | Capabilities to look at first |
   |---|---|
   | Deployment frequency | Deployment automation, small batches, streamlined change approval, trunk-based development |
   | Change lead time | CI, test automation, code review time, WIP limits, loosely coupled architecture |
   | Change fail rate / rework | Test automation, shift-left testing, code review quality, database change management, small batches |
   | Recovery time | Monitoring and observability, rollback/feature flags, proactive failure notification, incident practice |
3. Assess each candidate capability 1-5 with evidence; pick **one** constraint.
4. Write 1-3 experiments: hypothesis, change, metric expected to move, time box (4-8 weeks).
5. Review results with `dora-metrics-review`; keep, adapt or drop.

## Output
Capability assessment table, the chosen constraint with rationale, and experiment cards.
