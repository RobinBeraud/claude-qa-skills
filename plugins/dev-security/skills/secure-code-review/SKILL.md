---
name: secure-code-review
description: "Review a diff or a module for security flaws, focused on business web applications: broken access control and IDOR, injection (SQL, command, LDAP, XPath), XSS in Angular templates and bypassSecurityTrust, CSRF, insecure deserialisation, SSRF, file upload and path traversal, authentication and session handling, secrets and sensitive data exposure, with evidence and a fix per finding. Use when reviewing a pull request that touches endpoints, authentication, files, queries or user input, or when asked for a security review."
---

# Secure code review

## Approach
1. **Entry points** in the diff: controllers/endpoints, message handlers, file imports, scheduled jobs reading external data.
2. Follow **untrusted data** from each entry point to sinks (database, shell, file system, HTML, HTTP calls, deserialiser).
3. Check **authorisation** at each operation on a resource, server-side, including tenant scoping.

## Checklist (.NET / Angular)
| Risk | Look for | Fix |
|---|---|---|
| Broken access control / IDOR | `GET /invoices/{id}` without checking ownership or tenant | resource-based authorisation, tenant filter |
| SQL injection | string concatenation in SQL, `FromSqlRaw` with interpolated input | parameters, `FromSql` interpolation, stored procedures with parameters |
| XSS | `[innerHTML]`, `bypassSecurityTrustHtml`, Razor `@Html.Raw` | Angular sanitisation, encode output, CSP |
| CSRF | cookie auth + state-changing GET or no antiforgery token | antiforgery, SameSite cookies, no GET side effects |
| Deserialisation | `BinaryFormatter`, `TypeNameHandling.All` | System.Text.Json, no polymorphic type names from input |
| SSRF | server fetches a user-provided URL | allow-list hosts, block internal ranges |
| File upload / path traversal | user file name used in a path, no type/size check | generated names, `Path.GetFileName`, size limit, content check, storage outside web root |
| Sensitive data | personal data or secrets in logs, errors, URLs | ids only, generic error messages |
| Crypto | MD5/SHA1 for passwords, custom crypto, hard-coded keys | ASP.NET Identity hasher / PBKDF2+, Key Vault |

## Output
Findings: severity, location, exploit scenario in one sentence, fix, test to add. State what was **not** reviewed.
