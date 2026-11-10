---
name: mutation-testing
description: "Measure how good a test suite really is with mutation testing (Stryker for JS/TS/.NET, PIT for Java, mutmut or cosmic-ray for Python): run it on the risky module, read surviving mutants and write the missing assertions. Use when coverage is high but bugs still slip through, or to judge tests written by an AI agent."
---

# Mutation testing

Line coverage says code ran; mutation score says a test would notice if it were wrong.

## Steps
1. Scope it: one module or package with business logic (full-repo runs are slow).
2. Run the tool for the stack (`npx stryker run`, `mvn org.pitest:pitest-maven:mutationCoverage`, `mutmut run --paths-to-mutate src/billing`).
3. Read **survived** mutants. For each, classify: missing assertion, missing case, equivalent mutant (no behaviour change), or dead code.
4. Write the smallest test that kills each real survivor; delete dead code.
5. Report score before and after.

## Output
| Mutant (file:line, change) | Why it survived | Action |
plus the new tests and the score change.

## Notes
Useful as a quality gate on AI-generated tests: a suite that keeps 40 % of mutants alive was written to pass, not to check.
