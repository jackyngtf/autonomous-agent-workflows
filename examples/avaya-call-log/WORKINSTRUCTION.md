# Avaya IP500 Call Log Automation — Work Instruction (Sanitized Excerpt)

> 🔒 **Sanitized.** Structural reference only — all IPs, hostnames, share paths, and credentials redacted. Code snippets use `<redacted>` placeholders where production values live.

## 0. Critical Rules — Read First

1. **Factual accuracy is paramount.** This task writes to production workbooks.
2. **No credentials in any output.** NAS passwords live in the vault — never in reports, `.md` files, or logs.
3. **Export only up to yesterday** (Melbourne/AEST, UTC+10). Today's CSV may be incomplete.
4. **Only create NEW worksheets.** Never overwrite, delete, rename, or move an existing worksheet.
5. **Never delete a CSV** until its worksheet is confirmed present in the uploaded workbook.
6. **Never use ZIP-level merge** to modify XLSX. Always rebuild from scratch with `xlsxwriter`.
7. **Validate twice** — locally after rebuild, AND by re-downloading from the NAS after upload.
8. **Stop and report** on any ambiguity that would need human approval.

## 1. Overview

The agent reads SMDR (Station Message Detail Recording) CSV files produced by a Dockerized Avaya IP Office 500 call-data receiver, groups them by target monthly workbook, rebuilds each workbook from scratch with `xlsxwriter`, uploads via SMB to a NAS, validates, and deletes successfully-processed source CSVs.

```
Dockerized SMDR receiver ──▶ daily CSVs on NAS
                                    │
                          agent (this task)
                                    │
            rebuild monthly XLSX ──▶ upload via SMB ──▶ validate ──▶ cleanup CSVs
```

## 2. NAS Connection & File Paths

### Connection Parameters

| Parameter | Value |
|---|---|
| SMB Server | `<redacted — see vault>` |
| SMB Port | `<redacted>` |
| Share | `<redacted>` |
| Username | `<redacted — see vault>` |
| Password | `<redacted — see vault>` |

```python
# Always use keyword arguments (a hard-won lesson: positional args silently mismatch)
from smb.SMBConnection import SMBConnection
conn = SMBConnection(
    username=<redacted>,
    password=<redacted>,
    my_name="agent",
    remote_name=<redacted>,
    use_ntlm_v2=True,
)
conn.connect(<redacted>, <redacted>)
```

## 3. Procedure

### Step 0 — Pre-flight: dependency self-heal + archive size guard

The runtime VM's filesystem resets between runs. Each run re-installs its own dependencies:

```python
import subprocess, sys
subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "pysmb"])
```

Then run the archive size guard: if `.learnings/*.md` exceed a threshold, flag it for the month-end consolidation (Step 9) to prune.

### Step 1 — Discover processable CSVs

List CSVs on the NAS share, filter to those dated **on or before yesterday** (Melbourne timezone). Group by `{(year, "MON"): [csv_names]}` to find the target workbook for each.

### Step 2 — Inspect existing workbooks

For each target workbook, read existing sheet names (openpyxl read-only) so we only add **missing** sheets.

### Step 3 — Validate CSVs and build export plan

Parse each CSV. Skip CSVs with NUL bytes / no valid SMDR rows — record them as corrupted (kept on NAS, never auto-deleted). Produce the export plan table.

### Step 4 — Rebuild workbook

```python
import xlsxwriter
workbook = xlsxwriter.Workbook(tmp_path)
# Re-write ALL existing sheets exactly (preserved), then add new sheets from validated CSVs
# ... per-sheet formatting ...
workbook.close()
```

### Step 5 — Upload workbook via SMB

```python
conn.storeFile(<redacted share>, remote_path, open(tmp_path, "rb"))
```

> **Hard-won lesson (LRN):** This NAS returns `STATUS_INVALID_PARAMETER` for `createDirectory` on an already-existing folder. Treat that failure as non-fatal — re-list and proceed; `storeFile` fails loudly if the folder is genuinely missing.

### Step 6 — Validate upload

Re-download the workbook from the NAS, open read-only, confirm new sheet names + row counts match the rebuild.

### Step 7 — Delete processed CSVs

Only after Step 6 confirms the sheet exists in the uploaded workbook. Corrupted CSVs are **never** deleted.

### Step 8 — Generate report

Write `reports/avaya_call_log_report_YYYY-MM-DD.md` (see `sample-report.md` for format).

### Step 9 — Month-end consolidation (conditional)

On the last working day of the month (Mon–Fri minus Victorian public holidays via `holidays` package, `subdiv='VIC'`), run a consolidation pass on `.learnings/`. Idempotent per month — a missed trigger day carries forward. See [`docs/self-improvement-loop.md`](../../docs/self-improvement-loop.md).
