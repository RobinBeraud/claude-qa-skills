---
name: mutant-killer-tests
description: "Write the smallest, clearest tests that kill a list of surviving mutants (from a report or a triage), one behaviour per test, reusing existing fixtures, then re-run mutation testing on the file to prove each mutant is killed. Use after surviving-mutant-triage, or to harden tests around critical calculations."
---

# Tests that kill mutants

## Steps
1. Group survivors by behaviour (several mutants often fall to one good test).
2. For each group, write a test named after the **behaviour**, not the mutant (`test_fee_applies_from_the_day_after_due_date`, not `test_kill_mutant_42`).
3. Use the distinguishing input found in triage; assert the exact expected value.
4. Run the normal suite (green), then the mutation tool on the file only (incremental mode if available).
5. Report: mutants killed, still surviving (with reason), score before/after for the file.

## Rules
- Never assert on implementation details just to kill a mutant; if only an internal detail distinguishes the mutant, it is probably equivalent or the code is too clever.
- Keep tests readable for humans: they are documentation of the rule.
