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

The configuration hash was unchanged and mode remained **shadow** before and after deployment. A second direct read confirmed both deployed hashes and no leftover staging files. Deployment did not execute the operational engine. At that point, the user's post-fix Cowork run was pending. The earlier source hashes and **15:27 result of 30 HELD, 0 PLANNED and 0 SWAPPED** remain the historical record.

## Post-deployment shadow run: 22 September 2026

The user manually reran Cowork after deployment. Two retrieved reports record an intermediate pass at **16:35:14** and a final pass at **16:35:49**; no timezone is inferred from those report times. Both contain the **same 27 input filenames**, compared after removing status labels, against a **509-entry manifest**.

| Reported field | Intermediate pass | Final pass |
|---|---:|---:|
| Inbox inputs | 27 | 27 |
| `HELD` | 27 | 8 |
| `PLANNED` | 0 | 19 |

The report comparison identifies **19 inputs changing from HELD to PLANNED**, with **eight remaining HELD**. All 27 inputs were present in the earlier 30-input cohort; three earlier inputs were absent and none were new. The reason for the three absences is not established. The final report therefore records actual planning progress within this 27-input attempt, not a controlled comparison of two identical 30-input runs or a completed document replacement.

All eight held cases still require document-identity review. Three rename suggestions involve a questionnaire suffix; filename/code matching does not independently establish document type from content. These suggestions are not approval to rename files or accept targets.

| Retrieved report | Bytes | SHA-256 |
|---|---:|---|
| Intermediate pass | 13,543 | `9c93197804f68b1803213ce765dcc53b6a0960912302558e7dbd8cec5e272017` |
| Final pass | 10,560 | `d295989bebeb6524703cd80a907ea8f080054393b6fbbef09d1a04a81e12f1db` |

Read-only follow-up confirmed 27 inbox PDFs, the unchanged configuration hash with mode **shadow**, and both deployed source hashes unchanged. The final report records **0 SWAPPED, 0 ERROR and 0 PARTIAL**. This manually triggered attempt does not establish live replacement, rollback, scheduler reliability or notification delivery, and remains outside the 92-file Avaya/NAS reporting ledger.

## Live publication limitation found after the shadow run

Static review of the deployed source found that the driver parses swapped-file output using a path pattern that stops at whitespace (driver line 159; engine lines 465–466). All 19 planned destination paths contain whitespace, so none match that parser. If a live engine run marked those local files `SWAPPED`, the driver could skip the upload and HTTP-verification loops because its parsed completion list is empty, while still reaching inbox cleanup for successful local items (driver lines 196–197).

This is a source-level finding, not an observed live failure: the reviewed run remained shadow and did not enter that branch. **At that point, the 19 planned items were not established as safe for live publication.** A separate private guard candidate now accepts spaced paths, checks complete publication records before remote writes, and requires every intended target to be uploaded and hash-verified before inbox cleanup. Nine offline test methods passed: six shadow regressions and three publication tests covering 11 synthetic scenarios. The live-publication tests simulate engine output and SMB/HTTP; they do not execute a real live engine. At this 22 September snapshot, the candidate was not deployed; the later deployment is recorded below. General production rollback/concurrency safety is not established.

## Guard deployment and live configuration: 23 September 2026

At **08:41:54 +10:00 on 23 September 2026**, the tested guard driver was deployed with explicit user authorisation. The previous driver was backed up and its hash verified; the new driver was read back and verified **before** switching configuration. The configuration was also backed up, and a field-only replacement plus deep JSON comparison confirmed that its only change was **`shadow` → `live`**.

| Artifact | SHA-256 |
|---|---|
| Deployed guard driver | `f2d7849743d5d8829f132a0d43a78dbc4280cc0da0e96eca780a97f94eea3b69` |
| Unchanged engine | `bfa41f5ed860df0100fe382d13d4cf890b1781c24319308ab30da66e10037405` |

A second independent read confirmed driver, engine and configuration hashes, both backups and no leftover staging files. **No operational engine was executed during deployment; at that point, the first live Cowork run was pending.** The 22 September source snapshots and shadow outcomes remain historical evidence, not live replacement results.

## Observed live run: 23 September 2026

The retrieved **09:41** live report records **27 inputs, 19 SWAPPED and 8 HELD**. No timezone is inferred from the displayed report time. The trigger was not independently verified, so this record does not classify the attempt as a scheduled success. A preceding preflight summary recorded 27 HELD; the final result and read-only checks recorded at **11:55 +10:00 on 23 September** are separate evidence:

| Check | Observed result |
|---|---|
| Destination and archive files | All 19 destinations and 19 archives existed; each destination's bytes differed from its archive |
| Served copies | All 19 HTTP requests returned 200, with response SHA-256 matching the current NAS destination; zero check errors |
| Inbox | Exactly the eight held filenames remained; none of the 19 swapped inputs remained |
| Operational logs | Two logs each contained 19 new rows for this date |
| Deployed state | Mode remained live; driver and engine hashes matched the 23 September deployment |

All eight held items still require document-identity review. No rename suggestion is treated as approved. These checks support the reported live publication outcome, but **no prior destination hashes were captured**, so archive existence and differing bytes do not prove that each archive equals its exact pre-run destination.

An **archive-label defect** also remains: static review found that the engine derives the revision label from the incoming document and uses it when naming the archived old file (engine lines 182, 320 and 325). All 19 archive labels used the incoming revision. The label therefore does not establish the archived content's actual revision. No fix for this naming defect had been prepared or applied at this snapshot; the result is not presented as anomaly-free or proof of rollback safety.

| Retrieved artifact | Bytes | SHA-256 |
|---|---:|---|
| Preflight summary | 16,756 | `7803ce19b6e7a3a1391175e81a1c288256439c1fcfd672ee77ee7a0c7276acf3` |
| Live run report | 12,501 | `95f2ff3619f93bd4e7bd886d810a669cfdf1c87043a6129284dbd2de836d2c4d` |
| Live summary | 10,565 | `cc6d0d883eb0a341d9b775de630ae76851e46f6243568a7291c446d99291b238` |

## What this record does not establish

The live report and read-only checks establish one observed publication outcome, with the archive-label limitation above. They do not establish rollback safety, transactional guarantees, scheduler reliability, an unattended success rate or notification delivery. The public offline demo remains limited to Avaya and NAS reporting, and the eTMS evidence remains outside the 92-file reporting ledger.

[Read the case](../case-study/07-etms-document-handoff.md) · [Inspect the task reference](../../examples/etms-doc-swap/README.md) · [Claim index](claim-index.md).
