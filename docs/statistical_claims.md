# Statistical Claims and Method Specification

This document records the formal statistical target for ReliaCircuit. It is a
paper-writing support artifact, not paper prose. The intent is to make every
reliability claim traceable to an estimand, an algorithm step, an assumption, and
a local implementation file.

## 1. Estimands

Let `x` be a prompt or prompt cluster drawn from the evaluation population, and
let `m(x)` be a scalar behavior metric such as a target-vs-counter token logit
difference or a true-label occupation log-probability. For SAE feature `f`,
define the ablated metric under a fixed
intervention distribution `Q_f` as:

```text
m_f^abl(x) = m(x; do(a_f <- a_tilde_f)),  a_tilde_f ~ Q_f
```

The primary per-feature effect is the paired resample-ablation ATE:

```text
tau_f = E_x,E_Q [ m(x) - m_f^abl(x) ].
```

In finite synthetic runs the code also records the finite-test-split and
population ground-truth effects when known. The null hypothesis tested for
feature discovery is:

```text
H0_f: tau_f = 0
```

with two-sided paired tests. The causal interpretation is only for the specified
ablation intervention. Changing from resample or mean ablation to zero ablation
changes the estimand.

## 2. Algorithm Contract

1. Randomly split prompt units into screen split `A`, test split `B`, and
   held-out circuit split `C`.
2. On `A`, compute a cheap attribution-patching score for the full candidate
   feature universe and keep the top `N` features. This stage controls compute
   only; it does not make inferential claims.
3. On independent split `B`, run exact paired ablations only for the screened
   features. For each screened feature, compute paired differences
   `D_if = m(x_i) - m_f^abl(x_i)`.
4. Estimate `tau_f` by the mean paired difference. Compute a paired t p-value
   and a bootstrap-t confidence interval, using cluster bootstrap when
   `cluster_id` is present.
5. Convert valid p-values to e-values with the power calibrator
   `e(p) = (1 - gamma) p^(-gamma)` for `0 < gamma < 1`.
6. Select discoveries with e-BH at target FDR level `q`. BY-BH, ordinary BH,
   uncorrected p-value thresholding, and top-score thresholding are baselines.
7. On held-out split `C`, evaluate the selected node set as a circuit using
   completeness, necessity, selected/full correlation, and sign agreement.

Implementation hooks:

- `src/reliacircuit/pipeline.py`: synthetic split, screen, test, and held-out
  circuit summaries.
- `src/reliacircuit/inference.py`: paired t p-values and bootstrap-t intervals.
- `src/reliacircuit/fdr.py`: BH, BY-BH, p-to-e calibration, and e-BH.
- `src/reliacircuit/cache_analysis.py`: the same inference layer for returned
  GPU exact-ablation caches.

## 3. Assumptions

A1. Split independence. The screen split is independent of the test and held-out
splits. The screened feature set is a measurable function of split `A` only.

A2. Unit sampling. Test units are iid or can be treated as independent clusters.
When prompts are clustered, cluster ids define the bootstrap resampling units.

A3. Valid test p-values. For a true null feature and conditional on the screened
set, the test-split p-value is superuniform:

```text
Pr(p_f <= u | S(A)) <= u,  0 <= u <= 1.
```

This is exact for ideal tests and approximate for finite-sample paired t tests.
The synthetic benchmark directly audits the resulting FDP and CI coverage.

A4. Valid p-to-e calibration. If A3 holds and `0 < gamma < 1`, then
`e(p) = (1 - gamma) p^(-gamma)` is a valid e-value for each true null:

```text
E[e(p_f) | H0_f, S(A)] <= 1.
```

A5. Feature dependence is unrestricted after e-value validity. SAE features may
be strongly dependent and may share prompts, activations, and ablation noise.
The e-BH reduction only requires valid null e-values.

A6. Bootstrap-t intervals are conditional marginal intervals. They target
per-feature coverage conditional on the independent test split and standard
bootstrap regularity conditions. They are not simultaneous familywise intervals.

A7. Held-out circuit metrics are descriptive evaluation metrics unless a
separate resampling procedure is applied to them. They do not by themselves
establish FDR control.

## 4. Formal Claims

### Claim 1: Split-B Effect Estimates Are Selection-Free

Conditional on the screen split and selected candidate set `S(A)`, split `B` is
independent of the selection event. For any tested feature `f in S(A)`, if the
ablation sampler used in testing matches the estimand distribution `Q_f`, then:

```text
E[tau_hat_f | S(A)] = tau_f.
```

Sketch: conditional on `S(A)`, the feature identity is fixed before observing
test differences. The paired differences on split `B` are fresh draws from the
target difference distribution, so the sample mean has expectation `tau_f`.

### Claim 2: P-to-E Calibration Preserves Null Validity

For a true null feature with superuniform p-value, the power calibrator produces
a valid null e-value:

```text
E[(1 - gamma) p_f^(-gamma)] <= integral_0^1 (1 - gamma) u^(-gamma) du = 1.
```

Sketch: the inequality follows from p-value superuniformity; equality holds for
an exact Uniform(0, 1) null p-value.

### Claim 3: e-BH Controls FDR for Reported Features

Conditional on the screened family `S(A)`, if every true null feature in the
screened family has a valid e-value, e-BH at level `q` controls FDR under
arbitrary dependence among the screened e-values:

```text
E[FDP | S(A)] <= q.
```

Taking expectation over the random screen split gives unconditional FDR control
for the final reported discoveries. The reduction is exactly to the standard
e-BH theorem; the contribution here is making the SAE circuit-discovery pipeline
produce independent test-split p/e-values to which that theorem applies.

### Claim 4: Post-Selection CIs Are Valid as Marginal Feature Intervals

Because feature selection is performed on split `A` and interval construction is
performed on independent split `B`, the usual bootstrap-t interval for each
tested feature remains a conditional marginal interval after screening. For a
selected feature `f`, under A1, A2, and A6:

```text
Pr(tau_f in CI_f | f in S(A)) ~= 1 - alpha.
```

The current artifacts report empirical screened-feature and selected-feature
coverage in synthetic environments where `tau_f` is known. They do not claim
simultaneous coverage for all selected intervals.

### Claim 5: Circuit Metrics Evaluate Set-Level Faithfulness, Not Discovery
Error

After FDR-controlled node selection, held-out circuit metrics evaluate whether
the selected node set reproduces the full known behavior on fresh prompts:

```text
completeness_r2 = 1 - mean((full_difference - selected_difference)^2)
                    / mean(full_difference^2)
necessity_fraction = mean(selected_difference^2) / mean(full_difference^2)
```

`completeness_r2` is an uncentered amplitude-reconstruction ratio, not a
centered regression goodness-of-fit statistic. It can be positive when the
selected circuit reproduces the overall effect scale but fails to track
prompt-to-prompt variation. For that reason, real LLM circuit results must also
report `selected_full_corr`. In the current subject-verb run,
`completeness_r2=0.5031` but `selected_full_corr=0.0559`, so the correct
interpretation is that the selected set captures part of the behavior magnitude,
not that it explains half of the centered prompt-level variance.

These metrics answer whether the selected sparse set behaves like a useful
circuit. They complement but do not replace per-feature FDR analysis.

## 5. Non-Claims and Review-Sensitive Caveats

- FDR control does not guarantee high recall. The screen can miss true active
  features; this is why power and screen recall are reported separately.
- The e-BH guarantee is only as good as null e-value validity. In real LLM/SAE
  runs without ground truth, this is an assumption supported by design and
  checked indirectly through synthetic calibration.
- The top-score and uncorrected p-value baselines are intentionally included
  because they can produce visually plausible circuits while failing false
  discovery control.
- Dry-run GPU artifacts validate schemas and CPU post-processing only. They are
  not evidence about real Gemma/SAE behavior.
- Zero ablation, mean ablation, and resample ablation are different
  interventions. Results should be labeled by ablation type rather than treated
  as one universal feature effect.

## 6. Evidence Links

- Gate B FDR, power, and CI coverage:
  `results/synthetic_gate_b/aggregate_metrics.csv`.
- Q-grid FDR sensitivity:
  `results/synthetic_gate_b/q_grid_metrics.csv`.
- Robustness and sample-size frontiers:
  `results/synthetic_frontier/aggregate_metrics.csv` and
  `results/synthetic_ci_frontier/aggregate_metrics.csv`.
- Held-out circuit metrics:
  `results/synthetic_gate_b/circuit_aggregate_metrics.csv`.
- Downstream debiasing and erroneous-removal analysis:
  `results/synthetic_debias/aggregate_eval.csv`.
- Paper-ready summaries:
  `results/paper_assets/table_*.md`.
