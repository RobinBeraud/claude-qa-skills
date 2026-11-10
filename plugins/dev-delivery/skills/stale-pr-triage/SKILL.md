---
name: stale-pr-triage
description: "Triage the open pull request backlog: from an exported list (Azure DevOps, GitHub or GitLab JSON) compute age, idle time, draft status, reviewer load and size buckets with a bundled stdlib script, then decide per PR to merge, rebase, split, hand over or abandon, and set an aging policy. Use when many pull requests or merge requests are open for weeks or months, when review is a bottleneck, or before a cleanup or a release."
---

# Stale PR triage

Old open PRs are inventory: they rot, conflict, and hide work nobody will ship.

## Export
```bash
az repos pr list --status active --top 1000 -o json > prs.json          # Azure DevOps
gh pr list --state open --limit 1000 --json number,title,author,createdAt,updatedAt,isDraft,reviewRequests,additions,deletions > prs.json
glab mr list --output json > prs.json                                    # or the GitLab API
```

## Analyse
```bash
python "${CLAUDE_SKILL_DIR}/scripts/stale_prs.py" prs.json --as-of 2026-11-10 --stale-days 30
```
Detects the source format, then reports: count by age bucket (< 7 d, 7-30, 30-90, 90-365, > 1 year), median age, drafts, PRs idle (no update) longer than `--stale-days`, open PRs per author and per reviewer, and the oldest PRs.

## Decide per PR (with its author)
| Situation | Action |
|---|---|
| Ready, just waiting | assign a reviewer today, merge |
| Conflicts but still wanted | rebase, re-test, review |
| Too big | split (see `dev-workflow:small-pull-requests`) |
| Author gone | hand over or abandon |
| Superseded or experiment | close with a comment explaining why |

## Policy
WIP limit on open PRs per person, a review service level (first review within 1 working day), weekly 15-minute triage, auto-reminders at 7 days and a close-or-keep decision at 30 days.
