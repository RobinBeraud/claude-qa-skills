---
name: test-automation-roadmap
description: "Decide what to automate next and in which order: score candidate test cases or journeys by frequency of execution, business risk, stability of the feature, cost to automate and flakiness risk, choose the right level (unit, API, UI), and produce a 3-month automation roadmap. Use when a team has a big manual regression, wants to start automating, or automates the wrong things."
---

# Test automation roadmap

## Scoring each candidate (1-5)
| Criterion | Question |
|---|---|
| Frequency | How often is it run (each release, each PR)? |
| Risk | What does a regression here cost? |
| Stability | Is the feature stable or still changing every sprint? |
| Cost | Effort to automate at the right level, test data included |
| Flakiness risk | Async UI, third parties, timing |
Priority = (Frequency + Risk + Stability) - (Cost + Flakiness risk).

## Steps
1. List candidates (manual regression cases, smoke checks, bug-prone areas).
2. For each, pick the **lowest level** that proves it (most UI checks are really API or unit checks).
3. Score, sort, group into monthly increments with a definition of done (runs in CI, owner, no flake over 20 runs).
4. Track: manual regression time saved, automated checks added, flaky count.

## Output
Scored candidate table, the 3-month roadmap, and the metrics to follow.
