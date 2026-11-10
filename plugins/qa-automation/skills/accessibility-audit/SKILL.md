---
name: accessibility-audit
description: "Audit a web page or flow for accessibility against WCAG 2.2 AA and the French RGAA 4.1: automated axe-core scan through Playwright, plus the manual checks automation cannot do (keyboard, focus, screen reader names, contrast in context, error messages). Use before a release, for public-sector or B2B tenders, or when asked if a screen is accessible."
---

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
