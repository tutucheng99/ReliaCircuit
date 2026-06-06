from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from produce_sae_ablation_cache import (  # noqa: E402
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
    prompts = pd.read_csv(args.prompts)
    prompts = filter_prompts(prompts, args)
    validate_prompts(prompts, args)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    if args.features_output is not None:
        args.features_output.parent.mkdir(parents=True, exist_ok=True)

    metadata = base_metadata(args, prompts)
    if args.dry_run:
        scores = make_dry_run_scores(args)
        write_outputs(scores, args, metadata | {"dry_run": True})
        print(f"dry run wrote {len(scores)} screen-score rows to {safe_display_path(args.output)}")
        return

    started = time.time()
    torch, model, sae = load_runtime(args)
    hook_name = resolve_hook_name(sae, args.hook_name)
    sae_hook_name = args.sae_acts_hook or f"{hook_name}.hook_sae_acts_post"
    layer = args.layer if args.layer is not None else infer_layer(hook_name, args.sae_id)
    candidate_feature_ids = load_candidate_feature_ids(args.candidate_features, args.feature_id_column)

    accumulator: ScreenAccumulator | None = None
    for _, row in prompts.iterrows():
        target_token_id, counter_token_id = resolve_metric_tokens(model, row, args)
        clean_metric, clean_acts = forward_metric_and_acts(
            torch=torch,
            model=model,
            sae=sae,
            prompt=str(row[args.prompt_column]),
            target_token_id=target_token_id,
            counter_token_id=counter_token_id,
            sae_hook_name=sae_hook_name,
            seq_pos=args.seq_pos,
            prepend_bos=args.prepend_bos,
            use_error_term=args.use_error_term,
        )
        patch_metric, patch_acts = forward_metric_and_acts(
            torch=torch,
            model=model,
            sae=sae,
            prompt=str(row[args.patch_prompt_column]),
            target_token_id=target_token_id,
            counter_token_id=counter_token_id,
            sae_hook_name=sae_hook_name,
            seq_pos=args.seq_pos,
            prepend_bos=args.prepend_bos,
            use_error_term=args.use_error_term,
        )
        metric_gap = 1.0 if clean_metric is None or patch_metric is None else clean_metric - patch_metric
        if accumulator is None:
            feature_ids = candidate_feature_ids or list(range(int(clean_acts.shape[0])))
            accumulator = ScreenAccumulator(feature_ids=np.asarray(feature_ids, dtype=np.int64))
        accumulator.update(
            clean_acts=clean_acts,
            patch_acts=patch_acts,
            metric_gap=metric_gap,
        )

    if accumulator is None:
        raise SystemExit("no screen prompts were processed")
    scores = accumulator.to_frame(
        score_mode=args.score_mode,
        sae_release=args.sae_release,
        sae_id=args.sae_id,
        hook_name=hook_name,
        sae_acts_hook=sae_hook_name,
        layer=layer,
        ablation_type=args.ablation_type,
    )
    metadata.update(
        {
            "dry_run": False,
            "elapsed_sec": round(time.time() - started, 3),
            "sae_acts_hook": sae_hook_name,
            "hook_name": hook_name,
            "layer": layer,
            "scored_features": int(len(scores)),
        }
    )
    write_outputs(scores, args, metadata)
    print(f"wrote {len(scores)} screen-score rows to {safe_display_path(args.output)}")
    if args.features_output is not None:
        print(f"wrote top {min(args.top_k, len(scores))} features to {safe_display_path(args.features_output)}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Produce SAE feature screen scores for a later exact-ablation sweep.")
    parser.add_argument("--model-id", default="gemma-2-2b")
    parser.add_argument("--sae-release", default="gemma-scope-2b-pt-res-canonical")
    parser.add_argument("--sae-id", default="layer_20/width_16k/canonical")
    parser.add_argument(
        "--prompts",
        type=Path,
        default=ROOT / "data" / "subject_verb_agreement" / "prompts.csv",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "results" / "subject_verb_agreement" / "screen_scores.csv",
    )
    parser.add_argument(
        "--features-output",
        type=Path,
        default=ROOT / "data" / "subject_verb_agreement" / "screened_features.csv",
    )
    parser.add_argument("--candidate-features", type=Path, default=None)
    parser.add_argument("--prompt-id-column", default="prompt_id")
    parser.add_argument("--prompt-column", default="clean_prompt")
    parser.add_argument("--patch-prompt-column", default="patch_prompt")
    parser.add_argument("--target-column", default="target_token")
    parser.add_argument("--counter-column", default="counter_token")
    parser.add_argument("--feature-id-column", default="feature_id")
    parser.add_argument("--split", default="screen", choices=["screen", "test", "heldout", "all"])
    parser.add_argument("--max-prompts", type=int, default=None)
    parser.add_argument("--top-k", type=int, default=96)
    parser.add_argument("--dry-run-features", type=int, default=96)
    parser.add_argument(
        "--score-mode",
        choices=["metric_weighted_delta", "activation_delta", "signed_delta"],
        default="metric_weighted_delta",
    )
    parser.add_argument("--hook-name", default=None)
    parser.add_argument("--sae-acts-hook", default=None)
    parser.add_argument("--layer", type=int, default=None)
    parser.add_argument("--seq-pos", default="last")
    parser.add_argument("--ablation-type", choices=["resample", "zero"], default="resample")
    parser.add_argument("--dtype", choices=["auto", "bfloat16", "float16", "float32"], default="auto")
    parser.add_argument("--device", choices=["auto", "cuda", "cpu"], default="auto")
    parser.add_argument("--cache-dir", type=Path, default=None)
    parser.add_argument("--prepend-bos", action=argparse.BooleanOptionalAction, default=False)
    parser.add_argument("--use-error-term", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def filter_prompts(prompts: pd.DataFrame, args: argparse.Namespace) -> pd.DataFrame:
    out = prompts.copy()
    if args.split != "all" and "split" in out.columns:
        out = out[out["split"] == args.split].copy()
    if args.max_prompts is not None:
        out = out.head(args.max_prompts).copy()
    return out


def validate_prompts(prompts: pd.DataFrame, args: argparse.Namespace) -> None:
    if args.top_k <= 0:
        raise SystemExit("--top-k must be positive")
    if args.dry_run_features <= 0:
        raise SystemExit("--dry-run-features must be positive")
    required = {args.prompt_id_column, args.prompt_column, args.patch_prompt_column}
    if args.score_mode == "metric_weighted_delta":
        required.update({args.target_column, args.counter_column})
    missing = required - set(prompts.columns)
    if missing:
        raise SystemExit(f"prompt file missing required columns: {sorted(missing)}")
    if prompts.empty:
        raise SystemExit("no prompts remain after filtering")


def forward_metric_and_acts(
    *,
    torch,
    model,
    sae,
    prompt: str,
    target_token_id: int,
    counter_token_id: int,
    sae_hook_name: str,
    seq_pos: str,
    prepend_bos: bool,
    use_error_term: bool,
) -> tuple[float | None, np.ndarray]:
    tokens = to_tokens(model, prompt, prepend_bos)
    with torch.no_grad():
        logits, cache = model.run_with_cache_with_saes(tokens, saes=[sae], use_error_term=use_error_term)
    logits = unwrap_logits(logits)
    metric = None
    if target_token_id is not None and counter_token_id is not None:
        metric, _ = metric_from_logits(logits, target_token_id, counter_token_id)
    acts = cache[sae_hook_name]
    seq_idx = resolve_seq_index(seq_pos, acts.shape[1])
    return metric, acts[0, seq_idx].detach().float().cpu().numpy()


class ScreenAccumulator:
    def __init__(self, feature_ids: np.ndarray):
        self.feature_ids = feature_ids
        n = len(feature_ids)
        self.sum_abs_delta = np.zeros(n, dtype=np.float64)
        self.sum_signed_delta = np.zeros(n, dtype=np.float64)
        self.sum_metric_weighted_delta = np.zeros(n, dtype=np.float64)
        self.sum_abs_metric_gap = 0.0
        self.n_prompts = 0

    def update(self, clean_acts: np.ndarray, patch_acts: np.ndarray, metric_gap: float) -> None:
        delta = clean_acts[self.feature_ids] - patch_acts[self.feature_ids]
        abs_delta = np.abs(delta)
        abs_metric_gap = abs(float(metric_gap))
        self.sum_abs_delta += abs_delta
        self.sum_signed_delta += delta
        self.sum_metric_weighted_delta += abs_delta * abs_metric_gap
        self.sum_abs_metric_gap += abs_metric_gap
        self.n_prompts += 1

    def to_frame(
        self,
        *,
        score_mode: str,
        sae_release: str,
        sae_id: str,
        hook_name: str,
        sae_acts_hook: str,
        layer: int | None,
        ablation_type: str,
    ) -> pd.DataFrame:
        if self.n_prompts <= 0:
            raise ValueError("cannot build scores before any prompts are accumulated")
        mean_abs_delta = self.sum_abs_delta / self.n_prompts
        mean_signed_delta = self.sum_signed_delta / self.n_prompts
        mean_metric_weighted = self.sum_metric_weighted_delta / self.n_prompts
        if score_mode == "metric_weighted_delta":
            screen_score = mean_metric_weighted
        elif score_mode == "activation_delta":
            screen_score = mean_abs_delta
        elif score_mode == "signed_delta":
            screen_score = np.abs(mean_signed_delta)
        else:
            raise ValueError(f"unknown score mode {score_mode!r}")
        frame = pd.DataFrame(
            {
                "feature_id": self.feature_ids.astype(int),
                "screen_score": screen_score,
                "mean_abs_activation_delta": mean_abs_delta,
                "mean_signed_activation_delta": mean_signed_delta,
                "mean_metric_weighted_delta": mean_metric_weighted,
                "mean_abs_metric_gap": self.sum_abs_metric_gap / self.n_prompts,
                "n_screen_prompts": self.n_prompts,
                "sae_release": sae_release,
                "sae_id": sae_id,
                "hook_name": hook_name,
                "sae_acts_hook": sae_acts_hook,
                "layer": layer,
                "ablation_type": ablation_type,
            }
        )
        frame = frame.sort_values(["screen_score", "feature_id"], ascending=[False, True]).reset_index(drop=True)
        frame.insert(0, "screen_rank", np.arange(1, len(frame) + 1))
        return frame


def make_dry_run_scores(args: argparse.Namespace) -> pd.DataFrame:
    n = max(args.dry_run_features, args.top_k)
    feature_ids = np.arange(n, dtype=np.int64)
    accumulator = ScreenAccumulator(feature_ids)
    clean = np.linspace(1.0, 0.1, n)
    patch = np.zeros(n)
    accumulator.update(clean_acts=clean, patch_acts=patch, metric_gap=1.0)
    hook_name = args.hook_name or "blocks.20.hook_resid_post"
    layer = args.layer if args.layer is not None else infer_layer(hook_name, args.sae_id)
    sae_acts_hook = args.sae_acts_hook or f"{hook_name}.hook_sae_acts_post"
    return accumulator.to_frame(
        score_mode=args.score_mode,
        sae_release=args.sae_release,
        sae_id=args.sae_id,
        hook_name=hook_name,
        sae_acts_hook=sae_acts_hook,
        layer=layer,
        ablation_type=args.ablation_type,
    )


def resolve_metric_tokens(model, row: pd.Series, args: argparse.Namespace) -> tuple[int | None, int | None]:
    if args.score_mode != "metric_weighted_delta":
        return None, None
    return to_single_token(model, str(row[args.target_column])), to_single_token(
        model, str(row[args.counter_column])
    )


def write_outputs(scores: pd.DataFrame, args: argparse.Namespace, metadata: dict[str, Any]) -> None:
    scores.to_csv(args.output, index=False)
    if args.features_output is not None:
        features = scores.head(args.top_k).copy()
        features.to_csv(args.features_output, index=False)
        metadata["features_output"] = safe_display_path(args.features_output)
        metadata["features_written"] = int(len(features))
    args.output.with_suffix(".metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")


def load_candidate_feature_ids(path: Path | None, feature_col: str) -> list[int] | None:
    if path is None:
        return None
    features = pd.read_csv(path)
    if feature_col not in features.columns:
        raise SystemExit(f"candidate feature file missing column {feature_col!r}")
    return features[feature_col].astype(int).drop_duplicates().tolist()


def infer_layer(hook_name: str | None, sae_id: str) -> int | None:
    for text, pattern in [
        (hook_name or "", r"blocks\.(\d+)\."),
        (sae_id, r"layer_(\d+)"),
    ]:
        match = re.search(pattern, text)
        if match:
            return int(match.group(1))
    return None


def base_metadata(args: argparse.Namespace, prompts: pd.DataFrame) -> dict[str, Any]:
    return {
        "model_id": args.model_id,
        "sae_release": args.sae_release,
        "sae_id": args.sae_id,
        "prompts": safe_display_path(args.prompts),
        "prompt_rows": int(len(prompts)),
        "split": args.split,
        "top_k": args.top_k,
        "score_mode": args.score_mode,
        "seq_pos": args.seq_pos,
        "prepend_bos": args.prepend_bos,
        "use_error_term": args.use_error_term,
        "candidate_features": safe_display_path(args.candidate_features) if args.candidate_features else None,
    }


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT / "src"))
    main()
