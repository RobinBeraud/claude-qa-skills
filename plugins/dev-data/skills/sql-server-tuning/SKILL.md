---
name: sql-server-tuning
description: "Diagnose and fix slow SQL Server queries: read the actual execution plan, find scans, key lookups, spills and bad estimates, use Query Store to find regressions and plan changes, handle parameter sniffing, design covering indexes without over-indexing, and check statistics; measure logical reads before and after. Use when a query, report, batch or endpoint backed by SQL Server is slow, when CPU or blocking spikes, or when reviewing indexes."
---

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
