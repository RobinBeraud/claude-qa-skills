---
name: test-data-strategy
description: "Define how tests get their data: synthetic generation, anonymised production extracts, fixtures per test, seeded reference data, data reset between runs, GDPR constraints on personal data, and ownership. Use when tests fail because of data, when someone wants to copy production into test, or when building a new test environment."
---

# Test data strategy

## Principles
- **Each automated test creates the data it needs** (via API or fixtures) and does not depend on data left by others.
- **Reference data** (countries, VAT rates, charts of accounts) is seeded and versioned with the code.
- **Production data** never lands in test environments raw: anonymise (irreversibly), minimise, and document the legal basis (GDPR). Prefer synthetic data.
- **Volume data** for performance tests is generated, with realistic distributions.

## Steps
1. List data needs per test level and environment.
2. Choose the source per need: synthetic (`test-data-fr`), fixtures, anonymised extract, generated volume.
3. Define reset: transaction rollback, per-test tenant, database snapshot restore, nightly refresh.
4. Assign owners and write the anonymisation rules (which fields, which technique: masking, shuffling, fake values, keeping formats and checksums valid).
5. Check: no real names, e-mails, IBANs or national ids in test environments (scan regularly).

## Output
Data matrix (need -> source -> reset -> owner), anonymisation rules, and the compliance checklist.
