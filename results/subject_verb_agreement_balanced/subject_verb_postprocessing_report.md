# Subject-Verb Real Run Postprocessing

## FDR Selection
| method    |   q |   discoveries |
|:----------|----:|--------------:|
| e_bh_pcal | 0.1 |            17 |
| by_bh     | 0.1 |            29 |
| bh        | 0.1 |            47 |
| p_lt_q    | 0.1 |            72 |

## Tracking-Aware FDR Selection
| method    |   q |   discoveries |
|:----------|----:|--------------:|
| e_bh_pcal | 0.1 |             0 |
| by_bh     | 0.1 |             1 |
| bh        | 0.1 |             1 |
| p_lt_q    | 0.1 |             9 |

## Top-Score Baselines
| selection_method      | reference_method   |   k | path                                                                                               |
|:----------------------|:-------------------|----:|:---------------------------------------------------------------------------------------------------|
| top_score_k_e_bh_pcal | e_bh_pcal          |  17 | results/subject_verb_agreement_balanced/cache_analysis/selected_features_top_score_k_e_bh_pcal.csv |
| top_score_k_by_bh     | by_bh              |  29 | results/subject_verb_agreement_balanced/cache_analysis/selected_features_top_score_k_by_bh.csv     |
| top_score_k_bh        | bh                 |  47 | results/subject_verb_agreement_balanced/cache_analysis/selected_features_top_score_k_bh.csv        |
| top_score_k_p_lt_q    | p_lt_q             |  72 | results/subject_verb_agreement_balanced/cache_analysis/selected_features_top_score_k_p_lt_q.csv    |
| top_score_k_256       | fixed_top_k        | 256 | results/subject_verb_agreement_balanced/cache_analysis/selected_features_top_score_k_256.csv       |

## Tracking-Matched Top-Score Baselines
| selection_method         | reference_method   |   k | path                                                                                                  |
|:-------------------------|:-------------------|----:|:------------------------------------------------------------------------------------------------------|
| top_score_k_track_by_bh  | by_bh              |   1 | results/subject_verb_agreement_balanced/cache_analysis/selected_features_top_score_k_track_by_bh.csv  |
| top_score_k_track_bh     | bh                 |   1 | results/subject_verb_agreement_balanced/cache_analysis/selected_features_top_score_k_track_bh.csv     |
| top_score_k_track_p_lt_q | p_lt_q             |   9 | results/subject_verb_agreement_balanced/cache_analysis/selected_features_top_score_k_track_p_lt_q.csv |

## Circuit Manifest

- path: `data/subject_verb_agreement_balanced/circuit_eval_manifest.csv`
- rows: `2560`
- methods: `e_bh_pcal, by_bh, bh, p_lt_q, track_e_bh_pcal, track_by_bh, track_bh, track_p_lt_q, top_score_k_e_bh_pcal, top_score_k_by_bh, top_score_k_bh, top_score_k_p_lt_q, top_score_k_256, top_score_k_track_by_bh, top_score_k_track_bh, top_score_k_track_p_lt_q`

## Held-Out Joint Circuit Tracking
| method                   |   heldout_n |   heldout_full_mse |   heldout_residual_mse |   heldout_selected_mse |   completeness_r2 |   centered_r2 |   necessity_fraction |   abs_effect_fraction |   selected_full_corr |   sign_agreement |
|:-------------------------|------------:|-------------------:|-----------------------:|-----------------------:|------------------:|--------------:|---------------------:|----------------------:|---------------------:|-----------------:|
| e_bh_pcal                |         160 |            34.3411 |                16.4339 |             4.43067    |         0.521452  |      -4.40972 |          0.12902     |             0.350849  |          0.149339    |          0.99375 |
| by_bh                    |         160 |            34.3411 |                15.3805 |             5.13728    |         0.552124  |      -4.06299 |          0.149596    |             0.377748  |          0.166355    |          0.99375 |
| bh                       |         160 |            34.3411 |                14.0528 |             6.3397     |         0.590788  |      -3.62592 |          0.18461     |             0.401251  |          0.380065    |          0.99375 |
| p_lt_q                   |         160 |            34.3411 |                13.996  |             6.27929    |         0.59244   |      -3.60724 |          0.182851    |             0.40066   |          0.394575    |          1       |
| track_e_bh_pcal          |         160 |            34.3411 |                34.3411 |             0          |         0         |     -10.3044  |          0           |             0         |        nan           |          0       |
| track_by_bh              |         160 |            34.3411 |                33.9488 |             0.00827967 |         0.0114235 |     -10.1753  |          0.000241101 |             0.011011  |         -0.158382    |          0.49375 |
| track_bh                 |         160 |            34.3411 |                33.9488 |             0.00827967 |         0.0114235 |     -10.1753  |          0.000241101 |             0.011011  |         -0.158382    |          0.49375 |
| track_p_lt_q             |         160 |            34.3411 |                31.4268 |             0.429608   |         0.0848624 |      -9.34513 |          0.01251     |             0.0449882 |          0.49835     |          0.59375 |
| top_score_k_e_bh_pcal    |         160 |            34.3411 |                19.3499 |             3.24296    |         0.436537  |      -5.36964 |          0.0944339   |             0.294398  |          0.00798189  |          0.98125 |
| top_score_k_by_bh        |         160 |            34.3411 |                19.0841 |             3.35707    |         0.444276  |      -5.28215 |          0.0977568   |             0.297434  |          0.0479536   |          0.9875  |
| top_score_k_bh           |         160 |            34.3411 |                16.6948 |             4.50282    |         0.513852  |      -4.49563 |          0.131121    |             0.345587  |          0.170891    |          0.99375 |
| top_score_k_p_lt_q       |         160 |            34.3411 |                15.9897 |             4.88535    |         0.534386  |      -4.26351 |          0.14226     |             0.363746  |          0.154316    |          1       |
| top_score_k_256          |         160 |            34.3411 |                13.9336 |             6.28896    |         0.594259  |      -3.58668 |          0.183132    |             0.401172  |          0.405365    |          1       |
| top_score_k_track_by_bh  |         160 |            34.3411 |                30.6578 |             0.237885   |         0.107255  |      -9.09199 |          0.00692713  |             0.0681014 |         -0.0377713   |          0.83125 |
| top_score_k_track_bh     |         160 |            34.3411 |                30.6578 |             0.237885   |         0.107255  |      -9.09199 |          0.00692713  |             0.0681014 |         -0.0377713   |          0.83125 |
| top_score_k_track_p_lt_q |         160 |            34.3411 |                19.9072 |             2.9555     |         0.42031   |      -5.55307 |          0.0860631   |             0.281074  |          0.000848582 |          0.98125 |

## Reliability And Tracking Comparison
| method                   |     q |   discoveries |   heldout_n |   heldout_full_mse |   heldout_residual_mse |   heldout_selected_mse |   completeness_r2 |   centered_r2 |   necessity_fraction |   abs_effect_fraction |   selected_full_corr |   sign_agreement |
|:-------------------------|------:|--------------:|------------:|-------------------:|-----------------------:|-----------------------:|------------------:|--------------:|---------------------:|----------------------:|---------------------:|-----------------:|
| bh                       |   0.1 |            47 |         160 |            34.3411 |                14.0528 |             6.3397     |         0.590788  |      -3.62592 |          0.18461     |             0.401251  |          0.380065    |          0.99375 |
| by_bh                    |   0.1 |            29 |         160 |            34.3411 |                15.3805 |             5.13728    |         0.552124  |      -4.06299 |          0.149596    |             0.377748  |          0.166355    |          0.99375 |
| e_bh_pcal                |   0.1 |            17 |         160 |            34.3411 |                16.4339 |             4.43067    |         0.521452  |      -4.40972 |          0.12902     |             0.350849  |          0.149339    |          0.99375 |
| p_lt_q                   |   0.1 |            72 |         160 |            34.3411 |                13.996  |             6.27929    |         0.59244   |      -3.60724 |          0.182851    |             0.40066   |          0.394575    |          1       |
| top_score_k_256          | nan   |           nan |         160 |            34.3411 |                13.9336 |             6.28896    |         0.594259  |      -3.58668 |          0.183132    |             0.401172  |          0.405365    |          1       |
| top_score_k_bh           | nan   |           nan |         160 |            34.3411 |                16.6948 |             4.50282    |         0.513852  |      -4.49563 |          0.131121    |             0.345587  |          0.170891    |          0.99375 |
| top_score_k_by_bh        | nan   |           nan |         160 |            34.3411 |                19.0841 |             3.35707    |         0.444276  |      -5.28215 |          0.0977568   |             0.297434  |          0.0479536   |          0.9875  |
| top_score_k_e_bh_pcal    | nan   |           nan |         160 |            34.3411 |                19.3499 |             3.24296    |         0.436537  |      -5.36964 |          0.0944339   |             0.294398  |          0.00798189  |          0.98125 |
| top_score_k_p_lt_q       | nan   |           nan |         160 |            34.3411 |                15.9897 |             4.88535    |         0.534386  |      -4.26351 |          0.14226     |             0.363746  |          0.154316    |          1       |
| top_score_k_track_bh     | nan   |           nan |         160 |            34.3411 |                30.6578 |             0.237885   |         0.107255  |      -9.09199 |          0.00692713  |             0.0681014 |         -0.0377713   |          0.83125 |
| top_score_k_track_by_bh  | nan   |           nan |         160 |            34.3411 |                30.6578 |             0.237885   |         0.107255  |      -9.09199 |          0.00692713  |             0.0681014 |         -0.0377713   |          0.83125 |
| top_score_k_track_p_lt_q | nan   |           nan |         160 |            34.3411 |                19.9072 |             2.9555     |         0.42031   |      -5.55307 |          0.0860631   |             0.281074  |          0.000848582 |          0.98125 |
| track_bh                 |   0.1 |             1 |         160 |            34.3411 |                33.9488 |             0.00827967 |         0.0114235 |     -10.1753  |          0.000241101 |             0.011011  |         -0.158382    |          0.49375 |
| track_by_bh              |   0.1 |             1 |         160 |            34.3411 |                33.9488 |             0.00827967 |         0.0114235 |     -10.1753  |          0.000241101 |             0.011011  |         -0.158382    |          0.49375 |
| track_e_bh_pcal          |   0.1 |             0 |         160 |            34.3411 |                34.3411 |             0          |         0         |     -10.3044  |          0           |             0         |        nan           |          0       |
| track_p_lt_q             |   0.1 |             9 |         160 |            34.3411 |                31.4268 |             0.429608   |         0.0848624 |      -9.34513 |          0.01251     |             0.0449882 |          0.49835     |          0.59375 |
