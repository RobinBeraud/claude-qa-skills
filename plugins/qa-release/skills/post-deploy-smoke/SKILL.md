---
name: post-deploy-smoke
description: "Design a short post-deployment smoke and verification plan: the 10-20 checks that prove a deployment is healthy in minutes (critical journeys, integrations, background jobs, monitoring signals) with owners, expected results and a rollback trigger. Use before a deployment window, a hotfix, or a migration go-live."
---

# Post-deployment smoke plan

## Steps
1. List the **critical journeys** (log in, the 3 money-making flows, the most used screen) and pick one read-only or reversible check per journey.
2. Add **integrations**: payment, e-invoicing platform, identity provider, e-mail, exports to third parties.
3. Add **background work**: scheduled jobs, queues draining, batch outputs.
4. Add **signals**: error rate, latency, logs for new exceptions, business counters (orders, invoices created) compared with the same hour last week.
5. Define the **rollback trigger** in numbers (e.g. error rate > 2 % for 10 min, any data corruption, login failure).
6. Order by speed: automated checks first, then manual ones; total under 30 minutes.

## Output
| # | Check | How (automated / manual, command or URL) | Expected | Owner | Max time |
plus the rollback trigger and who decides. Never use real customer actions that cannot be undone (payments, outgoing invoices) as smoke tests.
