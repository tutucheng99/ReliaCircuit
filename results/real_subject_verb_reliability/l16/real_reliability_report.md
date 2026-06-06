# Real Subject-Verb Reliability: L16

## Null Decoy Reliability

| layer   | method                      | selection_rule        |   discoveries_mean |   discoveries_std |   known_null_decoys_selected_mean |   known_null_decoys_selected_std |   known_null_fdp_mean |   known_null_fdp_std |
|:--------|:----------------------------|:----------------------|-------------------:|------------------:|----------------------------------:|---------------------------------:|----------------------:|---------------------:|
| L16     | top_score_fixed_k_256       | screen_score_manual_k |            256     |          0        |                           256     |                         0        |            1          |            0         |
| L16     | top_score_fixed_k_7         | screen_score_manual_k |              7     |          0        |                             7     |                         0        |            1          |            0         |
| L16     | top_score_matched_bh        | screen_score_manual_k |             45.17  |          2.80722  |                            45.17  |                         2.80722  |            1          |            0         |
| L16     | top_score_matched_e_bh_pcal | screen_score_manual_k |             23     |          0        |                            23     |                         0        |            1          |            0         |
| L16     | bh                          | test_split_fdr        |             45.17  |          2.80722  |                             2.465 |                         1.67715  |            0.0526854  |            0.0322215 |
| L16     | by_bh                       | test_split_fdr        |             31.435 |          0.877282 |                             0.23  |                         0.488151 |            0.00691698 |            0.014551  |
| L16     | e_bh_pcal                   | test_split_fdr        |             23     |          0        |                             0     |                         0        |            0          |            0         |
| L16     | p_lt_q                      | test_split_fdr        |            115.135 |          4.48524  |                            25.135 |                         4.48524  |            0.217131   |            0.0304367 |

## Prompt-Resampling Selection Stability

| layer   | estimand                   | method          |   discoveries_mean |   discoveries_std |   jaccard_mean |   jaccard_std |   recall_full_mean |   recall_full_std |   full_discoveries |
|:--------|:---------------------------|:----------------|-------------------:|------------------:|---------------:|--------------:|-------------------:|------------------:|-------------------:|
| L16     | mean_effect                | bh              |             74.14  |         18.8173   |       0.591949 |     0.114727  |           0.887647 |         0.0451988 |                 51 |
| L16     | mean_effect                | by_bh           |             45.795 |          9.98657  |       0.688501 |     0.109973  |           0.896622 |         0.0426206 |                 37 |
| L16     | mean_effect                | e_bh_pcal       |             27.215 |          3.35036  |       0.807722 |     0.085198  |           0.969348 |         0.0328492 |                 23 |
| L16     | mean_effect                | p_lt_q          |            104.105 |         16.8088   |       0.610747 |     0.108241  |           0.806333 |         0.0743941 |                 90 |
| L16     | prompt_tracking_covariance | track_bh        |             49.67  |         53.1187   |       0.276919 |     0.161411  |           0.745    |         0.239345  |                 11 |
| L16     | prompt_tracking_covariance | track_by_bh     |             13.62  |         20.3839   |       0.324405 |     0.246396  |           0.8775   |         0.215583  |                  2 |
| L16     | prompt_tracking_covariance | track_e_bh_pcal |              1.165 |          0.700162 |       0.85625  |     0.299233  |           0.94     |         0.238083  |                  1 |
| L16     | prompt_tracking_covariance | track_p_lt_q    |             93.655 |         48.5123   |       0.414967 |     0.0959946 |           0.732667 |         0.209496  |                 60 |

## Real q Grid

| layer   | estimand                   |      q | method                            |   discoveries | selection_rule                     |
|:--------|:---------------------------|-------:|:----------------------------------|--------------:|:-----------------------------------|
| L16     | mean_effect                |   0.01 | e_bh_pcal                         |            20 | fdr_at_q                           |
| L16     | mean_effect                |   0.01 | by_bh                             |            28 | fdr_at_q                           |
| L16     | mean_effect                |   0.01 | bh                                |            36 | fdr_at_q                           |
| L16     | mean_effect                |   0.01 | p_lt_q                            |            45 | uncorrected_p_threshold            |
| L16     | mean_effect                |   0.01 | top_score_matched_e_bh_pcal       |            20 | manual_k_equal_to_e_bh_discoveries |
| L16     | prompt_tracking_covariance |   0.01 | track_e_bh_pcal                   |             1 | fdr_at_q                           |
| L16     | prompt_tracking_covariance |   0.01 | track_by_bh                       |             1 | fdr_at_q                           |
| L16     | prompt_tracking_covariance |   0.01 | track_bh                          |             2 | fdr_at_q                           |
| L16     | prompt_tracking_covariance |   0.01 | track_p_lt_q                      |            13 | uncorrected_p_threshold            |
| L16     | prompt_tracking_covariance |   0.01 | top_score_matched_track_e_bh_pcal |             1 | manual_k_equal_to_e_bh_discoveries |
| L16     | mean_effect                |   0.02 | e_bh_pcal                         |            22 | fdr_at_q                           |
| L16     | mean_effect                |   0.02 | by_bh                             |            29 | fdr_at_q                           |
| L16     | mean_effect                |   0.02 | bh                                |            38 | fdr_at_q                           |
| L16     | mean_effect                |   0.02 | p_lt_q                            |            51 | uncorrected_p_threshold            |
| L16     | mean_effect                |   0.02 | top_score_matched_e_bh_pcal       |            22 | manual_k_equal_to_e_bh_discoveries |
| L16     | prompt_tracking_covariance |   0.02 | track_e_bh_pcal                   |             1 | fdr_at_q                           |
| L16     | prompt_tracking_covariance |   0.02 | track_by_bh                       |             1 | fdr_at_q                           |
| L16     | prompt_tracking_covariance |   0.02 | track_bh                          |             3 | fdr_at_q                           |
| L16     | prompt_tracking_covariance |   0.02 | track_p_lt_q                      |            25 | uncorrected_p_threshold            |
| L16     | prompt_tracking_covariance |   0.02 | top_score_matched_track_e_bh_pcal |             1 | manual_k_equal_to_e_bh_discoveries |
| L16     | mean_effect                |   0.05 | e_bh_pcal                         |            23 | fdr_at_q                           |
| L16     | mean_effect                |   0.05 | by_bh                             |            32 | fdr_at_q                           |
| L16     | mean_effect                |   0.05 | bh                                |            42 | fdr_at_q                           |
| L16     | mean_effect                |   0.05 | p_lt_q                            |            69 | uncorrected_p_threshold            |
| L16     | mean_effect                |   0.05 | top_score_matched_e_bh_pcal       |            23 | manual_k_equal_to_e_bh_discoveries |
| L16     | prompt_tracking_covariance |   0.05 | track_e_bh_pcal                   |             1 | fdr_at_q                           |
| L16     | prompt_tracking_covariance |   0.05 | track_by_bh                       |             2 | fdr_at_q                           |
| L16     | prompt_tracking_covariance |   0.05 | track_bh                          |             5 | fdr_at_q                           |
| L16     | prompt_tracking_covariance |   0.05 | track_p_lt_q                      |            38 | uncorrected_p_threshold            |
| L16     | prompt_tracking_covariance |   0.05 | top_score_matched_track_e_bh_pcal |             1 | manual_k_equal_to_e_bh_discoveries |
| L16     | mean_effect                |   0.1  | e_bh_pcal                         |            23 | fdr_at_q                           |
| L16     | mean_effect                |   0.1  | by_bh                             |            37 | fdr_at_q                           |
| L16     | mean_effect                |   0.1  | bh                                |            51 | fdr_at_q                           |
| L16     | mean_effect                |   0.1  | p_lt_q                            |            90 | uncorrected_p_threshold            |
| L16     | mean_effect                |   0.1  | top_score_matched_e_bh_pcal       |            23 | manual_k_equal_to_e_bh_discoveries |
| L16     | prompt_tracking_covariance |   0.1  | track_e_bh_pcal                   |             1 | fdr_at_q                           |
| L16     | prompt_tracking_covariance |   0.1  | track_by_bh                       |             2 | fdr_at_q                           |
| L16     | prompt_tracking_covariance |   0.1  | track_bh                          |            11 | fdr_at_q                           |
| L16     | prompt_tracking_covariance |   0.1  | track_p_lt_q                      |            60 | uncorrected_p_threshold            |
| L16     | prompt_tracking_covariance |   0.1  | top_score_matched_track_e_bh_pcal |             1 | manual_k_equal_to_e_bh_discoveries |
| L16     | mean_effect                |   0.15 | e_bh_pcal                         |            26 | fdr_at_q                           |
| L16     | mean_effect                |   0.15 | by_bh                             |            39 | fdr_at_q                           |
| L16     | mean_effect                |   0.15 | bh                                |            61 | fdr_at_q                           |
| L16     | mean_effect                |   0.15 | p_lt_q                            |           105 | uncorrected_p_threshold            |
| L16     | mean_effect                |   0.15 | top_score_matched_e_bh_pcal       |            26 | manual_k_equal_to_e_bh_discoveries |
| L16     | prompt_tracking_covariance |   0.15 | track_e_bh_pcal                   |             1 | fdr_at_q                           |
| L16     | prompt_tracking_covariance |   0.15 | track_by_bh                       |             3 | fdr_at_q                           |
| L16     | prompt_tracking_covariance |   0.15 | track_bh                          |            12 | fdr_at_q                           |
| L16     | prompt_tracking_covariance |   0.15 | track_p_lt_q                      |            79 | uncorrected_p_threshold            |
| L16     | prompt_tracking_covariance |   0.15 | top_score_matched_track_e_bh_pcal |             1 | manual_k_equal_to_e_bh_discoveries |
| L16     | mean_effect                |   0.2  | e_bh_pcal                         |            27 | fdr_at_q                           |
| L16     | mean_effect                |   0.2  | by_bh                             |            40 | fdr_at_q                           |
| L16     | mean_effect                |   0.2  | bh                                |            80 | fdr_at_q                           |
| L16     | mean_effect                |   0.2  | p_lt_q                            |           111 | uncorrected_p_threshold            |
| L16     | mean_effect                |   0.2  | top_score_matched_e_bh_pcal       |            27 | manual_k_equal_to_e_bh_discoveries |
| L16     | prompt_tracking_covariance |   0.2  | track_e_bh_pcal                   |             1 | fdr_at_q                           |
| L16     | prompt_tracking_covariance |   0.2  | track_by_bh                       |             3 | fdr_at_q                           |
| L16     | prompt_tracking_covariance |   0.2  | track_bh                          |            25 | fdr_at_q                           |
| L16     | prompt_tracking_covariance |   0.2  | track_p_lt_q                      |           104 | uncorrected_p_threshold            |
| L16     | prompt_tracking_covariance |   0.2  | top_score_matched_track_e_bh_pcal |             1 | manual_k_equal_to_e_bh_discoveries |
| L16     | mean_effect                |   0.3  | e_bh_pcal                         |            29 | fdr_at_q                           |
| L16     | mean_effect                |   0.3  | by_bh                             |            42 | fdr_at_q                           |
| L16     | mean_effect                |   0.3  | bh                                |            90 | fdr_at_q                           |
| L16     | mean_effect                |   0.3  | p_lt_q                            |           138 | uncorrected_p_threshold            |
| L16     | mean_effect                |   0.3  | top_score_matched_e_bh_pcal       |            29 | manual_k_equal_to_e_bh_discoveries |
| L16     | prompt_tracking_covariance |   0.3  | track_e_bh_pcal                   |             1 | fdr_at_q                           |
| L16     | prompt_tracking_covariance |   0.3  | track_by_bh                       |             5 | fdr_at_q                           |
| L16     | prompt_tracking_covariance |   0.3  | track_bh                          |            33 | fdr_at_q                           |
| L16     | prompt_tracking_covariance |   0.3  | track_p_lt_q                      |           146 | uncorrected_p_threshold            |
| L16     | prompt_tracking_covariance |   0.3  | top_score_matched_track_e_bh_pcal |             1 | manual_k_equal_to_e_bh_discoveries |
| L16     | screen_score               | nan    | top_score_fixed_k_1               |             1 | manual_k_no_fdr_target             |
| L16     | screen_score               | nan    | top_score_fixed_k_5               |             5 | manual_k_no_fdr_target             |
| L16     | screen_score               | nan    | top_score_fixed_k_7               |             7 | manual_k_no_fdr_target             |
| L16     | screen_score               | nan    | top_score_fixed_k_10              |            10 | manual_k_no_fdr_target             |
| L16     | screen_score               | nan    | top_score_fixed_k_17              |            17 | manual_k_no_fdr_target             |
| L16     | screen_score               | nan    | top_score_fixed_k_29              |            29 | manual_k_no_fdr_target             |
| L16     | screen_score               | nan    | top_score_fixed_k_54              |            54 | manual_k_no_fdr_target             |
| L16     | screen_score               | nan    | top_score_fixed_k_100             |           100 | manual_k_no_fdr_target             |
| L16     | screen_score               | nan    | top_score_fixed_k_256             |           256 | manual_k_no_fdr_target             |

## Layer Scan Metrics

| layer   | method                |   discoveries |   completeness_r2 |   centered_r2 |   selected_full_corr |   abs_effect_fraction |   sign_agreement |
|:--------|:----------------------|--------------:|------------------:|--------------:|---------------------:|----------------------:|-----------------:|
| L16     | bh                    |            51 |          0.96508  |      0.605245 |             0.787874 |              0.972572 |                1 |
| L16     | by_bh                 |            37 |          0.96206  |      0.57111  |             0.771956 |              0.964109 |                1 |
| L16     | e_bh_pcal             |            23 |          0.963221 |      0.58423  |             0.780224 |              0.958715 |                1 |
| L16     | p_lt_q                |            90 |          0.966535 |      0.621701 |             0.803314 |              0.960768 |                1 |
| L16     | top_score_k_256       |           nan |          0.964158 |      0.594825 |             0.791069 |              1.00464  |                1 |
| L16     | top_score_k_e_bh_pcal |           nan |          0.964459 |      0.598225 |             0.807632 |              0.93242  |                1 |
| L16     | track_e_bh_pcal       |             1 |          0.571944 |     -3.83893  |             0.549454 |              0.366182 |                1 |
