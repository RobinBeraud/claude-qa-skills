from _gen import write_plugin

PLUGIN = "qa-automation"
DESC = "Write automated checks that stay green for the right reasons: Playwright end-to-end, API suites from OpenAPI, contract tests, property-based and mutation testing, k6 load tests, accessibility and visual regression, characterization tests for legacy code, and test-smell reviews."

S = {}

S["playwright-e2e"] = ("""Write or fix Playwright end-to-end tests (TypeScript or Python) with user-facing locators, web-first assertions, isolated test data and no fixed sleeps, then run them and iterate until they pass for the right reason. Use when asked for UI/E2E tests, to automate a scenario, or to stabilise a failing Playwright test.""", r"""
# Playwright end-to-end tests

## Principles
- **Locators users see**: `getByRole`, `getByLabel`, `getByText`, `getByTestId` as a last resort. No CSS chains, no XPath.
- **Web-first assertions** that auto-wait: `await expect(locator).toHaveText(...)`. Never `waitForTimeout`.
- **Independent tests**: each test creates its own data (API or fixture) and does not depend on order.
- **Authenticate once** with `storageState`, not through the login form in every test.
- **Mock only third parties** you do not own (`page.route`), never your own backend in an E2E test.
- One user journey per test; keep the pyramid: logic belongs in unit/API tests.

## Steps
1. Read the scenario (Gherkin or steps) and the app's existing test setup (`playwright.config`, fixtures, page objects).
2. Write the test with the conventions above; add a page object only if the screen is reused.
3. Run: `npx playwright test path --reporter=line` (or `pytest` for Python). Read failures and traces (`--trace on`).
4. Fix the **cause**: missing wait condition, wrong locator, shared data. Never add a sleep.
5. Run 5 times in a row (`--repeat-each=5`) to prove stability before handing over.

## Output
The test file, the commands run with their output, and the stability result. Mention anything you mocked.

## Red flags to refuse
`waitForTimeout`, `force: true` clicks to bypass overlays, `test.retry` used to hide a real race, assertions on CSS classes instead of behaviour.
""")

S["api-test-suite"] = ("""Generate an API test suite from an OpenAPI/Swagger spec or from example requests: happy paths, status codes, schema validation, authentication and authorization, validation errors, idempotency and pagination, in pytest+requests, REST Assured, Postman or Playwright request. Use when an API needs regression tests or a new endpoint lands.""", r"""
# API test suite

## Coverage checklist per endpoint
| Area | Cases |
|---|---|
| Happy path | Valid request, response body matches schema, values are correct |
| Validation | Each required field missing, wrong type, out of range, too long; error format is consistent |
| Auth | No token -> 401; expired token -> 401; wrong role -> 403; other tenant's resource -> 404 or 403 (never 200) |
| Idempotency | Same PUT/DELETE twice; POST retry with an idempotency key if supported |
| Lists | Empty list, pagination boundaries, sort and filter combinations, max page size |
| Concurrency | Update with stale version / ETag -> 409 or 412 |
| Errors | Downstream failure returns a clean 5xx with a correlation id, no stack trace |

## Steps
1. Read the spec (or capture examples). List endpoints by risk (money, permissions, data deletion first).
2. Generate tests with fixtures that create and delete their own data. Base URL and credentials from environment variables, never hard-coded.
3. Validate response **schemas** (jsonschema / openapi-core) as well as key values.
4. Run, report coverage per endpoint and per status code.

## Output
Test files, a table `endpoint x status codes covered`, and gaps (endpoints not covered, undocumented status codes seen).
""")

S["contract-testing"] = ("""Set up consumer-driven contract tests (Pact or schema-based) between a front end or service and the APIs it consumes, so breaking changes are caught in CI before deployment. Use when teams integrate across services, when E2E suites are slow or flaky, or when a provider change broke a consumer.""", r"""
# Contract testing

E2E tests prove two services work together once; contracts prove it on every build, fast.

## Steps
1. **Map interactions**: for each consumer, list the requests it really makes and the fields it really reads (not the whole provider schema).
2. **Consumer side**: write a Pact test per interaction (given state, request, minimal expected response with matchers like `like()` / `eachLike()`). Publish the pact to a broker or as a CI artifact.
3. **Provider side**: verify pacts against the real provider with state handlers that create the required data.
4. **CI gate**: `can-i-deploy` (Pact Broker) or a verification job that fails the provider build when a consumer contract breaks.
5. Without Pact: generate JSON Schemas of what the consumer reads and validate provider responses against them in the provider's test suite.

## Output
Consumer tests, provider verification setup, CI steps, and the list of interactions covered.

## Pitfalls
- Over-specified contracts (exact values, full payloads) break on harmless changes; match on types and the fields actually used.
- Contracts do not test business logic; keep API tests for that.
""")

S["property-based-tests"] = ("""Write property-based tests (Hypothesis for Python, fast-check for JS/TS, jqwik or FsCheck for JVM/.NET) that state invariants and let the framework search for counter-examples. Use for parsers, serializers, calculations, money/rounding, sorting, state machines, or anywhere example tests keep missing edge cases.""", r"""
# Property-based tests

## Find properties
| Pattern | Example |
|---|---|
| Round trip | `parse(format(x)) == x` (CSV, JSON, dates, amounts) |
| Invariant | Sum of invoice lines == invoice total; balance of debits == credits |
| Idempotence | `normalize(normalize(x)) == normalize(x)` |
| Oracle / reference | Optimised function == simple slow implementation |
| Metamorphic | Adding a 0-amount line does not change the total; sorting twice == sorting once |
| No crash | Any input of the right type -> no exception other than documented ones |

## Steps
1. Pick 2-4 properties for the unit under test; say why each matters.
2. Write generators that respect the domain (e.g. amounts as integers of cents, dates within the fiscal year), plus `assume()` for preconditions.
3. Run with enough examples (`max_examples=500` for critical code).
4. When a counter-example is found, keep the **shrunk** failing input as a regular example test.

## Output
Test code, the properties in plain words, and any counter-example found with its explanation.
""")

S["mutation-testing"] = ("""Measure how good a test suite really is with mutation testing (Stryker for JS/TS/.NET, PIT for Java, mutmut or cosmic-ray for Python): run it on the risky module, read surviving mutants and write the missing assertions. Use when coverage is high but bugs still slip through, or to judge tests written by an AI agent.""", r"""
# Mutation testing

Line coverage says code ran; mutation score says a test would notice if it were wrong.

## Steps
1. Scope it: one module or package with business logic (full-repo runs are slow).
2. Run the tool for the stack (`npx stryker run`, `mvn org.pitest:pitest-maven:mutationCoverage`, `mutmut run --paths-to-mutate src/billing`).
3. Read **survived** mutants. For each, classify: missing assertion, missing case, equivalent mutant (no behaviour change), or dead code.
4. Write the smallest test that kills each real survivor; delete dead code.
5. Report score before and after.

## Output
| Mutant (file:line, change) | Why it survived | Action |
plus the new tests and the score change.

## Notes
Useful as a quality gate on AI-generated tests: a suite that keeps 40 % of mutants alive was written to pass, not to check.
""")

S["performance-test-k6"] = ("""Design and script load, stress and soak tests with k6 (or Locust/Gatling if the team uses them): realistic scenarios, think time, thresholds on p95/p99 and error rate, and a readable results summary. Use before a release with performance risk, after an NFR is defined, or when users report slowness.""", r"""
# Performance tests with k6

## Steps
1. **Start from an NFR**: target load, p95/p99 latency, error rate, duration. No target, no test (see `nfr-checklist`).
2. **Model users**: the 3-5 journeys that matter, their mix (e.g. 70 % read list, 20 % open detail, 10 % create), think time.
3. **Choose the test type**: smoke (1-2 VUs), load (expected peak), stress (find the breaking point), soak (hours, memory leaks), spike.
4. **Script** with `scenarios`, `thresholds` and checks:
   ```js
   export const options = {
     scenarios: { browse: { executor: 'ramping-vus', stages: [{duration:'5m',target:50},{duration:'20m',target:50},{duration:'5m',target:0}] } },
     thresholds: { http_req_failed: ['rate<0.01'], http_req_duration: ['p(95)<800'] },
   };
   ```
5. **Data**: unique users and records per VU; never load-test production without written approval.
6. **Run** from a machine close to the system, watch server metrics (CPU, DB, queues) at the same time.
7. **Report**: thresholds pass/fail, latency percentiles per endpoint, errors, the bottleneck observed, and the next experiment.

## Pitfalls
Averages hide pain: use percentiles. A test with no server-side metrics finds *that* it is slow, not *why*.
""")

S["accessibility-audit"] = ("""Audit a web page or flow for accessibility against WCAG 2.2 AA and the French RGAA 4.1: automated axe-core scan through Playwright, plus the manual checks automation cannot do (keyboard, focus, screen reader names, contrast in context, error messages). Use before a release, for public-sector or B2B tenders, or when asked if a screen is accessible.""", r"""
# Accessibility audit

Automated tools find roughly a third of issues; the rest needs a person with a keyboard.

## Automated pass
```ts
import AxeBuilder from '@axe-core/playwright';
const results = await new AxeBuilder({ page }).withTags(['wcag2a','wcag2aa','wcag22aa']).analyze();
expect(results.violations).toEqual([]);
```
Run it on each key state (empty, filled, error, modal open).

## Manual pass (do every item)
1. **Keyboard only**: every action reachable with Tab/Shift+Tab/Enter/Space/Escape; visible focus; no keyboard trap; logical order.
2. **Names**: buttons, links, icons and form fields have an accessible name that says what they do.
3. **Forms**: labels tied to inputs; errors announced, explained and placed next to the field; required fields indicated without colour alone.
4. **Structure**: one `h1`, ordered headings, landmarks, lang attribute.
5. **Contrast**: 4.5:1 text, 3:1 large text and UI components, including hover/disabled states.
6. **Zoom 200 % and 320 px width**: no lost content, no horizontal scroll for text.
7. **Media and motion**: alt text, captions, no autoplay, respects `prefers-reduced-motion`.
8. **Screen reader spot check** (NVDA or VoiceOver) on the main journey.

## Output
| # | Criterion (WCAG / RGAA) | Where | Problem | Impact | Fix |
sorted by impact, plus the axe summary.
""")

S["visual-regression"] = ("""Add visual regression tests (Playwright toHaveScreenshot, or Percy/Chromatic/BackstopJS) on stable components and key screens, with masked dynamic areas, fixed viewports and a review workflow for baselines. Use when CSS or design-system changes keep breaking layouts unnoticed.""", r"""
# Visual regression

## Steps
1. Pick **stable, high-value** targets: design-system components in Storybook, key screens in fixed states. Avoid pages full of live data.
2. Make renders deterministic: fixed viewport and locale, frozen clock (`page.clock`), seeded data, disabled animations, web fonts loaded.
3. Mask dynamic regions: `await expect(page).toHaveScreenshot({ mask: [page.getByTestId('timestamp')], maxDiffPixelRatio: 0.01 })`.
4. Generate baselines **in CI's environment** (same OS and browser), commit them, and review every baseline update in the PR like code.
5. Keep the suite small; a screenshot that changes every week gets ignored.

## Output
Tests, config (thresholds, masks), and the baseline update procedure for the team.
""")

S["test-smell-review"] = ("""Review an existing test suite or a test file for smells that make tests useless or flaky: no or weak assertions, sleeps, order dependence, shared mutable state, logic in tests, over-mocking, tests that mirror the implementation, giant setups. Use when reviewing a PR's tests, auditing a legacy suite, or checking tests written by an AI agent.""", r"""
# Test smell review

## Smells to look for
| Smell | Sign | Why it hurts |
|---|---|---|
| No / weak assertion | `assert result` / `toBeTruthy()` / only "no exception" | Passes when the code is wrong |
| Mirror test | Expected value computed with the same formula as the code | Proves nothing |
| Over-mocking | Mocks of the unit's own collaborators everywhere | Tests the mocks, breaks on refactor |
| Sleep | `sleep`, `waitForTimeout`, `Thread.sleep` | Slow and flaky |
| Order dependence | Tests share records, statics, files | Fails when run alone or in parallel |
| Conditional logic | `if`/loops in the test | The test needs its own tests |
| Mystery guest | Data from an external file or DB nobody sees | Hard to understand, breaks silently |
| Eager test | One test checks ten behaviours | Unclear what broke |
| Catch-all | `try/except: pass` around the act | Swallows the failure |
| Snapshot dump | Huge snapshots accepted blindly | Reviewers click "update" |

## Steps
1. Read the tests next to the code they test.
2. List each smell with file:line and a concrete fix (rewrite the assertion, extract a fixture...).
3. Rate the suite: **trustworthy / needs work / misleading**, with the top 3 fixes.

## Output
Findings table `file:line | smell | fix`, the rating, and rewritten examples for the two worst tests.
""")

S["characterization-tests"] = ("""Pin down the current behaviour of legacy or untested code with characterization (golden master / approval) tests before refactoring or letting an agent change it: capture outputs for a wide input set, store them, and fail on any difference. Use before touching legacy code, migrating a calculation, or a big refactor.""", r"""
# Characterization tests

You do not know if the current behaviour is right, but you know it is what customers have today.

## Steps
1. Find the **seam**: a function, endpoint or batch whose inputs and outputs you can capture.
2. Build a wide input set: real anonymized samples, boundaries, random but seeded inputs (pairwise on options).
3. Record outputs to files (approval testing: ApprovalTests, `syrupy`, Jest snapshots, or plain JSON).
4. Make output stable: sort collections, freeze time, round floats explicitly, strip ids.
5. Commit the golden files. Any refactor must keep them identical; an intended change updates them in a reviewed commit that explains why.
6. Note behaviours that look like bugs in a list instead of fixing them during the refactor.

## Output
Test harness, golden files, and "suspicious behaviours" list for the product owner.
""")

write_plugin(PLUGIN, DESC, S, ["playwright", "api-testing", "k6", "accessibility", "mutation-testing"])
