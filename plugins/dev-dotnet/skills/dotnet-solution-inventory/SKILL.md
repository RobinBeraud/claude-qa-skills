---
name: dotnet-solution-inventory
description: "Inventory a .NET solution with a bundled stdlib script: every project with its SDK style, target frameworks with their support status (net48, net8.0, net10.0...), output type, project references, NuGet packages with version drift between projects, central package management status; then point out upgrade blockers. Use before an upgrade, when onboarding on a large solution, when versions of the same package differ across projects, or to plan a .NET Framework migration."
---

# .NET solution inventory

## Run
```bash
python "${CLAUDE_SKILL_DIR}/scripts/csproj_scan.py" path/to/repo --format md
python "${CLAUDE_SKILL_DIR}/scripts/csproj_scan.py" . --format json > inventory.json
```
Scans `*.csproj`, `*.vbproj`, `*.fsproj`, `Directory.Build.props`, `Directory.Packages.props` and `packages.config`. Reports:
- projects by target framework (legacy .NET Framework, .NET Standard, modern .NET), SDK-style or not;
- packages used in several versions (drift), and the projects using each version;
- `packages.config` projects (to migrate to PackageReference first);
- the project-reference graph: leaves first = the order to migrate.

## Read the result
1. **Leaves first**: libraries with no project references can move to `netstandard2.0` or multi-target `net48;net10.0` first.
2. **Drift**: align versions, ideally with Central Package Management (`Directory.Packages.props`).
3. **Blockers**: WCF server, WebForms, `System.Web`, AppDomains, Remoting, WWF: no direct path, see `dotnet-upgrade`.

## Output
Inventory table, drift table, migration order, blockers list.
