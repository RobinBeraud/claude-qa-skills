from _gen import write_plugin

PLUGIN = "dev-delivery"
DESC = "Delivery on Azure DevOps and GitLab: YAML pipelines with templates, caching and approvals, work-item linking and WIQL queries with the az CLI, Conventional Commits with a changelog and commit-lint script, stale pull request triage from exported PR lists with a bundled script, feature flags, and blameless incident reviews."

S = {}

S["azure-pipelines"] = ("""Write and fix Azure DevOps YAML pipelines: stages, jobs and templates for reuse, caching NuGet and npm, test results and coverage publishing, environments with approvals and checks, variable groups linked to Key Vault, path filters and PR validation, and diagnosing failed runs from logs. Use when creating or editing azure-pipelines.yml, converting classic build or release pipelines to YAML, speeding up a slow pipeline, or debugging a failing pipeline.""", r"""
# Azure Pipelines (YAML)

## Skeleton
```yaml
trigger:
  branches: { include: [main, release/*] }
  paths: { exclude: [docs/*] }
pr:
  branches: { include: [main] }

variables:
  - group: billing-common          # variable group, secrets from Key Vault
  - name: buildConfiguration
    value: Release

stages:
- stage: Build
  jobs:
  - job: build
    pool: { vmImage: windows-latest }
    steps:
    - task: Cache@2
      inputs:
        key: 'nuget | "$(Agent.OS)" | **/packages.lock.json'
        path: $(NUGET_PACKAGES)
    - script: dotnet restore --locked-mode
    - script: dotnet build -c $(buildConfiguration) --no-restore
    - script: dotnet test -c $(buildConfiguration) --no-build --logger trx --collect:"XPlat Code Coverage"
    - task: PublishTestResults@2
      condition: always()
      inputs: { testResultsFormat: VSTest, testResultsFiles: '**/*.trx' }
- stage: DeployProd
  dependsOn: Build
  condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
  jobs:
  - deployment: prod
    environment: billing-prod      # approvals and checks are configured on the environment
    strategy: { runOnce: { deploy: { steps: [ { script: echo deploy } ] } } }
```

## Practices
- **Templates** (`template: templates/dotnet-build.yml`, with parameters) shared from a central repo via `resources.repositories`; pin them to a tag.
- **Speed**: cache, `--no-restore/--no-build`, path filters, parallel jobs, test sharding; measure the slowest step first.
- **Security**: secrets only from variable groups/Key Vault, marked secret, never echoed; least-privilege service connections; approvals on production environments; protect `main` with build validation policies.
- **Debug a failure**: read the first error, not the last line; rerun with `system.debug: true`; reproduce the exact command locally.
""")

S["work-item-linking"] = ("""Link code to work items and query Azure DevOps Boards from the command line: AB#id mentions in commits and pull requests, branch naming by work item, az boards and az repos CLI commands, WIQL queries for open bugs or items without linked PRs, and GitLab or Jira equivalents. Use when committing or opening a pull request that relates to a ticket, when listing or updating work items, or when checking traceability between tickets and code.""", r"""
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
""")

S["conventional-commits"] = ("""Write commit messages that tools and humans can use: Conventional Commits (feat, fix, refactor, perf, test, docs, build, ci, chore; scope; breaking changes), lint them and generate a grouped changelog between two refs with a bundled stdlib script that also extracts work-item references. Use when writing commit messages, preparing release notes or a changelog, or setting up a commit convention for a team.""", r"""
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
""")

S["stale-pr-triage"] = ("""Triage the open pull request backlog: from an exported list (Azure DevOps, GitHub or GitLab JSON) compute age, idle time, draft status, reviewer load and size buckets with a bundled stdlib script, then decide per PR to merge, rebase, split, hand over or abandon, and set an aging policy. Use when many pull requests or merge requests are open for weeks or months, when review is a bottleneck, or before a cleanup or a release.""", r"""
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
""")

S["feature-flags"] = ("""Use feature flags to ship safely: choose the flag type (release, experiment, operational kill switch, permission or tenant), implement with a flag library or Azure App Configuration, roll out by tenant or percentage, test both paths, and remove flags once fully released to avoid flag debt. Use when shipping a risky change, decoupling deployment from release, doing a pilot with some customers, or cleaning up old flags.""", r"""
# Feature flags

## Types
| Type | Lifetime | Example |
|---|---|---|
| Release | days to weeks | new invoice screen hidden until ready |
| Pilot / tenant | weeks | enabled for 3 pilot customers |
| Experiment | duration of a test | A/B on onboarding |
| Operational kill switch | permanent | disable PDF generation if the service is down |
| Permission | permanent | paid option (this is entitlement, keep it separate) |

## Implementation
- .NET: `Microsoft.FeatureManagement` (filters for percentage, time window, targeting by tenant), backed by Azure App Configuration or config files. Front-end: read flags from the back end, never trust them for security.
- Evaluate once per request and pass the result down; no flag checks deep in loops.
- Default **off** for new features; kill switches default to the safe state.

## Testing
Both paths tested in CI while the flag lives. Production tests cover the "on" path for pilot tenants.

## Flag debt
Every release flag has an owner and a removal date in its work item. Remove the flag and the dead branch within one release after 100 % rollout (see `dev-legacy:dead-code-removal`).
""")

S["incident-review"] = ("""Run a blameless post-incident review: factual timeline from logs and chat, impact in customer terms, contributing factors (not a single root cause or a person), what helped and what slowed detection and recovery, and a few owned, dated actions; for production outages, data issues, security events or failed releases. Use after a production incident, a hotfix, a rollback, a data correction, or a near miss worth learning from.""", r"""
# Incident review (blameless)

People did what made sense with what they knew at the time. The question is what made it make sense.

## Document (within 5 working days)
```markdown
# Incident <id>: <short title>   Severity: <S1-S4>   Status: resolved
Impact: <who, how many tenants/users, which feature, how long, data affected?>
Detection: <how, when, by whom: monitoring, customer, support?>  Time to detect: <x>
Timeline (UTC): 10:02 deploy 12.4.1 ... 10:17 first alert ... 10:41 rollback ... 11:05 confirmed
Contributing factors: <technical, process, organisational; several>
What went well: <keep doing>
What slowed us: <detection, access, runbooks, communication>
Actions: | action | owner | due | type (prevent / detect / mitigate) |
```

## Facilitation
- Timeline first, from evidence (logs, deploy history, chat), before any discussion of causes.
- Ask "how" and "what", not "why did you"; no names in contributing factors.
- 3-5 actions maximum, each owned and dated; prefer detection and mitigation improvements over "be more careful".
- Share the review widely; track actions to completion.

## Links to delivery metrics
Feed the time to restore and the change failure into DORA metrics; a failed deployment counts even if fixed quickly.
""")

write_plugin(PLUGIN, DESC, S, ["azure-devops", "gitlab", "ci-cd", "changelog", "pull-requests"])
