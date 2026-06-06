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
    load_runtime,
    resolve_hook_name,
    resolve_seq_index,
    safe_display_path,
    to_tokens,
    unwrap_logits,
)


def main() -> None:
    args = parse_args()
    prompts = pd.read_csv(args.prompts)
    if args.max_rows is not None:
        prompts = prompts.head(args.max_rows).copy()
    validate_prompts(prompts, args)
    labels = load_labels(args.labels, prompts, target_col=args.target_column)
    feature_sets = load_feature_sets(args.feature_set, args.feature_id_column)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    metadata = base_metadata(args, prompts, labels, feature_sets)
    if args.dry_run:
        predictions = make_dry_run_predictions(prompts, labels, feature_sets, args)
        write_outputs(predictions, args.output, metadata | {"dry_run": True})
        print(f"dry run wrote {len(predictions)} BiasInBios prediction rows to {safe_display_path(args.output)}")
        return

    started = time.time()
    torch, model, sae = load_runtime(args)
    hook_name = resolve_hook_name(sae, args.hook_name)
    sae_acts_hook = args.sae_acts_hook or f"{hook_name}.hook_sae_acts_post"

    rows: list[dict[str, Any]] = []
    methods: list[tuple[str, list[int]]] = [("clean", [])] + feature_sets
    for _, row in prompts.iterrows():
        for method, feature_ids in methods:
            scores = score_candidates(
                torch=torch,
                model=model,
                sae=sae,
                prompt=str(row[args.prompt_column]),
                labels=labels,
                feature_ids=feature_ids,
                sae_hook_name=sae_acts_hook,
                intervention_pos=args.intervention_pos,
                prepend_bos=args.prepend_bos,
                use_error_term=args.use_error_term,
                label_prefix=args.label_prefix,
                label_score=args.label_score,
            )
            best = max(scores, key=lambda item: item["score"])
            rows.append(
                {
                    "example_id": row[args.example_column],
                    "method": method,
                    "predicted_label": best["label_id"],
                    "predicted_label_text": best["label_text"],
                    "prediction_score": best["score"],
                    "target_label": row.get(args.target_column, ""),
                    "protected_label": row.get(args.protected_column, ""),
                    "n_removed_features": len(feature_ids),
                }
            )
        if args.flush_every_rows > 0 and rows and len(rows) % args.flush_every_rows == 0:
            pd.DataFrame(rows).to_csv(args.output, index=False)

    predictions = pd.DataFrame(rows)
    metadata.update(
        {
            "dry_run": False,
            "elapsed_sec": round(time.time() - started, 3),
            "rows_written": int(len(predictions)),
            "hook_name": hook_name,
            "sae_acts_hook": sae_acts_hook,
        }
    )
    write_outputs(predictions, args.output, metadata)
    print(f"wrote {len(predictions)} BiasInBios prediction rows to {safe_display_path(args.output)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Produce BiasInBios profession prediction caches.")
    parser.add_argument("--model-id", default="gemma-2-2b")
    parser.add_argument("--sae-release", default="gemma-scope-2b-pt-res-canonical")
    parser.add_argument("--sae-id", default="layer_20/width_16k/canonical")
    parser.add_argument("--prompts", type=Path, default=ROOT / "data" / "bias_in_bios" / "prompts.csv")
    parser.add_argument("--labels", type=Path, default=ROOT / "data" / "bias_in_bios" / "profession_labels.csv")
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "results" / "bias_in_bios" / "bias_in_bios_prediction_cache.csv",
    )
    parser.add_argument(
        "--feature-set",
        action="append",
        default=[],
        metavar="METHOD=CSV",
        help="Optional selected-feature CSV to zero-ablate for one method. May be repeated.",
    )
    parser.add_argument("--example-column", default="example_id")
    parser.add_argument("--prompt-column", default="prompt")
    parser.add_argument("--target-column", default="target_label")
    parser.add_argument("--protected-column", default="protected_label")
    parser.add_argument("--feature-id-column", default="feature_id")
    parser.add_argument("--hook-name", default=None)
    parser.add_argument("--sae-acts-hook", default=None)
    parser.add_argument("--intervention-pos", default="prompt_last")
    parser.add_argument("--label-prefix", default=" ")
    parser.add_argument("--label-score", choices=["mean_logprob", "sum_logprob"], default="mean_logprob")
    parser.add_argument("--dtype", choices=["auto", "bfloat16", "float16", "float32"], default="auto")
    parser.add_argument("--device", choices=["auto", "cuda", "cpu"], default="auto")
    parser.add_argument("--cache-dir", type=Path, default=None)
    parser.add_argument("--max-rows", type=int, default=None)
    parser.add_argument("--flush-every-rows", type=int, default=25)
    parser.add_argument("--prepend-bos", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("--use-error-term", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def validate_prompts(prompts: pd.DataFrame, args: argparse.Namespace) -> None:
    required = {args.example_column, args.prompt_column, args.target_column, args.protected_column}
    missing = required - set(prompts.columns)
    if missing:
        raise SystemExit(f"prompt file missing required columns: {sorted(missing)}")
    if prompts.empty:
        raise SystemExit("prompt file has no rows after filtering")


def load_labels(path: Path, prompts: pd.DataFrame, *, target_col: str) -> pd.DataFrame:
    if path.exists():
        labels = pd.read_csv(path)
        required = {"label_id", "label_text"}
        missing = required - set(labels.columns)
        if missing:
            raise SystemExit(f"label file missing columns: {sorted(missing)}")
        return labels.loc[:, ["label_id", "label_text"]].drop_duplicates("label_id").copy()
    unique = sorted(str(value) for value in prompts[target_col].dropna().unique())
    return pd.DataFrame({"label_id": unique, "label_text": unique})


def load_feature_sets(specs: list[str], feature_col: str) -> list[tuple[str, list[int]]]:
    out: list[tuple[str, list[int]]] = []
    for spec in specs:
        if "=" not in spec:
            raise SystemExit(f"--feature-set must use METHOD=CSV format, got {spec!r}")
        method, path_text = spec.split("=", maxsplit=1)
        method = method.strip()
        path = Path(path_text.strip())
        if not method:
            raise SystemExit(f"--feature-set method is empty in {spec!r}")
        features = pd.read_csv(path)
        if feature_col not in features.columns:
            raise SystemExit(f"feature-set file {path} missing column {feature_col!r}")
        ids = features[feature_col].dropna().astype(int).drop_duplicates().tolist()
        out.append((method, ids))
    return out


def score_candidates(
    *,
    torch,
    model,
    sae,
    prompt: str,
    labels: pd.DataFrame,
    feature_ids: list[int],
    sae_hook_name: str,
    intervention_pos: str,
    prepend_bos: bool,
    use_error_term: bool,
    label_prefix: str,
    label_score: str,
) -> list[dict[str, Any]]:
    scores = []
    for _, label in labels.iterrows():
        full_text = prompt + label_prefix + str(label["label_text"])
        prefix_tokens = to_tokens(model, prompt, prepend_bos)
        full_tokens = to_tokens(model, full_text, prepend_bos)
        label_start = int(prefix_tokens.shape[1])
        if label_start >= int(full_tokens.shape[1]):
            raise ValueError(f"label {label['label_text']!r} produced no target tokens")
        with torch.no_grad():
            if feature_ids:
                logits = forward_with_zeroed_features(
                    model=model,
                    sae=sae,
                    tokens=full_tokens,
                    feature_ids=feature_ids,
                    sae_hook_name=sae_hook_name,
                    intervention_pos=intervention_pos,
                    prompt_len=label_start,
                    use_error_term=use_error_term,
                )
            else:
                logits = unwrap_logits(model(full_tokens))
        score = sequence_score(torch, logits, full_tokens, label_start, mode=label_score)
        scores.append({"label_id": str(label["label_id"]), "label_text": str(label["label_text"]), "score": score})
    return scores


def forward_with_zeroed_features(
    *,
    model,
    sae,
    tokens,
    feature_ids: list[int],
    sae_hook_name: str,
    intervention_pos: str,
    prompt_len: int,
    use_error_term: bool,
):
    def zero_features(sae_acts, hook):
        del hook
        seq_idx = resolve_intervention_index(intervention_pos, seq_len=int(sae_acts.shape[1]), prompt_len=prompt_len)
        out = sae_acts.clone()
        for feature_id in feature_ids:
            out[:, seq_idx, feature_id] = 0.0
        return out

    with model.saes(saes=[sae], use_error_term=use_error_term):
        return unwrap_logits(model.run_with_hooks(tokens, fwd_hooks=[(sae_hook_name, zero_features)]))


def resolve_intervention_index(position: str, *, seq_len: int, prompt_len: int) -> int:
    if position == "prompt_last":
        return max(prompt_len - 1, 0)
    return resolve_seq_index(position, seq_len)


def sequence_score(torch, logits, tokens, label_start: int, *, mode: str) -> float:
    log_probs = torch.log_softmax(logits[0], dim=-1)
    token_scores = []
    for pos in range(label_start, int(tokens.shape[1])):
        token_scores.append(log_probs[pos - 1, int(tokens[0, pos])])
    stacked = torch.stack(token_scores)
    value = torch.sum(stacked) if mode == "sum_logprob" else torch.mean(stacked)
    return float(value.detach().cpu())


def make_dry_run_predictions(
    prompts: pd.DataFrame,
    labels: pd.DataFrame,
    feature_sets: list[tuple[str, list[int]]],
    args: argparse.Namespace,
) -> pd.DataFrame:
    methods = [("clean", [])] + (feature_sets or [("e_bh_pcal", [0, 1, 2, 3, 4]), ("top_score", [0, 1, 2, 3, 4])])
    label_ids = [str(value) for value in labels["label_id"].tolist()]
    rows = []
    for i, row in prompts.reset_index(drop=True).iterrows():
        true_label = str(row[args.target_column])
        fallback = next((label for label in label_ids if label != true_label), true_label)
        for method, feature_ids in methods:
            predicted = true_label
            if method == "clean" and i % 2 == 0:
                predicted = fallback
            elif method == "top_score" and i % 3 == 0:
                predicted = fallback
            label_text = labels.set_index(labels["label_id"].astype(str)).loc[predicted, "label_text"]
            rows.append(
                {
                    "example_id": row[args.example_column],
                    "method": method,
                    "predicted_label": predicted,
                    "predicted_label_text": label_text,
                    "prediction_score": 0.0 if predicted == true_label else -1.0,
                    "target_label": true_label,
                    "protected_label": row[args.protected_column],
                    "n_removed_features": len(feature_ids),
                }
            )
    return pd.DataFrame(rows)


def base_metadata(
    args: argparse.Namespace,
    prompts: pd.DataFrame,
    labels: pd.DataFrame,
    feature_sets: list[tuple[str, list[int]]],
) -> dict[str, Any]:
    methods = ["clean", *[method for method, _ in feature_sets]]
    if args.dry_run and not feature_sets:
        methods = ["clean", "e_bh_pcal", "top_score"]
    return {
        "model_id": args.model_id,
        "sae_release": args.sae_release,
        "sae_id": args.sae_id,
        "prompts": safe_display_path(args.prompts),
        "labels": safe_display_path(args.labels),
        "prompt_rows": int(len(prompts)),
        "candidate_labels": int(len(labels)),
        "methods": methods,
        "label_score": args.label_score,
        "intervention_pos": args.intervention_pos,
        "prepend_bos": args.prepend_bos,
        "use_error_term": args.use_error_term,
    }


def write_outputs(predictions: pd.DataFrame, output: Path, metadata: dict[str, Any]) -> None:
    predictions.to_csv(output, index=False)
    metadata["rows_written"] = int(len(predictions))
    output.with_suffix(".metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT / "src"))
    main()
