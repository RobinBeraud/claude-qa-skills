---
name: parameterized-tests
description: "Collapse repetitive unit tests into parameterised, table-driven tests (pytest.mark.parametrize, JUnit @ParameterizedTest, xUnit Theory/InlineData, Jest test.each, Go table tests) with readable case ids, and fill the table with boundary and error cases. Use when tests are copy-pasted with different values, or for validation, calculation and mapping rules."
---

# Parameterised tests

## Steps
1. Find tests that differ only by data. Extract the inputs and the expected outcome.
2. Build a **table** with one row per case and a readable **id** (`"due date + 1 day"`, not `case3`).
3. Add rows from test design: partitions, both sides of each boundary, invalid values, null/empty, maximum.
4. Keep error cases in a **separate** parameterised test (different assertion: raises / returns error).
5. Run; make sure the failure output names the failing row.

## Example (pytest)
```python
@pytest.mark.parametrize("amount, days_late, fee", [
    pytest.param(Decimal("100.00"), 0, Decimal("0.00"), id="on due date"),
    pytest.param(Decimal("100.00"), 1, Decimal("40.00"), id="one day late"),
    pytest.param(Decimal("0.00"),   30, Decimal("0.00"), id="zero amount"),
])
def test_late_fee(amount, days_late, fee):
    assert late_fee(amount, days_late) == fee
```
## Pitfall
Do not hide logic in the table (computed expected values); expected values are literals.
