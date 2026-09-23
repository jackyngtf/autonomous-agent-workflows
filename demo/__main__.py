"""Run with: python -m demo --workflow all --output-dir output/demo."""
import argparse
from datetime import datetime
from pathlib import Path

from .workflows import MELBOURNE, run_demo

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = {
    "avaya": ROOT / "sample-data/smdr-receiver/output/smdr_2026-08-04.csv",
    "nas": ROOT / "sample-data/nas-syslog/nas_access_records_2026-08-04.json",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Offline synthetic workflows / 離線合成資料示範")
    parser.add_argument("--workflow", choices=("all", "avaya", "nas"), default="all")
    parser.add_argument("--output-dir", type=Path, default=Path("output/demo"))
    parser.add_argument("--scenario", choices=("success", "blocked"), default="success")
    args = parser.parse_args()
    names = tuple(FIXTURES) if args.workflow == "all" else (args.workflow,)
    statuses = []
    for name in names:
        evidence = run_demo(name, FIXTURES[name], args.output_dir / name,
                            datetime(2026, 8, 5, 10, tzinfo=MELBOURNE), args.scenario == "blocked")
        statuses.append(evidence["status"])
        print(f"{name}: {evidence['status']} -> {args.output_dir / name / 'run-report.md'}")
    return 2 if "BLOCKED" in statuses else 0


if __name__ == "__main__":
    raise SystemExit(main())
