from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from reliacircuit.pipeline import summarize_methods


def main() -> None:
    args = parse_args()
    features = pd.read_csv(args.per_feature)
    config = load_json(args.config)
    q_values = [float(q) for q in args.q_values.split(",")]
    n_active = int(config["synthetic"]["n_active"])

    rows = []
    for q in q_values:
        replicate_summaries = []
        for _, group in features.groupby("replicate", sort=True):
            replicate_summaries.append(
                summarize_methods(
                    features=group.reset_index(drop=True),
                    q=q,
                    n_total_active=n_active,
                    heldout_n=-1,
                )
            )
        summary = pd.concat(replicate_summaries, ignore_index=True)
        aggregate = aggregate_by_q(summary)
        aggregate.insert(0, "q", q)
        rows.append(aggregate)

    q_grid = pd.concat(rows, ignore_index=True)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    q_grid.to_csv(args.output_dir / "q_grid_metrics.csv", index=False)
    plot_q_grid(q_grid, args.output_dir / "q_grid_fdp_power.png")
    write_q_grid_report(args.output_dir / "q_grid_report.md", q_grid, q_values)
    print(q_grid.to_string(index=False))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--per-feature",
        type=Path,
        default=ROOT / "results" / "synthetic_gate_b" / "per_feature.csv",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=ROOT / "configs" / "synthetic_gate_b.json",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "results" / "synthetic_gate_b",
    )
    parser.add_argument("--q-values", default="0.02,0.05,0.1,0.15,0.2")
    return parser.parse_args()


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def aggregate_by_q(summary: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for method, group in summary.groupby("method", sort=False):
        row = {"method": method, "replicates": int(group.shape[0])}
        for metric in ["fdp", "power", "discoveries", "false_discoveries", "ci_coverage_selected"]:
            values = group[metric].dropna()
            row[f"{metric}_mean"] = float(values.mean()) if not values.empty else float("nan")
            row[f"{metric}_se"] = float(values.std(ddof=1) / (values.shape[0] ** 0.5)) if values.shape[0] > 1 else 0.0
        rows.append(row)
    return pd.DataFrame(rows)


def plot_q_grid(q_grid: pd.DataFrame, path: Path) -> None:
    methods = ["e_bh_pcal", "by_bh", "bh", "p_lt_q", "top_score_k_active"]
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), constrained_layout=True)
    for method in methods:
        data = q_grid[q_grid["method"] == method].sort_values("q")
        if data.empty:
            continue
        axes[0].errorbar(data["q"], data["fdp_mean"], yerr=data["fdp_se"], marker="o", label=method)
        axes[1].errorbar(data["q"], data["power_mean"], yerr=data["power_se"], marker="o", label=method)
    axes[0].plot([0, q_grid["q"].max()], [0, q_grid["q"].max()], linestyle="--", color="black", linewidth=1)
    axes[0].set_title("Achieved FDP vs nominal q")
    axes[0].set_xlabel("Nominal q")
    axes[0].set_ylabel("Mean FDP")
    axes[1].set_title("Power vs nominal q")
    axes[1].set_xlabel("Nominal q")
    axes[1].set_ylabel("Mean power")
    axes[1].legend(fontsize=8)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def write_q_grid_report(path: Path, q_grid: pd.DataFrame, q_values: list[float]) -> None:
    lines = [
        "# Synthetic q-grid Analysis",
        "",
        f"Nominal q values: {q_values}",
        "",
        "The dashed line in `q_grid_fdp_power.png` is achieved FDP = nominal q.",
        "",
        q_grid.to_markdown(index=False),
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
