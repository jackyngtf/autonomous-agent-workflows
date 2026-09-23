# NAS access-log workflow: procedure reference

[**English**](WORKINSTRUCTION.md) · [繁體中文](WORKINSTRUCTION.zh-TW.md)

> Rewritten design reference, not an executable deployment guide. No credentials or live authentication snippets are included. Project-specific NAS behaviour needs verification in any new environment.

## Purpose and source boundary

The historical workflow collected Synology file-transfer activity and added missing date coverage to monthly workbooks. Its original schedule was weekdays at 09:00. The procedure used SyslogClient with `logtype=cifs`, hourly windows and a 50,000-result limit.

These are recorded integration choices, not a supported API contract for every DSM version. Authentication requirements, pagination, filtering and retention must be verified for the target system. A response at its limit may be truncated; a successful HTTP request alone does not establish completeness.

The public [JSON fixture](../../sample-data/nas-syslog/nas_access_records_2026-08-04.json) is synthetic. The [local parser](../../demo/workflows.py) checks its declared fields and timestamps without calling a NAS.

## Dates and reporting policy

Use `Australia/Melbourne` to convert timestamps and determine the current day. Exclude current-day and future records. The historical design used Victorian working days and grouped consecutive non-working days within a month.

The offline demo deliberately uses one worksheet per completed local date, including weekends, and separates months. It does not implement the historical holiday-grouping policy. A live adapter must define its chosen policy explicitly, including zero-row dates and source-retention gaps.

## Procedure and failure boundaries

| Step | Action | Required decision or check |
|---|---|---|
| 1. Inspect | Establish actual destination coverage and source availability | A stale report is not authoritative; unreadable is not absent |
| 2. Fetch | Retrieve the required time windows through the configured adapter | Detect truncation, invalid filtering, timestamp gaps and failed requests |
| 3. Plan | Group accepted records by the declared date policy | Separate confirmed zero records from unknown completeness |
| 4. Prepare | Snapshot existing records and build the candidate | Reject conflicting updates rather than silently replacing prior records |
| 5. Validate | Compare expected sheets, counts and cell values | Expected records must be prepared independently of the rebuild output |
| 6. Publish | Write through the live destination adapter | Define concurrency, backup and partial-write recovery |
| 7. Retrieve | Download and check the published copy | Post-upload failure is an incident, not proof that the destination was untouched |
| 8. Report | Record coverage, changes, verification and unresolved gaps | Attribute scheduled, manual and unknown execution modes correctly |

Rebuilding replaces a file while aiming to preserve its supported tabular records. It does not preserve arbitrary Excel features. This workflow does not require source-log deletion.

## Deployment responsibilities

An owner must supply credential delivery, least-required permissions verified for the actual API, time-window and pagination handling, retention policy and a recovery method. Authentication workarounds observed in this project should not be generalised without testing. The public reference intentionally omits HTTP login code and privilege assumptions.

Document maintenance is separate from exporting. Track monthly maintenance completion only after successful completion, and retain original incident history if a complete audit trail is required. See [knowledge maintenance](../../docs/self-improvement-loop.md).

## Try the local reconstruction

```sh
python -m demo --workflow nas --output-dir output/demo
```

The demo checks synthetic local records, plans dates and verifies local workbooks. It cannot prove live API completeness, NAS delivery or scheduler reliability. See [the guide](../../demo/README.md) and [synthetic report format](sample-report.md).