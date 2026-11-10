---
name: test-data-fr
description: "Generate realistic but fake French business test data that passes real validation: SIREN/SIRET (Luhn), intra-EU VAT numbers, IBAN FR with RIB key, invoices with VAT rates 20/10/5.5/2.1 and correct rounding, using a deterministic stdlib script; it also validates identifiers. Use when tests need companies, bank details or invoices that the application will accept."
---

# French business test data

Random strings fail checksum validation; real data creates GDPR risk. This generates **valid, fictitious** data.

## Commands
```bash
python "${CLAUDE_SKILL_DIR}/scripts/fr_test_data.py" companies --count 20 --seed 42 --format csv > companies.csv
python "${CLAUDE_SKILL_DIR}/scripts/fr_test_data.py" invoices  --count 50 --seed 7  --format json > invoices.json
python "${CLAUDE_SKILL_DIR}/scripts/fr_test_data.py" validate 732829320 FR44732829320 FR7630006000011234567890189
```

## What it produces
- `companies`: name (invented), SIREN, SIRET (head office NIC 00010-style), VAT number `FRkk+SIREN`, IBAN FR with valid RIB key and check digits, postcode, city.
- `invoices`: number, issue/due dates, net amount, VAT rate, VAT amount (half-up to the cent, per line), gross.
- `validate`: says which checksum passes or fails for each identifier (SIREN/SIRET Luhn, VAT key, IBAN mod 97).

## Also generate on request
Edge records the script does not make by itself: VAT-exempt invoice (0 %), credit note (negative), invoice with 100 lines, company name with accents and apostrophes (`L'Étoile & Fils`), maximum-length fields.

## Rules
- Never use real people's identifiers. Company names are invented syllables.
- Same `--seed` gives the same data, so failures are reproducible.
