from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    args = parse_args()
    prompts = pd.read_csv(args.prompts)
    if args.max_rows is not None:
        prompts = prompts.head(args.max_rows).copy()
    required = {args.prompt_column, args.target_column, args.counter_column, "prompt_id"}
    missing = required - set(prompts.columns)
    if missing:
        raise SystemExit(f"prompt file missing columns: {sorted(missing)}")

    if args.dry_run:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        prompts.head(min(len(prompts), 10)).to_csv(args.output, index=False)
        print(f"dry run wrote prompt preview to {safe_display_path(args.output)}")
        return

    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")
    kwargs = {}
    if token:
        kwargs["token"] = token
    if args.cache_dir is not None:
        kwargs["cache_dir"] = str(args.cache_dir)

    dtype = choose_dtype(torch, args.dtype)
    tokenizer = AutoTokenizer.from_pretrained(args.model_id, **kwargs)
    model_kwargs = dict(kwargs)
    model_kwargs["torch_dtype"] = dtype
    if torch.cuda.is_available():
        model_kwargs["device_map"] = "auto"
    model = AutoModelForCausalLM.from_pretrained(args.model_id, **model_kwargs)
    if not torch.cuda.is_available():
        model.to("cpu")
    model.eval()

    rows = []
    started = time.time()
    for _, row in prompts.iterrows():
        metric = score_prompt(
            model=model,
            tokenizer=tokenizer,
            prompt=str(row[args.prompt_column]),
            target=str(row[args.target_column]),
            counter=str(row[args.counter_column]),
        )
        out = row.to_dict()
        out.update(metric)
        rows.append(out)

    result = pd.DataFrame(rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(args.output, index=False)
    metadata = {
        "model_id": args.model_id,
        "prompt_column": args.prompt_column,
        "rows": len(result),
        "elapsed_sec": round(time.time() - started, 3),
    }
    args.output.with_suffix(".metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(f"wrote {len(result)} metric rows to {safe_display_path(args.output)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-id", default="google/gemma-2-2b")
    parser.add_argument(
        "--prompts",
        type=Path,
        default=ROOT / "data" / "subject_verb_agreement" / "prompts.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "results" / "subject_verb_agreement" / "clean_metric_cache.csv",
    )
    parser.add_argument("--prompt-column", default="clean_prompt")
    parser.add_argument("--target-column", default="target_token")
    parser.add_argument("--counter-column", default="counter_token")
    parser.add_argument("--dtype", choices=["auto", "bfloat16", "float16", "float32"], default="auto")
    parser.add_argument("--cache-dir", type=Path, default=None)
    parser.add_argument("--max-rows", type=int, default=None)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def score_prompt(model, tokenizer, prompt: str, target: str, counter: str) -> dict[str, float | int]:
    import torch

    target_ids = tokenizer.encode(target, add_special_tokens=False)
    counter_ids = tokenizer.encode(counter, add_special_tokens=False)
    if len(target_ids) != 1 or len(counter_ids) != 1:
        raise ValueError(
            f"target/counter must each tokenize to one token; got {target!r}->{target_ids}, "
            f"{counter!r}->{counter_ids}"
        )

    inputs = tokenizer(prompt, return_tensors="pt")
    inputs = {k: v.to(model.device) for k, v in inputs.items()}
    with torch.no_grad():
        logits = model(**inputs).logits[0, -1]
    target_logit = float(logits[target_ids[0]].detach().cpu())
    counter_logit = float(logits[counter_ids[0]].detach().cpu())
    return {
        "target_token_id": int(target_ids[0]),
        "counter_token_id": int(counter_ids[0]),
        "target_logit": target_logit,
        "counter_logit": counter_logit,
        "metric": target_logit - counter_logit,
    }


def choose_dtype(torch, dtype: str):
    if dtype == "auto":
        return torch.bfloat16 if torch.cuda.is_available() else torch.float32
    return getattr(torch, dtype)


def safe_display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return path.name


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT / "src"))
    main()
