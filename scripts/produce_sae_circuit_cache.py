from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from produce_sae_ablation_cache import (  # noqa: E402
    forward_metric,
    load_patch_feature_values,
    load_runtime,
    metric_from_logits,
    resolve_hook_name,
    resolve_seq_index,
    safe_display_path,
    to_single_token,
    to_tokens,
    unwrap_logits,
)


def main() -> None:
    args = parse_args()
    manifest = pd.read_csv(args.manifest)
    if args.max_rows is not None:
        manifest = manifest.head(args.max_rows).copy()
    validate_manifest(manifest, args)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    metadata = base_metadata(args, manifest)
    if args.dry_run:
        cache = make_dry_run_cache(manifest, args)
        write_outputs(cache, args.output, metadata | {"dry_run": True})
        print(f"dry run wrote {len(cache)} circuit-cache rows to {safe_display_path(args.output)}")
        return

    started = time.time()
    torch, model, sae = load_runtime(args)
    hook_name = resolve_hook_name(sae, args.hook_name)
    sae_acts_hook = args.sae_acts_hook or f"{hook_name}.hook_sae_acts_post"

    rows: list[dict[str, Any]] = []
    for _, row in manifest.iterrows():
        feature_ids = parse_feature_ids(row[args.selected_features_column])
        target_token_id = to_single_token(model, str(row[args.target_column]))
        counter_token_id = to_single_token(model, str(row[args.counter_column]))
        clean_prompt = str(row[args.prompt_column])
        patch_prompt = str(row[args.patch_prompt_column])

        clean_metric, _ = forward_metric(
            torch=torch,
            model=model,
            prompt=clean_prompt,
            target_token_id=target_token_id,
            counter_token_id=counter_token_id,
            prepend_bos=args.prepend_bos,
        )
        patch_metric, _ = forward_metric(
            torch=torch,
            model=model,
            prompt=patch_prompt,
            target_token_id=target_token_id,
            counter_token_id=counter_token_id,
            prepend_bos=args.prepend_bos,
        )
        if feature_ids:
            patch_values = load_patch_feature_values(
                torch=torch,
                model=model,
                sae=sae,
                prompt=patch_prompt,
                feature_ids=feature_ids,
                sae_hook_name=sae_acts_hook,
                seq_pos=args.seq_pos,
                prepend_bos=args.prepend_bos,
                use_error_term=args.use_error_term,
            )
            selected_patch_metric = forward_joint_intervened_metric(
                torch=torch,
                model=model,
                sae=sae,
                prompt=clean_prompt,
                target_token_id=target_token_id,
                counter_token_id=counter_token_id,
                feature_ids=feature_ids,
                patch_values=patch_values,
                sae_hook_name=sae_acts_hook,
                seq_pos=args.seq_pos,
                prepend_bos=args.prepend_bos,
                use_error_term=args.use_error_term,
            )
        else:
            selected_patch_metric = clean_metric

        rows.append(
            output_row(
                row=row,
                args=args,
                feature_ids=feature_ids,
                clean_metric=clean_metric,
                patch_metric=patch_metric,
                selected_patch_metric=selected_patch_metric,
                target_token_id=target_token_id,
                counter_token_id=counter_token_id,
                hook_name=hook_name,
                sae_acts_hook=sae_acts_hook,
            )
        )
        if args.flush_every_rows > 0 and rows and len(rows) % args.flush_every_rows == 0:
            pd.DataFrame(rows).to_csv(args.output, index=False)

    cache = pd.DataFrame(rows)
    metadata.update(
        {
            "dry_run": False,
            "elapsed_sec": round(time.time() - started, 3),
            "rows_written": int(len(cache)),
            "hook_name": hook_name,
            "sae_acts_hook": sae_acts_hook,
        }
    )
    write_outputs(cache, args.output, metadata)
    print(f"wrote {len(cache)} circuit-cache rows to {safe_display_path(args.output)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Produce a held-out joint SAE circuit cache.")
    parser.add_argument("--model-id", default="gemma-2-2b")
    parser.add_argument("--sae-release", default="gemma-scope-2b-pt-res-canonical")
    parser.add_argument("--sae-id", default="layer_20/width_16k/canonical")
    parser.add_argument(
        "--manifest",
        type=Path,
        default=ROOT / "data" / "subject_verb_agreement" / "circuit_eval_manifest_smoke.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "results" / "subject_verb_agreement" / "joint_circuit_cache.csv",
    )
    parser.add_argument("--prompt-id-column", default="prompt_id")
    parser.add_argument("--prompt-column", default="clean_prompt")
    parser.add_argument("--patch-prompt-column", default="patch_prompt")
    parser.add_argument("--target-column", default="target_token")
    parser.add_argument("--counter-column", default="counter_token")
    parser.add_argument("--selected-features-column", default="selected_feature_ids")
    parser.add_argument("--method-column", default="method")
    parser.add_argument("--hook-name", default=None)
    parser.add_argument("--sae-acts-hook", default=None)
    parser.add_argument("--seq-pos", default="last")
    parser.add_argument("--dtype", choices=["auto", "bfloat16", "float16", "float32"], default="auto")
    parser.add_argument("--device", choices=["auto", "cuda", "cpu"], default="auto")
    parser.add_argument("--cache-dir", type=Path, default=None)
    parser.add_argument("--max-rows", type=int, default=None)
    parser.add_argument("--flush-every-rows", type=int, default=25)
    parser.add_argument("--include-text", action="store_true")
    parser.add_argument("--prepend-bos", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("--use-error-term", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def validate_manifest(manifest: pd.DataFrame, args: argparse.Namespace) -> None:
    required = {
        args.prompt_id_column,
        args.prompt_column,
        args.patch_prompt_column,
        args.target_column,
        args.counter_column,
        args.selected_features_column,
        args.method_column,
    }
    missing = required - set(manifest.columns)
    if missing:
        raise SystemExit(f"circuit manifest missing required columns: {sorted(missing)}")
    if manifest.empty:
        raise SystemExit("circuit manifest has no rows")


def parse_feature_ids(value: Any) -> list[int]:
    if pd.isna(value):
        return []
    text = str(value).strip()
    if not text:
        return []
    out = []
    for part in text.replace(",", ";").split(";"):
        part = part.strip()
        if not part:
            continue
        out.append(int(float(part)))
    return out


def forward_joint_intervened_metric(
    *,
    torch,
    model,
    sae,
    prompt: str,
    target_token_id: int,
    counter_token_id: int,
    feature_ids: list[int],
    patch_values: dict[int, Any],
    sae_hook_name: str,
    seq_pos: str,
    prepend_bos: bool,
    use_error_term: bool,
) -> float:
    tokens = to_tokens(model, prompt, prepend_bos)

    def replace_features(sae_acts, hook):
        del hook
        seq_idx = resolve_seq_index(seq_pos, sae_acts.shape[1])
        out = sae_acts.clone()
        for feature_id in feature_ids:
            out[:, seq_idx, feature_id] = patch_values[feature_id].to(device=out.device, dtype=out.dtype)
        return out

    with torch.no_grad():
        with model.saes(saes=[sae], use_error_term=use_error_term):
            logits = unwrap_logits(model.run_with_hooks(tokens, fwd_hooks=[(sae_hook_name, replace_features)]))
    metric, _ = metric_from_logits(logits, target_token_id, counter_token_id)
    return metric


def output_row(
    *,
    row: pd.Series,
    args: argparse.Namespace,
    feature_ids: list[int],
    clean_metric: float,
    patch_metric: float,
    selected_patch_metric: float,
    target_token_id: int,
    counter_token_id: int,
    hook_name: str | None,
    sae_acts_hook: str,
) -> dict[str, Any]:
    out: dict[str, Any] = {
        "prompt_id": row[args.prompt_id_column],
        "method": row[args.method_column],
        "clean_metric": clean_metric,
        "patch_metric": patch_metric,
        "selected_patch_metric": selected_patch_metric,
        "full_difference": clean_metric - patch_metric,
        "selected_difference": clean_metric - selected_patch_metric,
        "n_selected_features": len(feature_ids),
        "selected_feature_ids": ";".join(str(feature_id) for feature_id in feature_ids),
        "target_token_id": target_token_id,
        "counter_token_id": counter_token_id,
        "hook_point": hook_name or "",
        "sae_acts_hook": sae_acts_hook,
    }
    for col in ["circuit_eval_id", "split", "cluster_id", "template_id", "behavior", "subject_number", "attractor_number"]:
        if col in row.index:
            out[col] = row[col]
    if args.include_text:
        out["clean_prompt"] = row[args.prompt_column]
        out["patch_prompt"] = row[args.patch_prompt_column]
    return out


def make_dry_run_cache(manifest: pd.DataFrame, args: argparse.Namespace) -> pd.DataFrame:
    rows = []
    for i, (_, row) in enumerate(manifest.iterrows()):
        feature_ids = parse_feature_ids(row[args.selected_features_column])
        clean_metric = 1.0 + i * 0.01
        patch_metric = 0.25 + i * 0.005
        selected_fraction = min(len(feature_ids), 5) / 5 if feature_ids else 0.0
        full_difference = clean_metric - patch_metric
        selected_patch_metric = clean_metric - full_difference * selected_fraction
        rows.append(
            output_row(
                row=row,
                args=args,
                feature_ids=feature_ids,
                clean_metric=clean_metric,
                patch_metric=patch_metric,
                selected_patch_metric=selected_patch_metric,
                target_token_id=-1,
                counter_token_id=-1,
                hook_name=args.hook_name or "blocks.20.hook_resid_post",
                sae_acts_hook=args.sae_acts_hook or "blocks.20.hook_resid_post.hook_sae_acts_post",
            )
        )
    return pd.DataFrame(rows)


def base_metadata(args: argparse.Namespace, manifest: pd.DataFrame) -> dict[str, Any]:
    return {
        "model_id": args.model_id,
        "sae_release": args.sae_release,
        "sae_id": args.sae_id,
        "manifest": safe_display_path(args.manifest),
        "manifest_rows": int(len(manifest)),
        "unique_methods": int(manifest[args.method_column].nunique()) if args.method_column in manifest else None,
        "seq_pos": args.seq_pos,
        "prepend_bos": args.prepend_bos,
        "use_error_term": args.use_error_term,
    }


def write_outputs(cache: pd.DataFrame, output: Path, metadata: dict[str, Any]) -> None:
    cache.to_csv(output, index=False)
    metadata["rows_written"] = int(len(cache))
    output.with_suffix(".metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT / "src"))
    main()
