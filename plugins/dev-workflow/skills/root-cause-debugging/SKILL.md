---
name: root-cause-debugging
description: "Debug by finding the root cause before changing code: reproduce, read the full error, check what changed, form one hypothesis at a time and test it, write the failing test, then fix; with a hard stop after three failed fixes to question the approach. Use when a test fails, a bug is reported, behaviour is unexpected, a build breaks, or a previous fix did not work."
---

# Root-cause debugging

```
NO FIX WITHOUT A REPRODUCTION AND A ROOT CAUSE
```

## Phase 1: evidence
1. Read the **whole** error and stack trace: exception type, message, the first frame in our code, inner exceptions.
2. **Reproduce** with the smallest input. Not reproducible? Collect more data (logs, correlation id, tenant, version, time) instead of guessing.
3. **What changed?** `git log --since`, recent deployments, configuration, data, dependency updates. `git bisect` when a known good version exists.
4. In multi-layer flows (UI -> API -> service -> DB -> batch), log or inspect at each boundary to find where the value goes wrong.

## Phase 2: hypothesis
5. State **one** hypothesis: "the total is wrong because rounding is applied on the sum, not per line". Predict what you will see if it is true.
6. Test it with the cheapest experiment (debugger, a log line, a unit test). Revert experiments afterwards.

## Phase 3: fix
7. Write a **failing test** that reproduces the bug. Watch it fail for the right reason.
8. Fix the cause, not the symptom (no `try/catch` that hides it, no `if (value == weird) return`).
9. Run the test, then the whole suite. Search for the same pattern elsewhere (`git grep`).

## Stop rule
Three fixes tried and failed? **Stop.** The model of the system is wrong. Re-read the code path end to end, question the architecture, ask someone who knows the module.

## Red flags
"Quick fix for now", changing several things at once, a fix without a test, "works on my machine".
