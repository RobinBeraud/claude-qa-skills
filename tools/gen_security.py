from _gen import write_plugin

PLUGIN = "dev-security"
DESC = "Secure development for business applications: security review of a diff (OWASP Top 10 in .NET and Angular), STRIDE threat modelling of a feature, insecure defaults hunting, software supply chain checks (SBOM, licences, dependency confusion), and secrets kept out of code with a bundled scanner for diffs and repositories."

S = {}

S["secure-code-review"] = ("""Review a diff or a module for security flaws, focused on business web applications: broken access control and IDOR, injection (SQL, command, LDAP, XPath), XSS in Angular templates and bypassSecurityTrust, CSRF, insecure deserialisation, SSRF, file upload and path traversal, authentication and session handling, secrets and sensitive data exposure, with evidence and a fix per finding. Use when reviewing a pull request that touches endpoints, authentication, files, queries or user input, or when asked for a security review.""", r"""
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
""")

S["threat-model"] = ("""Threat model a feature or architecture with STRIDE before building it: data flow diagram with trust boundaries, threats per element (spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege), existing mitigations, risk rating and concrete security requirements and tests. Use when designing a new feature, integration, API, file exchange or admin tool, before a security review, or when a customer asks how a flow is protected.""", r"""
# Threat model (STRIDE)

## 1. Draw the flow (text is fine)
Actors (users, admins, external systems), processes, data stores, data flows, and **trust boundaries** (internet / DMZ / internal, tenant / tenant, user / admin, our system / partner).

## 2. Threats per element
| Letter | Question | Typical mitigation |
|---|---|---|
| **S**poofing | can someone pretend to be a user or system? | strong auth, mTLS, signed tokens |
| **T**ampering | can data be changed in transit or at rest? | TLS, signatures, integrity checks, DB permissions |
| **R**epudiation | can someone deny an action? | audit log with who/what/when, tamper-evident |
| **I**nformation disclosure | can data leak (other tenant, logs, errors)? | authorisation, encryption, minimisation |
| **D**enial of service | can someone exhaust resources? | rate limits, quotas, timeouts, size limits |
| **E**levation of privilege | can someone gain rights? | least privilege, server-side checks, input validation |

## 3. Rate and decide
Likelihood x impact (low/medium/high); for each high/medium: mitigation, owner, and a **testable security requirement** ("an accountant of tenant A gets 404 on tenant B's invoice id").

## Output
Diagram, threats table, decisions (mitigate / accept with reason / transfer), requirements and tests to add to the backlog.
""")

S["insecure-defaults"] = ("""Hunt for insecure defaults and configuration in an application and its infrastructure code: debug mode and detailed errors in production, permissive CORS, missing security headers, weak TLS, default credentials, open admin endpoints, verbose logging of sensitive data, overly broad cloud and database permissions. Use before a release, when hardening an application, reviewing configuration files, Dockerfiles, IaC or pipeline settings, or after a penetration test.""", r"""
# Insecure defaults

## Application configuration
- `ASPNETCORE_ENVIRONMENT=Development`, developer exception page, Swagger UI exposed in production without authentication.
- `customErrors Off` / detailed errors, stack traces in API responses.
- CORS `AllowAnyOrigin` with credentials; wildcard origins.
- Missing headers: `Strict-Transport-Security`, `Content-Security-Policy`, `X-Content-Type-Options: nosniff`, `Referrer-Policy`, frame protection.
- Cookies without `Secure`, `HttpOnly`, `SameSite`.
- Health or admin endpoints (`/metrics`, `/hangfire`, `/elmah`, actuator-like routes) public.

## Credentials and access
Default or shared accounts, connection strings with `sa` or `db_owner`, secrets in `appsettings.json`, long-lived tokens, service principals with Owner/Contributor on whole subscriptions.

## Infrastructure as code and containers
Public storage containers, firewall rules `0.0.0.0/0`, containers running as root, `latest` image tags, no resource limits, debug ports exposed.

## Logging
Request bodies logged with personal data or tokens; log level Debug in production.

## Output
Findings with file/setting, risk, safe value, and a check to add to CI (configuration tests, IaC scanner such as Checkov or PSRule for Azure).
""")

S["supply-chain"] = ("""Check the software supply chain of a project: generate an SBOM (CycloneDX or SPDX), list vulnerable and abandoned dependencies, licences incompatible with distribution to customers, dependency confusion risks between internal and public feeds, typosquatting, unpinned build tools and pipeline tasks, and build provenance. Use before a release or a customer security questionnaire, after a supply chain advisory, when adding a new dependency, or when setting up internal package feeds.""", r"""
# Supply chain

## Inventory
```bash
dotnet CycloneDX MySolution.sln -o sbom/            # .NET (CycloneDX tool)
npx @cyclonedx/cyclonedx-npm --output-file sbom/web.json
```
Keep the SBOM per release; customers increasingly ask for it.

## Checks
1. **Vulnerabilities**: `dotnet list package --vulnerable --include-transitive`, `npm audit --omit=dev`; triage by exploitability, not only by score.
2. **Abandoned packages**: last release, maintainers, open security issues; plan replacements for critical ones.
3. **Licences**: list them; flag GPL/AGPL/SSPL or "no licence" in distributed products; check with legal before use.
4. **Dependency confusion**: internal package names must not be resolvable from public feeds; NuGet package source mapping, npm scoped packages with `.npmrc` pointing scopes to the internal feed.
5. **New dependency review**: is it needed? popularity, maintenance, permissions (install scripts), size; prefer the platform's built-in features.
6. **Build**: pin pipeline tasks and actions to versions (or commit SHAs), pin container base images by digest, lock files in CI (`--locked-mode`, `npm ci`).

## Output
SBOM location, vulnerability table with decisions, licence exceptions, feed configuration changes, and the CI checks to add.
""")

S["secrets-hygiene"] = ("""Keep secrets out of code, history and logs: scan a diff, staged files or a whole repository with a bundled stdlib scanner (cloud keys, tokens, connection strings with passwords, private keys), move secrets to Key Vault, user secrets or pipeline variable groups, and handle a leaked secret properly: revoke and rotate first, then clean history. Use before committing or pushing, when reviewing configuration files, when a secret was committed, or when setting up a new project's configuration.""", r"""
# Secrets hygiene

## Scan
```bash
python "${CLAUDE_SKILL_DIR}/scripts/secret_scan.py" --staged                 # before a commit
python "${CLAUDE_SKILL_DIR}/scripts/secret_scan.py" --diff origin/main       # a branch
python "${CLAUDE_SKILL_DIR}/scripts/secret_scan.py" --path . --format md     # whole working tree
```
Detects cloud and SaaS keys (AWS, Azure storage, GitHub, GitLab, Slack, OpenAI, Anthropic), private keys, JWTs, connection strings with `Password=`, and generic `secret/password/apikey = value` assignments, skipping obvious placeholders. Prints masked values only; exit 1 if anything is found (usable as a pre-commit hook). Test fixtures that must contain fake secrets: add `secret-scan: ignore` on the line.

## Where secrets belong
| Context | Store |
|---|---|
| Local development (.NET) | `dotnet user-secrets` (outside the repo) |
| Azure-hosted apps | Key Vault + managed identity (no secret at all) |
| Pipelines | variable groups linked to Key Vault, secret variables |
| Front-end | nothing secret, ever: it ships to the browser |

## A secret was committed
1. **Revoke and rotate it now.** Assume it is compromised: history, forks, CI logs and caches keep it.
2. Check access logs of that credential for misuse.
3. Then clean history if policy requires (`git filter-repo`, coordinated force-push), and add the pattern to the scanner/pre-commit.
4. Write a short incident note (see `dev-delivery:incident-review`).
""")

write_plugin(PLUGIN, DESC, S, ["security", "owasp", "threat-modeling", "sbom", "secrets"])
