from _gen import write_plugin

PLUGIN = "qa-unit-testing"
DESC = "Unit tests that document behaviour and catch regressions: writing tests with Arrange-Act-Assert, red-green-refactor with an agent, choosing the right test double, parameterised tests, breaking dependencies to make legacy code testable, and sharp assertions."

S = {}

S["unit-test-writer"] = ("""Write focused unit tests for a function, class or module: one behaviour per test, Arrange-Act-Assert, descriptive names, boundary and error cases, no I/O, fast and deterministic; in the project's existing framework (pytest, JUnit 5, xUnit/NUnit, Jest/Vitest, PHPUnit, Go testing). Use when asked to add unit tests, cover a bug fix, or raise confidence in a module.""", r"""
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
""")

S["tdd-red-green-refactor"] = ("""Drive a change with test-driven development in short red-green-refactor cycles, with Claude as a disciplined pair: write one failing test, the minimum code to pass, refactor with tests green, repeat; keeps a visible test list. Use when implementing new logic, fixing a bug the TDD way, or coaching a team on TDD with an AI agent.""", r"""
# TDD: red, green, refactor

## Cycle (repeat, 2-10 minutes each)
1. **Test list**: write the behaviours to implement as a checklist; start with the simplest.
2. **Red**: write *one* failing test. Run it. It must fail for the expected reason (assertion, not compile error).
3. **Green**: write the minimum code that passes. Hard-coding is fine at first; the next test forces generalisation (triangulation).
4. **Refactor**: remove duplication, improve names, in code **and** tests, with all tests green. Run them.
5. Tick the item, add newly discovered cases to the list, next.

## Rules for the agent
- Never write production code without a failing test that requires it.
- Never write more than one failing test at a time.
- Show the test run after each step (red output, green output).
- Do not change a test to make it pass unless the test was wrong; say so explicitly.
- Commit at each green + refactor if the user wants small commits.

## Output
The evolving test list, each cycle's test and code diff, and the final run.
""")

S["test-doubles-chooser"] = ("""Choose and write the right test double (dummy, stub, spy, mock, fake) for each collaborator of the unit under test, avoid over-mocking, and prefer fakes or real objects where cheap; explains the trade-off in one line per collaborator. Use when a unit test needs to isolate a database, HTTP client, clock, queue or service, or when tests break on every refactor.""", r"""
# Choosing test doubles

| Double | What it does | Use when |
|---|---|---|
| Dummy | Fills a parameter, never used | Required argument irrelevant to the test |
| Stub | Returns canned answers | You need the collaborator's *output* (price, user, config) |
| Spy | Records calls for later assertions | The call itself is the behaviour (e-mail sent, event published) |
| Mock | Pre-programmed expectations, fails on unexpected calls | Protocol matters (order, exact arguments); use sparingly |
| Fake | Working lightweight implementation (in-memory repository, fake clock) | Collaborator is used a lot; you want realistic behaviour without I/O |

## Steps
1. List the unit's collaborators.
2. For each: is it a **value or pure logic**? Use the real thing. Is it **I/O or slow or non-deterministic**? Double it.
3. Pick the weakest double that does the job (stub before mock). Prefer one **fake** over many mocks for repositories and clocks.
4. Never mock what you do not own directly (HTTP library, ORM): wrap it in your own adapter and double the adapter.
5. Write the doubles and the tests; keep assertions on outcomes.

## Output
`collaborator -> double type -> why`, then the code. Flag any test with more than 3 mocks: the unit probably has too many responsibilities.
""")

S["parameterized-tests"] = ("""Collapse repetitive unit tests into parameterised, table-driven tests (pytest.mark.parametrize, JUnit @ParameterizedTest, xUnit Theory/InlineData, Jest test.each, Go table tests) with readable case ids, and fill the table with boundary and error cases. Use when tests are copy-pasted with different values, or for validation, calculation and mapping rules.""", r"""
# Parameterised tests

## Steps
1. Find tests that differ only by data. Extract the inputs and the expected outcome.
2. Build a **table** with one row per case and a readable **id** (`"due date + 1 day"`, not `case3`).
3. Add rows from test design: partitions, both sides of each boundary, invalid values, null/empty, maximum.
4. Keep error cases in a **separate** parameterised test (different assertion: raises / returns error).
5. Run; make sure the failure output names the failing row.

## Example (pytest)
```python
@pytest.mark.parametrize("amount, days_late, fee", [
    pytest.param(Decimal("100.00"), 0, Decimal("0.00"), id="on due date"),
    pytest.param(Decimal("100.00"), 1, Decimal("40.00"), id="one day late"),
    pytest.param(Decimal("0.00"),   30, Decimal("0.00"), id="zero amount"),
])
def test_late_fee(amount, days_late, fee):
    assert late_fee(amount, days_late) == fee
```
## Pitfall
Do not hide logic in the table (computed expected values); expected values are literals.
""")

S["testability-refactoring"] = ("""Make hard-to-test or legacy code unit-testable with safe, small refactorings (Michael Feathers' seams): extract method, inject dependencies, wrap static and global calls, introduce an interface, pass the clock and random source, separate pure logic from I/O; protected by characterization tests first. Use when code cannot be unit tested because of statics, singletons, new-ed dependencies, time, or database calls in the middle of logic.""", r"""
# Testability refactoring

## Steps
1. **Protect first**: write characterization tests around the current behaviour (`characterization-tests` skill) at the highest convenient level.
2. **Find the seam** that blocks testing:
   | Obstacle | Seam |
   |---|---|
   | `new Service()` inside the method | Constructor/parameter injection |
   | Static/global call (`DateTime.Now`, `Config.get`) | Wrap in an interface or pass a function/clock |
   | Logic mixed with SQL/HTTP | Extract the pure calculation into its own function |
   | Huge method | Extract method, then test the extracted piece |
   | Hidden singleton | Introduce a parameter with the singleton as default |
3. Apply **one** refactoring at a time, run the tests after each.
4. Write unit tests on the newly exposed pure logic.
5. Keep behaviour identical: no "while I'm here" changes.

## Output
Sequence of refactorings with diffs, tests after each step, and the new unit tests.
""")

S["assertion-quality"] = ("""Improve assertions so failures explain themselves and tests check what matters: precise matchers, whole-object comparison over field-by-field noise, custom assertion helpers, approximate comparison only where justified, and one logical assertion per test. Use when reviewing tests with weak assertions, unreadable failure messages, or brittle checks on irrelevant details.""", r"""
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
""")

write_plugin(PLUGIN, DESC, S, ["unit-testing", "tdd", "test-doubles", "refactoring"])
