# Run the reporting demonstration

**English** · [繁體中文](README.zh-TW.md) · [Portfolio](../README.md)

This is newly authored reference code for the portfolio. It demonstrates a narrow, inspectable reporting pipeline with synthetic data. It does not replay historical agent runs, call an LLM, contact the NAS or delete inputs.

## Start with a successful update

From the repository root, with Python 3.11 or later:

```bash
python -m pip install -r requirements.txt
python -m demo --workflow all --output-dir output/demo
```

On a fresh destination, the demo creates a fictional 3 August 2026 sheet with one existing row. It then adds the 4 August fixtures: 13 Avaya rows across 30 columns, and eight NAS rows. The resulting workbooks contain 14 and nine total data rows respectively, across two dated sheets each.

```text
output/demo/
  avaya/
    2026-08.xlsx
    run-report.md
    evidence.json
  nas/
    2026-08.xlsx
    run-report.md
    evidence.json
```

Open the workbooks to see the preserved prior-day record and the new records. The bilingual report records each outcome; the JSON provides the checkable details. The fixtures live in [sample-data](../sample-data), and the processing is in [workflows.py](workflows.py).

Run the identical command again. Matching existing records produce `NO_CHANGE`; the workbook bytes remain unchanged. If a same-date sheet conflicts with the input, the run stops instead of treating the date alone as proof of completion.

## Watch validation block an update

Use a separate output directory so there is still a pending update:

```bash
python -m demo --workflow all --scenario blocked --output-dir output/blocked
```

**Expected exit code: 2.** This scenario changes a cell in the staged candidate after it has been written. An independent reader compares every supported cell against the expected records, detects the change and prevents publication. The previously seeded workbook and all fixture inputs remain intact; cleanup eligibility stays false.

The mismatch may have the same row and column counts as the valid workbook. That is intentional: dimension checks alone cannot establish content equivalence. The automated test suite also covers a duplicated header and a partial transfer.

## What is checked

| Boundary | Local reference behaviour |
|---|---|
| Input | Exact schema, row width, parseable dates, complete-date cutoff and expected month |
| Existing workbook | Confirmed absence can be seeded; unreadable or unsupported content raises an error |
| Candidate | Compare complete supported text-cell values, sheet names and record ordering using openpyxl |
| Simulated transfer | Copy to local staging, compare digests and re-read the staged copy |
| Publication | Detect a changed destination before replacement; keep the old file on validation failure |
| Rerun | Match already-present data without adding a duplicate or rewriting the file |

The destination-change check is not a distributed lock. A real adapter would need a concurrency and recovery design appropriate to its storage system.

## Checks you can repeat

The [32-second recording](../images/demo-walkthrough.webm?raw=true) shows a read-only view of the generated artifacts. To inspect the same viewer locally after running both scenarios, run `python scripts/render_demo_walkthrough.py` and open `output/demo-walkthrough.html`. Displayed values come from the generated files; this is not a live agent interface.

```bash
python -m unittest discover -s tests -v
python scripts/check_docs.py
```

The [tests](../tests/test_workflows.py) exercise normal and blocked CLI outcomes, preservation, conflicting reruns, malformed records, unreadable workbooks, cell tampering, duplicate headers, partial transfer, destination changes, literal formula-like text, query-cap rejection and Melbourne daylight-saving boundaries. [CI](../.github/workflows/check.yml) runs the checks on Linux and Windows with Python 3.11 and 3.12.

The [legacy command](../sample-data/rebuild_workbook_demo.py) remains a wrapper around the Avaya demo. New documentation uses the module entry point so both workflows share one interface.

## Deliberate limits

The demonstration handles controlled text-only tables. It does not preserve arbitrary formulas, charts, macros, merged-cell layouts or existing workbook styling. NAS records are grouped into dated sheets in the demo; the historical weekend/holiday grouping policy is described in the case study, not implemented as a full calendar planner here. The query-cap check rejects a known completeness risk; it does not prove completeness of a live API. No real upload or deletion is performed. Passing these checks supports the local reference behaviour, not a guarantee about every historical run.
