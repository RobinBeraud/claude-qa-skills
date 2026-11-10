---
name: supply-chain
description: "Check the software supply chain of a project: generate an SBOM (CycloneDX or SPDX), list vulnerable and abandoned dependencies, licences incompatible with distribution to customers, dependency confusion risks between internal and public feeds, typosquatting, unpinned build tools and pipeline tasks, and build provenance. Use before a release or a customer security questionnaire, after a supply chain advisory, when adding a new dependency, or when setting up internal package feeds."
---

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
