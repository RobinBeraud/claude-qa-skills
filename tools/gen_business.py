from _gen import write_plugin

PLUGIN = "qa-business-apps"
DESC = "Test what breaks business software: accounting invariants, e-invoice (Factur-X/CII, EN 16931) consistency, money and rounding, dates and time zones, multi-tenant isolation, role permissions matrices, data migration reconciliation and localisation."

S = {}

S["accounting-invariants"] = ("""Derive and test the invariants accounting and finance software must never break: balanced double entries, trial balance, sequential numbering without gaps, closed periods immutable, VAT totals consistent, reversals and credit notes symmetric, audit trail complete. Use when testing ledgers, invoicing, payments, closing, or any change to financial calculations.""", r"""
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
""")

S["einvoice-consistency"] = ("""Check an electronic invoice in UN/CEFACT CII XML or a Factur-X PDF for EN 16931 arithmetic and mandatory-field consistency (line totals, VAT breakdown, tax basis, grand total, amount due, identifiers), with a bundled stdlib script, then list the business rules that fail. Use when testing invoice generation for the French e-invoicing reform, Factur-X/ZUGFeRD exports, or invoice import.""", r"""
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
""")

S["money-and-rounding"] = ("""Design tests for monetary calculations: decimal precision, rounding modes (half-up, half-even, truncation), per-line vs per-document VAT rounding, allocation of remainders (splitting 100.00 in 3), currency conversion and exponent, negative amounts and credit notes, and float bugs. Use when testing prices, invoices, payroll, discounts, tax, instalments or multi-currency features.""", r"""
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
""")

S["date-time-edge-cases"] = ("""Generate the date and time test cases that break business software: time zones and DST changes, end of month and leap years, fiscal years not aligned with calendar years, cut-off times, date-only vs timestamp, locale formats, week numbers and public holidays. Use when testing scheduling, billing periods, due dates, payroll, reporting by month, or any feature using now().""", r"""
# Date and time edge cases

## Checklist
| Area | Cases |
|---|---|
| Month ends | Jan 31 + 1 month; Feb 28/29; 30-day months; "last day of month" rules |
| Leap years | 2028-02-29, yearly recurrence from Feb 29, 366-day years in interest calculations |
| DST (Europe/Paris) | Last Sunday of March 02:00 -> 03:00 (02:30 does not exist); last Sunday of October 03:00 -> 02:00 (02:30 happens twice); jobs scheduled at those times |
| Time zones | User in Lisbon, server in UTC, tenant in Paris: which day is "today" at 23:30? |
| Cut-off | Order at 23:59:59 vs 00:00:00; batch running across midnight |
| Fiscal year | Year starting July 1; period 13; closing on a weekend |
| Date-only vs timestamp | A due date stored as midnight UTC shows as the previous day in America/* time zones |
| Formats | dd/mm/yyyy vs mm/dd/yyyy; ISO week 53; first day of week Monday vs Sunday |
| Holidays | Due dates moved by bank holidays (France, Spain, Portugal differ) |
| Clock in tests | Freeze the clock; never depend on the real date |

## Steps
1. Identify every date the feature reads, stores, computes or displays, and its time zone.
2. Pick the relevant rows above and write concrete cases with exact timestamps and zones.
3. Freeze or inject the clock in automated tests; run a few cases in a different machine time zone too.
""")

S["multi-tenant-isolation"] = ("""Test that a multi-tenant SaaS never leaks or mixes data between tenants (customers, companies, subsidiaries): ID guessing on APIs, list filters, search indexes, exports, caches, background jobs, file storage, reports and AI features. Use for any SaaS feature touching tenant data, before onboarding a large customer, or after a data-access refactor.""", r"""
# Multi-tenant isolation

A cross-tenant leak is a security incident and a contract breach. Test it deliberately.

## Setup
Two tenants (A and B) with similar data, users in each with the same role, and known ids for B's records.

## Cases
| Channel | Test |
|---|---|
| API by id | As user of A, GET/PUT/DELETE B's record ids -> 404/403, never 200 |
| Lists & search | A's lists, filters, full-text search and autocomplete never return B's data |
| Exports & reports | CSV/PDF exports, scheduled reports, dashboards only contain A's rows |
| Caches | Request as A, then as B: no cached response or aggregate from the other tenant |
| Background jobs | Jobs processing many tenants keep the tenant context per item (mail, invoices, imports) |
| Files | Pre-signed URLs or attachment ids of B not accessible from A; URLs expire |
| Admin / support tools | Impersonation is logged and scoped |
| AI features | Summaries, assistants and RAG retrieve only A's documents |
| Sub-entities | Companies or subsidiaries inside a tenant respect their own boundaries |

## Output
Test cases per channel with the exact request, the expected denial, and results. Any leak is a **blocker**.
""")

S["permissions-matrix"] = ("""Turn a roles x actions permission matrix (CSV) into positive and negative test cases, and compare expected permissions with observed results from a test run to list every mismatch, with a bundled stdlib script. Use when testing role-based access control, before a release that touches roles, or to audit what each profile can really do.""", r"""
# Permissions matrix

## Matrix format (CSV)
```
action,admin,accountant,viewer
invoice.create,allow,allow,deny
invoice.delete,allow,deny,deny
period.close,allow,deny,deny
```

## Commands
```bash
python "${CLAUDE_SKILL_DIR}/scripts/rbac_matrix.py" generate matrix.csv > rbac_cases.md
python "${CLAUDE_SKILL_DIR}/scripts/rbac_matrix.py" compare matrix.csv observed.csv
```
- `generate`: one test case per (role, action): allowed actions must succeed, denied ones must be refused (UI hidden **and** API refused with 403).
- `compare`: `observed.csv` has the same shape, filled from the test run. Prints each mismatch; a role allowed something it should not do is reported as `SECURITY`, the reverse as `FUNCTIONAL`. Exit 1 on any mismatch.

## Also test
Role changes taking effect immediately, users with several roles, inherited permissions, direct URL access to hidden screens, bulk actions, and API calls with a token from a lower role.
""")

S["data-migration-validation"] = ("""Validate a data migration or upgrade (legacy to new system, version upgrade, tenant onboarding): reconciliation of counts, totals and checksums per entity, sampling with field-level comparison, referential integrity, rejected-record review and business-level spot checks, plus a dry-run plan. Use before and after any data migration, import tool change or go-live with migrated data.""", r"""
# Data migration validation

## Steps
1. **Inventory** entities and mapping rules (source field -> target field, transformations, defaults).
2. **Reconcile counts** per entity and per partition (company, year, status). Every difference is explained by a rule (excluded, merged) or is a defect.
3. **Reconcile totals**: sums of amounts, balances per account, open items, quantities; must match to the cent.
4. **Checksums / hashes** on key fields per record to detect silent changes.
5. **Sample** 30-50 records per entity (random + edge: oldest, largest, special characters, nulls) and compare field by field.
6. **Integrity**: foreign keys, orphans, duplicates, unique constraints, sequences continued correctly.
7. **Rejected records**: count, reasons, decision for each category.
8. **Business spot checks** by key users: their 10 most important customers/accounts look right.
9. **Rehearse**: at least one full dry run on a copy, timed, with rollback tested.

## Output
Reconciliation table per entity (`source | target | diff | explained by`), sample results, integrity findings, and a go/no-go statement for the cut-over.
""")

S["localization-testing"] = ("""Test localisation and internationalisation for French, Spanish and Portuguese markets (and others): translations complete and in context, number, currency, date and address formats, accents and encoding in imports/exports, text expansion, sorting with diacritics, and country-specific legal mentions. Use when releasing a feature in several countries or languages, or when users report garbled characters.""", r"""
# Localisation testing

## Checklist
| Area | Cases |
|---|---|
| Translations | No missing keys or raw ids, no English left in FR/ES/PT screens, plural forms, gender agreement, context-appropriate business terms (validated by a native speaker) |
| Text expansion | Spanish/Portuguese strings can be 30 % longer: buttons, tables, PDFs, e-mails do not truncate |
| Numbers & currency | 1 234,56 EUR (fr), 1.234,56 EUR (es, pt); input accepts the local decimal separator; CSV exports document their separator |
| Dates | dd/mm/yyyy; month names; first day of week |
| Encoding | `é è ç ñ ã õ œ` and `€` survive imports, exports, PDFs, e-mails, file names; CSV opened in Excel (UTF-8 BOM) |
| Sorting & search | `Écran` sorts with `E`; accent-insensitive search finds `Élodie` with `elodie` |
| Addresses & ids | Postal code formats, NIF/NIE (ES), NIF (PT), SIREN/SIRET (FR), IBAN by country |
| Legal mentions | Invoice mandatory mentions per country, VAT wording, data-protection notices |

## Output
Findings per locale with screenshots descriptions, and a list of strings needing a native review.
""")

write_plugin(PLUGIN, DESC, S, ["erp", "accounting", "e-invoicing", "saas", "rbac", "i18n"])
