# Synology NAS Access Log Automation — Work Instruction (Reference Excerpt)

> 🔒 **Sanitized reference.** Based on a production work-instruction. All IPs, hostnames, share paths, and credentials are **realistic dummy values** — swap them for your own environment using the config table below.

## What to change for your setup

| Variable | Dummy value in this doc | What it is |
|---|---|---|
| `192.168.1.100` | NAS IP | Your Synology NAS IP |
| `DEMO-NAS` | SMB server name | Your NAS hostname |
| `5000` | web port | Your DSM web port |
| `shared` | SMB share name | The share where workbooks live |
| `svc_naslog` | service account | A dedicated account that's a member of `administrators` (needed for Log Center API) |
| `/shared/reports/access-logs/...` | workbook path | Where monthly workbooks are stored |
| `DSM 7.2` | DSM version | Your Synology DSM version |

## 0. Critical Rules — Read First

1. **No credentials or session tokens in any output.** NAS passwords live in the vault.
2. **Export only up to yesterday** (Melbourne/AEST, UTC+10). Today's log may be incomplete.
3. **ONLY create NEW worksheets for missing dates.** Never overwrite/delete/rename existing sheets or NAS files.
4. **Never use ZIP-level merge or `openpyxl` to WRITE XLSX.** Always rebuild from scratch with `xlsxwriter`. (`openpyxl` read-only is fine for validation.)
5. **Use Python `requests` for ALL `entry.cgi` API calls** (curl fails with error 105 / "noprivilege"). Do NOT pass `enable_syno_token` when authenticating.
6. **Validate twice** — locally after rebuild, AND by re-downloading from the NAS after upload. Keep rebuild and validation in SEPARATE bash calls (each ~20–32 s at production scale; combined exceeds a 45 s timeout).
7. **Stop and report** on any ambiguity needing human approval.

## 1. Overview

The agent authenticates to a Synology NAS (DSM 7.2), fetches file-transfer logs via the SyslogClient REST API (`logtype=cifs`, 1-hour windows, `limit=50000`), groups records by business day, rebuilds a monthly Excel workbook with `xlsxwriter`, uploads via SMB, and validates.

```
Synology NAS ──REST API──▶ agent ──▶ rebuild monthly XLSX ──SMB upload──▶ validate
```

### Input format

Synology SyslogClient returns `cifs` event records (file-transfer log entries). Each record looks like:

```json
{
  "UTC": "2026-08-03T23:05:12+00:00",
  "Account": "jsmith",
  "Event": "cifs:connect",
  "Share": "shared",
  "Path": "/shared/Projects/Q3-Report.pptx",
  "File size": "2456320",
  "Action": "write",
  "From": "10.20.30.41 (WS-JSMITH)"
}
```

See [`sample-data/nas-syslog/nas_access_records_2026-08-04.json`](../../sample-data/nas-syslog/nas_access_records_2026-08-04.json) for a full example.

## 2. NAS Connection Details

| Parameter | Value |
|---|---|
| IP | `192.168.1.100` |
| Web Portal | `http://192.168.1.100:5000` |
| Username | `svc_naslog` *(must be in `administrators` group — Log Center API requires it)* |
| Password | *(from vault — never written here)* |
| SMB Server Name | `DEMO-NAS` |
| SMB Share | `shared` |
| DSM Version | `7.2` |

> **Service account note:** the Log Center API (`SYNO.Core.SyslogClient.Log`) only lets administrators read logs, so a `users`-only account fails the log-fetch step. Use a dedicated service account in the `administrators` group with Read/Write on the share.

**Workbook path on NAS:**
```
/shared/reports/access-logs/{Year}/{MON}.xlsx
```

## 3. Auth (REST API)

Three-stage Synology auth flow, all via `requests`:

```python
import requests
BASE = "http://192.168.1.100:5000/webapi"

# 1. Login — do NOT pass enable_syno_token (it breaks entry.cgi auth)
r = requests.get(f"{BASE}/auth.cgi", params={
    "api": "SYNO.API.Auth", "version": "6", "method": "login",
    "account": "svc_naslog", "passwd": <password from vault>,
    "format": "sid",
}).json()
sid = r["data"]["sid"]

# 2. Use SyslogClient to fetch file-transfer logs
#    logtype=cifs is the ONLY value that returns file transfer records
#    Use 1-hour time windows (multi-day ranges return unfiltered results)
#    Use limit=50000 (pagination 'start' offset is broken — ignored by the API)
# 3. Logout
```

> **Lesson (LRN):** curl fails on `entry.cgi` with error 105 / "noprivilege". Always use Python `requests`. And `logtype=cifs` is the only value that returns file-transfer records — `"filetransfer"`, `"smb"`, `"ftp"` all return 0 results.

## 4. Business-day logic

```python
import holidays
vic_holidays = holidays.country_holidays("AU", subdiv="VIC", years=<year ± 1>)

def is_business_day(d):
    return d.weekday() < 5 and d not in vic_holidays
```

Group consecutive non-working days **within the same month** as one `DD-DD` sheet. Never cross a month boundary. Never create an empty worksheet for a zero-row date — stop and report it.

## 5. Procedure

- **Step 0** — Pre-flight: self-heal `requests`/`pysmb`/`xlsxwriter`/`holidays` (VM filesystem resets between runs) + archive size guard.
- **Step 1** — Auth + discover latest covered date in the existing workbook.
- **Step 2** — Fetch file-transfer logs for each missing business day via SyslogClient (1-hour windows, `limit=50000`, `logtype=cifs`).
- **Step 3** — Build export plan (date/range → worksheet → rows).
- **Step 4** — Rebuild the ENTIRE workbook from scratch with `xlsxwriter` (all existing sheets preserved exactly + new sheets added).
- **Step 5** — Upload via SMB (`pysmb`, keyword args).
- **Step 6** — Validate: re-download from NAS, confirm sheet names + row counts.
- **Step 7** — Generate report (`reports/nas_access_log_report_YYYY-MM-DD.md`).

## 6. Month-end consolidation (Step 11, conditional)

On the last working day of the month, AFTER the NAS export and main report are complete, run a consolidation pass on `.learnings/` (merge duplicates, prune superseded, promote durable rules to this file, rotate >90-day entries to `.learnings/archive/`). A consolidation failure must not affect the already-completed export. Idempotent per month with carry-forward catch-up. See [`docs/self-improvement-loop.md`](../../docs/self-improvement-loop.md).
