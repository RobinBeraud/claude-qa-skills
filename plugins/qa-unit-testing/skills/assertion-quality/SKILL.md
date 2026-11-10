---
name: assertion-quality
description: "Improve assertions so failures explain themselves and tests check what matters: precise matchers, whole-object comparison over field-by-field noise, custom assertion helpers, approximate comparison only where justified, and one logical assertion per test. Use when reviewing tests with weak assertions, unreadable failure messages, or brittle checks on irrelevant details."
---

# Assertion quality

## Checklist
- **Specific over generic**: `assertEqual(total, Decimal("120.00"))`, not `assertTrue(total > 0)`.
- **Readable failures**: prefer matchers that show expected vs actual (`toEqual`, AssertJ, pytest's rewriting). Add a message only when the value alone is ambiguous.
- **Compare meaningful objects**: build the expected object and compare once, ignoring volatile fields (ids, timestamps) explicitly.
- **Collections**: assert content and order only if order matters (`assertCountEqual` / `containsExactlyInAnyOrder` otherwise).
- **Exceptions**: assert the type **and** the message or code, and that no side effect happened.
- **Floats**: never for money; for real numbers, an explicit tolerance with a reason.
- **One logical assertion** per test: several asserts are fine if they check one behaviour.
- **Custom helpers** for repeated domain checks: `assert_balanced(entry)`, `assertThatInvoice(inv).isPaid()`.

## Output
Before/after rewrites of the weakest assertions and the helper functions introduced.
