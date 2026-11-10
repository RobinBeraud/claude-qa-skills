---
name: feature-flags
description: "Use feature flags to ship safely: choose the flag type (release, experiment, operational kill switch, permission or tenant), implement with a flag library or Azure App Configuration, roll out by tenant or percentage, test both paths, and remove flags once fully released to avoid flag debt. Use when shipping a risky change, decoupling deployment from release, doing a pilot with some customers, or cleaning up old flags."
---

# Feature flags

## Types
| Type | Lifetime | Example |
|---|---|---|
| Release | days to weeks | new invoice screen hidden until ready |
| Pilot / tenant | weeks | enabled for 3 pilot customers |
| Experiment | duration of a test | A/B on onboarding |
| Operational kill switch | permanent | disable PDF generation if the service is down |
| Permission | permanent | paid option (this is entitlement, keep it separate) |

## Implementation
- .NET: `Microsoft.FeatureManagement` (filters for percentage, time window, targeting by tenant), backed by Azure App Configuration or config files. Front-end: read flags from the back end, never trust them for security.
- Evaluate once per request and pass the result down; no flag checks deep in loops.
- Default **off** for new features; kill switches default to the safe state.

## Testing
Both paths tested in CI while the flag lives. Production tests cover the "on" path for pilot tenants.

## Flag debt
Every release flag has an owner and a removal date in its work item. Remove the flag and the dead branch within one release after 100 % rollout (see `dev-legacy:dead-code-removal`).
