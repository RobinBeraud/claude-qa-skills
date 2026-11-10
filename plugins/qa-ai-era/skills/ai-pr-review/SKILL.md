---
name: ai-pr-review
description: "Review a pull request written with a coding agent (Claude Code, Copilot, Cursor) against its brief: scope creep, acceptance criteria actually covered by tests, weak or mirrored tests, invented APIs or packages, missing error paths, security and data risks, and what was not verified. Use when reviewing any AI-assisted PR, especially large ones, before approving."
---

# Review an AI-generated pull request

Agents write plausible code fast; the reviewer's job is to check it does the **right** thing, and nothing more.

## Steps
1. **Read the brief first** (ticket, acceptance criteria). Without a brief, ask for one before reviewing.
2. **Scope**: list files changed that the brief did not need. Unrequested refactors, renamed APIs, config or dependency changes -> ask to split or justify.
3. **Criteria matrix**: for each acceptance criterion, which test proves it? Missing -> blocking comment.
4. **Tests**: read them before the code. Watch for mirrored expectations (same formula as the code), no assertion, snapshot dumps, mocks of the unit itself, tests that cannot fail.
5. **Hallucinations**: methods, config keys, endpoints or packages that do not exist in this codebase or registry; versions that do not exist.
6. **Unhappy paths**: null/empty, errors from dependencies, permissions, concurrency, time zones, rounding.
7. **Security & data**: secrets, injection, logging of personal data, disabled checks, broadened permissions.
8. **Evidence**: build, tests, linter output in the PR; "not verified" section present and honest.
9. **Size**: more than ~400 changed lines with mixed concerns -> request a split.

## Output
`BLOCKING` / `SHOULD` / `NIT` comments with file:line, the criteria matrix, and a verdict: approve, request changes, or split.
