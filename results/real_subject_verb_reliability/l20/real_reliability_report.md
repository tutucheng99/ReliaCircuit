# Real Subject-Verb Reliability: L20

## Null Decoy Reliability

| layer   | method                      | selection_rule        |   discoveries_mean |   discoveries_std |   known_null_decoys_selected_mean |   known_null_decoys_selected_std |   known_null_fdp_mean |   known_null_fdp_std |
|:--------|:----------------------------|:----------------------|-------------------:|------------------:|----------------------------------:|---------------------------------:|----------------------:|---------------------:|
| L20     | top_score_fixed_k_256       | screen_score_manual_k |            256     |          0        |                           256     |                         0        |            1          |            0         |
| L20     | top_score_fixed_k_7         | screen_score_manual_k |              7     |          0        |                             7     |                         0        |            1          |            0         |
| L20     | top_score_matched_bh        | screen_score_manual_k |             41.51  |          2.06183  |                            41.51  |                         2.06183  |            1          |            0         |
| L20     | top_score_matched_e_bh_pcal | screen_score_manual_k |             15     |          0        |                            15     |                         0        |            1          |            0         |
| L20     | bh                          | test_split_fdr        |             41.51  |          2.06183  |                             1.96  |                         1.65289  |            0.0454393  |            0.0363015 |
| L20     | by_bh                       | test_split_fdr        |             27.165 |          0.398206 |                             0.165 |                         0.398206 |            0.00586823 |            0.0141092 |
| L20     | e_bh_pcal                   | test_split_fdr        |             15     |          0        |                             0     |                         0        |            0          |            0         |
| L20     | p_lt_q                      | test_split_fdr        |             97.575 |          4.51623  |                            25.575 |                         4.51623  |            0.260537   |            0.0341206 |

## Prompt-Resampling Selection Stability

| layer   | estimand                   | method          |   discoveries_mean |   discoveries_std |   jaccard_mean |   jaccard_std |   recall_full_mean |   recall_full_std |   full_discoveries |
|:--------|:---------------------------|:----------------|-------------------:|------------------:|---------------:|--------------:|-------------------:|------------------:|-------------------:|
| L20     | mean_effect                | bh              |             64.94  |         32.5874   |       0.60059  |      0.146195 |           0.839362 |         0.0674766 |                 47 |
| L20     | mean_effect                | by_bh           |             39.05  |         18.2434   |       0.644181 |      0.126324 |           0.882586 |         0.0652341 |                 29 |
| L20     | mean_effect                | e_bh_pcal       |             20.25  |          7.91522  |       0.74468  |      0.116463 |           0.913235 |         0.0634968 |                 17 |
| L20     | mean_effect                | p_lt_q          |             95.575 |         33.0615   |       0.585558 |      0.144428 |           0.821319 |         0.0653034 |                 72 |
| L20     | prompt_tracking_covariance | track_bh        |             13.345 |         35.179    |       0.34663  |      0.300233 |           0.92     |         0.271974  |                  1 |
| L20     | prompt_tracking_covariance | track_by_bh     |              2.365 |          6.44901  |       0.548835 |      0.424327 |           0.755    |         0.431166  |                  1 |
| L20     | prompt_tracking_covariance | track_e_bh_pcal |              0.195 |          0.397195 |       0.805    |      0.397195 |           0.805    |         0.397195  |                  0 |
| L20     | prompt_tracking_covariance | track_p_lt_q    |             48.75  |         41.4482   |       0.198207 |      0.104778 |           0.758333 |         0.16463   |                  9 |

## Real q Grid

| layer   | estimand                   |      q | method                            |   discoveries | selection_rule                     |
|:--------|:---------------------------|-------:|:----------------------------------|--------------:|:-----------------------------------|
| L20     | mean_effect                |   0.01 | e_bh_pcal                         |            12 | fdr_at_q                           |
| L20     | mean_effect                |   0.01 | by_bh                             |            21 | fdr_at_q                           |
| L20     | mean_effect                |   0.01 | bh                                |            27 | fdr_at_q                           |
| L20     | mean_effect                |   0.01 | p_lt_q                            |            40 | uncorrected_p_threshold            |
| L20     | mean_effect                |   0.01 | top_score_matched_e_bh_pcal       |            12 | manual_k_equal_to_e_bh_discoveries |
| L20     | prompt_tracking_covariance |   0.01 | track_e_bh_pcal                   |             0 | fdr_at_q                           |
| L20     | prompt_tracking_covariance |   0.01 | track_by_bh                       |             1 | fdr_at_q                           |
| L20     | prompt_tracking_covariance |   0.01 | track_bh                          |             1 | fdr_at_q                           |
| L20     | prompt_tracking_covariance |   0.01 | track_p_lt_q                      |             5 | uncorrected_p_threshold            |
| L20     | prompt_tracking_covariance |   0.01 | top_score_matched_track_e_bh_pcal |             0 | manual_k_equal_to_e_bh_discoveries |
| L20     | mean_effect                |   0.02 | e_bh_pcal                         |            13 | fdr_at_q                           |
| L20     | mean_effect                |   0.02 | by_bh                             |            22 | fdr_at_q                           |
| L20     | mean_effect                |   0.02 | bh                                |            30 | fdr_at_q                           |
| L20     | mean_effect                |   0.02 | p_lt_q                            |            47 | uncorrected_p_threshold            |
| L20     | mean_effect                |   0.02 | top_score_matched_e_bh_pcal       |            13 | manual_k_equal_to_e_bh_discoveries |
| L20     | prompt_tracking_covariance |   0.02 | track_e_bh_pcal                   |             0 | fdr_at_q                           |
| L20     | prompt_tracking_covariance |   0.02 | track_by_bh                       |             1 | fdr_at_q                           |
| L20     | prompt_tracking_covariance |   0.02 | track_bh                          |             1 | fdr_at_q                           |
| L20     | prompt_tracking_covariance |   0.02 | track_p_lt_q                      |             5 | uncorrected_p_threshold            |
| L20     | prompt_tracking_covariance |   0.02 | top_score_matched_track_e_bh_pcal |             0 | manual_k_equal_to_e_bh_discoveries |
| L20     | mean_effect                |   0.05 | e_bh_pcal                         |            15 | fdr_at_q                           |
| L20     | mean_effect                |   0.05 | by_bh                             |            27 | fdr_at_q                           |
| L20     | mean_effect                |   0.05 | bh                                |            39 | fdr_at_q                           |
| L20     | mean_effect                |   0.05 | p_lt_q                            |            58 | uncorrected_p_threshold            |
| L20     | mean_effect                |   0.05 | top_score_matched_e_bh_pcal       |            15 | manual_k_equal_to_e_bh_discoveries |
| L20     | prompt_tracking_covariance |   0.05 | track_e_bh_pcal                   |             0 | fdr_at_q                           |
| L20     | prompt_tracking_covariance |   0.05 | track_by_bh                       |             1 | fdr_at_q                           |
| L20     | prompt_tracking_covariance |   0.05 | track_bh                          |             1 | fdr_at_q                           |
| L20     | prompt_tracking_covariance |   0.05 | track_p_lt_q                      |             5 | uncorrected_p_threshold            |
| L20     | prompt_tracking_covariance |   0.05 | top_score_matched_track_e_bh_pcal |             0 | manual_k_equal_to_e_bh_discoveries |
| L20     | mean_effect                |   0.1  | e_bh_pcal                         |            17 | fdr_at_q                           |
| L20     | mean_effect                |   0.1  | by_bh                             |            29 | fdr_at_q                           |
| L20     | mean_effect                |   0.1  | bh                                |            47 | fdr_at_q                           |
| L20     | mean_effect                |   0.1  | p_lt_q                            |            72 | uncorrected_p_threshold            |
| L20     | mean_effect                |   0.1  | top_score_matched_e_bh_pcal       |            17 | manual_k_equal_to_e_bh_discoveries |
| L20     | prompt_tracking_covariance |   0.1  | track_e_bh_pcal                   |             0 | fdr_at_q                           |
| L20     | prompt_tracking_covariance |   0.1  | track_by_bh                       |             1 | fdr_at_q                           |
| L20     | prompt_tracking_covariance |   0.1  | track_bh                          |             1 | fdr_at_q                           |
| L20     | prompt_tracking_covariance |   0.1  | track_p_lt_q                      |             9 | uncorrected_p_threshold            |
| L20     | prompt_tracking_covariance |   0.1  | top_score_matched_track_e_bh_pcal |             0 | manual_k_equal_to_e_bh_discoveries |
| L20     | mean_effect                |   0.15 | e_bh_pcal                         |            17 | fdr_at_q                           |
| L20     | mean_effect                |   0.15 | by_bh                             |            30 | fdr_at_q                           |
| L20     | mean_effect                |   0.15 | bh                                |            52 | fdr_at_q                           |
| L20     | mean_effect                |   0.15 | p_lt_q                            |            80 | uncorrected_p_threshold            |
| L20     | mean_effect                |   0.15 | top_score_matched_e_bh_pcal       |            17 | manual_k_equal_to_e_bh_discoveries |
| L20     | prompt_tracking_covariance |   0.15 | track_e_bh_pcal                   |             0 | fdr_at_q                           |
| L20     | prompt_tracking_covariance |   0.15 | track_by_bh                       |             1 | fdr_at_q                           |
| L20     | prompt_tracking_covariance |   0.15 | track_bh                          |             2 | fdr_at_q                           |
| L20     | prompt_tracking_covariance |   0.15 | track_p_lt_q                      |            15 | uncorrected_p_threshold            |
| L20     | prompt_tracking_covariance |   0.15 | top_score_matched_track_e_bh_pcal |             0 | manual_k_equal_to_e_bh_discoveries |
| L20     | mean_effect                |   0.2  | e_bh_pcal                         |            18 | fdr_at_q                           |
| L20     | mean_effect                |   0.2  | by_bh                             |            34 | fdr_at_q                           |
| L20     | mean_effect                |   0.2  | bh                                |            57 | fdr_at_q                           |
| L20     | mean_effect                |   0.2  | p_lt_q                            |            92 | uncorrected_p_threshold            |
| L20     | mean_effect                |   0.2  | top_score_matched_e_bh_pcal       |            18 | manual_k_equal_to_e_bh_discoveries |
| L20     | prompt_tracking_covariance |   0.2  | track_e_bh_pcal                   |             0 | fdr_at_q                           |
| L20     | prompt_tracking_covariance |   0.2  | track_by_bh                       |             1 | fdr_at_q                           |
| L20     | prompt_tracking_covariance |   0.2  | track_bh                          |             2 | fdr_at_q                           |
| L20     | prompt_tracking_covariance |   0.2  | track_p_lt_q                      |            22 | uncorrected_p_threshold            |
| L20     | prompt_tracking_covariance |   0.2  | top_score_matched_track_e_bh_pcal |             0 | manual_k_equal_to_e_bh_discoveries |
| L20     | mean_effect                |   0.3  | e_bh_pcal                         |            21 | fdr_at_q                           |
| L20     | mean_effect                |   0.3  | by_bh                             |            38 | fdr_at_q                           |
| L20     | mean_effect                |   0.3  | bh                                |            68 | fdr_at_q                           |
| L20     | mean_effect                |   0.3  | p_lt_q                            |           108 | uncorrected_p_threshold            |
| L20     | mean_effect                |   0.3  | top_score_matched_e_bh_pcal       |            21 | manual_k_equal_to_e_bh_discoveries |
| L20     | prompt_tracking_covariance |   0.3  | track_e_bh_pcal                   |             0 | fdr_at_q                           |
| L20     | prompt_tracking_covariance |   0.3  | track_by_bh                       |             1 | fdr_at_q                           |
| L20     | prompt_tracking_covariance |   0.3  | track_bh                          |             2 | fdr_at_q                           |
| L20     | prompt_tracking_covariance |   0.3  | track_p_lt_q                      |            41 | uncorrected_p_threshold            |
| L20     | prompt_tracking_covariance |   0.3  | top_score_matched_track_e_bh_pcal |             0 | manual_k_equal_to_e_bh_discoveries |
| L20     | screen_score               | nan    | top_score_fixed_k_1               |             1 | manual_k_no_fdr_target             |
| L20     | screen_score               | nan    | top_score_fixed_k_5               |             5 | manual_k_no_fdr_target             |
| L20     | screen_score               | nan    | top_score_fixed_k_7               |             7 | manual_k_no_fdr_target             |
| L20     | screen_score               | nan    | top_score_fixed_k_10              |            10 | manual_k_no_fdr_target             |
| L20     | screen_score               | nan    | top_score_fixed_k_17              |            17 | manual_k_no_fdr_target             |
| L20     | screen_score               | nan    | top_score_fixed_k_29              |            29 | manual_k_no_fdr_target             |
| L20     | screen_score               | nan    | top_score_fixed_k_54              |            54 | manual_k_no_fdr_target             |
| L20     | screen_score               | nan    | top_score_fixed_k_100             |           100 | manual_k_no_fdr_target             |
| L20     | screen_score               | nan    | top_score_fixed_k_256             |           256 | manual_k_no_fdr_target             |

## Layer Scan Metrics

| layer   | method                |   discoveries |   completeness_r2 |   centered_r2 |   selected_full_corr |   abs_effect_fraction |   sign_agreement |
|:--------|:----------------------|--------------:|------------------:|--------------:|---------------------:|----------------------:|-----------------:|
| L20     | bh                    |            47 |          0.590788 |      -3.62592 |           0.380065   |              0.401251 |          0.99375 |
| L20     | by_bh                 |            29 |          0.552124 |      -4.06299 |           0.166355   |              0.377748 |          0.99375 |
| L20     | e_bh_pcal             |            17 |          0.521452 |      -4.40972 |           0.149339   |              0.350849 |          0.99375 |
| L20     | p_lt_q                |            72 |          0.59244  |      -3.60724 |           0.394575   |              0.40066  |          1       |
| L20     | top_score_k_256       |           nan |          0.594259 |      -3.58668 |           0.405365   |              0.401172 |          1       |
| L20     | top_score_k_e_bh_pcal |           nan |          0.436537 |      -5.36964 |           0.00798189 |              0.294398 |          0.98125 |
| L20     | track_e_bh_pcal       |             0 |          0        |     -10.3044  |         nan          |              0        |          0       |
