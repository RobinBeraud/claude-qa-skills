---
name: test-smell-review
description: "Review an existing test suite or a test file for smells that make tests useless or flaky: no or weak assertions, sleeps, order dependence, shared mutable state, logic in tests, over-mocking, tests that mirror the implementation, giant setups. Use when reviewing a PR's tests, auditing a legacy suite, or checking tests written by an AI agent."
---

# Test smell review

## Smells to look for
| Smell | Sign | Why it hurts |
|---|---|---|
| No / weak assertion | `assert result` / `toBeTruthy()` / only "no exception" | Passes when the code is wrong |
| Mirror test | Expected value computed with the same formula as the code | Proves nothing |
| Over-mocking | Mocks of the unit's own collaborators everywhere | Tests the mocks, breaks on refactor |
| Sleep | `sleep`, `waitForTimeout`, `Thread.sleep` | Slow and flaky |
| Order dependence | Tests share records, statics, files | Fails when run alone or in parallel |
| Conditional logic | `if`/loops in the test | The test needs its own tests |
| Mystery guest | Data from an external file or DB nobody sees | Hard to understand, breaks silently |
| Eager test | One test checks ten behaviours | Unclear what broke |
| Catch-all | `try/except: pass` around the act | Swallows the failure |
| Snapshot dump | Huge snapshots accepted blindly | Reviewers click "update" |

## Steps
1. Read the tests next to the code they test.
2. List each smell with file:line and a concrete fix (rewrite the assertion, extract a fixture...).
3. Rate the suite: **trustworthy / needs work / misleading**, with the top 3 fixes.

## Output
Findings table `file:line | smell | fix`, the rating, and rewritten examples for the two worst tests.
