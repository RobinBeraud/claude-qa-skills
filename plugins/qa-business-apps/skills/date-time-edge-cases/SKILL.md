---
name: date-time-edge-cases
description: "Generate the date and time test cases that break business software: time zones and DST changes, end of month and leap years, fiscal years not aligned with calendar years, cut-off times, date-only vs timestamp, locale formats, week numbers and public holidays. Use when testing scheduling, billing periods, due dates, payroll, reporting by month, or any feature using now()."
---

# Date and time edge cases

## Checklist
| Area | Cases |
|---|---|
| Month ends | Jan 31 + 1 month; Feb 28/29; 30-day months; "last day of month" rules |
| Leap years | 2028-02-29, yearly recurrence from Feb 29, 366-day years in interest calculations |
| DST (Europe/Paris) | Last Sunday of March 02:00 -> 03:00 (02:30 does not exist); last Sunday of October 03:00 -> 02:00 (02:30 happens twice); jobs scheduled at those times |
| Time zones | User in Lisbon, server in UTC, tenant in Paris: which day is "today" at 23:30? |
| Cut-off | Order at 23:59:59 vs 00:00:00; batch running across midnight |
| Fiscal year | Year starting July 1; period 13; closing on a weekend |
| Date-only vs timestamp | A due date stored as midnight UTC shows as the previous day in America/* time zones |
| Formats | dd/mm/yyyy vs mm/dd/yyyy; ISO week 53; first day of week Monday vs Sunday |
| Holidays | Due dates moved by bank holidays (France, Spain, Portugal differ) |
| Clock in tests | Freeze the clock; never depend on the real date |

## Steps
1. Identify every date the feature reads, stores, computes or displays, and its time zone.
2. Pick the relevant rows above and write concrete cases with exact timestamps and zones.
3. Freeze or inject the clock in automated tests; run a few cases in a different machine time zone too.
