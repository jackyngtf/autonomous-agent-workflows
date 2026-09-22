# Claim index

[English](claim-index.md) · [繁體中文](claim-index.zh-TW.md) · [Evidence guide](README.md) · [Project overview](../../README.md)

Private source locators identify the reviewed snapshot. They are references for traceability, not links to publicly available raw operational reports. Public narratives are rewritten summaries.

| ID | Claim and evidence label | Private source locator | Public evidence and limitation |
|---|---|---|---|
| INV-20260922 | **Source inspection:** 47 Avaya and 45 NAS canonical run-report artifacts | Canonical monthly `reports/` inventories; report-name filters described in the guide | [Ledger](run-ledger.csv). Artifact count, not verified executions or unattended successes. |
| AVA-20260615 | **Reported outcome:** 14 rows added; eight previous sheets contained 182 data rows | `avaya_call_log_report_2026-06-15.md`, lines 59–64 | [Narrative](selected-run-extracts/README.md#ava-20260615--verification-before-cleanup). Pre-write content verification and post-upload counts are distinct checks. |
| NAS-20260625 | **Reported outcome:** content comparison caught duplicate headers before upload | `nas_access_log_report_2026-06-25.md`, lines 56–61 | [Narrative](selected-run-extracts/README.md#nas-20260625--two-matching-counts-were-both-wrong). A correction within one run; no failure-rate reduction inferred. |
| NAS-20260803 | **Reported outcome:** 23.6-second parse, 22.8-second write, 313,721 output data rows | `nas_access_log_report_2026-08-03.md`, lines 20–25 and 62 | [Narrative](selected-run-extracts/README.md#nas-20260803--changing-the-serialization-unit). Single-run observations; parse count includes headers. |
| AVA-20260810 | **Reported outcome:** two sheets / 36 rows added; malformed inputs retained | `avaya_call_log_report_2026-08-10.md`, lines 9–25 and 33–38 | [Narrative](selected-run-extracts/README.md#ava-20260810--valid-additions-malformed-inputs-retained). No claim that skipped inputs were resolved. |
| AVA-20260911 | **Reported outcome:** blocked scheduled session and later native recovery with 21 rows added | `avaya_call_log_report_2026-09-11_aborted.md`, lines 3 and 7–31; `avaya_call_log_report_2026-09-11.md`, lines 7–24 and 45–47 | [Narrative](selected-run-extracts/README.md#ava-20260911--a-blocked-session-and-a-separate-recovery). Native report does not establish an unattended scheduler trigger. |
| NAS-20260914 | **Reported outcome:** session aborted before authentication | `nas_access_log_report_2026-09-14.md`, lines 15–29 and 68 | [Narrative](selected-run-extracts/README.md#nas-20260914-and-nas-20260915--recoverable-data-and-visible-gaps). Current blocker and original August outage cause are not established as identical. |
| NAS-20260915 | **Reported outcome:** manual/native recovery added four sheets and 40,179 data rows | `nas_access_log_report_2026-09-15.md`, lines 3–4, 18–28 and 60–75 | [Narrative](selected-run-extracts/README.md#nas-20260914-and-nas-20260915--recoverable-data-and-visible-gaps). Historical gaps and unknown prior exporter remain visible. |
| VAL-20260915 | **Source inspection:** NAS recovery checks are narrower than full content equivalence | `step7c_validate_sep.py`, lines 21–29, 32–46 and 49–55 | [Integrity chapter](../case-study/03-integrity-and-verification.md). All-sheet counts; two sampled existing rows; complete date scan only for the weekend sheet. |
| RET-20260915 | **Unresolved:** no verified fixed retention duration | NAS September 15 report, lines 19, 64 and 70; learning `LRN-20260915-001` | Observed unavailable dates support a retrieval gap. The stated duration conflicts with the oldest returned date and is not published as a system specification. |
| KNOWLEDGE | **Design rule / source inspection:** incident findings can update operating instructions | NAS `SKILL.md`, lines 72–83; Avaya June 15 report, line 85 | [Lessons](../case-study/06-lessons-and-limitations.md). Document maintenance, not model training; no measured improvement rate. |

## Claims deliberately not carried forward

The reviewed files do not substantiate “60+ unattended runs each,” a continuous-success streak, a measured one-hour-to-seconds saving, a fixed safe recovery window, or universal byte-for-byte preservation. Their omission does not prove those claims impossible; it reflects the evidence available for this case study.

The offline demo has its own runnable code and tests. Historical rows in this table should not be relabeled “reproduced” merely because a synthetic example exercises a similar failure mode.
