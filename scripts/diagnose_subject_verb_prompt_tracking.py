from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    args = parse_args()
    prompts = pd.read_csv(args.prompts)
    clean_metrics = pd.read_csv(args.clean_metric_cache)
    exact_cache = pd.read_csv(args.exact_ablation_cache)
    feature_stats = pd.read_csv(args.feature_stats)
    screen_scores = pd.read_csv(args.screen_scores)

    prompt_effects = infer_full_prompt_effects(prompts, clean_metrics)
    tracking = additive_tracking_summary(
        exact_cache=exact_cache,
        prompt_effects=prompt_effects,
        feature_stats=feature_stats,
        screen_scores=screen_scores,
    )
    feature_tracking = feature_prompt_tracking(exact_cache, prompt_effects, feature_stats, screen_scores)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    prompt_effects.to_csv(args.output_dir / "prompt_full_effects_inferred.csv", index=False)
    tracking.to_csv(args.output_dir / "additive_tracking_summary.csv", index=False)
    feature_tracking.to_csv(args.output_dir / "feature_prompt_tracking.csv", index=False)
    write_report(args.output_dir / "prompt_tracking_report.md", tracking, feature_tracking)
    print(f"wrote prompt-tracking diagnostics to {safe_display_path(args.output_dir)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Diagnose whether selected feature effects track prompt-level subject-verb behavior variation."
    )
    parser.add_argument(
        "--prompts",
        type=Path,
        default=ROOT / "data" / "subject_verb_agreement" / "prompts.csv",
    )
    parser.add_argument(
        "--clean-metric-cache",
        type=Path,
        default=ROOT / "results" / "subject_verb_agreement" / "clean_metric_cache.csv",
    )
    parser.add_argument(
        "--exact-ablation-cache",
        type=Path,
        default=ROOT / "results" / "subject_verb_agreement" / "exact_ablation_cache.csv",
    )
    parser.add_argument(
        "--feature-stats",
        type=Path,
        default=ROOT / "results" / "subject_verb_agreement" / "cache_analysis" / "feature_stats.csv",
    )
    parser.add_argument(
        "--screen-scores",
        type=Path,
        default=ROOT / "results" / "subject_verb_agreement" / "screen_scores.csv",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "results" / "subject_verb_agreement" / "diagnostics",
    )
    return parser.parse_args()


def infer_full_prompt_effects(prompts: pd.DataFrame, clean_metrics: pd.DataFrame) -> pd.DataFrame:
    required_prompts = {"prompt_id", "clean_prompt", "patch_prompt", "split"}
    missing_prompts = required_prompts - set(prompts.columns)
    if missing_prompts:
        raise ValueError(f"prompts missing columns: {sorted(missing_prompts)}")
    required_metrics = {"prompt_id", "clean_prompt", "metric"}
    missing_metrics = required_metrics - set(clean_metrics.columns)
    if missing_metrics:
        raise ValueError(f"clean metric cache missing columns: {sorted(missing_metrics)}")

    metric_by_prompt_text = clean_metrics.set_index("clean_prompt")["metric"].to_dict()
    merged = prompts.merge(
        clean_metrics[["prompt_id", "metric"]],
        on="prompt_id",
        how="left",
        validate="one_to_one",
    )
    # Subject-verb patch rows swap target/counter labels, so the patch prompt's
    # own metric is the negative of the patch metric under the original labels.
    merged["patch_metric_inferred"] = -merged["patch_prompt"].map(metric_by_prompt_text)
    if merged["metric"].isna().any() or merged["patch_metric_inferred"].isna().any():
        raise ValueError("could not infer full clean-vs-patch effects for every prompt")
    merged["full_difference_inferred"] = merged["metric"] - merged["patch_metric_inferred"]
    keep = [
        col
        for col in [
            "prompt_id",
            "split",
            "template_id",
            "pair_id",
            "cluster_id",
            "metric",
            "patch_metric_inferred",
            "full_difference_inferred",
        ]
        if col in merged.columns
    ]
    return merged[keep].copy()


def additive_tracking_summary(
    *,
    exact_cache: pd.DataFrame,
    prompt_effects: pd.DataFrame,
    feature_stats: pd.DataFrame,
    screen_scores: pd.DataFrame,
) -> pd.DataFrame:
    method_sets = selected_feature_sets(feature_stats, screen_scores)
    rows = []
    for method, feature_ids in method_sets.items():
        selected = exact_cache[exact_cache["feature_id"].astype(int).isin(feature_ids)].copy()
        additive = (
            selected.groupby("prompt_id", as_index=False)["difference"]
            .sum()
            .rename(columns={"difference": "additive_selected_difference"})
        )
        merged = prompt_effects[prompt_effects["split"] == "test"].merge(additive, on="prompt_id", how="inner")
        if merged.empty:
            continue
        full = merged["full_difference_inferred"].to_numpy(dtype=float)
        selected_effect = merged["additive_selected_difference"].to_numpy(dtype=float)
        residual = full - selected_effect
        rows.append(
            {
                "method": method,
                "n_features": int(len(feature_ids)),
                "n_prompts": int(len(merged)),
                "full_mean": float(np.mean(full)),
                "full_std": float(np.std(full)),
                "additive_selected_mean": float(np.mean(selected_effect)),
                "additive_selected_std": float(np.std(selected_effect)),
                "additive_selected_full_corr": safe_corr(full, selected_effect),
                "additive_uncentered_completeness_r2": float(
                    1.0 - np.mean(residual**2) / max(np.mean(full**2), 1e-12)
                ),
                "additive_centered_r2": float(
                    1.0 - np.sum(residual**2) / max(np.sum((full - np.mean(full)) ** 2), 1e-12)
                ),
                "additive_abs_effect_fraction": float(
                    np.mean(np.abs(selected_effect)) / max(np.mean(np.abs(full)), 1e-12)
                ),
            }
        )
    return pd.DataFrame(rows).sort_values("method").reset_index(drop=True)


def selected_feature_sets(feature_stats: pd.DataFrame, screen_scores: pd.DataFrame) -> dict[str, set[int]]:
    out: dict[str, set[int]] = {}
    for col in feature_stats.columns:
        if col.startswith("selected_"):
            method = col.removeprefix("selected_")
            out[method] = set(feature_stats.loc[feature_stats[col].astype(bool), "feature_id"].astype(int))
    discoveries = {method: len(features) for method, features in out.items()}
    for method, k in discoveries.items():
        if k > 0:
            out[f"top_score_k_{method}"] = set(screen_scores.head(k)["feature_id"].astype(int))
    screened_k = int(feature_stats["feature_id"].nunique())
    out[f"top_score_k_screened_{screened_k}"] = set(screen_scores.head(screened_k)["feature_id"].astype(int))
    return out


def feature_prompt_tracking(
    exact_cache: pd.DataFrame,
    prompt_effects: pd.DataFrame,
    feature_stats: pd.DataFrame,
    screen_scores: pd.DataFrame,
) -> pd.DataFrame:
    merged = exact_cache.merge(
        prompt_effects[["prompt_id", "full_difference_inferred"]],
        on="prompt_id",
        how="left",
        validate="many_to_one",
    )
    rows = []
    for feature_id, group in merged.groupby("feature_id", sort=True):
        effect = group["difference"].to_numpy(dtype=float)
        full = group["full_difference_inferred"].to_numpy(dtype=float)
        rows.append(
            {
                "feature_id": int(feature_id),
                "effect_full_corr": safe_corr(effect, full),
                "effect_full_cov": safe_cov(effect, full),
                "effect_std": float(np.std(effect)),
            }
        )
    return (
        pd.DataFrame(rows)
        .merge(feature_stats, on="feature_id", how="left")
        .merge(screen_scores[["feature_id", "screen_rank", "screen_score"]], on="feature_id", how="left")
        .sort_values("screen_rank")
        .reset_index(drop=True)
    )


def safe_corr(x: np.ndarray, y: np.ndarray) -> float:
    if np.std(x) == 0.0 or np.std(y) == 0.0:
        return float("nan")
    return float(np.corrcoef(x, y)[0, 1])


def safe_cov(x: np.ndarray, y: np.ndarray) -> float:
    return float(np.mean((x - np.mean(x)) * (y - np.mean(y))))


def write_report(path: Path, tracking: pd.DataFrame, feature_tracking: pd.DataFrame) -> None:
    strongest_corr = feature_tracking.assign(abs_corr=feature_tracking["effect_full_corr"].abs()).sort_values(
        "abs_corr", ascending=False
    )
    lines = [
        "# Subject-Verb Prompt-Tracking Diagnostic",
        "",
        "This diagnostic uses the test split only and approximates a selected circuit",
        "by summing cached single-feature exact effects. It is not a replacement for",
        "held-out joint-circuit evaluation, but it tests whether the current mean-ATE",
        "selection criterion aligns with prompt-level behavior variation.",
        "",
        "## Additive Selected-Effect Tracking",
        tracking.to_markdown(index=False),
        "",
        "## Features With Largest Absolute Per-Prompt Correlation",
        strongest_corr[
            [
                "feature_id",
                "screen_rank",
                "tau_hat",
                "p_value",
                "effect_full_corr",
                "effect_full_cov",
                "effect_std",
            ]
        ]
        .head(20)
        .to_markdown(index=False),
        "",
        "## Interpretation",
        "- Low additive selected/full correlation means the existing feature-level test is not selecting for prompt-level covariance.",
        "- A new real circuit run should keep the resample-ablation cache, but evaluate prompt-tracking metrics explicitly after selection.",
        "- Final reporting must keep uncentered completeness and selected/full corr side by side.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def safe_display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    main()
