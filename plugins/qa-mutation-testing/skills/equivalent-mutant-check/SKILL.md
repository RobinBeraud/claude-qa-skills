---
name: equivalent-mutant-check
description: "Decide whether a surviving mutant is equivalent (no observable behaviour change, so no test can kill it) or a real gap, using reasoning about reachable inputs, side effects and invariants; document legitimate equivalents so they stop polluting the score. Use when mutants survive that look impossible to kill."
---

# Equivalent mutant check

## Reasoning steps
1. State the original and mutated expressions.
2. Find the **input domain actually reachable** at that point (guards above, types, invariants).
3. Is there any reachable input where both versions produce a different **observable** result (return value, state, exception, call, log that matters)?
   - Yes: real gap. Give the input that distinguishes them; it becomes the new test case.
   - No: equivalent. Typical cases: `i < n` vs `i != n` in a loop that only increments by one; removed call to a pure function whose result is unused; changed log message nobody asserts.
4. For equivalents, use the tool's ignore mechanism (Stryker `// Stryker disable next-line <mutator>: reason`, PIT `excludedMethods`, mutmut `# pragma: no mutate`) **with the reason**.
5. If many equivalents appear in the same code, it is often a hint to simplify the code.

## Output
Verdict per mutant: equivalent (proof) or gap (distinguishing input and test).
