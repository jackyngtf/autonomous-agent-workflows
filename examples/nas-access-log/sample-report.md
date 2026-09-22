# NAS access log: synthetic report example

[**English**](sample-report.md) · [繁體中文](sample-report.zh-TW.md)

> Fictional narrative example, not a production run or generated demo result. Dates and outcomes illustrate the report format. Use the offline demo's generated evidence for reproducible checks.

## Attempt summary

| Field | Illustrative value |
|---|---|
| Attempt | Example on 29 July 2026, 09:00 Australia/Melbourne |
| Execution mode | Synthetic walkthrough |
| Cutoff | Through 28 July 2026 |
| Outcome | One completed date prepared for publication |
| Destination | Fictional July reporting workbook |
| Live authentication and upload | Not performed |
| Validation | Expected sheet names, counts and cell values compared in the scenario |

## Coverage and exceptions

| Date or condition | Decision |
|---|---|
| 28 July | Plan the missing completed date |
| 29 July | Exclude the current local day |
| Already covered dates | Inspect existing records before declaring no change |
| Response reaches configured limit | Treat completeness as unresolved; do not publish that update |
| Zero-row response | Establish whether it means no activity or a query/retention gap |

These are illustrative decisions, not claims about a real query response.

## Month-end maintenance

29 July 2026 is a Wednesday, not the final weekday of that month. This example does not assert a month-end consolidation trigger or link to a future completed report. Any catch-up decision would require the configured working-day calendar and the last successfully completed maintenance month.

The earlier public example combined a 29 July report with a claim about 31 July consolidation. It has been replaced with this explicitly synthetic example; no historical outcome is inferred from the correction.

## Follow-up and limits

A live deployment would report actual API coverage, publication and retrieved-copy checks separately. It would retain unresolved source gaps instead of labelling every missing date as recovered. The [offline demo](../../demo/README.md) uses local synthetic JSON and does not authenticate to a NAS.