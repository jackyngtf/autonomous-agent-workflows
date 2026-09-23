# Learning from incidents through written procedures

[**English**](self-improvement-loop.md) · [繁體中文](self-improvement-loop.zh-TW.md)

“Self-improvement” here means maintaining operational knowledge in files: record an incident, retrieve a relevant previous finding, and change the procedure when justified. It is not model training. The available record does not measure a reduced failure rate or guarantee that an error cannot recur.

## From observation to procedure

1. Record the symptom, date, workflow and execution environment.
2. Search for relevant prior findings and inspect the current evidence.
3. Separate the observed response from its suspected cause.
4. Record the attempted action, outcome and unresolved questions.
5. When justified, revise the procedure within authorised scope and check the changed behaviour.

For example, scanner-like content in a CSV is an observation. Identifying the remote actor or proving the complete cause needs further evidence. A procedure revision should link to its source incident and explain the changed rule. Recording a lesson is not permission to broaden write access, deletion or other policy boundaries.

## Selective retrieval

The intended pattern reads the current procedure in full and searches historical material when an error or uncertainty makes it relevant:

```sh
rg -n -i 'smb|STATUS_INVALID_PARAMETER' .learnings/
rg -n -i 'header|row count|validation' .learnings/
```

Read enough surrounding context to understand a match. A finding about one NAS version or API request is not a universal rule. The private `.learnings/` archive is not included in the public templates.

## Append-only history and consolidation

The historical procedure combined post-run appends with monthly merging, pruning and rotation. If consolidation deletes or rewrites the only copy of an entry, the archive is no longer a complete append-only history.

A clearer future retention model keeps original incident entries in retained or versioned history, marks superseded conclusions, and maintains current rules separately in the work instruction. Search summaries can be condensed while retaining links to source entries. Open questions remain visibly unresolved.

This is a recommendation, not a claim that the existing archive preserves every revision. A consolidation report is a recorded claim about that run, not an independent audit of retained and removed entries.

## Month-end and catch-up

The recorded design schedules document maintenance on the last working day of the month, accounting for Victorian public holidays, with catch-up after a missed month. An implementation needs to record the eligible month, attempt outcome and last successfully completed month. Failed attempts must not advance the completion marker.

Use `Australia/Melbourne` for date calculations; fixed UTC+10 does not represent the city throughout the year. Keep maintenance separate from workbook publication so a documentation failure does not trigger a duplicate export.

The [NAS report example](../examples/nas-access-log/sample-report.md) is now explicitly synthetic. It no longer claims that 29 July 2026 was July's last working day, and is not evidence that consolidation ran.

## Evidence of improvement

An incident case study can show the failure, procedure or code change, a check that detects the failure, and a later outcome with its execution mode and limits. Comparing failure rates additionally requires complete attempt records and comparable observation windows.

The supported portfolio claim is that incidents informed instructions and validation. The [offline demo](../demo/README.md) makes selected checks reproducible; it does not retrospectively validate production history.

Related: [architecture](architecture.md) · [runtime and evidence](how-it-runs-in-claude-code-cowork.md) · [examples](../examples/README.md).