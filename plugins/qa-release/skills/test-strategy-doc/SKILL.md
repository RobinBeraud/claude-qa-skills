---
name: test-strategy-doc
description: "Write a one-page team test strategy: quality goals, test pyramid and ownership per level, what runs where in CI, environments and data, definition of done for testing, exploratory testing cadence, and how AI agents are used in testing. Use when a team starts, reorganises, adopts AI coding agents, or nobody can say who tests what."
---

# Team test strategy (one page)

## Sections
1. **Quality goals**: 3 measurable goals (e.g. "no critical escaped defect per quarter", "PR feedback in < 15 min").
2. **Levels and ownership**:
   | Level | What it proves | Owner | Runs when | Target time |
   |---|---|---|---|---|
   | Unit | Logic, calculations | Devs | Every commit | < 5 min |
   | API / integration | Contracts, persistence, permissions | Devs + QA | Every PR | < 15 min |
   | E2E | Critical journeys only | QA | Every PR (smoke) / nightly (full) | < 30 min |
   | Exploratory | Unknown risks | Whole team | Each feature, before release | time-boxed |
   | Non-functional | Performance, security, accessibility | QA + Ops | Per release / NFR | - |
3. **Environments and test data**: who owns them, how data is reset, anonymisation rules.
4. **Definition of done (testing)**: acceptance criteria automated or explicitly manual, no new flaky test, bug fixes come with a regression test.
5. **AI agents in testing**: tests written first from acceptance criteria, human review of agent-written tests, mutation score on critical modules, label on AI-assisted PRs.
6. **Feedback loop**: metrics reviewed monthly (`qa-flow-metrics`), escaped defects analysed (`escaped-defect-rca`).

Keep it to one page; link details elsewhere.
