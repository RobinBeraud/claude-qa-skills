---
name: playwright-e2e
description: "Write or fix Playwright end-to-end tests (TypeScript or Python) with user-facing locators, web-first assertions, isolated test data and no fixed sleeps, then run them and iterate until they pass for the right reason. Use when asked for UI/E2E tests, to automate a scenario, or to stabilise a failing Playwright test."
---

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
