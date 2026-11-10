---
name: ebm-experiment-loop
description: "Run hypothesis-driven experiments in the EBM loop: from a goal and its measures, write a falsifiable hypothesis, define the smallest experiment, the measure and threshold that would confirm or refute it, run it, inspect the evidence and adapt (persevere, pivot or stop). Use when deciding what to build next, when the backlog is a list of assumptions, or to replace feature roadmaps with learning."
---

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
