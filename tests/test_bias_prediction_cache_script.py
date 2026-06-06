from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace

import pandas as pd
import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import produce_bias_in_bios_prediction_cache as producer


def test_load_labels_from_file(tmp_path: Path) -> None:
    path = tmp_path / "labels.csv"
    pd.DataFrame({"label_id": [0, 1], "label_text": ["accountant", "architect"]}).to_csv(path, index=False)
    labels = producer.load_labels(path, pd.DataFrame(), target_col="target_label")
    assert labels["label_id"].tolist() == [0, 1]
    assert labels["label_text"].tolist() == ["accountant", "architect"]


def test_load_labels_falls_back_to_prompt_targets(tmp_path: Path) -> None:
    prompts = pd.DataFrame({"target_label": [2, 1, 2]})
    labels = producer.load_labels(tmp_path / "missing.csv", prompts, target_col="target_label")
    assert labels["label_id"].tolist() == ["1", "2"]
    assert labels["label_text"].tolist() == ["1", "2"]


def test_load_feature_sets_parses_method_csv_specs(tmp_path: Path) -> None:
    path = tmp_path / "features.csv"
    pd.DataFrame({"feature_id": [3, 3, 4]}).to_csv(path, index=False)
    loaded = producer.load_feature_sets([f"e_bh_pcal={path}"], feature_col="feature_id")
    assert loaded == [("e_bh_pcal", [3, 4])]


def test_load_feature_sets_rejects_bad_specs() -> None:
    with pytest.raises(SystemExit, match="METHOD=CSV"):
        producer.load_feature_sets(["bad-spec"], feature_col="feature_id")


def test_resolve_intervention_index_prompt_last() -> None:
    assert producer.resolve_intervention_index("prompt_last", seq_len=10, prompt_len=7) == 6
    assert producer.resolve_intervention_index("last", seq_len=10, prompt_len=7) == 9


def test_dry_run_metadata_records_default_methods(tmp_path: Path) -> None:
    args = SimpleNamespace(
        model_id="gemma-2-2b",
        sae_release="release",
        sae_id="sae",
        prompts=tmp_path / "prompts.csv",
        labels=tmp_path / "labels.csv",
        label_score="mean_logprob",
        intervention_pos="prompt_last",
        prepend_bos=False,
        use_error_term=True,
        dry_run=True,
    )
    prompts = pd.DataFrame({"example_id": ["a"], "prompt": ["x"], "target_label": ["0"], "protected_label": ["1"]})
    labels = pd.DataFrame({"label_id": ["0"], "label_text": ["nurse"]})
    metadata = producer.base_metadata(args, prompts, labels, [])
    assert metadata["methods"] == ["clean", "e_bh_pcal", "top_score"]
