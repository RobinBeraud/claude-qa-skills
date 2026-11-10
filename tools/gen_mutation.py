from _gen import write_plugin

PLUGIN = "qa-mutation-testing"
DESC = "Measure whether tests would notice a bug: set up mutation testing per stack, read reports with a bundled script, triage surviving and equivalent mutants, write the tests that kill them, and gate pull requests on the mutation score of changed code."

S = {}

S["mutation-testing-setup"] = ("""Set up mutation testing for a project: pick the tool for the stack (Stryker for JS/TS and .NET, PIT for Java/Kotlin, mutmut or cosmic-ray for Python, Infection for PHP, go-mutesting for Go), scope it to business-critical code, configure timeouts and reporters, and run a first baseline. Use when starting with mutation testing or when coverage is high but bugs still slip through.""", r"""
# Mutation testing setup

Line coverage says the code ran; the mutation score says a test would fail if the code were wrong.

## Tool per stack
| Stack | Tool | First run |
|---|---|---|
| JS / TS | StrykerJS | `npx stryker init` then `npx stryker run` |
| .NET | Stryker.NET | `dotnet tool install -g dotnet-stryker` then `dotnet stryker` |
| Java / Kotlin | PIT (pitest) | `mvn org.pitest:pitest-maven:mutationCoverage` or the Gradle plugin |
| Python | mutmut / cosmic-ray | `mutmut run --paths-to-mutate src/billing` |
| PHP | Infection | `vendor/bin/infection` |

## Steps
1. **Scope**: one package with business logic (pricing, rules, calculations). Exclude generated code, DTOs, logging.
2. **Configure**: test command, timeout factor, concurrency, the JSON reporter (`mutation-testing-report-schema` for Stryker, `XML`/`HTML` for PIT).
3. **Baseline**: run once, record the score and duration.
4. **Read the report** with `mutation-report-digest`, then triage with `surviving-mutant-triage`.
5. Make it part of the routine: nightly on critical packages, or incremental on PRs (`mutation-score-gate`).

## Output
Config file, commands, baseline score and duration, and the 10 most important survivors.
""")

S["mutation-report-digest"] = ("""Summarise a mutation testing report (Stryker mutation-testing-report-schema JSON, used by StrykerJS, Stryker.NET and Stryker4s, or PIT mutations.xml) with a bundled stdlib script: score per file, survivors and no-coverage mutants grouped by file and mutator, worst files first. Use after a mutation run, or when a report is too big to read.""", r"""
# Mutation report digest

## Run
```bash
python "${CLAUDE_SKILL_DIR}/scripts/mutation_report.py" reports/mutation/mutation.json --top 15
python "${CLAUDE_SKILL_DIR}/scripts/mutation_report.py" target/pit-reports/mutations.xml
```

## What you get
- Overall mutation score = killed / (killed + survived + no coverage + timeout counted as killed), with counts per status.
- Per file: score, survivors, no-coverage mutants; sorted by number of survivors.
- Survivors by mutator type (e.g. `EqualityOperator`, `ConditionalBoundary`, `ArithmeticOperator`): shows which kind of assertion the suite lacks.
- The first survivors with file:line and the mutated code, ready for triage.

## Then
Continue with `surviving-mutant-triage` on the worst files. Do not chase 100 %: aim at the critical files.
""")

S["surviving-mutant-triage"] = ("""Triage surviving mutants one by one: classify each as missing assertion, missing test case, equivalent mutant, or dead/unreachable code, explain why the tests did not notice the change, and propose the smallest fix (a test, an assertion, or deleting code). Use after a mutation run, when reviewing test quality, or when auditing tests written by an AI agent.""", r"""
# Surviving mutant triage

## For each survivor
1. Read the mutated line and the change (e.g. `>=` became `>`, `+` became `-`, a call removed, a return replaced by `null`).
2. Find the tests that execute that line (coverage report or by name).
3. Classify:
   | Class | Meaning | Action |
   |---|---|---|
   | Missing assertion | A test runs the line but does not check the result | Add the assertion |
   | Missing case | No test hits the distinguishing input (e.g. the exact boundary) | Add a test case |
   | Equivalent mutant | The change does not alter behaviour (see `equivalent-mutant-check`) | Mark ignored with a comment |
   | Dead code | The line can never matter | Delete it |
4. Write the fix and re-run the tool on that file to confirm the mutant is now killed.

## Output
| File:line | Mutation | Class | Fix | Killed after fix? |
""")

S["equivalent-mutant-check"] = ("""Decide whether a surviving mutant is equivalent (no observable behaviour change, so no test can kill it) or a real gap, using reasoning about reachable inputs, side effects and invariants; document legitimate equivalents so they stop polluting the score. Use when mutants survive that look impossible to kill.""", r"""
# Equivalent mutant check

## Reasoning steps
1. State the original and mutated expressions.
2. Find the **input domain actually reachable** at that point (guards above, types, invariants).
3. Is there any reachable input where both versions produce a different **observable** result (return value, state, exception, call, log that matters)?
   - Yes: real gap. Give the input that distinguishes them; it becomes the new test case.
   - No: equivalent. Typical cases: `i < n` vs `i != n` in a loop that only increments by one; removed call to a pure function whose result is unused; changed log message nobody asserts.
4. For equivalents, use the tool's ignore mechanism (Stryker `// Stryker disable next-line <mutator>: reason`, PIT `excludedMethods`, mutmut `# pragma: no mutate`) **with the reason**.
5. If many equivalents appear in the same code, it is often a hint to simplify the code.

## Output
Verdict per mutant: equivalent (proof) or gap (distinguishing input and test).
""")

S["mutant-killer-tests"] = ("""Write the smallest, clearest tests that kill a list of surviving mutants (from a report or a triage), one behaviour per test, reusing existing fixtures, then re-run mutation testing on the file to prove each mutant is killed. Use after surviving-mutant-triage, or to harden tests around critical calculations.""", r"""
# Tests that kill mutants

## Steps
1. Group survivors by behaviour (several mutants often fall to one good test).
2. For each group, write a test named after the **behaviour**, not the mutant (`test_fee_applies_from_the_day_after_due_date`, not `test_kill_mutant_42`).
3. Use the distinguishing input found in triage; assert the exact expected value.
4. Run the normal suite (green), then the mutation tool on the file only (incremental mode if available).
5. Report: mutants killed, still surviving (with reason), score before/after for the file.

## Rules
- Never assert on implementation details just to kill a mutant; if only an internal detail distinguishes the mutant, it is probably equivalent or the code is too clever.
- Keep tests readable for humans: they are documentation of the rule.
""")

S["mutation-score-gate"] = ("""Add a pragmatic mutation-testing quality gate to CI: incremental mutation on changed files only (Stryker --incremental / since, PIT with scmMutationCoverage or history), a threshold on the changed code rather than the whole repo, time limits, and a clear report in the pull request. Use when the team wants mutation testing in the pipeline without slowing every build.""", r"""
# Mutation score gate

## Design
- **Changed code only**: mutate files touched by the PR (`stryker run --since=main`, `--incremental`, PIT `scmMutationCoverage` or `withHistory`). Full runs stay nightly.
- **Threshold on changed code**, e.g. break below 70 % for files in critical packages, warn elsewhere. Start low, raise gradually.
- **Time box**: cap the job (e.g. 15 min); if exceeded, warn instead of failing.
- **Report in the PR**: score, survivors with file:line (the `mutation-report-digest` output fits a PR comment).

## Example (StrykerJS, GitHub Actions)
```yaml
- run: npx stryker run --incremental --since=origin/main --thresholds.break 70
```
## Rules
- Exclude generated code and tests from mutation.
- Equivalent mutants are ignored with a documented reason, never by lowering the threshold globally.

## Output
Pipeline snippet for the team's CI (GitHub Actions, Azure Pipelines or GitLab CI), threshold policy, and the rollout plan (warn for 2 weeks, then break).
""")

write_plugin(PLUGIN, DESC, S, ["mutation-testing", "stryker", "pitest", "test-quality"])
