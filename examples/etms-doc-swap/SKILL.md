---
name: etms-doc-swap-reference
description: Public reference for a weekday 09:30 document-replacement handoff to an externally deployed engine; implementation is not included.
---

# eTMS replacement: entry contract

[**English**](SKILL.md) · [繁體中文](SKILL.zh-TW.md)

> Rewritten entry-contract reference, not a runnable deployment configuration. A read-only deployment/source review on 22 September 2026 confirmed the external files and a shadow configuration. The source review did not execute the operational code. A separately assessed manual shadow report recorded 30 HELD and 0 SWAPPED; it does not establish successful replacement. See the [dated review](../../docs/evidence/etms-deployment-review-2026-09-22.md) for implementation gaps.

The intended scheduled task runs on weekdays at 09:30; the source does not establish a timezone. Its purpose is to hand incoming document updates to the prebuilt engine and report the outcome. Read the [procedure reference](WORKINSTRUCTION.md) for the handoff and evidence boundaries.

## Authority and limits

- Obtain the required deployed engine, driver and configuration through the authorised external store. If they are missing, stop and report that the engine is not deployed.
- Follow the configured mode. The entry contract intends shadow to plan and verify without production-document swaps. The reviewed driver still performs inbox housekeeping and report uploads in shadow; do not treat the mode as a guarantee of no remote changes. The operator owns any change to live mode; the agent cannot switch itself.
- Use the engine or driver for planned file changes, version archives and designated logs or reports. Do not perform ad hoc manual swaps.
- Do not access databases, use database credentials or execute SQL. A file manifest derived from a static snapshot is not permission to query a database.
- Do not change version fields, training progress, completions, assignments, quizzes, database references, application code or container configuration. Retraining decisions are outside scope.
- Stop and report on failure or ambiguity. Do not silently retry a failed live write or improvise a repair to database references.
- Keep credentials and internal connection information out of output and reports.

## Driver result and report

Read the driver's structured output and newest report. Summarise input dispositions using the reported `PLANNED`, `SWAPPED` or `HELD` states, together with the reason. Identify actions required from the submitting team or operator, unavailable manifest destinations, partial results and engine errors.

The reviewed driver ignores the first engine subprocess status and returns zero in shadow. A zero exit is therefore not sufficient evidence that planning succeeded. Inspect report content and per-item states; preserve `ERROR` and missing-result cases rather than presenting them as completion.

For live mode, identify each reported replacement and its archived predecessor within the authorised private report. If the driver crashes, report the error and the last known state; do not perform a manual substitute operation.

Rollback is a delegated requirement of the engine contract. Source inspection is separate from testing that requirement. The agent must not describe rollback as successful without supporting evidence; no exercised rollback result is claimed here.
