---
name: property-based-tests
description: "Write property-based tests (Hypothesis for Python, fast-check for JS/TS, jqwik or FsCheck for JVM/.NET) that state invariants and let the framework search for counter-examples. Use for parsers, serializers, calculations, money/rounding, sorting, state machines, or anywhere example tests keep missing edge cases."
---

# Property-based tests

## Find properties
| Pattern | Example |
|---|---|
| Round trip | `parse(format(x)) == x` (CSV, JSON, dates, amounts) |
| Invariant | Sum of invoice lines == invoice total; balance of debits == credits |
| Idempotence | `normalize(normalize(x)) == normalize(x)` |
| Oracle / reference | Optimised function == simple slow implementation |
| Metamorphic | Adding a 0-amount line does not change the total; sorting twice == sorting once |
| No crash | Any input of the right type -> no exception other than documented ones |

## Steps
1. Pick 2-4 properties for the unit under test; say why each matters.
2. Write generators that respect the domain (e.g. amounts as integers of cents, dates within the fiscal year), plus `assume()` for preconditions.
3. Run with enough examples (`max_examples=500` for critical code).
4. When a counter-example is found, keep the **shrunk** failing input as a regular example test.

## Output
Test code, the properties in plain words, and any counter-example found with its explanation.
