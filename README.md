<p align="center"><img src="assets/banner.svg" alt="claude-qa-skills: QA skills for Claude Code" width="100%"></p>

<p align="center">
  <img src="https://img.shields.io/badge/skills-49-2962FF?style=flat-square" alt="Skills count">
  <img src="https://img.shields.io/badge/plugins-7-7B61FF?style=flat-square" alt="Plugins">
  <img src="https://img.shields.io/badge/Claude%20Code-plugin%20marketplace-FF7A00?style=flat-square" alt="Claude Code marketplace">
  <img src="https://img.shields.io/badge/scripts-stdlib%20Python-16B3A6?style=flat-square" alt="Stdlib Python">
  <img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="License">
</p>

**claude-qa-skills** is a library of quality-engineering skills for [Claude Code](https://code.claude.com): from a fuzzy user story to a go/no-go decision, for testers, developers and teams who now ship code written with AI agents.

It is built around one observation from the field: **coding agents make writing code cheap; verification becomes the bottleneck.** These skills make verification faster and harder to fake.

## Install

In Claude Code:

```text
/plugin marketplace add RobinBeraud/claude-qa-skills
/plugin install qa-shift-left@claude-qa-skills
```

Install only the plugins you need (see the catalogue below), or all of them. From a shell: `claude plugin marketplace add RobinBeraud/claude-qa-skills` then `claude plugin install <plugin>@claude-qa-skills`.

Skills load automatically when your request matches their description ("review the testability of this story", "find our flaky tests"), or explicitly as `/<plugin>:<skill>`, e.g. `/qa-explore-and-report:bug-report`.

> Private repository: everyone who installs needs read access on GitHub and a working `git` login (`gh auth login`).

**Without plugins**: copy any `plugins/<plugin>/skills/<skill>/` folder into `~/.claude/skills/` (personal) or `.claude/skills/` (project).

## What makes it different

- **Real testing craft**: SFDIPOT and testing tours for exploration, FEW HICCUPPS oracles when there is no spec, RIMGEA bug advocacy, example mapping, decision tables, pairwise, property-based and mutation testing.
- **Built for the agent era**: review AI-generated PRs, write tests before the agent implements, demand evidence before "done", audit AI-written tests, evaluate and red-team LLM features.
- **Business software, not demo apps**: accounting invariants, EN 16931 / Factur-X e-invoice checks, money and rounding, dates and DST, multi-tenant isolation, RBAC matrices, data migrations, FR/ES/PT localisation.
- **Scripts you can trust**: 10 bundled tools, Python standard library only (no `pip install`), each covered by unit tests in CI.

## Catalogue

🐍 = ships a tested script.

<!-- CATALOG:START -->
### 🧭 Shift-left: test before the code exists

Plugin **`qa-shift-left`** (9 skills): `/plugin install qa-shift-left@claude-qa-skills`

| Skill | What it does | Script |
|---|---|---|
| [example-mapping](plugins/qa-shift-left/skills/example-mapping/SKILL.md) | Prepare or run an Example Mapping (Three Amigos) session for a story: rules, concrete examples per rule, and open questions, then turn the result into scenarios. |  |
| [gherkin-scenarios](plugins/qa-shift-left/skills/gherkin-scenarios/SKILL.md) | Write clean, business-readable Gherkin (Given/When/Then) scenarios and scenario outlines from acceptance criteria or examples, then lint them with a bundled script (one When per... | 🐍 |
| [nfr-checklist](plugins/qa-shift-left/skills/nfr-checklist/SKILL.md) | Turn vague non-functional expectations into measurable, testable quality requirements using ISO/IEC 25010 characteristics: performance, reliability, security, usability, accessibility,... |  |
| [pairwise-combinations](plugins/qa-shift-left/skills/pairwise-combinations/SKILL.md) | Generate a small all-pairs (pairwise) test set covering every pair of parameter values, with a bundled stdlib Python script, plus constraints to exclude impossible combinations. | 🐍 |
| [risk-based-test-plan](plugins/qa-shift-left/skills/risk-based-test-plan/SKILL.md) | Build a lean, risk-based test plan for a feature, epic or release: scope, risk matrix (impact x likelihood), test approach per risk, test types, data, environments, entry and exit criteria. |  |
| [story-testability-review](plugins/qa-shift-left/skills/story-testability-review/SKILL.md) | Review a user story, PBI or ticket for testability before development starts: ambiguous words, missing acceptance criteria, untestable rules, hidden edge cases, and a rewrite in... |  |
| [test-case-export](plugins/qa-shift-left/skills/test-case-export/SKILL.md) | Convert test cases written in Markdown or JSON into import-ready CSV for Azure DevOps Test Plans or Jira Xray (steps with action and expected result), with a bundled stdlib script. | 🐍 |
| [test-data-fr](plugins/qa-shift-left/skills/test-data-fr/SKILL.md) | Generate realistic but fake French business test data that passes real validation: SIREN/SIRET (Luhn), intra-EU VAT numbers, IBAN FR with RIB key, invoices with VAT rates 20/10/5.5/2.1... | 🐍 |
| [test-design-techniques](plugins/qa-shift-left/skills/test-design-techniques/SKILL.md) | Derive test cases systematically with equivalence partitioning, boundary value analysis, decision tables, state transitions and cause-effect reasoning, then output a compact,... |  |

### 🤖 Automation that stays green for the right reasons

Plugin **`qa-automation`** (10 skills): `/plugin install qa-automation@claude-qa-skills`

| Skill | What it does | Script |
|---|---|---|
| [accessibility-audit](plugins/qa-automation/skills/accessibility-audit/SKILL.md) | Audit a web page or flow for accessibility against WCAG 2.2 AA and the French RGAA 4.1: automated axe-core scan through Playwright, plus the manual checks automation cannot do (keyboard,... |  |
| [api-test-suite](plugins/qa-automation/skills/api-test-suite/SKILL.md) | Generate an API test suite from an OpenAPI/Swagger spec or from example requests: happy paths, status codes, schema validation, authentication and authorization, validation errors,... |  |
| [characterization-tests](plugins/qa-automation/skills/characterization-tests/SKILL.md) | Pin down the current behaviour of legacy or untested code with characterization (golden master / approval) tests before refactoring or letting an agent change it: capture outputs for a... |  |
| [contract-testing](plugins/qa-automation/skills/contract-testing/SKILL.md) | Set up consumer-driven contract tests (Pact or schema-based) between a front end or service and the APIs it consumes, so breaking changes are caught in CI before deployment. |  |
| [mutation-testing](plugins/qa-automation/skills/mutation-testing/SKILL.md) | Measure how good a test suite really is with mutation testing (Stryker for JS/TS/.NET, PIT for Java, mutmut or cosmic-ray for Python): run it on the risky module, read surviving mutants... |  |
| [performance-test-k6](plugins/qa-automation/skills/performance-test-k6/SKILL.md) | Design and script load, stress and soak tests with k6 (or Locust/Gatling if the team uses them): realistic scenarios, think time, thresholds on p95/p99 and error rate, and a readable... |  |
| [playwright-e2e](plugins/qa-automation/skills/playwright-e2e/SKILL.md) | Write or fix Playwright end-to-end tests (TypeScript or Python) with user-facing locators, web-first assertions, isolated test data and no fixed sleeps, then run them and iterate until... |  |
| [property-based-tests](plugins/qa-automation/skills/property-based-tests/SKILL.md) | Write property-based tests (Hypothesis for Python, fast-check for JS/TS, jqwik or FsCheck for JVM/.NET) that state invariants and let the framework search for counter-examples. |  |
| [test-smell-review](plugins/qa-automation/skills/test-smell-review/SKILL.md) | Review an existing test suite or a test file for smells that make tests useless or flaky: no or weak assertions, sleeps, order dependence, shared mutable state, logic in tests,... |  |
| [visual-regression](plugins/qa-automation/skills/visual-regression/SKILL.md) | Add visual regression tests (Playwright toHaveScreenshot, or Percy/Chromatic/BackstopJS) on stable components and key screens, with masked dynamic areas, fixed viewports and a review... |  |

### 🔎 Explore and report

Plugin **`qa-explore-and-report`** (6 skills): `/plugin install qa-explore-and-report@claude-qa-skills`

| Skill | What it does | Script |
|---|---|---|
| [bug-report](plugins/qa-explore-and-report/skills/bug-report/SKILL.md) | Write a clear, reproducible bug report from rough notes, logs, screenshots descriptions or a conversation: title that states the failure, minimal steps, expected vs actual, environment,... |  |
| [bug-triage](plugins/qa-explore-and-report/skills/bug-triage/SKILL.md) | Triage a batch of incoming bugs or a bug backlog export: detect likely duplicates, missing information, misfiled components, severity inconsistencies and stale items, then propose a... |  |
| [exploratory-charter](plugins/qa-explore-and-report/skills/exploratory-charter/SKILL.md) | Create focused exploratory testing charters ("Explore <target> with <resources> to discover <information>") using the SFDIPOT product elements and Whittaker's testing tours, with... |  |
| [oracle-heuristics](plugins/qa-explore-and-report/skills/oracle-heuristics/SKILL.md) | Decide whether an observed behaviour is a bug when there is no spec, using Michael Bolton's FEW HICCUPPS consistency oracles (familiar problems, explainability, world, history, image,... |  |
| [repro-minimizer](plugins/qa-explore-and-report/skills/repro-minimizer/SKILL.md) | Shrink a failing scenario to the smallest reproduction: fewer steps, smaller data, fewer settings, by delta-debugging style halving, and identify the trigger condition. |  |
| [session-debrief](plugins/qa-explore-and-report/skills/session-debrief/SKILL.md) | Turn raw exploratory session notes (bullet notes, screenshots descriptions, chat logs) into a session-based test management debrief: coverage, bugs, issues, questions, time split and... |  |

### 📈 CI insights

Plugin **`qa-ci-insights`** (5 skills): `/plugin install qa-ci-insights@claude-qa-skills`

| Skill | What it does | Script |
|---|---|---|
| [ci-failure-triage](plugins/qa-ci-insights/skills/ci-failure-triage/SKILL.md) | Triage a failed CI pipeline from its logs: classify each failure as product bug, test bug, flaky test, environment/infrastructure or dependency issue, find the first real error in long... |  |
| [coverage-gap-analysis](plugins/qa-ci-insights/skills/coverage-gap-analysis/SKILL.md) | Read a code coverage report (Cobertura, JaCoCo, lcov, coverage.py) together with risk signals (business-critical modules, recent bugs, churn) and recommend where new tests pay off most,... |  |
| [flaky-test-hunter](plugins/qa-ci-insights/skills/flaky-test-hunter/SKILL.md) | Find flaky tests by comparing JUnit XML reports from several CI runs of the same code: pass/fail flips, flip rate, failure messages, and a quarantine shortlist, using a bundled stdlib... | 🐍 |
| [junit-digest](plugins/qa-ci-insights/skills/junit-digest/SKILL.md) | Summarise one or many JUnit/xUnit XML test reports into a short digest: totals, failures grouped by error message, slowest tests and suites, skipped tests, using a bundled stdlib script. | 🐍 |
| [regression-scope](plugins/qa-ci-insights/skills/regression-scope/SKILL.md) | Select the regression tests a change most likely needs, from the files changed in a branch or PR: name-matching test files plus tests that historically change together with those files... | 🐍 |

### 🚀 Release with evidence

Plugin **`qa-release`** (5 skills): `/plugin install qa-release@claude-qa-skills`

| Skill | What it does | Script |
|---|---|---|
| [escaped-defect-rca](plugins/qa-release/skills/escaped-defect-rca/SKILL.md) | Run a blameless root-cause analysis of a defect that reached production: timeline, how it was introduced, why each test layer and review missed it, contributing factors, and concrete... |  |
| [post-deploy-smoke](plugins/qa-release/skills/post-deploy-smoke/SKILL.md) | Design a short post-deployment smoke and verification plan: the 10-20 checks that prove a deployment is healthy in minutes (critical journeys, integrations, background jobs, monitoring... |  |
| [qa-flow-metrics](plugins/qa-release/skills/qa-flow-metrics/SKILL.md) | Compute quality flow metrics from a work-item export (Azure DevOps or Jira CSV): bugs created vs closed per month, open bug backlog, median time to fix, escape rate to production, reopen... | 🐍 |
| [release-readiness](plugins/qa-release/skills/release-readiness/SKILL.md) | Produce a go/no-go release readiness report from test results, open bugs, story status and known risks: what was tested, what was not, open defects by severity, risks with mitigation,... |  |
| [test-strategy-doc](plugins/qa-release/skills/test-strategy-doc/SKILL.md) | Write a one-page team test strategy: quality goals, test pyramid and ownership per level, what runs where in CI, environments and data, definition of done for testing, exploratory... |  |

### 🧠 Quality in the age of coding agents

Plugin **`qa-ai-era`** (6 skills): `/plugin install qa-ai-era@claude-qa-skills`

| Skill | What it does | Script |
|---|---|---|
| [ai-pr-review](plugins/qa-ai-era/skills/ai-pr-review/SKILL.md) | Review a pull request written with a coding agent (Claude Code, Copilot, Cursor) against its brief: scope creep, acceptance criteria actually covered by tests, weak or mirrored tests,... |  |
| [ai-tests-audit](plugins/qa-ai-era/skills/ai-tests-audit/SKILL.md) | Audit a test suite or a batch of tests written by an AI agent: do they fail when the code is wrong? Combine a test-smell scan, a deliberate fault-injection (mini mutation) pass on the... |  |
| [done-evidence-check](plugins/qa-ai-era/skills/done-evidence-check/SKILL.md) | Refuse "it should work": before a task, PR or story is called done, collect the evidence: build and test commands actually run with their output, each acceptance criterion mapped to... |  |
| [llm-feature-eval](plugins/qa-ai-era/skills/llm-feature-eval/SKILL.md) | Design and run an evaluation suite for a product feature built on an LLM (summary, classification, extraction, chat assistant): golden dataset, rubric and graders (exact match, schema,... |  |
| [prompt-injection-redteam](plugins/qa-ai-era/skills/prompt-injection-redteam/SKILL.md) | Red-team an LLM feature or agent against prompt injection and data exfiltration: direct and indirect injection (documents, e-mails, web pages, tool outputs), instruction override, system... |  |
| [tests-first-for-agents](plugins/qa-ai-era/skills/tests-first-for-agents/SKILL.md) | Before letting a coding agent implement a story, turn its acceptance criteria into failing tests (unit or API level), get them reviewed by a human, then hand the agent the brief plus the... |  |

### 🏦 Business software: ERP, accounting, e-invoicing, SaaS

Plugin **`qa-business-apps`** (8 skills): `/plugin install qa-business-apps@claude-qa-skills`

| Skill | What it does | Script |
|---|---|---|
| [accounting-invariants](plugins/qa-business-apps/skills/accounting-invariants/SKILL.md) | Derive and test the invariants accounting and finance software must never break: balanced double entries, trial balance, sequential numbering without gaps, closed periods immutable, VAT... |  |
| [data-migration-validation](plugins/qa-business-apps/skills/data-migration-validation/SKILL.md) | Validate a data migration or upgrade (legacy to new system, version upgrade, tenant onboarding): reconciliation of counts, totals and checksums per entity, sampling with field-level... |  |
| [date-time-edge-cases](plugins/qa-business-apps/skills/date-time-edge-cases/SKILL.md) | Generate the date and time test cases that break business software: time zones and DST changes, end of month and leap years, fiscal years not aligned with calendar years, cut-off times,... |  |
| [einvoice-consistency](plugins/qa-business-apps/skills/einvoice-consistency/SKILL.md) | Check an electronic invoice in UN/CEFACT CII XML or a Factur-X PDF for EN 16931 arithmetic and mandatory-field consistency (line totals, VAT breakdown, tax basis, grand total, amount... | 🐍 |
| [localization-testing](plugins/qa-business-apps/skills/localization-testing/SKILL.md) | Test localisation and internationalisation for French, Spanish and Portuguese markets (and others): translations complete and in context, number, currency, date and address formats,... |  |
| [money-and-rounding](plugins/qa-business-apps/skills/money-and-rounding/SKILL.md) | Design tests for monetary calculations: decimal precision, rounding modes (half-up, half-even, truncation), per-line vs per-document VAT rounding, allocation of remainders (splitting... |  |
| [multi-tenant-isolation](plugins/qa-business-apps/skills/multi-tenant-isolation/SKILL.md) | Test that a multi-tenant SaaS never leaks or mixes data between tenants (customers, companies, subsidiaries): ID guessing on APIs, list filters, search indexes, exports, caches,... |  |
| [permissions-matrix](plugins/qa-business-apps/skills/permissions-matrix/SKILL.md) | Turn a roles x actions permission matrix (CSV) into positive and negative test cases, and compare expected permissions with observed results from a test run to list every mismatch, with... | 🐍 |

<!-- CATALOG:END -->

## Bundled scripts

| Script | What it does |
|---|---|
| `fr_test_data.py` | Fake but valid SIREN, SIRET, FR VAT numbers, IBANs; invoices with correct VAT rounding; identifier validation |
| `pairwise.py` | Greedy all-pairs generator with exclusion constraints, verifies full pair coverage |
| `gherkin_lint.py` | Lints `.feature` files: one When, no UI steps, no vague outcomes, outlines with Examples |
| `export_test_cases.py` | Markdown/JSON test cases to Azure DevOps Test Plans or Xray CSV |
| `flaky_tests.py` | Flaky tests across JUnit runs: flips, flip rate, top failure message |
| `junit_digest.py` | JUnit totals, failures grouped by normalised message, slowest tests |
| `co_change.py` | Tests most related to a change, from name matching and git co-change history |
| `qa_metrics.py` | Bug flow, time to fix, escape rate, backlog by severity and age from ADO/Jira CSV |
| `cii_check.py` | EN 16931 arithmetic and key fields of CII XML or Factur-X PDF |
| `rbac_matrix.py` | Permission test cases from a roles x actions matrix; expected vs observed diff |

## Repository layout

```
.claude-plugin/marketplace.json      the marketplace (7 plugins)
plugins/<plugin>/.claude-plugin/     plugin manifest
plugins/<plugin>/skills/<skill>/     SKILL.md (+ scripts/)
tests/                               unit tests of every script (stdlib unittest)
tools/validate_skills.py             structure and front-matter checks (also run in CI)
tools/build_readme.py                rebuilds the catalogue above
tools/gen_*.py                       optional generators used to bootstrap the skills
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). In short: one skill = one folder, a description that says **what** and **when to use**, concrete steps and an output format, scripts in stdlib Python with a test, then `python tools/validate_skills.py`, `python -m unittest discover -s tests` and `claude plugin validate .`.

## Author

Made by [Robin Béraud-Sudreau](https://coach-agile.com), agile and DevOps coach, Head of AI Transformation, author of *Build Your Own AI Workforce*. Sister project: [hermes-skills](https://github.com/RobinBeraud/hermes-skills) for Hermes Agent.

MIT licence.
