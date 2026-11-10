---
name: insecure-defaults
description: "Hunt for insecure defaults and configuration in an application and its infrastructure code: debug mode and detailed errors in production, permissive CORS, missing security headers, weak TLS, default credentials, open admin endpoints, verbose logging of sensitive data, overly broad cloud and database permissions. Use before a release, when hardening an application, reviewing configuration files, Dockerfiles, IaC or pipeline settings, or after a penetration test."
---

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
