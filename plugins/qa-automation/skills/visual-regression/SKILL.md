---
name: visual-regression
description: "Add visual regression tests (Playwright toHaveScreenshot, or Percy/Chromatic/BackstopJS) on stable components and key screens, with masked dynamic areas, fixed viewports and a review workflow for baselines. Use when CSS or design-system changes keep breaking layouts unnoticed."
---

# Visual regression

## Steps
1. Pick **stable, high-value** targets: design-system components in Storybook, key screens in fixed states. Avoid pages full of live data.
2. Make renders deterministic: fixed viewport and locale, frozen clock (`page.clock`), seeded data, disabled animations, web fonts loaded.
3. Mask dynamic regions: `await expect(page).toHaveScreenshot({ mask: [page.getByTestId('timestamp')], maxDiffPixelRatio: 0.01 })`.
4. Generate baselines **in CI's environment** (same OS and browser), commit them, and review every baseline update in the PR like code.
5. Keep the suite small; a screenshot that changes every week gets ignored.

## Output
Tests, config (thresholds, masks), and the baseline update procedure for the team.
