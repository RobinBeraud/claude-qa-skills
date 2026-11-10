---
name: multi-tenant-safety
description: "Prevent data leaks between customers in multi-tenant applications: find every query, cache key, file path, search index, background job and log that must carry the tenant, check global query filters and row-level security, write cross-tenant tests, and review new code for missing tenant scoping. Use when building or reviewing a SaaS feature, adding an endpoint, a batch job, a cache or an export, or after a suspected cross-tenant incident."
---

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
