# How the scheduled workflow runs

[**English**](how-it-runs-in-claude-code-cowork.md) · [繁體中文](how-it-runs-in-claude-code-cowork.zh-TW.md)

The original setup used Claude Cowork scheduled tasks: NAS access logs at 09:00 and Avaya call logs at 10:00 on weekdays. The procedure uses `Australia/Melbourne` for report dates. Configured schedules do not prove that every expected attempt started or completed.

The [eTMS entry contract](../examples/etms-doc-swap/README.md) specifies a third weekday task at 09:30, with no timezone stated in the inspected file. A [22 September 2026 read-only deployment review](evidence/etms-deployment-review-2026-09-22.md) confirmed external driver, engine and configuration files, with mode set to shadow. Source inspection found that shadow still performs inbox housekeeping and report uploads, and that the driver can exit zero without establishing engine success. This task does not follow the workbook sequence below. The assessed user-triggered Cowork report records 30 HELD and 0 SWAPPED. It must be distinguished from a scheduler-triggered run and from the separate offline repair checks and later verified deployment. A subsequent manual Cowork run reported 19 PLANNED, 8 HELD and 0 SWAPPED on a 27-input subset of the earlier 30; it does not establish scheduler-triggered success.

Some historical files called this “Claude Code Cowork.” This portfolio distinguishes Cowork scheduled sessions from later native Windows recovery work. A manual Claude Code or shell session is not counted as an unattended scheduled success.

## The recorded configuration

The retained screenshots show this project's historical setup, not instructions for a current product version.

| Field | Role in this project |
|---|---|
| Instructions | Entry text corresponding to `SKILL.md`, pointing to the detailed procedure |
| Folders | Working files, instructions and reports available to the task |
| Repeats | Weekday start time |
| Allowed tools | File and shell operations available without interactive approval |
| Run history | Runtime status to compare with reports and output artifacts |

Historical captures: [Avaya task](../images/cowork-avaya-task-detail.png) · [NAS task](../images/cowork-nas-task-detail.png).

The thin entry instructions separate scheduler configuration from an evolving procedure. Editing the work instruction changes what a future session reads; it does not prove that an already-running session used that revision.

## Expected session sequence

1. Read the current procedure and establish permitted scope.
2. Check dependencies, date cutoff and required access.
3. Inspect source and destination; plan missing completed dates.
4. Build a candidate workbook and validate it before publication.
5. In a live deployment, publish, retrieve and validate the remote copy before considering source cleanup.
6. Report the outcome and record new observations.

Some recorded sandbox sessions needed dependencies reinstalled. This is an environment observation, not a universal runtime guarantee. Reproducible setup should declare compatible dependencies and fail clearly if installation cannot complete. The public demo uses local Python and requires no scheduler.

Scheduling does not make processing adaptive or enforce written safety rules. The agent follows the procedure, investigates exceptions and explains corrections. Deterministic checks belong in code where possible. Tool permissions still need limits appropriate to the data being modified.

## Interpreting the operating record

| Source | Useful for | Limitation |
|---|---|---|
| Runtime history | Recorded attempts and runtime status | Does not independently validate workbook contents |
| Run report | Claimed inputs, actions, checks and unresolved issues | Can omit attempts or contain mistakes |
| Source and output artifacts | Inspecting records and destination coverage | May have changed since the report |

Later records include startup failures, interrupted work and native recovery. Preserve those distinctions. A recovered output demonstrates a recovery outcome; it does not turn a missed scheduled attempt into an unattended success. If the source of a destination update is unknown, its provenance remains unknown.

A ledger should record one row per attempt, including execution mode, outcome, validation scope and report source. Report-file counts alone cannot establish uptime or unattended-run totals.

## Reproducing the public example

Use the [offline demo](../demo/README.md) to exercise both workflows with local synthetic files. No NAS credentials, source deletion or agent account is involved. The [reference instructions](../examples/README.md) describe the live design, not a complete deployment.

Operational adaptation would require an owner to define source schemas, permissions, credential delivery, scheduler timezone, retention limits, concurrency controls and recovery for that environment. Project-specific API or runtime observations need verification there.

Related: [architecture](architecture.md) · [knowledge maintenance](self-improvement-loop.md) · [main portfolio](../README.md).
