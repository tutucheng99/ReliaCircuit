from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


SINGULAR_HEADS = [
    ("key", "keys"),
    ("report", "reports"),
    ("doctor", "doctors"),
    ("teacher", "teachers"),
    ("author", "authors"),
    ("manager", "managers"),
    ("student", "students"),
    ("lawyer", "lawyers"),
    ("engineer", "engineers"),
    ("artist", "artists"),
    ("scientist", "scientists"),
    ("analyst", "analysts"),
]

ATTRACTORS = [
    ("cabinet", "cabinets"),
    ("committee", "committees"),
    ("company", "companies"),
    ("school", "schools"),
    ("office", "offices"),
    ("lab", "labs"),
    ("department", "departments"),
    ("museum", "museums"),
]

TEMPLATES = [
    "The {head} near the {attr}",
    "The {head} beside the {attr}",
    "The {head} behind the {attr}",
    "The {head} from the {attr}",
]


def main() -> None:
    args = parse_args()
    rows = build_rows()
    df = pd.DataFrame(rows)
    df["split"] = assign_splits(
        df,
        screen_fraction=args.screen_fraction,
        test_fraction=args.test_fraction,
        strategy=args.split_strategy,
        seed=args.split_seed,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.output, index=False)
    print(f"wrote {len(df)} prompts to {safe_display_path(args.output)}")
    print(df.groupby(["split", "template_id", "subject_number", "attractor_number"]).size().to_string())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "data" / "subject_verb_agreement" / "prompts.csv",
    )
    parser.add_argument("--screen-fraction", type=float, default=0.4)
    parser.add_argument("--test-fraction", type=float, default=0.4)
    parser.add_argument(
        "--split-strategy",
        choices=["stratified_pair", "contiguous"],
        default="stratified_pair",
        help="stratified_pair assigns both number variants for each lexical pair to the same split within every template.",
    )
    parser.add_argument("--split-seed", type=int, default=0)
    return parser.parse_args()


def build_rows() -> list[dict[str, object]]:
    rows = []
    prompt_id = 0
    for template_id, template in enumerate(TEMPLATES):
        for head_id, (head_sg, head_pl) in enumerate(SINGULAR_HEADS):
            for attr_id, (attr_sg, attr_pl) in enumerate(ATTRACTORS):
                pair_id = f"tpl{template_id:02d}_head{head_id:02d}_attr{attr_id:02d}"
                variants = [
                    ("singular", "plural", head_sg, attr_pl, " is", " are"),
                    ("plural", "singular", head_pl, attr_sg, " are", " is"),
                ]
                for subject_number, attractor_number, head, attr, target, counter in variants:
                    clean_prompt = template.format(head=head, attr=attr)
                    patch_head = head_pl if subject_number == "singular" else head_sg
                    patch_attr = attr_sg if attractor_number == "plural" else attr_pl
                    patch_prompt = template.format(head=patch_head, attr=patch_attr)
                    rows.append(
                        {
                            "prompt_id": f"sva_{prompt_id:04d}",
                            "pair_id": pair_id,
                            "cluster_id": pair_id,
                            "template_id": template_id,
                            "head_id": head_id,
                            "attractor_id": attr_id,
                            "clean_prompt": clean_prompt,
                            "patch_prompt": patch_prompt,
                            "target_token": target,
                            "counter_token": counter,
                            "subject_number": subject_number,
                            "attractor_number": attractor_number,
                            "behavior": "subject_verb_agreement",
                        }
                    )
                    prompt_id += 1
    return rows


def assign_splits(
    df: pd.DataFrame,
    screen_fraction: float,
    test_fraction: float,
    strategy: str = "stratified_pair",
    seed: int = 0,
) -> list[str]:
    if screen_fraction <= 0.0 or test_fraction <= 0.0 or screen_fraction + test_fraction >= 1.0:
        raise ValueError("screen/test fractions must be positive and leave a heldout split")
    if strategy == "contiguous":
        return assign_contiguous_splits(len(df), screen_fraction, test_fraction)
    if strategy != "stratified_pair":
        raise ValueError(f"unknown split strategy: {strategy}")
    required = {"template_id", "pair_id"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"cannot stratify without columns: {sorted(missing)}")

    import numpy as np

    split_by_pair: dict[str, str] = {}
    generator = np.random.default_rng(seed)
    for _, group in df[["template_id", "pair_id"]].drop_duplicates().groupby("template_id", sort=True):
        pair_ids = group["pair_id"].astype(str).to_numpy()
        generator.shuffle(pair_ids)
        labels = assign_contiguous_splits(len(pair_ids), screen_fraction, test_fraction)
        split_by_pair.update({pair_id: label for pair_id, label in zip(pair_ids, labels, strict=True)})
    return [split_by_pair[str(pair_id)] for pair_id in df["pair_id"]]


def assign_contiguous_splits(n: int, screen_fraction: float, test_fraction: float) -> list[str]:
    n_screen = int(round(n * screen_fraction))
    n_test = int(round(n * test_fraction))
    split = ["heldout"] * n
    for i in range(n_screen):
        split[i] = "screen"
    for i in range(n_screen, n_screen + n_test):
        split[i] = "test"
    return split


def safe_display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return path.name


if __name__ == "__main__":
    main()
