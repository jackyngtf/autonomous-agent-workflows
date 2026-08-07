# Autonomous Agent Workflows

> How I run **scheduled, fully unattended LLM-agent tasks** that do real work every morning — and get better at it over time.

Two agents built on this pattern run **daily in production** (weekdays 9 AM and 10 AM), exporting call logs and file-transfer logs to monthly Excel workbooks on a NAS. They've completed 60+ runs each.

---

## What it actually does (concrete example)

```
Every weekday at 10 AM ──▶ agent wakes up (no human)
        │
        │  1. reads SMDR call-record CSVs produced overnight by a Dockerized PBX receiver
        │  2. rebuilds a monthly Excel workbook from scratch (xlsxwriter)
        │  3. uploads it to a NAS share via SMB
        │  4. re-downloads it to validate (sheet names + row counts match)
        │  5. deletes the now-processed source CSVs
        │  6. writes a structured run report
        │
        ▼
   monthly call-log workbook on the NAS, one worksheet per day
```

**Input** (a daily CSV from the PBX receiver — see [`sample-data/`](sample-data/smdr-receiver/output/smdr_2026-08-04.csv)):

```
Call Start,Connected Time,Ring Time,Caller,Direction,Called Number,...
2026-08-04 09:03:11,42,3,0298765432,Incoming,9333,...
2026-08-04 10:05:54,204,5,0400123456,Outgoing,,0400123456,...
```

**Output** (a monthly Excel workbook — one worksheet per day, rebuilt every run):

| Worksheet | Rows |
|-----------|-----:|
| `2026-08-04` | 13 |
| `2026-08-05` | 11 |
| … | … |

You can run this rebuild step yourself right now — no NAS, no credentials needed:

```bash
cd sample-data
pip install xlsxwriter openpyxl
python3 rebuild_workbook_demo.py
# → writes AUG_2026_demo.xlsx, validates it (13 rows, 32 cols)
```

The second agent (9 AM) does the same loop but for Synology NAS **file-transfer logs** — it authenticates via REST API, fetches `cifs` event records, and produces a monthly access-log workbook. See [`sample-data/nas-syslog/`](sample-data/nas-syslog/nas_access_records_2026-08-04.json) for the input format.

---

## Why this isn't just a cron job

A plain script does steps 1–6 and stops. These agents **also learn from their own mistakes**:

- Every run appends errors and insights to an append-only archive (`.learnings/`)
- On the next run, when something goes wrong, the agent **greps the archive** and applies the prior fix instead of repeating the failure
- Once a month, the agent **consolidates its own knowledge** — merges duplicates, prunes stale entries, promotes durable rules into the operational procedure

So a failure that cost an hour to diagnose the first time costs seconds every time after.

---

## The three-layer architecture

```
                    ┌─────────────────────────────────────────┐
   Scheduler ─────▶ │  SKILL.md        (entry point)          │
  (daily 9/10 AM)   │  the minimal "how to start" contract    │
                    └────────────────────┬────────────────────┘
                                         │ read in full
                                         ▼
                    ┌─────────────────────────────────────────┐
                    │  WORKINSTRUCTION.md  (operational truth) │
                    │  step-by-step procedure + critical rules │
                    │  THIS is the authoritative ruleset       │
                    └────────────────────┬────────────────────┘
                                         │ consult on errors only
                                         ▼
                    ┌─────────────────────────────────────────┐
                    │  .learnings/       (append-only archive) │
                    │  LEARNINGS.md  ERRORS.md  FEATURE_*.md   │
                    │  grep-only — NEVER read wholesale        │
                    └─────────────────────────────────────────┘
```

| Layer | File | Read when | Written when |
|-------|------|-----------|--------------|
| **Entry** | `SKILL.md` | Every run (start) | Rarely — stable contract |
| **Truth** | `WORKINSTRUCTION.md` | Every run (in full) | When an operational rule changes |
| **Archive** | `.learnings/*.md` | **Only via `grep`** on error/uncertainty | After every run (append-only) |

The key insight: **the archive is for audit, the work-instruction is for operations.** New knowledge gets written to both — the archive entry is the history, the work-instruction edit is the living rule.

📖 Deep dives: [`docs/architecture.md`](docs/architecture.md) · [`docs/self-improvement-loop.md`](docs/self-improvement-loop.md)

---

## Repository contents

```
sample-data/                 ← realistic dummy inputs + a runnable demo
  smdr-receiver/output/      ← daily SMDR CSV (what the PBX receiver writes)
  nas-syslog/                ← NAS file-transfer log records (JSON)
  rebuild_workbook_demo.py   ← run this to see the rebuild step work, offline

examples/                    ← sanitized reference implementations
  avaya-call-log/            ← SKILL.md + WORKINSTRUCTION.md + sample-report.md
  nas-access-log/            ← SKILL.md + WORKINSTRUCTION.md + sample-report.md

docs/                        ← the architecture & patterns explained
  architecture.md
  self-improvement-loop.md
```

Each example uses **realistic dummy values** for everything (IPs `192.168.1.100`, account `svc_calllog`, share `shared`). Every example doc has a **"What to change for your setup"** table showing exactly what to swap to run it against your own environment.

---

## Safety invariants baked into every run

- **Never expose credentials** — passwords/tokens live in a vault, never in a report or `.md`
- **Never overwrite** existing data without explicit approval — only create new entries
- **Export only up to yesterday** (Melbourne/AEST) — today's data may be incomplete
- **Never delete** a processed input until its output is confirmed in the uploaded file
- **Validate twice** — rebuild locally AND re-download from the NAS after upload
- **Stop and report** on any ambiguity that would need human approval — don't guess

---

## Results in production

- ✅ 60+ unattended daily runs per agent, across two agents
- ✅ Self-healing dependencies (the runtime VM's filesystem resets between runs; each run re-installs its own packages)
- ✅ Detects and tracks recurring anomalies (corrupted CSVs from an external port scanner) across 41 consecutive runs without crashing
- ✅ Month-end consolidation runs on schedule with cross-month catch-up
- ✅ Every run emits a structured markdown report

---

## Tech stack

`Python` · `xlsxwriter` · `pysmb` (SMB upload) · `requests` (Synology REST API) · `holidays` (deterministic business-day logic) · Docker (SMDR receiver) · markdown-driven agent runtime

---

## License

MIT — the architecture and patterns here are free to adapt. The reference implementations are sanitized excerpts from production work.
