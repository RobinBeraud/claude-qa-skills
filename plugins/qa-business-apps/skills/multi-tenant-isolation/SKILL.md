---
name: multi-tenant-isolation
description: "Test that a multi-tenant SaaS never leaks or mixes data between tenants (customers, companies, subsidiaries): ID guessing on APIs, list filters, search indexes, exports, caches, background jobs, file storage, reports and AI features. Use for any SaaS feature touching tenant data, before onboarding a large customer, or after a data-access refactor."
---

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
