from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_bias_in_bios_pair_prompts as pairs


def test_build_pairs_matches_same_profession_opposite_gender() -> None:
    data = pd.DataFrame(
        {
            "example_id": ["a", "b", "c"],
            "split": ["train", "train", "train"],
            "text": ["She is a professor.", "He is a professor.", "She is a nurse."],
            "profession": [21, 21, 13],
            "gender": [1, 0, 1],
            "group_id": ["21::1", "21::0", "13::1"],
        }
    )
    out = pairs.build_pairs(data)
    assert out.shape[0] == 2
    assert set(out["target_label"]) == {21}
    assert set(out["protected_label"].astype(str)) == {"0", "1"}
    assert all(out["clean_example_id"] != out["patch_example_id"])


def test_assign_pair_splits_maps_dataset_splits() -> None:
    frame = pd.DataFrame({"source_split": ["train", "dev", "test", "dry_run"]})
    assert pairs.assign_pair_splits(frame, "source") == ["screen", "test", "heldout", "screen"]
    assert pairs.assign_pair_splits(frame, "screen_only") == ["screen", "screen", "screen", "screen"]


def test_format_prompt_contains_biography_and_question() -> None:
    prompt = pairs.format_prompt("She is a professor.")
    assert "Biography:" in prompt
    assert "Question:" in prompt
    assert "She is a professor." in prompt
