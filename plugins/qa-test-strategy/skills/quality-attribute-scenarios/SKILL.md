---
name: quality-attribute-scenarios
description: "Turn quality attributes into testable scenarios with a utility tree (from the ATAM method): source, stimulus, environment, artifact, response and response measure, prioritised by business importance and technical difficulty. Use when defining a test strategy for a new product or a major change, when architects and testers disagree about what \"performant\" or \"reliable\" means."
---

# Quality attribute scenarios

## Scenario template
| Part | Example |
|---|---|
| Source | 300 accountants |
| Stimulus | run the month-end closing report simultaneously |
| Environment | normal production load, last working day of the month |
| Artifact | reporting service |
| Response | reports generated and downloadable |
| Response measure | p95 < 60 s, no error, other screens p95 < 2 s meanwhile |

## Steps
1. Brainstorm attributes (performance, availability, security, modifiability, usability, interoperability, compliance).
2. Write 2-4 scenarios per important attribute with the template.
3. Build the **utility tree**: attribute -> refinement -> scenario, rated (business importance H/M/L, difficulty H/M/L).
4. (H,H) scenarios drive the test strategy first: each gets a test approach, environment and owner.

## Output
Utility tree, scenario table, and the test approach for the top scenarios.
