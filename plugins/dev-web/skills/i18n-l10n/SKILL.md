---
name: i18n-l10n
description: "Internationalise and localise business software correctly: externalised strings with ICU plural and gender rules, locale-aware dates, numbers and currencies (fr-FR decimal comma and narrow no-break space, es-ES, pt-PT, en-GB), time zones, sorting and search with accents, text expansion in layouts, and invariant formats for files and APIs. Use when adding a language, when numbers or dates display or parse wrongly, when building exports or imports, or when reviewing UI text handling."
---

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
