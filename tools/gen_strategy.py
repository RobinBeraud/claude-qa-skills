from _gen import write_plugin

PLUGIN = "qa-test-strategy"
DESC = "Design a test strategy that fits the product and the team: one-page strategy, agile testing quadrants, measured test pyramid, quality-attribute scenarios, risk storming, environments and test data strategy, shift-right testing in production, automation roadmap and QA maturity assessment."

S = {}

S["test-strategy-doc"] = ("""Write a one-page team test strategy: quality goals, test pyramid and ownership per level, what runs where in CI, environments and data, definition of done for testing, exploratory testing cadence, and how AI agents are used in testing. Use when a team starts, reorganises, adopts AI coding agents, or nobody can say who tests what.""", r"""
# Team test strategy (one page)

## Sections
1. **Context**: product, users, release cadence, main risks (link the risk storming output).
2. **Quality goals**: 3 measurable goals (e.g. "no critical escaped defect per quarter", "PR feedback in < 15 min", "change fail rate < 15 %").
3. **Levels and ownership**:
   | Level | What it proves | Owner | Runs when | Target time |
   |---|---|---|---|---|
   | Unit | Logic, calculations | Devs | Every commit | < 5 min |
   | API / integration | Contracts, persistence, permissions | Devs + QA | Every PR | < 15 min |
   | E2E | Critical journeys only | QA | Every PR (smoke) / nightly (full) | < 30 min |
   | Exploratory | Unknown risks | Whole team | Each feature, before release | time-boxed |
   | Non-functional | Performance, security, accessibility | QA + Ops | Per release / NFR | - |
4. **Environments and test data**: who owns them, how data is reset, anonymisation rules.
5. **Definition of done (testing)**: acceptance criteria automated or explicitly manual, no new flaky test, bug fixes come with a regression test.
6. **AI agents in testing**: tests written first from acceptance criteria, human review of agent-written tests, mutation score on critical modules, label on AI-assisted PRs.
7. **Feedback loop**: DORA and quality metrics reviewed monthly, escaped defects analysed.

Keep it to one page; link details elsewhere. Review it every quarter.
""")

S["testing-quadrants-map"] = ("""Map a team's current and missing testing activities onto the Agile Testing Quadrants (Brian Marick, Lisa Crispin and Janet Gregory): technology- vs business-facing, supporting the team vs critiquing the product, then spot the empty quadrants and propose actions. Use when building or reviewing a test strategy, onboarding a QA, or when testing is only UI checks or only unit tests.""", r"""
# Agile testing quadrants map

| | Supporting the team | Critiquing the product |
|---|---|---|
| **Business-facing** | **Q2**: examples, story tests, prototypes, BDD scenarios | **Q3**: exploratory testing, usability, UAT, demos, alpha/beta |
| **Technology-facing** | **Q1**: unit, component, integration tests | **Q4**: performance, load, security, accessibility, resilience ("-ility" testing) |

## Steps
1. Interview or read: list what the team actually does today, with frequency and automation level.
2. Place each activity in a quadrant; note tools and owners.
3. Find **empty or thin quadrants**. Typical gaps: Q3 done only by the PO at the end, Q4 only after an incident, Q2 replaced by UI scripts.
4. For each gap, one concrete next step and the skill to use (e.g. Q3 -> `exploratory-charter`, Q4 -> `performance-test-k6`, `accessibility-audit`).

## Output
The filled 2x2 table, the gaps, and 3-5 prioritised actions.
""")

S["test-pyramid-assessment"] = ("""Measure the real shape of a repository's test suite with a bundled stdlib script: count test files and test cases classified as unit, integration/API or end-to-end from paths, names and imports, compare it to a healthy pyramid (or trophy), and recommend where to move effort. Use when someone claims the suite is too slow, too flaky or top-heavy, or before writing a test strategy.""", r"""
# Test pyramid assessment

## Run (from the repository root)
```bash
python "${CLAUDE_SKILL_DIR}/scripts/pyramid_scan.py" . --format md
```
The script walks the repo (skipping `node_modules`, `.git`, build folders), finds test files for Python, JS/TS, Java/Kotlin, C#, Go and PHP, counts test cases, and classifies each file:
- **e2e**: Playwright, Cypress, Selenium, WebDriver, Appium imports, or `e2e/` paths
- **integration/api**: HTTP clients, test containers, databases, `integration/`, `api/` paths
- **unit**: everything else that looks like a test

## Interpret
- A healthy suite usually has most cases at unit level and few E2E; a "testing trophy" (more integration) is fine for thin-logic apps.
- **Ice-cream cone** (mostly E2E/manual): slow, flaky; push logic checks down to unit/API.
- **No integration level**: units pass but wiring breaks; add API/contract tests.
- Heuristic classification: check a sample of files before concluding.

## Output
Counts per level (files and cases), the shape diagnosis, and 3 recommendations with the skills to apply.
""")

S["quality-attribute-scenarios"] = ("""Turn quality attributes into testable scenarios with a utility tree (from the ATAM method): source, stimulus, environment, artifact, response and response measure, prioritised by business importance and technical difficulty. Use when defining a test strategy for a new product or a major change, when architects and testers disagree about what "performant" or "reliable" means.""", r"""
# Quality attribute scenarios

## Scenario template
| Part | Example |
|---|---|
| Source | 300 accountants |
| Stimulus | run the month-end closing report simultaneously |
| Environment | normal production load, last working day of the month |
| Artifact | reporting service |
| Response | reports generated and downloadable |
| Response measure | p95 < 60 s, no error, other screens p95 < 2 s meanwhile |

## Steps
1. Brainstorm attributes (performance, availability, security, modifiability, usability, interoperability, compliance).
2. Write 2-4 scenarios per important attribute with the template.
3. Build the **utility tree**: attribute -> refinement -> scenario, rated (business importance H/M/L, difficulty H/M/L).
4. (H,H) scenarios drive the test strategy first: each gets a test approach, environment and owner.

## Output
Utility tree, scenario table, and the test approach for the top scenarios.
""")

S["risk-storming-workshop"] = ("""Facilitate a risk storming workshop (inspired by TestSphere and the risk storming format by Beren Van Daele) for a feature or release: quality aspects first, then risks per aspect, then test ideas per risk, with dot-voting and a prioritised outcome. Use at the start of an epic, before a release, or to involve the whole team in test strategy.""", r"""
# Risk storming workshop (45-60 min)

## Agenda
1. **Context (5 min)**: what we build, for whom, what changes.
2. **Quality aspects (10 min)**: each person picks the 6 aspects that matter most (e.g. correctness of calculations, security, performance, usability, compatibility, data integrity, compliance, recoverability). Converge on 6.
3. **Risks (15 min)**: silent writing, one risk per sticky, placed under its aspect. Phrase: "*X* may fail when *Y*, causing *Z*".
4. **Vote (5 min)**: 3 dots per person on the most worrying risks.
5. **Test ideas (15 min)**: for the top risks, what would reveal the problem early? (test types, data, tools, monitoring, a spike).
6. **Wrap-up (5 min)**: owners and next steps.

## Facilitator's prompts
"What would embarrass us in front of a customer?" "What happened last time in this area?" "What do we assume the third party does?" "What if the data is 100x bigger?"

## Output
A prepared Miro/whiteboard structure, the facilitator script, and after the session: risks table sorted by votes with test ideas and owners, ready for `risk-based-test-plan`.
""")

S["test-environment-strategy"] = ("""Design the test environment strategy: which environments exist (ephemeral per PR, integration, staging, pre-production), what each is for, how they are created and torn down, configuration parity with production, third-party stubs or sandboxes, ownership, booking and data refresh. Use when environments are a bottleneck, shared and broken, or when moving to ephemeral environments.""", r"""
# Test environment strategy

## Steps
1. **Inventory** current environments: purpose, owner, how built, data, uptime problems, who waits for them.
2. **Target design** per need:
   | Need | Environment | Lifetime |
   |---|---|---|
   | PR checks, API/E2E smoke | Ephemeral (containers / preview env) | Per PR |
   | Cross-team integration | Shared integration | Permanent, reset nightly |
   | Release validation, performance | Staging, prod-like sizing | Permanent |
   | Customer acceptance | Pre-production with anonymized data | Per release |
3. **Parity**: same build artifacts, infrastructure as code, config differences listed explicitly.
4. **Third parties**: sandbox, contract stub (WireMock, Prism) or recorded responses, per dependency.
5. **Data**: how each environment gets data (`test-data-strategy`), refresh frequency.
6. **Operations**: who fixes it, health checks, booking rules, cost limits for ephemeral envs.

## Output
Environment map table, gaps vs today, and a migration plan in 3 steps.
""")

S["test-data-strategy"] = ("""Define how tests get their data: synthetic generation, anonymised production extracts, fixtures per test, seeded reference data, data reset between runs, GDPR constraints on personal data, and ownership. Use when tests fail because of data, when someone wants to copy production into test, or when building a new test environment.""", r"""
# Test data strategy

## Principles
- **Each automated test creates the data it needs** (via API or fixtures) and does not depend on data left by others.
- **Reference data** (countries, VAT rates, charts of accounts) is seeded and versioned with the code.
- **Production data** never lands in test environments raw: anonymise (irreversibly), minimise, and document the legal basis (GDPR). Prefer synthetic data.
- **Volume data** for performance tests is generated, with realistic distributions.

## Steps
1. List data needs per test level and environment.
2. Choose the source per need: synthetic (`test-data-fr`), fixtures, anonymised extract, generated volume.
3. Define reset: transaction rollback, per-test tenant, database snapshot restore, nightly refresh.
4. Assign owners and write the anonymisation rules (which fields, which technique: masking, shuffling, fake values, keeping formats and checksums valid).
5. Check: no real names, e-mails, IBANs or national ids in test environments (scan regularly).

## Output
Data matrix (need -> source -> reset -> owner), anonymisation rules, and the compliance checklist.
""")

S["shift-right-testing"] = ("""Plan shift-right testing and verification in production: feature flags and progressive delivery (canary, percentage rollout), synthetic monitoring of key journeys, observability signals as test oracles, error budgets, A/B checks and fast rollback, without testing on real customers' data carelessly. Use when pre-production testing cannot reproduce production, for risky releases, or to complement CI tests.""", r"""
# Shift-right testing

## Building blocks
| Practice | What it gives | Guardrail |
|---|---|---|
| Feature flags | Deploy dark, enable per tenant/user | Flag removal plan, default off |
| Canary / progressive rollout | Compare new vs old version on a slice of traffic | Automatic rollback on SLO breach |
| Synthetic monitoring | Scripted journeys every few minutes in production | Dedicated test tenant, no real side effects |
| Observability as oracle | Error rate, latency, business counters per release | Dashboards per release, alerts on deviation |
| Error budgets (SLO) | Decide release speed with data | Agreed with product |
| Dogfooding / beta tenants | Real usage before general availability | Opt-in, fast feedback channel |

## Steps
1. Pick the release's riskiest change; choose the rollout pattern.
2. Define the signals and thresholds that mean "roll back" (from SLOs and business counters).
3. Write the synthetic checks for the critical journeys.
4. Rehearse the rollback.
5. Afterwards, compare signals before/after and feed findings into the test strategy.

## Output
Rollout plan, signal table with thresholds, synthetic checks list, and rollback procedure.
""")

S["test-automation-roadmap"] = ("""Decide what to automate next and in which order: score candidate test cases or journeys by frequency of execution, business risk, stability of the feature, cost to automate and flakiness risk, choose the right level (unit, API, UI), and produce a 3-month automation roadmap. Use when a team has a big manual regression, wants to start automating, or automates the wrong things.""", r"""
# Test automation roadmap

## Scoring each candidate (1-5)
| Criterion | Question |
|---|---|
| Frequency | How often is it run (each release, each PR)? |
| Risk | What does a regression here cost? |
| Stability | Is the feature stable or still changing every sprint? |
| Cost | Effort to automate at the right level, test data included |
| Flakiness risk | Async UI, third parties, timing |
Priority = (Frequency + Risk + Stability) - (Cost + Flakiness risk).

## Steps
1. List candidates (manual regression cases, smoke checks, bug-prone areas).
2. For each, pick the **lowest level** that proves it (most UI checks are really API or unit checks).
3. Score, sort, group into monthly increments with a definition of done (runs in CI, owner, no flake over 20 runs).
4. Track: manual regression time saved, automated checks added, flaky count.

## Output
Scored candidate table, the 3-month roadmap, and the metrics to follow.
""")

S["qa-maturity-assessment"] = ("""Run a lightweight QA and test maturity self-assessment for a team across 8 dimensions (strategy, shift-left, automation, CI feedback, exploratory testing, non-functional testing, defect management, metrics and learning), score 1-5 with evidence, and derive a 90-day improvement roadmap. Use for a team health check, a coaching engagement, or before investing in QA tooling.""", r"""
# QA maturity assessment

## Dimensions and evidence to look for
| Dimension | Level 1 | Level 5 |
|---|---|---|
| Strategy | No written strategy | One-page strategy reviewed quarterly, risk-driven |
| Shift-left | Testing starts after dev | Examples and acceptance tests before code, three amigos routine |
| Automation | Manual regression only | Pyramid-shaped suite, tests written with or before code |
| CI feedback | Nightly at best, often red | PR feedback < 15 min, green main, flaky tests quarantined |
| Exploratory | None or random | Chartered sessions per feature, debriefs |
| Non-functional | After incidents | Performance, security, accessibility in the pipeline per risk |
| Defects | Backlog of hundreds, no triage | Weekly triage, escaped defects analysed, trends known |
| Metrics & learning | None, or vanity metrics | DORA + quality metrics reviewed monthly, experiments run |

## Steps
1. Ask for evidence per dimension (artifacts, pipeline screenshots, metrics), not opinions.
2. Score 1-5 with one line of evidence each.
3. Pick the 2-3 dimensions with the best value/effort for the next 90 days.
4. Define actions, owners and how success will be measured.

## Output
Radar-ready score table, evidence notes, and the 90-day roadmap.
""")

write_plugin(PLUGIN, DESC, S, ["test-strategy", "test-pyramid", "risk", "shift-right", "maturity"])
