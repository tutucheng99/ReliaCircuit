from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROTOCOL = ROOT / "configs" / "subject_verb_layer_scan_protocol.json"


@dataclass(frozen=True)
class SubjectVerbLayerSpec:
    label: str
    layer: int
    sae_id: str
    data_dir: Path
    result_dir: Path


def load_protocol(path: Path = DEFAULT_PROTOCOL) -> dict[str, Any]:
    protocol_path = path if path.is_absolute() else ROOT / path
    return json.loads(protocol_path.read_text(encoding="utf-8"))


def layer_specs(path: Path = DEFAULT_PROTOCOL) -> list[SubjectVerbLayerSpec]:
    protocol = load_protocol(path)
    specs = []
    for item in protocol["layers"]:
        specs.append(
            SubjectVerbLayerSpec(
                label=str(item["label"]),
                layer=int(item["layer"]),
                sae_id=str(item["sae_id"]),
                data_dir=ROOT / str(item["data_dir"]),
                result_dir=ROOT / str(item["result_dir"]),
            )
        )
    return specs


def required_layer_files(spec: SubjectVerbLayerSpec) -> dict[str, Path]:
    return {
        "screened_features": spec.data_dir / "screened_features.csv",
        "ablation_manifest": spec.data_dir / "ablation_manifest.csv",
        "circuit_eval_manifest": spec.data_dir / "circuit_eval_manifest.csv",
        "clean_metric_cache": spec.result_dir / "clean_metric_cache.csv",
        "screen_scores": spec.result_dir / "screen_scores.csv",
        "exact_ablation_cache": spec.result_dir / "exact_ablation_cache.csv",
        "feature_stats": spec.result_dir / "cache_analysis" / "feature_stats.csv",
        "feature_stats_tracking": spec.result_dir / "cache_analysis" / "feature_stats_tracking.csv",
        "prompt_full_effects_exact": spec.result_dir / "cache_analysis" / "prompt_full_effects_exact.csv",
        "method_reliability_tracking_comparison": spec.result_dir / "method_reliability_tracking_comparison.csv",
        "joint_circuit_cache": spec.result_dir / "joint_circuit_cache.csv",
        "circuit_method_summary": spec.result_dir / "circuit_cache_analysis" / "circuit_method_summary.csv",
    }


def layer_status(path: Path = DEFAULT_PROTOCOL) -> pd.DataFrame:
    rows = []
    for spec in layer_specs(path):
        files = required_layer_files(spec)
        missing = [name for name, file_path in files.items() if not file_path.exists()]
        rows.append(
            {
                "layer": spec.label,
                "layer_index": spec.layer,
                "sae_id": spec.sae_id,
                "data_dir": safe_display_path(spec.data_dir),
                "result_dir": safe_display_path(spec.result_dir),
                "status": "complete" if not missing else "missing",
                "missing_files": ";".join(missing),
            }
        )
    return pd.DataFrame(rows)


def completed_layer_specs(path: Path = DEFAULT_PROTOCOL) -> list[SubjectVerbLayerSpec]:
    status = layer_status(path).set_index("layer")
    return [spec for spec in layer_specs(path) if status.loc[spec.label, "status"] == "complete"]


def safe_display_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT.resolve())).replace("\\", "/")
    except ValueError:
        return str(path)
