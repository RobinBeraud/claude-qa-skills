---
name: incident-review
description: "Run a blameless post-incident review: factual timeline from logs and chat, impact in customer terms, contributing factors (not a single root cause or a person), what helped and what slowed detection and recovery, and a few owned, dated actions; for production outages, data issues, security events or failed releases. Use after a production incident, a hotfix, a rollback, a data correction, or a near miss worth learning from."
---

# Incident review (blameless)

People did what made sense with what they knew at the time. The question is what made it make sense.

## Document (within 5 working days)
```markdown
# Incident <id>: <short title>   Severity: <S1-S4>   Status: resolved
Impact: <who, how many tenants/users, which feature, how long, data affected?>
Detection: <how, when, by whom: monitoring, customer, support?>  Time to detect: <x>
Timeline (UTC): 10:02 deploy 12.4.1 ... 10:17 first alert ... 10:41 rollback ... 11:05 confirmed
Contributing factors: <technical, process, organisational; several>
What went well: <keep doing>
What slowed us: <detection, access, runbooks, communication>
Actions: | action | owner | due | type (prevent / detect / mitigate) |
```

## Facilitation
- Timeline first, from evidence (logs, deploy history, chat), before any discussion of causes.
- Ask "how" and "what", not "why did you"; no names in contributing factors.
- 3-5 actions maximum, each owned and dated; prefer detection and mitigation improvements over "be more careful".
- Share the review widely; track actions to completion.

## Links to delivery metrics
Feed the time to restore and the change failure into DORA metrics; a failed deployment counts even if fixed quickly.
