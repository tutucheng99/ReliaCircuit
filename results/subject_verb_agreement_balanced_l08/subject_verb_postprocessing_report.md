# Subject-Verb Real Run Postprocessing

## FDR Selection
| method    |   q |   discoveries |
|:----------|----:|--------------:|
| e_bh_pcal | 0.1 |             6 |
| by_bh     | 0.1 |             9 |
| bh        | 0.1 |            15 |
| p_lt_q    | 0.1 |            52 |

## Tracking-Aware FDR Selection
| method    |   q |   discoveries |
|:----------|----:|--------------:|
| e_bh_pcal | 0.1 |             1 |
| by_bh     | 0.1 |             1 |
| bh        | 0.1 |             1 |
| p_lt_q    | 0.1 |            20 |

## Top-Score Baselines
| selection_method      | reference_method   |   k | path                                                                                                   |
|:----------------------|:-------------------|----:|:-------------------------------------------------------------------------------------------------------|
| top_score_k_e_bh_pcal | e_bh_pcal          |   6 | results/subject_verb_agreement_balanced_l08/cache_analysis/selected_features_top_score_k_e_bh_pcal.csv |
| top_score_k_by_bh     | by_bh              |   9 | results/subject_verb_agreement_balanced_l08/cache_analysis/selected_features_top_score_k_by_bh.csv     |
| top_score_k_bh        | bh                 |  15 | results/subject_verb_agreement_balanced_l08/cache_analysis/selected_features_top_score_k_bh.csv        |
| top_score_k_p_lt_q    | p_lt_q             |  52 | results/subject_verb_agreement_balanced_l08/cache_analysis/selected_features_top_score_k_p_lt_q.csv    |
| top_score_k_256       | fixed_top_k        | 256 | results/subject_verb_agreement_balanced_l08/cache_analysis/selected_features_top_score_k_256.csv       |

## Tracking-Matched Top-Score Baselines
| selection_method            | reference_method   |   k | path                                                                                                         |
|:----------------------------|:-------------------|----:|:-------------------------------------------------------------------------------------------------------------|
| top_score_k_track_e_bh_pcal | e_bh_pcal          |   1 | results/subject_verb_agreement_balanced_l08/cache_analysis/selected_features_top_score_k_track_e_bh_pcal.csv |
| top_score_k_track_by_bh     | by_bh              |   1 | results/subject_verb_agreement_balanced_l08/cache_analysis/selected_features_top_score_k_track_by_bh.csv     |
| top_score_k_track_bh        | bh                 |   1 | results/subject_verb_agreement_balanced_l08/cache_analysis/selected_features_top_score_k_track_bh.csv        |
| top_score_k_track_p_lt_q    | p_lt_q             |  20 | results/subject_verb_agreement_balanced_l08/cache_analysis/selected_features_top_score_k_track_p_lt_q.csv    |

## Circuit Manifest

- path: `data/subject_verb_agreement_balanced_l08/circuit_eval_manifest.csv`
- rows: `2720`
- methods: `e_bh_pcal, by_bh, bh, p_lt_q, track_e_bh_pcal, track_by_bh, track_bh, track_p_lt_q, top_score_k_e_bh_pcal, top_score_k_by_bh, top_score_k_bh, top_score_k_p_lt_q, top_score_k_256, top_score_k_track_e_bh_pcal, top_score_k_track_by_bh, top_score_k_track_bh, top_score_k_track_p_lt_q`

## Held-Out Joint Circuit Tracking
| method                      |   heldout_n |   heldout_full_mse |   heldout_residual_mse |   heldout_selected_mse |   completeness_r2 |   centered_r2 |   necessity_fraction |   abs_effect_fraction |   selected_full_corr |   sign_agreement |
|:----------------------------|------------:|-------------------:|-----------------------:|-----------------------:|------------------:|--------------:|---------------------:|----------------------:|---------------------:|-----------------:|
| e_bh_pcal                   |         160 |            34.3411 |                1.08264 |                32.537  |          0.968474 |      0.643614 |             0.947468 |              0.975706 |             0.816815 |                1 |
| by_bh                       |         160 |            34.3411 |                1.10567 |                32.1825 |          0.967803 |      0.636035 |             0.937144 |              0.969702 |             0.814877 |                1 |
| bh                          |         160 |            34.3411 |                1.11158 |                32.1432 |          0.967631 |      0.634089 |             0.935999 |              0.968441 |             0.815213 |                1 |
| p_lt_q                      |         160 |            34.3411 |                1.19732 |                31.1586 |          0.965134 |      0.605865 |             0.907329 |              0.950854 |             0.810084 |                1 |
| track_e_bh_pcal             |         160 |            34.3411 |                1.71488 |                28.073  |          0.950063 |      0.435492 |             0.817478 |              0.906093 |             0.739686 |                1 |
| track_by_bh                 |         160 |            34.3411 |                1.71488 |                28.073  |          0.950063 |      0.435492 |             0.817478 |              0.906093 |             0.739686 |                1 |
| track_bh                    |         160 |            34.3411 |                1.71488 |                28.073  |          0.950063 |      0.435492 |             0.817478 |              0.906093 |             0.739686 |                1 |
| track_p_lt_q                |         160 |            34.3411 |                1.26463 |                30.9123 |          0.963174 |      0.583706 |             0.900156 |              0.948752 |             0.79628  |                1 |
| top_score_k_e_bh_pcal       |         160 |            34.3411 |                1.25786 |                30.7546 |          0.963372 |      0.585936 |             0.895563 |              0.949334 |             0.792131 |                1 |
| top_score_k_by_bh           |         160 |            34.3411 |                1.19053 |                31.5934 |          0.965332 |      0.6081   |             0.919989 |              0.961841 |             0.800156 |                1 |
| top_score_k_bh              |         160 |            34.3411 |                1.05314 |                33.403  |          0.969333 |      0.653327 |             0.972683 |              0.99022  |             0.818608 |                1 |
| top_score_k_p_lt_q          |         160 |            34.3411 |                1.18267 |                33.2165 |          0.965561 |      0.610686 |             0.967254 |              0.984798 |             0.801    |                1 |
| top_score_k_256             |         160 |            34.3411 |                1.24759 |                31.847  |          0.963671 |      0.589315 |             0.927375 |              0.960985 |             0.799335 |                1 |
| top_score_k_track_e_bh_pcal |         160 |            34.3411 |                1.71488 |                28.073  |          0.950063 |      0.435492 |             0.817478 |              0.906093 |             0.739686 |                1 |
| top_score_k_track_by_bh     |         160 |            34.3411 |                1.71488 |                28.073  |          0.950063 |      0.435492 |             0.817478 |              0.906093 |             0.739686 |                1 |
| top_score_k_track_bh        |         160 |            34.3411 |                1.71488 |                28.073  |          0.950063 |      0.435492 |             0.817478 |              0.906093 |             0.739686 |                1 |
| top_score_k_track_p_lt_q    |         160 |            34.3411 |                1.04112 |                33.3511 |          0.969683 |      0.657282 |             0.971174 |              0.988976 |             0.821424 |                1 |

## Reliability And Tracking Comparison
| method                      |     q |   discoveries |   heldout_n |   heldout_full_mse |   heldout_residual_mse |   heldout_selected_mse |   completeness_r2 |   centered_r2 |   necessity_fraction |   abs_effect_fraction |   selected_full_corr |   sign_agreement |
|:----------------------------|------:|--------------:|------------:|-------------------:|-----------------------:|-----------------------:|------------------:|--------------:|---------------------:|----------------------:|---------------------:|-----------------:|
| bh                          |   0.1 |            15 |         160 |            34.3411 |                1.11158 |                32.1432 |          0.967631 |      0.634089 |             0.935999 |              0.968441 |             0.815213 |                1 |
| by_bh                       |   0.1 |             9 |         160 |            34.3411 |                1.10567 |                32.1825 |          0.967803 |      0.636035 |             0.937144 |              0.969702 |             0.814877 |                1 |
| e_bh_pcal                   |   0.1 |             6 |         160 |            34.3411 |                1.08264 |                32.537  |          0.968474 |      0.643614 |             0.947468 |              0.975706 |             0.816815 |                1 |
| p_lt_q                      |   0.1 |            52 |         160 |            34.3411 |                1.19732 |                31.1586 |          0.965134 |      0.605865 |             0.907329 |              0.950854 |             0.810084 |                1 |
| top_score_k_256             | nan   |           nan |         160 |            34.3411 |                1.24759 |                31.847  |          0.963671 |      0.589315 |             0.927375 |              0.960985 |             0.799335 |                1 |
| top_score_k_bh              | nan   |           nan |         160 |            34.3411 |                1.05314 |                33.403  |          0.969333 |      0.653327 |             0.972683 |              0.99022  |             0.818608 |                1 |
| top_score_k_by_bh           | nan   |           nan |         160 |            34.3411 |                1.19053 |                31.5934 |          0.965332 |      0.6081   |             0.919989 |              0.961841 |             0.800156 |                1 |
| top_score_k_e_bh_pcal       | nan   |           nan |         160 |            34.3411 |                1.25786 |                30.7546 |          0.963372 |      0.585936 |             0.895563 |              0.949334 |             0.792131 |                1 |
| top_score_k_p_lt_q          | nan   |           nan |         160 |            34.3411 |                1.18267 |                33.2165 |          0.965561 |      0.610686 |             0.967254 |              0.984798 |             0.801    |                1 |
| top_score_k_track_bh        | nan   |           nan |         160 |            34.3411 |                1.71488 |                28.073  |          0.950063 |      0.435492 |             0.817478 |              0.906093 |             0.739686 |                1 |
| top_score_k_track_by_bh     | nan   |           nan |         160 |            34.3411 |                1.71488 |                28.073  |          0.950063 |      0.435492 |             0.817478 |              0.906093 |             0.739686 |                1 |
| top_score_k_track_e_bh_pcal | nan   |           nan |         160 |            34.3411 |                1.71488 |                28.073  |          0.950063 |      0.435492 |             0.817478 |              0.906093 |             0.739686 |                1 |
| top_score_k_track_p_lt_q    | nan   |           nan |         160 |            34.3411 |                1.04112 |                33.3511 |          0.969683 |      0.657282 |             0.971174 |              0.988976 |             0.821424 |                1 |
| track_bh                    |   0.1 |             1 |         160 |            34.3411 |                1.71488 |                28.073  |          0.950063 |      0.435492 |             0.817478 |              0.906093 |             0.739686 |                1 |
| track_by_bh                 |   0.1 |             1 |         160 |            34.3411 |                1.71488 |                28.073  |          0.950063 |      0.435492 |             0.817478 |              0.906093 |             0.739686 |                1 |
| track_e_bh_pcal             |   0.1 |             1 |         160 |            34.3411 |                1.71488 |                28.073  |          0.950063 |      0.435492 |             0.817478 |              0.906093 |             0.739686 |                1 |
| track_p_lt_q                |   0.1 |            20 |         160 |            34.3411 |                1.26463 |                30.9123 |          0.963174 |      0.583706 |             0.900156 |              0.948752 |             0.79628  |                1 |
