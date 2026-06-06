from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import produce_sae_screen_scores as screen_scores


def minimal_args() -> argparse.Namespace:
    return argparse.Namespace(
        prompt_id_column="prompt_id",
        prompt_column="clean_prompt",
        patch_prompt_column="patch_prompt",
        target_column="target_token",
        counter_column="counter_token",
        top_k=3,
        dry_run_features=5,
        score_mode="metric_weighted_delta",
    )


def test_validate_prompts_accepts_required_columns() -> None:
    args = minimal_args()
    prompts = pd.DataFrame(
        {
            "prompt_id": ["p0"],
            "clean_prompt": ["The key"],
            "patch_prompt": ["The keys"],
            "target_token": [" is"],
            "counter_token": [" are"],
        }
    )
    screen_scores.validate_prompts(prompts, args)


def test_validate_prompts_rejects_missing_columns() -> None:
    args = minimal_args()
    prompts = pd.DataFrame({"prompt_id": ["p0"]})
    with pytest.raises(SystemExit, match="prompt file missing required columns"):
        screen_scores.validate_prompts(prompts, args)


def test_validate_prompts_allows_activation_delta_without_tokens() -> None:
    args = minimal_args()
    args.score_mode = "activation_delta"
    prompts = pd.DataFrame(
        {
            "prompt_id": ["p0"],
            "clean_prompt": ["Biography"],
            "patch_prompt": ["Biography patch"],
        }
    )
    screen_scores.validate_prompts(prompts, args)


def test_screen_accumulator_ranks_by_metric_weighted_delta() -> None:
    acc = screen_scores.ScreenAccumulator(np.asarray([0, 1, 2], dtype=np.int64))
    acc.update(clean_acts=np.asarray([1.0, 4.0, 2.0]), patch_acts=np.asarray([0.0, 1.0, 2.0]), metric_gap=2.0)
    frame = acc.to_frame(
        score_mode="metric_weighted_delta",
        sae_release="release",
        sae_id="layer_20/width_16k/canonical",
        hook_name="blocks.20.hook_resid_post",
        sae_acts_hook="blocks.20.hook_resid_post.hook_sae_acts_post",
        layer=20,
        ablation_type="resample",
    )
    assert frame["feature_id"].tolist() == [1, 0, 2]
    assert frame.loc[0, "screen_score"] == pytest.approx(6.0)
    assert frame.loc[2, "screen_score"] == pytest.approx(0.0)


def test_infer_layer_from_hook_or_sae_id() -> None:
    assert screen_scores.infer_layer("blocks.12.hook_resid_post", "layer_20/width_16k/canonical") == 12
    assert screen_scores.infer_layer(None, "layer_20/width_16k/canonical") == 20
    assert screen_scores.infer_layer("hook", "unknown") is None
