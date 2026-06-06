from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    args = parse_args()
    prompts = pd.read_csv(args.prompts)
    if args.split != "all" and "split" in prompts.columns:
        prompts = prompts[prompts["split"] == args.split].copy()
    feature_sets = load_feature_sets(args)
    frames = []
    eval_id = 0
    for method, feature_ids in feature_sets:
        frame = prompts.copy()
        frame.insert(0, "circuit_eval_id", [f"circuit_{eval_id + i:08d}" for i in range(len(frame))])
        frame["method"] = method
        frame["selected_feature_ids"] = ";".join(feature_ids)
        frame["n_selected_features"] = len(feature_ids)
        frame["eval_type"] = "joint_selected_circuit"
        frames.append(frame)
        eval_id += len(frame)
    manifest = pd.concat(frames, ignore_index=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    manifest.to_csv(args.output, index=False)
    print(f"wrote {len(manifest)} circuit eval rows to {safe_display_path(args.output)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--prompts",
        type=Path,
        default=ROOT / "data" / "subject_verb_agreement" / "prompts.csv",
    )
    parser.add_argument(
        "--selected-features",
        type=Path,
        action="append",
        default=[],
        help="Selected-feature CSV. Can be repeated; method is inferred from the file unless --method is set for one file.",
    )
    parser.add_argument(
        "--feature-set",
        action="append",
        default=[],
        metavar="METHOD=PATH",
        help="Named selected-feature CSV. Can be repeated, e.g. --feature-set e_bh_pcal=results/.../selected.csv.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "data" / "subject_verb_agreement" / "circuit_eval_manifest.csv",
    )
    parser.add_argument("--split", default="heldout", choices=["screen", "test", "heldout", "all"])
    parser.add_argument("--feature-column", default="feature_id")
    parser.add_argument("--method", default=None)
    return parser.parse_args()


def load_feature_sets(args: argparse.Namespace) -> list[tuple[str, list[str]]]:
    specs: list[tuple[str | None, Path]] = []
    for value in args.feature_set:
        if "=" not in value:
            raise SystemExit("--feature-set must have the form METHOD=PATH")
        method, path = value.split("=", 1)
        if not method.strip() or not path.strip():
            raise SystemExit("--feature-set must have non-empty METHOD and PATH")
        specs.append((method.strip(), Path(path)))
    for path in args.selected_features:
        specs.append((args.method, path))
    if not specs:
        raise SystemExit("provide --selected-features or --feature-set")

    out = []
    for explicit_method, path in specs:
        selected = pd.read_csv(path)
        feature_col = args.feature_column
        if feature_col not in selected.columns:
            raise SystemExit(f"selected feature file missing {feature_col}: {path}")
        feature_ids = selected[feature_col].dropna().astype(str).tolist()
        method = explicit_method or infer_method(selected, path)
        out.append((method, feature_ids))
    return out


def infer_method(selected: pd.DataFrame, path: Path) -> str:
    if "selection_method" in selected.columns and selected["selection_method"].notna().any():
        return str(selected["selection_method"].dropna().iloc[0])
    stem = path.stem
    return stem.removeprefix("selected_features_")


def safe_display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return path.name


if __name__ == "__main__":
    main()
