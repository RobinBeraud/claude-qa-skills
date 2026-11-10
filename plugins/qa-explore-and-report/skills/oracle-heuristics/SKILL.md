---
name: oracle-heuristics
description: "Decide whether an observed behaviour is a bug when there is no spec, using Michael Bolton's FEW HICCUPPS consistency oracles (familiar problems, explainability, world, history, image, comparable products, claims, user expectations, product, purpose, statutes), and write the argument a product owner can rule on. Use when someone says it is not a bug, it's a feature, or when requirements are silent."
---

# Oracle heuristics (FEW HICCUPPS)

A bug is something that bugs someone who matters. Without a spec, argue from consistency.

## Check the behaviour against each oracle
| Oracle | Ask |
|---|---|
| **F**amiliar problems | Does it look like a known class of bug (off-by-one, rounding, encoding, race)? |
| **E**xplainability | Can we explain the behaviour to a customer without embarrassment? |
| **W**orld | Is it consistent with how the real world works (calendars, laws of arithmetic, physical units)? |
| **H**istory | Is it consistent with earlier versions? |
| **I**mage | Is it consistent with the image the company wants to project? |
| **C**omparable products | What do similar products (competitors, other Cegid products) do? |
| **C**laims | What do the docs, marketing, contracts, help pages say? |
| **U**ser expectations | What would a reasonable user expect? |
| **P**roduct | Is it consistent with similar features elsewhere in the same product? |
| **P**urpose | Does it serve the purpose the feature exists for? |
| **S**tatutes & standards | Laws, regulations, accessibility norms, accounting rules, ISO formats? |

## Output
The observed behaviour, then the oracles that it **violates** (with evidence) and those it **satisfies**, then a recommendation: bug (severity), feature request, or works as designed, and the question to put to the product owner.
