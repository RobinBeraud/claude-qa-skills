---
name: risk-storming-workshop
description: "Facilitate a risk storming workshop (inspired by TestSphere and the risk storming format by Beren Van Daele) for a feature or release: quality aspects first, then risks per aspect, then test ideas per risk, with dot-voting and a prioritised outcome. Use at the start of an epic, before a release, or to involve the whole team in test strategy."
---

# Risk storming workshop (45-60 min)

## Agenda
1. **Context (5 min)**: what we build, for whom, what changes.
2. **Quality aspects (10 min)**: each person picks the 6 aspects that matter most (e.g. correctness of calculations, security, performance, usability, compatibility, data integrity, compliance, recoverability). Converge on 6.
3. **Risks (15 min)**: silent writing, one risk per sticky, placed under its aspect. Phrase: "*X* may fail when *Y*, causing *Z*".
4. **Vote (5 min)**: 3 dots per person on the most worrying risks.
5. **Test ideas (15 min)**: for the top risks, what would reveal the problem early? (test types, data, tools, monitoring, a spike).
6. **Wrap-up (5 min)**: owners and next steps.

## Facilitator's prompts
"What would embarrass us in front of a customer?" "What happened last time in this area?" "What do we assume the third party does?" "What if the data is 100x bigger?"

## Output
A prepared Miro/whiteboard structure, the facilitator script, and after the session: risks table sorted by votes with test ideas and owners, ready for `risk-based-test-plan`.
