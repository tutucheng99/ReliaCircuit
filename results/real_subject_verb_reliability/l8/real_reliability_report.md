# Real Subject-Verb Reliability: L8

## Null Decoy Reliability

| layer   | method                      | selection_rule        |   discoveries_mean |   discoveries_std |   known_null_decoys_selected_mean |   known_null_decoys_selected_std |   known_null_fdp_mean |   known_null_fdp_std |
|:--------|:----------------------------|:----------------------|-------------------:|------------------:|----------------------------------:|---------------------------------:|----------------------:|---------------------:|
| L8      | top_score_fixed_k_256       | screen_score_manual_k |            256     |          0        |                           256     |                         0        |            1          |            0         |
| L8      | top_score_fixed_k_7         | screen_score_manual_k |              7     |          0        |                             7     |                         0        |            1          |            0         |
| L8      | top_score_matched_bh        | screen_score_manual_k |             12.695 |          0.863541 |                            12.695 |                         0.863541 |            1          |            0         |
| L8      | top_score_matched_e_bh_pcal | screen_score_manual_k |              3     |          0        |                             3     |                         0        |            1          |            0         |
| L8      | bh                          | test_split_fdr        |             12.695 |          0.863541 |                             0.69  |                         0.841093 |            0.0504292  |            0.0586278 |
| L8      | by_bh                       | test_split_fdr        |              8.095 |          0.341406 |                             0.09  |                         0.303911 |            0.00979798 |            0.0325922 |
| L8      | e_bh_pcal                   | test_split_fdr        |              3     |          0        |                             0     |                         0        |            0          |            0         |
| L8      | p_lt_q                      | test_split_fdr        |             77.305 |          4.6917   |                            25.305 |                         4.6917   |            0.32486    |            0.0411891 |

## Prompt-Resampling Selection Stability

| layer   | estimand                   | method          |   discoveries_mean |   discoveries_std |   jaccard_mean |   jaccard_std |   recall_full_mean |   recall_full_std |   full_discoveries |
|:--------|:---------------------------|:----------------|-------------------:|------------------:|---------------:|--------------:|-------------------:|------------------:|-------------------:|
| L8      | mean_effect                | bh              |             43.615 |         40.0759   |       0.421538 |     0.192845  |           0.862333 |          0.100268 |                 15 |
| L8      | mean_effect                | by_bh           |             18.4   |         15.7751   |       0.541111 |     0.19166   |           0.910556 |          0.1101   |                  9 |
| L8      | mean_effect                | e_bh_pcal       |              5.405 |          1.43572  |       0.672182 |     0.156743  |           0.750833 |          0.129421 |                  6 |
| L8      | mean_effect                | p_lt_q          |             83.7   |         38.7812   |       0.456414 |     0.120314  |           0.775385 |          0.143571 |                 52 |
| L8      | prompt_tracking_covariance | track_bh        |             13.325 |         28.0473   |       0.368323 |     0.329991  |           1        |          0        |                  1 |
| L8      | prompt_tracking_covariance | track_by_bh     |              2.495 |          3.96213  |       0.682334 |     0.329382  |           1        |          0        |                  1 |
| L8      | prompt_tracking_covariance | track_e_bh_pcal |              1.015 |          0.121857 |       0.9925   |     0.0609287 |           1        |          0        |                  1 |
| L8      | prompt_tracking_covariance | track_p_lt_q    |             58.335 |         36.2352   |       0.279498 |     0.147685  |           0.6815   |          0.179426 |                 20 |

## Real q Grid

| layer   | estimand                   |      q | method                            |   discoveries | selection_rule                     |
|:--------|:---------------------------|-------:|:----------------------------------|--------------:|:-----------------------------------|
| L8      | mean_effect                |   0.01 | e_bh_pcal                         |             3 | fdr_at_q                           |
| L8      | mean_effect                |   0.01 | by_bh                             |             7 | fdr_at_q                           |
| L8      | mean_effect                |   0.01 | bh                                |             9 | fdr_at_q                           |
| L8      | mean_effect                |   0.01 | p_lt_q                            |            18 | uncorrected_p_threshold            |
| L8      | mean_effect                |   0.01 | top_score_matched_e_bh_pcal       |             3 | manual_k_equal_to_e_bh_discoveries |
| L8      | prompt_tracking_covariance |   0.01 | track_e_bh_pcal                   |             1 | fdr_at_q                           |
| L8      | prompt_tracking_covariance |   0.01 | track_by_bh                       |             1 | fdr_at_q                           |
| L8      | prompt_tracking_covariance |   0.01 | track_bh                          |             1 | fdr_at_q                           |
| L8      | prompt_tracking_covariance |   0.01 | track_p_lt_q                      |             3 | uncorrected_p_threshold            |
| L8      | prompt_tracking_covariance |   0.01 | top_score_matched_track_e_bh_pcal |             1 | manual_k_equal_to_e_bh_discoveries |
| L8      | mean_effect                |   0.02 | e_bh_pcal                         |             3 | fdr_at_q                           |
| L8      | mean_effect                |   0.02 | by_bh                             |             8 | fdr_at_q                           |
| L8      | mean_effect                |   0.02 | bh                                |             9 | fdr_at_q                           |
| L8      | mean_effect                |   0.02 | p_lt_q                            |            26 | uncorrected_p_threshold            |
| L8      | mean_effect                |   0.02 | top_score_matched_e_bh_pcal       |             3 | manual_k_equal_to_e_bh_discoveries |
| L8      | prompt_tracking_covariance |   0.02 | track_e_bh_pcal                   |             1 | fdr_at_q                           |
| L8      | prompt_tracking_covariance |   0.02 | track_by_bh                       |             1 | fdr_at_q                           |
| L8      | prompt_tracking_covariance |   0.02 | track_bh                          |             1 | fdr_at_q                           |
| L8      | prompt_tracking_covariance |   0.02 | track_p_lt_q                      |             6 | uncorrected_p_threshold            |
| L8      | prompt_tracking_covariance |   0.02 | top_score_matched_track_e_bh_pcal |             1 | manual_k_equal_to_e_bh_discoveries |
| L8      | mean_effect                |   0.05 | e_bh_pcal                         |             3 | fdr_at_q                           |
| L8      | mean_effect                |   0.05 | by_bh                             |             8 | fdr_at_q                           |
| L8      | mean_effect                |   0.05 | bh                                |            12 | fdr_at_q                           |
| L8      | mean_effect                |   0.05 | p_lt_q                            |            37 | uncorrected_p_threshold            |
| L8      | mean_effect                |   0.05 | top_score_matched_e_bh_pcal       |             3 | manual_k_equal_to_e_bh_discoveries |
| L8      | prompt_tracking_covariance |   0.05 | track_e_bh_pcal                   |             1 | fdr_at_q                           |
| L8      | prompt_tracking_covariance |   0.05 | track_by_bh                       |             1 | fdr_at_q                           |
| L8      | prompt_tracking_covariance |   0.05 | track_bh                          |             1 | fdr_at_q                           |
| L8      | prompt_tracking_covariance |   0.05 | track_p_lt_q                      |            12 | uncorrected_p_threshold            |
| L8      | prompt_tracking_covariance |   0.05 | top_score_matched_track_e_bh_pcal |             1 | manual_k_equal_to_e_bh_discoveries |
| L8      | mean_effect                |   0.1  | e_bh_pcal                         |             6 | fdr_at_q                           |
| L8      | mean_effect                |   0.1  | by_bh                             |             9 | fdr_at_q                           |
| L8      | mean_effect                |   0.1  | bh                                |            15 | fdr_at_q                           |
| L8      | mean_effect                |   0.1  | p_lt_q                            |            52 | uncorrected_p_threshold            |
| L8      | mean_effect                |   0.1  | top_score_matched_e_bh_pcal       |             6 | manual_k_equal_to_e_bh_discoveries |
| L8      | prompt_tracking_covariance |   0.1  | track_e_bh_pcal                   |             1 | fdr_at_q                           |
| L8      | prompt_tracking_covariance |   0.1  | track_by_bh                       |             1 | fdr_at_q                           |
| L8      | prompt_tracking_covariance |   0.1  | track_bh                          |             1 | fdr_at_q                           |
| L8      | prompt_tracking_covariance |   0.1  | track_p_lt_q                      |            20 | uncorrected_p_threshold            |
| L8      | prompt_tracking_covariance |   0.1  | top_score_matched_track_e_bh_pcal |             1 | manual_k_equal_to_e_bh_discoveries |
| L8      | mean_effect                |   0.15 | e_bh_pcal                         |             6 | fdr_at_q                           |
| L8      | mean_effect                |   0.15 | by_bh                             |             9 | fdr_at_q                           |
| L8      | mean_effect                |   0.15 | bh                                |            19 | fdr_at_q                           |
| L8      | mean_effect                |   0.15 | p_lt_q                            |            68 | uncorrected_p_threshold            |
| L8      | mean_effect                |   0.15 | top_score_matched_e_bh_pcal       |             6 | manual_k_equal_to_e_bh_discoveries |
| L8      | prompt_tracking_covariance |   0.15 | track_e_bh_pcal                   |             1 | fdr_at_q                           |
| L8      | prompt_tracking_covariance |   0.15 | track_by_bh                       |             1 | fdr_at_q                           |
| L8      | prompt_tracking_covariance |   0.15 | track_bh                          |             1 | fdr_at_q                           |
| L8      | prompt_tracking_covariance |   0.15 | track_p_lt_q                      |            22 | uncorrected_p_threshold            |
| L8      | prompt_tracking_covariance |   0.15 | top_score_matched_track_e_bh_pcal |             1 | manual_k_equal_to_e_bh_discoveries |
| L8      | mean_effect                |   0.2  | e_bh_pcal                         |             6 | fdr_at_q                           |
| L8      | mean_effect                |   0.2  | by_bh                             |            11 | fdr_at_q                           |
| L8      | mean_effect                |   0.2  | bh                                |            26 | fdr_at_q                           |
| L8      | mean_effect                |   0.2  | p_lt_q                            |            86 | uncorrected_p_threshold            |
| L8      | mean_effect                |   0.2  | top_score_matched_e_bh_pcal       |             6 | manual_k_equal_to_e_bh_discoveries |
| L8      | prompt_tracking_covariance |   0.2  | track_e_bh_pcal                   |             1 | fdr_at_q                           |
| L8      | prompt_tracking_covariance |   0.2  | track_by_bh                       |             1 | fdr_at_q                           |
| L8      | prompt_tracking_covariance |   0.2  | track_bh                          |             1 | fdr_at_q                           |
| L8      | prompt_tracking_covariance |   0.2  | track_p_lt_q                      |            30 | uncorrected_p_threshold            |
| L8      | prompt_tracking_covariance |   0.2  | top_score_matched_track_e_bh_pcal |             1 | manual_k_equal_to_e_bh_discoveries |
| L8      | mean_effect                |   0.3  | e_bh_pcal                         |             7 | fdr_at_q                           |
| L8      | mean_effect                |   0.3  | by_bh                             |            12 | fdr_at_q                           |
| L8      | mean_effect                |   0.3  | bh                                |            34 | fdr_at_q                           |
| L8      | mean_effect                |   0.3  | p_lt_q                            |           115 | uncorrected_p_threshold            |
| L8      | mean_effect                |   0.3  | top_score_matched_e_bh_pcal       |             7 | manual_k_equal_to_e_bh_discoveries |
| L8      | prompt_tracking_covariance |   0.3  | track_e_bh_pcal                   |             1 | fdr_at_q                           |
| L8      | prompt_tracking_covariance |   0.3  | track_by_bh                       |             1 | fdr_at_q                           |
| L8      | prompt_tracking_covariance |   0.3  | track_bh                          |             1 | fdr_at_q                           |
| L8      | prompt_tracking_covariance |   0.3  | track_p_lt_q                      |            52 | uncorrected_p_threshold            |
| L8      | prompt_tracking_covariance |   0.3  | top_score_matched_track_e_bh_pcal |             1 | manual_k_equal_to_e_bh_discoveries |
| L8      | screen_score               | nan    | top_score_fixed_k_1               |             1 | manual_k_no_fdr_target             |
| L8      | screen_score               | nan    | top_score_fixed_k_5               |             5 | manual_k_no_fdr_target             |
| L8      | screen_score               | nan    | top_score_fixed_k_7               |             7 | manual_k_no_fdr_target             |
| L8      | screen_score               | nan    | top_score_fixed_k_10              |            10 | manual_k_no_fdr_target             |
| L8      | screen_score               | nan    | top_score_fixed_k_17              |            17 | manual_k_no_fdr_target             |
| L8      | screen_score               | nan    | top_score_fixed_k_29              |            29 | manual_k_no_fdr_target             |
| L8      | screen_score               | nan    | top_score_fixed_k_54              |            54 | manual_k_no_fdr_target             |
| L8      | screen_score               | nan    | top_score_fixed_k_100             |           100 | manual_k_no_fdr_target             |
| L8      | screen_score               | nan    | top_score_fixed_k_256             |           256 | manual_k_no_fdr_target             |

## Layer Scan Metrics

| layer   | method                |   discoveries |   completeness_r2 |   centered_r2 |   selected_full_corr |   abs_effect_fraction |   sign_agreement |
|:--------|:----------------------|--------------:|------------------:|--------------:|---------------------:|----------------------:|-----------------:|
| L8      | bh                    |            15 |          0.967631 |      0.634089 |             0.815213 |              0.968441 |                1 |
| L8      | by_bh                 |             9 |          0.967803 |      0.636035 |             0.814877 |              0.969702 |                1 |
| L8      | e_bh_pcal             |             6 |          0.968474 |      0.643614 |             0.816815 |              0.975706 |                1 |
| L8      | p_lt_q                |            52 |          0.965134 |      0.605865 |             0.810084 |              0.950854 |                1 |
| L8      | top_score_k_256       |           nan |          0.963671 |      0.589315 |             0.799335 |              0.960985 |                1 |
| L8      | top_score_k_e_bh_pcal |           nan |          0.963372 |      0.585936 |             0.792131 |              0.949334 |                1 |
| L8      | track_e_bh_pcal       |             1 |          0.950063 |      0.435492 |             0.739686 |              0.906093 |                1 |
