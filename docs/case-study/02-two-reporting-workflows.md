# 02 · Two reporting workflows

[English](02-two-reporting-workflows.md) · [繁體中文](02-two-reporting-workflows.zh-TW.md) · [Project overview](../../README.md)

Both workflows produce a monthly workbook, but their input and recovery policies differ.

| Decision | PBX call reporting | NAS access reporting |
|---|---|---|
| Input | Daily SMDR CSV files from a separate receiver | File-transfer events from the NAS API |
| Intended schedule | Weekdays around 10 AM, Melbourne | Weekdays around 9 AM, Melbourne |
| Eligible dates | Completed dates, up to yesterday | Completed dates, up to yesterday |
| Worksheet grouping | One worksheet per eligible daily CSV | Working days individually; consecutive non-working days grouped within a month |
| Existing coverage | Inspect worksheets before adding a date | Inspect monthly workbooks and verify coverage before planning |
| Invalid or unavailable input | Retain malformed files and report them | Investigate zero-row dates; report unavailable history explicitly |
| After publication | Eligible source cleanup only after output verification | No source-record deletion |

Schedule entries describe the intended operation. They do not establish that every scheduled session ran or completed.

## Shared processing path

1. Check the execution environment and required dependencies.
2. Inspect source inputs and the actual destination workbook.
3. Plan additions for missing, completed dates.
4. Reconstruct the monthly workbook with existing tabular records and new worksheets.
5. Validate the local output, publish it, and download the published copy for another check.
6. Record additions, skipped inputs, failures, and any required intervention.

Each affected month has its own workbook. A catch-up session can update two months, but a grouped worksheet must not cross a month boundary.

## Different failure consequences

For call logs, a malformed CSV remains available for investigation. A June 15 report records one valid file added and a binary-contaminated file retained. Cleanup is a distinct decision after verification; successful parsing alone does not justify deletion.

For NAS logs, the original events may cease to be available through the live API. During the September 15 recovery, some old dates could no longer be retrieved. An empty worksheet would have obscured that gap, so the report kept it visible while processing recoverable dates.

## Why inspect the destination first?

Local reports can be missing while another session has already updated the destination. Both September recovery stories encountered this situation. Reusing a stale catch-up plan could duplicate work or misstate the backlog. The agent must reconcile the plan with the workbook it actually reads.

The [selected run narratives](../evidence/selected-run-extracts/README.md) describe these outcomes. The [architecture reference](../architecture.md) expands the responsibilities and boundaries.

[Previous](01-context-and-role.md) · [Next: integrity and verification](03-integrity-and-verification.md)
