---
name: ef-core-performance
description: "Find and fix Entity Framework Core performance problems: N+1 queries, missing AsNoTracking, client-side evaluation, cartesian explosion (AsSplitQuery), unbounded result sets, missing indexes, and compiled or raw SQL when justified; with query logging to see the real SQL. Use when an endpoint or batch using EF Core is slow, when the database shows many similar queries, or when reviewing data-access code."
---

# EF Core performance

## See the SQL first
```csharp
options.LogTo(Console.WriteLine, LogLevel.Information).EnableSensitiveDataLogging(false);
```
or `ToQueryString()` on the query, and the database's own tools (SQL Server Query Store, execution plans).

## Usual causes and fixes
| Symptom | Cause | Fix |
|---|---|---|
| Hundreds of identical queries | N+1 via lazy loading or a query in a loop | `Include`, or project with `Select` in one query; disable lazy loading |
| Slow read-only list | change tracking | `AsNoTracking()` (or `AsNoTrackingWithIdentityResolution`) |
| Huge result with several `Include` | cartesian explosion | `AsSplitQuery()` or project only needed columns |
| Memory grows with data | no paging, `ToList()` too early | `Skip/Take` with a stable `OrderBy`, keyset pagination for big tables |
| Slow `Where` | missing index, non-sargable expression | index (migration), avoid functions on columns |
| Bulk updates slow | entity-by-entity `SaveChanges` | `ExecuteUpdate` / `ExecuteDelete` (EF 7+), batching |
| Same query parsed repeatedly in hot path | query compilation | `EF.CompileQuery`, or a view / raw SQL with parameters |

## Rules
- Measure before and after (duration, number of queries, logical reads).
- Raw SQL only parameterised (`FromSql($"... {id}")` interpolation is parameterised; string concatenation is not).
- Multi-tenant: check that every new query keeps the tenant filter (global query filters).
