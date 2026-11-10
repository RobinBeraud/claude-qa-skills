---
name: plan-in-files
description: "Plan multi-step work in a markdown file kept in the repository: goal, constraints, task list with the test that proves each task, decisions log and progress, updated as you go so work survives context loss, a crash or a handoff. Use for any task longer than about an hour, a feature spanning several files, a migration, or when the user says \"plan it first\"."
---

# Plan in files

The plan lives in a file, not in the conversation. Conversations get compacted; files do not.

## File: `docs/plans/YYYY-MM-DD-<topic>.md` (or the user's preferred place)
```markdown
# <Feature> plan
Goal: <one sentence, from the user's words>
Done when: <observable acceptance criteria>
Constraints: <compatibility, performance, regulatory, deadline>
Out of scope: <explicitly>

## Tasks
- [ ] 1. <small change> -- proof: <test name or command>
- [ ] 2. ...

## Decisions
- 2026-11-10: chose X over Y because ...

## Progress / notes
- task 1 done, test `InvoiceTotalsTests.RoundsPerLine` green
```

## Rules
1. Each task is small enough to review on its own and has a **proof** (a test, a command output).
2. Order tasks so the build stays green after each one; commit after each.
3. Before each task re-read the plan; after it, tick it and add a note. Update the plan when reality differs; never silently drift.
4. Record decisions with the reason: the next person (or the next session) will ask.
5. When resuming, read the plan file first, then `git log` since the last note.

## Red flags
A plan with no proofs; tasks like "implement the feature"; ticking a task whose test was never run.
