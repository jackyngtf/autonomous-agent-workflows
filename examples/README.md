# Examples

Two sanitized reference implementations of the three-layer autonomous-agent architecture described in the [main README](../README.md).

Each example is **structurally faithful** to its production counterpart but has all identifiers removed:

- IP addresses → `<redacted>`
- Hostnames / share paths → `<redacted>`
- Credentials / tokens → `<redacted — see vault>`
- Company names → generic ("enterprise NAS", "PBX system")

## avaya-call-log

A scheduled agent (weekdays 10 AM) that reads call-data CSVs produced by a Dockerized PBX receiver, rebuilds a monthly Excel workbook, uploads it via SMB, validates, and cleans up.

- [`SKILL.md`](avaya-call-log/SKILL.md) — the entry-point file the scheduler loads
- [`WORKINSTRUCTION.md`](avaya-call-log/WORKINSTRUCTION.md) — the full operational procedure (trimmed & sanitized)
- [`sample-report.md`](avaya-call-log/sample-report.md) — a real run's structured output (sanitized)

## nas-access-log

A scheduled agent (weekdays 9 AM) that fetches file-transfer logs from a Synology NAS via REST API, rebuilds a monthly Excel workbook, uploads it via SMB, and validates.

- [`SKILL.md`](nas-access-log/SKILL.md) — the entry-point file
- [`WORKINSTRUCTION.md`](nas-access-log/WORKINSTRUCTION.md) — the full operational procedure (trimmed & sanitized)
- [`sample-report.md`](nas-access-log/sample-report.md) — a real run's structured output (sanitized)
