---
name: parallel-worktrees
description: "Work on several branches or let several agents work in parallel without collisions using git worktrees: one folder per task, shared object store, per-worktree build outputs, safe cleanup. Use when running multiple Claude sessions or sub-agents on the same repository, when a hotfix interrupts feature work, or when comparing two approaches side by side."
---

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
