from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_subject_verb_prompts as prompts


def test_stratified_pair_split_covers_every_template_and_keeps_pairs_together() -> None:
    df = pd.DataFrame(prompts.build_rows())
    df["split"] = prompts.assign_splits(df, screen_fraction=0.4, test_fraction=0.4, seed=7)

    coverage = pd.crosstab(df["template_id"], df["split"])
    assert set(coverage.columns) == {"heldout", "screen", "test"}
    assert (coverage > 0).all().all()

    pair_split_counts = df.groupby("pair_id")["split"].nunique()
    assert pair_split_counts.max() == 1
    assert {"pair_id", "cluster_id", "head_id", "attractor_id"}.issubset(df.columns)


def test_contiguous_split_preserves_legacy_counts() -> None:
    df = pd.DataFrame(prompts.build_rows())
    split = prompts.assign_splits(df, screen_fraction=0.4, test_fraction=0.4, strategy="contiguous")

    counts = pd.Series(split).value_counts().to_dict()
    assert counts == {"screen": 307, "test": 307, "heldout": 154}
