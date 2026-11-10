from _gen import write_plugin

PLUGIN = "dev-dotnet"
DESC = ".NET and C# for enterprise codebases: solution inventory (target frameworks, package drift) with a bundled script, .NET Framework to modern .NET upgrades, modern C# idioms and async pitfalls, testing with xUnit/NUnit and Testcontainers, EF Core performance and safe migrations, and NuGet vulnerability and licence hygiene."

S = {}

S["dotnet-solution-inventory"] = ("""Inventory a .NET solution with a bundled stdlib script: every project with its SDK style, target frameworks with their support status (net48, net8.0, net10.0...), output type, project references, NuGet packages with version drift between projects, central package management status; then point out upgrade blockers. Use before an upgrade, when onboarding on a large solution, when versions of the same package differ across projects, or to plan a .NET Framework migration.""", r"""
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
""")

S["dotnet-upgrade"] = ("""Plan and run an incremental upgrade from .NET Framework or an old .NET version to the current LTS: assessment (APIs, packages, blockers like System.Web, WCF, WebForms), SDK-style conversion, multi-targeting, side-by-side migration with YARP or System.Web adapters, test safety net and release plan. Use when asked to migrate to .NET 10 or another modern version, modernise a .NET Framework application, or leave an unsupported runtime.""", r"""
# .NET upgrade

Big-bang rewrites fail; incremental upgrades ship.

**Target**: the current LTS. As of November 2026 that is **.NET 10** (supported until November 2028); .NET 8 and .NET 9 reach end of support on 10 November 2026, .NET 5/6/7 and .NET Core are already out of support. .NET Framework 4.6.2-4.8.1 stays supported with Windows but gets no new features. Check https://dotnet.microsoft.com/platform/support/policy before planning.

## 1. Assess
- Inventory with `dotnet-solution-inventory` (frameworks, packages, reference graph).
- Run the .NET Upgrade Assistant analysis or the API portability analyzers; list unsupported APIs.
- Packages: does each have a modern version? Abandoned ones need a replacement.
- Blockers: `System.Web` (MVC 5, WebForms), WCF server (-> CoreWCF or gRPC/REST), `AppDomain`, Remoting, `BinaryFormatter`, Windows-only APIs (OK if you stay on Windows: `net10.0-windows`).

## 2. Safety net
Characterisation tests on critical flows before touching anything (see `qa-automation:characterization-tests`). CI must build both old and new targets.

## 3. Convert, leaves first
1. `packages.config` -> `PackageReference`.
2. Old csproj -> SDK-style (`try-convert` or Upgrade Assistant), still targeting `net48`; build, test, commit.
3. Libraries: multi-target `<TargetFrameworks>net48;net10.0</TargetFrameworks>`, fix with `#if NET` only where needed.
4. Applications last. For web apps: **side-by-side** (new ASP.NET Core app in front with YARP proxying unmigrated routes to the old app; System.Web adapters to share session/auth) and move routes one by one.

## 4. Release
Ship each step. Monitor errors and performance against the old version. Remove the old target when nothing depends on it.

## Red flags
Upgrading everything in one branch; "we will write tests after"; replacing libraries and the framework at the same time.
""")

S["modern-csharp"] = ("""Write and review modern, safe C#: nullable reference types enabled gradually, async/await without deadlocks or fire-and-forget, cancellation tokens, IDisposable and IAsyncDisposable, records and pattern matching, decimal for money, culture-safe parsing and formatting, and logging with structured templates. Use when writing or reviewing C# code, enabling nullable, fixing async bugs, or modernising old C# style.""", r"""
# Modern C#

## Async
- `async` all the way: never `.Result`, `.Wait()` or `GetAwaiter().GetResult()` on a request path (deadlocks in old ASP.NET, thread starvation everywhere).
- No `async void` except event handlers. No fire-and-forget `Task` without error handling (use a queue or a hosted service).
- Pass `CancellationToken` through, honour it in loops and I/O.
- `ConfigureAwait(false)` in libraries; not needed in ASP.NET Core app code.

## Nulls
Enable `<Nullable>enable</Nullable>` project by project (or `#nullable enable` file by file). Fix warnings, do not silence them with `!` except where you can prove non-null. `ArgumentNullException.ThrowIfNull(x)` at public boundaries.

## Money, dates, culture
- `decimal` for money and quantities with rounding rules, never `double`. Explicit `Math.Round(x, 2, MidpointRounding.AwayFromZero)` when the business rule says so (EN 16931, tax rules).
- `DateTimeOffset` or UTC `DateTime` for instants; `DateOnly` for business dates.
- Parsing and formatting files and APIs: `CultureInfo.InvariantCulture`. Display: the user's culture (`fr-FR` uses a decimal comma).

## Resources and errors
`using`/`await using` for disposables; `IHttpClientFactory`, never `new HttpClient()` per call. Catch specific exceptions; never `catch (Exception) {}`.

## Logging
Structured templates: `logger.LogInformation("Invoice {InvoiceId} posted", id)` (not string interpolation). Never log secrets or personal data.

## Style
Records for immutable data, pattern matching for branching on shape, file-scoped namespaces, `required` members, collection expressions; follow the repo's `.editorconfig` over personal taste.
""")

S["dotnet-testing"] = ("""Write effective .NET tests: xUnit, NUnit or MSTest conventions of the repo, Arrange-Act-Assert, test data builders, fakes over mocks, integration tests with WebApplicationFactory and Testcontainers (SQL Server, PostgreSQL), snapshot testing with Verify, time and randomness controlled with TimeProvider, and running only affected tests. Use when adding or fixing tests in a .NET solution, when tests are flaky, or when integration tests hit a shared database.""", r"""
# .NET testing

## Unit tests
- Follow the repo's framework and naming (`Method_State_Expected` or `Should_...`). One behaviour per test.
- Builders for test data (`new InvoiceBuilder().WithLine(100m, vat: 0.2m).Build()`), not 40-line setups.
- Prefer real objects and simple fakes; mock only boundaries (HTTP, clock, message bus). Over-mocked tests break on refactors and catch nothing.
- Time: inject `TimeProvider` (.NET 8+) and use `FakeTimeProvider`; never `DateTime.Now` in logic.
- Parameterise: `[Theory]` + `[InlineData]` / `[TestCase]` for rule tables (VAT rates, rounding, boundaries).

## Integration tests
- ASP.NET Core: `WebApplicationFactory<Program>` with services overridden for externals.
- Database: **Testcontainers** (`Testcontainers.MsSql`, `Testcontainers.PostgreSql`) with a fresh database per test class; apply real migrations; never a shared dev database.
- Reset state between tests (Respawn, transactions rolled back).

## Snapshot tests
`Verify` for large outputs (generated XML/JSON, e-invoices, reports): review the `.received` diff, scrub dates and ids.

## Run
```bash
dotnet test --filter "FullyQualifiedName~Billing" --logger "trx" --collect:"XPlat Code Coverage"
```

## Flaky tests
Usually time, ordering, shared state, real network or `Task.Delay`. Fix the cause; do not add retries to hide it.
""")

S["ef-core-performance"] = ("""Find and fix Entity Framework Core performance problems: N+1 queries, missing AsNoTracking, client-side evaluation, cartesian explosion (AsSplitQuery), unbounded result sets, missing indexes, and compiled or raw SQL when justified; with query logging to see the real SQL. Use when an endpoint or batch using EF Core is slow, when the database shows many similar queries, or when reviewing data-access code.""", r"""
# EF Core performance

## See the SQL first
```csharp
options.LogTo(Console.WriteLine, LogLevel.Information).EnableSensitiveDataLogging(false);
```
or `ToQueryString()` on the query, and the database's own tools (SQL Server Query Store, execution plans).

## Usual causes and fixes
| Symptom | Cause | Fix |
|---|---|---|
| Hundreds of identical queries | N+1 via lazy loading or a query in a loop | `Include`, or project with `Select` in one query; disable lazy loading |
| Slow read-only list | change tracking | `AsNoTracking()` (or `AsNoTrackingWithIdentityResolution`) |
| Huge result with several `Include` | cartesian explosion | `AsSplitQuery()` or project only needed columns |
| Memory grows with data | no paging, `ToList()` too early | `Skip/Take` with a stable `OrderBy`, keyset pagination for big tables |
| Slow `Where` | missing index, non-sargable expression | index (migration), avoid functions on columns |
| Bulk updates slow | entity-by-entity `SaveChanges` | `ExecuteUpdate` / `ExecuteDelete` (EF 7+), batching |
| Same query parsed repeatedly in hot path | query compilation | `EF.CompileQuery`, or a view / raw SQL with parameters |

## Rules
- Measure before and after (duration, number of queries, logical reads).
- Raw SQL only parameterised (`FromSql($"... {id}")` interpolation is parameterised; string concatenation is not).
- Multi-tenant: check that every new query keeps the tenant filter (global query filters).
""")

S["ef-core-migrations"] = ("""Create and ship Entity Framework Core migrations safely: review the generated SQL, expand and contract for zero-downtime changes (add nullable column, backfill, switch, then drop), data migrations in batches, idempotent scripts or bundles for deployment, and rollback planning. Use when changing an EF Core model, generating or reviewing a migration, renaming or dropping columns, or deploying schema changes to production.""", r"""
# EF Core migrations

## Always read the SQL
```bash
dotnet ef migrations add AddInvoiceDueDate
dotnet ef migrations script <from> <to> --idempotent -o migration.sql
```
A rename seen as drop + add destroys data: check every `DropColumn`/`DropTable`.

## Expand and contract (no downtime, old and new code both run)
1. **Expand**: add the new column/table, nullable or with a default. Deploy.
2. **Migrate data**: backfill in batches (e.g. 5,000 rows per transaction), off-peak, resumable.
3. **Switch**: code reads and writes the new structure (feature flag if needed). Deploy.
4. **Contract**: drop the old column in a later release, once no version uses it.

## Rules
- Large tables: adding an index or a non-null column can lock; use online index options where available and test on a production-sized copy.
- Deploy with idempotent scripts or migration bundles (`dotnet ef migrations bundle`), not `Database.Migrate()` at app start-up on several instances.
- Every migration has a tested rollback path (a down script or a forward fix plan).
- Seed/reference data changes are migrations too: versioned and reviewed.
""")

S["nuget-hygiene"] = ("""Keep NuGet dependencies safe and tidy: list vulnerable, deprecated and outdated packages with the dotnet CLI, check licences, adopt Central Package Management, lock files for reproducible restores, trusted package sources, and an update routine that does not break builds. Use when auditing dependencies, after a security advisory, before a release, or when package versions drift between projects.""", r"""
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
""")

write_plugin(PLUGIN, DESC, S, ["dotnet", "csharp", "ef-core", "nuget", "migration"])
