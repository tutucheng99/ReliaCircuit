from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd
import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import produce_sae_circuit_cache as circuit_cache


def minimal_args() -> argparse.Namespace:
    return argparse.Namespace(
        prompt_id_column="prompt_id",
        prompt_column="clean_prompt",
        patch_prompt_column="patch_prompt",
        target_column="target_token",
        counter_column="counter_token",
        selected_features_column="selected_feature_ids",
        method_column="method",
        hook_name=None,
        sae_acts_hook=None,
        include_text=False,
    )


def test_parse_feature_ids_accepts_semicolon_and_comma() -> None:
    assert circuit_cache.parse_feature_ids("1;2;3") == [1, 2, 3]
    assert circuit_cache.parse_feature_ids("1, 2, 3") == [1, 2, 3]
    assert circuit_cache.parse_feature_ids("") == []


def test_validate_manifest_accepts_required_columns() -> None:
    args = minimal_args()
    manifest = pd.DataFrame(
        {
            "prompt_id": ["p0"],
            "clean_prompt": ["The key"],
            "patch_prompt": ["The keys"],
            "target_token": [" is"],
            "counter_token": [" are"],
            "selected_feature_ids": ["1;2"],
            "method": ["e_bh_pcal"],
        }
    )
    circuit_cache.validate_manifest(manifest, args)


def test_validate_manifest_rejects_missing_columns() -> None:
    args = minimal_args()
    manifest = pd.DataFrame({"prompt_id": ["p0"], "method": ["e_bh_pcal"]})
    with pytest.raises(SystemExit, match="circuit manifest missing required columns"):
        circuit_cache.validate_manifest(manifest, args)


def test_output_row_matches_circuit_cache_schema() -> None:
    args = minimal_args()
    row = pd.Series(
        {
            "prompt_id": "p0",
            "method": "e_bh_pcal",
            "split": "heldout",
            "template_id": 4,
            "behavior": "subject_verb_agreement",
        }
    )
    out = circuit_cache.output_row(
        row=row,
        args=args,
        feature_ids=[1, 2, 3],
        clean_metric=2.0,
        patch_metric=0.5,
        selected_patch_metric=0.75,
        target_token_id=10,
        counter_token_id=20,
        hook_name="blocks.20.hook_resid_post",
        sae_acts_hook="blocks.20.hook_resid_post.hook_sae_acts_post",
    )
    assert out["prompt_id"] == "p0"
    assert out["method"] == "e_bh_pcal"
    assert out["full_difference"] == pytest.approx(1.5)
    assert out["selected_difference"] == pytest.approx(1.25)
    assert out["n_selected_features"] == 3
    assert out["selected_feature_ids"] == "1;2;3"
