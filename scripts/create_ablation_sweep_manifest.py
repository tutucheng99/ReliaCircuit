from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    args = parse_args()
    prompts = pd.read_csv(args.prompts)
    features = pd.read_csv(args.features)
    if args.split != "all" and "split" in prompts.columns:
        prompts = prompts[prompts["split"] == args.split].copy()
    if args.max_prompts is not None:
        prompts = prompts.head(args.max_prompts).copy()
    if args.max_features is not None:
        features = features.head(args.max_features).copy()
    manifest = prompts.merge(features, how="cross")
    manifest.insert(0, "sweep_id", [f"sweep_{i:08d}" for i in range(len(manifest))])
    manifest["resample_source_policy"] = args.resample_source_policy
    args.output.parent.mkdir(parents=True, exist_ok=True)
    manifest.to_csv(args.output, index=False)
    print(f"wrote {len(manifest)} sweep rows to {safe_display_path(args.output)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prompts",
        type=Path,
        default=ROOT / "data" / "subject_verb_agreement" / "prompts.csv",
    )
    parser.add_argument("--features", type=Path, default=ROOT / "data" / "gemma_scope_smoke_features.csv")
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "data" / "subject_verb_agreement" / "ablation_manifest_smoke.csv",
    )
    parser.add_argument("--split", default="test", choices=["screen", "test", "heldout", "all"])
    parser.add_argument("--max-prompts", type=int, default=None)
    parser.add_argument("--max-features", type=int, default=None)
    parser.add_argument("--resample-source-policy", default="same_split_random_patch_prompt")
    return parser.parse_args()


def safe_display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return path.name


if __name__ == "__main__":
    main()
