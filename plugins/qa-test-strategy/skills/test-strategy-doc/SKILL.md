---
name: test-strategy-doc
description: "Write a one-page team test strategy: quality goals, test pyramid and ownership per level, what runs where in CI, environments and data, definition of done for testing, exploratory testing cadence, and how AI agents are used in testing. Use when a team starts, reorganises, adopts AI coding agents, or nobody can say who tests what."
---

# Team test strategy (one page)

## Sections
1. **Context**: product, users, release cadence, main risks (link the risk storming output).
2. **Quality goals**: 3 measurable goals (e.g. "no critical escaped defect per quarter", "PR feedback in < 15 min", "change fail rate < 15 %").
3. **Levels and ownership**:
   | Level | What it proves | Owner | Runs when | Target time |
   |---|---|---|---|---|
   | Unit | Logic, calculations | Devs | Every commit | < 5 min |
   | API / integration | Contracts, persistence, permissions | Devs + QA | Every PR | < 15 min |
   | E2E | Critical journeys only | QA | Every PR (smoke) / nightly (full) | < 30 min |
   | Exploratory | Unknown risks | Whole team | Each feature, before release | time-boxed |
   | Non-functional | Performance, security, accessibility | QA + Ops | Per release / NFR | - |
4. **Environments and test data**: who owns them, how data is reset, anonymisation rules.
5. **Definition of done (testing)**: acceptance criteria automated or explicitly manual, no new flaky test, bug fixes come with a regression test.
6. **AI agents in testing**: tests written first from acceptance criteria, human review of agent-written tests, mutation score on critical modules, label on AI-assisted PRs.
7. **Feedback loop**: DORA and quality metrics reviewed monthly, escaped defects analysed.

Keep it to one page; link details elsewhere. Review it every quarter.
