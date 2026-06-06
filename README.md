# ReliaCircuit

Anonymous public artifact for the paper "Reliable Sparse Circuit Mining:
False Discovery Rate Control and Valid Post-Selection Inference for Language
Model Behavior."

This repository is in triple-blind review mode. Author identities, affiliations,
emails, account names, and the final camera-ready citation are intentionally
withheld until the review process permits disclosure.

## What Is Included

- `src/reliacircuit/`: reusable CPU statistical layer for FDR control,
  post-selection inference, cache analysis, synthetic benchmarks, and debiasing
  utilities.
- `scripts/`: reproducible experiment, analysis, figure, and verification entry
  points.
- `configs/`: fixed experiment configurations, including the pre-registered
  four-layer subject-verb protocol.
- `results/`: paper-supporting tables, figures, synthetic outputs, reviewer-gap
  analyses, and four cached real-model exact-ablation tables.
- `paper/`: anonymous LaTeX source and figures for the submitted paper.
- `data/`: lightweight public inputs and feature manifests. Full raw
  biographies and pod-return staging files are intentionally not included.

## Install

```bash
python -m pip install -r requirements-cpu.txt
python -m pip install -e .
```

The CPU path does not require a GPU or model download.

## Verify The Artifact

```bash
python scripts/verify_artifacts.py
python -m pytest
```

The verifier checks required paper artifacts, cached row counts, GitHub file
size limits, and the public-release sensitivity gate.

## CPU Reproduction

The paper's statistical results are reproducible from checked-in CSV caches:

```bash
python scripts/run_synthetic_gate_b.py --config configs/synthetic_gate_b.json
python scripts/run_synthetic_frontier.py --config configs/synthetic_frontier.json
python scripts/run_synthetic_frontier.py --config configs/synthetic_ci_frontier.json
python scripts/run_synthetic_debias.py --config configs/synthetic_debias.json
python scripts/analyze_real_subject_verb_reliability.py
python scripts/draw_reliacircuit_final_figures.py
python scripts/verify_artifacts.py
```

The four real-model exact-ablation caches are under:

- `results/subject_verb_agreement_balanced_l08/`
- `results/subject_verb_agreement_balanced_l12/`
- `results/subject_verb_agreement_balanced_l16/`
- `results/subject_verb_agreement_balanced/` for L20

These caches drive the decoy stress test, layer scan, q-grid, stability checks,
and final figures without any GPU access.

## GPU Stage

The GPU stage generates screen-score, exact-ablation, and held-out circuit
caches for Gemma-2-2B / Gemma Scope. It requires restricted model access,
substantial GPU memory, and local credentials supplied by the user. The public
repository includes the scripts and a generic job wrapper, but not any host,
pod, SSH, token, or returned-output staging logs.

See `docs/gpu_cache_generation.md` for the cache-generation recipe and
`.env.example` for placeholder environment variables.

## Data Scope

The public repository includes synthetic data, subject-verb prompt/feature
manifests, real-model cached effects, and summary tables. It excludes:

- raw BiasInBios biography text and derived prompt manifests containing personal
  contact details,
- local credential files and SSH keys,
- RunPod hostnames, ports, pod IDs, command logs, and returned-output staging
  directories,
- generated zip bundles and local test caches.

The bounded BiasInBios probe is represented by non-text cached/statistical
outputs and the paper table `results/paper_assets/table_8_bounded_bias_probe.*`.

## Citation

Use `CITATION.cff` during triple-blind review. The anonymous placeholder will be
replaced with the formal author list after camera-ready disclosure is allowed.
