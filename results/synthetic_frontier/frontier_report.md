# Synthetic Frontier Report

This report extends Gate B from one synthetic setting to a compact robustness frontier.

## Scenario configuration

| scenario        | description                                                           |   synthetic.n_prompts |   synthetic.n_features |   synthetic.n_active |   synthetic.n_blocks |   synthetic.within_block_corr |   synthetic.active_mean_shift |   synthetic.null_mean_shift_sd |   synthetic.effect_size |   synthetic.nuisance_effect_sd |   synthetic.metric_noise_sd |   synthetic.cluster_size |   synthetic.seed |   pipeline.screen_fraction |   pipeline.test_fraction |   pipeline.screen_n |   pipeline.q |   pipeline.e_gamma |   pipeline.n_bootstrap |   pipeline.confidence |
|:----------------|:----------------------------------------------------------------------|----------------------:|-----------------------:|---------------------:|---------------------:|------------------------------:|------------------------------:|-------------------------------:|------------------------:|-------------------------------:|----------------------------:|-------------------------:|-----------------:|---------------------------:|-------------------------:|--------------------:|-------------:|-------------------:|-----------------------:|----------------------:|
| nominal         | Base setting matching the first Gate B run at lower bootstrap budget. |                  1000 |                    512 |                   24 |                   32 |                          0.35 |                          1.25 |                           0.15 |                    0.55 |                            0.3 |                         0.4 |                        8 |         20260601 |                        0.4 |                      0.4 |                  96 |          0.1 |                0.5 |                     99 |                  0.95 |
| high_dependence | Stronger block correlation among features.                            |                  1000 |                    512 |                   24 |                   16 |                          0.75 |                          1.25 |                           0.15 |                    0.55 |                            0.3 |                         0.4 |                        8 |         20260601 |                        0.4 |                      0.4 |                  96 |          0.1 |                0.5 |                     99 |                  0.95 |
| weak_effect     | Smaller active causal effects.                                        |                  1000 |                    512 |                   24 |                   32 |                          0.35 |                          1.25 |                           0.15 |                    0.35 |                            0.3 |                         0.4 |                        8 |         20260601 |                        0.4 |                      0.4 |                  96 |          0.1 |                0.5 |                     99 |                  0.95 |
| narrow_screen   | Lower discovery budget in Stage 1 screening.                          |                  1000 |                    512 |                   24 |                   32 |                          0.35 |                          1.25 |                           0.15 |                    0.55 |                            0.3 |                         0.4 |                        8 |         20260601 |                        0.4 |                      0.4 |                  48 |          0.1 |                0.5 |                     99 |                  0.95 |
| high_nuisance   | More prompt-level nuisance variation for null features.               |                  1000 |                    512 |                   24 |                   32 |                          0.35 |                          1.25 |                           0.15 |                    0.55 |                            0.5 |                         0.4 |                        8 |         20260601 |                        0.4 |                      0.4 |                  96 |          0.1 |                0.5 |                     99 |                  0.95 |

## Aggregate metrics

| scenario        | method             |   discoveries_mean |   fdp_mean |   power_mean |   screen_recall_mean |   ci_coverage_screened_mean |
|:----------------|:-------------------|-------------------:|-----------:|-------------:|---------------------:|----------------------------:|
| nominal         | e_bh_pcal          |            18.0625 | 0          |     0.752604 |             0.752604 |                    0.953125 |
| nominal         | by_bh              |            18.25   | 0.00939066 |     0.752604 |             0.752604 |                    0.953125 |
| nominal         | bh                 |            19.6875 | 0.0784555  |     0.752604 |             0.752604 |                    0.953125 |
| nominal         | p_lt_q             |            24.8125 | 0.265683   |     0.752604 |             0.752604 |                    0.953125 |
| nominal         | top_score_k_active |            24      | 0.554688   |     0.445312 |             0.752604 |                    0.953125 |
| high_dependence | e_bh_pcal          |             8.9375 | 0          |     0.372396 |             0.372396 |                    0.951823 |
| high_dependence | by_bh              |             9.0625 | 0.0146104  |     0.372396 |             0.372396 |                    0.951823 |
| high_dependence | bh                 |            10.1875 | 0.114693   |     0.372396 |             0.372396 |                    0.951823 |
| high_dependence | p_lt_q             |            17.3125 | 0.473468   |     0.372396 |             0.372396 |                    0.951823 |
| high_dependence | top_score_k_active |            24      | 0.869792   |     0.130208 |             0.372396 |                    0.951823 |
| weak_effect     | e_bh_pcal          |            18.125  | 0          |     0.755208 |             0.755208 |                    0.953776 |
| weak_effect     | by_bh              |            18.4375 | 0.0156407  |     0.755208 |             0.755208 |                    0.953776 |
| weak_effect     | bh                 |            19.625  | 0.0715875  |     0.755208 |             0.755208 |                    0.953776 |
| weak_effect     | p_lt_q             |            26      | 0.298103   |     0.755208 |             0.755208 |                    0.953776 |
| weak_effect     | top_score_k_active |            24      | 0.567708   |     0.432292 |             0.755208 |                    0.953776 |
| narrow_screen   | e_bh_pcal          |            14.25   | 0          |     0.59375  |             0.59375  |                    0.955729 |
| narrow_screen   | by_bh              |            14.3125 | 0.00390625 |     0.59375  |             0.59375  |                    0.955729 |
| narrow_screen   | bh                 |            15.625  | 0.0840622  |     0.59375  |             0.59375  |                    0.955729 |
| narrow_screen   | p_lt_q             |            17.375  | 0.171685   |     0.59375  |             0.59375  |                    0.955729 |
| narrow_screen   | top_score_k_active |            24      | 0.554688   |     0.445312 |             0.59375  |                    0.955729 |
| high_nuisance   | e_bh_pcal          |            18.0625 | 0          |     0.752604 |             0.752604 |                    0.954427 |
| high_nuisance   | by_bh              |            18.25   | 0.00939066 |     0.752604 |             0.752604 |                    0.954427 |
| high_nuisance   | bh                 |            19.6875 | 0.0784555  |     0.752604 |             0.752604 |                    0.954427 |
| high_nuisance   | p_lt_q             |            24.8125 | 0.265683   |     0.752604 |             0.752604 |                    0.954427 |
| high_nuisance   | top_score_k_active |            24      | 0.554688   |     0.445312 |             0.752604 |                    0.954427 |

## Held-out circuit metrics

| scenario        | method             |   replicates |   completeness_r2_mean |   completeness_r2_se |   necessity_fraction_mean |   necessity_fraction_se |   abs_effect_fraction_mean |   abs_effect_fraction_se |   selected_full_corr_mean |   selected_full_corr_se |   sign_agreement_mean |   sign_agreement_se |
|:----------------|:-------------------|-------------:|-----------------------:|---------------------:|--------------------------:|------------------------:|---------------------------:|-------------------------:|--------------------------:|------------------------:|----------------------:|--------------------:|
| nominal         | e_bh_pcal          |           16 |               0.754716 |            0.0335301 |                  0.965787 |               0.0745604 |                   0.976891 |                0.0420406 |                  0.883999 |              0.00851105 |              0.855625 |           0.0160914 |
| nominal         | by_bh              |           16 |               0.754716 |            0.0335301 |                  0.965787 |               0.0745604 |                   0.976891 |                0.0420406 |                  0.883999 |              0.00851105 |              0.855625 |           0.0160914 |
| nominal         | bh                 |           16 |               0.754716 |            0.0335301 |                  0.965787 |               0.0745604 |                   0.976891 |                0.0420406 |                  0.883999 |              0.00851105 |              0.855625 |           0.0160914 |
| nominal         | p_lt_q             |           16 |               0.754716 |            0.0335301 |                  0.965787 |               0.0745604 |                   0.976891 |                0.0420406 |                  0.883999 |              0.00851105 |              0.855625 |           0.0160914 |
| nominal         | top_score_k_active |           16 |               0.445797 |            0.0681011 |                  0.770823 |               0.104738  |                   0.864451 |                0.0706059 |                  0.719849 |              0.0182     |              0.759375 |           0.0261441 |
| high_dependence | e_bh_pcal          |           16 |               0.639725 |            0.0415727 |                  0.765251 |               0.0722746 |                   0.872597 |                0.0459426 |                  0.794497 |              0.0127922  |              0.807813 |           0.0191484 |
| high_dependence | by_bh              |           16 |               0.639725 |            0.0415727 |                  0.765251 |               0.0722746 |                   0.872597 |                0.0459426 |                  0.794497 |              0.0127922  |              0.807813 |           0.0191484 |
| high_dependence | bh                 |           16 |               0.639725 |            0.0415727 |                  0.765251 |               0.0722746 |                   0.872597 |                0.0459426 |                  0.794497 |              0.0127922  |              0.807813 |           0.0191484 |
| high_dependence | p_lt_q             |           16 |               0.639725 |            0.0415727 |                  0.765251 |               0.0722746 |                   0.872597 |                0.0459426 |                  0.794497 |              0.0127922  |              0.807813 |           0.0191484 |
| high_dependence | top_score_k_active |           16 |               0.278595 |            0.0827388 |                  0.420698 |               0.0609429 |                   0.635787 |                0.0521044 |                  0.570972 |              0.0298847  |              0.698125 |           0.0399423 |
| weak_effect     | e_bh_pcal          |           16 |               0.73219  |            0.0474974 |                  0.972557 |               0.0668432 |                   0.980248 |                0.0378024 |                  0.885404 |              0.00877004 |              0.846875 |           0.0205136 |
| weak_effect     | by_bh              |           16 |               0.73219  |            0.0474974 |                  0.972557 |               0.0668432 |                   0.980248 |                0.0378024 |                  0.885404 |              0.00877004 |              0.846875 |           0.0205136 |
| weak_effect     | bh                 |           16 |               0.73219  |            0.0474974 |                  0.972557 |               0.0668432 |                   0.980248 |                0.0378024 |                  0.885404 |              0.00877004 |              0.846875 |           0.0205136 |
| weak_effect     | p_lt_q             |           16 |               0.73219  |            0.0474974 |                  0.972557 |               0.0668432 |                   0.980248 |                0.0378024 |                  0.885404 |              0.00877004 |              0.846875 |           0.0205136 |
| weak_effect     | top_score_k_active |           16 |               0.419501 |            0.0747989 |                  0.72415  |               0.0947714 |                   0.836854 |                0.0632098 |                  0.710697 |              0.0184714  |              0.742813 |           0.0304855 |
| narrow_screen   | e_bh_pcal          |           16 |               0.652147 |            0.0323267 |                  0.893337 |               0.107247  |                   0.934306 |                0.0625901 |                  0.802401 |              0.0138151  |              0.829375 |           0.0146407 |
| narrow_screen   | by_bh              |           16 |               0.652147 |            0.0323267 |                  0.893337 |               0.107247  |                   0.934306 |                0.0625901 |                  0.802401 |              0.0138151  |              0.829375 |           0.0146407 |
| narrow_screen   | bh                 |           16 |               0.652147 |            0.0323267 |                  0.893337 |               0.107247  |                   0.934306 |                0.0625901 |                  0.802401 |              0.0138151  |              0.829375 |           0.0146407 |
| narrow_screen   | p_lt_q             |           16 |               0.652147 |            0.0323267 |                  0.893337 |               0.107247  |                   0.934306 |                0.0625901 |                  0.802401 |              0.0138151  |              0.829375 |           0.0146407 |
| narrow_screen   | top_score_k_active |           16 |               0.445797 |            0.0681011 |                  0.770823 |               0.104738  |                   0.864451 |                0.0706059 |                  0.719849 |              0.0182     |              0.759375 |           0.0261441 |
| high_nuisance   | e_bh_pcal          |           16 |               0.754716 |            0.0335301 |                  0.965787 |               0.0745604 |                   0.976891 |                0.0420406 |                  0.883999 |              0.00851105 |              0.855625 |           0.0160914 |
| high_nuisance   | by_bh              |           16 |               0.754716 |            0.0335301 |                  0.965787 |               0.0745604 |                   0.976891 |                0.0420406 |                  0.883999 |              0.00851105 |              0.855625 |           0.0160914 |
| high_nuisance   | bh                 |           16 |               0.754716 |            0.0335301 |                  0.965787 |               0.0745604 |                   0.976891 |                0.0420406 |                  0.883999 |              0.00851105 |              0.855625 |           0.0160914 |
| high_nuisance   | p_lt_q             |           16 |               0.754716 |            0.0335301 |                  0.965787 |               0.0745604 |                   0.976891 |                0.0420406 |                  0.883999 |              0.00851105 |              0.855625 |           0.0160914 |
| high_nuisance   | top_score_k_active |           16 |               0.445797 |            0.0681011 |                  0.770823 |               0.104738  |                   0.864451 |                0.0706059 |                  0.719849 |              0.0182     |              0.759375 |           0.0261441 |

## Raw configuration

```json
{
  "replicates": 16,
  "output_dir": "results/synthetic_frontier",
  "base_pipeline": {
    "screen_fraction": 0.4,
    "test_fraction": 0.4,
    "screen_n": 96,
    "q": 0.1,
    "e_gamma": 0.5,
    "n_bootstrap": 99,
    "confidence": 0.95
  },
  "base_synthetic": {
    "n_prompts": 1000,
    "n_features": 512,
    "n_active": 24,
    "n_blocks": 32,
    "within_block_corr": 0.35,
    "active_mean_shift": 1.25,
    "null_mean_shift_sd": 0.15,
    "effect_size": 0.55,
    "nuisance_effect_sd": 0.3,
    "metric_noise_sd": 0.4,
    "cluster_size": 8,
    "seed": 20260601
  },
  "scenarios": [
    {
      "name": "nominal",
      "description": "Base setting matching the first Gate B run at lower bootstrap budget.",
      "synthetic": {},
      "pipeline": {}
    },
    {
      "name": "high_dependence",
      "description": "Stronger block correlation among features.",
      "synthetic": {
        "within_block_corr": 0.75,
        "n_blocks": 16
      },
      "pipeline": {}
    },
    {
      "name": "weak_effect",
      "description": "Smaller active causal effects.",
      "synthetic": {
        "effect_size": 0.35
      },
      "pipeline": {}
    },
    {
      "name": "narrow_screen",
      "description": "Lower discovery budget in Stage 1 screening.",
      "synthetic": {},
      "pipeline": {
        "screen_n": 48
      }
    },
    {
      "name": "high_nuisance",
      "description": "More prompt-level nuisance variation for null features.",
      "synthetic": {
        "nuisance_effect_sd": 0.5
      },
      "pipeline": {}
    }
  ]
}
```
