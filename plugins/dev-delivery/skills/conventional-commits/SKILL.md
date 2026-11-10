---
name: conventional-commits
description: "Write commit messages that tools and humans can use: Conventional Commits (feat, fix, refactor, perf, test, docs, build, ci, chore; scope; breaking changes), lint them and generate a grouped changelog between two refs with a bundled stdlib script that also extracts work-item references. Use when writing commit messages, preparing release notes or a changelog, or setting up a commit convention for a team."
---

# Conventional commits

## Format
```
fix(billing): round VAT per invoice line

EN 16931 BR-CO-17 requires the VAT amount per rate to equal the rounded
sum of line amounts x rate. AB#12346
```
- Type: `feat` (user-visible feature), `fix`, `perf`, `refactor` (no behaviour change), `test`, `docs`, `build`, `ci`, `chore`, `revert`.
- Subject: imperative, lower case, no final dot, <= 72 characters. Body: **why**, not what.
- Breaking change: `feat(api)!: ...` and a `BREAKING CHANGE:` footer.

## Lint and changelog
```bash
python "${CLAUDE_SKILL_DIR}/scripts/changelog.py" lint --repo . --range origin/main..HEAD
python "${CLAUDE_SKILL_DIR}/scripts/changelog.py" notes --repo . --range v12.3.0..v12.4.0 --format md
```
`lint` lists non-conforming subjects (exit 1 if any). `notes` groups commits by type (breaking changes first), keeps scopes, and lists referenced work items (AB#, #, JIRA-123).

## Release notes for customers
Generated notes are for developers. Customer notes are rewritten from `feat`/`fix` items in business language, without internal ids or names.
