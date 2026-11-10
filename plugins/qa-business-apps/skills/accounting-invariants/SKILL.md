---
name: accounting-invariants
description: "Derive and test the invariants accounting and finance software must never break: balanced double entries, trial balance, sequential numbering without gaps, closed periods immutable, VAT totals consistent, reversals and credit notes symmetric, audit trail complete. Use when testing ledgers, invoicing, payments, closing, or any change to financial calculations."
---

# Accounting invariants

Example-based tests check a few cases; invariants must hold for **every** entry. Test them as properties, database checks or reconciliation queries.

## Invariants checklist
| Invariant | How to check |
|---|---|
| Each journal entry balances: sum(debit) = sum(credit) | Query or property test on every posted entry |
| Trial balance: total debits = total credits per period | Report reconciliation |
| Invoice total = sum(lines) - discounts + charges + VAT | See `einvoice-consistency` and `money-and-rounding` |
| Document numbering is sequential and gap-free per series (legal requirement in France) | Sort by number per series, detect gaps and duplicates, including after failures/rollbacks |
| Posted entries and closed periods cannot be modified, only reversed | Try to edit/delete via UI and API: must fail and be logged |
| A credit note mirrors the invoice it cancels | Amounts, VAT breakdown and references match with opposite sign |
| Payments allocated never exceed the open amount | Partial, over and multi-currency payments |
| Audit trail: who, when, what for every change | Check log entries for each test action |
| FEC export (France) matches the ledger | Line counts and totals per journal/account |

## Steps
1. Pick the invariants that apply to the module under test.
2. For each, write: an automated check (property test or SQL/report reconciliation) and the hostile cases (failure mid-transaction, concurrent posting, rounding at the cent, year-end).
3. Run on test data **and** on an anonymized copy of production-like volume if possible.

## Output
Invariant list with the check for each, test code or queries, and violations found.
