---
name: dora-quick-check
description: "Run a quick, survey-based DORA estimate when no tooling data exists: ask the team the four classic questions (deployment frequency, lead time, change fail rate, recovery time) with the official answer ranges, collect answers per person, show spread and consensus, and turn disagreements into discussion. Use for a first assessment, a workshop, or to compare perception with measured data."
---

# DORA quick check

## Questions
Use the exact wording and answer ranges of the current quick check at dora.dev (they evolve with each report), for the primary application or service:
1. **Deployment frequency**: how often do you deploy to production?
2. **Change lead time**: how long from code committed to code running in production?
3. **Change fail rate**: what share of deployments cause a failure that needs remediation?
4. **Failed deployment recovery time**: how long to restore service after a failed deployment?
5. **Deployment rework rate**: what share of deployments are unplanned, to fix a defect in production?

## Steps
1. Ask each person individually (anonymous form).
2. Show the distribution per question; a wide spread means people do not share the same view of the system.
3. Discuss the spread first, the answer second.
4. Plan to replace the estimate with measured data (`dora-data-sources`).

## Output
Answer distribution per question, the consensus estimate, the disagreements worth discussing, and next steps.
