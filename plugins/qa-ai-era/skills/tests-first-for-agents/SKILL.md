---
name: tests-first-for-agents
description: "Before letting a coding agent implement a story, turn its acceptance criteria into failing tests (unit or API level), get them reviewed by a human, then hand the agent the brief plus the red tests as the definition of done. Use when starting any agent-implemented task, to keep agents honest and verification cheap."
---

# Tests first, then the agent

## Steps
1. Read the acceptance criteria; resolve ambiguities first (`story-testability-review`).
2. Write **failing** tests, one per criterion, at the lowest level that can prove it (unit > API > UI). Include the edge cases you know matter.
3. Run them and show they fail **for the right reason** (missing behaviour, not a syntax error or a broken import).
4. A human reviews the tests (5 minutes): do they encode the intent?
5. Hand the agent: the brief, the test files, and the rule "do not modify these tests; if one seems wrong, stop and explain why".
6. When the agent finishes: all tests green, plus any new tests it added reviewed separately.

## Output
Test files, the red run output, and the brief text for the agent:
```
Implement <story>. Done = the tests in <paths> pass, existing tests still pass, linter clean.
Do not edit <paths>. Stop and report after 3 failed attempts.
```
