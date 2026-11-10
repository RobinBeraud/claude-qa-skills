---
name: ebm-key-value-measures
description: "Choose a small, balanced set of key value measures across the four EBM key value areas (Current Value, Unrealized Value, Time to Market, Ability to Innovate) from the EBM guide's examples, adapted to the product, with data source, frequency and owner. Use when setting up EBM, building a product dashboard, or replacing output metrics (velocity, story points) with value measures."
---

# EBM key value measures

## Four key value areas (KVAs) and example measures
| KVA | Question | Example measures |
|---|---|---|
| **Current Value (CV)** | How much value does the product deliver today? | Customer satisfaction (NPS, CSAT), revenue per employee, product cost ratio, employee satisfaction, customer usage index |
| **Unrealized Value (UV)** | How much more value could it deliver? | Market share, customer or user satisfaction gap, desired customer experience, potential revenue |
| **Time to Market (T2M)** | How fast can we deliver and learn? | Release frequency, lead time, cycle time, release stabilization period, mean time to repair, time to learn |
| **Ability to Innovate (A2I)** | How effectively can we deliver new value? | Innovation rate (share of effort on new value), defect trends, technical debt, on-product index, installed version index, production incident trends, time spent context-switching, active code branches, feature usage index |

## Steps
1. Start from the goals (`ebm-goals`): which KVA does each depend on?
2. Pick **2-3 measures per KVA**, at most 10 in total; at least one per KVA so no area is invisible.
3. For each: definition, data source, frequency, owner, baseline, direction (higher/lower is better).
4. Prefer measures the team can influence and that customers would care about.
5. Plan the scorecard file for `ebm-scorecard`.

## Output
Measure catalogue table and the CSV layout to track them.
