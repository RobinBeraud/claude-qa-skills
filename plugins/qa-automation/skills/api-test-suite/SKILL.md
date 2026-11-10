---
name: api-test-suite
description: "Generate an API test suite from an OpenAPI/Swagger spec or from example requests: happy paths, status codes, schema validation, authentication and authorization, validation errors, idempotency and pagination, in pytest+requests, REST Assured, Postman or Playwright request. Use when an API needs regression tests or a new endpoint lands."
---

# API test suite

## Coverage checklist per endpoint
| Area | Cases |
|---|---|
| Happy path | Valid request, response body matches schema, values are correct |
| Validation | Each required field missing, wrong type, out of range, too long; error format is consistent |
| Auth | No token -> 401; expired token -> 401; wrong role -> 403; other tenant's resource -> 404 or 403 (never 200) |
| Idempotency | Same PUT/DELETE twice; POST retry with an idempotency key if supported |
| Lists | Empty list, pagination boundaries, sort and filter combinations, max page size |
| Concurrency | Update with stale version / ETag -> 409 or 412 |
| Errors | Downstream failure returns a clean 5xx with a correlation id, no stack trace |

## Steps
1. Read the spec (or capture examples). List endpoints by risk (money, permissions, data deletion first).
2. Generate tests with fixtures that create and delete their own data. Base URL and credentials from environment variables, never hard-coded.
3. Validate response **schemas** (jsonschema / openapi-core) as well as key values.
4. Run, report coverage per endpoint and per status code.

## Output
Test files, a table `endpoint x status codes covered`, and gaps (endpoints not covered, undocumented status codes seen).
