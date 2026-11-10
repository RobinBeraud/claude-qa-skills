---
name: test-environment-strategy
description: "Design the test environment strategy: which environments exist (ephemeral per PR, integration, staging, pre-production), what each is for, how they are created and torn down, configuration parity with production, third-party stubs or sandboxes, ownership, booking and data refresh. Use when environments are a bottleneck, shared and broken, or when moving to ephemeral environments."
---

# Test environment strategy

## Steps
1. **Inventory** current environments: purpose, owner, how built, data, uptime problems, who waits for them.
2. **Target design** per need:
   | Need | Environment | Lifetime |
   |---|---|---|
   | PR checks, API/E2E smoke | Ephemeral (containers / preview env) | Per PR |
   | Cross-team integration | Shared integration | Permanent, reset nightly |
   | Release validation, performance | Staging, prod-like sizing | Permanent |
   | Customer acceptance | Pre-production with anonymized data | Per release |
3. **Parity**: same build artifacts, infrastructure as code, config differences listed explicitly.
4. **Third parties**: sandbox, contract stub (WireMock, Prism) or recorded responses, per dependency.
5. **Data**: how each environment gets data (`test-data-strategy`), refresh frequency.
6. **Operations**: who fixes it, health checks, booking rules, cost limits for ephemeral envs.

## Output
Environment map table, gaps vs today, and a migration plan in 3 steps.
