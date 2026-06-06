from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    args = parse_args()
    screen = pd.read_csv(args.screen_scores).sort_values(["screen_score", "feature_id"], ascending=[False, True])
    summary = pd.read_csv(args.method_summary)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    rows = []
    for _, row in summary.iterrows():
        method = str(row["method"])
        k = int(row["discoveries"])
        if k <= 0:
            continue
        out_path = args.output_dir / f"selected_features_top_score_k_{method}.csv"
        selected = screen.head(k).copy()
        selected.insert(0, "selection_method", f"top_score_k_{method}")
        selected.to_csv(out_path, index=False)
        rows.append(
            {
                "selection_method": f"top_score_k_{method}",
                "reference_method": method,
                "k": k,
                "path": safe_display_path(out_path),
            }
        )

    if args.top_k is not None:
        out_path = args.output_dir / f"selected_features_top_score_k_{args.top_k}.csv"
        selected = screen.head(args.top_k).copy()
        selected.insert(0, "selection_method", f"top_score_k_{args.top_k}")
        selected.to_csv(out_path, index=False)
        rows.append(
            {
                "selection_method": f"top_score_k_{args.top_k}",
                "reference_method": "fixed_top_k",
                "k": int(args.top_k),
                "path": safe_display_path(out_path),
            }
        )

    index = pd.DataFrame(rows)
    index.to_csv(args.output_dir / "top_score_baselines.csv", index=False)
    print(f"wrote {len(index)} top-score baseline feature sets to {safe_display_path(args.output_dir)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build top-score baselines matched to discovery counts.")
    parser.add_argument(
        "--screen-scores",
        type=Path,
        default=ROOT / "results" / "subject_verb_agreement" / "screen_scores.csv",
    )
    parser.add_argument(
        "--method-summary",
        type=Path,
        default=ROOT / "results" / "subject_verb_agreement" / "cache_analysis" / "method_summary.csv",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "results" / "subject_verb_agreement" / "cache_analysis",
    )
    parser.add_argument("--top-k", type=int, default=None)
    return parser.parse_args()


def safe_display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    main()
