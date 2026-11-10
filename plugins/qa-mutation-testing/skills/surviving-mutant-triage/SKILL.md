---
name: surviving-mutant-triage
description: "Triage surviving mutants one by one: classify each as missing assertion, missing test case, equivalent mutant, or dead/unreachable code, explain why the tests did not notice the change, and propose the smallest fix (a test, an assertion, or deleting code). Use after a mutation run, when reviewing test quality, or when auditing tests written by an AI agent."
---

# Surviving mutant triage

## For each survivor
1. Read the mutated line and the change (e.g. `>=` became `>`, `+` became `-`, a call removed, a return replaced by `null`).
2. Find the tests that execute that line (coverage report or by name).
3. Classify:
   | Class | Meaning | Action |
   |---|---|---|
   | Missing assertion | A test runs the line but does not check the result | Add the assertion |
   | Missing case | No test hits the distinguishing input (e.g. the exact boundary) | Add a test case |
   | Equivalent mutant | The change does not alter behaviour (see `equivalent-mutant-check`) | Mark ignored with a comment |
   | Dead code | The line can never matter | Delete it |
4. Write the fix and re-run the tool on that file to confirm the mutant is now killed.

## Output
| File:line | Mutation | Class | Fix | Killed after fix? |
