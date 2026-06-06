# GPU Cache Generation

The paper separates cache generation from statistical analysis. The GPU stage
writes CSV caches once; every FDR, decoy, layer-scan, stability, q-grid, and
figure result is then recomputed on CPU from those caches.

## Requirements

- A GPU environment with enough memory for Gemma-2-2B and Gemma Scope SAEs.
- Access to the model and SAE releases.
- Local credentials supplied through environment variables or a local `.env`
  file based on `.env.example`.

Do not commit real credentials, SSH keys, hostnames, ports, or provider pod IDs.

## Subject-Verb Four-Layer Protocol

The fixed protocol is `configs/subject_verb_layer_scan_protocol.json`. For each
layer in `{8, 12, 16, 20}` the GPU stage produces:

- `screen_scores.csv`
- `clean_metric_cache.csv`
- `exact_ablation_cache.csv`
- `joint_circuit_cache.csv`

The checked-in public caches live under `results/subject_verb_agreement_balanced*`.

## Generic Commands

The commands below show the cache-producing sequence. Adjust output paths and
`SAE_ID` for the target layer.

```bash
python scripts/build_subject_verb_prompts.py
python scripts/produce_sae_screen_scores.py \
  --prompts data/subject_verb_agreement_balanced/prompts.csv \
  --split screen \
  --top-k 256 \
  --sae-id layer_16/width_16k/canonical \
  --output results/subject_verb_agreement_balanced_l16/screen_scores.csv \
  --features-output data/subject_verb_agreement_balanced_l16/screened_features.csv

python scripts/create_ablation_sweep_manifest.py \
  --prompts data/subject_verb_agreement_balanced/prompts.csv \
  --features data/subject_verb_agreement_balanced_l16/screened_features.csv \
  --split test \
  --output data/subject_verb_agreement_balanced_l16/ablation_manifest.csv

python scripts/produce_sae_ablation_cache.py \
  --manifest data/subject_verb_agreement_balanced_l16/ablation_manifest.csv \
  --output results/subject_verb_agreement_balanced_l16/exact_ablation_cache.csv

python scripts/analyze_ablation_cache.py \
  --cache results/subject_verb_agreement_balanced_l16/exact_ablation_cache.csv \
  --output-dir results/subject_verb_agreement_balanced_l16/cache_analysis
```

Held-out joint circuit caches are generated with
`scripts/create_circuit_eval_manifest.py` and `scripts/produce_sae_circuit_cache.py`.

## Public Data Policy

Large generated manifests can be regenerated from the prompt and screened-feature
files and are not required for CPU verification. Raw BiasInBios biography text is
excluded from the public release; the repository keeps only toy schema fixtures
and non-text summary/cache outputs for the bounded negative probe.
