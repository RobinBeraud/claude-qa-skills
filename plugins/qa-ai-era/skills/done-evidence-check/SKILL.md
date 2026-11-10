---
name: done-evidence-check
description: "Refuse \"it should work\": before a task, PR or story is called done, collect the evidence: build and test commands actually run with their output, each acceptance criterion mapped to proof, what was not verified, and residual risks. Use at the end of any implementation task by a human or an agent, or when asked whether something is really finished."
---

# Done means evidence

## Steps
1. List the acceptance criteria / definition of done items.
2. **Run** the checks now, in this session: build, unit tests, relevant integration/E2E tests, linter, type check. Paste the commands and the tail of their output. Do not report results you did not observe.
3. Map each criterion to its proof: test name, command output, screenshot description, or manual check performed (by whom).
4. List **not verified** items plainly (other browsers, performance, migration on real data volume...).
5. List residual risks and how they are mitigated (flag, monitoring, rollback).

## Output
```
DONE CHECK: <task>
Commands run: ...
Criteria:   1 ✔ test_x  2 ✔ test_y  3 ✘ not covered -> blocking
Not verified: ...
Risks: ...
Verdict: DONE | NOT DONE (what is missing)
```
