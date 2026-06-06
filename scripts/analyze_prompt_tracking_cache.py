from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from reliacircuit.cache_analysis import analyze_prompt_tracking_cache, selected_feature_list


def main() -> None:
    args = parse_args()
    prompts = pd.read_csv(args.prompts)
    cache = pd.read_csv(args.cache)
    prompt_effects = infer_prompt_effects_from_exact_cache(prompts, cache)
    feature_stats, summary = analyze_prompt_tracking_cache(
        cache,
        prompt_effects,
        q=args.q,
        e_gamma=args.e_gamma,
        n_bootstrap=args.n_bootstrap,
        confidence=args.confidence,
        seed=args.seed,
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    prompt_effects.to_csv(args.output_dir / "prompt_full_effects_exact.csv", index=False)
    feature_stats.to_csv(args.output_dir / "feature_stats_tracking.csv", index=False)
    summary.to_csv(args.output_dir / "method_summary_tracking.csv", index=False)
    selected_cols = [
        "feature_id",
        "tau_hat",
        "tracking_cov_hat",
        "tracking_corr",
        "tracking_slope_full_on_feature",
        "mean_effect_tau_hat",
        "p_value",
        "e_value",
        "ci_lower",
        "ci_upper",
    ]
    selected_cols += [col for col in feature_stats.columns if col.startswith("selected_")]
    feature_stats.loc[:, selected_cols].to_csv(args.output_dir / "selected_features_tracking.csv", index=False)
    for method in [col.removeprefix("selected_") for col in feature_stats.columns if col.startswith("selected_")]:
        selected_feature_list(feature_stats, method=method).to_csv(
            args.output_dir / f"selected_features_tracking_{method}.csv",
            index=False,
        )
    write_report(args.output_dir / "prompt_tracking_cache_report.md", prompt_effects, summary, feature_stats)
    print(summary.to_string(index=False))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze exact-ablation cache for prompt-tracking covariance.")
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument(
        "--prompts",
        type=Path,
        default=ROOT / "data" / "subject_verb_agreement" / "prompts.csv",
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--q", type=float, default=0.1)
    parser.add_argument("--e-gamma", type=float, default=0.5)
    parser.add_argument("--n-bootstrap", type=int, default=499)
    parser.add_argument("--confidence", type=float, default=0.95)
    parser.add_argument("--seed", type=int, default=0)
    return parser.parse_args()


def infer_prompt_effects_from_exact_cache(prompts: pd.DataFrame, cache: pd.DataFrame) -> pd.DataFrame:
    required_prompts = {"prompt_id", "clean_prompt", "patch_prompt", "split"}
    missing_prompts = required_prompts - set(prompts.columns)
    if missing_prompts:
        raise ValueError(f"prompts missing columns: {sorted(missing_prompts)}")
    required_cache = {"prompt_id", "clean_metric"}
    missing_cache = required_cache - set(cache.columns)
    if missing_cache:
        raise ValueError(f"exact cache missing columns: {sorted(missing_cache)}")

    clean_metric = cache.groupby("prompt_id", as_index=False)["clean_metric"].first()
    clean_metric = clean_metric.rename(columns={"clean_metric": "exact_clean_metric"})
    merged = prompts.merge(clean_metric, on="prompt_id", how="left", validate="one_to_one")
    metric_by_prompt_text = merged.dropna(subset=["exact_clean_metric"]).set_index("clean_prompt")[
        "exact_clean_metric"
    ].to_dict()
    # The paired subject-verb row has swapped target/counter labels, so its
    # own clean metric is the negative of the patch metric under this row's
    # target/counter labels.
    merged["patch_metric_inferred"] = -merged["patch_prompt"].map(metric_by_prompt_text)
    merged["full_difference"] = merged["exact_clean_metric"] - merged["patch_metric_inferred"]
    keep = [
        col
        for col in [
            "prompt_id",
            "split",
            "template_id",
            "pair_id",
            "cluster_id",
            "exact_clean_metric",
            "patch_metric_inferred",
            "full_difference",
        ]
        if col in merged.columns
    ]
    return merged.loc[merged["full_difference"].notna(), keep].copy()


def write_report(
    path: Path,
    prompt_effects: pd.DataFrame,
    summary: pd.DataFrame,
    feature_stats: pd.DataFrame,
) -> None:
    strongest = feature_stats.assign(abs_tracking_corr=feature_stats["tracking_corr"].abs()).sort_values(
        "abs_tracking_corr",
        ascending=False,
    )
    lines = [
        "# Prompt-Tracking Cache Analysis",
        "",
        "This analysis tests feature-level covariance with the full clean-vs-patch",
        "prompt effect inferred from the same exact-ablation runtime. It is a",
        "tracking-aware alternative to the mean-ATE feature test.",
        "",
        "## Prompt Effects",
        prompt_effects.groupby("split")["full_difference"].agg(["count", "mean", "std"]).to_markdown(),
        "",
        "## Tracking-Aware FDR Summary",
        summary.to_markdown(index=False),
        "",
        "## Highest Absolute Tracking Correlations",
        strongest[
            [
                "feature_id",
                "tracking_corr",
                "tracking_cov_hat",
                "mean_effect_tau_hat",
                "p_value",
                "e_value",
            ]
        ]
        .head(20)
        .to_markdown(index=False),
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
