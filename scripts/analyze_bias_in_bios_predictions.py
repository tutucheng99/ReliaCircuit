from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from reliacircuit.bias_eval import (  # noqa: E402
    attach_removal_metadata,
    group_metrics,
    method_summary,
    normalize_prediction_cache,
)


def main() -> None:
    args = parse_args()
    if args.dry_run:
        labels = pd.read_csv(args.labels)
        predictions, removal_metadata = make_dry_run_predictions(labels)
        args.predictions.parent.mkdir(parents=True, exist_ok=True)
        predictions.to_csv(args.predictions, index=False)
        if args.removal_metadata is None:
            args.removal_metadata = args.predictions.with_name("bias_in_bios_removal_metadata_dry_run.csv")
        removal_metadata.to_csv(args.removal_metadata, index=False)
    else:
        predictions = pd.read_csv(args.predictions)
        removal_metadata = pd.read_csv(args.removal_metadata) if args.removal_metadata else None

    labels = pd.read_csv(args.labels) if args.labels else None
    normalized = normalize_prediction_cache(
        predictions,
        labels,
        example_col=args.example_column,
        method_col=args.method_column,
        prediction_col=args.prediction_column,
        target_col=args.target_column,
        protected_col=args.protected_column,
    )
    groups = group_metrics(
        normalized,
        method_col=args.method_column,
        target_col=args.target_column,
        protected_col=args.protected_column,
    )
    summary = method_summary(normalized, groups, method_col=args.method_column, baseline_method=args.baseline_method)
    summary = attach_removal_metadata(summary, removal_metadata)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    normalized.to_csv(args.output_dir / "example_metrics.csv", index=False)
    groups.to_csv(args.output_dir / "group_metrics.csv", index=False)
    summary.to_csv(args.output_dir / "method_summary.csv", index=False)
    print(summary.to_string(index=False))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze BiasInBios profession prediction caches.")
    parser.add_argument(
        "--predictions",
        type=Path,
        default=ROOT / "results" / "bias_in_bios" / "bias_in_bios_predictions_dry_run.csv",
    )
    parser.add_argument(
        "--labels",
        type=Path,
        default=ROOT / "data" / "bias_in_bios" / "prompts.csv",
        help="Prompt/label file used to add target/protected labels when predictions omit them.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "results" / "bias_in_bios" / "prediction_analysis_dry_run",
    )
    parser.add_argument("--removal-metadata", type=Path, default=None)
    parser.add_argument("--example-column", default="example_id")
    parser.add_argument("--method-column", default="method")
    parser.add_argument("--prediction-column", default="predicted_label")
    parser.add_argument("--target-column", default="target_label")
    parser.add_argument("--protected-column", default="protected_label")
    parser.add_argument("--baseline-method", default="clean")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def make_dry_run_predictions(labels: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    required = {"example_id", "target_label", "protected_label"}
    missing = required - set(labels.columns)
    if missing:
        raise SystemExit(f"label file missing columns for dry run: {sorted(missing)}")
    rows = []
    labels = labels.copy().reset_index(drop=True)
    for i, row in labels.iterrows():
        true_label = str(row["target_label"])
        wrong_label = str((int(row["target_label"]) + 1) % max(int(labels["target_label"].nunique()), 2))
        for method in ["clean", "e_bh_pcal", "top_score"]:
            pred = true_label
            if method == "clean" and i % 2 == 0:
                pred = wrong_label
            elif method == "top_score" and i % 3 == 0:
                pred = wrong_label
            rows.append(
                {
                    "example_id": row["example_id"],
                    "method": method,
                    "predicted_label": pred,
                }
            )
    metadata = pd.DataFrame(
        [
            {"method": "clean", "removed_features": 0, "erroneous_removal_rate": 0.0},
            {"method": "e_bh_pcal", "removed_features": 5, "erroneous_removal_rate": 0.0},
            {"method": "top_score", "removed_features": 5, "erroneous_removal_rate": 0.6},
        ]
    )
    return pd.DataFrame(rows), metadata


if __name__ == "__main__":
    main()
