---
name: session-handoff
description: "Hand off work between sessions, people or agents without losing context: a short handoff note with goal, state, what was verified, what is left, decisions, gotchas and the exact next step, stored with the code. Use at the end of a work session, before a context reset, when passing a task to a colleague or a sub-agent, or when resuming someone else's branch."
---

# Session handoff

## Write `HANDOFF.md` (or a section of the plan file) before stopping
```markdown
# Handoff: <task> -- <date>
Branch: <name> @ <short sha>   Plan: docs/plans/<file>.md
Goal: <one sentence>
State: <what works now>
Verified: <commands run and results>
Not verified: <gaps>
Left to do: <ordered list>
Decisions: <decision + reason>
Gotchas: <traps: flaky test X, needs env var Y, do not touch Z>
Next step: <the exact first action, e.g. "run tests in Billing.Tests, then implement task 4">
```

## Resuming
1. Read the handoff and the plan, then `git log` and `git status`.
2. Re-run the verification listed; trust nothing that was not re-run (`qa-ai-era:done-evidence-check`).
3. Delete or archive the handoff once merged; do not let stale notes mislead the next person.

## Rules
Facts, not narrative. No secrets or customer data in the note. Keep it under one screen.
