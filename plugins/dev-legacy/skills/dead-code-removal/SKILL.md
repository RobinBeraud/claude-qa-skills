---
name: dead-code-removal
description: "Remove dead code, unused dependencies and obsolete feature flags safely: find candidates with compiler and IDE analysis, coverage and production telemetry, verify nothing calls them dynamically (reflection, configuration, reports, external callers), delete in small reviewed steps, and keep the deletion revertible. Use when cleaning a legacy codebase, before an upgrade or migration, when a feature flag is fully rolled out, or when the build is slowed by unused projects."
---

# Dead code removal

Deleting code is the cheapest way to reduce bugs, build time and upgrade effort, if it is really dead.

## Find candidates
- Compiler/IDE: unused private members, unreferenced projects and files (Roslyn analyzers IDE0051/IDE0052, ReSharper/Rider solution-wide analysis, `ts-prune`/`knip` for TypeScript).
- Production evidence: endpoints with zero calls over a full business cycle (logs, APM), reports never run, jobs never scheduled.
- Feature flags at 100 % for more than one release: remove the flag and the old branch of code.
- Dependencies: packages not referenced by any code (`dotnet list package` + search, `depcheck`/`knip`).

## Verify before deleting
Reflection and dependency injection by name, configuration files, stored procedures called from reports, scheduled tasks, external clients calling an API, customer-specific extensions or scripts. Search the whole organisation's repositories, not only this one, for public APIs.

## Delete
Small PRs by area, each building and passing tests; the PR lists the evidence (zero calls since ..., no references). For public APIs: deprecate first (warning, header, docs), remove one version later.
