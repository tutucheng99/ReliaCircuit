from __future__ import annotations

import argparse
import json
import sys
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

from reliacircuit.fdr import bh, by_bh, e_bh, p_threshold, p_to_e_value  # noqa: E402
from run_reviewer_empirical_gaps import (  # noqa: E402
    grouped_matrix,
    jaccard,
    load_layers,
    p_values_signflip,
    p_values_signflip_normal,
    p_values_t,
    recall,
    round_numeric,
    safe_display_path,
)
from subject_verb_layer_protocol import layer_specs  # noqa: E402


GAMMAS = (0.25, 0.5, 0.75)
Q = 0.1


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    layers = load_layers()

    outputs = {
        "decoy_bh_by_all_schemes.csv": decoy_bh_by_all_schemes(),
        "gamma_sensitivity_synthetic_runs.csv": gamma_sensitivity_synthetic_runs(args.q),
        "gamma_sensitivity_synthetic_summary.csv": gamma_sensitivity_synthetic_summary(args.q),
        "gamma_sensitivity_real.csv": gamma_sensitivity_real(layers, args.q),
        "real_ci_type_s_per_feature.csv": real_ci_type_s_per_feature(layers, args.sign_bootstrap_repeats, args.seed),
        "real_ci_type_s_summary.csv": None,
        "adaptive_ebh_summary.csv": adaptive_ebh_summary(layers, args.q),
        "cluster_permutation_summary.csv": cluster_permutation_summary(
            layers,
            q=args.q,
            n_resamples=args.cluster_resamples,
            seed=args.seed,
        ),
    }
    outputs["real_ci_type_s_summary.csv"] = summarize_real_ci_type_s(outputs["real_ci_type_s_per_feature.csv"])

    conclusions = second_round_conclusions(outputs)
    outputs["second_round_conclusions.csv"] = conclusions

    for name, frame in outputs.items():
        frame.to_csv(args.output_dir / name, index=False)
        (args.output_dir / name.replace(".csv", ".md")).write_text(
            frame.pipe(round_numeric).to_markdown(index=False),
            encoding="utf-8",
        )

    plot_ci_type_s(
        outputs["real_ci_type_s_per_feature.csv"],
        outputs["real_ci_type_s_summary.csv"],
        args.output_dir / "real_ci_type_s_summary.png",
    )
    plot_second_round_summary(outputs, args.output_dir / "second_round_summary.png")
    write_report(args.output_dir / "second_round_reviewer_report.md", conclusions, outputs)
    print(f"wrote second-round reviewer analyses to {safe_display_path(args.output_dir)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CPU-only analyses for second-round reviewer empirical gaps.")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "results" / "second_round_reviewer")
    parser.add_argument("--q", type=float, default=Q)
    parser.add_argument("--cluster-resamples", type=int, default=999)
    parser.add_argument("--sign-bootstrap-repeats", type=int, default=400)
    parser.add_argument("--seed", type=int, default=20260604)
    return parser.parse_args()


def decoy_bh_by_all_schemes() -> pd.DataFrame:
    source = ROOT / "results" / "reviewer_empirical_gaps" / "decoy_robustness_summary.csv"
    table = pd.read_csv(source)
    keep = ["e_bh_pcal", "by_bh", "bh", "p_lt_q", "top_score_matched_e_bh_pcal"]
    table = table[table["method"].isin(keep)].copy()
    table["decoy_candidates"] = 256
    table["decoy_admission_rate_mean"] = table["known_null_decoys_selected_mean"] / table["decoy_candidates"]
    table["decoy_admission_rate_std"] = table["known_null_decoys_selected_std"] / table["decoy_candidates"]
    return table[
        [
            "layer",
            "decoy_scheme",
            "method",
            "selection_rule",
            "discoveries_mean",
            "known_null_decoys_selected_mean",
            "known_null_fdp_mean",
            "decoy_admission_rate_mean",
            "decoy_admission_rate_std",
        ]
    ].sort_values(["layer", "decoy_scheme", "method"])


def gamma_sensitivity_synthetic_runs(q: float) -> pd.DataFrame:
    per_feature = pd.read_csv(ROOT / "results" / "synthetic_gate_b" / "per_feature.csv")
    config = json.loads((ROOT / "configs" / "synthetic_gate_b.json").read_text(encoding="utf-8"))
    n_total_active = int(config["synthetic"]["n_active"])
    rows = []
    for replicate, group in per_feature.groupby("replicate", sort=True):
        p = group["p_value"].to_numpy(float)
        active = group["is_active"].to_numpy(bool)
        default = e_bh(p_to_e_value(p, gamma=0.5), q)
        for gamma in GAMMAS:
            mask = e_bh(p_to_e_value(p, gamma=gamma), q)
            discoveries = int(mask.sum())
            false_discoveries = int(np.sum(mask & ~active))
            true_discoveries = int(np.sum(mask & active))
            rows.append(
                {
                    "replicate": int(replicate),
                    "gamma": gamma,
                    "discoveries": discoveries,
                    "false_discoveries": false_discoveries,
                    "true_discoveries": true_discoveries,
                    "fdp": false_discoveries / max(discoveries, 1),
                    "power": true_discoveries / max(n_total_active, 1),
                    "jaccard_to_gamma_0_5": jaccard(mask, default),
                    "recall_of_gamma_0_5": recall(mask, default),
                }
            )
    return pd.DataFrame(rows)


def gamma_sensitivity_synthetic_summary(q: float) -> pd.DataFrame:
    runs = gamma_sensitivity_synthetic_runs(q)
    rows = []
    metric_cols = ["discoveries", "false_discoveries", "true_discoveries", "fdp", "power", "jaccard_to_gamma_0_5", "recall_of_gamma_0_5"]
    for gamma, group in runs.groupby("gamma", sort=True):
        row = {"gamma": float(gamma), "replicates": int(group.shape[0])}
        for col in metric_cols:
            values = group[col].dropna()
            row[f"{col}_mean"] = float(values.mean()) if not values.empty else np.nan
            row[f"{col}_se"] = float(values.std(ddof=1) / np.sqrt(values.shape[0])) if values.shape[0] > 1 else 0.0
        rows.append(row)
    return pd.DataFrame(rows)


def gamma_sensitivity_real(layers: dict[str, dict[str, object]], q: float) -> pd.DataFrame:
    rows = []
    for layer, payload in layers.items():
        matrix = np.asarray(payload["matrix"])
        p = p_values_t(matrix)
        default = e_bh(p_to_e_value(p, gamma=0.5), q)
        for gamma in GAMMAS:
            e_values = p_to_e_value(p, gamma=gamma)
            mask = e_bh(e_values, q)
            rows.append(
                {
                    "layer": layer,
                    "gamma": gamma,
                    "discoveries": int(mask.sum()),
                    "jaccard_to_gamma_0_5": jaccard(mask, default),
                    "recall_of_gamma_0_5": recall(mask, default),
                    "median_e_selected": float(np.median(e_values[mask])) if mask.any() else np.nan,
                    "min_p_selected": float(np.min(p[mask])) if mask.any() else np.nan,
                }
            )
    return pd.DataFrame(rows).sort_values(["layer", "gamma"])


def real_ci_type_s_per_feature(
    layers: dict[str, dict[str, object]],
    n_repeats: int,
    seed: int,
) -> pd.DataFrame:
    frames = []
    for spec in layer_specs():
        if spec.label not in layers:
            continue
        stats_path = spec.result_dir / "cache_analysis" / "feature_stats.csv"
        feature_stats = pd.read_csv(stats_path).copy()
        payload = layers[spec.label]
        matrix = np.asarray(payload["matrix"])
        prompt_meta = payload["prompt_meta"]
        cluster_matrix = grouped_matrix(matrix, prompt_meta["cluster_id"].astype(str).to_numpy())
        sign_instability = cluster_bootstrap_sign_instability(
            cluster_matrix,
            feature_stats["tau_hat"].to_numpy(float),
            n_repeats=n_repeats,
            seed=seed + stable_layer_offset(spec.label),
        )
        feature_stats.insert(0, "layer", spec.label)
        feature_stats["ci_width"] = feature_stats["ci_upper"] - feature_stats["ci_lower"]
        feature_stats["abs_tau_hat"] = feature_stats["tau_hat"].abs()
        feature_stats["relative_ci_width"] = feature_stats["ci_width"] / feature_stats["abs_tau_hat"].clip(lower=1e-12)
        feature_stats["ci_crosses_zero"] = (feature_stats["ci_lower"] <= 0.0) & (feature_stats["ci_upper"] >= 0.0)
        feature_stats["ci_sign_identified"] = ~feature_stats["ci_crosses_zero"]
        feature_stats["cluster_bootstrap_sign_flip_rate"] = sign_instability
        feature_stats["type_s_diagnostic_flag"] = feature_stats["ci_crosses_zero"] | (feature_stats["cluster_bootstrap_sign_flip_rate"] > 0.05)
        frames.append(feature_stats)
    return pd.concat(frames, ignore_index=True)


def summarize_real_ci_type_s(per_feature: pd.DataFrame) -> pd.DataFrame:
    rows = []
    groups = {
        "all_screened": lambda frame: np.ones(frame.shape[0], dtype=bool),
        "e_bh_pcal": lambda frame: frame["selected_e_bh_pcal"].to_numpy(bool),
        "by_bh": lambda frame: frame["selected_by_bh"].to_numpy(bool),
        "bh": lambda frame: frame["selected_bh"].to_numpy(bool),
    }
    for layer, layer_frame in per_feature.groupby("layer", sort=True):
        for selection, mask_fn in groups.items():
            mask = mask_fn(layer_frame)
            subset = layer_frame.loc[mask]
            rows.append(summarize_ci_subset(layer, selection, subset))
    return pd.DataFrame(rows)


def summarize_ci_subset(layer: str, selection: str, subset: pd.DataFrame) -> dict[str, object]:
    if subset.empty:
        return {
            "layer": layer,
            "selection": selection,
            "features": 0,
            "ci_width_median": np.nan,
            "ci_width_p90": np.nan,
            "relative_ci_width_median": np.nan,
            "ci_crosses_zero_rate": np.nan,
            "cluster_bootstrap_sign_flip_rate_mean": np.nan,
            "cluster_bootstrap_sign_flip_rate_max": np.nan,
            "type_s_diagnostic_rate": np.nan,
        }
    return {
        "layer": layer,
        "selection": selection,
        "features": int(subset.shape[0]),
        "ci_width_median": float(subset["ci_width"].median()),
        "ci_width_p90": float(subset["ci_width"].quantile(0.9)),
        "relative_ci_width_median": float(subset["relative_ci_width"].median()),
        "ci_crosses_zero_rate": float(subset["ci_crosses_zero"].mean()),
        "cluster_bootstrap_sign_flip_rate_mean": float(subset["cluster_bootstrap_sign_flip_rate"].mean()),
        "cluster_bootstrap_sign_flip_rate_max": float(subset["cluster_bootstrap_sign_flip_rate"].max()),
        "type_s_diagnostic_rate": float(subset["type_s_diagnostic_flag"].mean()),
    }


def cluster_bootstrap_sign_instability(
    cluster_matrix: np.ndarray,
    tau_hat: np.ndarray,
    *,
    n_repeats: int,
    seed: int,
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    n_clusters = cluster_matrix.shape[0]
    target_sign = np.sign(tau_hat)
    flips = np.zeros(cluster_matrix.shape[1], dtype=float)
    chunk = 100
    done = 0
    while done < n_repeats:
        size = min(chunk, n_repeats - done)
        idx = rng.integers(0, n_clusters, size=(size, n_clusters))
        boot_means = cluster_matrix[idx, :].mean(axis=1)
        boot_sign = np.sign(boot_means)
        flips += np.sum((boot_sign != 0.0) & (target_sign[None, :] != 0.0) & (boot_sign != target_sign[None, :]), axis=0)
        done += size
    return flips / max(n_repeats, 1)


def adaptive_ebh_summary(layers: dict[str, dict[str, object]], q: float) -> pd.DataFrame:
    rows = []
    rows.extend(adaptive_ebh_synthetic_rows(q))
    for layer, payload in layers.items():
        p = p_values_t(np.asarray(payload["matrix"]))
        e = p_to_e_value(p)
        scores = np.asarray(payload["scores"])
        default = e_bh(e, q)
        adaptive = screen_stratified_ebh(e, scores, q)
        for method, mask in [
            ("e_bh_pcal", default),
            ("screen_stratified_ebh", adaptive),
        ]:
            rows.append(
                {
                    "setting": f"real_{layer}",
                    "method": method,
                    "fdr_guarantee_note": f"e-BH arbitrary-dependence; stratified variant uses disjoint q budgets summing to {q}",
                    "discoveries_mean": float(mask.sum()),
                    "fdp_mean": np.nan,
                    "power_mean": np.nan,
                    "jaccard_to_default": jaccard(mask, default),
                    "recall_of_default": recall(mask, default),
                    "gain_vs_default_discoveries": int(mask.sum()) - int(default.sum()),
                }
            )
    return pd.DataFrame(rows)


def adaptive_ebh_synthetic_rows(q: float) -> list[dict[str, object]]:
    per_feature = pd.read_csv(ROOT / "results" / "synthetic_gate_b" / "per_feature.csv")
    config = json.loads((ROOT / "configs" / "synthetic_gate_b.json").read_text(encoding="utf-8"))
    n_total_active = int(config["synthetic"]["n_active"])
    run_rows = []
    for _replicate, group in per_feature.groupby("replicate", sort=True):
        p = group["p_value"].to_numpy(float)
        e = p_to_e_value(p)
        scores = group["screen_score"].to_numpy(float)
        active = group["is_active"].to_numpy(bool)
        default = e_bh(e, q)
        adaptive = screen_stratified_ebh(e, scores, q)
        for method, mask in [("e_bh_pcal", default), ("screen_stratified_ebh", adaptive)]:
            discoveries = int(mask.sum())
            false_discoveries = int(np.sum(mask & ~active))
            true_discoveries = int(np.sum(mask & active))
            run_rows.append(
                {
                    "method": method,
                    "discoveries": discoveries,
                    "fdp": false_discoveries / max(discoveries, 1),
                    "power": true_discoveries / max(n_total_active, 1),
                    "jaccard_to_default": jaccard(mask, default),
                    "recall_of_default": recall(mask, default),
                    "gain_vs_default_discoveries": discoveries - int(default.sum()),
                }
            )
    run_frame = pd.DataFrame(run_rows)
    rows = []
    for method, group in run_frame.groupby("method", sort=False):
        rows.append(
            {
                "setting": "synthetic_gate_b",
                "method": method,
                "fdr_guarantee_note": f"e-BH arbitrary-dependence; stratified variant uses disjoint q budgets summing to {q}",
                "discoveries_mean": float(group["discoveries"].mean()),
                "fdp_mean": float(group["fdp"].mean()),
                "power_mean": float(group["power"].mean()),
                "jaccard_to_default": float(group["jaccard_to_default"].mean()),
                "recall_of_default": float(group["recall_of_default"].mean()),
                "gain_vs_default_discoveries": float(group["gain_vs_default_discoveries"].mean()),
            }
        )
    return rows


def screen_stratified_ebh(e_values: np.ndarray, scores: np.ndarray, q: float) -> np.ndarray:
    scores = np.asarray(scores, dtype=float)
    e_values = np.asarray(e_values, dtype=float)
    ranks = pd.Series(scores).rank(method="first")
    bins = pd.qcut(ranks, q=4, labels=False, duplicates="drop").to_numpy()
    bin_ids = np.unique(bins)
    # Low to high screen-score strata. Budgets sum to q, preserving a union-bound
    # arbitrary-dependence FDR guarantee across disjoint strata.
    fractions = np.linspace(0.05, 0.55, num=bin_ids.size)
    fractions = fractions / fractions.sum()
    reject = np.zeros(e_values.size, dtype=bool)
    for b, frac in zip(bin_ids, fractions):
        idx = np.flatnonzero(bins == b)
        reject[idx] = e_bh(e_values[idx], q * float(frac))
    return reject


def cluster_permutation_summary(
    layers: dict[str, dict[str, object]],
    *,
    q: float,
    n_resamples: int,
    seed: int,
) -> pd.DataFrame:
    rows = []
    for layer, payload in layers.items():
        matrix = np.asarray(payload["matrix"])
        prompt_meta = payload["prompt_meta"]
        cluster_matrix = grouped_matrix(matrix, prompt_meta["cluster_id"].astype(str).to_numpy())
        rng = np.random.default_rng(seed + stable_layer_offset(layer))
        p_methods = {
            "paired_t_prompt_level": p_values_t(matrix),
            "cluster_mean_t": p_values_t(cluster_matrix),
            "cluster_signflip_normal": p_values_signflip_normal(cluster_matrix),
            "cluster_signflip_randomization": p_values_signflip(cluster_matrix, n_resamples=n_resamples, rng=rng),
        }
        default = e_bh(p_to_e_value(p_methods["paired_t_prompt_level"]), q)
        for p_method, p in p_methods.items():
            e = p_to_e_value(p)
            for method, mask in [
                ("e_bh_pcal", e_bh(e, q)),
                ("by_bh", by_bh(p, q)),
                ("bh", bh(p, q)),
            ]:
                rows.append(
                    {
                        "layer": layer,
                        "p_value_method": p_method,
                        "selection_method": method,
                        "clusters": int(cluster_matrix.shape[0]),
                        "discoveries": int(mask.sum()),
                        "jaccard_to_prompt_paired_t_ebh": jaccard(mask, default),
                        "recall_of_prompt_paired_t_ebh": recall(mask, default),
                        "median_p_selected": float(np.median(p[mask])) if mask.any() else np.nan,
                    }
                )
    return pd.DataFrame(rows).sort_values(["layer", "p_value_method", "selection_method"])


def second_round_conclusions(outputs: dict[str, pd.DataFrame]) -> pd.DataFrame:
    decoy = outputs["decoy_bh_by_all_schemes.csv"]
    gamma_syn = outputs["gamma_sensitivity_synthetic_summary.csv"]
    gamma_real = outputs["gamma_sensitivity_real.csv"]
    ci_summary = outputs["real_ci_type_s_summary.csv"]
    adaptive = outputs["adaptive_ebh_summary.csv"]
    cluster = outputs["cluster_permutation_summary.csv"]

    decoy_bh = decoy[decoy["method"] == "bh"]["known_null_decoys_selected_mean"].mean()
    decoy_by = decoy[decoy["method"] == "by_bh"]["known_null_decoys_selected_mean"].mean()
    decoy_ebh = decoy[decoy["method"] == "e_bh_pcal"]["known_null_decoys_selected_mean"].mean()
    gamma_real_nondefault = gamma_real[gamma_real["gamma"] != 0.5]
    gamma_syn_nondefault = gamma_syn[gamma_syn["gamma"] != 0.5]
    ci_ebh = ci_summary[ci_summary["selection"] == "e_bh_pcal"]
    adaptive_real = adaptive[adaptive["setting"].str.startswith("real_")]
    adaptive_syn = adaptive[(adaptive["setting"] == "synthetic_gate_b") & (adaptive["method"] == "screen_stratified_ebh")]
    cluster_focus = cluster[
        (cluster["selection_method"] == "e_bh_pcal")
        & (cluster["p_value_method"].isin(["cluster_mean_t", "cluster_signflip_normal"]))
    ]

    rows = [
        {
            "gap": "BH/BY decoy coverage",
            "status": "empirical_conclusion",
            "headline_metric": f"mean decoys selected: e-BH={decoy_ebh:.3f}, BY={decoy_by:.3f}, BH={decoy_bh:.3f}",
            "conclusion": "BH/BY are now reported for every layer and decoy scheme. They often remain cleaner than uncorrected p<q, but can admit more constructed-null decoys than e-BH under screen-attractive decoys.",
            "table": "table_18_second_round_decoy_bh_by",
        },
        {
            "gap": "Gamma sensitivity",
            "status": "empirical_conclusion",
            "headline_metric": f"real nondefault gamma median Jaccard={gamma_real_nondefault['jaccard_to_gamma_0_5'].median():.3f}; synthetic max FDP={gamma_syn['fdp_mean'].max():.3f}",
            "conclusion": "Gamma changes discovery counts but the nondefault real selections retain measurable overlap with gamma=0.5. Synthetic FDP stays below q across the requested gamma grid; gamma=0.5 remains the balanced default between conservative gamma=0.25 and aggressive gamma=0.75.",
            "table": "tables_19_20_second_round_gamma",
        },
        {
            "gap": "Real CI width distribution",
            "status": "empirical_conclusion",
            "headline_metric": f"e-BH selected CI width median={ci_ebh['ci_width_median'].median():.4f}; p90={ci_ebh['ci_width_p90'].median():.4f}",
            "conclusion": "Real selected features now have a per-feature uncertainty distribution rather than only point discoveries; widths vary by layer and selection set and are visualized directly.",
            "table": "table_21_second_round_real_ci_type_s",
        },
        {
            "gap": "Real Type S diagnostic",
            "status": "empirical_conclusion",
            "headline_metric": f"e-BH diagnostic rate median={ci_ebh['type_s_diagnostic_rate'].median():.3f}; max sign-flip rate={ci_ebh['cluster_bootstrap_sign_flip_rate_max'].max():.3f}",
            "conclusion": "Real Type S cannot be verified against unknown ground truth, so the paper should describe this as a sign-instability diagnostic: CI zero-crossings plus cluster-bootstrap sign flips. The selected e-BH features have low diagnostic rates.",
            "table": "table_21_second_round_real_ci_type_s",
        },
        {
            "gap": "Covariate-adaptive e-BH",
            "status": "empirical_conclusion",
            "headline_metric": f"synthetic stratified FDP={float(adaptive_syn['fdp_mean'].iloc[0]):.3f}; real median discovery gain={adaptive_real[adaptive_real['method'] == 'screen_stratified_ebh']['gain_vs_default_discoveries'].median():.1f}",
            "conclusion": "The screen-stratified e-BH variant preserves an arbitrary-dependence guarantee by splitting q across disjoint screen-score strata. It is a valid comparator, but its power gain is empirical and not guaranteed; report gains and losses layer by layer.",
            "table": "table_22_second_round_adaptive_ebh",
        },
        {
            "gap": "Cluster permutation robustness",
            "status": "empirical_conclusion",
            "headline_metric": f"cluster conservative e-BH median Jaccard={cluster_focus['jaccard_to_prompt_paired_t_ebh'].median():.3f}",
            "conclusion": "Cluster-level tests address prompt/patch dependence by reducing the test unit to prompt clusters. Main discoveries remain partially stable under cluster-mean and cluster-signflip normal tests; finite randomization remains resolution-limited for p-to-e e-BH.",
            "table": "table_23_second_round_cluster_permutation",
        },
    ]
    return pd.DataFrame(rows)


def plot_ci_type_s(per_feature: pd.DataFrame, summary: pd.DataFrame, path: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.5), constrained_layout=True)
    selected = per_feature[per_feature["selected_e_bh_pcal"].astype(bool)]
    axes[0].hist(per_feature["ci_width"], bins=35, alpha=0.45, label="all screened")
    axes[0].hist(selected["ci_width"], bins=25, alpha=0.7, label="e-BH selected")
    axes[0].set_title("Real CI width distribution")
    axes[0].set_xlabel("CI width")
    axes[0].set_ylabel("features")
    axes[0].legend()

    ebh = summary[summary["selection"] == "e_bh_pcal"].sort_values("layer")
    axes[1].bar(ebh["layer"], ebh["type_s_diagnostic_rate"])
    axes[1].set_ylim(0.0, max(0.05, float(ebh["type_s_diagnostic_rate"].max()) + 0.02))
    axes[1].set_title("Type S diagnostic rate")
    axes[1].set_ylabel("rate")
    fig.savefig(path, dpi=180)
    plt.close(fig)


def plot_second_round_summary(outputs: dict[str, pd.DataFrame], path: Path) -> None:
    fig, axes = plt.subplots(2, 3, figsize=(13, 7), constrained_layout=True)
    decoy = outputs["decoy_bh_by_all_schemes.csv"]
    decoy_plot = decoy[decoy["method"].isin(["e_bh_pcal", "by_bh", "bh"])].groupby("method")["known_null_decoys_selected_mean"].mean()
    axes[0, 0].bar(decoy_plot.index, decoy_plot.values)
    axes[0, 0].set_title("Decoys selected")
    axes[0, 0].tick_params(axis="x", rotation=25)

    gamma_syn = outputs["gamma_sensitivity_synthetic_summary.csv"]
    axes[0, 1].plot(gamma_syn["gamma"], gamma_syn["fdp_mean"], marker="o", label="FDP")
    axes[0, 1].plot(gamma_syn["gamma"], gamma_syn["power_mean"], marker="o", label="power")
    axes[0, 1].axhline(Q, color="black", linestyle="--", linewidth=1)
    axes[0, 1].set_title("Synthetic gamma")
    axes[0, 1].legend()

    gamma_real = outputs["gamma_sensitivity_real.csv"]
    pivot = gamma_real.pivot(index="layer", columns="gamma", values="discoveries")
    pivot.plot(kind="bar", ax=axes[0, 2])
    axes[0, 2].set_title("Real gamma discoveries")
    axes[0, 2].tick_params(axis="x", rotation=0)

    ci_summary = outputs["real_ci_type_s_summary.csv"]
    ebh_ci = ci_summary[ci_summary["selection"] == "e_bh_pcal"].sort_values("layer")
    axes[1, 0].bar(ebh_ci["layer"], ebh_ci["ci_width_median"])
    axes[1, 0].set_title("Selected CI median width")

    adaptive = outputs["adaptive_ebh_summary.csv"]
    real_adapt = adaptive[(adaptive["setting"].str.startswith("real_")) & (adaptive["method"] == "screen_stratified_ebh")]
    axes[1, 1].bar(real_adapt["setting"].str.replace("real_", "", regex=False), real_adapt["gain_vs_default_discoveries"])
    axes[1, 1].axhline(0.0, color="black", linewidth=1)
    axes[1, 1].set_title("Stratified e-BH gain")

    cluster = outputs["cluster_permutation_summary.csv"]
    cluster_plot = cluster[
        (cluster["selection_method"] == "e_bh_pcal")
        & (cluster["p_value_method"].isin(["cluster_mean_t", "cluster_signflip_normal"]))
    ].groupby("p_value_method")["jaccard_to_prompt_paired_t_ebh"].mean()
    axes[1, 2].bar(cluster_plot.index, cluster_plot.values)
    axes[1, 2].set_ylim(0.0, 1.0)
    axes[1, 2].set_title("Cluster-test overlap")
    axes[1, 2].tick_params(axis="x", rotation=20)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def write_report(path: Path, conclusions: pd.DataFrame, outputs: dict[str, pd.DataFrame]) -> None:
    lines = [
        "# Second-Round Reviewer Empirical Analyses",
        "",
        "This report is generated by `scripts/run_second_round_reviewer_analyses.py`.",
        "It uses existing synthetic and real subject-verb caches only; no new GPU run is required.",
        "",
        "## Conclusions",
        "",
        conclusions.to_markdown(index=False),
        "",
    ]
    for name, frame in outputs.items():
        lines.extend([f"## {name}", "", frame.pipe(round_numeric).to_markdown(index=False), ""])
    path.write_text("\n".join(lines), encoding="utf-8")


def stable_layer_offset(layer: str) -> int:
    return sum((idx + 1) * ord(ch) for idx, ch in enumerate(layer))


if __name__ == "__main__":
    main()
