---
name: azure-pipelines
description: "Write and fix Azure DevOps YAML pipelines: stages, jobs and templates for reuse, caching NuGet and npm, test results and coverage publishing, environments with approvals and checks, variable groups linked to Key Vault, path filters and PR validation, and diagnosing failed runs from logs. Use when creating or editing azure-pipelines.yml, converting classic build or release pipelines to YAML, speeding up a slow pipeline, or debugging a failing pipeline."
---

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
