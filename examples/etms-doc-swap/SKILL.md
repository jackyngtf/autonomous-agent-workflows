---
name: etms-doc-swap-reference
description: Public reference for a weekday 09:30 document-replacement handoff to an externally deployed engine; implementation is not included.
---

# eTMS replacement: entry contract

[**English**](SKILL.md) · [繁體中文](SKILL.zh-TW.md)

> Rewritten reference based on the available entry instructions. This file is not a runnable deployment configuration and contains no connection details. Engine behaviour and completed executions are not verified by this document.

The intended scheduled task runs on weekdays at 09:30; the source does not establish a timezone. Its purpose is to hand incoming document updates to the prebuilt engine and report the outcome. Read the [procedure reference](WORKINSTRUCTION.md) for the handoff and evidence boundaries.

## Authority and limits

- Obtain the required deployed engine, driver and configuration through the authorised external store. If they are missing, stop and report that the engine is not deployed.
- Follow the configured mode. Shadow means planning and verification with no production writes. The operator owns any change to live mode; the agent cannot switch itself.
- Use the engine or driver for planned file changes, version archives and designated logs or reports. Do not perform ad hoc manual swaps.
- Do not access databases, use database credentials or execute SQL. A file manifest derived from a static snapshot is not permission to query a database.
- Do not change version fields, training progress, completions, assignments, quizzes, database references, application code or container configuration. Retraining decisions are outside scope.
- Stop and report on failure or ambiguity. Do not silently retry a failed live write or improvise a repair to database references.
- Keep credentials and internal connection information out of output and reports.

## Driver result and report

Read the driver's structured output and newest report. Summarise input dispositions using the reported `PLANNED`, `SWAPPED` or `HELD` states, together with the reason. Identify actions required from the submitting team or operator, unavailable manifest destinations, partial results and engine errors.

For live mode, identify each reported replacement and its archived predecessor within the authorised private report. If the driver crashes, report the error and the last known state; do not perform a manual substitute operation.

Rollback is a delegated requirement of the engine contract. The agent must not describe it as successful without supporting output, and this public reference makes no claim that rollback has been tested.
