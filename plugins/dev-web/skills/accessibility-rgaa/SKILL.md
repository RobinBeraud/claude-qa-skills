---
name: accessibility-rgaa
description: "Check and fix web accessibility against WCAG 2.2 AA and the French RGAA 4.1 (mandatory for public-sector customers and large companies in France): semantic HTML, keyboard navigation and focus, labels and error messages in forms, contrast, ARIA used correctly, tables and dynamic content, with automated tools plus a manual pass. Use when building or reviewing UI, before a release to public-sector customers, or when an accessibility audit or declaration is requested."
---

# Accessibility (WCAG 2.2 AA / RGAA 4.1)

Automated tools catch about a third of problems; the rest needs a keyboard and a screen reader.

## Automated
axe (browser extension, `@axe-core/playwright` in e2e), Lighthouse accessibility, eslint `angular-eslint/template` accessibility rules or `jsx-a11y`.

## Manual pass (the checks that matter most in business apps)
1. **Keyboard only**: every action reachable with Tab/Shift-Tab/Enter/Space/Escape; visible focus; no trap; logical order; focus moved into dialogs and back on close.
2. **Forms**: every field has a visible `<label>`; required fields stated in text; errors linked to the field (`aria-describedby`), announced, and saying how to fix.
3. **Structure**: one `h1`, ordered headings, landmarks (`header`, `nav`, `main`), page `title` per screen, `lang` attribute.
4. **Tables**: data tables with `th` and `scope`, caption; no layout tables. Sortable headers are buttons with state.
5. **Contrast**: 4.5:1 text, 3:1 large text and UI components; information never by colour alone (statuses need text or icon + label).
6. **Dynamic content**: toasts and async results in `aria-live` regions; spinners announced; no auto-dismiss for important messages.
7. **ARIA**: native elements first (`<button>`, not `<div (click)>`); ARIA only to fill gaps, with correct roles and states.
8. **Zoom**: usable at 200 % and 320 px width (reflow).

## RGAA specifics
Public-sector customers must publish an accessibility declaration (compliance rate, non-compliances, alternatives) and a multi-year plan. Map each issue to its RGAA criterion number in the report.

## Output
Issues table: criterion (WCAG / RGAA), page, element, impact, fix; plus the tests added to prevent regressions.
