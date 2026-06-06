from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import summarize_environment as env


def test_parse_requirement_line_handles_specs_and_comments() -> None:
    assert env.parse_requirement_line("numpy>=1.26") == ("numpy", "numpy>=1.26")
    assert env.parse_requirement_line("huggingface-hub>=0.25") == ("huggingface-hub", "huggingface-hub>=0.25")
    assert env.parse_requirement_line("# comment") is None
    assert env.parse_requirement_line("") is None


def test_collect_requirements_merges_cpu_and_gpu_specs(tmp_path: Path) -> None:
    cpu = tmp_path / "requirements-cpu.txt"
    gpu = tmp_path / "requirements-gpu.txt"
    cpu.write_text("numpy>=1\npytest>=8\n", encoding="utf-8")
    gpu.write_text("numpy>=1\ntorch>=2\n", encoding="utf-8")
    requirements = env.collect_requirements([cpu, gpu])
    assert requirements["numpy"] == {"cpu_spec": "numpy>=1", "gpu_spec": "numpy>=1"}
    assert requirements["pytest"] == {"cpu_spec": "pytest>=8"}
    assert requirements["torch"] == {"gpu_spec": "torch>=2"}
