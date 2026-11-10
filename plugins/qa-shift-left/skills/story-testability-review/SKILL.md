---
name: story-testability-review
description: "Review a user story, PBI or ticket for testability before development starts: ambiguous words, missing acceptance criteria, untestable rules, hidden edge cases, and a rewrite in Given/When/Then. Use when a story is about to enter a sprint, during refinement, or when asked whether a ticket is ready to test."
---

# Story testability review

Catch defects in the requirement, where they cost the least. The output is a verdict plus a better story, not a lecture.

## Inputs
- The story text (title, description, acceptance criteria). Ask for it if missing.
- Optional: linked mockups, business rules, the product glossary.

## Steps
1. **Restate** the story in one sentence: who, what, why. If you cannot, the story is not ready.
2. **Hunt ambiguity**: flag every vague word (`fast`, `user-friendly`, `etc.`, `appropriate`, `all`, `some`, `should`, `if needed`) and every undefined term.
3. **Check each acceptance criterion** against: observable, binary (pass/fail), independent of implementation, one behaviour per criterion.
4. **Find the missing cases** with this list: empty / null input, maximum length, duplicates, permissions (who may not do it), concurrency (two users at once), errors from dependencies, undo / cancel, existing data created before the change, localisation (dates, decimals, currency).
5. **Rewrite** the criteria as Given / When / Then, one scenario per rule, with concrete values.
6. **List open questions** for the product owner, each answerable with yes/no or a value.

## Output
```
Verdict: READY | READY WITH QUESTIONS | NOT READY
Ambiguities: <word> -> <why it is untestable> -> <proposed precise wording>
Missing cases: <case> (risk: high/med/low)
Rewritten acceptance criteria (Gherkin)
Questions for the PO (numbered)
```

## Quality bar
- Every rewritten criterion contains at least one concrete value (amount, date, role, count).
- Never invent business rules: when the rule is unknown, write it as a question.
- Answer in the user's language.
