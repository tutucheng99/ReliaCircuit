from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd
import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import produce_sae_ablation_cache as sae_cache


def minimal_args() -> argparse.Namespace:
    return argparse.Namespace(
        prompt_id_column="prompt_id",
        prompt_column="clean_prompt",
        patch_prompt_column="patch_prompt",
        target_column="target_token",
        counter_column="counter_token",
        target_label_column="target_label",
        feature_id_column="feature_id",
        metric_mode="token_logit_diff",
        label_score="mean_logprob",
        hook_name=None,
        ablation_type="resample",
        include_text=False,
        batch_size=32,
        cache_dir=None,
        row_offset=0,
        max_rows=None,
        resume=False,
    )


def test_validate_manifest_accepts_required_columns() -> None:
    args = minimal_args()
    manifest = pd.DataFrame(
        {
            "prompt_id": ["p0"],
            "clean_prompt": ["The key"],
            "patch_prompt": ["The keys"],
            "target_token": [" is"],
            "counter_token": [" are"],
            "feature_id": [7],
        }
    )
    sae_cache.validate_manifest(manifest, args)


def test_validate_manifest_rejects_missing_columns() -> None:
    args = minimal_args()
    manifest = pd.DataFrame({"prompt_id": ["p0"], "feature_id": [7]})
    with pytest.raises(SystemExit, match="manifest missing required columns"):
        sae_cache.validate_manifest(manifest, args)


def test_validate_manifest_accepts_label_logprob_mode_without_token_columns() -> None:
    args = minimal_args()
    args.metric_mode = "label_logprob"
    manifest = pd.DataFrame(
        {
            "prompt_id": ["p0"],
            "clean_prompt": ["Biography:\nText\n\nQuestion:"],
            "patch_prompt": ["Biography:\nOther\n\nQuestion:"],
            "target_label": [2],
            "feature_id": [7],
        }
    )

    sae_cache.validate_manifest(manifest, args)


def test_resolve_seq_index() -> None:
    assert sae_cache.resolve_seq_index("last", 5) == 4
    assert sae_cache.resolve_seq_index("-1", 5) == 4
    assert sae_cache.resolve_seq_index("2", 5) == 2
    with pytest.raises(IndexError):
        sae_cache.resolve_seq_index("5", 5)


def test_output_row_matches_cache_schema() -> None:
    args = minimal_args()
    row = pd.Series(
        {
            "split": "test",
            "template_id": 3,
            "layer": 20,
            "hook_name": "blocks.20.hook_resid_post",
            "ablation_type": "resample",
            "behavior": "subject_verb_agreement",
            "sweep_id": 42,
        }
    )
    out = sae_cache.output_row(
        row=row,
        args=args,
        prompt_id="p0",
        feature_id=11,
        clean_metric=1.5,
        ablated_metric=0.25,
        target_token_id=10,
        counter_token_id=20,
        sae_hook_name="blocks.20.hook_resid_post.hook_sae_acts_post",
        clean_logits_meta={"target_logit": 2.0, "counter_logit": 0.5},
    )
    assert out["feature_id"] == 11
    assert out["difference"] == pytest.approx(1.25)
    assert out["split"] == "test"
    assert out["cluster_id"] == 3
    assert out["sweep_id"] == 42
    assert out["sae_acts_hook"] == "blocks.20.hook_resid_post.hook_sae_acts_post"


def test_make_dry_run_cache_has_exact_cache_columns() -> None:
    args = minimal_args()
    manifest = pd.DataFrame(
        {
            "prompt_id": ["p0"],
            "clean_prompt": ["The key"],
            "patch_prompt": ["The keys"],
            "target_token": [" is"],
            "counter_token": [" are"],
            "feature_id": [2],
            "split": ["test"],
        }
    )
    cache = sae_cache.make_dry_run_cache(manifest, args)
    assert {"feature_id", "clean_metric", "ablated_metric", "difference"}.issubset(cache.columns)
    assert cache.loc[0, "difference"] == pytest.approx(
        cache.loc[0, "clean_metric"] - cache.loc[0, "ablated_metric"]
    )


def test_make_dry_run_cache_records_label_metric_columns() -> None:
    args = minimal_args()
    args.metric_mode = "label_logprob"
    manifest = pd.DataFrame(
        {
            "prompt_id": ["p0"],
            "clean_prompt": ["Biography:\nText\n\nQuestion:"],
            "patch_prompt": ["Biography:\nOther\n\nQuestion:"],
            "target_label": [2],
            "protected_label": [1],
            "feature_id": [2],
            "split": ["test"],
        }
    )

    cache = sae_cache.make_dry_run_cache(manifest, args)

    assert cache.loc[0, "metric_mode"] == "label_logprob"
    assert cache.loc[0, "target_label"] == 2
    assert cache.loc[0, "label_score"] == "mean_logprob"


def test_build_hooked_model_kwargs_does_not_duplicate_hf_token(monkeypatch) -> None:
    monkeypatch.setenv("HF_TOKEN", "hf_secret")
    args = minimal_args()

    kwargs = sae_cache.build_hooked_model_kwargs(args, device="cuda", dtype="bf16")

    assert kwargs == {"device": "cuda", "dtype": "bf16"}
    assert "token" not in kwargs


def test_slice_manifest_applies_row_offset_before_max_rows() -> None:
    args = minimal_args()
    args.row_offset = 2
    args.max_rows = 3
    manifest = pd.DataFrame({"prompt_id": range(10), "feature_id": range(10)})

    sliced = sae_cache.slice_manifest(manifest, args)

    assert sliced["prompt_id"].tolist() == [2, 3, 4]


def test_filter_completed_rows_uses_sweep_id_when_available(tmp_path: Path) -> None:
    args = minimal_args()
    manifest = pd.DataFrame(
        {
            "sweep_id": [10, 11, 12],
            "prompt_id": ["p0", "p0", "p1"],
            "feature_id": [1, 2, 1],
            "ablation_type": ["resample", "resample", "resample"],
        }
    )
    output = tmp_path / "cache.csv"
    pd.DataFrame({"sweep_id": [10], "prompt_id": ["p0"], "feature_id": [1]}).to_csv(output, index=False)

    filtered, skipped = sae_cache.filter_completed_rows(manifest, output, args)

    assert skipped == 1
    assert filtered["sweep_id"].tolist() == [11, 12]


def test_append_rows_writes_header_once(tmp_path: Path) -> None:
    output = tmp_path / "cache.csv"

    sae_cache.append_rows(output, [{"prompt_id": "p0", "feature_id": 1}])
    sae_cache.append_rows(output, [{"prompt_id": "p1", "feature_id": 2}])

    lines = output.read_text(encoding="utf-8").strip().splitlines()
    assert lines[0] == "prompt_id,feature_id"
    assert len(lines) == 3
