from _gen import write_plugin

PLUGIN = "qa-explore-and-report"
DESC = "Explore like a seasoned tester and report like a pro: exploratory charters with SFDIPOT and tours, session debriefs, oracle heuristics when there is no spec, bug reports developers can act on, batch triage and repro minimisation."

S = {}

S["exploratory-charter"] = ("""Create focused exploratory testing charters ("Explore <target> with <resources> to discover <information>") using the SFDIPOT product elements and Whittaker's testing tours, with time-boxes and a session sheet. Use when planning exploratory testing of a feature, a release or a risky area, or when scripted tests feel blind.""", r"""
# Exploratory testing charters

## Charter format (Elisabeth Hendrickson)
> **Explore** *target* **with** *resources / techniques* **to discover** *information*.

## Steps
1. Model the target with **SFDIPOT**: Structure (components, files), Function (what it does), Data (inputs, outputs, states), Interfaces (UI, API, imports/exports), Platform (browsers, OS, infra), Operations (how real users use it, at month-end, at scale), Time (dates, time zones, concurrency, timeouts).
2. For each risky element, write a charter. Pick a **tour** when useful:
   - *Money tour*: the features sales demos. *Landmark*: jump between key features in odd orders.
   - *Bad-data / saboteur*: hostile input, interrupted operations. *Back alley*: least-used features.
   - *Supermodel*: look only at the UI. *Couch potato*: do the minimum, accept every default.
   - *Obsessive-compulsive*: repeat actions, double submit. *Garbage collector*: visit every screen once.
3. Time-box each session (45-90 min), name a tester, list the test data needed.
4. Order charters by risk.

## Output
| # | Charter | Tour / technique | Time-box | Data needed | Risk |
plus a blank session sheet:
```
CHARTER:  TESTER:  START:  DURATION:
SETUP %  TEST %  BUG INVESTIGATION %
NOTES:
BUGS:
ISSUES / QUESTIONS:
```
""")

S["session-debrief"] = ("""Turn raw exploratory session notes (bullet notes, screenshots descriptions, chat logs) into a session-based test management debrief: coverage, bugs, issues, questions, time split and next charters. Use right after an exploratory session or bug bash, or to summarise several sessions for a test report.""", r"""
# Session debrief (SBTM)

## Steps
1. Read the notes. Separate **bugs** (product misbehaves), **issues** (things that slowed testing: missing data, environment down, unclear requirement) and **questions**.
2. Rebuild **what was covered** (areas, data, platforms) and what was **not** covered.
3. Estimate the time split: setup / testing / bug investigation. High setup time is itself a finding.
4. Rate the confidence for the area: low / medium / high, with one sentence why.
5. Propose the next 1-3 charters.
6. For each bug, draft a one-line summary; full reports go through `bug-report`.

## Output
```
CHARTER:      TESTER:     DURATION:
COVERAGE:     ...
NOT COVERED:  ...
BUGS:         B1 ... (severity)
ISSUES:       I1 ...
QUESTIONS:    Q1 ...
TIME SPLIT:   setup x % / test y % / investigation z %
CONFIDENCE:   medium, because ...
NEXT:         charter ...
```
""")

S["oracle-heuristics"] = ("""Decide whether an observed behaviour is a bug when there is no spec, using Michael Bolton's FEW HICCUPPS consistency oracles (familiar problems, explainability, world, history, image, comparable products, claims, user expectations, product, purpose, statutes), and write the argument a product owner can rule on. Use when someone says it is not a bug, it's a feature, or when requirements are silent.""", r"""
# Oracle heuristics (FEW HICCUPPS)

A bug is something that bugs someone who matters. Without a spec, argue from consistency.

## Check the behaviour against each oracle
| Oracle | Ask |
|---|---|
| **F**amiliar problems | Does it look like a known class of bug (off-by-one, rounding, encoding, race)? |
| **E**xplainability | Can we explain the behaviour to a customer without embarrassment? |
| **W**orld | Is it consistent with how the real world works (calendars, laws of arithmetic, physical units)? |
| **H**istory | Is it consistent with earlier versions? |
| **I**mage | Is it consistent with the image the company wants to project? |
| **C**omparable products | What do similar products (competitors, other Cegid products) do? |
| **C**laims | What do the docs, marketing, contracts, help pages say? |
| **U**ser expectations | What would a reasonable user expect? |
| **P**roduct | Is it consistent with similar features elsewhere in the same product? |
| **P**urpose | Does it serve the purpose the feature exists for? |
| **S**tatutes & standards | Laws, regulations, accessibility norms, accounting rules, ISO formats? |

## Output
The observed behaviour, then the oracles that it **violates** (with evidence) and those it **satisfies**, then a recommendation: bug (severity), feature request, or works as designed, and the question to put to the product owner.
""")

S["bug-report"] = ("""Write a clear, reproducible bug report from rough notes, logs, screenshots descriptions or a conversation: title that states the failure, minimal steps, expected vs actual, environment, evidence, impact, and separate severity and priority suggestions; formatted for Azure DevOps or Jira. Use whenever a defect must be logged or an existing report is too vague to act on.""", r"""
# Bug report

Cem Kaner's **RIMGEA**: Replicate, Isolate, Maximize (show the worst consequence), Generalize (find the broader case), Externalize (impact on users), And say it dispassionately.

## Steps
1. **Title**: `<where> - <what fails> when <condition>`. e.g. "Invoice export - VAT total off by 0.01 EUR when lines have 3 decimals".
2. **Steps**: numbered, minimal, starting from a known state, with exact data.
3. **Expected** vs **Actual**, each one sentence, with values.
4. **Environment**: version/build, environment, browser/OS, tenant, user role, feature flags.
5. **Evidence**: log excerpt (trimmed, no secrets), screenshot names, request id / correlation id, timestamp with time zone.
6. **Scope**: what else is affected (generalize), what is *not* affected (isolate).
7. **Impact**: who is hurt, how often, workaround.
8. **Severity** (technical impact) and **priority** (business urgency) as *suggestions*, kept separate.

## Output
Markdown ready to paste, with an Azure DevOps field mapping when relevant (Repro Steps, System Info, Severity, Priority, Area Path, Tags).

## Never
Blame people, include personal data or credentials, or mix two bugs in one report.
""")

S["bug-triage"] = ("""Triage a batch of incoming bugs or a bug backlog export: detect likely duplicates, missing information, misfiled components, severity inconsistencies and stale items, then propose a ranked action list. Use for weekly bug triage meetings, after a bug bash, or when a backlog has grown out of control.""", r"""
# Bug triage

## Input
A list or export (CSV/JSON) with at least id, title, description, state, created date; ideally severity, priority, area, assignee, last update.

## Steps
1. **Normalise** titles (lowercase, strip ids and versions) and group near-duplicates by shared key terms and same area; list them as *candidate* duplicates with the reason.
2. **Completeness**: flag reports missing steps, expected/actual, environment or evidence; draft the question to ask the reporter.
3. **Severity sanity**: data loss, security, money or legal impact must not be "low"; cosmetic issues must not be "critical".
4. **Staleness**: open > 180 days with no activity -> propose close or re-validate.
5. **Clusters**: areas with many bugs this period -> hint for root-cause analysis.
6. **Rank** what to fix first: severity x frequency x customer impact.

## Output
1. Proposed decisions table: `id | proposal (fix now / schedule / need info / duplicate of X / close) | reason`.
2. Duplicate groups.
3. Hot spots by area with counts.
Decisions are proposals: the triage meeting decides.
""")

S["repro-minimizer"] = ("""Shrink a failing scenario to the smallest reproduction: fewer steps, smaller data, fewer settings, by delta-debugging style halving, and identify the trigger condition. Use when a bug only appears in long sessions, big imports, specific customer data or complex configurations, before handing it to a developer.""", r"""
# Repro minimizer

## Steps
1. Confirm the full reproduction works reliably (at least 3/3). If not, record the rate and look for timing or data dependencies first.
2. **Halve the input**: remove half of the steps, rows, files or settings; keep the half that still fails. Repeat (delta debugging).
3. **Vary one thing at a time** at the end: each remaining value -> neutral value. Note which change makes the bug disappear: that is the trigger.
4. **Generalize**: does it fail with other values of the same kind (other customer, other month, other browser)?
5. Write the minimal steps and the trigger in one sentence.

## Output
```
Original: 37 steps, 12,000-row import, tenant X
Minimal:  3 steps, 2-row import
Trigger:  a line amount with 3 decimals followed by a credit note line
Still fails on: other tenants, Chrome and Firefox
```
plus the minimal data file content.
""")

write_plugin(PLUGIN, DESC, S, ["exploratory-testing", "bug-report", "triage", "heuristics"])
