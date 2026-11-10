---
name: test-design-techniques
description: "Derive test cases systematically with equivalence partitioning, boundary value analysis, decision tables, state transitions and cause-effect reasoning, then output a compact, de-duplicated test case table. Use when you need test cases for a rule, a form, a calculation, a workflow or a validation, instead of ad-hoc examples."
---

# Test design techniques

Pick the technique that matches the shape of the rule, apply it fully, then trim duplicates.

## Choose the technique
| The rule looks like | Technique |
|---|---|
| A field or numeric range | Equivalence partitions + boundary values (min-1, min, min+1, max-1, max, max+1) |
| Several conditions combine into an outcome | Decision table (one column per combination, then collapse "don't care") |
| An object moves through statuses | State transition table: valid transitions, invalid transitions, repeated events |
| Many independent parameters | Pairwise (see the `pairwise-combinations` skill) |
| A calculation | Partitions on each input + known-answer oracle + rounding edges |
| A list or collection | 0, 1, many, max, duplicates, ordering |

## Steps
1. Write the rule precisely (inputs, outputs, constraints). Ask if something is unknown.
2. Apply the chosen technique and **show the model** (partitions, decision table or state table).
3. Derive one test case per partition / column / transition; add boundaries.
4. Remove duplicates; keep the invalid cases separate (one invalid input per test, so a failure points to one cause).
5. Give the expected result for every case. If you cannot compute it, mark `ORACLE NEEDED`.

## Output
The model, then:
| ID | Technique | Inputs | Expected result | Priority |

## Quality bar
- Every boundary is tested on both sides.
- Invalid partitions are tested one at a time.
- Expected results are exact values, not "works correctly".
