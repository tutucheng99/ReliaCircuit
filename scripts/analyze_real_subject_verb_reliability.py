from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
sys.path.insert(0, str(ROOT / "src"))

from reliacircuit.fdr import bh, by_bh, e_bh, p_threshold, p_to_e_value  # noqa: E402
from subject_verb_layer_protocol import layer_specs, layer_status, required_layer_files  # noqa: E402


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    status = layer_status(args.protocol)
    status.to_csv(args.output_dir / "layer_protocol_status.csv", index=False)
    if not args.allow_missing and (status["status"] != "complete").any():
        missing = status[status["status"] != "complete"][["layer", "missing_files"]]
        raise SystemExit("layer scan protocol is incomplete:\n" + missing.to_string(index=False))

    q_rows = []
    stability_rows = []
    decoy_rows = []
    layer_rows = []
    for spec in layer_specs(args.protocol):
        required = required_layer_files(spec)
        missing = [name for name, path in required.items() if not path.exists()]
        if missing:
            if args.allow_missing:
                continue
            raise SystemExit(f"{spec.label} missing required files: {', '.join(missing)}")
        out = args.output_dir / spec.label.lower()
        out.mkdir(parents=True, exist_ok=True)
        feature_stats = pd.read_csv(spec.result_dir / "cache_analysis" / "feature_stats.csv")
        tracking_stats = pd.read_csv(spec.result_dir / "cache_analysis" / "feature_stats_tracking.csv")
        screen_scores = pd.read_csv(spec.result_dir / "screen_scores.csv")
        exact_cache = pd.read_csv(spec.result_dir / "exact_ablation_cache.csv")
        comparison = pd.read_csv(spec.result_dir / "method_reliability_tracking_comparison.csv")
        prompt_effects = pd.read_csv(spec.result_dir / "cache_analysis" / "prompt_full_effects_exact.csv")

        q_grid = q_grid_for_layer(spec.label, feature_stats, tracking_stats, args.q_values)
        q_grid.to_csv(out / "real_q_grid.csv", index=False)
        q_rows.append(q_grid)

        stability = stability_for_layer(
            spec.label,
            exact_cache,
            prompt_effects,
            feature_stats,
            tracking_stats,
            q=args.q,
            n_resamples=args.stability_resamples,
            seed=args.seed,
        )
        stability.to_csv(out / "selection_stability_runs.csv", index=False)
        stability_summary = summarize_stability(stability)
        stability_summary.to_csv(out / "selection_stability_summary.csv", index=False)
        stability_rows.append(stability_summary)

        decoys = decoy_reliability_for_layer(
            spec.label,
            exact_cache,
            screen_scores,
            q=args.q,
            n_repeats=args.decoy_repeats,
            seed=args.seed,
        )
        decoys.to_csv(out / "decoy_reliability_runs.csv", index=False)
        decoy_summary = summarize_decoys(decoys)
        decoy_summary.to_csv(out / "decoy_reliability_summary.csv", index=False)
        decoy_rows.append(decoy_summary)

        layer_scan = layer_scan_rows(spec.label, comparison)
        layer_scan.to_csv(out / "layer_scan_summary.csv", index=False)
        layer_rows.append(layer_scan)

        write_layer_report(out / "real_reliability_report.md", spec.label, q_grid, stability_summary, decoy_summary, layer_scan)

    if not q_rows:
        raise SystemExit("no complete layer specs were available for reliability analysis")
    all_q = pd.concat(q_rows, ignore_index=True)
    all_stability = pd.concat(stability_rows, ignore_index=True)
    all_decoys = pd.concat(decoy_rows, ignore_index=True)
    all_layers = pd.concat(layer_rows, ignore_index=True)
    all_q.to_csv(args.output_dir / "real_q_grid.csv", index=False)
    all_stability.to_csv(args.output_dir / "selection_stability_summary.csv", index=False)
    all_decoys.to_csv(args.output_dir / "decoy_reliability_summary.csv", index=False)
    all_layers.to_csv(args.output_dir / "layer_scan_summary.csv", index=False)
    write_combined_report(
        args.output_dir / "real_subject_verb_reliability_report.md",
        all_q,
        all_stability,
        all_decoys,
        all_layers,
    )
    print(f"wrote real subject-verb reliability analyses to {safe_display_path(args.output_dir)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CPU-only reliability analyses for real subject-verb caches.")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "results" / "real_subject_verb_reliability")
    parser.add_argument(
        "--protocol",
        type=Path,
        default=ROOT / "configs" / "subject_verb_layer_scan_protocol.json",
    )
    parser.add_argument("--allow-missing", action="store_true")
    parser.add_argument("--q", type=float, default=0.1)
    parser.add_argument("--q-values", type=float, nargs="+", default=[0.01, 0.02, 0.05, 0.1, 0.15, 0.2, 0.3])
    parser.add_argument("--stability-resamples", type=int, default=200)
    parser.add_argument("--decoy-repeats", type=int, default=200)
    parser.add_argument("--seed", type=int, default=0)
    return parser.parse_args()


def q_grid_for_layer(
    layer: str,
    feature_stats: pd.DataFrame,
    tracking_stats: pd.DataFrame,
    q_values: list[float],
) -> pd.DataFrame:
    rows = []
    for q in q_values:
        for prefix, stats_frame, estimand in [
            ("", feature_stats, "mean_effect"),
            ("track_", tracking_stats, "prompt_tracking_covariance"),
        ]:
            masks = selection_masks(stats_frame["p_value"].to_numpy(float), stats_frame["e_value"].to_numpy(float), q)
            for method, mask in masks.items():
                rows.append(
                    {
                        "layer": layer,
                        "estimand": estimand,
                        "q": q,
                        "method": f"{prefix}{method}",
                        "discoveries": int(mask.sum()),
                        "selection_rule": selection_rule_for_method(method),
                    }
                )
            e_k = int(masks["e_bh_pcal"].sum())
            rows.append(
                {
                    "layer": layer,
                    "estimand": estimand,
                    "q": q,
                    "method": f"top_score_matched_{prefix}e_bh_pcal",
                    "discoveries": e_k,
                    "selection_rule": "manual_k_equal_to_e_bh_discoveries",
                }
            )
    for k in [1, 5, 7, 10, 17, 29, 54, 100, 256]:
        rows.append(
            {
                "layer": layer,
                "estimand": "screen_score",
                "q": np.nan,
                "method": f"top_score_fixed_k_{k}",
                "discoveries": k,
                "selection_rule": "manual_k_no_fdr_target",
            }
        )
    return pd.DataFrame(rows)


def stability_for_layer(
    layer: str,
    exact_cache: pd.DataFrame,
    prompt_effects: pd.DataFrame,
    feature_stats: pd.DataFrame,
    tracking_stats: pd.DataFrame,
    *,
    q: float,
    n_resamples: int,
    seed: int,
) -> pd.DataFrame:
    matrix, prompt_table = effect_matrix(exact_cache)
    full_effect = prompt_full_effects(prompt_effects, prompt_table)
    cluster_indices = cluster_prompt_indices(prompt_table)
    rng = np.random.default_rng(seed)

    base_mean = selection_masks(feature_stats["p_value"].to_numpy(float), feature_stats["e_value"].to_numpy(float), q)
    base_tracking = selection_masks(tracking_stats["p_value"].to_numpy(float), tracking_stats["e_value"].to_numpy(float), q)

    rows = []
    for rep in range(n_resamples):
        sample_idx = sample_cluster_indices(cluster_indices, rng)
        mean_p = p_values_for_matrix(matrix[sample_idx, :])
        mean_e = p_to_e_value(mean_p)
        tracking_samples = tracking_covariance_matrix(matrix[sample_idx, :], full_effect[sample_idx])
        track_p = p_values_for_matrix(tracking_samples)
        track_e = p_to_e_value(track_p)
        for estimand, prefix, p_values, e_values, base in [
            ("mean_effect", "", mean_p, mean_e, base_mean),
            ("prompt_tracking_covariance", "track_", track_p, track_e, base_tracking),
        ]:
            masks = selection_masks(p_values, e_values, q)
            for method, mask in masks.items():
                base_mask = base[method]
                rows.append(
                    {
                        "layer": layer,
                        "resample_id": rep,
                        "estimand": estimand,
                        "method": f"{prefix}{method}",
                        "discoveries": int(mask.sum()),
                        "full_discoveries": int(base_mask.sum()),
                        "jaccard_with_full": jaccard(mask, base_mask),
                        "recall_of_full_selection": recall(mask, base_mask),
                    }
                )
    return pd.DataFrame(rows)


def decoy_reliability_for_layer(
    layer: str,
    exact_cache: pd.DataFrame,
    screen_scores: pd.DataFrame,
    *,
    q: float,
    n_repeats: int,
    seed: int,
) -> pd.DataFrame:
    matrix, _prompt_table = effect_matrix(exact_cache)
    features = feature_ids_from_cache(exact_cache)
    score_map = dict(zip(screen_scores["feature_id"].astype(int), screen_scores["screen_score"].astype(float)))
    real_scores = np.array([score_map[int(feature)] for feature in features], dtype=float)
    sorted_source = np.argsort(-real_scores)
    real_p = p_values_for_matrix(matrix)
    real_e = p_to_e_value(real_p)
    rng = np.random.default_rng(seed)
    rows = []
    for rep in range(n_repeats):
        signs = rng.choice([-1.0, 1.0], size=matrix.shape)
        decoy_matrix = matrix[:, sorted_source] * signs
        decoy_p = p_values_for_matrix(decoy_matrix)
        decoy_e = p_to_e_value(decoy_p)
        p = np.concatenate([real_p, decoy_p])
        e = np.concatenate([real_e, decoy_e])
        is_decoy = np.concatenate([np.zeros(real_p.size, dtype=bool), np.ones(decoy_p.size, dtype=bool)])
        scores = np.concatenate([real_scores, real_scores[sorted_source] + 1000.0])
        masks = selection_masks(p, e, q)
        for method, mask in masks.items():
            rows.append(decoy_row(layer, rep, method, mask, is_decoy, "test_split_fdr"))
        for method, k in [
            ("top_score_matched_e_bh_pcal", int(masks["e_bh_pcal"].sum())),
            ("top_score_matched_bh", int(masks["bh"].sum())),
            ("top_score_fixed_k_7", 7),
            ("top_score_fixed_k_256", 256),
        ]:
            rows.append(decoy_row(layer, rep, method, top_score_mask(scores, k), is_decoy, "screen_score_manual_k"))
    return pd.DataFrame(rows)


def layer_scan_rows(layer: str, comparison: pd.DataFrame) -> pd.DataFrame:
    keep = [
        "e_bh_pcal",
        "by_bh",
        "bh",
        "p_lt_q",
        "track_e_bh_pcal",
        "top_score_k_e_bh_pcal",
        "top_score_k_256",
    ]
    cols = [
        "method",
        "discoveries",
        "completeness_r2",
        "centered_r2",
        "selected_full_corr",
        "abs_effect_fraction",
        "sign_agreement",
    ]
    out = comparison[comparison["method"].isin(keep)].loc[:, cols].copy()
    out.insert(0, "layer", layer)
    return out


def effect_matrix(exact_cache: pd.DataFrame) -> tuple[np.ndarray, pd.DataFrame]:
    work = exact_cache.copy()
    if "difference" not in work.columns:
        work["difference"] = work["clean_metric"] - work["ablated_metric"]
    prompt_table = (
        work[["prompt_id", "cluster_id"]]
        .drop_duplicates()
        .sort_values("prompt_id")
        .reset_index(drop=True)
    )
    pivot = work.pivot(index="prompt_id", columns="feature_id", values="difference").reindex(prompt_table["prompt_id"])
    return pivot.to_numpy(dtype=float), prompt_table


def feature_ids_from_cache(exact_cache: pd.DataFrame) -> np.ndarray:
    return np.array(sorted(exact_cache["feature_id"].astype(int).unique()), dtype=int)


def prompt_full_effects(prompt_effects: pd.DataFrame, prompt_table: pd.DataFrame) -> np.ndarray:
    required = {"prompt_id", "full_difference"}
    missing = required - set(prompt_effects.columns)
    if missing:
        raise ValueError(f"prompt effects missing columns: {sorted(missing)}")
    full_by_prompt = prompt_effects.set_index("prompt_id")["full_difference"]
    aligned = full_by_prompt.reindex(prompt_table["prompt_id"])
    if aligned.isna().any():
        missing_ids = prompt_table.loc[aligned.isna().to_numpy(), "prompt_id"].head(5).tolist()
        raise ValueError(f"prompt effects missing prompt_ids such as {missing_ids}")
    return aligned.to_numpy(dtype=float)


def cluster_prompt_indices(prompt_table: pd.DataFrame) -> list[np.ndarray]:
    return [
        group.index.to_numpy(dtype=int)
        for _cluster, group in prompt_table.groupby("cluster_id", sort=False)
    ]


def sample_cluster_indices(cluster_indices: list[np.ndarray], rng: np.random.Generator) -> np.ndarray:
    choices = rng.integers(0, len(cluster_indices), size=len(cluster_indices))
    return np.concatenate([cluster_indices[idx] for idx in choices])


def p_values_for_matrix(matrix: np.ndarray) -> np.ndarray:
    means = np.mean(matrix, axis=0)
    se = np.std(matrix, axis=0, ddof=1) / np.sqrt(matrix.shape[0])
    t_stat = np.divide(means, se, out=np.zeros_like(means), where=se > 0)
    p = 2.0 * stats.t.sf(np.abs(t_stat), df=matrix.shape[0] - 1)
    p = np.where((se == 0.0) & (means != 0.0), 0.0, p)
    p = np.where((se == 0.0) & (means == 0.0), 1.0, p)
    return np.clip(p.astype(float), 0.0, 1.0)


def tracking_covariance_matrix(matrix: np.ndarray, full_effect: np.ndarray) -> np.ndarray:
    centered_matrix = matrix - np.mean(matrix, axis=0, keepdims=True)
    centered_full = full_effect - np.mean(full_effect)
    return centered_matrix * centered_full[:, None]


def selection_masks(p_values: np.ndarray, e_values: np.ndarray, q: float) -> dict[str, np.ndarray]:
    return {
        "e_bh_pcal": e_bh(e_values, q),
        "by_bh": by_bh(p_values, q),
        "bh": bh(p_values, q),
        "p_lt_q": p_threshold(p_values, q),
    }


def selection_rule_for_method(method: str) -> str:
    if method in {"e_bh_pcal", "by_bh", "bh"}:
        return "fdr_at_q"
    if method == "p_lt_q":
        return "uncorrected_p_threshold"
    return "selection_rule_unknown"


def top_score_mask(scores: np.ndarray, k: int) -> np.ndarray:
    mask = np.zeros(scores.size, dtype=bool)
    if k > 0:
        mask[np.argsort(-scores)[: min(k, scores.size)]] = True
    return mask


def decoy_row(layer: str, rep: int, method: str, mask: np.ndarray, is_decoy: np.ndarray, selection_rule: str) -> dict[str, object]:
    decoys = int(np.sum(mask & is_decoy))
    discoveries = int(np.sum(mask))
    return {
        "layer": layer,
        "repeat_id": rep,
        "method": method,
        "selection_rule": selection_rule,
        "discoveries": discoveries,
        "known_null_decoys_selected": decoys,
        "known_null_fdp": decoys / max(discoveries, 1),
    }


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


def summarize_stability(stability: pd.DataFrame) -> pd.DataFrame:
    return (
        stability.groupby(["layer", "estimand", "method"], as_index=False)
        .agg(
            discoveries_mean=("discoveries", "mean"),
            discoveries_std=("discoveries", "std"),
            jaccard_mean=("jaccard_with_full", "mean"),
            jaccard_std=("jaccard_with_full", "std"),
            recall_full_mean=("recall_of_full_selection", "mean"),
            recall_full_std=("recall_of_full_selection", "std"),
            full_discoveries=("full_discoveries", "first"),
        )
        .sort_values(["layer", "estimand", "method"])
    )


def summarize_decoys(decoys: pd.DataFrame) -> pd.DataFrame:
    return (
        decoys.groupby(["layer", "method", "selection_rule"], as_index=False)
        .agg(
            discoveries_mean=("discoveries", "mean"),
            discoveries_std=("discoveries", "std"),
            known_null_decoys_selected_mean=("known_null_decoys_selected", "mean"),
            known_null_decoys_selected_std=("known_null_decoys_selected", "std"),
            known_null_fdp_mean=("known_null_fdp", "mean"),
            known_null_fdp_std=("known_null_fdp", "std"),
        )
        .sort_values(["layer", "selection_rule", "method"])
    )


def write_layer_report(
    path: Path,
    layer: str,
    q_grid: pd.DataFrame,
    stability: pd.DataFrame,
    decoys: pd.DataFrame,
    layer_scan: pd.DataFrame,
) -> None:
    lines = [
        f"# Real Subject-Verb Reliability: {layer}",
        "",
        "## Null Decoy Reliability",
        "",
        decoys.to_markdown(index=False),
        "",
        "## Prompt-Resampling Selection Stability",
        "",
        stability.to_markdown(index=False),
        "",
        "## Real q Grid",
        "",
        q_grid.to_markdown(index=False),
        "",
        "## Layer Scan Metrics",
        "",
        layer_scan.to_markdown(index=False),
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def write_combined_report(
    path: Path,
    q_grid: pd.DataFrame,
    stability: pd.DataFrame,
    decoys: pd.DataFrame,
    layer_scan: pd.DataFrame,
) -> None:
    headline_decoys = decoys[
        decoys["method"].isin(["e_bh_pcal", "p_lt_q", "top_score_matched_e_bh_pcal", "top_score_fixed_k_256"])
    ].copy()
    headline_layers = layer_scan[
        layer_scan["method"].isin(["e_bh_pcal", "track_e_bh_pcal", "top_score_k_e_bh_pcal", "top_score_k_256"])
    ].copy()
    headline_stability = stability[
        stability["method"].isin(["e_bh_pcal", "track_e_bh_pcal", "bh", "p_lt_q"])
    ].copy()
    lines = [
        "# Real Subject-Verb Reliability Extensions",
        "",
        "These analyses use only existing real Gemma/Gemma Scope caches. No new GPU",
        "runs are required for the null-decoy, stability, or q-grid analyses.",
        "",
        "The screen-score decoy stress test constructs known-null candidate features",
        "by random sign flips of real test-split feature effects, while assigning the",
        "decoys high screen scores. Decoys are therefore null by construction on the",
        "test estimand but attractive to screen-only top-score selection.",
        "",
        "## Headline Null-Decoy Result",
        "",
        headline_decoys.to_markdown(index=False),
        "",
        "## Prompt-Resampling Stability",
        "",
        headline_stability.to_markdown(index=False),
        "",
        "## Layer Scan",
        "",
        headline_layers.to_markdown(index=False),
        "",
        "## Real q Grid",
        "",
        q_grid.to_markdown(index=False),
        "",
        "Reporting guardrails: single-feature tracking results are labeled as such;",
        "top-score circuit metrics are reported as baselines, not as FDR-controlled",
        "discoveries; completeness is always paired with centered R2 and correlation.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def safe_display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT.resolve())).replace("\\", "/")
    except ValueError:
        return str(path)


if __name__ == "__main__":
    main()
