# eTMS document replacement: scheduled handoff

[**English**](README.md) · [繁體中文](README.zh-TW.md)

This third workflow hands document replacement to a separately deployed engine. Its available entry instructions specify an unattended weekday task at **09:30**: inspect an incoming-document folder, obtain the deployed engine and driver from an external store, run under the configured mode, then explain the result.

The source does not specify the schedule timezone. A read-only inspection on **22 September 2026** confirmed deployed driver, engine and configuration files, with the captured mode set to **shadow**. Their source was reviewed without executing the operational code. A separately assessed user-triggered shadow report recorded 30 HELD, 0 PLANNED and 0 SWAPPED. This is an observed held result, not a successful replacement or scheduler-triggered success.

## What the agent is responsible for

The agent checks that the required deployed files exist, invokes the driver within the authorised configuration, and reads the driver's JSON output and report. It should describe which inputs were planned, replaced or held, why an item was held, and what requires attention.

The agent must not perform ad hoc file swaps, connect to a database, execute SQL, change training records or switch itself from shadow to live mode. Changes are limited to files in the engine's plan and its designated archives, logs and reports, through the engine or driver.

## What remains delegated

| Item | Evidence boundary |
|---|---|
| Shadow mode | Captured configuration selects shadow. The source skips production-document swaps but still performs inbox housekeeping and report uploads; it is not free of remote changes. |
| Live mode | Selected by the responsible operator through configuration, not by the scheduled agent; no live outcome is claimed here. |
| Replacement and rollback | Delegated engine responsibilities. Static review does not establish successful replacement, rollback or recovery under failure. |
| Manifest | The contract refers to a file manifest derived from a static SQL snapshot; this does not authorise database connections or SQL execution |
| Result reporting | The driver does not propagate the first engine subprocess status and returns zero in shadow. Completion and per-item results must be checked independently; no completed live run is asserted. |

The [dated deployment review](../../docs/evidence/etms-deployment-review-2026-09-22.md) records the code findings, including the initial planning/download dependency. The external engine, credentials, internal locations and raw deployment configuration are excluded from this public reference. The repository's runnable offline demo covers **Avaya and NAS reporting only**, not eTMS replacement.

Read the [entry contract](SKILL.md), [procedure reference](WORKINSTRUCTION.md) or [workflow index](../README.md).
