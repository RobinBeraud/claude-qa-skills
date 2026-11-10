---
name: session-debrief
description: "Turn raw exploratory session notes (bullet notes, screenshots descriptions, chat logs) into a session-based test management debrief: coverage, bugs, issues, questions, time split and next charters. Use right after an exploratory session or bug bash, or to summarise several sessions for a test report."
---

# Session debrief (SBTM)

## Steps
1. Read the notes. Separate **bugs** (product misbehaves), **issues** (things that slowed testing: missing data, environment down, unclear requirement) and **questions**.
2. Rebuild **what was covered** (areas, data, platforms) and what was **not** covered.
3. Estimate the time split: setup / testing / bug investigation. High setup time is itself a finding.
4. Rate the confidence for the area: low / medium / high, with one sentence why.
5. Propose the next 1-3 charters.
6. For each bug, draft a one-line summary; full reports go through `bug-report`.

## Output
```
CHARTER:      TESTER:     DURATION:
COVERAGE:     ...
NOT COVERED:  ...
BUGS:         B1 ... (severity)
ISSUES:       I1 ...
QUESTIONS:    Q1 ...
TIME SPLIT:   setup x % / test y % / investigation z %
CONFIDENCE:   medium, because ...
NEXT:         charter ...
```
