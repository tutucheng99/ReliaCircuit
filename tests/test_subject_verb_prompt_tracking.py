from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import diagnose_subject_verb_prompt_tracking as tracking


def test_infer_full_prompt_effects_uses_reversed_patch_metric() -> None:
    prompts = pd.DataFrame(
        {
            "prompt_id": ["p0", "p1"],
            "clean_prompt": ["The key", "The keys"],
            "patch_prompt": ["The keys", "The key"],
            "split": ["test", "test"],
        }
    )
    clean = pd.DataFrame(
        {
            "prompt_id": ["p0", "p1"],
            "clean_prompt": ["The key", "The keys"],
            "metric": [2.0, 3.0],
        }
    )

    out = tracking.infer_full_prompt_effects(prompts, clean).set_index("prompt_id")

    assert out.loc["p0", "patch_metric_inferred"] == pytest.approx(-3.0)
    assert out.loc["p0", "full_difference_inferred"] == pytest.approx(5.0)
    assert out.loc["p1", "patch_metric_inferred"] == pytest.approx(-2.0)
    assert out.loc["p1", "full_difference_inferred"] == pytest.approx(5.0)


def test_additive_tracking_summary_reports_corr_for_selected_methods() -> None:
    exact = pd.DataFrame(
        {
            "prompt_id": ["p0", "p1", "p0", "p1"],
            "feature_id": [1, 1, 2, 2],
            "difference": [1.0, 2.0, 0.0, 0.0],
        }
    )
    prompt_effects = pd.DataFrame(
        {
            "prompt_id": ["p0", "p1"],
            "split": ["test", "test"],
            "full_difference_inferred": [1.0, 2.0],
        }
    )
    feature_stats = pd.DataFrame(
        {
            "feature_id": [1, 2],
            "selected_e_bh_pcal": [True, False],
        }
    )
    screen = pd.DataFrame({"feature_id": [1, 2], "screen_score": [10.0, 1.0]})

    summary = tracking.additive_tracking_summary(
        exact_cache=exact,
        prompt_effects=prompt_effects,
        feature_stats=feature_stats,
        screen_scores=screen,
    ).set_index("method")

    assert summary.loc["e_bh_pcal", "n_features"] == 1
    assert summary.loc["e_bh_pcal", "additive_selected_full_corr"] == pytest.approx(1.0)
