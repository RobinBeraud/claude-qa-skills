---
name: release-backports
description: "Manage fixes across several maintained release branches: decide where a fix must go, cherry-pick or merge forward in a consistent direction, track which fixes are missing from which branch with a bundled script (git cherry with patch-id matching), and avoid regressions where a fix exists in an old version but not in a newer one. Use when maintaining several product versions, when a hotfix must reach multiple branches, or before cutting a release to check no fix was forgotten."
---

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
