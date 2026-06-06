from __future__ import annotations

import re
import uuid
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def tmp_path(request: pytest.FixtureRequest) -> Path:
    """Local tmp_path replacement for sync-folders that block pytest temp cleanup."""

    safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", request.node.name)[:80]
    path = ROOT / ".test_tmp" / f"{safe_name}_{uuid.uuid4().hex[:8]}"
    path.mkdir(parents=True, exist_ok=False)
    return path
