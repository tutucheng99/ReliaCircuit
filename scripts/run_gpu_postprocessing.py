from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from reliacircuit.bias_eval import group_metrics, method_summary, normalize_prediction_cache  # noqa: E402
from reliacircuit.cache_analysis import analyze_ablation_cache, analyze_circuit_cache, selected_feature_list  # noqa: E402
from validate_runpod_outputs import validate_one  # noqa: E402


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    validation = validate_inputs(args)
    validation.to_csv(args.output_dir / "runpod_output_validation.csv", index=False)

    steps: list[dict[str, Any]] = []
    if not validation["ok"].all():
        steps.append({"step": "validation", "status": "failed", "details": "one or more input files failed schema checks"})
        write_summary(args.output_dir, steps)
        raise SystemExit(1)
    steps.append({"step": "validation", "status": "ok", "details": f"{len(validation)} files checked"})

    exact_status = run_exact_analysis(args)
    steps.append(exact_status)
    circuit_status = run_circuit_analysis(args)
    steps.append(circuit_status)
    bias_status = run_bias_prediction_analysis(args)
    steps.append(bias_status)

    write_summary(args.output_dir, steps)
    print(pd.DataFrame(steps).to_string(index=False))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run CPU post-processing after RunPod outputs are copied back.")
    parser.add_argument("--smoke-report", type=Path, default=ROOT / "results" / "gpu_smoke" / "local_skip_report.json")
    parser.add_argument(
        "--screen-scores",
        type=Path,
        default=ROOT / "results" / "subject_verb_agreement" / "screen_scores_dry_run.csv",
    )
    parser.add_argument(
        "--exact-ablation-cache",
        type=Path,
        default=ROOT / "results" / "subject_verb_agreement" / "exact_ablation_cache_dry_run.csv",
    )
    parser.add_argument(
        "--joint-circuit-cache",
        type=Path,
        default=ROOT / "results" / "subject_verb_agreement" / "joint_circuit_cache_dry_run.csv",
    )
    parser.add_argument(
        "--prediction-cache",
        type=Path,
        default=ROOT / "results" / "bias_in_bios" / "bias_in_bios_prediction_cache_dry_run.csv",
    )
    parser.add_argument("--bias-labels", type=Path, default=ROOT / "data" / "bias_in_bios" / "prompts.csv")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "results" / "postrun_analysis_dry_run")
    parser.add_argument("--q", type=float, default=0.1)
    parser.add_argument("--e-gamma", type=float, default=0.5)
    parser.add_argument("--n-bootstrap", type=int, default=99)
    parser.add_argument("--confidence", type=float, default=0.95)
    parser.add_argument("--seed", type=int, default=0)
    return parser.parse_args()


def validate_inputs(args: argparse.Namespace) -> pd.DataFrame:
    rows = [
        validate_one("smoke_report", args.smoke_report),
        validate_one("screen_scores", args.screen_scores),
        validate_one("exact_ablation_cache", args.exact_ablation_cache),
        validate_one("joint_circuit_cache", args.joint_circuit_cache),
        validate_one("prediction_cache", args.prediction_cache),
    ]
    return pd.DataFrame(rows)


def run_exact_analysis(args: argparse.Namespace) -> dict[str, Any]:
    out_dir = args.output_dir / "exact_ablation_analysis"
    cache = pd.read_csv(args.exact_ablation_cache)
    per_feature_n = cache.groupby("feature_id").size()
    if per_feature_n.empty or int(per_feature_n.min()) < 2:
        return {
            "step": "exact_ablation_analysis",
            "status": "skipped",
            "details": "need at least two rows per feature for paired inference",
        }
    feature_stats, summary = analyze_ablation_cache(
        cache,
        q=args.q,
        e_gamma=args.e_gamma,
        n_bootstrap=args.n_bootstrap,
        confidence=args.confidence,
        seed=args.seed,
    )
    out_dir.mkdir(parents=True, exist_ok=True)
    feature_stats.to_csv(out_dir / "feature_stats.csv", index=False)
    summary.to_csv(out_dir / "method_summary.csv", index=False)
    selected_cols = ["feature_id", "tau_hat", "p_value", "e_value", "ci_lower", "ci_upper"]
    selected_cols += [c for c in feature_stats.columns if c.startswith("selected_")]
    feature_stats.loc[:, selected_cols].to_csv(out_dir / "selected_features.csv", index=False)
    for method in [c.removeprefix("selected_") for c in feature_stats.columns if c.startswith("selected_")]:
        selected_feature_list(feature_stats, method=method).to_csv(
            out_dir / f"selected_features_{method}.csv",
            index=False,
        )
    return {
        "step": "exact_ablation_analysis",
        "status": "ok",
        "details": f"{feature_stats.shape[0]} features; {summary['discoveries'].sum()} total method discoveries",
    }


def run_circuit_analysis(args: argparse.Namespace) -> dict[str, Any]:
    out_dir = args.output_dir / "circuit_analysis"
    cache = pd.read_csv(args.joint_circuit_cache)
    summary = analyze_circuit_cache(cache)
    out_dir.mkdir(parents=True, exist_ok=True)
    summary.to_csv(out_dir / "circuit_method_summary.csv", index=False)
    return {
        "step": "circuit_analysis",
        "status": "ok",
        "details": f"{summary.shape[0]} methods",
    }


def run_bias_prediction_analysis(args: argparse.Namespace) -> dict[str, Any]:
    out_dir = args.output_dir / "bias_prediction_analysis"
    predictions = pd.read_csv(args.prediction_cache)
    labels = pd.read_csv(args.bias_labels) if args.bias_labels else None
    normalized = normalize_prediction_cache(predictions, labels)
    groups = group_metrics(normalized)
    summary = method_summary(normalized, groups)
    out_dir.mkdir(parents=True, exist_ok=True)
    normalized.to_csv(out_dir / "example_metrics.csv", index=False)
    groups.to_csv(out_dir / "group_metrics.csv", index=False)
    summary.to_csv(out_dir / "method_summary.csv", index=False)
    return {
        "step": "bias_prediction_analysis",
        "status": "ok",
        "details": f"{summary.shape[0]} methods",
    }


def write_summary(output_dir: Path, steps: list[dict[str, Any]]) -> None:
    frame = pd.DataFrame(steps)
    frame.to_csv(output_dir / "postrun_summary.csv", index=False)
    lines = [
        "# GPU Post-Run Analysis Summary",
        "",
        frame.to_markdown(index=False),
        "",
    ]
    (output_dir / "postrun_summary.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
