---
name: dora-metrics-review
description: "Facilitate a monthly DORA metrics review that leads to learning instead of gaming: trends with context, throughput and instability read together, outliers explained by the team, one improvement experiment, and guardrails against misuse (no team rankings, no individual targets). Includes how to read DORA alongside AI coding adoption. Use for monthly team or department delivery reviews."
---

# DORA metrics review (45 min)

## Agenda
1. **Trends (10 min)**: the five metrics over 6-12 months, throughput and instability **side by side**. Faster with more failures is not progress.
2. **Outliers (10 min)**: the team explains spikes (holidays, migration, incident, process change). Write the explanation on the chart.
3. **Experiment check (10 min)**: did last month's experiment move its metric? Keep, adapt, drop.
4. **Next experiment (10 min)**: one, from `dora-capabilities-plan`.
5. **Close (5 min)**: what we tell stakeholders.

## Guardrails
- Metrics belong to the team. No ranking of teams, no individual targets, no bonuses on DORA numbers (Goodhart's law).
- Look at all five together; a single metric can always be gamed.
- Small samples: say "n = 6 deployments" next to the percentage.

## Reading AI coding adoption
The DORA 2024 report found higher AI adoption associated with slightly *lower* delivery throughput and stability on average, while individuals reported higher productivity. When AI tools ramp up, watch change lead time **and** change fail rate and rework rate together, plus review time on PRs: more code is not more delivery if verification becomes the bottleneck.

## Output
Review notes template, the charts to prepare, and the experiment card.
