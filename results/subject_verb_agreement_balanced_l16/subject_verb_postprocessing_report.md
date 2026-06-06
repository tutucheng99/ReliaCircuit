# Subject-Verb Real Run Postprocessing

## FDR Selection
| method    |   q |   discoveries |
|:----------|----:|--------------:|
| e_bh_pcal | 0.1 |            23 |
| by_bh     | 0.1 |            37 |
| bh        | 0.1 |            51 |
| p_lt_q    | 0.1 |            90 |

## Tracking-Aware FDR Selection
| method    |   q |   discoveries |
|:----------|----:|--------------:|
| e_bh_pcal | 0.1 |             1 |
| by_bh     | 0.1 |             2 |
| bh        | 0.1 |            11 |
| p_lt_q    | 0.1 |            60 |

## Top-Score Baselines
| selection_method      | reference_method   |   k | path                                                                                                   |
|:----------------------|:-------------------|----:|:-------------------------------------------------------------------------------------------------------|
| top_score_k_e_bh_pcal | e_bh_pcal          |  23 | results/subject_verb_agreement_balanced_l16/cache_analysis/selected_features_top_score_k_e_bh_pcal.csv |
| top_score_k_by_bh     | by_bh              |  37 | results/subject_verb_agreement_balanced_l16/cache_analysis/selected_features_top_score_k_by_bh.csv     |
| top_score_k_bh        | bh                 |  51 | results/subject_verb_agreement_balanced_l16/cache_analysis/selected_features_top_score_k_bh.csv        |
| top_score_k_p_lt_q    | p_lt_q             |  90 | results/subject_verb_agreement_balanced_l16/cache_analysis/selected_features_top_score_k_p_lt_q.csv    |
| top_score_k_256       | fixed_top_k        | 256 | results/subject_verb_agreement_balanced_l16/cache_analysis/selected_features_top_score_k_256.csv       |

## Tracking-Matched Top-Score Baselines
| selection_method            | reference_method   |   k | path                                                                                                         |
|:----------------------------|:-------------------|----:|:-------------------------------------------------------------------------------------------------------------|
| top_score_k_track_e_bh_pcal | e_bh_pcal          |   1 | results/subject_verb_agreement_balanced_l16/cache_analysis/selected_features_top_score_k_track_e_bh_pcal.csv |
| top_score_k_track_by_bh     | by_bh              |   2 | results/subject_verb_agreement_balanced_l16/cache_analysis/selected_features_top_score_k_track_by_bh.csv     |
| top_score_k_track_bh        | bh                 |  11 | results/subject_verb_agreement_balanced_l16/cache_analysis/selected_features_top_score_k_track_bh.csv        |
| top_score_k_track_p_lt_q    | p_lt_q             |  60 | results/subject_verb_agreement_balanced_l16/cache_analysis/selected_features_top_score_k_track_p_lt_q.csv    |

## Circuit Manifest

- path: `data/subject_verb_agreement_balanced_l16/circuit_eval_manifest.csv`
- rows: `2720`
- methods: `e_bh_pcal, by_bh, bh, p_lt_q, track_e_bh_pcal, track_by_bh, track_bh, track_p_lt_q, top_score_k_e_bh_pcal, top_score_k_by_bh, top_score_k_bh, top_score_k_p_lt_q, top_score_k_256, top_score_k_track_e_bh_pcal, top_score_k_track_by_bh, top_score_k_track_bh, top_score_k_track_p_lt_q`

## Held-Out Joint Circuit Tracking
| method                      |   heldout_n |   heldout_full_mse |   heldout_residual_mse |   heldout_selected_mse |   completeness_r2 |   centered_r2 |   necessity_fraction |   abs_effect_fraction |   selected_full_corr |   sign_agreement |
|:----------------------------|------------:|-------------------:|-----------------------:|-----------------------:|------------------:|--------------:|---------------------:|----------------------:|---------------------:|-----------------:|
| e_bh_pcal                   |         160 |            34.3411 |                1.26304 |              31.0376   |          0.963221 |     0.58423   |            0.903805  |              0.958715 |             0.780224 |          1       |
| by_bh                       |         160 |            34.3411 |                1.3029  |              31.4455   |          0.96206  |     0.57111   |            0.915683  |              0.964109 |             0.771956 |          1       |
| bh                          |         160 |            34.3411 |                1.1992  |              31.9403   |          0.96508  |     0.605245  |            0.93009   |              0.972572 |             0.787874 |          1       |
| p_lt_q                      |         160 |            34.3411 |                1.14921 |              31.3088   |          0.966535 |     0.621701  |            0.911703  |              0.960768 |             0.803314 |          1       |
| track_e_bh_pcal             |         160 |            34.3411 |               14.6999  |               5.23796  |          0.571944 |    -3.83893   |            0.152528  |              0.366182 |             0.549454 |          1       |
| track_by_bh                 |         160 |            34.3411 |                3.31787 |              19.8759   |          0.903385 |    -0.0921835 |            0.578779  |              0.748099 |             0.75925  |          1       |
| track_bh                    |         160 |            34.3411 |                1.33132 |              30.1038   |          0.961232 |     0.561755  |            0.876613  |              0.937718 |             0.787213 |          1       |
| track_p_lt_q                |         160 |            34.3411 |                1.14143 |              33.6434   |          0.966762 |     0.624264  |            0.979686  |              0.990437 |             0.809529 |          1       |
| top_score_k_e_bh_pcal       |         160 |            34.3411 |                1.22053 |              29.628    |          0.964459 |     0.598225  |            0.862758  |              0.93242  |             0.807632 |          1       |
| top_score_k_by_bh           |         160 |            34.3411 |                1.23086 |              29.5376   |          0.964158 |     0.594825  |            0.860124  |              0.932135 |             0.80472  |          1       |
| top_score_k_bh              |         160 |            34.3411 |                1.31341 |              29.2973   |          0.961754 |     0.56765   |            0.853127  |              0.92476  |             0.799208 |          1       |
| top_score_k_p_lt_q          |         160 |            34.3411 |                1.16793 |              31.4844   |          0.96599  |     0.615538  |            0.916816  |              0.96232  |             0.800822 |          1       |
| top_score_k_256             |         160 |            34.3411 |                1.23086 |              34.4316   |          0.964158 |     0.594825  |            1.00264   |              1.00464  |             0.791069 |          1       |
| top_score_k_track_e_bh_pcal |         160 |            34.3411 |               27.7139  |               0.661521 |          0.19298  |    -8.12291   |            0.0192633 |              0.112073 |             0.210434 |          0.94375 |
| top_score_k_track_by_bh     |         160 |            34.3411 |               20.746   |               2.50661  |          0.395883 |    -5.82921   |            0.0729916 |              0.248121 |             0.23679  |          0.98125 |
| top_score_k_track_bh        |         160 |            34.3411 |                1.466   |              27.6568   |          0.957311 |     0.51742   |            0.805356  |              0.898546 |             0.79482  |          1       |
| top_score_k_track_p_lt_q    |         160 |            34.3411 |                1.33257 |              29.4833   |          0.961196 |     0.561341  |            0.858545  |              0.927078 |             0.795048 |          1       |

## Reliability And Tracking Comparison
| method                      |     q |   discoveries |   heldout_n |   heldout_full_mse |   heldout_residual_mse |   heldout_selected_mse |   completeness_r2 |   centered_r2 |   necessity_fraction |   abs_effect_fraction |   selected_full_corr |   sign_agreement |
|:----------------------------|------:|--------------:|------------:|-------------------:|-----------------------:|-----------------------:|------------------:|--------------:|---------------------:|----------------------:|---------------------:|-----------------:|
| bh                          |   0.1 |            51 |         160 |            34.3411 |                1.1992  |              31.9403   |          0.96508  |     0.605245  |            0.93009   |              0.972572 |             0.787874 |          1       |
| by_bh                       |   0.1 |            37 |         160 |            34.3411 |                1.3029  |              31.4455   |          0.96206  |     0.57111   |            0.915683  |              0.964109 |             0.771956 |          1       |
| e_bh_pcal                   |   0.1 |            23 |         160 |            34.3411 |                1.26304 |              31.0376   |          0.963221 |     0.58423   |            0.903805  |              0.958715 |             0.780224 |          1       |
| p_lt_q                      |   0.1 |            90 |         160 |            34.3411 |                1.14921 |              31.3088   |          0.966535 |     0.621701  |            0.911703  |              0.960768 |             0.803314 |          1       |
| top_score_k_256             | nan   |           nan |         160 |            34.3411 |                1.23086 |              34.4316   |          0.964158 |     0.594825  |            1.00264   |              1.00464  |             0.791069 |          1       |
| top_score_k_bh              | nan   |           nan |         160 |            34.3411 |                1.31341 |              29.2973   |          0.961754 |     0.56765   |            0.853127  |              0.92476  |             0.799208 |          1       |
| top_score_k_by_bh           | nan   |           nan |         160 |            34.3411 |                1.23086 |              29.5376   |          0.964158 |     0.594825  |            0.860124  |              0.932135 |             0.80472  |          1       |
| top_score_k_e_bh_pcal       | nan   |           nan |         160 |            34.3411 |                1.22053 |              29.628    |          0.964459 |     0.598225  |            0.862758  |              0.93242  |             0.807632 |          1       |
| top_score_k_p_lt_q          | nan   |           nan |         160 |            34.3411 |                1.16793 |              31.4844   |          0.96599  |     0.615538  |            0.916816  |              0.96232  |             0.800822 |          1       |
| top_score_k_track_bh        | nan   |           nan |         160 |            34.3411 |                1.466   |              27.6568   |          0.957311 |     0.51742   |            0.805356  |              0.898546 |             0.79482  |          1       |
| top_score_k_track_by_bh     | nan   |           nan |         160 |            34.3411 |               20.746   |               2.50661  |          0.395883 |    -5.82921   |            0.0729916 |              0.248121 |             0.23679  |          0.98125 |
| top_score_k_track_e_bh_pcal | nan   |           nan |         160 |            34.3411 |               27.7139  |               0.661521 |          0.19298  |    -8.12291   |            0.0192633 |              0.112073 |             0.210434 |          0.94375 |
| top_score_k_track_p_lt_q    | nan   |           nan |         160 |            34.3411 |                1.33257 |              29.4833   |          0.961196 |     0.561341  |            0.858545  |              0.927078 |             0.795048 |          1       |
| track_bh                    |   0.1 |            11 |         160 |            34.3411 |                1.33132 |              30.1038   |          0.961232 |     0.561755  |            0.876613  |              0.937718 |             0.787213 |          1       |
| track_by_bh                 |   0.1 |             2 |         160 |            34.3411 |                3.31787 |              19.8759   |          0.903385 |    -0.0921835 |            0.578779  |              0.748099 |             0.75925  |          1       |
| track_e_bh_pcal             |   0.1 |             1 |         160 |            34.3411 |               14.6999  |               5.23796  |          0.571944 |    -3.83893   |            0.152528  |              0.366182 |             0.549454 |          1       |
| track_p_lt_q                |   0.1 |            60 |         160 |            34.3411 |                1.14143 |              33.6434   |          0.966762 |     0.624264  |            0.979686  |              0.990437 |             0.809529 |          1       |
