from _gen import write_plugin

PLUGIN = "dev-web"
DESC = "Front-end for business applications: Angular modernisation (standalone, signals, control flow, migration schematics), TypeScript strictness enabled step by step, accessibility to WCAG 2.2 and RGAA for French public-sector customers, and internationalisation of dates, numbers, currencies and translations."

S = {}

S["angular-modernize"] = ("""Modernise an Angular application step by step: version-by-version upgrades with ng update, standalone components, signals and the new control flow, inject() function, typed reactive forms, OnPush change detection, and removal of deprecated modules, each through official migration schematics with tests between steps. Use when upgrading Angular, migrating NgModules or RxJS-heavy state to signals, or reviewing Angular code for modern patterns.""", r"""
# Angular modernisation

## Upgrade path
1. One major version at a time: check https://angular.dev/update-guide for the exact steps of your versions.
2. `ng update @angular/core@<next> @angular/cli@<next>`; then the libraries (Material, NgRx...), which must support that version.
3. Build, unit tests, e2e smoke tests, commit. Next major.

## Official migrations (each its own PR)
```bash
ng generate @angular/core:standalone          # NgModules -> standalone (run its 3 modes in order)
ng generate @angular/core:control-flow        # *ngIf/*ngFor -> @if/@for (track is required)
ng generate @angular/core:inject              # constructor injection -> inject()
ng generate @angular/core:signal-input-migration
ng generate @angular/core:signal-queries-migration
```

## Patterns
- State in components: signals (`signal`, `computed`, `effect` sparingly); RxJS for event streams and HTTP, bridged with `toSignal`.
- `ChangeDetectionStrategy.OnPush` for new components.
- Typed reactive forms; no `any` in form models.
- `@defer` for heavy, below-the-fold parts.
- Lazy-loaded routes per feature; no shared mega-module.

## Rules
Never mix a framework upgrade with a refactor in the same PR. Keep e2e tests on the critical journeys green at every step.
""")

S["typescript-strict"] = ("""Turn on TypeScript strictness in an existing codebase without a big-bang: measure errors per flag, enable flags one at a time (noImplicitAny, strictNullChecks, ...), fix by folder with a ratchet so the error count only goes down, and ban new any. Use when a TypeScript or Angular project has strict mode off, when runtime undefined errors are frequent, or when reviewing type safety.""", r"""
# TypeScript strictness

## Measure
```bash
npx tsc --noEmit -p tsconfig.json --strict 2>&1 | grep -c "error TS"
```
Count errors per flag by enabling them one at a time in a scratch `tsconfig.strict.json` that `extends` the main one.

## Order (easiest value first)
1. `noImplicitAny`, 2. `strictNullChecks` (most bugs found), 3. `strictFunctionTypes`, `strictBindCallApply`, 4. `noImplicitOverride`, `noUncheckedIndexedAccess` (optional, strong), 5. full `strict`. Angular: also `strictTemplates`.

## Ratchet
- Enable the flag in a separate config checked in CI for already-clean folders; widen the list folder by folder.
- Or record the current error count in CI and fail when it grows.
- Lint rule `@typescript-eslint/no-explicit-any` as error for new code.

## Fixing
- Model the data: interfaces for API responses (generate from OpenAPI when possible).
- `undefined` handled at the boundary (parse/validate API data, e.g. with zod), not with `!` everywhere.
- `unknown` + narrowing instead of `any` for truly unknown input.
""")

S["accessibility-rgaa"] = ("""Check and fix web accessibility against WCAG 2.2 AA and the French RGAA 4.1 (mandatory for public-sector customers and large companies in France): semantic HTML, keyboard navigation and focus, labels and error messages in forms, contrast, ARIA used correctly, tables and dynamic content, with automated tools plus a manual pass. Use when building or reviewing UI, before a release to public-sector customers, or when an accessibility audit or declaration is requested.""", r"""
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
""")

S["i18n-l10n"] = ("""Internationalise and localise business software correctly: externalised strings with ICU plural and gender rules, locale-aware dates, numbers and currencies (fr-FR decimal comma and narrow no-break space, es-ES, pt-PT, en-GB), time zones, sorting and search with accents, text expansion in layouts, and invariant formats for files and APIs. Use when adding a language, when numbers or dates display or parse wrongly, when building exports or imports, or when reviewing UI text handling.""", r"""
# i18n and l10n

## Two different worlds
| Where | Format |
|---|---|
| UI, PDF for humans | the user's locale |
| Files, APIs, databases, logs | invariant: ISO 8601 dates, `.` decimal, no thousands separator, UTF-8 |
Mixing them is the classic bug: an export opened in French Excel, a CSV with `;` and decimal commas parsed as invariant.

## Strings
- No concatenated sentences (`"Invoice " + n + " sent"`); use message templates with ICU: `{count, plural, one {# facture} other {# factures}}`.
- Keys by meaning, not by English text; translators get context and max length.
- Plan for +30 % text length (German, Spanish, Portuguese); no fixed-width buttons.

## Numbers, money, dates
- Format with the platform (`Intl.NumberFormat`, Angular pipes with `LOCALE_ID`, .NET `CultureInfo`). `fr-FR`: `1 234,56 €` with a narrow no-break space (U+202F) as thousands separator: tests comparing strings must use it.
- Currency code travels with the amount; never assume EUR.
- Store instants in UTC, display in the user's time zone; business dates (invoice date) are dates without time.

## Text
- Sorting and search: culture-aware collation; accent-insensitive search where users expect it (`é` = `e`).
- Case conversions with the right culture (Turkish i), or invariant for identifiers.

## Tests
Pseudo-localisation (long, accented strings) to find hard-coded text and truncation; unit tests of formatting per supported locale; round-trip tests for imports/exports. For a full localisation test plan, see `qa-business-apps:localization-testing`.
""")

write_plugin(PLUGIN, DESC, S, ["angular", "typescript", "accessibility", "rgaa", "i18n"])
