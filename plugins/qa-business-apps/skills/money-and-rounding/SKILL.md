---
name: money-and-rounding
description: "Design tests for monetary calculations: decimal precision, rounding modes (half-up, half-even, truncation), per-line vs per-document VAT rounding, allocation of remainders (splitting 100.00 in 3), currency conversion and exponent, negative amounts and credit notes, and float bugs. Use when testing prices, invoices, payroll, discounts, tax, instalments or multi-currency features."
---

# Money and rounding

## Rules of thumb
- Money is never a binary float. `0.1 + 0.2 != 0.3` in float; use decimal types or integer minor units.
- Rounding mode and **where** rounding happens (per line or per total) are business rules: find them in the spec or ask.

## Test cases to always include
| Case | Example |
|---|---|
| Half-way values | 0.125 -> 0.13 (half-up) or 0.12 (half-even): which one is specified? |
| Per-line vs per-total VAT | 3 lines of 0.33 at 20 %: VAT per line 0.07 x 3 = 0.21, on total 0.99 x 20 % = 0.20 |
| Allocation remainder | Split 100.00 into 3 instalments: 33.33 + 33.33 + 33.34 = 100.00 exactly, and who gets the cent |
| Discount stacking | 10 % then 5 % vs 15 %; discount before or after VAT |
| Negative amounts | Credit notes round symmetrically: -0.125 -> -0.13 with half-up away from zero? |
| Currency exponents | JPY has 0 decimals, TND/KWD 3; conversion then rounding at the target currency's precision |
| Large values | 999,999,999.99 and overflow of the column/type |
| Zero and tiny | 0.00, 0.01, 0.005 |

## Steps
1. Write the rounding policy as a table (where, mode, precision) and get it confirmed.
2. Generate cases from the table above plus boundaries of each rate.
3. Use a **reference oracle** (spreadsheet or small decimal script) for expected values, never the code under test.
4. Add property tests: total always equals sum of rounded parts after allocation.
