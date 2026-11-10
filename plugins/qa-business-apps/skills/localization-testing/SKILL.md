---
name: localization-testing
description: "Test localisation and internationalisation for French, Spanish and Portuguese markets (and others): translations complete and in context, number, currency, date and address formats, accents and encoding in imports/exports, text expansion, sorting with diacritics, and country-specific legal mentions. Use when releasing a feature in several countries or languages, or when users report garbled characters."
---

# Localisation testing

## Checklist
| Area | Cases |
|---|---|
| Translations | No missing keys or raw ids, no English left in FR/ES/PT screens, plural forms, gender agreement, context-appropriate business terms (validated by a native speaker) |
| Text expansion | Spanish/Portuguese strings can be 30 % longer: buttons, tables, PDFs, e-mails do not truncate |
| Numbers & currency | 1 234,56 EUR (fr), 1.234,56 EUR (es, pt); input accepts the local decimal separator; CSV exports document their separator |
| Dates | dd/mm/yyyy; month names; first day of week |
| Encoding | `é è ç ñ ã õ œ` and `€` survive imports, exports, PDFs, e-mails, file names; CSV opened in Excel (UTF-8 BOM) |
| Sorting & search | `Écran` sorts with `E`; accent-insensitive search finds `Élodie` with `elodie` |
| Addresses & ids | Postal code formats, NIF/NIE (ES), NIF (PT), SIREN/SIRET (FR), IBAN by country |
| Legal mentions | Invoice mandatory mentions per country, VAT wording, data-protection notices |

## Output
Findings per locale with screenshots descriptions, and a list of strings needing a native review.
