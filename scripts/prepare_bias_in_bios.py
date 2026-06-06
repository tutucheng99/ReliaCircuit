from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    args = parse_args()
    config = load_json(args.config)
    if args.max_rows is not None:
        config["max_rows_per_split"] = args.max_rows
    if args.splits is not None:
        config["splits"] = args.splits
    output_dir = resolve_output_dir(args.output_dir or Path(config["output_dir"]))
    config["output_dir"] = safe_display_path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    frames = []
    if args.input_csv:
        frame = normalize_frame(pd.read_csv(args.input_csv), config, split=args.split_name)
        frames.append(frame)
    elif args.dry_run:
        frame = make_dry_run_frame()
        frames.append(normalize_frame(frame, config, split="dry_run"))
    else:
        frames.extend(load_hf_splits(config, loader=args.loader))

    data = pd.concat(frames, ignore_index=True)
    data = add_group_columns(data)
    data.to_csv(output_dir / "bias_in_bios_normalized.csv", index=False)
    write_split_files(data, output_dir)
    summary = summarize(data, config)
    summary.to_csv(output_dir / "summary.csv", index=False)
    (output_dir / "metadata.json").write_text(json.dumps(metadata(config, data), indent=2), encoding="utf-8")
    print(f"wrote {len(data)} normalized rows to {safe_display_path(output_dir)}")
    print(summary.to_string(index=False))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=ROOT / "configs" / "bias_in_bios.json")
    parser.add_argument("--input-csv", type=Path, default=None)
    parser.add_argument("--split-name", default="custom")
    parser.add_argument(
        "--splits",
        nargs="+",
        default=None,
        help="Override HuggingFace splits from config, e.g. --splits train test.",
    )
    parser.add_argument("--max-rows", type=int, default=None)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=None,
        help="Directory for normalized CSVs. Relative paths are resolved from the artifact root.",
    )
    parser.add_argument(
        "--loader",
        choices=["auto", "datasets", "viewer", "parquet"],
        default="auto",
        help="Online loader for HuggingFace data. viewer is intended for --max-rows probes.",
    )
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_hf_splits(config: dict, loader: str = "auto") -> list[pd.DataFrame]:
    if loader == "datasets":
        return load_hf_splits_datasets(config)
    if loader == "viewer":
        return load_hf_splits_viewer(config)
    if loader == "parquet":
        return load_hf_splits_parquet(config)
    try:
        return load_hf_splits_datasets(config)
    except Exception as exc:
        if config.get("max_rows_per_split") is not None:
            print(f"datasets loader failed ({exc.__class__.__name__}); falling back to viewer API")
            return load_hf_splits_viewer(config)
        print(f"datasets loader failed ({exc.__class__.__name__}); falling back to parquet files")
        return load_hf_splits_parquet(config)


def load_hf_splits_datasets(config: dict) -> list[pd.DataFrame]:
    from datasets import load_dataset

    frames = []
    for split in config["splits"]:
        ds = load_dataset(config["dataset_name"], split=split)
        frame = ds.to_pandas()
        max_rows = config.get("max_rows_per_split")
        if max_rows is not None:
            frame = frame.head(int(max_rows))
        frames.append(normalize_frame(frame, config, split=split))
    return frames


def load_hf_splits_viewer(config: dict) -> list[pd.DataFrame]:
    max_rows = config.get("max_rows_per_split")
    if max_rows is None:
        raise ValueError("viewer loader requires --max-rows to avoid paginating the full dataset")
    frames = []
    for split in config["splits"]:
        frame = load_viewer_rows(
            dataset_name=config["dataset_name"],
            split=split,
            max_rows=int(max_rows),
            dataset_config=config.get("hf_config", "default"),
        )
        frames.append(normalize_frame(frame, config, split=split))
    return frames


def load_viewer_rows(dataset_name: str, split: str, max_rows: int, dataset_config: str) -> pd.DataFrame:
    rows = []
    offset = 0
    while len(rows) < max_rows:
        length = min(100, max_rows - len(rows))
        query = urlencode(
            {
                "dataset": dataset_name,
                "config": dataset_config,
                "split": split,
                "offset": offset,
                "length": length,
            }
        )
        with urlopen(f"https://datasets-server.huggingface.co/rows?{query}", timeout=60) as response:
            payload = json.load(response)
        batch = [item["row"] for item in payload.get("rows", [])]
        if not batch:
            break
        rows.extend(batch)
        offset += len(batch)
    return pd.DataFrame(rows)


def load_hf_splits_parquet(config: dict) -> list[pd.DataFrame]:
    parquet_files = discover_parquet_files(config["dataset_name"])
    frames = []
    for split in config["splits"]:
        split_paths = parquet_files.get(split, [])
        if not split_paths:
            raise ValueError(f"no parquet files found for split {split!r}")
        pieces = [pd.read_parquet(hf_resolve_url(config["dataset_name"], rel_path)) for rel_path in split_paths]
        frame = pd.concat(pieces, ignore_index=True)
        max_rows = config.get("max_rows_per_split")
        if max_rows is not None:
            frame = frame.head(int(max_rows))
        frames.append(normalize_frame(frame, config, split=split))
    return frames


def discover_parquet_files(dataset_name: str) -> dict[str, list[str]]:
    with urlopen(f"https://huggingface.co/api/datasets/{dataset_name}", timeout=60) as response:
        payload = json.load(response)
    by_split: dict[str, list[str]] = {}
    for item in payload.get("siblings", []):
        filename = item.get("rfilename", "")
        if not filename.startswith("data/") or not filename.endswith(".parquet"):
            continue
        split = Path(filename).name.split("-", maxsplit=1)[0]
        by_split.setdefault(split, []).append(filename)
    return {split: sorted(paths) for split, paths in by_split.items()}


def hf_resolve_url(dataset_name: str, rel_path: str) -> str:
    return f"https://huggingface.co/datasets/{dataset_name}/resolve/main/{rel_path}"


def normalize_frame(frame: pd.DataFrame, config: dict, split: str) -> pd.DataFrame:
    text_col = config["text_column"]
    profession_col = config["profession_column"]
    gender_col = config["gender_column"]
    missing = {text_col, profession_col, gender_col} - set(frame.columns)
    if missing:
        raise ValueError(f"input data missing required columns: {sorted(missing)}")
    out = pd.DataFrame(
        {
            "example_id": [f"{split}_{i:07d}" for i in range(len(frame))],
            "split": split,
            "text": frame[text_col].astype(str),
            "profession": frame[profession_col],
            "gender": frame[gender_col],
        }
    )
    out["text_len_chars"] = out["text"].str.len()
    return out


def add_group_columns(data: pd.DataFrame) -> pd.DataFrame:
    out = data.copy()
    out["profession"] = out["profession"].astype(str)
    out["gender"] = out["gender"].astype(str)
    out["group_id"] = out["profession"] + "::" + out["gender"]
    return out


def write_split_files(data: pd.DataFrame, output_dir: Path) -> None:
    for split, group in data.groupby("split", sort=True):
        group.to_csv(output_dir / f"{split}.csv", index=False)


def summarize(data: pd.DataFrame, config: dict) -> pd.DataFrame:
    rows = []
    for split, group in data.groupby("split", sort=True):
        rows.append(
            {
                "split": split,
                "rows": int(group.shape[0]),
                "professions": int(group["profession"].nunique()),
                "genders": int(group["gender"].nunique()),
                "groups": int(group["group_id"].nunique()),
                "mean_text_len_chars": float(group["text_len_chars"].mean()),
            }
        )
    rows.append(
        {
            "split": "all",
            "rows": int(data.shape[0]),
            "professions": int(data["profession"].nunique()),
            "genders": int(data["gender"].nunique()),
            "groups": int(data["group_id"].nunique()),
            "mean_text_len_chars": float(data["text_len_chars"].mean()),
        }
    )
    return pd.DataFrame(rows)


def metadata(config: dict, data: pd.DataFrame) -> dict:
    return {
        "dataset_name": config.get("dataset_name"),
        "source_url": config.get("source_url"),
        "normalized_rows": int(data.shape[0]),
        "columns": list(data.columns),
        "notes": [
            "gender/profession label semantics are inherited from the upstream dataset card.",
            "Use this normalized file for prompt construction and group metrics.",
        ],
    }


def resolve_output_dir(path: Path) -> Path:
    if path.is_absolute():
        return path
    return ROOT / path


def make_dry_run_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "hard_text": [
                "She is a nurse with experience in emergency care.",
                "He is a software engineer focused on distributed systems.",
                "She is a professor of molecular biology.",
                "He is an attorney specializing in civil rights.",
            ],
            "profession": [0, 1, 2, 3],
            "gender": [1, 0, 1, 0],
        }
    )


def safe_display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    main()
