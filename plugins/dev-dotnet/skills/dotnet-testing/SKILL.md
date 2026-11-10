---
name: dotnet-testing
description: "Write effective .NET tests: xUnit, NUnit or MSTest conventions of the repo, Arrange-Act-Assert, test data builders, fakes over mocks, integration tests with WebApplicationFactory and Testcontainers (SQL Server, PostgreSQL), snapshot testing with Verify, time and randomness controlled with TimeProvider, and running only affected tests. Use when adding or fixing tests in a .NET solution, when tests are flaky, or when integration tests hit a shared database."
---

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
