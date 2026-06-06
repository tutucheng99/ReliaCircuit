# Artifact Map

## Paper

- `paper/reliacircuit.tex`: anonymous LaTeX source.
- `paper/figures/*.pdf`: final vector figures used by the paper.
- `results/figure_drafts/`: source/previews for the custom final figures.

## CPU Statistical Layer

- `src/reliacircuit/fdr.py`: BH/BY/e-BH selection.
- `src/reliacircuit/inference.py`: confidence intervals and effect estimates.
- `src/reliacircuit/cache_analysis.py`: cache-to-selection summaries.
- `src/reliacircuit/synthetic.py`: known-ground-truth synthetic generator.

## Synthetic Results

- `results/synthetic_gate_b/`
- `results/synthetic_frontier/`
- `results/synthetic_ci_frontier/`
- `results/synthetic_debias/`

## Real Cached Results

- `results/subject_verb_agreement_balanced_l08/`
- `results/subject_verb_agreement_balanced_l12/`
- `results/subject_verb_agreement_balanced_l16/`
- `results/subject_verb_agreement_balanced/` for L20
- `results/real_subject_verb_reliability/`

## Paper Tables And Claim Ledger

- `results/paper_assets/table_*.csv`
- `results/paper_assets/table_*.md`
- `results/paper_assets/claim_evidence_matrix.*`

## GPU Recipe

- `docs/gpu_cache_generation.md`
- `requirements-gpu.txt`
- `runpod_job.sh`
- `scripts/produce_sae_screen_scores.py`
- `scripts/produce_sae_ablation_cache.py`
- `scripts/produce_sae_circuit_cache.py`
