---
name: small-pull-requests
description: "Keep pull requests small and reviewable: measure a diff against a size budget with a bundled script (lines, files, areas touched, generated or lock files excluded), and split oversized work into a stack of independent PRs (refactor first, feature behind a flag, cleanup last). Use before opening a pull request, when a branch keeps growing, or when reviews are slow because PRs are big."
---

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
