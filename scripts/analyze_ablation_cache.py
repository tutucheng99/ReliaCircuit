from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from reliacircuit.cache_analysis import analyze_ablation_cache, selected_feature_list


def main() -> None:
    args = parse_args()
    cache = pd.read_csv(args.cache)
    ground_truth = pd.read_csv(args.ground_truth) if args.ground_truth else None
    feature_stats, summary = analyze_ablation_cache(
        cache,
        q=args.q,
        e_gamma=args.e_gamma,
        n_bootstrap=args.n_bootstrap,
        confidence=args.confidence,
        seed=args.seed,
        ground_truth=ground_truth,
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    feature_stats.to_csv(args.output_dir / "feature_stats.csv", index=False)
    summary.to_csv(args.output_dir / "method_summary.csv", index=False)
    selected_cols = ["feature_id", "tau_hat", "p_value", "e_value", "ci_lower", "ci_upper"]
    selected_cols += [c for c in feature_stats.columns if c.startswith("selected_")]
    feature_stats.loc[:, selected_cols].to_csv(args.output_dir / "selected_features.csv", index=False)
    for method in [c.removeprefix("selected_") for c in feature_stats.columns if c.startswith("selected_")]:
        selected_feature_list(feature_stats, method=method).to_csv(
            args.output_dir / f"selected_features_{method}.csv",
            index=False,
        )
    print(summary.to_string(index=False))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--ground-truth", type=Path, default=None)
    parser.add_argument("--q", type=float, default=0.1)
    parser.add_argument("--e-gamma", type=float, default=0.5)
    parser.add_argument("--n-bootstrap", type=int, default=499)
    parser.add_argument("--confidence", type=float, default=0.95)
    parser.add_argument("--seed", type=int, default=0)
    return parser.parse_args()


if __name__ == "__main__":
    main()
