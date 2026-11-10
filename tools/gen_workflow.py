from _gen import write_plugin

PLUGIN = "dev-workflow"
DESC = "Agentic development discipline: explore before editing, plan in files, root-cause debugging (pairs with qa-ai-era:done-evidence-check), small pull requests with a size budget, PR descriptions from the diff, self-review, handling review feedback, parallel worktrees and session handoff."

S = {}

S["explore-before-editing"] = ("""Build a working map of an unfamiliar codebase before changing it: entry points, layers, conventions, build and test commands, where the change belongs, and what could break. Use when starting work in a repository or module you have not touched yet, when a change request names code you have not read, or before any refactor that crosses several files.""", r"""
# Explore before editing

```
NO EDIT BEFORE YOU CAN SAY WHERE THE CHANGE GOES AND HOW YOU WILL KNOW IT WORKS
```

## Steps
1. **Build and test commands**: find them (README, `*.sln`, `package.json`, `Makefile`, pipeline YAML) and run the tests once to get a baseline. Note pre-existing failures; they are not yours.
2. **Map**: entry points (controllers, jobs, CLI, UI routes), layers, the 5-10 files that matter for this change. Use search, not guesses: `git grep`, symbol search, callers of the function.
3. **Conventions**: naming, error handling, logging, DI, test style. Read two neighbouring files and copy their patterns.
4. **History**: `git log --oneline -15 -- <path>` and blame on the lines you will touch. Why is it like this? A strange line often fixes a real bug.
5. **Blast radius**: who calls this code (other modules, APIs, batch jobs, reports)? Public contracts (API, DB schema, file formats) need extra care.
6. **Write it down** in 10 lines: where the change goes, files to touch, tests to add, risks, open questions. Ask the open questions before coding.

## Red flags
- "I'll just add it here" without having read the callers.
- Creating a new helper when an equivalent exists two folders away.
- Changing formatting or names in files you only needed to read.

## Output
A short map: commands, key files, conventions, blast radius, plan, questions.
""")

S["plan-in-files"] = ("""Plan multi-step work in a markdown file kept in the repository: goal, constraints, task list with the test that proves each task, decisions log and progress, updated as you go so work survives context loss, a crash or a handoff. Use for any task longer than about an hour, a feature spanning several files, a migration, or when the user says "plan it first".""", r"""
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
""")

S["root-cause-debugging"] = ("""Debug by finding the root cause before changing code: reproduce, read the full error, check what changed, form one hypothesis at a time and test it, write the failing test, then fix; with a hard stop after three failed fixes to question the approach. Use when a test fails, a bug is reported, behaviour is unexpected, a build breaks, or a previous fix did not work.""", r"""
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
""")

S["small-pull-requests"] = ("""Keep pull requests small and reviewable: measure a diff against a size budget with a bundled script (lines, files, areas touched, generated or lock files excluded), and split oversized work into a stack of independent PRs (refactor first, feature behind a flag, cleanup last). Use before opening a pull request, when a branch keeps growing, or when reviews are slow because PRs are big.""", r"""
# Small pull requests

Review time grows faster than PR size; defects slip through large diffs. Aim for **< 400 changed lines** and one purpose per PR.

## Measure
```bash
python "${CLAUDE_SKILL_DIR}/scripts/pr_size.py" --base origin/main
python "${CLAUDE_SKILL_DIR}/scripts/pr_size.py" --base origin/develop --budget 300 --format md
```
Reports changed lines and files (lock files, generated code, snapshots and migrations' designer files counted apart), top-level areas touched, and a verdict against the budget with a split suggestion by area.

## Split strategies
| Situation | Split |
|---|---|
| Refactor + feature | PR 1 pure refactor (no behaviour change), PR 2 feature |
| Feature too big | Vertical slices behind a feature flag, each shippable |
| Rename / move | Mechanical PR alone, reviewed fast |
| Schema change | Expand migration first, code next, contract later |
| Formatting noise | Separate PR or nothing |

## Rules
- One purpose per PR, stated in its title.
- Generated changes (migrations, lock files, snapshots) are listed in the description so reviewers can skip them knowingly.
- Stacked PRs: each targets the previous branch, and each passes CI alone.
""")

S["pr-description"] = ("""Write a pull request description from the actual diff and the work item: why (problem and link), what changed, how it was tested with evidence, risks and rollback, what reviewers should look at first, and checklist items (migrations, config, feature flags, docs). Use when opening or updating a pull request or merge request in Azure DevOps, GitHub or GitLab.""", r"""
# PR description

## Gather
`git log --oneline <base>..HEAD`, `git diff --stat <base>...HEAD`, the work item or ticket (id, acceptance criteria), test output.

## Template
```markdown
## Why
<problem in 1-3 sentences> -- AB#12345 (Azure DevOps) / PROJ-123 (Jira) / #123

## What
- <change 1, user-visible first>
- <change 2>

## How it was tested
- Unit: <tests added>, suite <n> passed
- Manual: <steps, environment, data>
- Not tested: <honest gaps>

## Risk and rollback
<what could break, who is affected, how to roll back (flag, revert, migration down)>

## Review guide
Start with <file>, the core change; <folder> is generated / mechanical.

## Checklist
- [ ] DB migration (backward compatible?)  - [ ] config / feature flag  - [ ] docs / changelog  - [ ] security or personal-data impact
```

## Rules
- Describe the diff that exists, not the intention. Re-read the diff before writing.
- In Azure DevOps, `AB#<id>` in the description or commit links the work item; in GitLab, `Closes #id`.
- Title: imperative, specific, < 72 characters ("Round VAT per invoice line (EN 16931 BR-CO-17)").
- Never paste secrets, customer data or production logs with personal data.
""")

S["self-review"] = ("""Review your own diff before asking anyone else: read it as a reviewer would, file by file, against a checklist (correctness, edge cases, errors, tests, security, performance, naming, leftovers like debug code, TODOs and commented code), then fix what you find. Use before opening a pull request, before asking for review, and after an AI agent produced a change.""", r"""
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
""")

S["receive-review"] = ("""Handle code review feedback rigorously: understand each comment, verify the claim against the code before agreeing, fix or push back with evidence, answer every thread, and avoid both blind acceptance and defensiveness. Use when a pull request receives review comments, when an AI reviewer leaves suggestions, or when feedback seems wrong or unclear.""", r"""
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
""")

S["parallel-worktrees"] = ("""Work on several branches or let several agents work in parallel without collisions using git worktrees: one folder per task, shared object store, per-worktree build outputs, safe cleanup. Use when running multiple Claude sessions or sub-agents on the same repository, when a hotfix interrupts feature work, or when comparing two approaches side by side.""", r"""
# Parallel worktrees

## Create
```bash
git fetch origin
git worktree add ../repo-fix-1234 -b fix/1234-vat-rounding origin/main
git worktree add ../repo-spike-cache -b spike/cache origin/develop
git worktree list
```
Each worktree is a full checkout sharing the same `.git` objects: cheap and fast.

## Rules
1. One task, one worktree, one branch. Never two agents in the same folder.
2. Build outputs, `node_modules`, `bin/obj` are per worktree: the first build is slower; plan it.
3. Local config (`.env`, `appsettings.Development.json`, user secrets) is not copied; recreate it deliberately, never commit it.
4. Ports and databases: give each worktree its own port and test database to avoid collisions.
5. Large repositories: `git clone --filter=blob:none` once, then worktrees; `git sparse-checkout` for monorepos.

## Clean up
```bash
git worktree remove ../repo-spike-cache     # refuses if there are uncommitted changes: good
git branch -D spike/cache                    # only when the work is merged or abandoned
git worktree prune
```
""")

S["session-handoff"] = ("""Hand off work between sessions, people or agents without losing context: a short handoff note with goal, state, what was verified, what is left, decisions, gotchas and the exact next step, stored with the code. Use at the end of a work session, before a context reset, when passing a task to a colleague or a sub-agent, or when resuming someone else's branch.""", r"""
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
""")

write_plugin(PLUGIN, DESC, S, ["workflow", "pull-requests", "debugging", "planning"])
