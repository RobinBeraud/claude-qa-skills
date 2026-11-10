---
name: nfr-checklist
description: "Turn vague non-functional expectations into measurable, testable quality requirements using ISO/IEC 25010 characteristics: performance, reliability, security, usability, accessibility, compatibility, maintainability. Use when a feature or epic has no explicit NFRs, before load or security testing, or when someone says it must be fast."
---

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
