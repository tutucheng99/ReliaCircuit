# Method Specification, Complexity, and Hyperparameters

This document is the reproducibility-facing specification for the current
ReliaCircuit artifacts. It consolidates algorithm steps, input/output contracts,
complexity, and final hyperparameter values from the code and config files.

## 1. Core Procedure

Inputs:

- prompt table with `prompt_id`, split label, clean prompt, patch prompt, and
  behavior target columns when applicable;
- candidate SAE feature universe or an explicit feature manifest;
- scalar behavior metric `m(x)`;
- ablation intervention type, currently `resample` or `zero`;
- FDR level `q`, p-to-e calibrator `gamma`, and bootstrap settings.

Outputs:

- screened feature table with cheap screen scores;
- exact-ablation cache with one row per prompt-feature intervention;
- per-feature statistics with effect estimates, p-values, e-values, and CIs;
- selected-feature tables for each discovery method;
- held-out joint circuit metrics;
- downstream debiasing metrics when a prediction cache is available.

Algorithm:

```text
1. Split prompts into screen A, test B, and held-out C.
2. Score candidate features on A using a cheap attribution/activation proxy.
3. Keep top screen_n features.
4. On B, run exact paired ablations for screened features.
5. Estimate tau_f = mean(clean_metric - ablated_metric).
6. Compute paired t p-values and bootstrap-t CIs.
7. Convert p-values to e-values with e(p) = (1 - gamma) p^(-gamma).
8. Select features with e-BH at q; report BY-BH, BH, p-value, and top-score
   baselines.
9. On held-out C, evaluate the selected set jointly as a circuit.
10. For debiasing, remove selected task-irrelevant features and evaluate
    worst-group accuracy plus erroneous-removal rate.
```

Formal estimands and claims are in `docs/statistical_claims.md`.

## 2. Complexity

Notation:

- `n`: total prompt units.
- `n_A`, `n_B`, `n_C`: screen, test, and held-out prompt counts.
- `m`: candidate feature count before screening.
- `s`: screened feature count.
- `k`: selected feature count.
- `b`: bootstrap resample count.
- `r`: repeated synthetic replicates.
- `g`: number of discovery methods evaluated.

CPU synthetic screen:

```text
time  O(r * n_A * m)
space O(n_A * m) for generated feature matrices in the synthetic benchmark
```

Exact test-stage ablation:

```text
time  O(n_B * s) model interventions or synthetic paired differences
space O(n_B * s) cache rows
```

The real LLM constant factor is one forward/intervention path per cache row,
with batching determined by GPU memory and SAE implementation. The CPU-side
statistics are intentionally separated so the expensive GPU phase writes caches
once and then exits.

Per-feature inference:

```text
time  O(s * (n_B + b * n_B)) for paired tests and bootstrap-t intervals
space O(n_B) per feature, O(s) for summary tables
```

FDR correction:

```text
time  O(s log s) for BH/BY/e-BH sorting
space O(s)
```

Held-out circuit evaluation:

```text
time  O(n_C * g) when selected sets are evaluated jointly by method
space O(n_C * g) cache rows
```

Downstream prediction-cache evaluation:

```text
time  O(n_examples * n_methods * n_labels) for cached label scoring
space O(n_examples * n_methods) prediction rows
```

## 3. Final Local Hyperparameters

### Gate B synthetic validation

Source: `configs/synthetic_gate_b.json`.

| Parameter | Value |
|---|---:|
| Replicates | 40 |
| Prompts | 1200 |
| Candidate features | 512 |
| Active features | 24 |
| Feature blocks | 32 |
| Within-block correlation | 0.35 |
| Screen/test/held-out fractions | 0.4 / 0.4 / 0.2 |
| Screened features | 96 |
| FDR level q | 0.1 |
| p-to-e gamma | 0.5 |
| Bootstrap resamples | 299 |
| Confidence level | 0.95 |
| Cluster size | 8 |
| Seed | 20260531 |

### Synthetic robustness frontier

Source: `configs/synthetic_frontier.json`.

| Parameter | Value |
|---|---:|
| Replicates per scenario | 16 |
| Base prompts | 1000 |
| Base candidate features | 512 |
| Base active features | 24 |
| Base screened features | 96 |
| FDR level q | 0.1 |
| p-to-e gamma | 0.5 |
| Bootstrap resamples | 99 |
| Scenarios | nominal, high_dependence, weak_effect, narrow_screen, high_nuisance |

Scenario changes:

- `high_dependence`: within-block correlation 0.75, feature blocks 16.
- `weak_effect`: active effect size 0.35.
- `narrow_screen`: screened features 48.
- `high_nuisance`: nuisance effect standard deviation 0.5.

### Synthetic CI frontier

Source: `configs/synthetic_ci_frontier.json`.

| Parameter | Value |
|---|---:|
| Replicates per scenario | 12 |
| Base prompts | 1000 |
| Base screened features | 96 |
| FDR level q | 0.1 |
| p-to-e gamma | 0.5 |
| Bootstrap resamples | 149 |
| Confidence level | 0.95 |
| Scenarios | n600, n1000, n1600, test20, test50 |

Scenario changes:

- `n600`: 600 prompts.
- `n1600`: 1600 prompts.
- `test20`: screen/test/held-out fractions 0.5 / 0.2 / 0.3.
- `test50`: screen/test/held-out fractions 0.3 / 0.5 / 0.2.

### Synthetic downstream debiasing

Source: `configs/synthetic_debias.json`.

| Parameter | Value |
|---|---:|
| Replicates | 40 |
| Train/test examples | 1600 / 1600 |
| Features | 256 |
| Task/spurious/proxy features | 24 / 24 / 24 |
| Feature blocks | 32 |
| Within-block correlation | 0.25 |
| Train alignment probability | 0.9 |
| Test alignment probability | 0.5 |
| Screen/test/held-out fractions | 0.4 / 0.4 / 0.2 |
| FDR level q | 0.1 |
| p-to-e gamma | 0.5 |
| Seed | 20260620 |

### BiasInBios preparation

Source: `configs/bias_in_bios.json`.

| Parameter | Value |
|---|---|
| Dataset | `LabHC/bias_in_bios` |
| Text column | `hard_text` |
| Profession column | `profession` |
| Protected column | `gender` |
| Splits | train, dev, test |
| Default bounded real rows | 60 |
| Retained toy dry-run rows | 4 in `data/bias_in_bios/dry_run.csv` |
| Profession labels | 28 |

### GPU/Gemma Scope defaults

Sources: GPU producer scripts and `docs/gpu_smoke_workflow.md`.

| Parameter | Default |
|---|---|
| Model id | `gemma-2-2b` in scripts; 9B is the intended full anchor when GPU access allows |
| SAE release | `gemma-scope-2b-pt-res-canonical` |
| SAE id | `layer_20/width_16k/canonical` |
| Screen top-k | 96 |
| Screen score mode | `metric_weighted_delta` for subject-verb; `activation_delta` for BiasInBios pairs |
| Exact metric mode | `token_logit_diff` for subject-verb; `label_logprob` for BiasInBios occupation labels |
| Ablation type | `resample` |
| Sequence position | `last` for subject-verb and BiasInBios pair ablation; `prompt_last` for BiasInBios prediction |
| Device/dtype | auto |
| Exact-ablation flush interval | 25 prompt groups |
| Prediction-cache flush interval | 25 rows |

Dry-run outputs validate schema only. They are not evidence about real
Gemma/Gemma Scope behavior.

## 4. Method Defaults and Baselines

Discovery methods:

- `e_bh_pcal`: p-to-e calibrated e-values plus e-BH. This is the primary
  method for dependent SAE features.
- `by_bh`: Benjamini-Yekutieli correction as an arbitrary-dependence p-value
  sanity baseline.
- `bh`: ordinary Benjamini-Hochberg, included to expose dependence sensitivity.
- `p_lt_q`: uncorrected p-value thresholding, included as a failure baseline.
- `top_score_k_active` or `top_score_k_spurious`: score-threshold baseline with
  an oracle-sized budget in synthetic settings.
- `random_k_spurious`: random removal baseline for synthetic debiasing.

Reported metrics:

- Synthetic discovery: FDP, power, discoveries, screen recall, CI coverage.
- Held-out circuit: uncentered completeness R2, necessity fraction,
  selected/full Pearson correlation, sign agreement. Completeness R2 is an
  amplitude-reconstruction ratio; selected/full correlation must be reported
  beside it when discussing prompt-level variation.
- Downstream debiasing: overall accuracy, worst-group accuracy, conflict
  accuracy, spurious recall, erroneous-removal rate.
- GPU cache validation: schema validity, row counts, required metadata presence.

## 5. Compute Contract

The intended compute separation is:

- local CPU: synthetic benchmarks, statistical post-processing, q-grid analysis,
  paper tables, artifact verification;
- GPU pod: model/SAE loading, screen-score forward passes, exact per-feature
  ablation cache production, held-out joint circuit cache production, and
  BiasInBios prediction-cache production;
- local CPU after GPU: output validation, FDR/CI analysis, circuit metrics, and
  downstream summaries.

This separation is enforced by the cache format in `docs/cache_schema.md` and
the post-run wrapper `scripts/run_gpu_postprocessing.py`.
