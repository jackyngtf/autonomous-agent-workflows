---
name: nas-access-log-reference
description: Design reference for scheduled NAS activity reporting; not a deployable NAS integration.
---

# NAS reporting: entry instructions

[**English**](SKILL.md) · [繁體中文](SKILL.zh-TW.md)

> Public design reference. No live API or SMB configuration is supplied. Use the [offline demo](../../demo/README.md) for executable synthetic examples.

Read [WORKINSTRUCTION.md](WORKINSTRUCTION.md) before processing. Establish permitted scope, the actual source contract, date cutoff and supported destination format. Read current rules first; search historical incidents when a specific error or uncertainty makes them relevant.

## Expected task behaviour

- Use `Australia/Melbourne` to calculate completed dates; exclude the current local day.
- Inspect destination coverage rather than assuming a previous report is complete.
- Distinguish confirmed file absence from access or parsing failures.
- Treat capped, unfiltered or otherwise uncertain API responses as a completeness problem.
- Validate existing and new records against independently prepared expectations before publication.
- In a live adapter, retrieve and verify the published copy.
- Stop and report ambiguous date coverage, conflicting records or decisions outside authorised scope.
- Keep credentials, tokens and identifying file paths out of operational summaries.

Historical date-grouping and holiday rules belong in an explicit policy, not in ad hoc agent inference. A reported zero-row date must be distinguished from an unsuccessful or incomplete query.

## Reporting and knowledge

Record execution mode, source coverage, planned dates, actual changes, validation scope and unresolved gaps. The [synthetic report](sample-report.md) illustrates those fields; it is not a production result.

Report new findings with their date and source. Revisions to procedure must remain within the task's authority. Month-end document maintenance should have its own completion record and must not rerun a completed export after a documentation failure.

These instructions describe intended constraints. Technical enforcement, live credentials and recovery procedures are separate deployment responsibilities.