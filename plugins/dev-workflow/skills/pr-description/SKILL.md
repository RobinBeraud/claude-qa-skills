---
name: pr-description
description: "Write a pull request description from the actual diff and the work item: why (problem and link), what changed, how it was tested with evidence, risks and rollback, what reviewers should look at first, and checklist items (migrations, config, feature flags, docs). Use when opening or updating a pull request or merge request in Azure DevOps, GitHub or GitLab."
---

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
