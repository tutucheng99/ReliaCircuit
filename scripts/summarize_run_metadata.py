"""Summarize public GPU-stage metadata files without local execution details."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def summarize(root: Path = ROOT) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for path in sorted(root.glob("results/**/**/*.metadata.json")):
        rel = path.relative_to(root).as_posix()
        data = json.loads(path.read_text(encoding="utf-8"))
        rows.append(
            {
                "path": rel,
                "model_id": data.get("model_id"),
                "sae_release": data.get("sae_release"),
                "sae_id": data.get("sae_id"),
                "rows_written": data.get("rows_written"),
                "manifest_rows": data.get("manifest_rows"),
                "elapsed_sec": data.get("elapsed_sec"),
                "dry_run": data.get("dry_run", False),
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "results" / "paper_assets" / "compute_metadata_summary.csv")
    args = parser.parse_args()
    frame = summarize()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(args.output, index=False)


if __name__ == "__main__":
    main()
