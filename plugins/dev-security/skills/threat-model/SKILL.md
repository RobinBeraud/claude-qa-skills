---
name: threat-model
description: "Threat model a feature or architecture with STRIDE before building it: data flow diagram with trust boundaries, threats per element (spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege), existing mitigations, risk rating and concrete security requirements and tests. Use when designing a new feature, integration, API, file exchange or admin tool, before a security review, or when a customer asks how a flow is protected."
---

# Threat model (STRIDE)

## 1. Draw the flow (text is fine)
Actors (users, admins, external systems), processes, data stores, data flows, and **trust boundaries** (internet / DMZ / internal, tenant / tenant, user / admin, our system / partner).

## 2. Threats per element
| Letter | Question | Typical mitigation |
|---|---|---|
| **S**poofing | can someone pretend to be a user or system? | strong auth, mTLS, signed tokens |
| **T**ampering | can data be changed in transit or at rest? | TLS, signatures, integrity checks, DB permissions |
| **R**epudiation | can someone deny an action? | audit log with who/what/when, tamper-evident |
| **I**nformation disclosure | can data leak (other tenant, logs, errors)? | authorisation, encryption, minimisation |
| **D**enial of service | can someone exhaust resources? | rate limits, quotas, timeouts, size limits |
| **E**levation of privilege | can someone gain rights? | least privilege, server-side checks, input validation |

## 3. Rate and decide
Likelihood x impact (low/medium/high); for each high/medium: mitigation, owner, and a **testable security requirement** ("an accountant of tenant A gets 404 on tenant B's invoice id").

## Output
Diagram, threats table, decisions (mitigate / accept with reason / transfer), requirements and tests to add to the backlog.
