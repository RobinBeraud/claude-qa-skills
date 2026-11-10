---
name: unit-test-writer
description: "Write focused unit tests for a function, class or module: one behaviour per test, Arrange-Act-Assert, descriptive names, boundary and error cases, no I/O, fast and deterministic; in the project's existing framework (pytest, JUnit 5, xUnit/NUnit, Jest/Vitest, PHPUnit, Go testing). Use when asked to add unit tests, cover a bug fix, or raise confidence in a module."
---

# Unit test writer

## Before writing
1. Read the code **and** the existing tests: framework, folder layout, naming style, fixtures, helpers. Follow them.
2. List the behaviours of the unit (not its lines): normal results, boundaries, invalid input, errors from collaborators, state changes.

## Rules for each test
- **One behaviour**, named after it: `test_late_fee_is_zero_on_due_date`, `Should_reject_negative_amount`.
- **Arrange / Act / Assert** separated by a blank line; a single Act.
- **Concrete expected values** computed independently of the code (by hand or from the spec), never by calling the code under test.
- **No I/O**: no network, database, file system or real clock; inject or fake them.
- **Deterministic**: fixed seeds, frozen time, no order dependence.
- Assert on **outputs and observable state**, not on private methods or internal calls (unless the call *is* the behaviour, e.g. "an e-mail is sent").
- Cover: happy path, each boundary, each error path, null/empty, and the bug being fixed (regression test first, red, then fix).

## Steps
1. Write the tests, run them, show the output.
2. If a test passes before the code exists or after deliberately breaking the code, it is not testing anything: fix it.
3. Report what is covered and what deliberately is not.

## Output
Test file(s), the run output, and a short behaviour checklist with ✔ per test.
