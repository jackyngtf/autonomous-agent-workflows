# eTMS replacement: handoff procedure reference

[**English**](WORKINSTRUCTION.md) · [繁體中文](WORKINSTRUCTION.zh-TW.md)

This reference reconstructs the handoff described by the available entry skill. The deployed engine and driver are outside the public repository. No engine source, tests or run reports have been inspected as evidence for this case, so the steps below are requirements, not observed execution results.

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

**Shadow:** the contract requires planning and verification only, with zero production writes. It is the instructed mode until the operator changes configuration. The available entry file does not establish the current deployed mode.

**Live:** the driver may perform only the file replacements in the engine's plan and the associated archive, log and report writes authorised by the contract. The engine owns replacement and required rollback behaviour. No atomicity, rollback reliability or successful live outcome has been verified here.

The agent cannot compensate for a driver failure by manually copying files or changing database references. Database version fields, training records, progress, completions, assignments, quizzes, application code and container configuration remain outside scope. A document-file replacement must not be described as updating any of those records.

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

Engine inspection, configuration evidence, controlled shadow output and failure tests would be needed to verify planning, file constraints and rollback. A completed live claim would additionally require an authorised execution record and before/after evidence. Until then, this case demonstrates a constrained scheduled handoff design.

Related: [case boundary](README.md) · [entry contract](SKILL.md) · [workflow index](../README.md).
