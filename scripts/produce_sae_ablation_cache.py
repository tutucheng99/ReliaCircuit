from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    args = parse_args()
    raw_manifest = pd.read_csv(args.manifest)
    requested_manifest = slice_manifest(raw_manifest, args)
    validate_manifest(requested_manifest, args)
    label_lookup = load_label_lookup(args) if args.metric_mode == "label_logprob" else {}

    args.output.parent.mkdir(parents=True, exist_ok=True)
    manifest = requested_manifest
    rows_skipped_existing = 0
    if args.resume:
        manifest, rows_skipped_existing = filter_completed_rows(manifest, args.output, args)
    elif not args.dry_run:
        reset_output_files(args.output)

    metadata = base_metadata(args, requested_manifest)
    metadata.update(
        {
            "input_manifest_rows": int(len(raw_manifest)),
            "row_offset": int(args.row_offset),
            "max_rows": args.max_rows,
            "resume": bool(args.resume),
            "rows_skipped_existing": int(rows_skipped_existing),
            "rows_to_compute": int(len(manifest)),
        }
    )
    if args.dry_run:
        result = make_dry_run_cache(manifest, args)
        if args.resume:
            append_rows(args.output, result.to_dict("records"))
        else:
            result.to_csv(args.output, index=False)
        metadata.update(
            {
                "dry_run": True,
                "rows_written": int(len(result)),
                "output_rows_total": count_csv_rows(args.output),
            }
        )
        write_metadata(args.output, metadata)
        print(f"dry run wrote {len(result)} exact-ablation schema rows to {safe_display_path(args.output)}")
        return
    if manifest.empty:
        metadata.update(
            {
                "dry_run": False,
                "elapsed_sec": 0.0,
                "rows_written": 0,
                "output_rows_total": count_csv_rows(args.output),
            }
        )
        write_metadata(args.output, metadata)
        print(f"no exact-ablation rows left to compute for {safe_display_path(args.output)}")
        return

    started = time.time()
    torch, model, sae = load_runtime(args)
    sae_hook_name = args.sae_acts_hook or f"{resolve_hook_name(sae, args.hook_name)}.hook_sae_acts_post"
    feature_batches = build_feature_batches(manifest, args.feature_id_column, args.batch_size)

    rows: list[dict[str, Any]] = []
    rows_written = 0
    prompt_groups_since_flush = 0
    for prompt_id, prompt_rows in manifest.groupby(args.prompt_id_column, sort=False):
        prompt_row = prompt_rows.iloc[0]
        clean_prompt = str(prompt_row[args.prompt_column])
        patch_prompt = str(prompt_row[args.patch_prompt_column])
        if args.metric_mode == "token_logit_diff":
            target_token_id = to_single_token(model, str(prompt_row[args.target_column]))
            counter_token_id = to_single_token(model, str(prompt_row[args.counter_column]))
            clean_metric, clean_logits_meta = forward_metric(
                torch=torch,
                model=model,
                prompt=clean_prompt,
                target_token_id=target_token_id,
                counter_token_id=counter_token_id,
                prepend_bos=args.prepend_bos,
            )
            patch_values = load_patch_feature_values(
                torch=torch,
                model=model,
                sae=sae,
                prompt=patch_prompt,
                feature_ids=prompt_rows[args.feature_id_column].astype(int).unique().tolist(),
                sae_hook_name=sae_hook_name,
                seq_pos=args.seq_pos,
                prepend_bos=args.prepend_bos,
                use_error_term=args.use_error_term,
            )
        else:
            target_token_id = ""
            counter_token_id = ""
            target_label = prompt_row[args.target_label_column]
            target_label_text = resolve_label_text(target_label, label_lookup)
            clean_metric, clean_logits_meta = forward_label_score(
                torch=torch,
                model=model,
                prompt=clean_prompt,
                label_text=target_label_text,
                label_prefix=args.label_prefix,
                label_score=args.label_score,
                prepend_bos=args.prepend_bos,
            )
            patch_values = load_patch_feature_values_for_label_prompt(
                torch=torch,
                model=model,
                sae=sae,
                prompt=patch_prompt,
                label_prefix=args.label_prefix,
                feature_ids=prompt_rows[args.feature_id_column].astype(int).unique().tolist(),
                sae_hook_name=sae_hook_name,
                prepend_bos=args.prepend_bos,
                use_error_term=args.use_error_term,
            )

        for batch in feature_batches_for_prompt(prompt_rows, feature_batches, args.feature_id_column):
            for _, row in batch.iterrows():
                feature_id = int(row[args.feature_id_column])
                ablation_type = str(row.get("ablation_type", args.ablation_type))
                replacement = replacement_value(torch, ablation_type, patch_values[feature_id])
                if args.metric_mode == "token_logit_diff":
                    ablated_metric = forward_intervened_metric(
                        torch=torch,
                        model=model,
                        sae=sae,
                        prompt=clean_prompt,
                        target_token_id=target_token_id,
                        counter_token_id=counter_token_id,
                        feature_id=feature_id,
                        replacement=replacement,
                        sae_hook_name=sae_hook_name,
                        seq_pos=args.seq_pos,
                        prepend_bos=args.prepend_bos,
                        use_error_term=args.use_error_term,
                    )
                else:
                    ablated_metric = forward_intervened_label_score(
                        torch=torch,
                        model=model,
                        sae=sae,
                        prompt=clean_prompt,
                        label_text=clean_logits_meta["target_label_text"],
                        label_prefix=args.label_prefix,
                        label_score=args.label_score,
                        feature_id=feature_id,
                        replacement=replacement,
                        sae_hook_name=sae_hook_name,
                        prepend_bos=args.prepend_bos,
                        use_error_term=args.use_error_term,
                    )
                rows.append(
                    output_row(
                        row=row,
                        args=args,
                        prompt_id=str(prompt_id),
                        feature_id=feature_id,
                        clean_metric=clean_metric,
                        ablated_metric=ablated_metric,
                        target_token_id=target_token_id,
                        counter_token_id=counter_token_id,
                        sae_hook_name=sae_hook_name,
                        clean_logits_meta=clean_logits_meta,
                    )
                )

        prompt_groups_since_flush += 1
        if args.flush_every_prompts > 0 and rows and prompt_groups_since_flush >= args.flush_every_prompts:
            append_rows(args.output, rows)
            rows_written += len(rows)
            rows = []
            prompt_groups_since_flush = 0

    if rows:
        append_rows(args.output, rows)
        rows_written += len(rows)
    metadata.update(
        {
            "dry_run": False,
            "elapsed_sec": round(time.time() - started, 3),
            "rows_written": int(rows_written),
            "output_rows_total": count_csv_rows(args.output),
            "sae_acts_hook": sae_hook_name,
        }
    )
    write_metadata(args.output, metadata)
    print(f"wrote {rows_written} exact-ablation rows to {safe_display_path(args.output)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Produce an SAE exact-ablation cache from a sweep manifest.")
    parser.add_argument("--model-id", default="gemma-2-2b")
    parser.add_argument("--sae-release", default="gemma-scope-2b-pt-res-canonical")
    parser.add_argument("--sae-id", default="layer_20/width_16k/canonical")
    parser.add_argument(
        "--manifest",
        type=Path,
        default=ROOT / "data" / "subject_verb_agreement" / "ablation_manifest_smoke.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "results" / "subject_verb_agreement" / "exact_ablation_cache.csv",
    )
    parser.add_argument("--prompt-id-column", default="prompt_id")
    parser.add_argument("--prompt-column", default="clean_prompt")
    parser.add_argument("--patch-prompt-column", default="patch_prompt")
    parser.add_argument("--target-column", default="target_token")
    parser.add_argument("--counter-column", default="counter_token")
    parser.add_argument("--target-label-column", default="target_label")
    parser.add_argument("--feature-id-column", default="feature_id")
    parser.add_argument(
        "--metric-mode",
        choices=["token_logit_diff", "label_logprob"],
        default="token_logit_diff",
        help="Scalar behavior metric: token logit difference or target-label log probability.",
    )
    parser.add_argument("--labels", type=Path, default=ROOT / "data" / "bias_in_bios" / "profession_labels.csv")
    parser.add_argument("--label-id-column", default="label_id")
    parser.add_argument("--label-text-column", default="label_text")
    parser.add_argument("--label-prefix", default=" ")
    parser.add_argument("--label-score", choices=["mean_logprob", "sum_logprob"], default="mean_logprob")
    parser.add_argument("--hook-name", default=None)
    parser.add_argument("--sae-acts-hook", default=None)
    parser.add_argument("--seq-pos", default="last", help="SAE activation position to intervene on: last or an integer.")
    parser.add_argument("--ablation-type", choices=["resample", "zero"], default="resample")
    parser.add_argument("--dtype", choices=["auto", "bfloat16", "float16", "float32"], default="auto")
    parser.add_argument("--device", choices=["auto", "cuda", "cpu"], default="auto")
    parser.add_argument("--cache-dir", type=Path, default=None)
    parser.add_argument("--batch-size", type=int, default=32, help="Reserved for grouping metadata; interventions are exact per row.")
    parser.add_argument("--row-offset", type=int, default=0, help="Skip this many manifest rows before applying --max-rows.")
    parser.add_argument("--max-rows", type=int, default=None)
    parser.add_argument("--resume", action="store_true", help="Append missing rows and skip rows already present in --output.")
    parser.add_argument("--flush-every-prompts", type=int, default=25)
    parser.add_argument("--include-text", action="store_true")
    parser.add_argument("--prepend-bos", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("--use-error-term", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def slice_manifest(manifest: pd.DataFrame, args: argparse.Namespace) -> pd.DataFrame:
    row_offset = int(getattr(args, "row_offset", 0) or 0)
    max_rows = getattr(args, "max_rows", None)
    if row_offset < 0:
        raise SystemExit("--row-offset must be non-negative")
    if max_rows is not None and int(max_rows) <= 0:
        raise SystemExit("--max-rows must be positive when provided")
    end = None if max_rows is None else row_offset + int(max_rows)
    return manifest.iloc[row_offset:end].copy()


def reset_output_files(output: Path) -> None:
    for path in (output, output.with_suffix(".metadata.json")):
        if path.exists():
            path.unlink()


def append_rows(output: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    write_header = not output.exists() or output.stat().st_size == 0
    pd.DataFrame(rows).to_csv(output, mode="a", header=write_header, index=False)


def count_csv_rows(path: Path) -> int:
    if not path.exists() or path.stat().st_size == 0:
        return 0
    return int(pd.read_csv(path).shape[0])


def filter_completed_rows(manifest: pd.DataFrame, output: Path, args: argparse.Namespace) -> tuple[pd.DataFrame, int]:
    if not output.exists() or output.stat().st_size == 0:
        return manifest.copy(), 0
    completed = pd.read_csv(output)
    if completed.empty:
        return manifest.copy(), 0
    use_sweep_id = "sweep_id" in manifest.columns and "sweep_id" in completed.columns
    completed_keys = completed_resume_keys(completed, use_sweep_id)
    keep_mask = [
        manifest_resume_key(row, args, use_sweep_id) not in completed_keys
        for _, row in manifest.iterrows()
    ]
    filtered = manifest.loc[keep_mask].copy()
    return filtered, int(len(manifest) - len(filtered))


def completed_resume_keys(completed: pd.DataFrame, use_sweep_id: bool) -> set[tuple[Any, ...]]:
    if use_sweep_id:
        return {("sweep_id", normalize_key_value(value)) for value in completed["sweep_id"]}
    required = {"prompt_id", "feature_id", "resample_source_id", "ablation_type"}
    missing = required - set(completed.columns)
    if missing:
        raise SystemExit(f"cannot resume from output missing key columns: {sorted(missing)}")
    return {
        (
            normalize_key_value(row["prompt_id"]),
            normalize_key_value(row["feature_id"]),
            normalize_key_value(row["resample_source_id"]),
            normalize_key_value(row["ablation_type"]),
        )
        for _, row in completed.iterrows()
    }


def manifest_resume_key(row: pd.Series, args: argparse.Namespace, use_sweep_id: bool) -> tuple[Any, ...]:
    if use_sweep_id:
        return ("sweep_id", normalize_key_value(row["sweep_id"]))
    return (
        normalize_key_value(row[args.prompt_id_column]),
        normalize_key_value(row[args.feature_id_column]),
        normalize_key_value(row.get("patch_prompt_id", row.get("patch_id", row[args.prompt_id_column]))),
        normalize_key_value(row.get("ablation_type", args.ablation_type)),
    )


def normalize_key_value(value: Any) -> str:
    if pd.isna(value):
        return ""
    return str(value)


def validate_manifest(manifest: pd.DataFrame, args: argparse.Namespace) -> None:
    if args.batch_size <= 0:
        raise SystemExit("--batch-size must be positive")
    required = {
        args.prompt_id_column,
        args.prompt_column,
        args.patch_prompt_column,
        args.feature_id_column,
    }
    metric_mode = getattr(args, "metric_mode", "token_logit_diff")
    if metric_mode == "token_logit_diff":
        required.update({args.target_column, args.counter_column})
    elif metric_mode == "label_logprob":
        required.add(args.target_label_column)
    else:
        raise SystemExit(f"unknown --metric-mode {metric_mode!r}")
    missing = required - set(manifest.columns)
    if missing:
        raise SystemExit(f"manifest missing required columns: {sorted(missing)}")
    if manifest.empty:
        raise SystemExit("manifest has no rows")
    if manifest[args.feature_id_column].isna().any():
        raise SystemExit(f"manifest column {args.feature_id_column!r} contains missing values")


def load_runtime(args: argparse.Namespace):
    import torch

    try:
        from sae_lens import HookedSAETransformer, SAE
    except Exception:
        from sae_lens import SAE
        from sae_lens.analysis.hooked_sae_transformer import HookedSAETransformer

    device = choose_device(torch, args.device)
    dtype = choose_dtype(torch, args.dtype, device)

    model_kwargs = build_hooked_model_kwargs(args, device=device, dtype=dtype)
    model = HookedSAETransformer.from_pretrained(args.model_id, **model_kwargs)
    model.eval()

    loaded = SAE.from_pretrained(release=args.sae_release, sae_id=args.sae_id, device=device)
    sae = loaded[0] if isinstance(loaded, tuple) else loaded
    return torch, model, sae


def load_label_lookup(args: argparse.Namespace) -> dict[str, str]:
    labels = pd.read_csv(args.labels)
    required = {args.label_id_column, args.label_text_column}
    missing = required - set(labels.columns)
    if missing:
        raise SystemExit(f"label file missing required columns: {sorted(missing)}")
    return {
        str(row[args.label_id_column]): str(row[args.label_text_column])
        for _, row in labels.drop_duplicates(args.label_id_column).iterrows()
    }


def resolve_label_text(label_id: Any, labels: dict[str, str]) -> str:
    key = str(label_id)
    if key not in labels:
        raise ValueError(f"target label {key!r} is not present in the label map")
    return labels[key]


def build_hooked_model_kwargs(args: argparse.Namespace, *, device: str, dtype: Any) -> dict[str, Any]:
    # TransformerLens reads HF_TOKEN internally and forwards it to HuggingFace.
    # Passing token here duplicates that keyword on current TransformerLens.
    model_kwargs: dict[str, Any] = {"device": device, "dtype": dtype}
    if args.cache_dir is not None:
        model_kwargs["cache_dir"] = str(args.cache_dir)
    return model_kwargs


def choose_device(torch, requested: str) -> str:
    if requested == "cpu":
        return "cpu"
    if requested == "cuda":
        if not torch.cuda.is_available():
            raise SystemExit("--device cuda requested but CUDA is not available")
        return "cuda"
    return "cuda" if torch.cuda.is_available() else "cpu"


def choose_dtype(torch, requested: str, device: str):
    if requested == "float32" or device == "cpu":
        return torch.float32
    if requested == "float16":
        return torch.float16
    if requested == "bfloat16":
        return torch.bfloat16
    return torch.bfloat16 if device == "cuda" else torch.float32


def resolve_hook_name(sae, fallback: str | None) -> str:
    if fallback:
        return fallback
    cfg = getattr(sae, "cfg", None)
    metadata = getattr(cfg, "metadata", None)
    for obj in (metadata, cfg):
        for key in ("hook_name", "act_name"):
            if obj is not None and hasattr(obj, key):
                value = getattr(obj, key)
                if value:
                    return str(value)
            if isinstance(obj, dict) and obj.get(key):
                return str(obj[key])
    raise ValueError("could not infer SAE hook name; pass --hook-name or --sae-acts-hook")


def to_single_token(model, token_text: str) -> int:
    if hasattr(model, "to_single_token"):
        return int(model.to_single_token(token_text))
    tokenizer = getattr(model, "tokenizer", None)
    if tokenizer is None:
        raise ValueError("model has no tokenizer for token lookup")
    ids = tokenizer.encode(token_text, add_special_tokens=False)
    if len(ids) != 1:
        raise ValueError(f"{token_text!r} must tokenize to one token, got {ids}")
    return int(ids[0])


def forward_metric(
    *,
    torch,
    model,
    prompt: str,
    target_token_id: int,
    counter_token_id: int,
    prepend_bos: bool,
) -> tuple[float, dict[str, Any]]:
    tokens = to_tokens(model, prompt, prepend_bos)
    with torch.no_grad():
        logits = unwrap_logits(model(tokens))
    metric, meta = metric_from_logits(logits, target_token_id, counter_token_id)
    return metric, meta


def load_patch_feature_values(
    *,
    torch,
    model,
    sae,
    prompt: str,
    feature_ids: list[int],
    sae_hook_name: str,
    seq_pos: str,
    prepend_bos: bool,
    use_error_term: bool,
) -> dict[int, Any]:
    tokens = to_tokens(model, prompt, prepend_bos)
    with torch.no_grad():
        _, cache = model.run_with_cache_with_saes(tokens, saes=[sae], use_error_term=use_error_term)
    acts = cache[sae_hook_name]
    seq_idx = resolve_seq_index(seq_pos, acts.shape[1])
    return {feature_id: acts[0, seq_idx, feature_id].detach() for feature_id in feature_ids}


def load_patch_feature_values_for_label_prompt(
    *,
    torch,
    model,
    sae,
    prompt: str,
    label_prefix: str,
    feature_ids: list[int],
    sae_hook_name: str,
    prepend_bos: bool,
    use_error_term: bool,
) -> dict[int, Any]:
    tokens = to_tokens(model, prompt + label_prefix, prepend_bos)
    with torch.no_grad():
        _, cache = model.run_with_cache_with_saes(tokens, saes=[sae], use_error_term=use_error_term)
    acts = cache[sae_hook_name]
    seq_idx = int(acts.shape[1]) - 1
    return {feature_id: acts[0, seq_idx, feature_id].detach() for feature_id in feature_ids}


def forward_intervened_metric(
    *,
    torch,
    model,
    sae,
    prompt: str,
    target_token_id: int,
    counter_token_id: int,
    feature_id: int,
    replacement,
    sae_hook_name: str,
    seq_pos: str,
    prepend_bos: bool,
    use_error_term: bool,
) -> float:
    tokens = to_tokens(model, prompt, prepend_bos)

    def replace_feature(sae_acts, hook):
        del hook
        seq_idx = resolve_seq_index(seq_pos, sae_acts.shape[1])
        out = sae_acts.clone()
        out[:, seq_idx, feature_id] = replacement.to(device=out.device, dtype=out.dtype)
        return out

    with torch.no_grad():
        with model.saes(saes=[sae], use_error_term=use_error_term):
            logits = unwrap_logits(model.run_with_hooks(tokens, fwd_hooks=[(sae_hook_name, replace_feature)]))
    metric, _ = metric_from_logits(logits, target_token_id, counter_token_id)
    return metric


def forward_label_score(
    *,
    torch,
    model,
    prompt: str,
    label_text: str,
    label_prefix: str,
    label_score: str,
    prepend_bos: bool,
) -> tuple[float, dict[str, Any]]:
    prefix_tokens = to_tokens(model, prompt, prepend_bos)
    full_tokens = to_tokens(model, prompt + label_prefix + label_text, prepend_bos)
    label_start = int(prefix_tokens.shape[1])
    if label_start >= int(full_tokens.shape[1]):
        raise ValueError(f"label {label_text!r} produced no target tokens")
    with torch.no_grad():
        logits = unwrap_logits(model(full_tokens))
    score = sequence_score(torch, logits, full_tokens, label_start, mode=label_score)
    return (
        score,
        {
            "target_logit": score,
            "counter_logit": 0.0,
            "target_label_text": label_text,
            "label_start": label_start,
        },
    )


def forward_intervened_label_score(
    *,
    torch,
    model,
    sae,
    prompt: str,
    label_text: str,
    label_prefix: str,
    label_score: str,
    feature_id: int,
    replacement,
    sae_hook_name: str,
    prepend_bos: bool,
    use_error_term: bool,
) -> float:
    prefix_tokens = to_tokens(model, prompt, prepend_bos)
    full_tokens = to_tokens(model, prompt + label_prefix + label_text, prepend_bos)
    label_start = int(prefix_tokens.shape[1])
    if label_start >= int(full_tokens.shape[1]):
        raise ValueError(f"label {label_text!r} produced no target tokens")

    def replace_feature(sae_acts, hook):
        del hook
        seq_idx = max(label_start - 1, 0)
        out = sae_acts.clone()
        out[:, seq_idx, feature_id] = replacement.to(device=out.device, dtype=out.dtype)
        return out

    with torch.no_grad():
        with model.saes(saes=[sae], use_error_term=use_error_term):
            logits = unwrap_logits(model.run_with_hooks(full_tokens, fwd_hooks=[(sae_hook_name, replace_feature)]))
    return sequence_score(torch, logits, full_tokens, label_start, mode=label_score)


def to_tokens(model, prompt: str, prepend_bos: bool):
    if hasattr(model, "to_tokens"):
        return model.to_tokens(prompt, prepend_bos=prepend_bos)
    tokenizer = getattr(model, "tokenizer", None)
    if tokenizer is None:
        raise ValueError("model has no tokenizer")
    inputs = tokenizer(prompt, return_tensors="pt")
    return inputs["input_ids"].to(model.device)


def unwrap_logits(output):
    if isinstance(output, tuple):
        return output[0]
    return output


def metric_from_logits(logits, target_token_id: int, counter_token_id: int) -> tuple[float, dict[str, Any]]:
    final_logits = logits[0, -1]
    target_logit = float(final_logits[target_token_id].detach().cpu())
    counter_logit = float(final_logits[counter_token_id].detach().cpu())
    return (
        target_logit - counter_logit,
        {
            "target_logit": target_logit,
            "counter_logit": counter_logit,
            "position": -1,
        },
    )


def sequence_score(torch, logits, tokens, label_start: int, *, mode: str) -> float:
    log_probs = torch.log_softmax(logits[0], dim=-1)
    token_scores = []
    for pos in range(label_start, int(tokens.shape[1])):
        token_scores.append(log_probs[pos - 1, int(tokens[0, pos])])
    stacked = torch.stack(token_scores)
    value = torch.sum(stacked) if mode == "sum_logprob" else torch.mean(stacked)
    return float(value.detach().cpu())


def resolve_seq_index(seq_pos: str, seq_len: int) -> int:
    if seq_pos == "last":
        return seq_len - 1
    idx = int(seq_pos)
    if idx < 0:
        idx = seq_len + idx
    if idx < 0 or idx >= seq_len:
        raise IndexError(f"seq_pos {seq_pos!r} is out of bounds for sequence length {seq_len}")
    return idx


def replacement_value(torch, ablation_type: str, patch_value):
    if ablation_type == "resample":
        return patch_value
    if ablation_type == "zero":
        return torch.zeros_like(patch_value)
    raise ValueError(f"unsupported ablation_type {ablation_type!r}")


def build_feature_batches(manifest: pd.DataFrame, feature_col: str, batch_size: int) -> list[list[int]]:
    feature_ids = manifest[feature_col].astype(int).drop_duplicates().tolist()
    return [feature_ids[i : i + batch_size] for i in range(0, len(feature_ids), batch_size)]


def feature_batches_for_prompt(
    prompt_rows: pd.DataFrame,
    feature_batches: list[list[int]],
    feature_col: str,
) -> list[pd.DataFrame]:
    out = []
    feature_values = prompt_rows[feature_col].astype(int)
    for batch in feature_batches:
        mask = feature_values.isin(batch)
        if mask.any():
            out.append(prompt_rows[mask].copy())
    return out


def output_row(
    *,
    row: pd.Series,
    args: argparse.Namespace,
    prompt_id: str,
    feature_id: int,
    clean_metric: float,
    ablated_metric: float,
    target_token_id: int,
    counter_token_id: int,
    sae_hook_name: str,
    clean_logits_meta: dict[str, Any],
) -> dict[str, Any]:
    out: dict[str, Any] = {
        "prompt_id": prompt_id,
        "feature_id": feature_id,
        "split": row.get("split", "test"),
        "cluster_id": row.get("cluster_id", row.get("template_id", prompt_id)),
        "layer": row.get("layer", ""),
        "hook_point": row.get("hook_name", args.hook_name or ""),
        "sae_acts_hook": sae_hook_name,
        "ablation_type": row.get("ablation_type", args.ablation_type),
        "resample_source_id": row.get("patch_prompt_id", row.get("patch_id", prompt_id)),
        "clean_metric": clean_metric,
        "ablated_metric": ablated_metric,
        "difference": clean_metric - ablated_metric,
        "target_token_id": target_token_id,
        "counter_token_id": counter_token_id,
        "target_logit": clean_logits_meta["target_logit"],
        "counter_logit": clean_logits_meta["counter_logit"],
    }
    if "sweep_id" in row.index:
        out["sweep_id"] = row["sweep_id"]
    for col in ["behavior", "subject_number", "attractor_number", "target_token", "counter_token"]:
        if col in row.index:
            out[col] = row[col]
    for col in ["target_label", "protected_label", "patch_protected_label"]:
        if col in row.index:
            out[col] = row[col]
    metric_mode = getattr(args, "metric_mode", "token_logit_diff")
    out["metric_mode"] = metric_mode
    if metric_mode == "label_logprob":
        out["target_label_text"] = clean_logits_meta.get("target_label_text", "")
        out["label_score"] = getattr(args, "label_score", "")
    if args.include_text:
        out["clean_prompt"] = row[args.prompt_column]
        out["patch_prompt"] = row[args.patch_prompt_column]
    return out


def make_dry_run_cache(manifest: pd.DataFrame, args: argparse.Namespace) -> pd.DataFrame:
    rows = []
    for i, (_, row) in enumerate(manifest.iterrows()):
        feature_id = int(row[args.feature_id_column])
        clean_metric = 1.0 + 0.01 * i
        ablated_metric = clean_metric - 0.1 / (1 + feature_id)
        rows.append(
            output_row(
                row=row,
                args=args,
                prompt_id=str(row[args.prompt_id_column]),
                feature_id=feature_id,
                clean_metric=clean_metric,
                ablated_metric=ablated_metric,
                target_token_id=-1,
                counter_token_id=-1,
                sae_hook_name=row.get("sae_acts_hook", f"{row.get('hook_name', args.hook_name or 'hook')}.hook_sae_acts_post"),
                clean_logits_meta={"target_logit": clean_metric, "counter_logit": 0.0},
            )
        )
    return pd.DataFrame(rows)


def base_metadata(args: argparse.Namespace, manifest: pd.DataFrame) -> dict[str, Any]:
    metadata = {
        "model_id": args.model_id,
        "sae_release": args.sae_release,
        "sae_id": args.sae_id,
        "manifest": safe_display_path(args.manifest),
        "manifest_rows": int(len(manifest)),
        "unique_prompts": int(manifest[args.prompt_id_column].nunique()) if args.prompt_id_column in manifest else None,
        "unique_features": int(manifest[args.feature_id_column].nunique()) if args.feature_id_column in manifest else None,
        "prompt_column": args.prompt_column,
        "patch_prompt_column": args.patch_prompt_column,
        "seq_pos": args.seq_pos,
        "prepend_bos": args.prepend_bos,
        "use_error_term": args.use_error_term,
        "metric_mode": args.metric_mode,
    }
    if args.metric_mode == "label_logprob":
        metadata.update(
            {
                "labels": safe_display_path(args.labels),
                "target_label_column": args.target_label_column,
                "label_score": args.label_score,
                "label_prefix": args.label_prefix,
            }
        )
    return metadata


def write_metadata(output: Path, metadata: dict[str, Any]) -> None:
    output.with_suffix(".metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")


def safe_display_path(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT / "src"))
    main()
