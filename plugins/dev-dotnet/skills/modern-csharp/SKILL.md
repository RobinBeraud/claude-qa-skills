---
name: modern-csharp
description: "Write and review modern, safe C#: nullable reference types enabled gradually, async/await without deadlocks or fire-and-forget, cancellation tokens, IDisposable and IAsyncDisposable, records and pattern matching, decimal for money, culture-safe parsing and formatting, and logging with structured templates. Use when writing or reviewing C# code, enabling nullable, fixing async bugs, or modernising old C# style."
---

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
