from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import create_circuit_eval_manifest as circuit_manifest


def test_load_feature_sets_accepts_named_specs(tmp_path: Path) -> None:
    selected_a = tmp_path / "a.csv"
    selected_b = tmp_path / "b.csv"
    pd.DataFrame({"feature_id": [1, 2]}).to_csv(selected_a, index=False)
    pd.DataFrame({"feature_id": [3]}).to_csv(selected_b, index=False)
    args = argparse.Namespace(
        feature_set=[f"e_bh={selected_a}", f"top_score={selected_b}"],
        selected_features=[],
        method=None,
        feature_column="feature_id",
    )

    sets = circuit_manifest.load_feature_sets(args)

    assert sets == [("e_bh", ["1", "2"]), ("top_score", ["3"])]


def test_load_feature_sets_preserves_legacy_selected_features(tmp_path: Path) -> None:
    selected = tmp_path / "selected_features_bh.csv"
    pd.DataFrame({"feature_id": [4], "selection_method": ["bh"]}).to_csv(selected, index=False)
    args = argparse.Namespace(
        feature_set=[],
        selected_features=[selected],
        method=None,
        feature_column="feature_id",
    )

    sets = circuit_manifest.load_feature_sets(args)

    assert sets == [("bh", ["4"])]
