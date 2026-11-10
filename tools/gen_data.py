from _gen import write_plugin

PLUGIN = "dev-data"
DESC = "Data layer of business software: SQL Server query tuning from execution plans and Query Store, zero-downtime schema changes, multi-tenant isolation checks, and GDPR (RGPD) built into the code: minimisation, retention, pseudonymisation, rights of access and erasure, logs without personal data."

S = {}

S["sql-server-tuning"] = ("""Diagnose and fix slow SQL Server queries: read the actual execution plan, find scans, key lookups, spills and bad estimates, use Query Store to find regressions and plan changes, handle parameter sniffing, design covering indexes without over-indexing, and check statistics; measure logical reads before and after. Use when a query, report, batch or endpoint backed by SQL Server is slow, when CPU or blocking spikes, or when reviewing indexes.""", r"""
# SQL Server tuning

## Measure
```sql
SET STATISTICS IO, TIME ON;   -- logical reads and CPU per statement
-- run the query, keep the ACTUAL execution plan
```
Query Store: "Top resource consuming queries" and "Regressed queries" show what got worse and when (a plan change after a deployment or a statistics update).

## Read the plan, right to left
| You see | Usually means | Try |
|---|---|---|
| Index scan on a big table with a selective `WHERE` | no usable index, or non-sargable predicate | index on the filter columns; remove functions on columns (`WHERE YEAR(d)=2026` -> range) |
| Key lookup executed thousands of times | index lacks columns | covering index with `INCLUDE` |
| Estimated rows << actual rows | stale statistics, parameter sniffing, table variables | update statistics; `OPTION (RECOMPILE)` or `OPTIMIZE FOR` on that statement; temp tables |
| Sort/hash with warning (spill) | memory grant too small, bad estimate | fix estimates first |
| Implicit conversion warning | type mismatch (`nvarchar` parameter vs `varchar` column) | align parameter types (EF: column types, Dapper: `DbString`) |

## Rules
- One change at a time; compare logical reads and duration on production-like data volume.
- Every new index has a cost on writes: check existing indexes for overlap (`sys.dm_db_index_usage_stats`).
- Blocking: look at the head blocker and the transaction length, not only the waiting query.
- Never tune on an empty dev database.
""")

S["zero-downtime-schema"] = ("""Change a production database schema without downtime or data loss: expand and contract, backward-compatible steps across deployments, batched backfills, online index operations, renames through new columns, dual writes when needed, and a rollback plan per step; independent of the ORM. Use when renaming, splitting or dropping columns and tables, changing types or constraints, or planning a migration on a large live table.""", r"""
# Zero-downtime schema changes

Rule: at every moment, the **running** version of the code and the **next** one must both work with the schema.

## Patterns
| Change | Safe sequence |
|---|---|
| Add column | nullable or with default -> deploy code that writes it -> backfill -> make NOT NULL later if needed |
| Rename column | add new -> write both -> backfill -> read new -> stop writing old -> drop old (later release) |
| Change type | new column with new type, same as rename |
| Drop column | stop reading -> stop writing -> deploy -> drop in a later release |
| Add NOT NULL / FK / unique | clean the data first, then add the constraint (`WITH NOCHECK` + validate later on huge tables, where supported) |
| Split a table | new table, dual write, backfill, switch reads, stop old writes |

## Backfill
Batches (1-10k rows), commit per batch, resumable (by key range), throttled, logged; run off-peak; check replication or log growth.

## Large tables
Online index create/rebuild where the edition allows; avoid long schema locks; rehearse on a production-sized copy and time it.

## Checklist per step
SQL reviewed, rollback written, duration measured, monitoring ready, owner on call.
""")

S["multi-tenant-safety"] = ("""Prevent data leaks between customers in multi-tenant applications: find every query, cache key, file path, search index, background job and log that must carry the tenant, check global query filters and row-level security, write cross-tenant tests, and review new code for missing tenant scoping. Use when building or reviewing a SaaS feature, adding an endpoint, a batch job, a cache or an export, or after a suspected cross-tenant incident.""", r"""
# Multi-tenant safety

A cross-tenant leak is the worst incident a SaaS can have: one customer seeing another's invoices or payroll.

## Where the tenant must travel
- **Queries**: every table with tenant data filtered by tenant. Prefer a central mechanism: EF Core global query filters, SQL Server row-level security, schema or database per tenant. Search for `IgnoreQueryFilters()` and raw SQL: each one needs a justification.
- **Caches**: tenant id in every cache key (`tenant:{id}:invoice:{n}`).
- **Files and blobs**: tenant in the path and in the access check, never only an obscure URL.
- **Background jobs and messages**: tenant in the payload; the job re-establishes the tenant context before any query.
- **Search indexes, reports, exports**: filtered by tenant at query time.
- **Logs and traces**: tenant id as a structured field (useful), no other tenant's data.

## Review checklist for a change
1. Where does the tenant come from? From the authenticated identity, **never** from a request parameter the user controls.
2. Every new query, cache, file, job: tenant-scoped?
3. Admin or support tools that cross tenants: separate, audited, least privilege.

## Tests
- Integration test pattern: create data for tenants A and B, act as A, assert nothing of B is returned (lists, by-id access -> 404, exports, search).
- Run these tests on every new endpoint (a test template helps); `qa-business-apps:multi-tenant-isolation` designs the full test set.
""")

S["gdpr-by-design"] = ("""Build GDPR (RGPD) compliance into code: map personal data in the schema, minimise what is collected, retention periods with automatic purge, pseudonymisation and encryption, access and erasure requests (with legal retention exceptions such as accounting and payroll), consent where needed, personal data out of logs and test datasets. Use when designing a feature that touches personal data, adding fields, logs or exports, preparing a data protection review, or implementing a subject access or erasure request.""", r"""
# GDPR by design

Not legal advice: decisions on legal bases and retention belong to the DPO. The code must make them enforceable.

## Steps for a feature
1. **Inventory**: which personal data (identity, contact, bank details, salary, health, NIR...), whose (employees, customers' customers), why (purpose), legal basis (contract, legal obligation, consent...). Write it in the PR or the data map.
2. **Minimise**: collect only what the purpose needs; no "might be useful" fields.
3. **Retention**: a period per data category, and a job that purges or anonymises after it. Accounting, invoicing and payroll data often have legal retention obligations (e.g. 10 years for accounting records in France): keep, but restrict access.
4. **Protect**: encryption in transit and at rest; field-level encryption or pseudonymisation for sensitive data (bank details, NIR, health); access by role, audited.
5. **Rights**: access (export the person's data in a readable format), rectification, erasure (delete or anonymise, except data under legal retention), portability. Implement them as tested functions, not manual SQL.
6. **Logs and observability**: no names, e-mails, IBANs or free text with personal data in logs, traces or error messages; ids instead.
7. **Non-production**: test and demo data synthetic or anonymised; never copy production personal data to dev or to an AI tool without approval.

## Review checklist
New personal field justified? Retention defined? Purge implemented and tested? Logged anywhere? Exported anywhere? Shared with a third party (processor contract)?
""")

write_plugin(PLUGIN, DESC, S, ["sql-server", "database", "multi-tenant", "gdpr", "rgpd"])
