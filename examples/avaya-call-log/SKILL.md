---
name: avaya-call-log
description: Avaya IP500 Call Log Export — read SMDR CSV files from a Dockerized PBX receiver, rebuild a monthly Excel workbook with xlsxwriter, upload via SMB, validate, and clean up processed CSVs. Runs weekdays at 10 AM.
---

# Avaya IP500 Call Log Automation

> 🔒 **Sanitized reference excerpt.** Mirrors the structure of a production agent. Realistic dummy values used — see [`WORKINSTRUCTION.md`](WORKINSTRUCTION.md) "What to change for your setup" to adapt.

You are running a scheduled task. No user is present. Follow all steps precisely.

## Pre-flight

**Read `WORKINSTRUCTION.md` in full — it is your complete operational ruleset** (Section 0 critical rules, Step 0 pre-flight, the full procedure, reference implementation, and troubleshooting). Follow it exactly.

Do **NOT** read the `.learnings/` files (`LEARNINGS.md`, `ERRORS.md`, `FEATURE_REQUESTS.md`) wholesale. They are append-only audit archives. Consult them via targeted `grep -rn "<keyword>" .learnings/` **only** when you hit an error, an unexpected result, or an uncertain decision (e.g. SMB connect fails → `grep -rn "smb"`; a CSV won't parse → `grep -rn "nul\|encoding"`).

Run **Step 0** of the work instruction first: it self-heals Python dependencies (`pysmb`) and runs the archive size guard that keeps `.learnings/` bounded.

## Working Directory

All work happens in: `<your-working-directory>/avaya-call-log`

Use Python for all file operations — SMB (`pysmb`) for NAS access, `csv` module for reading SMDR data.

## Key Rules

- Do **NOT** process today's CSV — only up to yesterday (Melbourne timezone, AEST UTC+10).
- Do **NOT** delete a CSV until its worksheet is confirmed in the uploaded workbook.
- Do **NOT** save or expose NAS passwords/credentials in reports.
- Do **NOT** overwrite valid worksheets.
- If SMB connection fails, stop and report clearly.
- **Never** use ZIP-level merge to modify XLSX workbooks. Always rebuild from scratch with `xlsxwriter`.
- Always use keyword arguments for the `pysmb` `SMBConnection` constructor.
- If user approval would be needed (e.g. overwrite), stop and produce the planned export table instead of modifying workbooks.

## Report

Save the final run report as:
`<your-working-directory>/avaya-call-log/reports/avaya_call_log_report_YYYY-MM-DD.md`

The report must include:
- **Run Summary** table (date/time, SMB connection result, CSVs found, workbooks processed, sheets added, CSVs deleted)
- **Export Summary** table (CSV File, Target Workbook, Worksheet, Rows, Status)
- **Skipped Items** section (today's CSV, already-existing sheets)
- **Issues / Open Questions** section

## Post-run

After completing the run (or if an error occurs), **append** any genuinely new learnings or errors to the `.learnings/` archives — append-only, never rewrite history. Do not duplicate existing entries. The Step 0 size guard keeps these files bounded, and the Step 9 month-end consolidation merges and prunes them.
