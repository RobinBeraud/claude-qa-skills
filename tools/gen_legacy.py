from _gen import write_plugin

PLUGIN = "dev-legacy"
DESC = "Working safely in large, old codebases: hotspot analysis from git history (churn x size) with a bundled script, strangler-fig migrations (pin behaviour first with qa-automation:characterization-tests), TFVC to Git migration, fix backporting across release branches with a missing-commit report script, and dead-code removal."

S = {}

S["codebase-hotspots"] = ("""Find where a legacy codebase hurts with a bundled stdlib script over git history: files ranked by change frequency x size (hotspots), number of authors, recent activity, and files that always change together (hidden coupling), to decide where to refactor, test or review first. Use when starting on a large legacy repository, prioritising technical debt, planning refactoring, or choosing where to add tests first.""", r"""
# Codebase hotspots

Complexity that never changes is not urgent. Complexity that changes every week is where bugs and slow reviews come from.

## Run
```bash
python "${CLAUDE_SKILL_DIR}/scripts/hotspots.py" --repo . --since 2025-01-01 --top 25
python "${CLAUDE_SKILL_DIR}/scripts/hotspots.py" --repo . --since 12.months --path src/Billing --format md
```
For each file: commits in the period, distinct authors, current lines, a hotspot score (commits x lines, normalised), last change; plus the most frequent co-changing pairs.

## Read it
1. **Top hotspots**: big files that change all the time. Candidates for characterisation tests first (`qa-automation:characterization-tests`), then refactoring in small steps.
2. **Many authors on one file**: knowledge is diluted; reviews must be careful there.
3. **Co-change pairs across modules**: hidden coupling (e.g. a UI file and a stored procedure always changed together); consider moving them closer or making the contract explicit.
4. Exclude generated files (`--exclude` patterns) before drawing conclusions.

## Output
Top hotspots with a one-line recommendation each (test first / split / leave alone), coupling list, and the 3 refactorings with the best return.
""")

S["strangler-fig"] = ("""Replace a legacy system or module incrementally with the strangler fig pattern: facade or proxy in front, route one capability at a time to the new implementation, keep data in sync, compare old and new outputs (parallel run), switch with feature flags, and retire the old path when traffic is zero. Use when rewriting or re-platforming a legacy module, moving from a monolith to services, or replacing an old UI or API without a big-bang cut-over.""", r"""
# Strangler fig

## Steps
0. **Pin behaviour first** with `qa-automation:characterization-tests` on the slice you will replace.
1. **Slice by capability**, not by layer: "invoice PDF generation", "customer search". Order by value and risk; start with a small, low-risk, well-understood slice.
2. **Facade**: a single entry point (reverse proxy such as YARP, API gateway, an interface in the code) that can route each capability to old or new.
3. **Data**: decide who owns each data set during transition. Options: new reads from old DB (anti-corruption layer), change data capture to sync, or dual writes with reconciliation.
4. **Parallel run** for risky slices: send the request to both, return the old result, log differences, fix until the diff rate is ~0.
5. **Switch** with a flag per tenant or percentage (internal users -> pilot customers -> all). Monitor errors, latency, business KPIs.
6. **Retire**: when traffic on the old path is zero for a full business cycle (month-end, year-end closing for finance software), delete the old code.

## Rules
- Each slice ships to production; no long-lived rewrite branch.
- Business cycles matter: test month-end and year-end paths before retiring anything in finance or payroll software.
- Keep a visible board of slices: old / both / new / retired.
""")

S["tfvc-to-git"] = ("""Migrate source code from TFVC (Team Foundation Version Control) to Git in Azure DevOps: choose history depth (tip only, recent history or full via git-tfs), map TFVC branches to Git branches, handle large binaries with Git LFS or removal, rewrite build pipelines, and switch the team over with a freeze window. Use when a team still on TFVC wants Git, when planning the migration of a large TFVC repository, or when changesets must be mapped to commits.""", r"""
# TFVC to Git

## Decide the history
| Option | When | How |
|---|---|---|
| Tip only (+ TFVC kept read-only for archaeology) | most teams, fastest | Azure DevOps "Import repository" from TFVC (up to 180 days of history), or a clean snapshot |
| Recent history | need blame on recent work | Azure DevOps import with history window |
| Full history | audit or heavy archaeology needs | `git-tfs clone` (slow on big repos; can take days) |

## Prepare
1. **Branches**: list TFVC branches (`tf branches`), decide which become Git branches (Main -> `main`, releases -> `release/x.y`); many old branches are not worth migrating.
2. **Size**: find large binaries (third-party DLLs, installers, databases). Move dependencies to NuGet/npm packages, put needed binaries in Git LFS, drop the rest.
3. **`.gitignore`** for `bin/ obj/ packages/ *.user` before the first commit; normalise line endings with `.gitattributes`.
4. **Pipelines**: update build definitions (TFVC paths, workspace mappings, `$(Build.SourceVersion)` semantics: changeset number -> commit SHA, so version numbering must change).

## Cut-over
Freeze TFVC check-ins, final import, verify the build and the tests from Git, lock TFVC as read-only, train the team (branching model, pull requests, policies). Keep a mapping changeset -> commit if history was migrated (git-tfs notes) for audits.

## Rules
Rehearse on a copy first and time it; never migrate during a release crunch.
""")

S["release-backports"] = ("""Manage fixes across several maintained release branches: decide where a fix must go, cherry-pick or merge forward in a consistent direction, track which fixes are missing from which branch with a bundled script (git cherry with patch-id matching), and avoid regressions where a fix exists in an old version but not in a newer one. Use when maintaining several product versions, when a hotfix must reach multiple branches, or before cutting a release to check no fix was forgotten.""", r"""
# Release backports

## Policy first (write it down)
- **Direction**: fix on the oldest supported branch and merge **forward**, or fix on `main` and cherry-pick **back**. Pick one per repository; mixing both creates duplicates and conflicts.
- **Which branches**: supported versions list, with end-of-support dates.
- **Traceability**: the commit message or PR references the work item (`AB#1234`) and the original commit (`git cherry-pick -x` adds "cherry picked from commit ...").

## Find missing fixes
```bash
python "${CLAUDE_SKILL_DIR}/scripts/backport_check.py" --repo . --source release/12.4 --targets release/13.0,main --since 2026-01-01
python "${CLAUDE_SKILL_DIR}/scripts/backport_check.py" --repo . --source main --targets release/12.4 --grep "AB#" --format md
```
For each target: commits of the source branch whose change (patch-id) is not in the target, with their work-item references; also reports work items present in the source but absent from the target's history even when the patch differs (conflict-resolved backports).

## Rules
- A fix present in version N but missing in N+1 is a **regression waiting for an upgrade**: check before every release.
- Conflicts on backport: re-test on that branch; do not assume the original tests cover it.
- Automate the check in the release pipeline and list exceptions explicitly (fix not needed on that version, with reason).
""")

S["dead-code-removal"] = ("""Remove dead code, unused dependencies and obsolete feature flags safely: find candidates with compiler and IDE analysis, coverage and production telemetry, verify nothing calls them dynamically (reflection, configuration, reports, external callers), delete in small reviewed steps, and keep the deletion revertible. Use when cleaning a legacy codebase, before an upgrade or migration, when a feature flag is fully rolled out, or when the build is slowed by unused projects.""", r"""
# Dead code removal

Deleting code is the cheapest way to reduce bugs, build time and upgrade effort, if it is really dead.

## Find candidates
- Compiler/IDE: unused private members, unreferenced projects and files (Roslyn analyzers IDE0051/IDE0052, ReSharper/Rider solution-wide analysis, `ts-prune`/`knip` for TypeScript).
- Production evidence: endpoints with zero calls over a full business cycle (logs, APM), reports never run, jobs never scheduled.
- Feature flags at 100 % for more than one release: remove the flag and the old branch of code.
- Dependencies: packages not referenced by any code (`dotnet list package` + search, `depcheck`/`knip`).

## Verify before deleting
Reflection and dependency injection by name, configuration files, stored procedures called from reports, scheduled tasks, external clients calling an API, customer-specific extensions or scripts. Search the whole organisation's repositories, not only this one, for public APIs.

## Delete
Small PRs by area, each building and passing tests; the PR lists the evidence (zero calls since ..., no references). For public APIs: deprecate first (warning, header, docs), remove one version later.
""")

write_plugin(PLUGIN, DESC, S, ["legacy", "refactoring", "tfvc", "git", "release-management"])
