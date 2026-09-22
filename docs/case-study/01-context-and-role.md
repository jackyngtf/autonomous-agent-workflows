# 01 · Context and role

[English](01-context-and-role.md) · [繁體中文](01-context-and-role.zh-TW.md) · [Project overview](../../README.md)

Two recurring reporting tasks connected operational systems to the format people already used: monthly Excel workbooks. One collected PBX call records from daily CSV files. The other collected NAS file-transfer events through an API. Both required decisions about completed dates, existing coverage, malformed input, and whether an updated workbook was safe to publish.

I developed the operating instructions, the Python processing approach, and the reporting and exception-handling rules around these tasks. The work included adapting the procedure after workbook defects, execution limits, and unavailable runtime environments appeared in the operating record.

## What I owned

| Area | Contribution |
|---|---|
| Workflow design | Define the eligible inputs, date boundaries, output structure, and stop conditions. |
| Integration | Connect existing CSV/API sources to workbook processing and NAS publication. |
| Integrity | Establish checks before reconstruction, before upload, and after downloading the published copy. |
| Operations | Capture run outcomes and incidents; turn useful findings into revised instructions. |
| Portfolio | Publish sanitized explanations and a synthetic, offline demonstration that a reviewer can inspect. |

The project builds on existing PBX/NAS systems, Claude's execution tools, and Python libraries. I did not build the underlying language model or the scheduling platform. The receiver that creates the call CSVs is a separate component.

## Where the agent fits

The agent reads the procedure, inspects the situation, invokes deterministic processing, and responds to exceptions. Python handles parsing, grouping, reconstruction, and comparisons. Scheduling starts a session; the useful agent behavior is its handling of evidence and operational decisions within written boundaries.

This arrangement was useful while the procedures were evolving and unusual failures needed investigation. Stable processing rules belong in reusable functions and tests. An instruction document alone cannot enforce every safety condition.

The portfolio also documents the [eTMS scheduled handoff](07-etms-document-handoff.md), which assigns file replacements to a separate engine. The retained entry instructions support a discussion of the job's scope and operator-controlled modes; they do not establish engine authorship, deployment or successful executions.

## What this case study establishes

The available record contains dated reports, failure notes, instruction changes, and recovery helpers. It supports specific examples of successful additions, blocked runs, and changes to validation. It does not establish continuous uptime, a measured labor-saving figure, or fully unattended recovery.

The public repository demonstrates the design without exposing operational records or requiring access to the original systems. Historical outcomes and the current offline demo are kept separate in the [evidence index](../evidence/README.md).

[Next: the two workflows](02-two-reporting-workflows.md)
