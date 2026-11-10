---
name: work-item-linking
description: "Link code to work items and query Azure DevOps Boards from the command line: AB#id mentions in commits and pull requests, branch naming by work item, az boards and az repos CLI commands, WIQL queries for open bugs or items without linked PRs, and GitLab or Jira equivalents. Use when committing or opening a pull request that relates to a ticket, when listing or updating work items, or when checking traceability between tickets and code."
---

# Work-item linking

## Conventions
- Branch: `feature/12345-short-title`, `fix/12346-vat-rounding`.
- Commit or PR description: `AB#12345` links the Azure Boards item (also from GitHub repos with the Boards app). GitLab: `Closes #12`, Jira: `PROJ-123` in the title.
- One PR, one main work item; others linked as related.

## az CLI (needs `az extension add --name azure-devops` and `az devops configure --defaults organization=https://dev.azure.com/<org> project=<project>`)
```bash
az boards work-item show --id 12345 --fields System.Title,System.State,System.AssignedTo
az boards query --wiql "SELECT [System.Id],[System.Title] FROM WorkItems WHERE [System.WorkItemType]='Bug' AND [System.State] <> 'Done' AND [System.AreaPath] UNDER '<project>\\<team>' ORDER BY [System.CreatedDate] DESC"
az repos pr create --source-branch fix/12346-vat-rounding --target-branch main --title "Round VAT per line" --work-items 12346 --draft
az repos pr list --status active --output table
```

## Rules
- Update the work item state through the PR (policies can require a linked work item).
- Never paste customer personal data into work items or commits.
- Changing work items in bulk (state, assignment) affects other people's boards: confirm with the user first.
