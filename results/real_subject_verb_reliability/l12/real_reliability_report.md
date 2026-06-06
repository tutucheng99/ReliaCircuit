# Real Subject-Verb Reliability: L12

## Null Decoy Reliability

| layer   | method                      | selection_rule        |   discoveries_mean |   discoveries_std |   known_null_decoys_selected_mean |   known_null_decoys_selected_std |   known_null_fdp_mean |   known_null_fdp_std |
|:--------|:----------------------------|:----------------------|-------------------:|------------------:|----------------------------------:|---------------------------------:|----------------------:|---------------------:|
| L12     | top_score_fixed_k_256       | screen_score_manual_k |            256     |          0        |                           256     |                         0        |             1         |            0         |
| L12     | top_score_fixed_k_7         | screen_score_manual_k |              7     |          0        |                             7     |                         0        |             1         |            0         |
| L12     | top_score_matched_bh        | screen_score_manual_k |             24.99  |          1.64726  |                            24.99  |                         1.64726  |             1         |            0         |
| L12     | top_score_matched_e_bh_pcal | screen_score_manual_k |              6     |          0        |                             6     |                         0        |             1         |            0         |
| L12     | bh                          | test_split_fdr        |             24.99  |          1.64726  |                             1.32  |                         1.27109  |             0.0498441 |            0.0459038 |
| L12     | by_bh                       | test_split_fdr        |             12.095 |          0.326355 |                             0.095 |                         0.326355 |             0.0071978 |            0.0244756 |
| L12     | e_bh_pcal                   | test_split_fdr        |              6     |          0        |                             0     |                         0        |             0         |            0         |
| L12     | p_lt_q                      | test_split_fdr        |             79.805 |          5.08984  |                            25.805 |                         5.08984  |             0.320579  |            0.0438427 |

## Prompt-Resampling Selection Stability

| layer   | estimand                   | method          |   discoveries_mean |   discoveries_std |   jaccard_mean |   jaccard_std |   recall_full_mean |   recall_full_std |   full_discoveries |
|:--------|:---------------------------|:----------------|-------------------:|------------------:|---------------:|--------------:|-------------------:|------------------:|-------------------:|
| L12     | mean_effect                | bh              |             47.06  |         25.6297   |       0.531777 |      0.148431 |           0.838621 |         0.085433  |                 29 |
| L12     | mean_effect                | by_bh           |             24.275 |         10.0691   |       0.569169 |      0.127136 |           0.816111 |         0.0891798 |                 18 |
| L12     | mean_effect                | e_bh_pcal       |              8.44  |          2.92733  |       0.660302 |      0.157676 |           0.859286 |         0.170948  |                  7 |
| L12     | mean_effect                | p_lt_q          |             82.54  |         26.6164   |       0.517126 |      0.12832  |           0.822037 |         0.0652894 |                 54 |
| L12     | prompt_tracking_covariance | track_bh        |             41.585 |         59.1025   |       0.20209  |      0.193981 |           0.8325   |         0.236587  |                  2 |
| L12     | prompt_tracking_covariance | track_by_bh     |              9.235 |         24.1717   |       0.545307 |      0.38704  |           1        |         0         |                  1 |
| L12     | prompt_tracking_covariance | track_e_bh_pcal |              1.07  |          0.368482 |       0.974167 |      0.121465 |           1        |         0         |                  1 |
| L12     | prompt_tracking_covariance | track_p_lt_q    |             91.64  |         57.4894   |       0.364517 |      0.102676 |           0.666102 |         0.241581  |                 59 |

## Real q Grid

| layer   | estimand                   |      q | method                            |   discoveries | selection_rule                     |
|:--------|:---------------------------|-------:|:----------------------------------|--------------:|:-----------------------------------|
| L12     | mean_effect                |   0.01 | e_bh_pcal                         |             4 | fdr_at_q                           |
| L12     | mean_effect                |   0.01 | by_bh                             |             9 | fdr_at_q                           |
| L12     | mean_effect                |   0.01 | bh                                |            14 | fdr_at_q                           |
| L12     | mean_effect                |   0.01 | p_lt_q                            |            29 | uncorrected_p_threshold            |
| L12     | mean_effect                |   0.01 | top_score_matched_e_bh_pcal       |             4 | manual_k_equal_to_e_bh_discoveries |
| L12     | prompt_tracking_covariance |   0.01 | track_e_bh_pcal                   |             1 | fdr_at_q                           |
| L12     | prompt_tracking_covariance |   0.01 | track_by_bh                       |             1 | fdr_at_q                           |
| L12     | prompt_tracking_covariance |   0.01 | track_bh                          |             1 | fdr_at_q                           |
| L12     | prompt_tracking_covariance |   0.01 | track_p_lt_q                      |            10 | uncorrected_p_threshold            |
| L12     | prompt_tracking_covariance |   0.01 | top_score_matched_track_e_bh_pcal |             1 | manual_k_equal_to_e_bh_discoveries |
| L12     | mean_effect                |   0.02 | e_bh_pcal                         |             5 | fdr_at_q                           |
| L12     | mean_effect                |   0.02 | by_bh                             |            10 | fdr_at_q                           |
| L12     | mean_effect                |   0.02 | bh                                |            19 | fdr_at_q                           |
| L12     | mean_effect                |   0.02 | p_lt_q                            |            33 | uncorrected_p_threshold            |
| L12     | mean_effect                |   0.02 | top_score_matched_e_bh_pcal       |             5 | manual_k_equal_to_e_bh_discoveries |
| L12     | prompt_tracking_covariance |   0.02 | track_e_bh_pcal                   |             1 | fdr_at_q                           |
| L12     | prompt_tracking_covariance |   0.02 | track_by_bh                       |             1 | fdr_at_q                           |
| L12     | prompt_tracking_covariance |   0.02 | track_bh                          |             1 | fdr_at_q                           |
| L12     | prompt_tracking_covariance |   0.02 | track_p_lt_q                      |            11 | uncorrected_p_threshold            |
| L12     | prompt_tracking_covariance |   0.02 | top_score_matched_track_e_bh_pcal |             1 | manual_k_equal_to_e_bh_discoveries |
| L12     | mean_effect                |   0.05 | e_bh_pcal                         |             6 | fdr_at_q                           |
| L12     | mean_effect                |   0.05 | by_bh                             |            12 | fdr_at_q                           |
| L12     | mean_effect                |   0.05 | bh                                |            23 | fdr_at_q                           |
| L12     | mean_effect                |   0.05 | p_lt_q                            |            45 | uncorrected_p_threshold            |
| L12     | mean_effect                |   0.05 | top_score_matched_e_bh_pcal       |             6 | manual_k_equal_to_e_bh_discoveries |
| L12     | prompt_tracking_covariance |   0.05 | track_e_bh_pcal                   |             1 | fdr_at_q                           |
| L12     | prompt_tracking_covariance |   0.05 | track_by_bh                       |             1 | fdr_at_q                           |
| L12     | prompt_tracking_covariance |   0.05 | track_bh                          |             1 | fdr_at_q                           |
| L12     | prompt_tracking_covariance |   0.05 | track_p_lt_q                      |            27 | uncorrected_p_threshold            |
| L12     | prompt_tracking_covariance |   0.05 | top_score_matched_track_e_bh_pcal |             1 | manual_k_equal_to_e_bh_discoveries |
| L12     | mean_effect                |   0.1  | e_bh_pcal                         |             7 | fdr_at_q                           |
| L12     | mean_effect                |   0.1  | by_bh                             |            18 | fdr_at_q                           |
| L12     | mean_effect                |   0.1  | bh                                |            29 | fdr_at_q                           |
| L12     | mean_effect                |   0.1  | p_lt_q                            |            54 | uncorrected_p_threshold            |
| L12     | mean_effect                |   0.1  | top_score_matched_e_bh_pcal       |             7 | manual_k_equal_to_e_bh_discoveries |
| L12     | prompt_tracking_covariance |   0.1  | track_e_bh_pcal                   |             1 | fdr_at_q                           |
| L12     | prompt_tracking_covariance |   0.1  | track_by_bh                       |             1 | fdr_at_q                           |
| L12     | prompt_tracking_covariance |   0.1  | track_bh                          |             2 | fdr_at_q                           |
| L12     | prompt_tracking_covariance |   0.1  | track_p_lt_q                      |            59 | uncorrected_p_threshold            |
| L12     | prompt_tracking_covariance |   0.1  | top_score_matched_track_e_bh_pcal |             1 | manual_k_equal_to_e_bh_discoveries |
| L12     | mean_effect                |   0.15 | e_bh_pcal                         |             8 | fdr_at_q                           |
| L12     | mean_effect                |   0.15 | by_bh                             |            19 | fdr_at_q                           |
| L12     | mean_effect                |   0.15 | bh                                |            37 | fdr_at_q                           |
| L12     | mean_effect                |   0.15 | p_lt_q                            |            70 | uncorrected_p_threshold            |
| L12     | mean_effect                |   0.15 | top_score_matched_e_bh_pcal       |             8 | manual_k_equal_to_e_bh_discoveries |
| L12     | prompt_tracking_covariance |   0.15 | track_e_bh_pcal                   |             1 | fdr_at_q                           |
| L12     | prompt_tracking_covariance |   0.15 | track_by_bh                       |             1 | fdr_at_q                           |
| L12     | prompt_tracking_covariance |   0.15 | track_bh                          |             2 | fdr_at_q                           |
| L12     | prompt_tracking_covariance |   0.15 | track_p_lt_q                      |            90 | uncorrected_p_threshold            |
| L12     | prompt_tracking_covariance |   0.15 | top_score_matched_track_e_bh_pcal |             1 | manual_k_equal_to_e_bh_discoveries |
| L12     | mean_effect                |   0.2  | e_bh_pcal                         |             9 | fdr_at_q                           |
| L12     | mean_effect                |   0.2  | by_bh                             |            20 | fdr_at_q                           |
| L12     | mean_effect                |   0.2  | bh                                |            41 | fdr_at_q                           |
| L12     | mean_effect                |   0.2  | p_lt_q                            |            77 | uncorrected_p_threshold            |
| L12     | mean_effect                |   0.2  | top_score_matched_e_bh_pcal       |             9 | manual_k_equal_to_e_bh_discoveries |
| L12     | prompt_tracking_covariance |   0.2  | track_e_bh_pcal                   |             1 | fdr_at_q                           |
| L12     | prompt_tracking_covariance |   0.2  | track_by_bh                       |             1 | fdr_at_q                           |
| L12     | prompt_tracking_covariance |   0.2  | track_bh                          |             2 | fdr_at_q                           |
| L12     | prompt_tracking_covariance |   0.2  | track_p_lt_q                      |           107 | uncorrected_p_threshold            |
| L12     | prompt_tracking_covariance |   0.2  | top_score_matched_track_e_bh_pcal |             1 | manual_k_equal_to_e_bh_discoveries |
| L12     | mean_effect                |   0.3  | e_bh_pcal                         |             9 | fdr_at_q                           |
| L12     | mean_effect                |   0.3  | by_bh                             |            23 | fdr_at_q                           |
| L12     | mean_effect                |   0.3  | bh                                |            45 | fdr_at_q                           |
| L12     | mean_effect                |   0.3  | p_lt_q                            |            94 | uncorrected_p_threshold            |
| L12     | mean_effect                |   0.3  | top_score_matched_e_bh_pcal       |             9 | manual_k_equal_to_e_bh_discoveries |
| L12     | prompt_tracking_covariance |   0.3  | track_e_bh_pcal                   |             1 | fdr_at_q                           |
| L12     | prompt_tracking_covariance |   0.3  | track_by_bh                       |             1 | fdr_at_q                           |
| L12     | prompt_tracking_covariance |   0.3  | track_bh                          |            11 | fdr_at_q                           |
| L12     | prompt_tracking_covariance |   0.3  | track_p_lt_q                      |           160 | uncorrected_p_threshold            |
| L12     | prompt_tracking_covariance |   0.3  | top_score_matched_track_e_bh_pcal |             1 | manual_k_equal_to_e_bh_discoveries |
| L12     | screen_score               | nan    | top_score_fixed_k_1               |             1 | manual_k_no_fdr_target             |
| L12     | screen_score               | nan    | top_score_fixed_k_5               |             5 | manual_k_no_fdr_target             |
| L12     | screen_score               | nan    | top_score_fixed_k_7               |             7 | manual_k_no_fdr_target             |
| L12     | screen_score               | nan    | top_score_fixed_k_10              |            10 | manual_k_no_fdr_target             |
| L12     | screen_score               | nan    | top_score_fixed_k_17              |            17 | manual_k_no_fdr_target             |
| L12     | screen_score               | nan    | top_score_fixed_k_29              |            29 | manual_k_no_fdr_target             |
| L12     | screen_score               | nan    | top_score_fixed_k_54              |            54 | manual_k_no_fdr_target             |
| L12     | screen_score               | nan    | top_score_fixed_k_100             |           100 | manual_k_no_fdr_target             |
| L12     | screen_score               | nan    | top_score_fixed_k_256             |           256 | manual_k_no_fdr_target             |

## Layer Scan Metrics

| layer   | method                |   discoveries |   completeness_r2 |   centered_r2 |   selected_full_corr |   abs_effect_fraction |   sign_agreement |
|:--------|:----------------------|--------------:|------------------:|--------------:|---------------------:|----------------------:|-----------------:|
| L12     | bh                    |            29 |          0.927549 |      0.180983 |             0.73859  |              0.816847 |                1 |
| L12     | by_bh                 |            18 |          0.927067 |      0.175529 |             0.728711 |              0.820494 |                1 |
| L12     | e_bh_pcal             |             7 |          0.928115 |      0.187378 |             0.725867 |              0.826864 |                1 |
| L12     | p_lt_q                |            54 |          0.929206 |      0.199718 |             0.732541 |              0.824481 |                1 |
| L12     | top_score_k_256       |           nan |          0.944764 |      0.375587 |             0.753603 |              0.869361 |                1 |
| L12     | top_score_k_e_bh_pcal |           nan |          0.94652  |      0.395435 |             0.766367 |              0.872505 |                1 |
| L12     | track_e_bh_pcal       |             1 |          0.956483 |      0.50806  |             0.761473 |              0.923485 |                1 |
