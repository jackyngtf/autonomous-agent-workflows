# Avaya IP500 Call Log Automation — Work Instruction (Reference Excerpt)

> 🔒 **Sanitized reference.** Based on a production work-instruction. All IPs, hostnames, share paths, and credentials are **realistic dummy values** — swap them for your own environment using the config table below. See [`sample-report.md`](sample-report.md) for a real run's output.

## What to change for your setup

| Variable | Dummy value in this doc | What it is |
|---|---|---|
| `192.168.1.100` | NAS IP | Your Synology NAS IP |
| `DEMO-NAS` | SMB server name | Your NAS hostname |
| `shared` | SMB share name | The share where workbooks live |
| `svc_calllog` | service account | A dedicated account with Read/Write on the share |
| `/shared/reports/call-logs/...` | workbook path | Where monthly workbooks are stored |
| `9000` | SMDR receiver port | The TCP port your `smdr-receiver` container listens on |

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

The agent reads SMDR (Station Message Detail Recording) CSV files produced by a Dockerized Avaya IP Office 500 call-data receiver ([github.com/jackyngtf/smdr-receiver](https://github.com/jackyngtf/smdr-receiver)), groups them by target monthly workbook, rebuilds each workbook from scratch with `xlsxwriter`, uploads via SMB to a NAS, validates, and deletes successfully-processed source CSVs.

```
Dockerized SMDR receiver ──▶ daily CSVs on NAS
                                    │
                          agent (this task)
                                    │
            rebuild monthly XLSX ──▶ upload via SMB ──▶ validate ──▶ cleanup CSVs
```

### Input format

A daily SMDR CSV (`smdr_YYYY-MM-DD.csv`). First row is the Avaya IP Office SMDR header (29 columns):

```
Call Start,Connected Time,Ring Time,Caller,Direction,Called Number,Dialled Number,Account,Is Internal,Call ID,Continuation,Party1Device,Party1Name,Party2Device,Party2Name,Hold Time,Park Time,AuthValid,AuthCode,UserCharged,CallCharge,Currency,AmountAtLastUserChange,CallUnits,UnitsAtLastUserChange,CostPerUnit,MarkUp,ExternalTargetingCause,ExternalTargeterId,ExternalTargetedNumber
2026-08-04 09:03:11,42,3,0298765432,Incoming,9333,,1001,N,18455,0,"Ext 333","Reception","9333","Main Line",0,0,0,,,,0.00,AUD,...
```

See [`sample-data/smdr-receiver/output/smdr_2026-08-04.csv`](../../sample-data/smdr-receiver/output/smdr_2026-08-04.csv) for a full example.

## 2. NAS Connection & File Paths

### Connection Parameters

| Parameter | Value |
|---|---|
| SMB Server | `192.168.1.100` |
| SMB Port | `445` |
| Share | `shared` |
| Username | `svc_calllog` |
| Password | *(from vault — never written here)* |

```python
# Always use keyword arguments (a hard-won lesson: positional args silently mismatch
# because the pysmb SMBConnection parameter order changed in 1.2.14)
from smb.SMBConnection import SMBConnection
conn = SMBConnection(
    username="svc_calllog",
    password=<password from vault>,
    my_name="agent",
    remote_name="DEMO-NAS",
    use_ntlm_v2=True,
)
conn.connect("192.168.1.100", 445)
```

**Workbook path on NAS:**
```
/shared/reports/call-logs/{Year}/{MON}.xlsx
```
where `{Year}` is four-digit year and `{MON}` is the three-letter uppercase month (JAN, FEB, …).

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

The core step. **Always rebuild from scratch with `xlsxwriter`** — never ZIP-merge or openpyxl-write. A minimal version of this rebuild logic is in [`sample-data/rebuild_workbook_demo.py`](../../sample-data/rebuild_workbook_demo.py) (runnable offline).

```python
import xlsxwriter
workbook = xlsxwriter.Workbook(tmp_path)
# Re-write ALL existing sheets exactly (preserved), then add new sheets from validated CSVs
workbook.close()
```

### Step 5 — Upload workbook via SMB

```python
conn.storeFile("shared", "reports/call-logs/2026/AUG.xlsx", open(tmp_path, "rb"))
```

> **Hard-won lesson:** This NAS returns `STATUS_INVALID_PARAMETER` for `createDirectory` on an already-existing folder. Treat that failure as non-fatal — re-listPath and proceed; `storeFile` fails loudly if the folder is genuinely missing.

### Step 6 — Validate upload

Re-download the workbook from the NAS, open read-only, confirm new sheet names + row counts match the rebuild.

### Step 7 — Delete processed CSVs

Only after Step 6 confirms the sheet exists in the uploaded workbook. Corrupted CSVs are **never** deleted.

### Step 8 — Generate report

Write `reports/avaya_call_log_report_YYYY-MM-DD.md` (see [`sample-report.md`](sample-report.md) for format).

### Step 9 — Month-end consolidation (conditional)

On the last working day of the month (Mon–Fri minus Victorian public holidays via `holidays` package, `subdiv='VIC'`), run a consolidation pass on `.learnings/`. Idempotent per month — a missed trigger day carries forward. See [`docs/self-improvement-loop.md`](../../docs/self-improvement-loop.md).
