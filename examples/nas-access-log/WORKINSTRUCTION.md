# Synology NAS Access Log Automation — Work Instruction (Sanitized Excerpt)

> 🔒 **Sanitized.** Structural reference only — all IPs, hostnames, share paths, session tokens, and credentials redacted.

## 0. Critical Rules — Read First

1. **No credentials or session tokens in any output.** NAS passwords live in the vault.
2. **Export only up to yesterday** (Melbourne/AEST, UTC+10). Today's log may be incomplete.
3. **ONLY create NEW worksheets for missing dates.** Never overwrite/delete/rename existing sheets or NAS files.
4. **Never use ZIP-level merge or `openpyxl` to WRITE XLSX.** Always rebuild from scratch with `xlsxwriter`. (`openpyxl` read-only is fine for validation.)
5. **Use Python `requests` for ALL `entry.cgi` API calls** (curl fails with error 105). Do NOT pass `enable_syno_token` when authenticating.
6. **Validate twice** — locally after rebuild, AND by re-downloading from the NAS after upload. Keep rebuild and validation in SEPARATE bash calls (each ~20–32 s; combined exceeds the 45 s timeout).
7. **Stop and report** on any ambiguity needing human approval.

## 1. Overview

The agent authenticates to a Synology NAS (DSM 6.2.4), fetches file-transfer logs via the SyslogClient REST API (`logtype=cifs`, 1-hour windows, `limit=50000`), groups records by business day, rebuilds a monthly Excel workbook with `xlsxwriter`, uploads via SMB, and validates.

```
Synology NAS ──REST API──▶ agent ──▶ rebuild monthly XLSX ──SMB upload──▶ validate
```

## 2. Auth (REST API)

Three-stage Synology auth flow, all via `requests`:

```python
import requests
BASE = "<redacted>"          # e.g. https://<nas>:<port>/webapi

# 1. Login — do NOT pass enable_syno_token
r = requests.get(f"{BASE}/auth.cgi", params={
    "api": "SYNO.API.Auth", "version": "3", "method": "login",
    "account": "<redacted>", "passwd": "<redacted>", "session": "FileStation",
}).json()
sid = r["data"]["sid"]

# 2. Use SyslogClient to fetch file-transfer logs
#    logtype=cifs, 1-hour time windows, limit=50000
# 3. Logout
```

> **Lesson (LRN):** curl fails on `entry.cgi` with error 105. Always use Python `requests`.

## 3. Business-day logic

```python
import holidays
vic_holidays = holidays.country_holidays("AU", subdiv="VIC", years=<year ± 1>)

def is_business_day(d):
    return d.weekday() < 5 and d not in vic_holidays
```

Group consecutive non-working days **within the same month** as one `DD-DD` sheet. Never cross a month boundary. Never create an empty worksheet for a zero-row date — stop and report it.

## 4. Procedure

- **Step 0** — Pre-flight: self-heal `requests`/`pysmb`/`holidays` (VM filesystem resets between runs) + archive size guard.
- **Step 1** — Auth + discover latest covered date in the existing workbook.
- **Step 2** — Fetch file-transfer logs for each missing business day via SyslogClient (1-hour windows, `limit=50000`).
- **Step 3** — Build export plan (date/range → worksheet → rows).
- **Step 4** — Rebuild the ENTIRE workbook from scratch with `xlsxwriter` (all existing sheets preserved exactly + new sheets added).
- **Step 5** — Upload via SMB (`pysmb`, keyword args).
- **Step 6** — Validate: re-download from NAS, confirm sheet names + row counts.
- **Step 7** — Generate report (`reports/nas_access_log_report_YYYY-MM-DD.md`).

## 5. Month-end consolidation (Step 11, conditional)

On the last working day of the month, AFTER the NAS export and main report are complete, run a consolidation pass on `.learnings/` (merge duplicates, prune superseded, promote durable rules to this file, rotate >90-day entries to `.learnings/archive/`). A consolidation failure must not affect the already-completed export. Idempotent per month with carry-forward catch-up. See [`docs/self-improvement-loop.md`](../../docs/self-improvement-loop.md).
