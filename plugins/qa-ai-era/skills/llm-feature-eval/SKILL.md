---
name: llm-feature-eval
description: "Design and run an evaluation suite for a product feature built on an LLM (summary, classification, extraction, chat assistant): golden dataset, rubric and graders (exact match, schema, LLM-as-judge with calibration), regression thresholds, cost and latency, plus edge and adversarial cases. Use when shipping or changing a prompt, a model or a RAG pipeline."
---

# Evaluate an LLM feature

## Steps
1. **Define success** per task with the product owner: what a good output is, what is unacceptable (wrong numbers, invented facts, unsafe content, wrong language).
2. **Golden set**: 50-200 real, anonymized inputs with expected outputs or reference facts; cover common cases, long inputs, multilingual, empty/garbage, ambiguous requests.
3. **Graders**, cheapest first: exact/regex match, JSON schema validity, numeric tolerance, fact checklists, then LLM-as-judge with a written rubric. Calibrate the judge on 20 human-graded items and report agreement.
4. **Run** the suite on the current version: score per category, failures with examples, cost per call, p95 latency.
5. **Regression gate**: thresholds per category; any change of prompt, model, temperature or retrieval reruns the suite in CI.
6. **Monitor** in production: sample outputs for human review, user feedback signals.

## Output
Eval plan, dataset schema, grader definitions, results table by category, and the thresholds proposed.

## Pitfalls
Five hand-picked examples are a demo, not an eval. A judge model without calibration measures its own taste.
