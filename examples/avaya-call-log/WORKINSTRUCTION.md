# Avaya call-log workflow: procedure reference

[**English**](WORKINSTRUCTION.md) · [繁體中文](WORKINSTRUCTION.zh-TW.md)

> Rewritten design reference, not an executable production runbook. Live connection details and credentials are omitted. Historical implementations had varying validation depth; the checks below distinguish the intended contract from deployment work still required.

## Purpose and data contract

The workflow takes daily SMDR CSV files from a PBX receiver and plans missing dates in monthly reporting workbooks. The original schedule was weekdays at 10:00. Date eligibility uses `Australia/Melbourne`, including daylight saving, with the current local day excluded.

The public [SMDR fixture](../../sample-data/smdr-receiver/output/smdr_2026-08-04.csv) and [demo parser](../../demo/workflows.py) declare a 30-column contract. This is the example's schema, not a claim that every PBX installation produces identical records. Validate headers, row widths and dates before using a source.

The workbook contract is tabular text data with known sheet names and columns. Arbitrary formulas, macros, drawings and other Excel features are outside this reconstruction.

## Procedure and stop conditions

| Step | Action | Required decision or check |
|---|---|---|
| 1. Inspect | Establish cutoff, source inventory and current destination | Authentication, access or parsing failure is not file absence |
| 2. Plan | Identify eligible dates not already represented | Existing dates must not silently gain duplicate or changed records |
| 3. Parse | Validate the complete source against its declared schema | Malformed or mixed-width records block the affected update |
| 4. Prepare | Snapshot existing records and build a candidate workbook | Expected records must not be derived solely from the rebuild output |
| 5. Validate | Compare sheet names, counts and expected cell values | Detect altered records and duplicated headers before publication |
| 6. Publish | A live adapter writes the approved candidate | Define concurrency, backup and partial-upload recovery separately |
| 7. Retrieve | Download and verify the published copy | Failed verification blocks source cleanup and requires a publication incident report |
| 8. Report | Record outcome, validation scope and cleanup decision | A live cleanup decision needs verified correspondence with each source |

Rebuilding may replace a workbook file. “Preserve” refers to its supported existing records, not an unchanged file or byte-identical XLSX package.

A source file is only a cleanup candidate after its records have been verified in the intended destination. The public demo reports this eligibility and performs no deletion. Malformed inputs and uncertainty remain visible for operator review.

## What a live deployment must supply

- Source and destination configuration, service permissions and secure credential delivery.
- The actual PBX schema and policy for conflicting or previously covered dates.
- A publication method with defined concurrency, backups and recovery.
- A cleanup policy, retention period and incident escalation owner.
- Dependency versions and an explicit supported workbook contract.

Instructions do not substitute for these controls. An SMB or receiver observation from one environment should be verified before becoming a rule elsewhere.

## Try the local reconstruction

```sh
python -m demo --workflow avaya --output-dir output/demo
```

The demo uses synthetic files, validates local artifacts and generates a run report with machine-readable evidence. It does not test SMB delivery, scheduler operation or live deletion. See [the guide](../../demo/README.md) and [synthetic report format](sample-report.md).