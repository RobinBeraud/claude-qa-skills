---
name: nuget-hygiene
description: "Keep NuGet dependencies safe and tidy: list vulnerable, deprecated and outdated packages with the dotnet CLI, check licences, adopt Central Package Management, lock files for reproducible restores, trusted package sources, and an update routine that does not break builds. Use when auditing dependencies, after a security advisory, before a release, or when package versions drift between projects."
---

# NuGet hygiene

## Audit
```bash
dotnet list package --vulnerable --include-transitive
dotnet list package --deprecated
dotnet list package --outdated
```
.NET 8+ also warns at restore (`NuGetAudit`); keep it on, and set `<NuGetAuditMode>all</NuGetAuditMode>` to include transitive packages.

## Triage a vulnerable package
1. Is the vulnerable code path used? Severity and exploitability in our context.
2. Upgrade the direct package; for a transitive one, add an explicit reference to the fixed version (or a CPM transitive pin).
3. Build, test, note it in the PR with the advisory id.

## Hygiene
- **Central Package Management**: `Directory.Packages.props` with `<ManagePackageVersionsCentrally>true</ManagePackageVersionsCentrally>`; one version per package for the whole repo.
- **Lock files** (`RestorePackagesWithLockFile`) and `--locked-mode` in CI for reproducible builds.
- **Sources**: `nuget.config` with the internal feed and package source mapping, so a public package cannot shadow an internal name (dependency confusion).
- **Licences**: list them (e.g. `dotnet-project-licenses` or the SBOM tool) and flag copyleft or "no licence" before shipping to customers.
- Update routine: small batches, one family at a time, read release notes for majors.
