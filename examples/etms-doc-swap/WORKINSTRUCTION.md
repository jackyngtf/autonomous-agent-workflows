# eTMS replacement: handoff procedure reference

[**English**](WORKINSTRUCTION.md) · [繁體中文](WORKINSTRUCTION.zh-TW.md)

This reference distinguishes the intended handoff from the **22 September 2026** deployment/source inspection. That read-only review confirmed driver, engine and configuration files and a captured mode of **shadow**, without executing the operational code. A separately assessed user-triggered shadow report recorded 30 HELD, 0 PLANNED and 0 SWAPPED. The private implementation remains outside the public repository; the procedure below is not a claim that all its requirements are enforced.

## Inputs and deployment boundary

The task expects an incoming-document folder and a deployed engine package obtained from an authorised external store. The package supplies the driver and configuration. A manifest derived from a static SQL snapshot is a file input used by the engine; the task remains prohibited from connecting to a database or executing SQL.

The instructions specify weekday 09:30 execution, without a timezone. The deployment owner must resolve scheduling and access details. This public reference omits hosts, accounts, credentials, shares and internal filesystem locations.

## Handoff sequence

| Step | Contract | On failure or uncertainty |
|---|---|---|
| 1. Obtain the deployed package | Retrieve the expected engine, driver and configuration through authorised access | If required files are absent, report “ENGINE NOT DEPLOYED” and stop |
| 2. Respect configuration | Use the configured shadow or live mode without changing it | Do not infer permission to enable live mode |
| 3. Invoke the driver | Delegate planning, verification and permitted replacement to the prebuilt implementation | Report a crash and the last known state; do not perform manual swaps |
| 4. Inspect results | Read structured output and the newest report | Retain partial, failed and unknown states rather than inventing success |
| 5. Report dispositions | Explain planned, replaced and held inputs, reasons and required follow-up | Stop on ambiguity; do not retry a failed live write without reporting |

## Modes and permitted changes

**Shadow:** the captured configuration selects this mode. The entry contract describes planning and verification without production changes. The inspected source skips production-document swaps, but the driver performs hidden/temporary/metadata inbox cleanup before the mode branch and uploads reports in shadow. The mode therefore does not guarantee zero remote mutation. These are source-level behaviours, not a claim that specific entries were deleted in an observed run.

**Live:** the intended contract permits only the file replacements in the engine's plan and associated authorised archive, log and report writes. The engine owns replacement and required rollback behaviour. Static source inspection does not establish atomicity, rollback reliability or a successful live outcome.

The agent cannot compensate for a driver failure by manually copying files or changing database references. Database version fields, training records, progress, completions, assignments, quizzes, application code and container configuration remain outside scope. A document-file replacement must not be described as updating any of those records.

## Source findings that affect interpretation

The driver does not propagate the first engine subprocess return code and can substitute an empty result when JSON is missing; its shadow branch returns zero. Read report contents and per-item states independently. In the reviewed code, `HELD` represents a precheck stop and `ERROR` a caught processing exception. Neither should be promoted to a completed swap because the outer process exited zero.

The first planning pass also depends on destination files that the driver downloads from the resulting plan. An isolated follow-up reproduced that bootstrap failure and tested a private candidate with mocked PDF metadata and blocked transport. The [deployment review](../../docs/evidence/etms-deployment-review-2026-09-22.md) separates the inspected deployment, held run, 22/22 remote-target check, offline candidate results and later verified deployment.

## Reporting contract

The private operational report should record:

- The configured mode and driver outcome, including crash or partial states.
- Each input's reported `PLANNED`, `SWAPPED` or `HELD` disposition and reason.
- What the submitting team or responsible operator needs to resolve.
- Manifest destinations that fail the expected availability check, and engine errors.
- In live mode, the reported replaced files and corresponding archived filenames.
- Any rollback attempt and its reported state, without inferring success from silence.

These are expected fields, not a fabricated sample run. Private reports may need internal file identifiers; public evidence would require a separate sanitisation pass.

## What would support a stronger claim

Deployment presence, configuration and selected source paths have now been inspected. Controlled execution evidence and failure tests are still needed to assess planning, permitted mutations and recovery. A completed live claim additionally requires an authorised execution record and before/after evidence. The assessed user-triggered Cowork attempt remains a held shadow outcome. Neither it nor the offline candidate checks establish a successful scheduled run or a live swap. The repair was later deployed with verified hashes and shadow configuration; a later manual run reported 19 PLANNED, 8 HELD and 0 SWAPPED on a 27-input subset of the earlier 30. All eight held cases require document-identity review; rename suggestions are not approvals.

Related: [case boundary](README.md) · [entry contract](SKILL.md) · [workflow index](../README.md).
