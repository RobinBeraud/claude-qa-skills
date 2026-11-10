---
name: shift-right-testing
description: "Plan shift-right testing and verification in production: feature flags and progressive delivery (canary, percentage rollout), synthetic monitoring of key journeys, observability signals as test oracles, error budgets, A/B checks and fast rollback, without testing on real customers' data carelessly. Use when pre-production testing cannot reproduce production, for risky releases, or to complement CI tests."
---

# Shift-right testing

## Building blocks
| Practice | What it gives | Guardrail |
|---|---|---|
| Feature flags | Deploy dark, enable per tenant/user | Flag removal plan, default off |
| Canary / progressive rollout | Compare new vs old version on a slice of traffic | Automatic rollback on SLO breach |
| Synthetic monitoring | Scripted journeys every few minutes in production | Dedicated test tenant, no real side effects |
| Observability as oracle | Error rate, latency, business counters per release | Dashboards per release, alerts on deviation |
| Error budgets (SLO) | Decide release speed with data | Agreed with product |
| Dogfooding / beta tenants | Real usage before general availability | Opt-in, fast feedback channel |

## Steps
1. Pick the release's riskiest change; choose the rollout pattern.
2. Define the signals and thresholds that mean "roll back" (from SLOs and business counters).
3. Write the synthetic checks for the critical journeys.
4. Rehearse the rollback.
5. Afterwards, compare signals before/after and feed findings into the test strategy.

## Output
Rollout plan, signal table with thresholds, synthetic checks list, and rollback procedure.
