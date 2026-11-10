---
name: mutation-testing-setup
description: "Set up mutation testing for a project: pick the tool for the stack (Stryker for JS/TS and .NET, PIT for Java/Kotlin, mutmut or cosmic-ray for Python, Infection for PHP, go-mutesting for Go), scope it to business-critical code, configure timeouts and reporters, and run a first baseline. Use when starting with mutation testing or when coverage is high but bugs still slip through."
---

# Mutation testing setup

Line coverage says the code ran; the mutation score says a test would fail if the code were wrong.

## Tool per stack
| Stack | Tool | First run |
|---|---|---|
| JS / TS | StrykerJS | `npx stryker init` then `npx stryker run` |
| .NET | Stryker.NET | `dotnet tool install -g dotnet-stryker` then `dotnet stryker` |
| Java / Kotlin | PIT (pitest) | `mvn org.pitest:pitest-maven:mutationCoverage` or the Gradle plugin |
| Python | mutmut / cosmic-ray | `mutmut run --paths-to-mutate src/billing` |
| PHP | Infection | `vendor/bin/infection` |

## Steps
1. **Scope**: one package with business logic (pricing, rules, calculations). Exclude generated code, DTOs, logging.
2. **Configure**: test command, timeout factor, concurrency, the JSON reporter (`mutation-testing-report-schema` for Stryker, `XML`/`HTML` for PIT).
3. **Baseline**: run once, record the score and duration.
4. **Read the report** with `mutation-report-digest`, then triage with `surviving-mutant-triage`.
5. Make it part of the routine: nightly on critical packages, or incremental on PRs (`mutation-score-gate`).

## Output
Config file, commands, baseline score and duration, and the 10 most important survivors.
