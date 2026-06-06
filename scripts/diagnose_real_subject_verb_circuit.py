from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    args = parse_args()
    prompts = pd.read_csv(args.prompts)
    screen = pd.read_csv(args.screen_scores)
    feature_stats = pd.read_csv(args.feature_stats)
    circuit = pd.read_csv(args.circuit_cache)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    split_template = pd.crosstab(prompts["template_id"], prompts["split"])
    split_template.to_csv(args.output_dir / "split_template_crosstab.csv")

    feature_diag = feature_stats.merge(
        screen[
            [
                "feature_id",
                "screen_rank",
                "screen_score",
                "mean_abs_activation_delta",
                "mean_metric_weighted_delta",
            ]
        ],
        on="feature_id",
        how="left",
    )
    feature_diag.to_csv(args.output_dir / "feature_screen_exact_diagnostics.csv", index=False)

    circuit_diag = circuit_metrics(circuit)
    circuit_diag.to_csv(args.output_dir / "circuit_prompt_tracking_diagnostics.csv", index=False)

    summary = build_summary(prompts, feature_diag, circuit_diag)
    summary.to_csv(args.output_dir / "diagnostic_summary.csv", index=False)
    write_report(args.output_dir / "diagnostic_report.md", summary, split_template, feature_diag, circuit_diag)
    print(f"wrote subject-verb diagnostics to {safe_display_path(args.output_dir)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Diagnose weak real subject-verb circuit tracking.")
    parser.add_argument(
        "--prompts",
        type=Path,
        default=ROOT / "data" / "subject_verb_agreement" / "prompts.csv",
    )
    parser.add_argument(
        "--screen-scores",
        type=Path,
        default=ROOT / "results" / "subject_verb_agreement" / "screen_scores.csv",
    )
    parser.add_argument(
        "--feature-stats",
        type=Path,
        default=ROOT / "results" / "subject_verb_agreement" / "cache_analysis" / "feature_stats.csv",
    )
    parser.add_argument(
        "--circuit-cache",
        type=Path,
        default=ROOT / "results" / "subject_verb_agreement" / "joint_circuit_cache.csv",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "results" / "subject_verb_agreement" / "diagnostics",
    )
    return parser.parse_args()


def circuit_metrics(circuit: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for method, group in circuit.groupby("method", sort=False):
        full = group["full_difference"].to_numpy(dtype=float)
        selected = group["selected_difference"].to_numpy(dtype=float)
        residual = full - selected
        centered_denom = float(np.sum((full - np.mean(full)) ** 2))
        corr = np.nan
        if np.std(full) > 0.0 and np.std(selected) > 0.0:
            corr = float(np.corrcoef(full, selected)[0, 1])
        rows.append(
            {
                "method": method,
                "heldout_n": int(len(group)),
                "full_mean": float(np.mean(full)),
                "full_std": float(np.std(full)),
                "selected_mean": float(np.mean(selected)),
                "selected_std": float(np.std(selected)),
                "residual_mean": float(np.mean(residual)),
                "residual_std": float(np.std(residual)),
                "selected_full_corr": corr,
                "centered_r2": float(1.0 - np.sum(residual**2) / max(centered_denom, 1e-12)),
                "uncentered_completeness_r2": float(1.0 - np.mean(residual**2) / max(np.mean(full**2), 1e-12)),
                "abs_effect_fraction": float(np.mean(np.abs(selected)) / max(np.mean(np.abs(full)), 1e-12)),
            }
        )
    return pd.DataFrame(rows)


def build_summary(prompts: pd.DataFrame, feature_diag: pd.DataFrame, circuit_diag: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    split_counts = prompts.groupby("split").size()
    rows.append(
        {
            "check": "split_rows",
            "value": "; ".join(f"{split}={count}" for split, count in split_counts.items()),
            "assessment": "informational",
        }
    )
    for split, group in prompts.groupby("split"):
        template_share = group["template_id"].value_counts(normalize=True).max()
        n_templates = group["template_id"].nunique()
        rows.append(
            {
                "check": f"{split}_template_coverage",
                "value": f"n_templates={n_templates}; max_template_share={template_share:.3f}",
                "assessment": "fail" if n_templates < prompts["template_id"].nunique() else "pass",
            }
        )

    for flag in [col for col in feature_diag.columns if col.startswith("selected_")]:
        selected = feature_diag[feature_diag[flag].fillna(False).astype(bool)]
        if selected.empty:
            rows.append({"check": f"{flag}_screen_recall_proxy", "value": "n=0", "assessment": "informational"})
            continue
        rows.append(
            {
                "check": f"{flag}_screen_recall_proxy",
                "value": (
                    f"n={len(selected)}; max_screen_rank={int(selected['screen_rank'].max())}; "
                    f"median_screen_rank={float(selected['screen_rank'].median()):.1f}"
                ),
                "assessment": "warning" if selected["screen_rank"].max() > 0.8 * len(feature_diag) else "pass",
            }
        )

    tail = feature_diag.sort_values("screen_rank").tail(max(5, int(0.1 * len(feature_diag))))
    rows.append(
        {
            "check": "top_k_boundary_signal",
            "value": f"tail_min_p={tail['p_value'].min():.4g}; tail_max_abs_tau={tail['tau_hat'].abs().max():.4g}",
            "assessment": "warning" if tail["p_value"].min() < 0.01 else "pass",
        }
    )

    for _, row in circuit_diag.iterrows():
        corr = float(row["selected_full_corr"])
        centered_r2 = float(row["centered_r2"])
        rows.append(
            {
                "check": f"{row['method']}_prompt_tracking",
                "value": (
                    f"corr={corr:.4f}; centered_r2={centered_r2:.4f}; "
                    f"uncentered_completeness_r2={float(row['uncentered_completeness_r2']):.4f}"
                ),
                "assessment": "fail" if corr < 0.2 or centered_r2 < 0.0 else "pass",
            }
        )
    return pd.DataFrame(rows)


def write_report(
    path: Path,
    summary: pd.DataFrame,
    split_template: pd.DataFrame,
    feature_diag: pd.DataFrame,
    circuit_diag: pd.DataFrame,
) -> None:
    strongest = feature_diag.sort_values("p_value").head(12)
    lines = [
        "# Real subject-verb circuit diagnostic",
        "",
        "## Summary",
        summary.to_markdown(index=False),
        "",
        "## Split by template",
        split_template.to_markdown(),
        "",
        "## Prompt-level tracking",
        circuit_diag.to_markdown(index=False),
        "",
        "## Strongest exact-ablation features",
        strongest[
            [
                "feature_id",
                "screen_rank",
                "screen_score",
                "tau_hat",
                "se",
                "p_value",
                "e_value",
            ]
        ].to_markdown(index=False),
        "",
        "## Diagnosis",
        "- The current split is template-confounded when any split lacks all templates.",
        "- The FDR test selects nonzero mean resample-ablation effects; this does not by itself optimize prompt-level covariance with the full clean-vs-patch effect.",
        "- A convincing real circuit should be rerun on pair/template-stratified splits and evaluated with corr beside uncentered completeness.",
    ]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def safe_display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    main()
