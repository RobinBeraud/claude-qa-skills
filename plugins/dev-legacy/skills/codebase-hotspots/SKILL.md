---
name: codebase-hotspots
description: "Find where a legacy codebase hurts with a bundled stdlib script over git history: files ranked by change frequency x size (hotspots), number of authors, recent activity, and files that always change together (hidden coupling), to decide where to refactor, test or review first. Use when starting on a large legacy repository, prioritising technical debt, planning refactoring, or choosing where to add tests first."
---

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
