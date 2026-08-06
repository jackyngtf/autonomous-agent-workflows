---
name: nas-access-log
description: Synology NAS Access Log Export — fetch file-transfer logs via SyslogClient REST API, rebuild a monthly Excel workbook with xlsxwriter, upload via SMB, and validate. Runs weekdays at 9 AM.
---

# Synology NAS Access Log Automation

> 🔒 **Sanitized reference excerpt.** All IPs, hostnames, share paths, and credentials have been redacted. This mirrors the structure of a production agent.

You are running a scheduled task. No user is present. Follow all steps precisely.

## Pre-flight

Before doing anything else, read and follow the complete work instruction:

`<working-directory>/nas-access-log/WORKINSTRUCTION.md`

That file is your **complete operational ruleset** — its Section 0 (Critical Rules) plus the step-by-step procedure contains ALL the details: NAS connection parameters, REST API endpoints, SMB share paths, code examples, troubleshooting, and safety constraints. Its **Step 0** runs BOTH the dependency check AND the archive size guard. Follow it exactly, starting at Step 0.

**Do NOT read the `.learnings/` files wholesale.** They are append-only audit archives whose operational conclusions are already distilled into `WORKINSTRUCTION.md`. Consult them only via targeted `grep` when you hit an error, an unexpected result, or an uncertain decision:

```
grep -rn "auth" .learnings/
grep -rn "smb\|upload" .learnings/
```

## Working Directory

All work happens in: `<working-directory>/nas-access-log/`

Use Python for all operations — `requests` for Synology REST API calls (auth, File Station, SyslogClient), and `pysmb` for the workbook upload. No browser automation.

## Key Rules

- Do **NOT** export today's records — only up to yesterday (Melbourne timezone, AEST UTC+10). Today's log may be incomplete.
- Use `Australia/Melbourne` timezone for all date logic.
- **ONLY create NEW worksheets for missing dates.** Do NOT overwrite, delete, rename, or move any existing worksheet or NAS file.
- Business days = Mon–Fri, excluding Victorian public holidays. Determine holidays deterministically with the Python `holidays` package (`subdiv='VIC'`) — do NOT guess. Group consecutive non-working days within the same month as one `DD-DD` sheet; never cross a month boundary.
- Do NOT create an empty worksheet for a date with zero matching rows — stop and report it.
- Do NOT save or expose NAS passwords/credentials or session tokens in reports.
- **Never** use ZIP-level merge or `openpyxl` to modify/write XLSX workbooks. Always rebuild the ENTIRE workbook from scratch with `xlsxwriter`, preserving all existing sheets exactly. (`openpyxl` read-only is fine for reading/validating.)
- Use Python `requests` for ALL `entry.cgi` API calls (curl fails with error 105). Do NOT pass `enable_syno_token` when authenticating. For SyslogClient use `logtype=cifs`, 1-hour time windows, `limit=50000`.
- Always use keyword arguments for the `pysmb` `SMBConnection` constructor.
- **Validate the rebuilt file locally AND re-download it from the NAS after upload** to confirm sheet names and row counts. Keep the rebuild pass and the validation read in SEPARATE bash calls.
- If auth fails, NAS access fails, or a pre-flight check fails, stop and report clearly.

## Report

Save the final run report as:
`<working-directory>/nas-access-log/reports/nas_access_log_report_YYYY-MM-DD.md`

The report must include:
- **Run Summary** table (date/time, auth result, pre-flight result, latest covered date, missing dates, sheets added, upload + validation result)
- **Export Summary** table (Date/Range, Target Workbook, Worksheet, Rows, Status)
- **Skipped Items** section (today's date, already-covered dates, zero-row dates)
- **Issues / Open Questions** section

## Month-end consolidation (conditional, same session)

On the **last working day of the month** (Melbourne timezone — Mon–Fri excluding Victorian public holidays), AFTER the NAS export and main report are complete, also run **WORKINSTRUCTION.md Step 11** — a consolidation pass on the `.learnings/` archive. A consolidation failure must not affect the already-completed NAS export.

## Post-run

After completing the run (or if an error occurs), capture genuinely new knowledge:

- If a NEW error or insight occurred, append a TERSE entry to `.learnings/ERRORS.md` or `.learnings/LEARNINGS.md`.
- If the new knowledge changes HOW the task should run operationally, ALSO update `WORKINSTRUCTION.md` — that file is the always-read ruleset.
- Do NOT read the `.learnings/` archives wholesale to decide whether an entry is new — use targeted `grep` instead.
