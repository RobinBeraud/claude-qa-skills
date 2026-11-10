---
name: characterization-tests
description: "Pin down the current behaviour of legacy or untested code with characterization (golden master / approval) tests before refactoring or letting an agent change it: capture outputs for a wide input set, store them, and fail on any difference. Use before touching legacy code, migrating a calculation, or a big refactor."
---

# Characterization tests

You do not know if the current behaviour is right, but you know it is what customers have today.

## Steps
1. Find the **seam**: a function, endpoint or batch whose inputs and outputs you can capture.
2. Build a wide input set: real anonymized samples, boundaries, random but seeded inputs (pairwise on options).
3. Record outputs to files (approval testing: ApprovalTests, `syrupy`, Jest snapshots, or plain JSON).
4. Make output stable: sort collections, freeze time, round floats explicitly, strip ids.
5. Commit the golden files. Any refactor must keep them identical; an intended change updates them in a reviewed commit that explains why.
6. Note behaviours that look like bugs in a list instead of fixing them during the refactor.

## Output
Test harness, golden files, and "suspicious behaviours" list for the product owner.
