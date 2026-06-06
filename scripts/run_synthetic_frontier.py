from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from reliacircuit.pipeline import PipelineConfig, run_replicate
from reliacircuit.synthetic import SyntheticConfig


def main() -> None:
    args = parse_args()
    config = load_json(args.config)
    if args.replicates is not None:
        config["replicates"] = args.replicates
    output_dir = ROOT / config["output_dir"]
    output_dir.mkdir(parents=True, exist_ok=True)

    feature_frames = []
    summary_frames = []
    circuit_frames = []
    scenario_records = []
    for scenario in config["scenarios"]:
        name = scenario["name"]
        synth_dict = {**config["base_synthetic"], **scenario.get("synthetic", {})}
        pipe_dict = {**config["base_pipeline"], **scenario.get("pipeline", {})}
        scenario_records.append(
            {
                "scenario": name,
                "description": scenario.get("description", ""),
                **{f"synthetic.{k}": v for k, v in synth_dict.items()},
                **{f"pipeline.{k}": v for k, v in pipe_dict.items()},
            }
        )
        for rep in range(int(config["replicates"])):
            synthetic = SyntheticConfig(**synth_dict)
            pipeline = PipelineConfig(synthetic=synthetic, **pipe_dict)
            features, summary, circuit = run_replicate(pipeline, replicate=rep)
            features.insert(0, "scenario", name)
            summary.insert(0, "scenario", name)
            circuit.insert(0, "scenario", name)
            feature_frames.append(features)
            summary_frames.append(summary)
            circuit_frames.append(circuit)
            print(f"{name}: replicate {rep + 1}/{config['replicates']} complete", flush=True)

    feature_table = pd.concat(feature_frames, ignore_index=True)
    summary_table = pd.concat(summary_frames, ignore_index=True)
    circuit_table = pd.concat(circuit_frames, ignore_index=True)
    scenario_table = pd.DataFrame(scenario_records)
    aggregate = aggregate_frontier(summary_table)
    circuit_aggregate = aggregate_circuit_frontier(circuit_table)

    feature_table.to_csv(output_dir / "per_feature.csv", index=False)
    summary_table.to_csv(output_dir / "replicate_summary.csv", index=False)
    circuit_table.to_csv(output_dir / "circuit_summary.csv", index=False)
    scenario_table.to_csv(output_dir / "scenario_config.csv", index=False)
    aggregate.to_csv(output_dir / "aggregate_metrics.csv", index=False)
    circuit_aggregate.to_csv(output_dir / "circuit_aggregate_metrics.csv", index=False)
    plot_frontier(aggregate, output_dir / "frontier_fdp_power.png")
    write_report(output_dir / "frontier_report.md", aggregate, circuit_aggregate, scenario_table, config)

    print("\nFrontier aggregate metrics:")
    print(aggregate.to_string(index=False))
    print("\nFrontier circuit aggregate metrics:")
    print(circuit_aggregate.to_string(index=False))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=ROOT / "configs" / "synthetic_frontier.json")
    parser.add_argument("--replicates", type=int, default=None)
    return parser.parse_args()


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def aggregate_frontier(summary: pd.DataFrame) -> pd.DataFrame:
    rows = []
    metrics = [
        "discoveries",
        "false_discoveries",
        "true_discoveries",
        "fdp",
        "power",
        "ci_coverage_selected",
        "screen_recall",
        "ci_coverage_screened",
    ]
    for (scenario, method), group in summary.groupby(["scenario", "method"], sort=False):
        row = {
            "scenario": scenario,
            "method": method,
            "replicates": int(group.shape[0]),
        }
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


def aggregate_circuit_frontier(circuit: pd.DataFrame) -> pd.DataFrame:
    rows = []
    metrics = [
        "completeness_r2",
        "necessity_fraction",
        "abs_effect_fraction",
        "selected_full_corr",
        "sign_agreement",
    ]
    for (scenario, method), group in circuit.groupby(["scenario", "method"], sort=False):
        row = {
            "scenario": scenario,
            "method": method,
            "replicates": int(group.shape[0]),
        }
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


def plot_frontier(aggregate: pd.DataFrame, path: Path) -> None:
    methods = ["e_bh_pcal", "by_bh", "bh", "p_lt_q", "top_score_k_active"]
    scenarios = list(dict.fromkeys(aggregate["scenario"].tolist()))
    x = range(len(scenarios))
    fig, axes = plt.subplots(2, 1, figsize=(10, 7), constrained_layout=True)
    for method in methods:
        data = aggregate[aggregate["method"] == method].set_index("scenario").reindex(scenarios)
        axes[0].plot(x, data["fdp_mean"], marker="o", label=method)
        axes[1].plot(x, data["power_mean"], marker="o", label=method)
    axes[0].axhline(0.1, linestyle="--", color="black", linewidth=1, label="nominal q=0.1")
    axes[0].set_ylabel("Mean FDP")
    axes[0].set_title("Synthetic frontier: achieved FDP")
    axes[1].set_ylabel("Mean power")
    axes[1].set_title("Synthetic frontier: power")
    for ax in axes:
        ax.set_xticks(list(x), scenarios, rotation=20, ha="right")
        ax.set_ylim(bottom=0.0)
        ax.grid(axis="y", alpha=0.25)
    axes[1].legend(fontsize=8, ncol=3)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def write_report(
    path: Path,
    aggregate: pd.DataFrame,
    circuit_aggregate: pd.DataFrame,
    scenarios: pd.DataFrame,
    config: dict,
) -> None:
    focus_cols = [
        "scenario",
        "method",
        "discoveries_mean",
        "fdp_mean",
        "power_mean",
        "screen_recall_mean",
        "ci_coverage_screened_mean",
    ]
    lines = [
        "# Synthetic Frontier Report",
        "",
        "This report extends Gate B from one synthetic setting to a compact robustness frontier.",
        "",
        "## Scenario configuration",
        "",
        scenarios.to_markdown(index=False),
        "",
        "## Aggregate metrics",
        "",
        aggregate.loc[:, focus_cols].to_markdown(index=False),
        "",
        "## Held-out circuit metrics",
        "",
        circuit_aggregate.to_markdown(index=False),
        "",
        "## Raw configuration",
        "",
        "```json",
        json.dumps(config, indent=2),
        "```",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
