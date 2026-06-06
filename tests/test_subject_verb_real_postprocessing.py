from __future__ import annotations

import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import postprocess_subject_verb_real_run as post


def test_public_postprocess_stub_points_to_cache_analysis_scripts() -> None:
    with pytest.raises(SystemExit, match="public analysis scripts"):
        post.main()
