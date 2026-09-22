# Evidence guide

[English](README.md) · [繁體中文](README.zh-TW.md) · [Project overview](../../README.md)

This directory separates historical reports from design rules and from behavior a reviewer can reproduce locally. The inventory date is **September 22, 2026**. No live production connection was made for this portfolio review.

The [eTMS case](../case-study/07-etms-document-handoff.md) has a different evidence level: its entry instructions were inspected, but its private engine, configuration and operating outcomes were unavailable. It contributes no rows to the reporting ledger and no verified swap-count or rollback claim.

## Start here

- [Claim index](claim-index.md): the source and limitation behind each principal claim.
- [Selected run narratives](selected-run-extracts/README.md): rewritten, sanitized accounts of specific observations.
- [Report-artifact ledger](run-ledger.csv): all 92 canonical run-report files, with source digests and explicit unknown fields.
- [Operating-record chapter](../case-study/05-operating-record.md): the results that the inventory supports.

## Evidence labels

| Label | Meaning |
|---|---|
| Design rule | An intended boundary expressed in instructions; enforcement must be assessed separately. |
| Reported outcome | A dated report says this happened. The private integration was not rerun for this review. |
| Source inspection | The behavior is visible in inspected code or documents. It need not have been exercised. |
| Reproduced offline | A local synthetic demonstration or test; it does not establish production behavior. |
| Proposed | A future improvement, not a present capability claim. |
| Unresolved | Available sources are contradictory or insufficient. |

## Ledger scope and columns

Only files named `avaya_call_log_report_*.md` or `nas_access_log_report_*.md` directly within each workflow's canonical monthly `reports/` tree are included. Archive copies, consolidation reports, and self-improvement reports are excluded. This produces **47 Avaya artifacts across 46 dates** and **45 NAS artifacts across 45 dates**.

| Column | Interpretation |
|---|---|
| `artifact_id` | Stable ledger label; not a scheduler execution ID. |
| `workflow`, `report_date`, `source_report` | Workflow, date in filename, and basename of the private source. |
| `execution_mode`, `reported_outcome` | Assessed for selected narratives only; `unknown` elsewhere. |
| `assessment_scope` | `selected_narrative` or `inventory_only`. |
| `reported_new_sheets`, `reported_new_data_rows` | Selected reported additions; blank means not assessed, not zero. |
| `validation_scope`, `intervention`, `provenance_notes` | Conservative annotations, including recovery and unknown actors. |
| `source_sha256` | SHA-256 of the private report bytes at inventory time. |
| `inventory_date` | Date the inventory was assembled. |

Most entries are deliberately inventory-only. That avoids inferring success from a filename or a generic completion phrase. The two Avaya September 11 artifacts remain separate. Known blocked attempts have zero reported additions; an unassessed report has blank addition fields.

A SHA-256 digest lets the owner identify the exact source snapshot later. It does not authenticate a report's claims or give public reviewers access to private contents. Source locators below use only workflow names, dates, basenames, and line ranges; raw reports, identifiers, infrastructure details, and operational records are not published.

## Limits retained in the public narrative

The original report set is incomplete as an execution history. September inspections found destination updates with no corresponding local reporting provenance. Some reports overstate content verification or contradict subsequent findings. The selected narratives narrow those claims rather than treating a report as conclusive proof.

Neither the artifact total nor the reported additions provides an uptime denominator. No success-rate, labor-saving, ROI, universal data-preservation, or uninterrupted-operation claim is derived from this ledger.
