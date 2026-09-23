# eTMS document replacement: scheduled handoff

[**English**](README.md) · [繁體中文](README.zh-TW.md)

This third workflow hands document replacement to a separately deployed engine. Its available entry instructions specify an unattended weekday task at **09:30**: inspect an incoming-document folder, obtain the deployed engine and driver from an external store, run under the configured mode, then explain the result.

The source does not specify the schedule timezone. Inspection began on **22 September 2026** with shadow configuration and a manual run that held all 30 inputs. After tested repairs and an authorised switch to live, the **23 September** report records 19 SWAPPED and 8 HELD, supported by read-only file and HTTP checks. The [dated review](../../docs/evidence/etms-deployment-review-2026-09-22.md) separates these stages and records the remaining archive-label defect and evidence limits.

## What the agent is responsible for

The agent checks that the required deployed files exist, invokes the driver within the authorised configuration, and reads the driver's JSON output and report. It should describe which inputs were planned, replaced or held, why an item was held, and what requires attention.

The agent must not perform ad hoc file swaps, connect to a database, execute SQL, change training records or switch itself from shadow to live mode. Changes are limited to files in the engine's plan and its designated archives, logs and reports, through the engine or driver.

## What remains delegated

| Item | Evidence boundary |
|---|---|
| Shadow mode | The 22 September snapshot selected shadow. The source skips production-document swaps but still performs inbox housekeeping and report uploads. |
| Live mode | Selected by the operator through configuration. The authorised switch on 23 September preceded the observed live result. |
| Replacement and rollback | Delegated engine responsibilities. One publication outcome is supported by read-only checks; exact pre-run backup preservation and rollback safety remain unverified. |
| Manifest | The contract refers to a file manifest derived from a static SQL snapshot; this does not authorise database connections or SQL execution |
| Result reporting | A zero driver exit does not establish engine success. Check the report, per-item states and remote results independently. |

The [dated deployment review](../../docs/evidence/etms-deployment-review-2026-09-22.md) records the code findings, including the initial planning/download dependency. The external engine, credentials, internal locations and raw deployment configuration are excluded from this public reference. The repository's runnable offline demo covers **Avaya and NAS reporting only**, not eTMS replacement.

Read the [entry contract](SKILL.md), [procedure reference](WORKINSTRUCTION.md) or [workflow index](../README.md).
