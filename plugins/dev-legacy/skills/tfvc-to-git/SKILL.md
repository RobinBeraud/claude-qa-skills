---
name: tfvc-to-git
description: "Migrate source code from TFVC (Team Foundation Version Control) to Git in Azure DevOps: choose history depth (tip only, recent history or full via git-tfs), map TFVC branches to Git branches, handle large binaries with Git LFS or removal, rewrite build pipelines, and switch the team over with a freeze window. Use when a team still on TFVC wants Git, when planning the migration of a large TFVC repository, or when changesets must be mapped to commits."
---

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
