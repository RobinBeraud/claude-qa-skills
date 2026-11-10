---
name: einvoice-consistency
description: "Check an electronic invoice in UN/CEFACT CII XML or a Factur-X PDF for EN 16931 arithmetic and mandatory-field consistency (line totals, VAT breakdown, tax basis, grand total, amount due, identifiers), with a bundled stdlib script, then list the business rules that fail. Use when testing invoice generation for the French e-invoicing reform, Factur-X/ZUGFeRD exports, or invoice import."
---

# E-invoice consistency (CII / Factur-X)

The French e-invoicing reform makes structured invoices (Factur-X, CII, UBL) the norm; a wrong total is now a rejected invoice, not a typo. Check the arithmetic before the platform does.

## Run
```bash
python "${CLAUDE_SKILL_DIR}/scripts/cii_check.py" invoice.xml
python "${CLAUDE_SKILL_DIR}/scripts/cii_check.py" facturx.pdf      # extracts the embedded XML when it can
```
Checks (EN 16931 rule ids in brackets):
- sum of line net amounts = LineTotalAmount [BR-CO-10]
- TaxBasisTotal = LineTotal - AllowanceTotal + ChargeTotal [BR-CO-13]
- TaxTotal = sum of VAT breakdown amounts [BR-CO-14]
- GrandTotal = TaxBasisTotal + TaxTotal [BR-CO-15]
- DuePayable = GrandTotal - TotalPrepaid [BR-CO-16]
- each VAT breakdown amount = basis x rate, rounded to the cent [BR-CO-17]
- presence of invoice number, issue date, seller and buyer names, currency, seller VAT id when VAT is charged
Totals must match exactly (EN 16931); `--vat-tolerance` (default 0.01) applies only to basis x rate per VAT category. Exit code 1 when a rule fails.

## Then
- For each failure, find whether the generator rounds per line or per document, and what the spec of the receiving platform expects.
- Add the failing invoice as a regression fixture.
- This script is **not** a full schema/Schematron validator: run the official validator of your platform or the EN 16931 Schematron for complete compliance.
