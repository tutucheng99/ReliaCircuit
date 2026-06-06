import numpy as np
import pandas as pd

from reliacircuit.cache_analysis import (
    analyze_ablation_cache,
    analyze_circuit_cache,
    analyze_prompt_tracking_cache,
    selected_feature_list,
)


def test_ablation_cache_analysis_selects_strong_feature():
    rng = np.random.default_rng(3)
    rows = []
    for feature_id, mean in [(0, 1.0), (1, 0.0)]:
        for i in range(80):
            diff = rng.normal(mean, 0.2)
            rows.append(
                {
                    "feature_id": feature_id,
                    "prompt_id": i,
                    "split": "test",
                    "cluster_id": i // 4,
                    "difference": diff,
                }
            )
    cache = pd.DataFrame(rows)
    truth = pd.DataFrame(
        {
            "feature_id": [0, 1],
            "is_active": [True, False],
            "true_tau": [1.0, 0.0],
        }
    )
    feature_stats, summary = analyze_ablation_cache(
        cache,
        q=0.1,
        n_bootstrap=19,
        seed=5,
        ground_truth=truth,
    )
    assert feature_stats.shape[0] == 2
    selected = feature_stats.set_index("feature_id")["selected_bh"].to_dict()
    assert selected[0] is True
    assert selected[1] is False
    assert "fdp" in summary.columns
    selected_features = selected_feature_list(feature_stats, method="bh")
    assert selected_features["feature_id"].tolist() == [0]


def test_circuit_cache_analysis_reports_completeness():
    cache = pd.DataFrame(
        {
            "prompt_id": [f"p{i}" for i in range(5)] * 2,
            "method": ["good"] * 5 + ["bad"] * 5,
            "full_difference": [1, 2, 3, 4, 5] * 2,
            "selected_difference": [1, 2, 3, 4, 5] + [0, 0, 0, 0, 0],
        }
    )
    summary = analyze_circuit_cache(cache).set_index("method")
    assert summary.loc["good", "completeness_r2"] == 1.0
    assert summary.loc["good", "centered_r2"] == 1.0
    assert summary.loc["bad", "completeness_r2"] < summary.loc["good", "completeness_r2"]
    assert summary.loc["bad", "centered_r2"] < 0.0


def test_prompt_tracking_cache_analysis_selects_covarying_feature():
    rows = []
    prompt_effects = []
    for i, full in enumerate([-2.0, -1.0, 1.0, 2.0] * 20):
        prompt_id = f"p{i}"
        prompt_effects.append({"prompt_id": prompt_id, "full_difference": full})
        rows.append({"prompt_id": prompt_id, "feature_id": 0, "split": "test", "difference": full})
        rows.append({"prompt_id": prompt_id, "feature_id": 1, "split": "test", "difference": 0.25})

    feature_stats, summary = analyze_prompt_tracking_cache(
        pd.DataFrame(rows),
        pd.DataFrame(prompt_effects),
        q=0.1,
        n_bootstrap=19,
        seed=5,
    )

    selected = feature_stats.set_index("feature_id")["selected_bh"].to_dict()
    assert selected[0] is True
    assert selected[1] is False
    assert feature_stats.set_index("feature_id").loc[0, "tracking_corr"] > 0.99
    assert "discoveries" in summary.columns
