---
name: tdd-red-green-refactor
description: "Drive a change with test-driven development in short red-green-refactor cycles, with Claude as a disciplined pair: write one failing test, the minimum code to pass, refactor with tests green, repeat; keeps a visible test list. Use when implementing new logic, fixing a bug the TDD way, or coaching a team on TDD with an AI agent."
---

# TDD: red, green, refactor

## Cycle (repeat, 2-10 minutes each)
1. **Test list**: write the behaviours to implement as a checklist; start with the simplest.
2. **Red**: write *one* failing test. Run it. It must fail for the expected reason (assertion, not compile error).
3. **Green**: write the minimum code that passes. Hard-coding is fine at first; the next test forces generalisation (triangulation).
4. **Refactor**: remove duplication, improve names, in code **and** tests, with all tests green. Run them.
5. Tick the item, add newly discovered cases to the list, next.

## Rules for the agent
- Never write production code without a failing test that requires it.
- Never write more than one failing test at a time.
- Show the test run after each step (red output, green output).
- Do not change a test to make it pass unless the test was wrong; say so explicitly.
- Commit at each green + refactor if the user wants small commits.

## Output
The evolving test list, each cycle's test and code diff, and the final run.
