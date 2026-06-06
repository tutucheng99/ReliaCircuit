from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    args = parse_args()
    data = pd.read_csv(args.input)
    pairs = build_pairs(data, max_pairs_per_profession=args.max_pairs_per_profession)
    if args.max_pairs is not None:
        pairs = pairs.head(args.max_pairs).copy()
    pairs["split"] = assign_pair_splits(pairs, args.split_policy)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    pairs.to_csv(args.output, index=False)
    print(f"wrote {len(pairs)} BiasInBios paired prompts to {safe_display_path(args.output)}")
    if len(pairs) > 0:
        print(pairs.groupby("split").size().to_string())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build BiasInBios same-profession opposite-gender prompt pairs.")
    parser.add_argument("--input", type=Path, default=ROOT / "data" / "bias_in_bios" / "bias_in_bios_normalized.csv")
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "data" / "bias_in_bios" / "paired_prompts.csv",
    )
    parser.add_argument("--max-pairs", type=int, default=None)
    parser.add_argument("--max-pairs-per-profession", type=int, default=None)
    parser.add_argument("--split-policy", choices=["source", "screen_only"], default="source")
    return parser.parse_args()


def build_pairs(data: pd.DataFrame, max_pairs_per_profession: int | None = None) -> pd.DataFrame:
    required = {"example_id", "split", "text", "profession", "gender", "group_id"}
    missing = required - set(data.columns)
    if missing:
        raise ValueError(f"normalized data missing columns: {sorted(missing)}")
    rows = []
    pair_idx = 0
    for profession, group in data.groupby("profession", sort=True):
        gender_values = sorted(group["gender"].dropna().astype(str).unique().tolist())
        if len(gender_values) < 2:
            continue
        left = group[group["gender"].astype(str) == gender_values[0]].reset_index(drop=True)
        right = group[group["gender"].astype(str) == gender_values[1]].reset_index(drop=True)
        n_pairs = min(len(left), len(right))
        if max_pairs_per_profession is not None:
            n_pairs = min(n_pairs, max_pairs_per_profession)
        for i in range(n_pairs):
            pair_idx = append_pair_rows(rows, pair_idx, profession, left.iloc[i], right.iloc[i])
    return pd.DataFrame(rows)


def append_pair_rows(rows: list[dict[str, object]], pair_idx: int, profession: object, a: pd.Series, b: pd.Series) -> int:
    for clean, patch in [(a, b), (b, a)]:
        rows.append(
            {
                "prompt_id": f"bib_pair_{pair_idx:07d}",
                "clean_example_id": clean["example_id"],
                "patch_example_id": patch["example_id"],
                "source_split": clean["split"],
                "clean_prompt": format_prompt(str(clean["text"])),
                "patch_prompt": format_prompt(str(patch["text"])),
                "target_label": profession,
                "protected_label": clean["gender"],
                "patch_protected_label": patch["gender"],
                "group_id": clean["group_id"],
                "patch_group_id": patch["group_id"],
                "behavior": "bias_in_bios_gender_pair_activation_screen",
            }
        )
        pair_idx += 1
    return pair_idx


def assign_pair_splits(pairs: pd.DataFrame, policy: str) -> list[str]:
    if pairs.empty:
        return []
    if policy == "screen_only":
        return ["screen"] * len(pairs)
    mapped = []
    for split in pairs["source_split"].astype(str):
        if split == "train":
            mapped.append("screen")
        elif split in {"dev", "validation"}:
            mapped.append("test")
        elif split == "test":
            mapped.append("heldout")
        else:
            mapped.append("screen")
    return mapped


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
        return str(path)


if __name__ == "__main__":
    main()
