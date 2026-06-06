# Subject-Verb Real Run Postprocessing

## FDR Selection
| method    |   q |   discoveries |
|:----------|----:|--------------:|
| e_bh_pcal | 0.1 |             7 |
| by_bh     | 0.1 |            18 |
| bh        | 0.1 |            29 |
| p_lt_q    | 0.1 |            54 |

## Tracking-Aware FDR Selection
| method    |   q |   discoveries |
|:----------|----:|--------------:|
| e_bh_pcal | 0.1 |             1 |
| by_bh     | 0.1 |             1 |
| bh        | 0.1 |             2 |
| p_lt_q    | 0.1 |            59 |

## Top-Score Baselines
| selection_method      | reference_method   |   k | path                                                                                                   |
|:----------------------|:-------------------|----:|:-------------------------------------------------------------------------------------------------------|
| top_score_k_e_bh_pcal | e_bh_pcal          |   7 | results/subject_verb_agreement_balanced_l12/cache_analysis/selected_features_top_score_k_e_bh_pcal.csv |
| top_score_k_by_bh     | by_bh              |  18 | results/subject_verb_agreement_balanced_l12/cache_analysis/selected_features_top_score_k_by_bh.csv     |
| top_score_k_bh        | bh                 |  29 | results/subject_verb_agreement_balanced_l12/cache_analysis/selected_features_top_score_k_bh.csv        |
| top_score_k_p_lt_q    | p_lt_q             |  54 | results/subject_verb_agreement_balanced_l12/cache_analysis/selected_features_top_score_k_p_lt_q.csv    |
| top_score_k_256       | fixed_top_k        | 256 | results/subject_verb_agreement_balanced_l12/cache_analysis/selected_features_top_score_k_256.csv       |

## Tracking-Matched Top-Score Baselines
| selection_method            | reference_method   |   k | path                                                                                                         |
|:----------------------------|:-------------------|----:|:-------------------------------------------------------------------------------------------------------------|
| top_score_k_track_e_bh_pcal | e_bh_pcal          |   1 | results/subject_verb_agreement_balanced_l12/cache_analysis/selected_features_top_score_k_track_e_bh_pcal.csv |
| top_score_k_track_by_bh     | by_bh              |   1 | results/subject_verb_agreement_balanced_l12/cache_analysis/selected_features_top_score_k_track_by_bh.csv     |
| top_score_k_track_bh        | bh                 |   2 | results/subject_verb_agreement_balanced_l12/cache_analysis/selected_features_top_score_k_track_bh.csv        |
| top_score_k_track_p_lt_q    | p_lt_q             |  59 | results/subject_verb_agreement_balanced_l12/cache_analysis/selected_features_top_score_k_track_p_lt_q.csv    |

## Circuit Manifest

- path: `data/subject_verb_agreement_balanced_l12/circuit_eval_manifest.csv`
- rows: `2720`
- methods: `e_bh_pcal, by_bh, bh, p_lt_q, track_e_bh_pcal, track_by_bh, track_bh, track_p_lt_q, top_score_k_e_bh_pcal, top_score_k_by_bh, top_score_k_bh, top_score_k_p_lt_q, top_score_k_256, top_score_k_track_e_bh_pcal, top_score_k_track_by_bh, top_score_k_track_bh, top_score_k_track_p_lt_q`

## Held-Out Joint Circuit Tracking
| method                      |   heldout_n |   heldout_full_mse |   heldout_residual_mse |   heldout_selected_mse |   completeness_r2 |   centered_r2 |   necessity_fraction |   abs_effect_fraction |   selected_full_corr |   sign_agreement |
|:----------------------------|------------:|-------------------:|-----------------------:|-----------------------:|------------------:|--------------:|---------------------:|----------------------:|---------------------:|-----------------:|
| e_bh_pcal                   |         160 |            34.3411 |                2.46861 |                23.8674 |          0.928115 |      0.187378 |             0.69501  |              0.826864 |             0.725867 |                1 |
| by_bh                       |         160 |            34.3411 |                2.50461 |                23.4361 |          0.927067 |      0.175529 |             0.682451 |              0.820494 |             0.728711 |                1 |
| bh                          |         160 |            34.3411 |                2.48804 |                23.2176 |          0.927549 |      0.180983 |             0.67609  |              0.816847 |             0.73859  |                1 |
| p_lt_q                      |         160 |            34.3411 |                2.43113 |                23.5889 |          0.929206 |      0.199718 |             0.686901 |              0.824481 |             0.732541 |                1 |
| track_e_bh_pcal             |         160 |            34.3411 |                1.49443 |                28.9876 |          0.956483 |      0.50806  |             0.844109 |              0.923485 |             0.761473 |                1 |
| track_by_bh                 |         160 |            34.3411 |                1.49443 |                28.9876 |          0.956483 |      0.50806  |             0.844109 |              0.923485 |             0.761473 |                1 |
| track_bh                    |         160 |            34.3411 |                1.46707 |                29.0105 |          0.957279 |      0.517067 |             0.844777 |              0.924327 |             0.765331 |                1 |
| track_p_lt_q                |         160 |            34.3411 |                1.45331 |                30.4442 |          0.95768  |      0.521597 |             0.886526 |              0.945752 |             0.756174 |                1 |
| top_score_k_e_bh_pcal       |         160 |            34.3411 |                1.83657 |                26.4154 |          0.94652  |      0.395435 |             0.769209 |              0.872505 |             0.766367 |                1 |
| top_score_k_by_bh           |         160 |            34.3411 |                1.96189 |                26.0014 |          0.94287  |      0.354182 |             0.757153 |              0.865225 |             0.754091 |                1 |
| top_score_k_bh              |         160 |            34.3411 |                2.00704 |                24.8796 |          0.941556 |      0.33932  |             0.724485 |              0.847799 |             0.769082 |                1 |
| top_score_k_p_lt_q          |         160 |            34.3411 |                2.19492 |                24.0734 |          0.936085 |      0.277472 |             0.70101  |              0.835695 |             0.752235 |                1 |
| top_score_k_256             |         160 |            34.3411 |                1.89686 |                26.0214 |          0.944764 |      0.375587 |             0.757735 |              0.869361 |             0.753603 |                1 |
| top_score_k_track_e_bh_pcal |         160 |            34.3411 |                1.49443 |                28.9876 |          0.956483 |      0.50806  |             0.844109 |              0.923485 |             0.761473 |                1 |
| top_score_k_track_by_bh     |         160 |            34.3411 |                1.49443 |                28.9876 |          0.956483 |      0.50806  |             0.844109 |              0.923485 |             0.761473 |                1 |
| top_score_k_track_bh        |         160 |            34.3411 |                1.49125 |                28.975  |          0.956575 |      0.509109 |             0.843744 |              0.923082 |             0.762695 |                1 |
| top_score_k_track_p_lt_q    |         160 |            34.3411 |                2.17417 |                24.3693 |          0.936689 |      0.284303 |             0.709625 |              0.840822 |             0.746882 |                1 |

## Reliability And Tracking Comparison
| method                      |     q |   discoveries |   heldout_n |   heldout_full_mse |   heldout_residual_mse |   heldout_selected_mse |   completeness_r2 |   centered_r2 |   necessity_fraction |   abs_effect_fraction |   selected_full_corr |   sign_agreement |
|:----------------------------|------:|--------------:|------------:|-------------------:|-----------------------:|-----------------------:|------------------:|--------------:|---------------------:|----------------------:|---------------------:|-----------------:|
| bh                          |   0.1 |            29 |         160 |            34.3411 |                2.48804 |                23.2176 |          0.927549 |      0.180983 |             0.67609  |              0.816847 |             0.73859  |                1 |
| by_bh                       |   0.1 |            18 |         160 |            34.3411 |                2.50461 |                23.4361 |          0.927067 |      0.175529 |             0.682451 |              0.820494 |             0.728711 |                1 |
| e_bh_pcal                   |   0.1 |             7 |         160 |            34.3411 |                2.46861 |                23.8674 |          0.928115 |      0.187378 |             0.69501  |              0.826864 |             0.725867 |                1 |
| p_lt_q                      |   0.1 |            54 |         160 |            34.3411 |                2.43113 |                23.5889 |          0.929206 |      0.199718 |             0.686901 |              0.824481 |             0.732541 |                1 |
| top_score_k_256             | nan   |           nan |         160 |            34.3411 |                1.89686 |                26.0214 |          0.944764 |      0.375587 |             0.757735 |              0.869361 |             0.753603 |                1 |
| top_score_k_bh              | nan   |           nan |         160 |            34.3411 |                2.00704 |                24.8796 |          0.941556 |      0.33932  |             0.724485 |              0.847799 |             0.769082 |                1 |
| top_score_k_by_bh           | nan   |           nan |         160 |            34.3411 |                1.96189 |                26.0014 |          0.94287  |      0.354182 |             0.757153 |              0.865225 |             0.754091 |                1 |
| top_score_k_e_bh_pcal       | nan   |           nan |         160 |            34.3411 |                1.83657 |                26.4154 |          0.94652  |      0.395435 |             0.769209 |              0.872505 |             0.766367 |                1 |
| top_score_k_p_lt_q          | nan   |           nan |         160 |            34.3411 |                2.19492 |                24.0734 |          0.936085 |      0.277472 |             0.70101  |              0.835695 |             0.752235 |                1 |
| top_score_k_track_bh        | nan   |           nan |         160 |            34.3411 |                1.49125 |                28.975  |          0.956575 |      0.509109 |             0.843744 |              0.923082 |             0.762695 |                1 |
| top_score_k_track_by_bh     | nan   |           nan |         160 |            34.3411 |                1.49443 |                28.9876 |          0.956483 |      0.50806  |             0.844109 |              0.923485 |             0.761473 |                1 |
| top_score_k_track_e_bh_pcal | nan   |           nan |         160 |            34.3411 |                1.49443 |                28.9876 |          0.956483 |      0.50806  |             0.844109 |              0.923485 |             0.761473 |                1 |
| top_score_k_track_p_lt_q    | nan   |           nan |         160 |            34.3411 |                2.17417 |                24.3693 |          0.936689 |      0.284303 |             0.709625 |              0.840822 |             0.746882 |                1 |
| track_bh                    |   0.1 |             2 |         160 |            34.3411 |                1.46707 |                29.0105 |          0.957279 |      0.517067 |             0.844777 |              0.924327 |             0.765331 |                1 |
| track_by_bh                 |   0.1 |             1 |         160 |            34.3411 |                1.49443 |                28.9876 |          0.956483 |      0.50806  |             0.844109 |              0.923485 |             0.761473 |                1 |
| track_e_bh_pcal             |   0.1 |             1 |         160 |            34.3411 |                1.49443 |                28.9876 |          0.956483 |      0.50806  |             0.844109 |              0.923485 |             0.761473 |                1 |
| track_p_lt_q                |   0.1 |            59 |         160 |            34.3411 |                1.45331 |                30.4442 |          0.95768  |      0.521597 |             0.886526 |              0.945752 |             0.756174 |                1 |
