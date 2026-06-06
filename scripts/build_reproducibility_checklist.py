"""Build a compact public reproducibility checklist."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def build_checklist_rows() -> list[dict[str, str]]:
    return [
        {
            "item": "CPU install",
            "status": "supported",
            "evidence": "requirements-cpu.txt, pyproject.toml",
        },
        {
            "item": "Synthetic benchmark reproduction",
            "status": "supported",
            "evidence": "scripts/run_synthetic_gate_b.py, scripts/run_synthetic_frontier.py",
        },
        {
            "item": "Cached real-model analysis",
            "status": "supported",
            "evidence": "results/subject_verb_agreement_balanced*/exact_ablation_cache.csv",
        },
        {
            "item": "GPU cache generation recipe",
            "status": "documented",
            "evidence": "docs/gpu_cache_generation.md, runpod_job.sh",
        },
        {
            "item": "Anonymous public release scan",
            "status": "supported",
            "evidence": "scripts/verify_artifacts.py",
        },
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=ROOT / "results" / "paper_assets")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    frame = pd.DataFrame(build_checklist_rows())
    frame.to_csv(args.output_dir / "reproducibility_checklist.csv", index=False)
    (args.output_dir / "reproducibility_checklist.md").write_text(
        "# Public Reproducibility Checklist\n\n" + frame.to_markdown(index=False) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
