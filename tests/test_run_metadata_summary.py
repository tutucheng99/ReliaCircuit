from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import summarize_run_metadata as summarize


def test_summarize_public_metadata_has_paths() -> None:
    frame = summarize.summarize(ROOT)
    assert "path" in frame.columns
    assert frame.shape[0] >= 4
