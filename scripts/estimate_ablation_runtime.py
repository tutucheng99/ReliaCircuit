from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    args = parse_args()
    estimate = build_estimate(args)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    estimate.to_csv(args.output, index=False)
    write_report(args.report, estimate)
    print(f"wrote runtime estimate to {safe_display_path(args.output)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Estimate exact-ablation sweep runtime from completed pilot metadata.")
    parser.add_argument(
        "--metadata",
        type=Path,
        action="append",
        default=None,
        help="Completed exact-ablation metadata JSON. Can be passed more than once.",
    )
    parser.add_argument("--prompts", type=Path, default=ROOT / "data" / "subject_verb_agreement" / "prompts.csv")
    parser.add_argument(
        "--features",
        type=Path,
        default=ROOT / "data" / "subject_verb_agreement" / "screened_features.csv",
    )
    parser.add_argument("--split", default="test")
    parser.add_argument("--target-rows", type=int, default=None)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "results" / "subject_verb_agreement" / "ablation_runtime_estimate.csv",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=ROOT / "results" / "subject_verb_agreement" / "ablation_runtime_estimate.md",
    )
    return parser.parse_args()


def build_estimate(args: argparse.Namespace) -> pd.DataFrame:
    metadata_paths = args.metadata or default_metadata_paths()
    points = [load_point(path) for path in metadata_paths if resolve_path(path).exists()]
    if not points:
        raise SystemExit("no metadata points found for runtime estimation")
    target_prompts, target_features, target_rows = target_shape(args)
    largest = max(points, key=lambda row: row["rows_written"])
    conservative_sec = target_rows * largest["sec_per_row"]
    amortized = amortized_fit(points, target_rows)
    return pd.DataFrame(
        [
            {
                "target_split": args.split,
                "target_prompts": target_prompts,
                "target_features": target_features,
                "target_rows": target_rows,
                "metadata_points": len(points),
                "largest_point_rows": largest["rows_written"],
                "largest_point_elapsed_sec": largest["elapsed_sec"],
                "largest_point_sec_per_row": largest["sec_per_row"],
                "conservative_elapsed_sec": conservative_sec,
                "conservative_elapsed_hours": conservative_sec / 3600.0,
                "amortized_overhead_sec": amortized["overhead_sec"],
                "amortized_sec_per_row": amortized["sec_per_row"],
                "amortized_elapsed_sec": amortized["elapsed_sec"],
                "amortized_elapsed_hours": amortized["elapsed_sec"] / 3600.0,
                "source_metadata": "; ".join(row["path"] for row in points),
            }
        ]
    ).round(4)


def default_metadata_paths() -> list[Path]:
    return [
        ROOT / "results" / "subject_verb_agreement" / "exact_ablation_cache_smoke.metadata.json",
        ROOT / "results" / "subject_verb_agreement" / "exact_ablation_cache_pilot.metadata.json",
    ]


def load_point(path: Path) -> dict[str, Any]:
    resolved = resolve_path(path)
    payload = json.loads(resolved.read_text(encoding="utf-8"))
    rows = int(payload.get("rows_written") or payload.get("manifest_rows") or 0)
    elapsed = float(payload.get("elapsed_sec") or 0)
    if rows <= 0 or elapsed <= 0:
        raise ValueError(f"metadata lacks positive rows_written and elapsed_sec: {path}")
    return {
        "path": safe_display_path(resolved),
        "rows_written": rows,
        "elapsed_sec": elapsed,
        "sec_per_row": elapsed / rows,
    }


def target_shape(args: argparse.Namespace) -> tuple[int, int, int]:
    if args.target_rows is not None:
        return 0, 0, args.target_rows
    prompts = pd.read_csv(resolve_path(args.prompts))
    if args.split != "all" and "split" in prompts.columns:
        prompts = prompts[prompts["split"] == args.split]
    features = pd.read_csv(resolve_path(args.features))
    target_prompts = int(len(prompts))
    target_features = int(len(features))
    return target_prompts, target_features, target_prompts * target_features


def amortized_fit(points: list[dict[str, Any]], target_rows: int) -> dict[str, float]:
    ordered = sorted(points, key=lambda row: row["rows_written"])
    if len(ordered) < 2 or ordered[-1]["rows_written"] == ordered[0]["rows_written"]:
        sec_per_row = ordered[-1]["sec_per_row"]
        return {"overhead_sec": 0.0, "sec_per_row": sec_per_row, "elapsed_sec": sec_per_row * target_rows}
    first = ordered[0]
    last = ordered[-1]
    sec_per_row = max(
        0.0,
        (last["elapsed_sec"] - first["elapsed_sec"]) / (last["rows_written"] - first["rows_written"]),
    )
    overhead = max(0.0, last["elapsed_sec"] - sec_per_row * last["rows_written"])
    return {
        "overhead_sec": overhead,
        "sec_per_row": sec_per_row,
        "elapsed_sec": overhead + sec_per_row * target_rows,
    }


def write_report(path: Path, estimate: pd.DataFrame) -> None:
    row = estimate.iloc[0]
    lines = [
        "# Ablation Runtime Estimate",
        "",
        "This estimate uses completed real RunPod exact-ablation metadata. The",
        "conservative estimate scales the largest pilot run directly per row; the",
        "amortized estimate fits a fixed startup cost plus per-row slope from the",
        "available pilot points.",
        "",
        estimate.to_markdown(index=False),
        "",
        f"Conservative estimate: {row['conservative_elapsed_hours']:.2f} hours.",
        f"Amortized estimate: {row['amortized_elapsed_hours']:.2f} hours.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def resolve_path(path: Path) -> Path:
    return path if path.is_absolute() else ROOT / path


def safe_display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    main()
