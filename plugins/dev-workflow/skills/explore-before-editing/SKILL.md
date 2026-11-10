---
name: explore-before-editing
description: "Build a working map of an unfamiliar codebase before changing it: entry points, layers, conventions, build and test commands, where the change belongs, and what could break. Use when starting work in a repository or module you have not touched yet, when a change request names code you have not read, or before any refactor that crosses several files."
---

# Explore before editing

```
NO EDIT BEFORE YOU CAN SAY WHERE THE CHANGE GOES AND HOW YOU WILL KNOW IT WORKS
```

## Steps
1. **Build and test commands**: find them (README, `*.sln`, `package.json`, `Makefile`, pipeline YAML) and run the tests once to get a baseline. Note pre-existing failures; they are not yours.
2. **Map**: entry points (controllers, jobs, CLI, UI routes), layers, the 5-10 files that matter for this change. Use search, not guesses: `git grep`, symbol search, callers of the function.
3. **Conventions**: naming, error handling, logging, DI, test style. Read two neighbouring files and copy their patterns.
4. **History**: `git log --oneline -15 -- <path>` and blame on the lines you will touch. Why is it like this? A strange line often fixes a real bug.
5. **Blast radius**: who calls this code (other modules, APIs, batch jobs, reports)? Public contracts (API, DB schema, file formats) need extra care.
6. **Write it down** in 10 lines: where the change goes, files to touch, tests to add, risks, open questions. Ask the open questions before coding.

## Red flags
- "I'll just add it here" without having read the callers.
- Creating a new helper when an equivalent exists two folders away.
- Changing formatting or names in files you only needed to read.

## Output
A short map: commands, key files, conventions, blast radius, plan, questions.
