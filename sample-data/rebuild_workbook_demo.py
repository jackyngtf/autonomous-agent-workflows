"""Compatibility entry point: python sample-data/rebuild_workbook_demo.py.

The verified synthetic Avaya result is written to output/legacy-demo/avaya/.
"""
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from demo.workflows import MELBOURNE, run_demo

if __name__ == "__main__":
    result = run_demo("avaya", ROOT / "sample-data/smdr-receiver/output/smdr_2026-08-04.csv",
                      ROOT / "output/legacy-demo/avaya", datetime(2026, 8, 5, 10, tzinfo=MELBOURNE))
    print(f"{result['status']}: {ROOT / 'output/legacy-demo/avaya/run-report.md'}")
    raise SystemExit(2 if result["status"] == "BLOCKED" else 0)
