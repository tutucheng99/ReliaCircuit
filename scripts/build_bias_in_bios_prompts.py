from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    args = parse_args()
    data = pd.read_csv(args.input)
    required = {"example_id", "split", "text", "profession", "gender", "group_id"}
    missing = required - set(data.columns)
    if missing:
        raise SystemExit(f"normalized data missing columns: {sorted(missing)}")
    if args.max_rows is not None:
        data = data.groupby("split", group_keys=False).head(args.max_rows)
    prompts = data.copy()
    prompts["prompt"] = prompts["text"].map(format_prompt)
    prompts["behavior"] = "bias_in_bios_profession_classification"
    prompts["target_label"] = prompts["profession"]
    prompts["protected_label"] = prompts["gender"]
    keep = [
        "example_id",
        "split",
        "prompt",
        "target_label",
        "protected_label",
        "group_id",
        "behavior",
    ]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    prompts.loc[:, keep].to_csv(args.output, index=False)
    print(f"wrote {len(prompts)} BiasInBios prompts to {safe_display_path(args.output)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        type=Path,
        default=ROOT / "data" / "bias_in_bios" / "bias_in_bios_normalized.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "data" / "bias_in_bios" / "prompts.csv",
    )
    parser.add_argument("--max-rows", type=int, default=None)
    return parser.parse_args()


def format_prompt(text: str) -> str:
    return (
        "Biography:\n"
        f"{text}\n\n"
        "Question: What is the person's profession? Answer with the occupation label only."
    )


def safe_display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return path.name


if __name__ == "__main__":
    main()
