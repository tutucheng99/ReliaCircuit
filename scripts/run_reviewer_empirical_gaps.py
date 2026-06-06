from __future__ import annotations

import argparse
import sys
from dataclasses import replace
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from reliacircuit.debias import (  # noqa: E402
    DebiasConfig,
    evaluate_mask,
    feature_gender_effects,
    generate_debias_dataset,
    split_train_indices,
)
from reliacircuit.fdr import bh, by_bh, e_bh, p_threshold, p_to_e_value  # noqa: E402
from subject_verb_layer_protocol import layer_specs  # noqa: E402


Q = 0.1


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    layers = load_layers()
    qf = qf_sensitivity(layers, q=args.q)
    pvals = pvalue_robustness(layers, q=args.q, n_resamples=args.pvalue_resamples, seed=args.seed)
    methods = method_comparison(layers, q=args.q, seed=args.seed)
    multisplit = multisplit_analysis(
        layers,
        q=args.q,
        n_splits=args.multisplit_repeats,
        seed=args.seed,
    )
    decoys = decoy_robustness(
        layers,
        q=args.q,
        n_repeats=args.decoy_repeats,
        seed=args.seed,
    )
    type_sm = type_sm_analysis(
        q=args.q,
        replicates=args.type_sm_replicates,
        seed=args.seed,
    )

    outputs = {
        "qf_sensitivity_summary.csv": qf,
        "pvalue_robustness_summary.csv": pvals,
        "method_comparison_summary.csv": methods,
        "multisplit_summary.csv": multisplit,
        "decoy_robustness_summary.csv": decoys,
        "type_sm_summary.csv": type_sm,
    }
    for name, frame in outputs.items():
        frame.to_csv(args.output_dir / name, index=False)
        (args.output_dir / name.replace(".csv", ".md")).write_text(
            frame.pipe(round_numeric).to_markdown(index=False),
            encoding="utf-8",
        )

    conclusions = reviewer_gap_conclusions(qf, pvals, methods, multisplit, decoys, type_sm)
    conclusions.to_csv(args.output_dir / "reviewer_gap_conclusions.csv", index=False)
    (args.output_dir / "reviewer_gap_conclusions.md").write_text(
        conclusions.to_markdown(index=False),
        encoding="utf-8",
    )
    plot_summary(qf, pvals, methods, multisplit, decoys, type_sm, args.output_dir / "reviewer_gap_summary.png")
    write_report(args.output_dir / "reviewer_empirical_gaps_report.md", conclusions, outputs)
    print(f"wrote reviewer empirical gap analyses to {safe_display_path(args.output_dir)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CPU-only empirical checks for reviewer-raised robustness gaps.")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "results" / "reviewer_empirical_gaps")
    parser.add_argument("--q", type=float, default=Q)
    parser.add_argument("--pvalue-resamples", type=int, default=999)
    parser.add_argument("--multisplit-repeats", type=int, default=80)
    parser.add_argument("--decoy-repeats", type=int, default=120)
    parser.add_argument("--type-sm-replicates", type=int, default=120)
    parser.add_argument("--seed", type=int, default=20260603)
    return parser.parse_args()


def load_layers() -> dict[str, dict[str, object]]:
    out: dict[str, dict[str, object]] = {}
    for spec in layer_specs():
        exact_path = spec.result_dir / "exact_ablation_cache.csv"
        score_path = spec.result_dir / "screen_scores.csv"
        if not exact_path.exists() or not score_path.exists():
            continue
        exact = pd.read_csv(exact_path)
        scores = pd.read_csv(score_path)
        matrix, prompt_meta, features = effect_matrix(exact)
        score_map = dict(zip(scores["feature_id"].astype(int), scores["screen_score"].astype(float)))
        score_vec = np.array([score_map[int(feature)] for feature in features], dtype=float)
        out[spec.label] = {
            "exact": exact,
            "matrix": matrix,
            "prompt_meta": prompt_meta,
            "features": features,
            "scores": score_vec,
        }
    if not out:
        raise FileNotFoundError("no completed subject-verb exact-ablation caches found")
    return out


def effect_matrix(exact_cache: pd.DataFrame) -> tuple[np.ndarray, pd.DataFrame, np.ndarray]:
    work = exact_cache.copy()
    if "difference" not in work.columns:
        work["difference"] = work["clean_metric"] - work["ablated_metric"]
    prompt_cols = [
        col
        for col in [
            "prompt_id",
            "cluster_id",
            "subject_number",
            "attractor_number",
            "behavior",
            "metric_mode",
        ]
        if col in work.columns
    ]
    prompt_meta = work[prompt_cols].drop_duplicates("prompt_id").sort_values("prompt_id").reset_index(drop=True)
    pivot = work.pivot(index="prompt_id", columns="feature_id", values="difference").reindex(prompt_meta["prompt_id"])
    features = pivot.columns.to_numpy(dtype=int)
    return pivot.to_numpy(dtype=float), prompt_meta, features


def qf_sensitivity(layers: dict[str, dict[str, object]], q: float) -> pd.DataFrame:
    rows = []
    for layer, payload in layers.items():
        matrix = payload["matrix"]
        prompt_meta = payload["prompt_meta"]
        scores = payload["scores"]
        base_p = p_values_t(np.asarray(matrix))
        base = all_method_masks(base_p, scores, q)
        base_ebh = base["e_bh_pcal"]
        variants = {
            "prompt_uniform_resample": np.asarray(matrix),
            "cluster_mean_resample": grouped_matrix(np.asarray(matrix), prompt_meta["cluster_id"].astype(str).to_numpy()),
            "subject_number_balanced": balanced_group_matrix(np.asarray(matrix), prompt_meta["subject_number"].astype(str).to_numpy()),
            "attractor_number_balanced": balanced_group_matrix(np.asarray(matrix), prompt_meta["attractor_number"].astype(str).to_numpy()),
            "winsorized_5_95": winsorized_matrix(np.asarray(matrix), lower=0.05, upper=0.95),
        }
        for variant, variant_matrix in variants.items():
            p = p_values_t(variant_matrix)
            masks = all_method_masks(p, scores, q)
            for method in ["e_bh_pcal", "bh", "by_bh", "p_lt_q", "weighted_bh_screen", "ihw_quantile"]:
                mask = masks[method]
                rows.append(
                    {
                        "gap": "qf_sensitivity",
                        "layer": layer,
                        "q_variant": variant,
                        "method": method,
                        "discoveries": int(mask.sum()),
                        "jaccard_to_prompt_uniform_ebh": jaccard(mask, base_ebh),
                        "recall_of_prompt_uniform_ebh": recall(mask, base_ebh),
                        "median_abs_tau": float(np.median(np.abs(np.mean(variant_matrix, axis=0)[mask]))) if mask.any() else 0.0,
                    }
                )
    return pd.DataFrame(rows).sort_values(["layer", "q_variant", "method"])


def pvalue_robustness(
    layers: dict[str, dict[str, object]],
    *,
    q: float,
    n_resamples: int,
    seed: int,
) -> pd.DataFrame:
    rows = []
    for layer, payload in layers.items():
        matrix = np.asarray(payload["matrix"])
        scores = np.asarray(payload["scores"])
        rng = np.random.default_rng(seed + stable_layer_offset(layer))
        p_methods = {
            "paired_t": p_values_t(matrix),
            "signflip_normal_approx": p_values_signflip_normal(matrix),
            "signflip_randomization": p_values_signflip(matrix, n_resamples=n_resamples, rng=rng),
            "centered_wild_bootstrap": p_values_wild_bootstrap(matrix, n_resamples=n_resamples, rng=rng),
        }
        base = all_method_masks(p_methods["paired_t"], scores, q)["e_bh_pcal"]
        for p_method, p in p_methods.items():
            masks = all_method_masks(p, scores, q)
            for method in ["e_bh_pcal", "bh", "by_bh", "p_lt_q"]:
                mask = masks[method]
                rows.append(
                    {
                        "gap": "pvalue_robustness",
                        "layer": layer,
                        "p_value_method": p_method,
                        "method": method,
                        "discoveries": int(mask.sum()),
                        "jaccard_to_paired_t_ebh": jaccard(mask, base),
                        "recall_of_paired_t_ebh": recall(mask, base),
                        "median_p_selected": float(np.median(p[mask])) if mask.any() else np.nan,
                    }
                )
    return pd.DataFrame(rows).sort_values(["layer", "p_value_method", "method"])


def method_comparison(
    layers: dict[str, dict[str, object]],
    *,
    q: float,
    seed: int,
) -> pd.DataFrame:
    rows = []
    for layer, payload in layers.items():
        matrix = np.asarray(payload["matrix"])
        scores = np.asarray(payload["scores"])
        p = p_values_t(matrix)
        masks = all_method_masks(p, scores, q)
        knock_mask, knock_stats = knockoff_pair_mask(matrix, scores, q, seed + stable_layer_offset(layer))
        masks["paired_knockoff_plus"] = knock_mask
        base = masks["e_bh_pcal"]
        for method, mask in masks.items():
            row = {
                "gap": "adaptive_knockoff_comparison",
                "layer": layer,
                "method": method,
                "discoveries": int(mask.sum()),
                "jaccard_to_ebh": jaccard(mask, base),
                "recall_of_ebh": recall(mask, base),
                "selection_rule": method_selection_rule(method),
                "knockoff_negative_count": np.nan,
                "knockoff_threshold": np.nan,
            }
            if method == "paired_knockoff_plus":
                row["knockoff_negative_count"] = knock_stats["negative_count"]
                row["knockoff_threshold"] = knock_stats["threshold"]
            rows.append(row)
    return pd.DataFrame(rows).sort_values(["layer", "method"])


def multisplit_analysis(
    layers: dict[str, dict[str, object]],
    *,
    q: float,
    n_splits: int,
    seed: int,
) -> pd.DataFrame:
    rows = []
    for layer, payload in layers.items():
        matrix = np.asarray(payload["matrix"])
        scores = np.asarray(payload["scores"])
        rng = np.random.default_rng(seed + 10_000 + stable_layer_offset(layer))
        base_p = p_values_t(matrix)
        base = all_method_masks(base_p, scores, q)["e_bh_pcal"]
        split_p = []
        split_masks = []
        n = matrix.shape[0]
        half = max(8, n // 2)
        for _ in range(n_splits):
            idx = rng.choice(n, size=half, replace=False)
            p = p_values_t(matrix[idx, :])
            split_p.append(p)
            split_masks.append(all_method_masks(p, scores, q)["e_bh_pcal"])
        p_stack = np.vstack(split_p)
        mask_stack = np.vstack(split_masks)
        selection_frequency = mask_stack.mean(axis=0)
        freq_mask = selection_frequency >= 0.5
        quantile_p = np.minimum(1.0, np.quantile(p_stack / 0.5, 0.5, axis=0))
        quantile_mask = all_method_masks(quantile_p, scores, q)["e_bh_pcal"]
        stouffer_p = crossfit_stouffer_p(matrix, n_folds=4)
        stouffer_mask = all_method_masks(stouffer_p, scores, q)["e_bh_pcal"]
        rows.extend(
            [
                multisplit_row(layer, "single_split_ebh", base, base, selection_frequency),
                multisplit_row(layer, "frequency_ge_0.5", freq_mask, base, selection_frequency),
                multisplit_row(layer, "multi_split_quantile_p", quantile_mask, base, selection_frequency),
                multisplit_row(layer, "crossfit_stouffer_4fold", stouffer_mask, base, selection_frequency),
            ]
        )
    return pd.DataFrame(rows).sort_values(["layer", "aggregation"])


def decoy_robustness(
    layers: dict[str, dict[str, object]],
    *,
    q: float,
    n_repeats: int,
    seed: int,
) -> pd.DataFrame:
    rows = []
    for layer, payload in layers.items():
        matrix = np.asarray(payload["matrix"])
        scores = np.asarray(payload["scores"])
        rng = np.random.default_rng(seed + 20_000 + stable_layer_offset(layer))
        real_p = p_values_t(matrix)
        real_e = p_to_e_value(real_p)
        for decoy_scheme in ["high_score_signflip", "random_score_signflip", "low_score_signflip", "centered_permutation"]:
            run_rows = []
            for rep in range(n_repeats):
                decoy_matrix, decoy_scores = make_decoy_matrix(matrix, scores, decoy_scheme, rng)
                decoy_p = p_values_t(decoy_matrix)
                decoy_e = p_to_e_value(decoy_p)
                p = np.concatenate([real_p, decoy_p])
                e = np.concatenate([real_e, decoy_e])
                combined_scores = np.concatenate([scores, decoy_scores])
                is_decoy = np.concatenate([np.zeros(real_p.size, dtype=bool), np.ones(decoy_p.size, dtype=bool)])
                masks = all_method_masks_from_pe(p, e, combined_scores, q)
                for method in ["e_bh_pcal", "by_bh", "bh", "p_lt_q", "weighted_bh_screen", "ihw_quantile", "adapt_lite", "top_score_matched_e_bh_pcal"]:
                    if method == "top_score_matched_e_bh_pcal":
                        k = int(masks["e_bh_pcal"].sum())
                        mask = top_score_mask(combined_scores, k)
                        selection_rule = "manual_k_equal_to_e_bh"
                    else:
                        mask = masks[method]
                        selection_rule = method_selection_rule(method)
                    run_rows.append(decoy_eval_row(layer, decoy_scheme, rep, method, selection_rule, mask, is_decoy))
            summary = summarize_decoy_runs(pd.DataFrame(run_rows))
            rows.append(summary)
    return pd.concat(rows, ignore_index=True).sort_values(["layer", "decoy_scheme", "method"])


def type_sm_analysis(*, q: float, replicates: int, seed: int) -> pd.DataFrame:
    cfg = DebiasConfig(seed=seed)
    rows = []
    for rep in range(replicates):
        rep_cfg = replace(cfg, seed=cfg.seed + rep)
        dataset = generate_debias_dataset(rep_cfg)
        rng = np.random.default_rng(rep_cfg.seed + 9173)
        screen_idx, infer_idx = split_train_indices(rep_cfg, rng)
        features = feature_gender_effects(dataset, screen_idx, infer_idx, rep_cfg)
        true_effect = dataset.weights * true_residualized_gender_coefficients(dataset.x_test, dataset.y_test, dataset.g_test)
        features["true_gender_effect"] = true_effect
        masks = debias_method_masks(features, dataset, rep_cfg, rng)
        for method, mask in masks.items():
            selected = features.loc[mask].copy()
            metrics = evaluate_mask(dataset, mask)
            task_removed = int(np.sum(mask & dataset.is_task))
            spurious_removed = int(np.sum(mask & dataset.is_spurious))
            proxy_removed = int(np.sum(mask & dataset.is_proxy))
            noise_removed = int(np.sum(mask & ~(dataset.is_task | dataset.is_spurious | dataset.is_proxy)))
            nonzero = selected[np.abs(selected["true_gender_effect"]) > 1e-8]
            type_s = np.nan
            type_m = np.nan
            if not nonzero.empty:
                type_s = float(np.mean(np.sign(nonzero["tau_gender"]) != np.sign(nonzero["true_gender_effect"])))
                type_m = float(np.median(np.abs(nonzero["tau_gender"] / nonzero["true_gender_effect"])))
            rows.append(
                {
                    "replicate": rep,
                    "method": method,
                    "removed": int(mask.sum()),
                    "task_removed": task_removed,
                    "spurious_removed": spurious_removed,
                    "proxy_removed": proxy_removed,
                    "noise_removed": noise_removed,
                    "task_irrelevant_harmful_recall": spurious_removed / max(int(dataset.is_spurious.sum()), 1),
                    "task_feature_removal_rate": task_removed / max(int(mask.sum()), 1),
                    "proxy_or_noise_removal_rate": (proxy_removed + noise_removed) / max(int(mask.sum()), 1),
                    "type_s_rate_selected_nonzero": type_s,
                    "type_m_median_selected_nonzero": type_m,
                    **metrics,
                }
            )
    frame = pd.DataFrame(rows)
    metrics = [
        "removed",
        "task_removed",
        "spurious_removed",
        "proxy_removed",
        "noise_removed",
        "task_irrelevant_harmful_recall",
        "task_feature_removal_rate",
        "proxy_or_noise_removal_rate",
        "type_s_rate_selected_nonzero",
        "type_m_median_selected_nonzero",
        "worst_group_acc",
        "conflict_acc",
        "gap_aligned_conflict",
    ]
    out_rows = []
    for method, group in frame.groupby("method", sort=False):
        row = {"gap": "type_s_m_debias", "method": method, "replicates": int(group.shape[0])}
        for metric in metrics:
            values = group[metric].dropna()
            row[f"{metric}_mean"] = float(values.mean()) if not values.empty else np.nan
            row[f"{metric}_se"] = float(values.std(ddof=1) / np.sqrt(values.shape[0])) if values.shape[0] > 1 else 0.0
        out_rows.append(row)
    return pd.DataFrame(out_rows).sort_values("method")


def grouped_matrix(matrix: np.ndarray, labels: np.ndarray) -> np.ndarray:
    rows = []
    for label in pd.Series(labels).drop_duplicates().tolist():
        rows.append(matrix[labels == label].mean(axis=0))
    return np.vstack(rows)


def balanced_group_matrix(matrix: np.ndarray, labels: np.ndarray) -> np.ndarray:
    unique, counts = np.unique(labels, return_counts=True)
    min_count = int(counts.min())
    rows = []
    for label in unique:
        idx = np.flatnonzero(labels == label)[:min_count]
        rows.append(matrix[idx])
    return np.vstack(rows)


def winsorized_matrix(matrix: np.ndarray, *, lower: float, upper: float) -> np.ndarray:
    lo = np.quantile(matrix, lower, axis=0, keepdims=True)
    hi = np.quantile(matrix, upper, axis=0, keepdims=True)
    return np.clip(matrix, lo, hi)


def p_values_t(matrix: np.ndarray) -> np.ndarray:
    matrix = np.asarray(matrix, dtype=float)
    means = np.mean(matrix, axis=0)
    se = np.std(matrix, axis=0, ddof=1) / np.sqrt(matrix.shape[0])
    t_stat = np.divide(means, se, out=np.zeros_like(means), where=se > 0)
    p = 2.0 * stats.t.sf(np.abs(t_stat), df=max(matrix.shape[0] - 1, 1))
    p = np.where((se == 0.0) & (means != 0.0), 0.0, p)
    p = np.where((se == 0.0) & (means == 0.0), 1.0, p)
    return np.clip(p.astype(float), 0.0, 1.0)


def p_values_signflip(matrix: np.ndarray, *, n_resamples: int, rng: np.random.Generator) -> np.ndarray:
    matrix = np.asarray(matrix, dtype=float)
    obs = np.abs(np.mean(matrix, axis=0))
    counts = np.zeros(matrix.shape[1], dtype=int)
    chunk = 250
    for start in range(0, n_resamples, chunk):
        size = min(chunk, n_resamples - start)
        signs = rng.choice([-1.0, 1.0], size=(size, matrix.shape[0]))
        null_means = np.abs(signs @ matrix / matrix.shape[0])
        counts += np.sum(null_means >= obs[None, :], axis=0)
    return (counts + 1.0) / (n_resamples + 1.0)


def p_values_signflip_normal(matrix: np.ndarray) -> np.ndarray:
    matrix = np.asarray(matrix, dtype=float)
    obs = np.mean(matrix, axis=0)
    randomization_se = np.sqrt(np.sum(matrix**2, axis=0)) / matrix.shape[0]
    z = np.divide(obs, randomization_se, out=np.zeros_like(obs), where=randomization_se > 0)
    p = 2.0 * stats.norm.sf(np.abs(z))
    p = np.where((randomization_se == 0.0) & (obs != 0.0), 0.0, p)
    p = np.where((randomization_se == 0.0) & (obs == 0.0), 1.0, p)
    return np.clip(p.astype(float), 0.0, 1.0)


def p_values_wild_bootstrap(matrix: np.ndarray, *, n_resamples: int, rng: np.random.Generator) -> np.ndarray:
    matrix = np.asarray(matrix, dtype=float)
    centered = matrix - np.mean(matrix, axis=0, keepdims=True)
    obs = np.abs(np.mean(matrix, axis=0))
    counts = np.zeros(matrix.shape[1], dtype=int)
    chunk = 250
    for start in range(0, n_resamples, chunk):
        size = min(chunk, n_resamples - start)
        signs = rng.choice([-1.0, 1.0], size=(size, centered.shape[0]))
        null_means = np.abs(signs @ centered / centered.shape[0])
        counts += np.sum(null_means >= obs[None, :], axis=0)
    return (counts + 1.0) / (n_resamples + 1.0)


def all_method_masks(p_values: np.ndarray, scores: np.ndarray, q: float) -> dict[str, np.ndarray]:
    return all_method_masks_from_pe(p_values, p_to_e_value(p_values), scores, q)


def all_method_masks_from_pe(p_values: np.ndarray, e_values: np.ndarray, scores: np.ndarray, q: float) -> dict[str, np.ndarray]:
    masks = {
        "e_bh_pcal": e_bh(e_values, q),
        "by_bh": by_bh(p_values, q),
        "bh": bh(p_values, q),
        "p_lt_q": p_threshold(p_values, q),
        "weighted_bh_screen": weighted_bh(p_values, score_weights(scores), q),
        "ihw_quantile": ihw_quantile_bh(p_values, scores, q),
        "adapt_lite": weighted_bh(p_values, adapt_lite_weights(p_values, scores), q),
    }
    return masks


def weighted_bh(p_values: np.ndarray, weights: np.ndarray, q: float) -> np.ndarray:
    weights = np.asarray(weights, dtype=float)
    weights = weights / max(float(np.mean(weights)), 1e-12)
    adjusted = np.minimum(1.0, p_values / np.clip(weights, 1e-6, None))
    return bh(adjusted, q)


def score_weights(scores: np.ndarray) -> np.ndarray:
    ranks = stats.rankdata(scores, method="average")
    scaled = (ranks - 0.5) / max(len(ranks), 1)
    return 0.25 + 1.5 * scaled


def ihw_quantile_bh(p_values: np.ndarray, scores: np.ndarray, q: float, n_bins: int = 4) -> np.ndarray:
    bins = pd.qcut(pd.Series(scores).rank(method="first"), q=n_bins, labels=False, duplicates="drop").to_numpy()
    reject = np.zeros(p_values.size, dtype=bool)
    bin_ids = np.unique(bins)
    bin_scores = np.array([np.mean(scores[bins == b]) for b in bin_ids], dtype=float)
    allocations = score_weights(bin_scores)
    allocations = allocations / allocations.sum()
    for b, alloc in zip(bin_ids, allocations):
        idx = np.flatnonzero(bins == b)
        reject[idx] = bh(p_values[idx], q * float(alloc))
    return reject


def adapt_lite_weights(p_values: np.ndarray, scores: np.ndarray, n_bins: int = 4) -> np.ndarray:
    bins = pd.qcut(pd.Series(scores).rank(method="first"), q=n_bins, labels=False, duplicates="drop").to_numpy()
    weights = np.ones(p_values.size, dtype=float)
    for b in np.unique(bins):
        idx = np.flatnonzero(bins == b)
        pi0 = min(1.0, max(0.1, float(np.mean(p_values[idx] > 0.5) / 0.5)))
        weights[idx] = 1.0 / pi0
    return weights


def knockoff_pair_mask(matrix: np.ndarray, scores: np.ndarray, q: float, seed: int) -> tuple[np.ndarray, dict[str, float]]:
    rng = np.random.default_rng(seed)
    decoy_matrix, _decoy_scores = make_decoy_matrix(matrix, scores, "centered_permutation", rng)
    stat_real = -np.log10(np.clip(p_values_t(matrix), 1e-300, 1.0)) * score_weights(scores)
    stat_decoy = -np.log10(np.clip(p_values_t(decoy_matrix), 1e-300, 1.0)) * score_weights(scores)
    w = stat_real - stat_decoy
    positive = np.sort(np.unique(np.abs(w[w > 0])))
    threshold = np.inf
    for t in positive:
        ratio = (1.0 + float(np.sum(w <= -t))) / max(float(np.sum(w >= t)), 1.0)
        if ratio <= q:
            threshold = float(t)
            break
    mask = w >= threshold if np.isfinite(threshold) else np.zeros(w.size, dtype=bool)
    return mask, {"threshold": threshold, "negative_count": int(np.sum(w <= -threshold)) if np.isfinite(threshold) else 0}


def crossfit_stouffer_p(matrix: np.ndarray, n_folds: int) -> np.ndarray:
    folds = np.array_split(np.arange(matrix.shape[0]), n_folds)
    z_rows = []
    for fold in folds:
        p = p_values_t(matrix[fold, :])
        means = np.mean(matrix[fold, :], axis=0)
        signed_z = stats.norm.isf(np.clip(p / 2.0, 1e-300, 1.0)) * np.sign(means)
        z_rows.append(signed_z)
    z = np.sum(np.vstack(z_rows), axis=0) / np.sqrt(n_folds)
    return np.clip(2.0 * stats.norm.sf(np.abs(z)), 0.0, 1.0)


def make_decoy_matrix(
    matrix: np.ndarray,
    scores: np.ndarray,
    scheme: str,
    rng: np.random.Generator,
) -> tuple[np.ndarray, np.ndarray]:
    n, m = matrix.shape
    order = np.argsort(-scores)
    if scheme == "centered_permutation":
        centered = matrix - np.mean(matrix, axis=0, keepdims=True)
        out = np.empty_like(centered)
        for j in range(m):
            out[:, j] = centered[rng.permutation(n), j]
        return out[:, order], scores[order]
    signs = rng.choice([-1.0, 1.0], size=matrix.shape)
    decoy = matrix[:, order] * signs
    if scheme == "high_score_signflip":
        decoy_scores = scores[order] + 1000.0
    elif scheme == "random_score_signflip":
        decoy_scores = rng.permutation(scores)
    elif scheme == "low_score_signflip":
        decoy_scores = -np.abs(scores[order]) - 1000.0
    else:
        raise ValueError(f"unknown decoy scheme {scheme}")
    return decoy, decoy_scores


def multisplit_row(
    layer: str,
    aggregation: str,
    mask: np.ndarray,
    base: np.ndarray,
    selection_frequency: np.ndarray,
) -> dict[str, object]:
    selected_freq = selection_frequency[mask]
    return {
        "gap": "multi_split_crossfit",
        "layer": layer,
        "aggregation": aggregation,
        "discoveries": int(mask.sum()),
        "jaccard_to_single_split_ebh": jaccard(mask, base),
        "recall_of_single_split_ebh": recall(mask, base),
        "mean_selection_frequency_selected": float(np.mean(selected_freq)) if selected_freq.size else np.nan,
    }


def decoy_eval_row(
    layer: str,
    decoy_scheme: str,
    repeat: int,
    method: str,
    selection_rule: str,
    mask: np.ndarray,
    is_decoy: np.ndarray,
) -> dict[str, object]:
    discoveries = int(mask.sum())
    decoys = int(np.sum(mask & is_decoy))
    return {
        "layer": layer,
        "decoy_scheme": decoy_scheme,
        "repeat": repeat,
        "method": method,
        "selection_rule": selection_rule,
        "discoveries": discoveries,
        "known_null_decoys_selected": decoys,
        "known_null_fdp": decoys / max(discoveries, 1),
    }


def summarize_decoy_runs(runs: pd.DataFrame) -> pd.DataFrame:
    return (
        runs.groupby(["layer", "decoy_scheme", "method", "selection_rule"], as_index=False)
        .agg(
            discoveries_mean=("discoveries", "mean"),
            discoveries_std=("discoveries", "std"),
            known_null_decoys_selected_mean=("known_null_decoys_selected", "mean"),
            known_null_decoys_selected_std=("known_null_decoys_selected", "std"),
            known_null_fdp_mean=("known_null_fdp", "mean"),
            known_null_fdp_std=("known_null_fdp", "std"),
        )
    )


def debias_method_masks(features: pd.DataFrame, dataset, config: DebiasConfig, rng: np.random.Generator) -> dict[str, np.ndarray]:
    p = features["p_value"].to_numpy(float)
    e = features["e_value"].to_numpy(float)
    scores = features["screen_score"].to_numpy(float)
    masks = {
        "e_bh_pcal": e_bh(e, config.q),
        "by_bh": by_bh(p, config.q),
        "bh": bh(p, config.q),
        "p_lt_q": p_threshold(p, config.q),
        "top_score_k_spurious": top_score_mask(np.abs(scores), int(dataset.is_spurious.sum())),
    }
    return masks


def true_residualized_gender_coefficients(x: np.ndarray, y: np.ndarray, g: np.ndarray) -> np.ndarray:
    residual_x = np.empty_like(x, dtype=float)
    residual_g = np.empty_like(g, dtype=float)
    for label in [-1, 1]:
        mask = y == label
        residual_x[mask] = x[mask] - np.mean(x[mask], axis=0, keepdims=True)
        residual_g[mask] = g[mask] - float(np.mean(g[mask]))
    denom = float(np.mean(residual_g**2))
    return np.mean(residual_x * residual_g[:, None], axis=0) / max(denom, 1e-12)


def top_score_mask(scores: np.ndarray, k: int) -> np.ndarray:
    mask = np.zeros(scores.size, dtype=bool)
    if k > 0:
        mask[np.argsort(-scores)[: min(k, scores.size)]] = True
    return mask


def method_selection_rule(method: str) -> str:
    if method == "e_bh_pcal":
        return "e_bh_p_calibrated"
    if method in {"bh", "by_bh", "weighted_bh_screen", "ihw_quantile", "adapt_lite"}:
        return "p_value_fdr"
    if method == "p_lt_q":
        return "uncorrected_p_threshold"
    if method == "paired_knockoff_plus":
        return "paired_decoy_knockoff_plus"
    return "manual_or_other"


def jaccard(mask: np.ndarray, reference: np.ndarray) -> float:
    union = int(np.sum(mask | reference))
    if union == 0:
        return 1.0
    return float(np.sum(mask & reference) / union)


def recall(mask: np.ndarray, reference: np.ndarray) -> float:
    denom = int(np.sum(reference))
    if denom == 0:
        return 1.0 if int(np.sum(mask)) == 0 else 0.0
    return float(np.sum(mask & reference) / denom)


def stable_layer_offset(layer: str) -> int:
    return sum((idx + 1) * ord(ch) for idx, ch in enumerate(layer))


def reviewer_gap_conclusions(
    qf: pd.DataFrame,
    pvals: pd.DataFrame,
    methods: pd.DataFrame,
    multisplit: pd.DataFrame,
    decoys: pd.DataFrame,
    type_sm: pd.DataFrame,
) -> pd.DataFrame:
    qf_ebh = qf[(qf["method"] == "e_bh_pcal") & (qf["q_variant"] != "prompt_uniform_resample")]
    p_ebh = pvals[pvals["method"] == "e_bh_pcal"]
    p_signflip = p_ebh[p_ebh["p_value_method"] == "signflip_normal_approx"]
    method_alt = methods[methods["method"].isin(["weighted_bh_screen", "ihw_quantile", "adapt_lite", "paired_knockoff_plus"])]
    adaptive_alt = methods[methods["method"].isin(["weighted_bh_screen", "ihw_quantile", "adapt_lite"])]
    knockoff_alt = methods[methods["method"] == "paired_knockoff_plus"]
    decoy_ebh = decoys[decoys["method"] == "e_bh_pcal"]
    decoy_top = decoys[decoys["method"] == "top_score_matched_e_bh_pcal"]
    multi_focus = multisplit[multisplit["aggregation"].isin(["multi_split_quantile_p", "crossfit_stouffer_4fold"])]
    type_focus = type_sm[type_sm["method"].isin(["e_bh_pcal", "top_score_k_spurious"])]

    rows = [
        {
            "gap": "Q_f sensitivity",
            "status": "empirical_conclusion",
            "headline_metric": f"e-BH median Jaccard across non-baseline Q_f variants={qf_ebh['jaccard_to_prompt_uniform_ebh'].median():.3f}",
            "conclusion": "Reasonable CPU reweightings of the cached resample-ablation estimand preserve the core e-BH selections at moderate-to-high overlap; any layer-specific deviations are reported as sensitivity, not hidden.",
            "table": "table_12_reviewer_qf_sensitivity",
        },
        {
            "gap": "Permutation/bootstrap p-values",
            "status": "empirical_conclusion",
            "headline_metric": f"sign-flip normal e-BH median Jaccard to paired-t={p_signflip['jaccard_to_paired_t_ebh'].median():.3f}; finite-MC variants are resolution-limited",
            "conclusion": "The sign-flip randomization normal approximation gives comparable e-BH conclusions to paired-t. Finite Monte Carlo randomization/bootstrap p-values are valid but too discrete for p-to-e e-BH at practical resample counts, making them useful as conservative sensitivity checks rather than replacements.",
            "table": "table_13_reviewer_pvalue_robustness",
        },
        {
            "gap": "Covariate-adaptive and knockoff alternatives",
            "status": "empirical_conclusion",
            "headline_metric": f"adaptive median discoveries={adaptive_alt['discoveries'].median():.1f}; paired-decoy knockoff median discoveries={knockoff_alt['discoveries'].median():.1f}",
            "conclusion": "Screen-covariate weighting/IHW/AdaPT-lite can recover additional discoveries in some layers, but decoy robustness must be checked. The paired-decoy knockoff-plus diagnostic is not a formal model-X knockoff result here and selects all candidates in this cache, so it is reported as a failed/over-liberal comparator rather than a viable replacement.",
            "table": "table_14_reviewer_method_comparison",
        },
        {
            "gap": "Multi-split/cross-fitting",
            "status": "empirical_conclusion",
            "headline_metric": f"median Jaccard to single split={multi_focus['jaccard_to_single_split_ebh'].median():.3f}",
            "conclusion": "Multi-split aggregation and four-fold Stouffer cross-fitting generally trade discoveries for higher selection reproducibility; they are viable stability checks rather than clear replacements.",
            "table": "table_15_reviewer_multisplit",
        },
        {
            "gap": "Decoy construction robustness",
            "status": "empirical_conclusion",
            "headline_metric": f"e-BH decoys mean={decoy_ebh['known_null_decoys_selected_mean'].mean():.3f}; matched top-score decoys mean={decoy_top['known_null_decoys_selected_mean'].mean():.3f}",
            "conclusion": "Across high-score, random-score, low-score, and centered-permutation decoys, e-BH keeps constructed null decoys near zero while top-score only fails when decoys are screen-attractive; this separates FDR reliability from screen-rank artifacts.",
            "table": "table_16_reviewer_decoy_robustness",
        },
        {
            "gap": "Downstream Type S/M",
            "status": "empirical_conclusion",
            "headline_metric": "; ".join(
                f"{row.method}: TypeS={row.type_s_rate_selected_nonzero_mean:.3f}, TypeM={row.type_m_median_selected_nonzero_mean:.2f}"
                for row in type_focus.itertuples(index=False)
            ),
            "conclusion": "Task-irrelevant harmful features are operationalized as non-task spurious features with nonzero downstream model weight; Type S errors are low for controlled selections, while top-score can remove more proxy/noise features.",
            "table": "table_17_reviewer_type_sm",
        },
    ]
    return pd.DataFrame(rows)


def plot_summary(
    qf: pd.DataFrame,
    pvals: pd.DataFrame,
    methods: pd.DataFrame,
    multisplit: pd.DataFrame,
    decoys: pd.DataFrame,
    type_sm: pd.DataFrame,
    path: Path,
) -> None:
    fig, axes = plt.subplots(2, 3, figsize=(15, 8), constrained_layout=True)
    qf_plot = qf[qf["method"] == "e_bh_pcal"].groupby("q_variant")["jaccard_to_prompt_uniform_ebh"].mean()
    axes[0, 0].bar(qf_plot.index, qf_plot.values)
    axes[0, 0].set_title("Q_f sensitivity")
    axes[0, 0].tick_params(axis="x", rotation=35)
    axes[0, 0].set_ylim(0, 1.05)

    p_plot = pvals[pvals["method"] == "e_bh_pcal"].groupby("p_value_method")["jaccard_to_paired_t_ebh"].mean()
    axes[0, 1].bar(p_plot.index, p_plot.values)
    axes[0, 1].set_title("p-value robustness")
    axes[0, 1].tick_params(axis="x", rotation=35)
    axes[0, 1].set_ylim(0, 1.05)

    m_plot = methods.groupby("method")["discoveries"].mean()
    axes[0, 2].bar(m_plot.index, m_plot.values)
    axes[0, 2].set_title("Alternative methods")
    axes[0, 2].tick_params(axis="x", rotation=55)

    ms_plot = multisplit.groupby("aggregation")["jaccard_to_single_split_ebh"].mean()
    axes[1, 0].bar(ms_plot.index, ms_plot.values)
    axes[1, 0].set_title("Multi-split overlap")
    axes[1, 0].tick_params(axis="x", rotation=45)
    axes[1, 0].set_ylim(0, 1.05)

    d_plot = decoys[decoys["method"].isin(["e_bh_pcal", "p_lt_q", "top_score_matched_e_bh_pcal"])].groupby("method")["known_null_decoys_selected_mean"].mean()
    axes[1, 1].bar(d_plot.index, d_plot.values)
    axes[1, 1].set_title("Decoy robustness")
    axes[1, 1].tick_params(axis="x", rotation=35)

    ts_plot = type_sm[type_sm["method"].isin(["e_bh_pcal", "top_score_k_spurious"])].set_index("method")["type_s_rate_selected_nonzero_mean"]
    axes[1, 2].bar(ts_plot.index, ts_plot.values)
    axes[1, 2].set_title("Type S rate")
    axes[1, 2].set_ylim(0, 1.05)
    axes[1, 2].tick_params(axis="x", rotation=35)

    fig.savefig(path, dpi=180)
    plt.close(fig)


def write_report(path: Path, conclusions: pd.DataFrame, outputs: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Reviewer Empirical Gap Analyses",
        "",
        "This report is generated by `scripts/run_reviewer_empirical_gaps.py`.",
        "It uses existing real subject-verb caches plus CPU-only synthetic",
        "downstream simulations. No new GPU cache is produced here.",
        "",
        "## Conclusions",
        "",
        conclusions.to_markdown(index=False),
        "",
    ]
    for name, frame in outputs.items():
        lines.extend([f"## {name}", "", frame.pipe(round_numeric).to_markdown(index=False), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def round_numeric(table: pd.DataFrame) -> pd.DataFrame:
    out = table.copy()
    for col in out.columns:
        if pd.api.types.is_numeric_dtype(out[col]):
            out[col] = out[col].round(4)
    return out


def safe_display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT.resolve())).replace("\\", "/")
    except ValueError:
        return str(path)


if __name__ == "__main__":
    main()
