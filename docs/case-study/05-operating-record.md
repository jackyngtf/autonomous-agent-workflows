# 05 · Operating record

[English](05-operating-record.md) · [繁體中文](05-operating-record.zh-TW.md) · [Project overview](../../README.md)

The evidence inventory was assembled on **September 22, 2026**, from the two canonical report folders. Archived copies and consolidation reports are excluded from the run-report count.

| Workflow | Report artifacts | Distinct dates | First–last report date |
|---|---:|---:|---|
| Avaya call logs | 47 | 46 | June 11–September 14, 2026 |
| NAS access logs | 45 | 45 | June 12–September 15, 2026 |
| Total | 92 | — | Different windows; no shared uptime denominator |

Avaya has both an aborted-session report and a native recovery report dated September 11. They remain separate ledger rows. A filename is not a verified execution ID, and two artifacts do not automatically prove two scheduler launches.

## Selected outcomes

| Date / workflow | Recorded outcome | Interpretation |
|---|---|---|
| June 15 / Avaya | 14 new rows; 182 existing data rows across eight sheets; 196 output data rows | Report describes pre-write content verification and post-upload count checks. |
| June 25 / NAS | Duplicate-header defect detected and corrected before upload | Evidence of a validation-driven correction, not a zero-defect history. |
| August 3 / NAS | 313,721 output data rows; 23.6-second parse and 22.8-second write | One recorded run; existing parse rows include headers. |
| August 10 / Avaya | Two new sheets, 36 new data rows | Scheduled report; malformed inputs retained for investigation. |
| September 11 / Avaya | Scheduled session blocked; native recovery added 21 rows | Separate artifacts and execution modes. |
| September 15 / NAS | Four new sheets, 40,179 new rows; older gaps remained | Manual/native recovery with incomplete historical coverage. |

Each row links through the [claim index](../evidence/claim-index.md) to a sanitized narrative and private source locator. The [CSV ledger](../evidence/run-ledger.csv) includes a SHA-256 digest for each source report; a digest identifies a file snapshot, not the truth of its contents.

## What remains unknown

Some destination workbooks were updated by sessions or actors absent from the local report history. Scheduler logs and complete intervention records were not part of this inventory. Most ledger entries are intentionally inventory-only, with execution mode and outcome marked unknown until individually assessed.

The record therefore cannot support an uptime percentage, success rate, “60+ unattended runs per agent,” hours saved, or continuous operation through the inventory date. No production connection was made to refresh those historical observations during portfolio preparation.

[Previous](04-incidents-and-recovery.md) · [Next: lessons and limitations](06-lessons-and-limitations.md)
