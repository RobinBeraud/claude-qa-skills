---
name: gdpr-by-design
description: "Build GDPR (RGPD) compliance into code: map personal data in the schema, minimise what is collected, retention periods with automatic purge, pseudonymisation and encryption, access and erasure requests (with legal retention exceptions such as accounting and payroll), consent where needed, personal data out of logs and test datasets. Use when designing a feature that touches personal data, adding fields, logs or exports, preparing a data protection review, or implementing a subject access or erasure request."
---

# GDPR by design

Not legal advice: decisions on legal bases and retention belong to the DPO. The code must make them enforceable.

## Steps for a feature
1. **Inventory**: which personal data (identity, contact, bank details, salary, health, NIR...), whose (employees, customers' customers), why (purpose), legal basis (contract, legal obligation, consent...). Write it in the PR or the data map.
2. **Minimise**: collect only what the purpose needs; no "might be useful" fields.
3. **Retention**: a period per data category, and a job that purges or anonymises after it. Accounting, invoicing and payroll data often have legal retention obligations (e.g. 10 years for accounting records in France): keep, but restrict access.
4. **Protect**: encryption in transit and at rest; field-level encryption or pseudonymisation for sensitive data (bank details, NIR, health); access by role, audited.
5. **Rights**: access (export the person's data in a readable format), rectification, erasure (delete or anonymise, except data under legal retention), portability. Implement them as tested functions, not manual SQL.
6. **Logs and observability**: no names, e-mails, IBANs or free text with personal data in logs, traces or error messages; ids instead.
7. **Non-production**: test and demo data synthetic or anonymised; never copy production personal data to dev or to an AI tool without approval.

## Review checklist
New personal field justified? Retention defined? Purge implemented and tested? Logged anywhere? Exported anywhere? Shared with a third party (processor contract)?
