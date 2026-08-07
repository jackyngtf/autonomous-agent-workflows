#!/usr/bin/env python3
"""
Minimal demo of the workbook-rebuild step used by the avaya-call-log agent.

Reads the sample SMDR CSV (sample-data/smdr-receiver/output/smdr_2026-08-04.csv),
rebuilds a monthly Excel workbook from scratch with xlsxwriter, and writes it to
sample-data/smdr-receiver/output/AUG_2026_demo.xlsx.

This is the core of Step 4 in the work-instruction. The production agent does the
same thing, but: (a) reads many CSVs, (b) preserves all existing sheets, (c) uploads
via SMB, (d) validates by re-downloading. This script strips all of that so you can
see the rebuild logic in isolation.

Usage:
    python3 rebuild_workbook_demo.py

Requirements:
    pip install xlsxwriter openpyxl

No network, no NAS, no credentials needed — 100% offline demo.
"""

import csv
import glob
import os
import sys

import xlsxwriter

# --- Configuration (swap these for your own setup) ----------------------------
DATA_DIR = os.path.join(os.path.dirname(__file__), "smdr-receiver", "output")
OUTPUT_WORKBOOK = os.path.join(DATA_DIR, "AUG_2026_demo.xlsx")


def load_csv(path):
    """Parse an SMDR CSV, returning (header_row, data_rows)."""
    with open(path, newline="", encoding="utf-8-sig") as f:
        # Sniff past any BOM; SMDR lines are CRLF-terminated
        reader = csv.reader(f)
        rows = [r for r in reader if r and any(cell.strip() for cell in r)]
    if not rows:
        return [], []
    return rows[0], rows[1:]


def build_workbook(csv_paths, output_path):
    """Rebuild a workbook from scratch — one worksheet per CSV file."""
    wb = xlsxwriter.Workbook(output_path)

    # Header format
    hdr = wb.add_format({
        "bold": True, "bg_color": "#1F4E79", "font_color": "white",
        "border": 1, "text_wrap": True, "valign": "vcenter",
    })
    cell = wb.add_format({"border": 1, "valign": "top"})

    for csv_path in sorted(csv_paths):
        # Worksheet name from filename: smdr_2026-08-04.csv -> 2026-08-04
        name = os.path.basename(csv_path).replace("smdr_", "").replace(".csv", "")
        ws = wb.add_worksheet(name[:31])  # Excel 31-char sheet name limit

        header, rows = load_csv(csv_path)
        if not header:
            continue

        for col, title in enumerate(header):
            ws.write(0, col, title, hdr)
        for r, row in enumerate(rows, start=1):
            for c, val in enumerate(row):
                ws.write(r, c, val, cell)

        ws.freeze_panes(1, 0)
        ws.set_column(0, 0, 19)   # Call Start
        ws.set_column(1, 1, 14)   # Connected Time
        ws.set_column(4, 6, 13)   # Caller / Direction / Called

    wb.close()
    return output_path


def validate(output_path):
    """Re-open the workbook read-only and report sheet names + row counts.
    Mirrors the production validation step (Step 6)."""
    try:
        import openpyxl
    except ImportError:
        print("  (openpyxl not installed — skipping validation)")
        return
    wb = openpyxl.load_workbook(output_path, read_only=True, data_only=True)
    for ws in wb.worksheets:
        print(f"  sheet '{ws.title}': {ws.max_row - 1} data rows, {ws.max_column} cols")
    wb.close()


def main():
    csv_paths = glob.glob(os.path.join(DATA_DIR, "smdr_*.csv"))
    if not csv_paths:
        sys.exit(f"No sample SMDR CSVs found in {DATA_DIR}")

    print(f"Rebuilding workbook from {len(csv_paths)} CSV(s):")
    for p in csv_paths:
        print(f"  - {os.path.basename(p)}")

    out = build_workbook(csv_paths, OUTPUT_WORKBOOK)
    print(f"\nWrote workbook: {out}")

    print("\nValidation (re-read with openpyxl):")
    validate(out)
    print("\nDone. Open AUG_2026_demo.xlsx to inspect the result.")


if __name__ == "__main__":
    main()
