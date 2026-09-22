---
name: avaya-call-log-reference
description: Design reference for a scheduled SMDR-to-workbook reporting workflow; not a deployable integration.
---

# Avaya reporting: entry instructions

[**English**](SKILL.md) · [繁體中文](SKILL.zh-TW.md)

> Public design reference. These instructions explain the intended task contract; they provide no live NAS access. Use the [offline demo](../../demo/README.md) to run the synthetic example.

Read [WORKINSTRUCTION.md](WORKINSTRUCTION.md) before processing. Establish the configured working scope, source schema, `Australia/Melbourne` cutoff and supported workbook contract. Search incident history when a specific error or uncertainty makes it relevant, and check whether the finding is still applicable.

## Expected task behaviour

- Plan only missing dates completed before the current Melbourne day.
- Treat a confirmed missing destination differently from an unreadable or inaccessible workbook.
- Preserve existing tabular records within the supported workbook contract; rebuilding can replace the file.
- Validate a candidate against independently prepared expected records before publication.
- In a live adapter, retrieve and verify the published copy before considering source cleanup.
- Keep malformed or unverified source files for review; report the reason.
- Stop when ambiguity or a policy decision exceeds the task's configured authority.
- Keep credentials and sensitive record values out of operational summaries.

A failed post-upload check can block cleanup but cannot undo an earlier upload. Live publication, backup and recovery behaviour must be defined separately.

## Reporting and knowledge

Record the attempt's execution mode, cutoff, plan, outcome, verification scope, cleanup decision and unresolved questions. Use [the synthetic report](sample-report.md) as a format illustration, not a source of production results.

Add new observations with provenance. A procedure change needs a reason and an appropriate scope check; recording a lesson is not permission to change deletion policy. See [knowledge maintenance](../../docs/self-improvement-loop.md).

These are intended constraints, not a claim that written instructions alone enforce them.