from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import sys
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from subject_verb_layer_protocol import layer_specs  # noqa: E402


def main() -> None:
    args = parse_args()
    output_dir = ROOT / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    tables = {
        "table_1_gate_b_fdr_ci": build_gate_b_table(),
        "table_2_q_grid": build_q_grid_table(),
        "table_3_synthetic_frontier": build_frontier_table(),
        "table_4_circuit_metrics": build_circuit_table(),
        "table_5_ci_frontier": build_ci_table(),
        "table_6_downstream_debias": build_debias_table(),
        "table_7_real_subject_verb": build_real_subject_verb_table(),
        "table_8_bounded_bias_probe": build_bounded_bias_probe_table(),
        "table_9_real_decoy_reliability": build_real_decoy_reliability_table(),
        "table_10_real_selection_stability": build_real_selection_stability_table(),
        "table_11_real_q_grid": build_real_q_grid_table(),
        "table_12_reviewer_qf_sensitivity": build_reviewer_qf_sensitivity_table(),
        "table_13_reviewer_pvalue_robustness": build_reviewer_pvalue_robustness_table(),
        "table_14_reviewer_method_comparison": build_reviewer_method_comparison_table(),
        "table_15_reviewer_multisplit": build_reviewer_multisplit_table(),
        "table_16_reviewer_decoy_robustness": build_reviewer_decoy_robustness_table(),
        "table_17_reviewer_type_sm": build_reviewer_type_sm_table(),
        "table_18_second_round_decoy_bh_by": build_second_round_decoy_bh_by_table(),
        "table_19_second_round_gamma_synthetic": build_second_round_gamma_synthetic_table(),
        "table_20_second_round_gamma_real": build_second_round_gamma_real_table(),
        "table_21_second_round_real_ci_type_s": build_second_round_real_ci_type_s_table(),
        "table_22_second_round_adaptive_ebh": build_second_round_adaptive_ebh_table(),
        "table_23_second_round_cluster_permutation": build_second_round_cluster_permutation_table(),
    }
    for name, table in tables.items():
        table.to_csv(output_dir / f"{name}.csv", index=False)
        (output_dir / f"{name}.md").write_text(table.to_markdown(index=False), encoding="utf-8")

    figures = copy_figures(output_dir)
    inventory = build_inventory()
    inventory.to_csv(output_dir / "artifact_inventory.csv", index=False)
    write_summary(output_dir / "paper_assets_index.md", tables, figures, inventory)
    print(
        f"wrote {len(tables)} tables, {len(figures)} figures, and artifact inventory "
        f"to {safe_display_path(output_dir)}"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="results/paper_assets")
    return parser.parse_args()


def build_gate_b_table() -> pd.DataFrame:
    agg = pd.read_csv(ROOT / "results" / "synthetic_gate_b" / "aggregate_metrics.csv")
    keep = ["e_bh_pcal", "by_bh", "bh", "p_lt_q", "top_score_k_active"]
    table = agg[agg["method"].isin(keep)].copy()
    return table[
        [
            "method",
            "discoveries_mean",
            "fdp_mean",
            "power_mean",
            "ci_coverage_screened_mean",
            "ci_coverage_selected_mean",
        ]
    ].pipe(round_numeric)


def build_q_grid_table() -> pd.DataFrame:
    q = pd.read_csv(ROOT / "results" / "synthetic_gate_b" / "q_grid_metrics.csv")
    table = q[q["method"].isin(["e_bh_pcal", "by_bh", "bh", "p_lt_q"])].copy()
    return table[["q", "method", "fdp_mean", "power_mean", "discoveries_mean"]].pipe(round_numeric)


def build_frontier_table() -> pd.DataFrame:
    agg = pd.read_csv(ROOT / "results" / "synthetic_frontier" / "aggregate_metrics.csv")
    table = agg[agg["method"].isin(["e_bh_pcal", "p_lt_q", "top_score_k_active"])].copy()
    return table[
        [
            "scenario",
            "method",
            "fdp_mean",
            "power_mean",
            "screen_recall_mean",
            "ci_coverage_screened_mean",
        ]
    ].pipe(round_numeric)


def build_circuit_table() -> pd.DataFrame:
    gate = pd.read_csv(ROOT / "results" / "synthetic_gate_b" / "circuit_aggregate_metrics.csv")
    table = gate[gate["method"].isin(["e_bh_pcal", "top_score_k_active"])].copy()
    return table[
        [
            "method",
            "completeness_r2_mean",
            "necessity_fraction_mean",
            "selected_full_corr_mean",
            "sign_agreement_mean",
        ]
    ].pipe(round_numeric)


def build_ci_table() -> pd.DataFrame:
    agg = pd.read_csv(ROOT / "results" / "synthetic_ci_frontier" / "aggregate_metrics.csv")
    table = agg[agg["method"] == "e_bh_pcal"].copy()
    return table[
        [
            "scenario",
            "fdp_mean",
            "power_mean",
            "ci_coverage_screened_mean",
            "ci_coverage_selected_mean",
        ]
    ].pipe(round_numeric)


def build_debias_table() -> pd.DataFrame:
    agg = pd.read_csv(ROOT / "results" / "synthetic_debias" / "aggregate_eval.csv")
    keep = ["none", "oracle_spurious", "e_bh_pcal", "by_bh", "bh", "p_lt_q", "top_score_k_spurious", "random_k_spurious"]
    table = agg[agg["method"].isin(keep)].copy()
    return table[
        [
            "method",
            "removed_mean",
            "spurious_recall_mean",
            "erroneous_removal_rate_mean",
            "overall_acc_mean",
            "worst_group_acc_mean",
            "conflict_acc_mean",
        ]
    ].pipe(round_numeric)


def build_real_subject_verb_table() -> pd.DataFrame:
    keep = [
        "e_bh_pcal",
        "by_bh",
        "bh",
        "p_lt_q",
        "track_e_bh_pcal",
        "top_score_k_e_bh_pcal",
        "top_score_k_256",
    ]
    frames = []
    for spec in layer_specs():
        path = spec.result_dir / "method_reliability_tracking_comparison.csv"
        if not path.exists():
            continue
        table = pd.read_csv(path)
        table = table[table["method"].isin(keep)].copy()
        table.insert(0, "layer", spec.label)
        frames.append(table)
    if not frames:
        raise FileNotFoundError("no completed subject-verb layer comparison files were found")
    table = pd.concat(frames, ignore_index=True)
    return table[
        [
            "layer",
            "method",
            "discoveries",
            "completeness_r2",
            "centered_r2",
            "abs_effect_fraction",
            "selected_full_corr",
            "sign_agreement",
        ]
    ].pipe(round_numeric)


def build_bounded_bias_probe_table() -> pd.DataFrame:
    discoveries = pd.read_csv(ROOT / "results" / "bias_in_bios" / "cache_analysis" / "method_summary.csv")
    prediction = pd.read_csv(ROOT / "results" / "bias_in_bios" / "prediction_analysis" / "method_summary.csv")
    table = discoveries.merge(prediction, on="method", how="outer")
    return table[
        [
            "method",
            "discoveries",
            "overall_acc",
            "worst_group_acc",
            "group_gap",
            "delta_overall_acc_vs_baseline",
            "delta_worst_group_acc_vs_baseline",
        ]
    ].pipe(round_numeric)


def build_real_decoy_reliability_table() -> pd.DataFrame:
    table = pd.read_csv(ROOT / "results" / "real_subject_verb_reliability" / "decoy_reliability_summary.csv")
    keep = [
        "e_bh_pcal",
        "by_bh",
        "bh",
        "p_lt_q",
        "top_score_matched_e_bh_pcal",
        "top_score_fixed_k_256",
    ]
    table = table[table["method"].isin(keep)].copy()
    return table[
        [
            "layer",
            "method",
            "selection_rule",
            "discoveries_mean",
            "known_null_decoys_selected_mean",
            "known_null_fdp_mean",
        ]
    ].pipe(round_numeric)


def build_real_selection_stability_table() -> pd.DataFrame:
    table = pd.read_csv(ROOT / "results" / "real_subject_verb_reliability" / "selection_stability_summary.csv")
    keep = ["e_bh_pcal", "track_e_bh_pcal", "bh", "p_lt_q"]
    table = table[table["method"].isin(keep)].copy()
    return table[
        [
            "layer",
            "estimand",
            "method",
            "full_discoveries",
            "discoveries_mean",
            "jaccard_mean",
            "recall_full_mean",
        ]
    ].pipe(round_numeric)


def build_real_q_grid_table() -> pd.DataFrame:
    table = pd.read_csv(ROOT / "results" / "real_subject_verb_reliability" / "real_q_grid.csv")
    keep_methods = [
        "e_bh_pcal",
        "bh",
        "p_lt_q",
        "track_e_bh_pcal",
        "track_p_lt_q",
        "top_score_matched_e_bh_pcal",
        "top_score_matched_track_e_bh_pcal",
    ]
    keep_q = {0.01, 0.05, 0.1, 0.2, 0.3}
    table = table[table["method"].isin(keep_methods)].copy()
    table = table[table["q"].isin(keep_q)]
    return table[["layer", "estimand", "q", "method", "discoveries", "selection_rule"]].pipe(round_numeric)


def build_reviewer_qf_sensitivity_table() -> pd.DataFrame:
    table = pd.read_csv(ROOT / "results" / "reviewer_empirical_gaps" / "qf_sensitivity_summary.csv")
    table = table[table["method"] == "e_bh_pcal"].copy()
    return table[
        [
            "layer",
            "q_variant",
            "discoveries",
            "jaccard_to_prompt_uniform_ebh",
            "recall_of_prompt_uniform_ebh",
            "median_abs_tau",
        ]
    ].pipe(round_numeric)


def build_reviewer_pvalue_robustness_table() -> pd.DataFrame:
    table = pd.read_csv(ROOT / "results" / "reviewer_empirical_gaps" / "pvalue_robustness_summary.csv")
    table = table[table["method"] == "e_bh_pcal"].copy()
    return table[
        [
            "layer",
            "p_value_method",
            "discoveries",
            "jaccard_to_paired_t_ebh",
            "recall_of_paired_t_ebh",
            "median_p_selected",
        ]
    ].pipe(round_numeric)


def build_reviewer_method_comparison_table() -> pd.DataFrame:
    table = pd.read_csv(ROOT / "results" / "reviewer_empirical_gaps" / "method_comparison_summary.csv")
    return table[
        [
            "layer",
            "method",
            "discoveries",
            "jaccard_to_ebh",
            "recall_of_ebh",
            "selection_rule",
            "knockoff_negative_count",
            "knockoff_threshold",
        ]
    ].pipe(round_numeric)


def build_reviewer_multisplit_table() -> pd.DataFrame:
    table = pd.read_csv(ROOT / "results" / "reviewer_empirical_gaps" / "multisplit_summary.csv")
    return table[
        [
            "layer",
            "aggregation",
            "discoveries",
            "jaccard_to_single_split_ebh",
            "recall_of_single_split_ebh",
            "mean_selection_frequency_selected",
        ]
    ].pipe(round_numeric)


def build_reviewer_decoy_robustness_table() -> pd.DataFrame:
    table = pd.read_csv(ROOT / "results" / "reviewer_empirical_gaps" / "decoy_robustness_summary.csv")
    keep = [
        "e_bh_pcal",
        "by_bh",
        "bh",
        "weighted_bh_screen",
        "ihw_quantile",
        "adapt_lite",
        "p_lt_q",
        "top_score_matched_e_bh_pcal",
    ]
    table = table[table["method"].isin(keep)].copy()
    return table[
        [
            "layer",
            "decoy_scheme",
            "method",
            "discoveries_mean",
            "known_null_decoys_selected_mean",
            "known_null_fdp_mean",
        ]
    ].pipe(round_numeric)


def build_reviewer_type_sm_table() -> pd.DataFrame:
    table = pd.read_csv(ROOT / "results" / "reviewer_empirical_gaps" / "type_sm_summary.csv")
    return table[
        [
            "method",
            "removed_mean",
            "task_irrelevant_harmful_recall_mean",
            "task_feature_removal_rate_mean",
            "proxy_or_noise_removal_rate_mean",
            "type_s_rate_selected_nonzero_mean",
            "type_m_median_selected_nonzero_mean",
            "worst_group_acc_mean",
            "conflict_acc_mean",
        ]
    ].pipe(round_numeric)


def build_second_round_decoy_bh_by_table() -> pd.DataFrame:
    table = pd.read_csv(ROOT / "results" / "second_round_reviewer" / "decoy_bh_by_all_schemes.csv")
    return table[
        [
            "layer",
            "decoy_scheme",
            "method",
            "discoveries_mean",
            "known_null_decoys_selected_mean",
            "known_null_fdp_mean",
            "decoy_admission_rate_mean",
        ]
    ].pipe(round_numeric)


def build_second_round_gamma_synthetic_table() -> pd.DataFrame:
    table = pd.read_csv(ROOT / "results" / "second_round_reviewer" / "gamma_sensitivity_synthetic_summary.csv")
    return table[
        [
            "gamma",
            "discoveries_mean",
            "fdp_mean",
            "power_mean",
            "jaccard_to_gamma_0_5_mean",
            "recall_of_gamma_0_5_mean",
        ]
    ].pipe(round_numeric)


def build_second_round_gamma_real_table() -> pd.DataFrame:
    table = pd.read_csv(ROOT / "results" / "second_round_reviewer" / "gamma_sensitivity_real.csv")
    return table[
        [
            "layer",
            "gamma",
            "discoveries",
            "jaccard_to_gamma_0_5",
            "recall_of_gamma_0_5",
            "min_p_selected",
        ]
    ].pipe(round_numeric)


def build_second_round_real_ci_type_s_table() -> pd.DataFrame:
    table = pd.read_csv(ROOT / "results" / "second_round_reviewer" / "real_ci_type_s_summary.csv")
    return table[
        [
            "layer",
            "selection",
            "features",
            "ci_width_median",
            "ci_width_p90",
            "ci_crosses_zero_rate",
            "cluster_bootstrap_sign_flip_rate_max",
            "type_s_diagnostic_rate",
        ]
    ].pipe(round_numeric)


def build_second_round_adaptive_ebh_table() -> pd.DataFrame:
    table = pd.read_csv(ROOT / "results" / "second_round_reviewer" / "adaptive_ebh_summary.csv")
    return table[
        [
            "setting",
            "method",
            "discoveries_mean",
            "fdp_mean",
            "power_mean",
            "jaccard_to_default",
            "recall_of_default",
            "gain_vs_default_discoveries",
        ]
    ].pipe(round_numeric)


def build_second_round_cluster_permutation_table() -> pd.DataFrame:
    table = pd.read_csv(ROOT / "results" / "second_round_reviewer" / "cluster_permutation_summary.csv")
    return table[
        [
            "layer",
            "p_value_method",
            "selection_method",
            "clusters",
            "discoveries",
            "jaccard_to_prompt_paired_t_ebh",
            "recall_of_prompt_paired_t_ebh",
        ]
    ].pipe(round_numeric)


def copy_figures(output_dir: Path) -> list[dict[str, str]]:
    figure_specs = [
        (
            "figure_1_gate_b_metrics.png",
            ROOT / "results" / "synthetic_gate_b" / "gate_b_metrics.png",
            "Gate B FDP, power, and CI coverage summary.",
        ),
        (
            "figure_2_q_grid_fdp_power.png",
            ROOT / "results" / "synthetic_gate_b" / "q_grid_fdp_power.png",
            "FDP and power across nominal q values.",
        ),
        (
            "figure_3_synthetic_frontier_fdp_power.png",
            ROOT / "results" / "synthetic_frontier" / "frontier_fdp_power.png",
            "Robustness frontier across dependence, effect, screen, and nuisance scenarios.",
        ),
        (
            "figure_4_ci_frontier_fdp_power.png",
            ROOT / "results" / "synthetic_ci_frontier" / "frontier_fdp_power.png",
            "CI and sample-size frontier.",
        ),
        (
            "figure_5_downstream_debias.png",
            ROOT / "results" / "synthetic_debias" / "debias_worst_group_vs_error.png",
            "Worst-group accuracy versus erroneous-removal rate.",
        ),
        (
            "figure_6_reviewer_empirical_gaps.png",
            ROOT / "results" / "reviewer_empirical_gaps" / "reviewer_gap_summary.png",
            "Summary of the six reviewer-requested empirical gap analyses.",
        ),
        (
            "figure_7_second_round_real_ci_type_s.png",
            ROOT / "results" / "second_round_reviewer" / "real_ci_type_s_summary.png",
            "Real per-feature CI width distribution and Type S sign-instability diagnostic.",
        ),
        (
            "figure_8_second_round_summary.png",
            ROOT / "results" / "second_round_reviewer" / "second_round_summary.png",
            "Summary of second-round reviewer empirical analyses.",
        ),
    ]
    copied = []
    for name, source, description in figure_specs:
        if not source.exists():
            continue
        target = output_dir / name
        shutil.copy2(source, target)
        copied.append(
            {
                "file": name,
                "source": source.relative_to(ROOT).as_posix(),
                "description": description,
            }
        )
    return copied


def build_inventory() -> pd.DataFrame:
    rows = []
    excluded_parts = {
        "__pycache__",
        ".pytest_cache",
        "pytest_tmp",
        "pytest_cache",
        "pytest_env_tmp",
    }
    for dirpath, dirnames, filenames in os.walk(ROOT, onerror=lambda _exc: None):
        dirnames[:] = [
            name
            for name in dirnames
            if name not in excluded_parts and not name.startswith("pytest-cache-files-")
        ]
        for filename in filenames:
            rel = Path(dirpath) / filename
            if any(part in excluded_parts or part.startswith("pytest-cache-files-") for part in rel.parts):
                continue
            rel_path = rel.relative_to(ROOT).as_posix()
            try:
                rows.append(
                    {
                        "path": rel_path,
                        "bytes": rel.stat().st_size,
                        "sha256_12": sha256_prefix(rel),
                    }
                )
            except OSError:
                continue
    return pd.DataFrame(rows)


def sha256_prefix(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()[:12]


def write_summary(
    path: Path,
    tables: dict[str, pd.DataFrame],
    figures: list[dict[str, str]],
    inventory: pd.DataFrame,
) -> None:
    lines = [
        "# Paper Asset Index",
        "",
        "This folder contains compact tables and an artifact inventory generated",
        "from the current experiment outputs. It is for paper writing support, not",
        "paper prose.",
        "",
        "## Tables",
        "",
    ]
    for name, table in tables.items():
        lines.extend(
            [
                f"### {name}",
                "",
                table.to_markdown(index=False),
                "",
            ]
        )
    lines.extend(["## Figures", ""])
    if figures:
        for figure in figures:
            lines.append(
                f"- `{figure['file']}`: {figure['description']} "
                f"Source: `{figure['source']}`."
            )
    else:
        lines.append("- No figure files were found to copy.")
    lines.append("")
    lines.extend(
        [
            "## Inventory",
            "",
            f"Tracked files: {len(inventory)}",
            "",
            "See `artifact_inventory.csv` for file sizes and SHA-256 prefixes.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def round_numeric(table: pd.DataFrame) -> pd.DataFrame:
    out = table.copy()
    for col in out.columns:
        if pd.api.types.is_numeric_dtype(out[col]):
            out[col] = out[col].round(4)
    return out


def safe_display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return path.name


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT / "src"))
    main()
