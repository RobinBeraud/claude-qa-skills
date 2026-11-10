---
name: self-review
description: "Review your own diff before asking anyone else: read it as a reviewer would, file by file, against a checklist (correctness, edge cases, errors, tests, security, performance, naming, leftovers like debug code, TODOs and commented code), then fix what you find. Use before opening a pull request, before asking for review, and after an AI agent produced a change."
---

# Self-review

Reviewers' attention is the scarce resource. Spend yours first.

## Read the diff, not the files
`git diff <base>...HEAD` (or the PR view). Files in the order a reviewer would read them: contracts, core logic, tests, the rest.

## Checklist
- **Correctness**: does each change do what the work item asks? Off-by-one, null/empty, time zones, rounding, culture (decimal comma), concurrency.
- **Errors**: failures handled at the right level, no swallowed exceptions, useful messages, no stack trace to the user.
- **Tests**: a test fails without the change? Edge cases covered? No test deleted or weakened to go green.
- **Security**: inputs validated, authorisation checked server-side, no secret, SQL parameterised, personal data not logged.
- **Performance**: no query in a loop, no unbounded list, pagination on new endpoints.
- **Compatibility**: public API, DB schema, file formats, configuration keys; old clients still work?
- **Leftovers**: debug output, commented code, stray TODOs, unrelated formatting, files committed by mistake.
- **Readability**: names say what things are; a comment explains *why* where the code cannot.

## Output
List what you found and fixed; list what you deliberately left (with the reason) so reviewers do not rediscover it.
