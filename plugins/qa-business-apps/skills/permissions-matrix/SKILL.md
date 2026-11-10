---
name: permissions-matrix
description: "Turn a roles x actions permission matrix (CSV) into positive and negative test cases, and compare expected permissions with observed results from a test run to list every mismatch, with a bundled stdlib script. Use when testing role-based access control, before a release that touches roles, or to audit what each profile can really do."
---

# Permissions matrix

## Matrix format (CSV)
```
action,admin,accountant,viewer
invoice.create,allow,allow,deny
invoice.delete,allow,deny,deny
period.close,allow,deny,deny
```

## Commands
```bash
python "${CLAUDE_SKILL_DIR}/scripts/rbac_matrix.py" generate matrix.csv > rbac_cases.md
python "${CLAUDE_SKILL_DIR}/scripts/rbac_matrix.py" compare matrix.csv observed.csv
```
- `generate`: one test case per (role, action): allowed actions must succeed, denied ones must be refused (UI hidden **and** API refused with 403).
- `compare`: `observed.csv` has the same shape, filled from the test run. Prints each mismatch; a role allowed something it should not do is reported as `SECURITY`, the reverse as `FUNCTIONAL`. Exit 1 on any mismatch.

## Also test
Role changes taking effect immediately, users with several roles, inherited permissions, direct URL access to hidden screens, bulk actions, and API calls with a token from a lower role.
