from __future__ import annotations

import numpy as np
import pandas as pd

from reliacircuit.fdr import bh, by_bh, e_bh, p_threshold, p_to_e_value
from reliacircuit.inference import infer_effect


REQUIRED_CACHE_COLUMNS = {"feature_id"}


def analyze_ablation_cache(
    cache: pd.DataFrame,
    q: float = 0.1,
    e_gamma: float = 0.5,
    n_bootstrap: int = 499,
    confidence: float = 0.95,
    seed: int = 0,
    ground_truth: pd.DataFrame | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Analyze exact-ablation cache from a GPU sweep.

    Required cache columns:
    - `feature_id`
    - either `difference`, or both `clean_metric` and `ablated_metric`

    Optional columns:
    - `cluster_id` for cluster bootstrap
    - `split`, where rows with split == "test" are used when present
    """
    _validate_cache(cache)
    work = cache.copy()
    if "split" in work.columns and (work["split"] == "test").any():
        work = work[work["split"] == "test"].copy()
    if "difference" not in work.columns:
        work["difference"] = work["clean_metric"] - work["ablated_metric"]

    rng = np.random.default_rng(seed)
    feature_rows = []
    for feature_id, group in work.groupby("feature_id", sort=True):
        diffs = group["difference"].to_numpy(dtype=float)
        cluster_ids = None
        if "cluster_id" in group.columns:
            cluster_ids = group["cluster_id"].to_numpy()
        effect = infer_effect(
            diffs,
            rng=rng,
            n_bootstrap=n_bootstrap,
            confidence=confidence,
            cluster_ids=cluster_ids,
        )
        feature_rows.append(
            {
                "feature_id": feature_id,
                "n": int(diffs.size),
                "tau_hat": effect.tau_hat,
                "se": effect.se,
                "t_stat": effect.t_stat,
                "p_value": effect.p_value,
                "e_value": float(p_to_e_value(np.array([effect.p_value]), gamma=e_gamma)[0]),
                "ci_lower": effect.ci_lower,
                "ci_upper": effect.ci_upper,
            }
        )

    feature_stats = pd.DataFrame(feature_rows)
    if ground_truth is not None:
        feature_stats = feature_stats.merge(ground_truth, on="feature_id", how="left")
        if "true_tau" in feature_stats.columns:
            feature_stats["ci_covers"] = (
                (feature_stats["ci_lower"] <= feature_stats["true_tau"])
                & (feature_stats["true_tau"] <= feature_stats["ci_upper"])
            )

    summary = summarize_cache_methods(feature_stats, q=q)
    return feature_stats, summary


def summarize_cache_methods(feature_stats: pd.DataFrame, q: float) -> pd.DataFrame:
    p = feature_stats["p_value"].to_numpy(dtype=float)
    e = feature_stats["e_value"].to_numpy(dtype=float)
    methods = {
        "e_bh_pcal": e_bh(e, q),
        "by_bh": by_bh(p, q),
        "bh": bh(p, q),
        "p_lt_q": p_threshold(p, q),
    }
    rows = []
    for method, reject in methods.items():
        row = {
            "method": method,
            "q": q,
            "discoveries": int(np.sum(reject)),
        }
        if "is_active" in feature_stats.columns:
            active = feature_stats["is_active"].fillna(False).to_numpy(dtype=bool)
            false_discoveries = int(np.sum(reject & ~active))
            true_discoveries = int(np.sum(reject & active))
            row.update(
                {
                    "false_discoveries": false_discoveries,
                    "true_discoveries": true_discoveries,
                    "fdp": false_discoveries / max(int(np.sum(reject)), 1),
                    "power": true_discoveries / max(int(np.sum(active)), 1),
                }
            )
        if "ci_covers" in feature_stats.columns and np.sum(reject) > 0:
            row["ci_coverage_selected"] = float(feature_stats.loc[reject, "ci_covers"].mean())
        rows.append(row)
        feature_stats[f"selected_{method}"] = reject
    return pd.DataFrame(rows)


def selected_feature_list(feature_stats: pd.DataFrame, method: str = "e_bh_pcal") -> pd.DataFrame:
    """Return selected features for one method in sweep-ready format."""
    flag = f"selected_{method}"
    if flag not in feature_stats.columns:
        raise ValueError(f"feature_stats does not contain {flag}; run summarize/analyze first")
    columns = [
        col
        for col in [
            "feature_id",
            "tau_hat",
            "se",
            "p_value",
            "e_value",
            "ci_lower",
            "ci_upper",
            "is_active",
            "true_tau",
        ]
        if col in feature_stats.columns
    ]
    selected = feature_stats.loc[feature_stats[flag].astype(bool), columns].copy()
    selected.insert(0, "selection_method", method)
    return selected.sort_values("p_value" if "p_value" in selected.columns else "feature_id")


def analyze_circuit_cache(cache: pd.DataFrame) -> pd.DataFrame:
    """Analyze joint circuit-level held-out cache.

    Required columns:
    - `prompt_id`
    - `method`
    - either `full_difference` and `selected_difference`, or metrics allowing
      them to be computed:
      `clean_metric`, `patch_metric`, and `selected_patch_metric`.
    """
    work = cache.copy()
    required = {"prompt_id", "method"}
    missing = required - set(work.columns)
    if missing:
        raise ValueError(f"circuit cache missing required columns: {sorted(missing)}")
    has_direct = {"full_difference", "selected_difference"}.issubset(work.columns)
    has_metrics = {"clean_metric", "patch_metric", "selected_patch_metric"}.issubset(work.columns)
    if not has_direct and not has_metrics:
        raise ValueError(
            "circuit cache must contain full/selected differences or clean/patch/selected metrics"
        )
    if "full_difference" not in work.columns:
        work["full_difference"] = work["clean_metric"] - work["patch_metric"]
    if "selected_difference" not in work.columns:
        work["selected_difference"] = work["clean_metric"] - work["selected_patch_metric"]

    rows = []
    for method, group in work.groupby("method", sort=False):
        rows.append({"method": method, "heldout_n": int(group.shape[0]), **_circuit_metrics(group)})
    return pd.DataFrame(rows)


def analyze_prompt_tracking_cache(
    cache: pd.DataFrame,
    prompt_effects: pd.DataFrame,
    q: float = 0.1,
    e_gamma: float = 0.5,
    n_bootstrap: int = 499,
    confidence: float = 0.95,
    seed: int = 0,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Analyze whether feature effects track prompt-level full behavior variation.

    This uses the same exact-ablation cache as the mean-ATE analysis, but changes
    the tested estimand from nonzero mean effect to nonzero covariance between a
    feature's per-prompt effect and the full clean-vs-patch prompt effect.
    """
    _validate_cache(cache)
    required_effects = {"prompt_id", "full_difference"}
    missing_effects = required_effects - set(prompt_effects.columns)
    if missing_effects:
        raise ValueError(f"prompt effects missing required columns: {sorted(missing_effects)}")

    work = cache.copy()
    if "split" in work.columns and (work["split"] == "test").any():
        work = work[work["split"] == "test"].copy()
    if "difference" not in work.columns:
        work["difference"] = work["clean_metric"] - work["ablated_metric"]
    work = work.merge(
        prompt_effects[["prompt_id", "full_difference"]],
        on="prompt_id",
        how="inner",
        validate="many_to_one",
    )
    if work.empty:
        raise ValueError("no exact-ablation rows overlap with prompt effects")

    rng = np.random.default_rng(seed)
    feature_rows = []
    for feature_id, group in work.groupby("feature_id", sort=True):
        effects = group["difference"].to_numpy(dtype=float)
        full = group["full_difference"].to_numpy(dtype=float)
        effect_centered = effects - np.mean(effects)
        full_centered = full - np.mean(full)
        covariance_samples = effect_centered * full_centered
        cluster_ids = None
        if "cluster_id" in group.columns:
            cluster_ids = group["cluster_id"].to_numpy()
        inference = infer_effect(
            covariance_samples,
            rng=rng,
            n_bootstrap=n_bootstrap,
            confidence=confidence,
            cluster_ids=cluster_ids,
        )
        effect_std = float(np.std(effects))
        full_std = float(np.std(full))
        corr = np.nan if effect_std == 0.0 or full_std == 0.0 else float(inference.tau_hat / (effect_std * full_std))
        feature_rows.append(
            {
                "feature_id": feature_id,
                "n": int(effects.size),
                "tau_hat": inference.tau_hat,
                "tracking_cov_hat": inference.tau_hat,
                "tracking_corr": corr,
                "tracking_slope_full_on_feature": float(
                    inference.tau_hat / max(float(np.var(effects)), 1e-12)
                ),
                "mean_effect_tau_hat": float(np.mean(effects)),
                "effect_std": effect_std,
                "full_effect_std": full_std,
                "se": inference.se,
                "t_stat": inference.t_stat,
                "p_value": inference.p_value,
                "e_value": float(p_to_e_value(np.array([inference.p_value]), gamma=e_gamma)[0]),
                "ci_lower": inference.ci_lower,
                "ci_upper": inference.ci_upper,
            }
        )

    feature_stats = pd.DataFrame(feature_rows)
    summary = summarize_cache_methods(feature_stats, q=q)
    return feature_stats, summary


def _circuit_metrics(group: pd.DataFrame) -> dict[str, float]:
    full = group["full_difference"].to_numpy(dtype=float)
    selected = group["selected_difference"].to_numpy(dtype=float)
    residual = full - selected
    full_mse = float(np.mean(full**2))
    residual_mse = float(np.mean(residual**2))
    selected_mse = float(np.mean(selected**2))
    centered_full_ss = float(np.sum((full - np.mean(full)) ** 2))
    residual_ss = float(np.sum(residual**2))
    abs_full = float(np.mean(np.abs(full)))
    abs_selected = float(np.mean(np.abs(selected)))
    if np.std(full) == 0.0 or np.std(selected) == 0.0:
        corr = np.nan
    else:
        corr = float(np.corrcoef(full, selected)[0, 1])
    sign_mask = np.abs(full) > 1e-12
    sign_agreement = np.nan
    if np.any(sign_mask):
        sign_agreement = float(np.mean(np.sign(full[sign_mask]) == np.sign(selected[sign_mask])))
    return {
        "heldout_full_mse": full_mse,
        "heldout_residual_mse": residual_mse,
        "heldout_selected_mse": selected_mse,
        "completeness_r2": float(1.0 - residual_mse / max(full_mse, 1e-12)),
        "centered_r2": float(1.0 - residual_ss / max(centered_full_ss, 1e-12)),
        "necessity_fraction": float(selected_mse / max(full_mse, 1e-12)),
        "abs_effect_fraction": float(abs_selected / max(abs_full, 1e-12)),
        "selected_full_corr": corr,
        "sign_agreement": sign_agreement,
    }


def _validate_cache(cache: pd.DataFrame) -> None:
    missing = REQUIRED_CACHE_COLUMNS - set(cache.columns)
    if missing:
        raise ValueError(f"cache is missing required columns: {sorted(missing)}")
    has_difference = "difference" in cache.columns
    has_metric_pair = {"clean_metric", "ablated_metric"}.issubset(cache.columns)
    if not has_difference and not has_metric_pair:
        raise ValueError("cache must contain `difference` or clean/ablated metric columns")
