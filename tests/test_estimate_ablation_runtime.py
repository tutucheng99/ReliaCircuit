from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import estimate_ablation_runtime as estimate


def test_amortized_fit_uses_two_point_slope() -> None:
    points = [
        {"rows_written": 40, "elapsed_sec": 160.0, "sec_per_row": 4.0, "path": "a"},
        {"rows_written": 120, "elapsed_sec": 200.0, "sec_per_row": 1.667, "path": "b"},
    ]

    fit = estimate.amortized_fit(points, target_rows=200)

    assert fit["sec_per_row"] == 0.5
    assert fit["overhead_sec"] == 140.0
    assert fit["elapsed_sec"] == 240.0


def test_build_estimate_infers_target_rows(tmp_path: Path) -> None:
    smoke = tmp_path / "smoke.metadata.json"
    pilot = tmp_path / "pilot.metadata.json"
    smoke.write_text(json.dumps({"rows_written": 40, "elapsed_sec": 160.0}), encoding="utf-8")
    pilot.write_text(json.dumps({"rows_written": 120, "elapsed_sec": 200.0}), encoding="utf-8")
    prompts = tmp_path / "prompts.csv"
    features = tmp_path / "features.csv"
    pd.DataFrame({"prompt_id": ["a", "b", "c"], "split": ["test", "test", "screen"]}).to_csv(prompts, index=False)
    pd.DataFrame({"feature_id": [1, 2, 3, 4]}).to_csv(features, index=False)
    args = argparse.Namespace(
        metadata=[smoke, pilot],
        prompts=prompts,
        features=features,
        split="test",
        target_rows=None,
    )

    frame = estimate.build_estimate(args)

    assert int(frame.loc[0, "target_rows"]) == 8
    assert int(frame.loc[0, "metadata_points"]) == 2
