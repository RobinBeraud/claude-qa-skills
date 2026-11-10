---
name: receive-review
description: "Handle code review feedback rigorously: understand each comment, verify the claim against the code before agreeing, fix or push back with evidence, answer every thread, and avoid both blind acceptance and defensiveness. Use when a pull request receives review comments, when an AI reviewer leaves suggestions, or when feedback seems wrong or unclear."
---

# Receive review

## For each comment
1. **Understand**: restate it. Unclear? Ask a question; do not guess.
2. **Verify**: is the reviewer right? Read the code, run the case, check the docs. Reviewers (human or AI) are often right and sometimes wrong.
3. **Decide**:
   - Right: fix it, reply with what changed (commit link).
   - Partly right: fix the valid part, explain the rest.
   - Wrong: reply with evidence (test, spec, measurement), politely. Not "I disagree".
   - Out of scope: agree, open a follow-up work item, link it.
4. **Resolve** only your own threads when the reviewer's policy allows; otherwise let them resolve.

## Rules
- No performative agreement ("Great catch!" then a fix that does not address it).
- Do not mix review fixes with new features in the same push.
- After the fixes, re-run the suite and say so in the PR.
- AI review comments: apply the same verification; discard noise without arguing.
