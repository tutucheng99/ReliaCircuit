from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from reliacircuit.debias import DebiasConfig, run_debias_replicate


def main() -> None:
    args = parse_args()
    config = load_json(args.config)
    if args.replicates is not None:
        config["replicates"] = args.replicates
    output_dir = ROOT / config["output_dir"]
    output_dir.mkdir(parents=True, exist_ok=True)

    debias_config = DebiasConfig(**config["config"])
    feature_frames = []
    eval_frames = []
    for rep in range(int(config["replicates"])):
        features, evaluation = run_debias_replicate(debias_config, rep)
        feature_frames.append(features)
        eval_frames.append(evaluation)
        print(f"debias replicate {rep + 1}/{config['replicates']} complete", flush=True)

    feature_table = pd.concat(feature_frames, ignore_index=True)
    eval_table = pd.concat(eval_frames, ignore_index=True)
    aggregate = aggregate_eval(eval_table)
    feature_table.to_csv(output_dir / "feature_stats.csv", index=False)
    eval_table.to_csv(output_dir / "replicate_eval.csv", index=False)
    aggregate.to_csv(output_dir / "aggregate_eval.csv", index=False)
    plot_debias(aggregate, output_dir / "debias_worst_group_vs_error.png")
    write_report(output_dir / "debias_report.md", aggregate, config)

    print("\nDebias aggregate metrics:")
    print(aggregate.to_string(index=False))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=ROOT / "configs" / "synthetic_debias.json")
    parser.add_argument("--replicates", type=int, default=None)
    return parser.parse_args()


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def aggregate_eval(eval_table: pd.DataFrame) -> pd.DataFrame:
    rows = []
    metrics = [
        "removed",
        "spurious_removed",
        "task_removed",
        "proxy_removed",
        "noise_removed",
        "erroneous_removal_rate",
        "spurious_recall",
        "overall_acc",
        "worst_group_acc",
        "aligned_acc",
        "conflict_acc",
        "gap_aligned_conflict",
        "mean_abs_score",
    ]
    for method, group in eval_table.groupby("method", sort=False):
        row = {"method": method, "replicates": int(group.shape[0])}
        for metric in metrics:
            values = group[metric].dropna()
            row[f"{metric}_mean"] = float(values.mean()) if not values.empty else float("nan")
            row[f"{metric}_se"] = (
                float(values.std(ddof=1) / (values.shape[0] ** 0.5))
                if values.shape[0] > 1
                else 0.0
            )
        rows.append(row)
    return pd.DataFrame(rows)


def plot_debias(aggregate: pd.DataFrame, path: Path) -> None:
    methods = aggregate["method"].tolist()
    fig, axes = plt.subplots(1, 2, figsize=(12, 4), constrained_layout=True)
    axes[0].bar(methods, aggregate["worst_group_acc_mean"], yerr=aggregate["worst_group_acc_se"], capsize=3)
    axes[0].set_title("Worst-group accuracy")
    axes[0].set_ylim(0.0, 1.0)
    axes[0].tick_params(axis="x", rotation=35)
    axes[1].bar(methods, aggregate["erroneous_removal_rate_mean"], yerr=aggregate["erroneous_removal_rate_se"], capsize=3)
    axes[1].set_title("Erroneous removal rate")
    axes[1].set_ylim(0.0, 1.0)
    axes[1].tick_params(axis="x", rotation=35)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def write_report(path: Path, aggregate: pd.DataFrame, config: dict) -> None:
    focus = [
        "method",
        "removed_mean",
        "spurious_recall_mean",
        "erroneous_removal_rate_mean",
        "overall_acc_mean",
        "worst_group_acc_mean",
        "conflict_acc_mean",
        "gap_aligned_conflict_mean",
    ]
    lines = [
        "# Synthetic SHIFT-style Debiasing Report",
        "",
        "This experiment evaluates FDR-controlled removal of task-irrelevant",
        "gender-spurious features in a controlled downstream classification task.",
        "",
        "## Aggregate metrics",
        "",
        aggregate.loc[:, focus].to_markdown(index=False),
        "",
        "## Configuration",
        "",
        "```json",
        json.dumps(config, indent=2),
        "```",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
