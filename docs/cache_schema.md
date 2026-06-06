# Exact-Ablation Cache Schema

The GPU stage should write exact-ablation results in a table that the CPU
statistics layer can analyze without rerunning model forwards.

## Required columns

- `feature_id`: stable SAE feature identifier.
- Either `difference`, or both:
  - `clean_metric`
  - `ablated_metric`

The analysis defines `difference = clean_metric - ablated_metric`.

For Gemma Scope runs, `scripts/produce_sae_ablation_cache.py` writes this
schema from an ablation manifest by replacing one SAE feature activation at a
time on `<hook_name>.hook_sae_acts_post`.

## Screen-score table

Before exact ablation, `scripts/produce_sae_screen_scores.py` can rank candidate
SAE features on the independent `screen` split. Its selected feature output is
accepted by `scripts/create_ablation_sweep_manifest.py`.

Recommended screen columns:

- `screen_rank`
- `feature_id`
- `screen_score`
- `mean_abs_activation_delta`
- `mean_metric_weighted_delta`
- `n_screen_prompts`
- `sae_release`
- `sae_id`
- `hook_name`
- `layer`
- `ablation_type`

## Recommended columns

- `prompt_id`: stable prompt/example id.
- `sweep_id`: stable manifest row id for resume-safe production and duplicate
  detection.
- `split`: `screen`, `test`, or `heldout`. If any `test` rows are present, the
  analyzer uses only `test` rows for inference.
- `cluster_id`: prompt cluster for cluster bootstrap.
- `layer`: model layer or SAE hook layer.
- `hook_point`: activation hook point.
- `ablation_type`: `resample`, `mean`, or another explicit intervention name.
- `resample_source_id`: prompt id or row id supplying the replacement activation.
- `clean_label`, `patch_label`, `group`: task-specific metadata for later audits.

## Optional ground truth columns

For synthetic or semi-synthetic validation, provide a separate CSV:

- `feature_id`
- `is_active`
- `true_tau`

Then run:

```powershell
python scripts/analyze_ablation_cache.py --cache path\to\cache.csv --ground-truth path\to\truth.csv --output-dir results\cache_analysis
```

For real LLM experiments, omit `--ground-truth`; the output will contain
discoveries and CIs but no FDP or power.

## Selected feature lists

`scripts/analyze_ablation_cache.py` writes:

- `feature_stats.csv`: per-feature effect estimates, p-values, e-values, CIs,
  and method-specific `selected_*` flags.
- `method_summary.csv`: discoveries and optional FDP/power when ground truth is
  available.
- `selected_features.csv`: one wide table with all selected flags.
- `selected_features_<method>.csv`: one selected-feature list per method.

Use the method-specific file to build the next GPU sweep manifest.

## Joint circuit-level cache

After selecting features, the GPU stage should also run a held-out joint circuit
evaluation. This cache is separate from per-feature exact ablations.

Required columns:

- `prompt_id`
- `method`
- Either:
  - `full_difference`
  - `selected_difference`
- Or metrics from which they can be computed:
  - `clean_metric`
  - `patch_metric`
  - `selected_patch_metric`

Definitions:

- `full_difference = clean_metric - patch_metric`
- `selected_difference = clean_metric - selected_patch_metric`

The analyzer computes completeness, necessity, selected/full correlation, and
sign agreement:

```powershell
python scripts/analyze_circuit_cache.py --cache path\to\circuit_cache.csv --output-dir results\circuit_cache_analysis
```

For Gemma Scope runs, `scripts/produce_sae_circuit_cache.py` writes this schema
from a circuit eval manifest by simultaneously replacing all selected SAE
features on the clean prompt with the corresponding patch-prompt activations.

Generate a held-out joint-eval manifest from selected features:

```powershell
python scripts/create_circuit_eval_manifest.py --selected-features results\cache_analysis\selected_features_e_bh_pcal.csv --output data\subject_verb_agreement\circuit_eval_manifest.csv
```
