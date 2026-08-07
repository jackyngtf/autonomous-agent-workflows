# Examples

Two sanitized reference implementations of the three-layer autonomous-agent architecture described in the [main README](../README.md).

Each example is **structurally faithful** to its production counterpart, but uses **realistic dummy values** (IPs `192.168.1.100`, account `svc_calllog` / `svc_naslog`, share `shared`) instead of real identifiers. Every example has a **"What to change for your setup"** table at the top of its `WORKINSTRUCTION.md` showing exactly what to swap for your own environment.

## avaya-call-log

A scheduled agent (weekdays 10 AM) that reads call-data CSVs produced by a Dockerized PBX receiver, rebuilds a monthly Excel workbook, uploads it via SMB, validates, and cleans up.

- [`SKILL.md`](avaya-call-log/SKILL.md) — the entry-point file the scheduler loads
- [`WORKINSTRUCTION.md`](avaya-call-log/WORKINSTRUCTION.md) — the full operational procedure (sanitized)
- [`sample-report.md`](avaya-call-log/sample-report.md) — a real run's structured output (sanitized)

## nas-access-log

A scheduled agent (weekdays 9 AM) that fetches file-transfer logs from a Synology NAS via REST API, rebuilds a monthly Excel workbook, uploads it via SMB, and validates.

- [`SKILL.md`](nas-access-log/SKILL.md) — the entry-point file
- [`WORKINSTRUCTION.md`](nas-access-log/WORKINSTRUCTION.md) — the full operational procedure (sanitized)
- [`sample-report.md`](nas-access-log/sample-report.md) — a real run's structured output (sanitized)

## See also

Realistic dummy input data and a **runnable offline demo** of the rebuild step are in [`sample-data/`](../sample-data/).
