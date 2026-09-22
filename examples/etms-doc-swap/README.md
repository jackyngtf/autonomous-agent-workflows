# eTMS document replacement: scheduled handoff

[**English**](README.md) · [繁體中文](README.zh-TW.md)

This third workflow hands document replacement to a separately deployed engine. Its available entry instructions specify an unattended weekday task at **09:30**: inspect an incoming-document folder, obtain the deployed engine and driver from an external store, run under the configured mode, then explain the result.

The source does not specify the schedule timezone. The task configuration, deployed engine, tests and completed executions have not been verified in this review. The retained evidence establishes an instruction contract, not successful document swaps.

## What the agent is responsible for

The agent checks that the required deployed files exist, invokes the driver within the authorised configuration, and reads the driver's JSON output and report. It should describe which inputs were planned, replaced or held, why an item was held, and what requires attention.

The agent must not perform ad hoc file swaps, connect to a database, execute SQL, change training records or switch itself from shadow to live mode. Changes are limited to files in the engine's plan and its designated archives, logs and reports, through the engine or driver.

## What remains delegated

| Item | Evidence boundary |
|---|---|
| Shadow mode | The entry contract requires planning and verification with no production writes |
| Live mode | Selected by the responsible operator through configuration, not by the scheduled agent |
| Replacement and rollback | Required engine behaviour described by the contract; implementation and failure recovery are unverified here |
| Manifest | The contract refers to a file manifest derived from a static SQL snapshot; this does not authorise database connections or SQL execution |
| Result reporting | Required fields are documented; no example is presented as a completed live run |

The external engine, credentials, internal locations and deployment configuration are excluded from this public reference. The repository's runnable offline demo covers **Avaya and NAS reporting only**, not eTMS replacement.

Read the [entry contract](SKILL.md), [procedure reference](WORKINSTRUCTION.md) or [workflow index](../README.md).
