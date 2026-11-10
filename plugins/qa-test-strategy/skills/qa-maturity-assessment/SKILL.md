---
name: qa-maturity-assessment
description: "Run a lightweight QA and test maturity self-assessment for a team across 8 dimensions (strategy, shift-left, automation, CI feedback, exploratory testing, non-functional testing, defect management, metrics and learning), score 1-5 with evidence, and derive a 90-day improvement roadmap. Use for a team health check, a coaching engagement, or before investing in QA tooling."
---

# QA maturity assessment

## Dimensions and evidence to look for
| Dimension | Level 1 | Level 5 |
|---|---|---|
| Strategy | No written strategy | One-page strategy reviewed quarterly, risk-driven |
| Shift-left | Testing starts after dev | Examples and acceptance tests before code, three amigos routine |
| Automation | Manual regression only | Pyramid-shaped suite, tests written with or before code |
| CI feedback | Nightly at best, often red | PR feedback < 15 min, green main, flaky tests quarantined |
| Exploratory | None or random | Chartered sessions per feature, debriefs |
| Non-functional | After incidents | Performance, security, accessibility in the pipeline per risk |
| Defects | Backlog of hundreds, no triage | Weekly triage, escaped defects analysed, trends known |
| Metrics & learning | None, or vanity metrics | DORA + quality metrics reviewed monthly, experiments run |

## Steps
1. Ask for evidence per dimension (artifacts, pipeline screenshots, metrics), not opinions.
2. Score 1-5 with one line of evidence each.
3. Pick the 2-3 dimensions with the best value/effort for the next 90 days.
4. Define actions, owners and how success will be measured.

## Output
Radar-ready score table, evidence notes, and the 90-day roadmap.
