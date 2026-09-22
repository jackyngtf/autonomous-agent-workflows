# eTMS: deployment inspection and a held shadow run

[English](etms-deployment-review-2026-09-22.md) · [繁體中文](etms-deployment-review-2026-09-22.zh-TW.md) · [Evidence guide](README.md)

This record separates three kinds of evidence captured on **22 September 2026**: read-only inspection of a private deployment, static review of its source, and reports from a **user-triggered Cowork shadow run**. The reviewer did not execute the operational engine during source inspection. The manual run is not evidence that the weekday scheduler fired.

Raw document names, document identifiers, accounts, credentials, internal locations and report contents are excluded. The reviewed private source is not published or attributed to an author by this record.

## Deployment snapshot

| Observation | What it establishes | Limit |
|---|---|---|
| Driver, engine and configuration files present | The deployment artifacts existed at inspection time | Presence alone does not prove a working integration |
| Configuration mode: `shadow` | The captured configuration selected shadow | Not proof of zero remote mutation |
| Incoming folder: 30 PDFs | The read-only inventory found 30 direct PDF inputs | Not 30 accepted plans or successful swaps |
| Entry instruction: weekdays at 09:30 | The intended recurring schedule | The instruction does not specify its timezone; this run was manually triggered |

## What the run report records

The reviewed report header records a shadow run at **15:27 on 22 September 2026**. No timezone is inferred from that displayed time.

| Reported field | Count |
|---|---:|
| Inbox inputs | 30 |
| Manifest entries | 509 |
| `HELD` | 30 |
| `PLANNED` | 0 |
| `SWAPPED` | 0 |
| `ERROR` | 0 |
| `PARTIAL` | 0 |

This is a held outcome, not a successful update. Zero `ERROR` entries do not make 30 `HELD` entries successful. The reported disposition contains no document swaps; it does not establish that inbox housekeeping or report uploads made no changes.

Two report artifacts were retrieved with identical bytes and SHA-256. They provide one identical report content for this review, not evidence of two independent successful executions. These artifacts remain separate from the **92-file Avaya/NAS reporting ledger**.

The Cowork summary grouped the held items into **22 target-missing messages** and **8 unmatched inputs**. A subsequent read-only metadata check found **all 22 referenced target PDFs present at the intended NAS destination**, with **zero missing targets and zero read errors**. The report message therefore does not establish missing NAS files or broken database references. Offline follow-up classified the eight matching cases for review without turning any into an accepted plan; the deployed run's counts remain unchanged.

Any “IT notified” wording is report text. No separate message dispatch or recipient delivery was verified, so this record does not claim that a notification was sent.

## Static findings in the inspected source

Line locators refer to the exact private source snapshots identified below. They are audit pointers, not links to publicly available code.

| Source finding | Location | Interpretation |
|---|---|---|
| Hidden, temporary and metadata inbox entries are handled before the mode branch | Driver lines 86–90 | Shadow can mutate the inbox. This review does not claim that a particular entry was deleted during the observed run. |
| The shadow path uploads reports while skipping production-document replacement | Driver lines 136–167; engine lines 306–328 | Shadow is not a read-only remote operation, even when no production document is swapped. |
| The first engine subprocess return code is not propagated; missing JSON can become an empty result, and the driver returns zero in shadow | Driver lines 110–114 and 141 | Outer-process success is not a substitute for reading plan/report outcomes. |
| The engine has nonzero outcomes for planning or held states | Engine line 177 | A nonzero engine status and a zero driver status can coexist; statuses need interpretation at the correct layer. |
| The initial plan requires local destination files, while destination download depends on that plan | Reviewed planning/download sequence | The isolated follow-up below reproduces this staging bootstrap failure. Together with the 22/22 remote-existence check, it supports local staging rather than missing NAS targets as the issue to repair. |

In the inspected engine, `HELD` is a precheck stop and `ERROR` is a caught processing exception. Their meanings should not be collapsed into a generic completion state.

## Snapshot identifiers

| Private artifact | SHA-256 |
|---|---|
| Reviewed driver | `4dd8f822ac3b8014d9deff7d42a433b2b9716f555a42bf693dbfea588b887a9c` |
| Reviewed engine | `ccbf13dfda9de40aedfd3e726a8ea7e0c41327d5eda88cdca7ecfdf3dee13149` |
| Report content, identical in both retrieved artifacts | `c7e31b56ce06ab71776f8d5c8f5adfc058f8a55e0fb20cf46b0f794b0fb6bfed` |

Each report artifact was **13,544 bytes**. Digests identify the reviewed bytes; they do not independently authenticate the statements inside a report or prove which exact runtime source copy produced it.

## Offline follow-up: not deployed

This section records the pre-deployment checks. The later deployment is recorded separately below.

A private candidate was prepared and checked in isolation. It uses first-pass target information to stage destination files before running final validation, and stops on unsafe candidate paths or target-read failures. An isolated case reproduced an existing target being held by the original sequence; the candidate then produced `PLANNED` for that test case. PDF metadata was mocked and SMB was simulated in memory, with real network calls blocked, so this does **not** establish that the 22 real documents are ready to swap.

The matching change extends the recognised document-prefix pattern from one family to two while retaining the exact-title requirement. The eight filename cases still remained held: **three require rename review and five require manual review**, including **one ambiguous case with two candidates**. Recognition alone was not treated as permission to select a target.

**Six integrated driver/engine tests passed**, and **six separate matching tests passed**. These are private candidate checks, not the public reporting demo's test suite and not live eTMS execution. The candidate source is not published. No NAS deployment or post-fix rerun had occurred at this snapshot.

## Deployment follow-up: 22 September 2026

At **16:22:42 +10:00 on 22 September 2026**, the two tested scripts were deployed with the user's authorisation. Both original scripts were backed up and their SHA-256 hashes verified. Staged candidate bytes were verified before deployment; read-back checks then confirmed the deployed files matched the tested candidates:

| Deployed artifact | SHA-256 |
|---|---|
| Driver | `5c6b1c57af2d542bea5067f2ac7298c0a029785b2c219d1bd5071c9e53f77b19` |
| Engine | `bfa41f5ed860df0100fe382d13d4cf890b1781c24319308ab30da66e10037405` |

The configuration hash was unchanged and mode remained **shadow** before and after deployment. A second direct read confirmed both deployed hashes and no leftover staging files. Deployment did not execute the operational engine. The user's post-fix Cowork run remains pending; no new planning or swap result is claimed. The earlier source hashes and **15:27 result of 30 HELD, 0 PLANNED and 0 SWAPPED** remain the historical record.

## What this record does not establish

No successful live swap, rollback, transactional guarantee, unattended success rate or notification delivery is established. Verified deployment does not establish a successful post-fix execution. The public offline demo remains limited to Avaya and NAS reporting.

[Read the case](../case-study/07-etms-document-handoff.md) · [Inspect the task reference](../../examples/etms-doc-swap/README.md) · [Claim index](claim-index.md).
