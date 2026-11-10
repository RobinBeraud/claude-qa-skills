# Getting started with claude-qa-skills

Five minutes from zero to your first skill. French version: [GUIDE_FR.md](GUIDE_FR.md).

## 1. Prerequisites

- **Claude Code** (CLI, desktop app or IDE extension), signed in.
- **git** on your machine (Claude Code clones the marketplace with it).
- **Python 3.9+** only if you want to run the bundled scripts (no `pip install` needed, standard library only).

## 2. Add the marketplace and install plugins

In a Claude Code session:

```text
/plugin marketplace add RobinBeraud/claude-qa-skills
/plugin install qa-test-strategy@claude-qa-skills
/plugin install qa-ai-era@claude-qa-skills
```

Or from a shell:

```bash
claude plugin marketplace add RobinBeraud/claude-qa-skills
claude plugin install qa-unit-testing@claude-qa-skills
```

Run `/plugin` to browse all 19 plugins, read their descriptions and install or disable them.

> No GitHub SSH key on your machine? Set `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1` before adding the marketplace.

## 3. Pick a starter pack for your role

| You are | Install | Then try |
|---|---|---|
| QA engineer / tester | `qa-shift-left`, `qa-explore-and-report`, `qa-automation` | "Review the testability of this story", "Write exploratory charters for the payment screen" |
| Developer | `qa-unit-testing`, `qa-mutation-testing`, `qa-ai-era` | "Write unit tests for `invoice.py` following our conventions", "Review this AI-generated PR against the ticket" |
| Tech lead / QA lead | `qa-test-strategy`, `qa-ci-insights`, `qa-release` | "Write our one-page test strategy", "Find the flaky tests in these JUnit reports" |
| Agile coach / manager / PO | `dora-metrics`, `evidence-based-management`, `qa-test-strategy` | "Compute our DORA metrics from this deployments export", "Help us define EBM goals and key value measures" |
| Business software team (ERP, finance, SaaS) | `qa-business-apps` | "Check this Factur-X invoice", "Generate permission tests from this roles matrix" |

## 4. Use a skill

Two ways:

1. **Just ask.** Claude reads every skill's description and loads the right one when your request matches. "Our CI is red then green on retry, which tests are flaky?" triggers `flaky-test-hunter`.
2. **Call it explicitly** with `/<plugin>:<skill>`, for example:
   ```text
   /qa-explore-and-report:bug-report  the export button crashes when the invoice has 3-decimal amounts
   /dora-metrics:dora-metrics-calculator  deployments.csv
   ```

Give Claude the material the skill needs (a story, a diff, a CSV export, a report). Skills tell Claude to ask for what is missing rather than invent it.

## 5. Try the scripts on the examples (30 seconds)

Clone the repository and run any tool on the sample data in `examples/`:

```bash
git clone https://github.com/RobinBeraud/claude-qa-skills && cd claude-qa-skills
python plugins/qa-business-apps/skills/einvoice-consistency/scripts/cii_check.py examples/invoice-wrong-vat.xml
python plugins/dora-metrics/skills/dora-metrics-calculator/scripts/dora_metrics.py --deployments examples/deployments.csv --time-col deployed_at --env-col environment --env production --failed-col caused_incident --restored-col restored_at --rework-col hotfix --commit-col first_commit_at
python plugins/evidence-based-management/skills/ebm-scorecard/scripts/ebm_scorecard.py examples/ebm.csv
python plugins/qa-ci-insights/skills/flaky-test-hunter/scripts/flaky_tests.py examples/junit-runs
python plugins/qa-business-apps/skills/permissions-matrix/scripts/rbac_matrix.py compare examples/rbac-matrix.csv examples/rbac-observed.csv
python plugins/qa-shift-left/skills/pairwise-combinations/scripts/pairwise.py examples/pairwise.json
python plugins/qa-mutation-testing/skills/mutation-report-digest/scripts/mutation_report.py examples/stryker-report.json
```

## 6. Set it up for the whole team

Run once in your project repository, then commit the `.claude/settings.json` it writes:

```bash
claude plugin marketplace add RobinBeraud/claude-qa-skills --scope project
claude plugin install qa-ai-era@claude-qa-skills --scope project
```

Every teammate who opens the project and trusts the folder gets the marketplace and the plugins. For a whole organisation, an administrator can declare the marketplace in managed settings (`extraKnownMarketplaces` and `enabledPlugins`).

## 7. Stay up to date

- `/plugin marketplace update claude-qa-skills` pulls new skills and versions.
- Or enable automatic updates: `/plugin` > **Marketplaces** > `claude-qa-skills` > **Enable auto-update**.

## 8. Without the plugin system

Copy any skill folder (`plugins/<plugin>/skills/<skill>/`) into `~/.claude/skills/` for yourself or `.claude/skills/` in a repository. It is then available as `/<skill>`.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `Permission denied (publickey)` when adding | `export CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1` (PowerShell: `$env:CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1`) |
| A skill does not trigger | Call it explicitly with `/<plugin>:<skill>`, or mention the skill name in your request |
| `python` not found when a skill runs a script | Install Python 3, or tell Claude to use `python3` |
| Strange characters in script output on Windows | Use Windows Terminal; scripts print UTF-8 |
