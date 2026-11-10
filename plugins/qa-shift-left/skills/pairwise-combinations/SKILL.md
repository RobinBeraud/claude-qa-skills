---
name: pairwise-combinations
description: "Generate a small all-pairs (pairwise) test set covering every pair of parameter values, with a bundled stdlib Python script, plus constraints to exclude impossible combinations. Use for configuration matrices (browser x OS x role x language), feature flags, or any form with many independent options."
---

# Pairwise combinations

Most defects are triggered by one parameter or an interaction of two. Pairwise covers every pair with a fraction of the full matrix.

## Steps
1. List parameters and their values. Keep values representative (partitions), not exhaustive.
2. Write constraints for impossible combinations, e.g. `os=iOS & browser=Edge`.
3. Run the script:
   ```bash
   python "${CLAUDE_SKILL_DIR}/scripts/pairwise.py" params.json --format md
   ```
   `params.json`:
   ```json
   {"parameters": {"browser": ["Chrome","Firefox","Safari"], "role": ["admin","accountant","viewer"], "lang": ["fr","es","pt"]},
    "exclude": [{"browser": "Safari", "role": "viewer"}],
    "seed": 1}
   ```
4. Report the number of rows versus the full product, and the pairs that a constraint made impossible.
5. Add by hand any **high-risk triple** the business cares about (pairwise does not cover triples).

## Output
A Markdown or CSV table, one row per test configuration, and a one-line coverage summary from the script.

## Notes
The script is greedy (not optimal) but deterministic for a given seed; it verifies that every allowed pair is covered and exits non-zero otherwise.
