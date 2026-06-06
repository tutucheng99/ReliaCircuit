# Reproducibility

## CPU Path

Install dependencies:

```bash
python -m pip install -r requirements-cpu.txt
python -m pip install -e .
```

Run tests and artifact checks:

```bash
python scripts/verify_artifacts.py
python -m pytest
```

Regenerate synthetic outputs:

```bash
python scripts/run_synthetic_gate_b.py --config configs/synthetic_gate_b.json
python scripts/run_synthetic_frontier.py --config configs/synthetic_frontier.json
python scripts/run_synthetic_frontier.py --config configs/synthetic_ci_frontier.json
python scripts/run_synthetic_debias.py --config configs/synthetic_debias.json
```

Recompute real-model statistics from checked-in caches:

```bash
python scripts/analyze_real_subject_verb_reliability.py
python scripts/draw_reliacircuit_final_figures.py
python scripts/build_paper_assets.py
```

## GPU Path

GPU cache regeneration is optional and requires model access. See
`docs/gpu_cache_generation.md`. The checked-in caches are sufficient for CPU
verification of the paper's key statistical claims.
