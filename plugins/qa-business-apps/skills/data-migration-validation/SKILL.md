---
name: data-migration-validation
description: "Validate a data migration or upgrade (legacy to new system, version upgrade, tenant onboarding): reconciliation of counts, totals and checksums per entity, sampling with field-level comparison, referential integrity, rejected-record review and business-level spot checks, plus a dry-run plan. Use before and after any data migration, import tool change or go-live with migrated data."
---

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
