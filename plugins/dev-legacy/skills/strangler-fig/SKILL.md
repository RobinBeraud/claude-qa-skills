---
name: strangler-fig
description: "Replace a legacy system or module incrementally with the strangler fig pattern: facade or proxy in front, route one capability at a time to the new implementation, keep data in sync, compare old and new outputs (parallel run), switch with feature flags, and retire the old path when traffic is zero. Use when rewriting or re-platforming a legacy module, moving from a monolith to services, or replacing an old UI or API without a big-bang cut-over."
---

# Strangler fig

## Steps
0. **Pin behaviour first** with `qa-automation:characterization-tests` on the slice you will replace.
1. **Slice by capability**, not by layer: "invoice PDF generation", "customer search". Order by value and risk; start with a small, low-risk, well-understood slice.
2. **Facade**: a single entry point (reverse proxy such as YARP, API gateway, an interface in the code) that can route each capability to old or new.
3. **Data**: decide who owns each data set during transition. Options: new reads from old DB (anti-corruption layer), change data capture to sync, or dual writes with reconciliation.
4. **Parallel run** for risky slices: send the request to both, return the old result, log differences, fix until the diff rate is ~0.
5. **Switch** with a flag per tenant or percentage (internal users -> pilot customers -> all). Monitor errors, latency, business KPIs.
6. **Retire**: when traffic on the old path is zero for a full business cycle (month-end, year-end closing for finance software), delete the old code.

## Rules
- Each slice ships to production; no long-lived rewrite branch.
- Business cycles matter: test month-end and year-end paths before retiring anything in finance or payroll software.
- Keep a visible board of slices: old / both / new / retired.
