from _gen import write_plugin

PLUGIN = "qa-shift-left"
DESC = "Test before the code exists: testable stories, example mapping, risk-based test plans, test design techniques, pairwise combinations, Gherkin, French business test data and test-case export to Azure Test Plans or Xray."

S = {}

S["story-testability-review"] = ("""Review a user story, PBI or ticket for testability before development starts: ambiguous words, missing acceptance criteria, untestable rules, hidden edge cases, and a rewrite in Given/When/Then. Use when a story is about to enter a sprint, during refinement, or when asked whether a ticket is ready to test.""", r"""
# Story testability review

Catch defects in the requirement, where they cost the least. The output is a verdict plus a better story, not a lecture.

## Inputs
- The story text (title, description, acceptance criteria). Ask for it if missing.
- Optional: linked mockups, business rules, the product glossary.

## Steps
1. **Restate** the story in one sentence: who, what, why. If you cannot, the story is not ready.
2. **Hunt ambiguity**: flag every vague word (`fast`, `user-friendly`, `etc.`, `appropriate`, `all`, `some`, `should`, `if needed`) and every undefined term.
3. **Check each acceptance criterion** against: observable, binary (pass/fail), independent of implementation, one behaviour per criterion.
4. **Find the missing cases** with this list: empty / null input, maximum length, duplicates, permissions (who may not do it), concurrency (two users at once), errors from dependencies, undo / cancel, existing data created before the change, localisation (dates, decimals, currency).
5. **Rewrite** the criteria as Given / When / Then, one scenario per rule, with concrete values.
6. **List open questions** for the product owner, each answerable with yes/no or a value.

## Output
```
Verdict: READY | READY WITH QUESTIONS | NOT READY
Ambiguities: <word> -> <why it is untestable> -> <proposed precise wording>
Missing cases: <case> (risk: high/med/low)
Rewritten acceptance criteria (Gherkin)
Questions for the PO (numbered)
```

## Quality bar
- Every rewritten criterion contains at least one concrete value (amount, date, role, count).
- Never invent business rules: when the rule is unknown, write it as a question.
- Answer in the user's language.
""")

S["example-mapping"] = ("""Prepare or run an Example Mapping (Three Amigos) session for a story: rules, concrete examples per rule, and open questions, then turn the result into scenarios. Use before refinement, when a story feels fuzzy, or when PO, dev and QA disagree on what done means.""", r"""
# Example mapping

Matt Wynne's technique: a story (yellow), its rules (blue), examples for each rule (green), and questions (red). Twenty-five minutes, three roles.

## Steps
1. Write the **story** card in one line.
2. Extract **rules**: each business rule or constraint becomes one blue card. Merge duplicates; split rules that contain "and".
3. For each rule, write **2 to 4 examples** as concrete, short titles ("the one where the invoice is already paid"). Include at least one counter-example per rule.
4. Every disagreement or unknown becomes a **red question card**. Do not resolve it by guessing.
5. Read the map: many red cards = not ready; many blue cards = story too big, propose a split by rule.
6. Convert green cards to Given / When / Then scenarios.

## Output
A text map:
```
STORY: ...
RULE 1: ...
  ex: the one where ...   ex: the one where ...
RULE 2: ...
QUESTIONS: ?1 ... ?2 ...
SIGNAL: ready | needs answers | split suggested (how)
```
followed by the Gherkin scenarios for the examples.

## Tips
- Examples use real-looking data from the domain, never "foo/bar".
- Time-box: if one rule needs more than 4 examples, it is probably two rules.
""")

S["risk-based-test-plan"] = ("""Build a lean, risk-based test plan for a feature, epic or release: scope, risk matrix (impact x likelihood), test approach per risk, test types, data, environments, entry and exit criteria. Use when a feature needs a plan, before a release, or when asked what to test first with limited time.""", r"""
# Risk-based test plan

Spend test effort where failure would hurt most. One to two pages, not a 40-page template.

## Inputs
Feature description or epic, list of stories, architecture notes if any, deadline and team capacity.

## Steps
1. **Scope**: in scope, out of scope (and why), assumptions.
2. **Risk storming**: list product risks with the SFDIPOT prompts (Structure, Function, Data, Interfaces, Platform, Operations, Time). Phrase each risk as "*X* may fail when *Y*, causing *Z*".
3. **Score** each risk: impact 1-3 x likelihood 1-3. Likelihood rises with new code, complex logic, many integrations, past bugs in the area, and AI-generated code that nobody fully read.
4. **Approach per risk**: which level (unit, API, UI, exploratory, performance, security, accessibility), who, and how much.
5. **Test data and environments**: what data must exist, how to reset it, which environment, which flags.
6. **Entry / exit criteria**: concrete and measurable (e.g. "no open blocker or critical bug", "all high risks covered by at least one automated check").
7. **Schedule**: tie the high risks to the earliest moment they can be tested.

## Output
Markdown with sections 1 to 7 and a risk table:
| # | Risk | Impact | Likelihood | Score | Approach | Owner |
Sort by score, highest first.

## Pitfalls
- A risk without an approach is a wish. A test type without a risk is waste.
- Mark explicitly what will **not** be tested; silence is not a decision.
""")

S["test-design-techniques"] = ("""Derive test cases systematically with equivalence partitioning, boundary value analysis, decision tables, state transitions and cause-effect reasoning, then output a compact, de-duplicated test case table. Use when you need test cases for a rule, a form, a calculation, a workflow or a validation, instead of ad-hoc examples.""", r"""
# Test design techniques

Pick the technique that matches the shape of the rule, apply it fully, then trim duplicates.

## Choose the technique
| The rule looks like | Technique |
|---|---|
| A field or numeric range | Equivalence partitions + boundary values (min-1, min, min+1, max-1, max, max+1) |
| Several conditions combine into an outcome | Decision table (one column per combination, then collapse "don't care") |
| An object moves through statuses | State transition table: valid transitions, invalid transitions, repeated events |
| Many independent parameters | Pairwise (see the `pairwise-combinations` skill) |
| A calculation | Partitions on each input + known-answer oracle + rounding edges |
| A list or collection | 0, 1, many, max, duplicates, ordering |

## Steps
1. Write the rule precisely (inputs, outputs, constraints). Ask if something is unknown.
2. Apply the chosen technique and **show the model** (partitions, decision table or state table).
3. Derive one test case per partition / column / transition; add boundaries.
4. Remove duplicates; keep the invalid cases separate (one invalid input per test, so a failure points to one cause).
5. Give the expected result for every case. If you cannot compute it, mark `ORACLE NEEDED`.

## Output
The model, then:
| ID | Technique | Inputs | Expected result | Priority |

## Quality bar
- Every boundary is tested on both sides.
- Invalid partitions are tested one at a time.
- Expected results are exact values, not "works correctly".
""")

S["pairwise-combinations"] = ("""Generate a small all-pairs (pairwise) test set covering every pair of parameter values, with a bundled stdlib Python script, plus constraints to exclude impossible combinations. Use for configuration matrices (browser x OS x role x language), feature flags, or any form with many independent options.""", r"""
# Pairwise combinations

Most defects are triggered by one parameter or an interaction of two. Pairwise covers every pair with a fraction of the full matrix.

## Steps
1. List parameters and their values. Keep values representative (partitions), not exhaustive.
2. Write constraints for impossible combinations, e.g. `os=iOS & browser=Edge`.
3. Run the script:
   ```bash
   python "${CLAUDE_SKILL_DIR}/scripts/pairwise.py" params.json --format md
   ```
   `params.json`:
   ```json
   {"parameters": {"browser": ["Chrome","Firefox","Safari"], "role": ["admin","accountant","viewer"], "lang": ["fr","es","pt"]},
    "exclude": [{"browser": "Safari", "role": "viewer"}],
    "seed": 1}
   ```
4. Report the number of rows versus the full product, and the pairs that a constraint made impossible.
5. Add by hand any **high-risk triple** the business cares about (pairwise does not cover triples).

## Output
A Markdown or CSV table, one row per test configuration, and a one-line coverage summary from the script.

## Notes
The script is greedy (not optimal) but deterministic for a given seed; it verifies that every allowed pair is covered and exits non-zero otherwise.
""")

S["gherkin-scenarios"] = ("""Write clean, business-readable Gherkin (Given/When/Then) scenarios and scenario outlines from acceptance criteria or examples, then lint them with a bundled script (one When per scenario, no UI clicks in steps, no vague words). Use for BDD, Cucumber/SpecFlow/Reqnroll/behave suites, or living documentation.""", r"""
# Gherkin scenarios

Declarative scenarios describe **behaviour**, not clicks.

## Rules
- One behaviour per scenario, one `When`.
- `Given` sets state, `When` is the action, `Then` is an observable outcome.
- Business language: "Given an unpaid invoice of 120.00 EUR", not "Given I click the Invoices tab".
- Concrete values; use `Scenario Outline` + `Examples` when only data varies.
- `Background` only for setup shared by **every** scenario of the feature.
- Name scenarios after the rule: "Late fee is not applied before the due date".

## Steps
1. Group criteria by rule; one `Feature` per capability.
2. Write scenarios, then outlines for data-driven variants (include boundaries).
3. Lint:
   ```bash
   python "${CLAUDE_SKILL_DIR}/scripts/gherkin_lint.py" path/to/features
   ```
4. Fix every finding or justify it.

## Output
`.feature` file content, then the lint result.

## Example
```gherkin
Feature: Late payment fee
  Rule: A fee applies only after the due date
    Scenario Outline: Fee depends on days overdue
      Given an unpaid invoice of <amount> EUR due on 2026-03-31
      When the fee job runs on <run_date>
      Then the late fee is <fee> EUR
      Examples:
        | amount | run_date   | fee   |
        | 100.00 | 2026-03-31 | 0.00  |
        | 100.00 | 2026-04-01 | 40.00 |
```
""")

S["test-data-fr"] = ("""Generate realistic but fake French business test data that passes real validation: SIREN/SIRET (Luhn), intra-EU VAT numbers, IBAN FR with RIB key, invoices with VAT rates 20/10/5.5/2.1 and correct rounding, using a deterministic stdlib script; it also validates identifiers. Use when tests need companies, bank details or invoices that the application will accept.""", r"""
# French business test data

Random strings fail checksum validation; real data creates GDPR risk. This generates **valid, fictitious** data.

## Commands
```bash
python "${CLAUDE_SKILL_DIR}/scripts/fr_test_data.py" companies --count 20 --seed 42 --format csv > companies.csv
python "${CLAUDE_SKILL_DIR}/scripts/fr_test_data.py" invoices  --count 50 --seed 7  --format json > invoices.json
python "${CLAUDE_SKILL_DIR}/scripts/fr_test_data.py" validate 732829320 FR44732829320 FR7630006000011234567890189
```

## What it produces
- `companies`: name (invented), SIREN, SIRET (head office NIC 00010-style), VAT number `FRkk+SIREN`, IBAN FR with valid RIB key and check digits, postcode, city.
- `invoices`: number, issue/due dates, net amount, VAT rate, VAT amount (half-up to the cent, per line), gross.
- `validate`: says which checksum passes or fails for each identifier (SIREN/SIRET Luhn, VAT key, IBAN mod 97).

## Also generate on request
Edge records the script does not make by itself: VAT-exempt invoice (0 %), credit note (negative), invoice with 100 lines, company name with accents and apostrophes (`L'Étoile & Fils`), maximum-length fields.

## Rules
- Never use real people's identifiers. Company names are invented syllables.
- Same `--seed` gives the same data, so failures are reproducible.
""")

S["test-case-export"] = ("""Convert test cases written in Markdown or JSON into import-ready CSV for Azure DevOps Test Plans or Jira Xray (steps with action and expected result), with a bundled stdlib script. Use when test cases designed with Claude must land in the team's test management tool without retyping.""", r"""
# Test case export

## Input format (JSON)
```json
[{"title": "Late fee applied the day after due date",
  "priority": 2, "area": "Billing\\Invoices",
  "steps": [{"action": "Create an unpaid invoice of 100 EUR due 2026-03-31", "expected": "Invoice is saved, status Unpaid"},
            {"action": "Run the fee job on 2026-04-01", "expected": "A late fee of 40 EUR is added"}]}]
```
Markdown is also accepted: a `## Title` heading per test, then a table `| Action | Expected |`.

## Commands
```bash
python "${CLAUDE_SKILL_DIR}/scripts/export_test_cases.py" cases.json --target azure > azure_import.csv
python "${CLAUDE_SKILL_DIR}/scripts/export_test_cases.py" cases.md   --target xray  > xray_import.csv
```

## Notes
- Azure DevOps: the CSV uses the columns `ID, Work Item Type, Title, Test Step, Step Action, Step Expected, Priority, Area Path`; import it from *Test Plans > Import test cases from CSV*. Leave `ID` empty for new items.
- Xray: one row per step with a shared `Test ID`; map columns in the Xray CSV importer.
- Check the column names against your project's process template before a large import; import 2 cases first.
""")

S["nfr-checklist"] = ("""Turn vague non-functional expectations into measurable, testable quality requirements using ISO/IEC 25010 characteristics: performance, reliability, security, usability, accessibility, compatibility, maintainability. Use when a feature or epic has no explicit NFRs, before load or security testing, or when someone says it must be fast.""", r"""
# Non-functional requirements checklist

## Steps
1. For the feature, walk each characteristic and ask the questions below. Skip what does not apply, but say so.
2. Rewrite each answer as a **measurable requirement**: metric, threshold, condition, how to verify.

| Characteristic | Questions |
|---|---|
| Performance | Expected volume (users, records, files)? Acceptable p95 response time? Batch window? |
| Reliability | What happens if a dependency is down? Retries? Data loss tolerated? Recovery time? |
| Security | Who may see / change what? Personal data involved? Audit trail needed? |
| Usability & accessibility | Keyboard-only use? Screen readers? Target RGAA/WCAG level? Error messages? |
| Compatibility | Browsers, devices, OS, API versions, file formats, other Cegid/third-party products? |
| Maintainability | Logs and metrics needed to support it? Feature flag? Config without redeploy? |
| Portability / data | Export, import, migration of existing data? |

## Output
| ID | Characteristic | Requirement (measurable) | Verification | Priority |
e.g. `p95 < 800 ms for the invoice list with 10,000 invoices, 50 concurrent users, verified by k6 in staging`.

## Pitfall
A requirement with no number is an opinion. Ask for the number; if nobody knows, propose one and flag it as an assumption.
""")

write_plugin(PLUGIN, DESC, S, ["shift-left", "test-design", "bdd", "test-data"])
