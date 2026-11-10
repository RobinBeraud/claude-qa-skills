---
name: bug-report
description: "Write a clear, reproducible bug report from rough notes, logs, screenshots descriptions or a conversation: title that states the failure, minimal steps, expected vs actual, environment, evidence, impact, and separate severity and priority suggestions; formatted for Azure DevOps or Jira. Use whenever a defect must be logged or an existing report is too vague to act on."
---

# Bug report

Cem Kaner's **RIMGEA**: Replicate, Isolate, Maximize (show the worst consequence), Generalize (find the broader case), Externalize (impact on users), And say it dispassionately.

## Steps
1. **Title**: `<where> - <what fails> when <condition>`. e.g. "Invoice export - VAT total off by 0.01 EUR when lines have 3 decimals".
2. **Steps**: numbered, minimal, starting from a known state, with exact data.
3. **Expected** vs **Actual**, each one sentence, with values.
4. **Environment**: version/build, environment, browser/OS, tenant, user role, feature flags.
5. **Evidence**: log excerpt (trimmed, no secrets), screenshot names, request id / correlation id, timestamp with time zone.
6. **Scope**: what else is affected (generalize), what is *not* affected (isolate).
7. **Impact**: who is hurt, how often, workaround.
8. **Severity** (technical impact) and **priority** (business urgency) as *suggestions*, kept separate.

## Output
Markdown ready to paste, with an Azure DevOps field mapping when relevant (Repro Steps, System Info, Severity, Priority, Area Path, Tags).

## Never
Blame people, include personal data or credentials, or mix two bugs in one report.
