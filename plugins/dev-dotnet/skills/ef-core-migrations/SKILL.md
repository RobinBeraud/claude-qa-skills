---
name: ef-core-migrations
description: "Create and ship Entity Framework Core migrations safely: review the generated SQL, expand and contract for zero-downtime changes (add nullable column, backfill, switch, then drop), data migrations in batches, idempotent scripts or bundles for deployment, and rollback planning. Use when changing an EF Core model, generating or reviewing a migration, renaming or dropping columns, or deploying schema changes to production."
---

# EF Core migrations

## Always read the SQL
```bash
dotnet ef migrations add AddInvoiceDueDate
dotnet ef migrations script <from> <to> --idempotent -o migration.sql
```
A rename seen as drop + add destroys data: check every `DropColumn`/`DropTable`.

## Expand and contract (no downtime, old and new code both run)
1. **Expand**: add the new column/table, nullable or with a default. Deploy.
2. **Migrate data**: backfill in batches (e.g. 5,000 rows per transaction), off-peak, resumable.
3. **Switch**: code reads and writes the new structure (feature flag if needed). Deploy.
4. **Contract**: drop the old column in a later release, once no version uses it.

## Rules
- Large tables: adding an index or a non-null column can lock; use online index options where available and test on a production-sized copy.
- Deploy with idempotent scripts or migration bundles (`dotnet ef migrations bundle`), not `Database.Migrate()` at app start-up on several instances.
- Every migration has a tested rollback path (a down script or a forward fix plan).
- Seed/reference data changes are migrations too: versioned and reviewed.
