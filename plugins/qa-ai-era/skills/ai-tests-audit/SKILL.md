---
name: ai-tests-audit
description: "Audit a test suite or a batch of tests written by an AI agent: do they fail when the code is wrong? Combine a test-smell scan, a deliberate fault-injection (mini mutation) pass on the code under test, and a check of coverage of the acceptance criteria. Use when an agent produced many tests quickly, or coverage jumped suspiciously."
---

# Audit AI-written tests

High coverage from an agent can mean tests written to pass. Check that they can fail.

## Steps
1. **Smell scan** (see `test-smell-review`): no assertions, mirrored expectations, over-mocking, snapshot dumps.
2. **Fault injection**: in a scratch branch, make 5-10 small wrong changes to the code under test (flip a comparison, off-by-one, drop a rounding, skip a permission check, return early). Run the tests after each. Every change that survives is a missing assertion. Revert all changes afterwards. Use a real mutation tool when available (`mutation-testing`).
3. **Criteria coverage**: map acceptance criteria to tests; list criteria without a test.
4. **Determinism**: run the new tests 5 times and in random order.

## Output
| Injected fault | Caught? | Missing assertion |
plus smells found, uncovered criteria, and a verdict: trustworthy / needs work / misleading.
