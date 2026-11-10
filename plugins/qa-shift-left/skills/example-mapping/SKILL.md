---
name: example-mapping
description: "Prepare or run an Example Mapping (Three Amigos) session for a story: rules, concrete examples per rule, and open questions, then turn the result into scenarios. Use before refinement, when a story feels fuzzy, or when PO, dev and QA disagree on what done means."
---

# Example mapping

Matt Wynne's technique: a story (yellow), its rules (blue), examples for each rule (green), and questions (red). Twenty-five minutes, three roles.

## Steps
1. Write the **story** card in one line.
2. Extract **rules**: each business rule or constraint becomes one blue card. Merge duplicates; split rules that contain "and".
3. For each rule, write **2 to 4 examples** as concrete, short titles ("the one where the invoice is already paid"). Include at least one counter-example per rule.
4. Every disagreement or unknown becomes a **red question card**. Do not resolve it by guessing.
5. Read the map: many red cards = not ready; many blue cards = story too big, propose a split by rule.
6. Convert green cards to Given / When / Then scenarios.

## Output
A text map:
```
STORY: ...
RULE 1: ...
  ex: the one where ...   ex: the one where ...
RULE 2: ...
QUESTIONS: ?1 ... ?2 ...
SIGNAL: ready | needs answers | split suggested (how)
```
followed by the Gherkin scenarios for the examples.

## Tips
- Examples use real-looking data from the domain, never "foo/bar".
- Time-box: if one rule needs more than 4 examples, it is probably two rules.
