from _gen import write_plugin

PLUGIN = "evidence-based-management"
DESC = "Evidence-Based Management (Scrum.org): set strategic, intermediate and immediate tactical goals, choose key value measures across the four key value areas (current value, unrealized value, time to market, ability to innovate), track them with a scorecard script, run hypothesis-driven experiments and facilitate EBM reviews."

S = {}

S["ebm-goals"] = ("""Define an Evidence-Based Management goal structure for a product or organisation: a strategic goal, intermediate goals and immediate tactical goals, each stated as a measurable outcome for customers or the business, not as an output or a feature list. Use when a product lacks clear goals, before a roadmap review, or when starting with EBM.""", r"""
# EBM goals

## Structure
- **Strategic Goal**: an ambitious, long-term outcome (often years), unlikely to be reached without big uncertainty. Example: "Accountants of small firms close their month in one day."
- **Intermediate Goals**: milestones that show progress toward it (months). Example: "50 % of pilot firms close in under 3 days."
- **Immediate Tactical Goals**: what the team pursues now (weeks, a Sprint or a few). Example: "Bank reconciliation for the top 3 banks runs without manual matching."

## Steps
1. Write the strategic goal as an outcome for a specific customer, with a measure.
2. Derive 2-4 intermediate goals that would be evidence of progress.
3. Pick the next immediate tactical goal; check it is testable within weeks.
4. For each goal, name the measure that will tell you it is reached (`ebm-key-value-measures`).
5. Check for outputs in disguise: "deliver module X" is not a goal; "customers do Y faster" is.

## Output
Goal tree with measures and target dates, plus the assumptions behind each goal (what must be true).
""")

S["ebm-key-value-measures"] = ("""Choose a small, balanced set of key value measures across the four EBM key value areas (Current Value, Unrealized Value, Time to Market, Ability to Innovate) from the EBM guide's examples, adapted to the product, with data source, frequency and owner. Use when setting up EBM, building a product dashboard, or replacing output metrics (velocity, story points) with value measures.""", r"""
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
""")

S["ebm-scorecard"] = ("""Track Evidence-Based Management measures over time with a bundled stdlib script: from a CSV of measurements (period, key value area, measure, value, direction) it computes the latest value, change vs previous period and vs baseline, an improving / worsening / flat signal per measure and a summary per key value area. Use for monthly or quarterly EBM reviews or a product value dashboard.""", r"""
# EBM scorecard

## CSV format
```
period,kva,measure,value,direction
2026-Q1,CV,Customer satisfaction (CSAT),7.6,higher
2026-Q1,T2M,Lead time (days),21,lower
2026-Q2,CV,Customer satisfaction (CSAT),7.9,higher
2026-Q2,T2M,Lead time (days),17,lower
```
`kva` is one of CV, UV, T2M, A2I. `direction` says whether higher or lower is better.

## Run
```bash
python "${CLAUDE_SKILL_DIR}/scripts/ebm_scorecard.py" ebm.csv --threshold 5
```
`--threshold` (percent) below which a change counts as flat.

## Output and reading
- Per measure: baseline, previous, latest, change vs previous and baseline, signal.
- Per KVA: how many measures improve, worsen or stay flat.
- Then discuss with the team: which goal hypothesis do these signals support or contradict? Which experiment next (`ebm-experiment-loop`)?
""")

S["ebm-experiment-loop"] = ("""Run hypothesis-driven experiments in the EBM loop: from a goal and its measures, write a falsifiable hypothesis, define the smallest experiment, the measure and threshold that would confirm or refute it, run it, inspect the evidence and adapt (persevere, pivot or stop). Use when deciding what to build next, when the backlog is a list of assumptions, or to replace feature roadmaps with learning.""", r"""
# EBM experiment loop

## Experiment card
```
Goal:        <immediate tactical goal>
Hypothesis:  We believe that <change> for <users> will result in <outcome>.
             We will know it when <measure> moves from <baseline> to <threshold> by <date>.
Experiment:  smallest thing to build or do (prototype, feature flag to 10 % of tenants, manual concierge test)
Measure(s):  primary + a guardrail measure that must not worsen
Time box:    2-6 weeks
Decision rule: persevere if ..., pivot if ..., stop if ...
```

## Steps
1. Turn the top backlog items into hypotheses; drop those that do not serve a goal.
2. Size the experiment to answer the question cheaply.
3. Agree the decision rule **before** the data comes in.
4. Run, collect evidence, update the scorecard.
5. Inspect and adapt: write down what was learned, even when the hypothesis is refuted.

## Output
Experiment cards for the next cycle and, after the run, a result card with the decision.
""")

S["ebm-review"] = ("""Facilitate an Evidence-Based Management review with stakeholders (monthly or quarterly): progress toward goals, key value area signals, results of experiments, decisions on investment and next goals, without vanity metrics or blame. Use for product reviews, portfolio reviews, or steering committees that want evidence instead of status reports.""", r"""
# EBM review (60-90 min)

## Agenda
1. **Goals (10 min)**: strategic and intermediate goals, are they still right?
2. **Evidence (20 min)**: scorecard by KVA (`ebm-scorecard`), the 3 biggest movements and their explanations.
3. **Experiments (20 min)**: what we tried, what we learned, decisions taken (persevere, pivot, stop).
4. **Investment decisions (15 min)**: where to put more, less, or stop; trade-offs between current value and ability to innovate.
5. **Next immediate tactical goals and experiments (10 min)**.

## Guardrails
- Discuss outcomes and learning, not activity (story points, hours, number of features).
- A worsening measure is information, not a fault: ask what changed.
- Every decision ties back to a goal and a measure.

## Output
Pre-read template (one page), facilitation script, and the decision log template.
""")

write_plugin(PLUGIN, DESC, S, ["ebm", "evidence-based-management", "scrum", "product-management", "metrics"])
