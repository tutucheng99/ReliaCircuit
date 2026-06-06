# Paper Asset Index

This folder contains compact tables and an artifact inventory generated
from the current experiment outputs. It is for paper writing support, not
paper prose.

## Tables

### table_1_gate_b_fdr_ci

| method             |   discoveries_mean |   fdp_mean |   power_mean |   ci_coverage_screened_mean |   ci_coverage_selected_mean |
|:-------------------|-------------------:|-----------:|-------------:|----------------------------:|----------------------------:|
| e_bh_pcal          |             19.325 |     0.0013 |       0.8042 |                      0.9628 |                      0.9741 |
| by_bh              |             19.6   |     0.0144 |       0.8042 |                      0.9628 |                      0.9627 |
| bh                 |             21.4   |     0.0931 |       0.8042 |                      0.9628 |                      0.917  |
| p_lt_q             |             27.35  |     0.2885 |       0.8042 |                      0.9628 |                      0.888  |
| top_score_k_active |             24     |     0.4771 |       0.5229 |                      0.9628 |                      0.9646 |

### table_2_q_grid

|    q | method    |   fdp_mean |   power_mean |   discoveries_mean |
|-----:|:----------|-----------:|-------------:|-------------------:|
| 0.02 | e_bh_pcal |     0      |       0.8042 |             19.3   |
| 0.02 | by_bh     |     0.0038 |       0.8042 |             19.375 |
| 0.02 | bh        |     0.0144 |       0.8042 |             19.6   |
| 0.02 | p_lt_q    |     0.0833 |       0.8042 |             21.15  |
| 0.05 | e_bh_pcal |     0      |       0.8042 |             19.3   |
| 0.05 | by_bh     |     0.0075 |       0.8042 |             19.45  |
| 0.05 | bh        |     0.0398 |       0.8042 |             20.15  |
| 0.05 | p_lt_q    |     0.1672 |       0.8042 |             23.35  |
| 0.1  | e_bh_pcal |     0.0013 |       0.8042 |             19.325 |
| 0.1  | by_bh     |     0.0144 |       0.8042 |             19.6   |
| 0.1  | bh        |     0.0931 |       0.8042 |             21.4   |
| 0.1  | p_lt_q    |     0.2885 |       0.8042 |             27.35  |
| 0.15 | e_bh_pcal |     0.0013 |       0.8042 |             19.325 |
| 0.15 | by_bh     |     0.0238 |       0.8042 |             19.8   |
| 0.15 | bh        |     0.1314 |       0.8042 |             22.4   |
| 0.15 | p_lt_q    |     0.3741 |       0.8042 |             31.175 |
| 0.2  | e_bh_pcal |     0.0026 |       0.8042 |             19.35  |
| 0.2  | by_bh     |     0.033  |       0.8042 |             20     |
| 0.2  | bh        |     0.171  |       0.8042 |             23.525 |
| 0.2  | p_lt_q    |     0.439  |       0.8042 |             34.8   |

### table_3_synthetic_frontier

| scenario        | method             |   fdp_mean |   power_mean |   screen_recall_mean |   ci_coverage_screened_mean |
|:----------------|:-------------------|-----------:|-------------:|---------------------:|----------------------------:|
| nominal         | e_bh_pcal          |     0      |       0.7526 |               0.7526 |                      0.9531 |
| nominal         | p_lt_q             |     0.2657 |       0.7526 |               0.7526 |                      0.9531 |
| nominal         | top_score_k_active |     0.5547 |       0.4453 |               0.7526 |                      0.9531 |
| high_dependence | e_bh_pcal          |     0      |       0.3724 |               0.3724 |                      0.9518 |
| high_dependence | p_lt_q             |     0.4735 |       0.3724 |               0.3724 |                      0.9518 |
| high_dependence | top_score_k_active |     0.8698 |       0.1302 |               0.3724 |                      0.9518 |
| weak_effect     | e_bh_pcal          |     0      |       0.7552 |               0.7552 |                      0.9538 |
| weak_effect     | p_lt_q             |     0.2981 |       0.7552 |               0.7552 |                      0.9538 |
| weak_effect     | top_score_k_active |     0.5677 |       0.4323 |               0.7552 |                      0.9538 |
| narrow_screen   | e_bh_pcal          |     0      |       0.5938 |               0.5938 |                      0.9557 |
| narrow_screen   | p_lt_q             |     0.1717 |       0.5938 |               0.5938 |                      0.9557 |
| narrow_screen   | top_score_k_active |     0.5547 |       0.4453 |               0.5938 |                      0.9557 |
| high_nuisance   | e_bh_pcal          |     0      |       0.7526 |               0.7526 |                      0.9544 |
| high_nuisance   | p_lt_q             |     0.2657 |       0.7526 |               0.7526 |                      0.9544 |
| high_nuisance   | top_score_k_active |     0.5547 |       0.4453 |               0.7526 |                      0.9544 |

### table_4_circuit_metrics

| method             |   completeness_r2_mean |   necessity_fraction_mean |   selected_full_corr_mean |   sign_agreement_mean |
|:-------------------|-----------------------:|--------------------------:|--------------------------:|----------------------:|
| e_bh_pcal          |                 0.7874 |                    0.9359 |                    0.9076 |                0.8646 |
| top_score_k_active |                 0.5428 |                    0.6897 |                    0.7581 |                0.7886 |

### table_5_ci_frontier

| scenario   |   fdp_mean |   power_mean |   ci_coverage_screened_mean |   ci_coverage_selected_mean |
|:-----------|-----------:|-------------:|----------------------------:|----------------------------:|
| n600       |          0 |       0.6562 |                      0.9497 |                      0.9349 |
| n1000      |          0 |       0.7986 |                      0.954  |                      0.9532 |
| n1600      |          0 |       0.8542 |                      0.9722 |                      0.971  |
| test20     |          0 |       0.7882 |                      0.9514 |                      0.9595 |
| test50     |          0 |       0.7431 |                      0.9627 |                      0.9544 |

### table_6_downstream_debias

| method               |   removed_mean |   spurious_recall_mean |   erroneous_removal_rate_mean |   overall_acc_mean |   worst_group_acc_mean |   conflict_acc_mean |
|:---------------------|---------------:|-----------------------:|------------------------------:|-------------------:|-----------------------:|--------------------:|
| none                 |          0     |                 0      |                        0      |             0.8177 |                 0.6199 |              0.6349 |
| oracle_spurious      |         24     |                 1      |                        0      |             1      |                 0.9999 |              1      |
| e_bh_pcal            |         24     |                 1      |                        0      |             1      |                 0.9999 |              1      |
| by_bh                |         24.025 |                 1      |                        0.001  |             1      |                 0.9999 |              1      |
| bh                   |         24.2   |                 1      |                        0.0079 |             1      |                 0.9999 |              1      |
| p_lt_q               |         26.65  |                 1      |                        0.0966 |             1      |                 0.9999 |              1      |
| top_score_k_spurious |         24     |                 0.2177 |                        0.7823 |             0.9201 |                 0.8272 |              0.84   |
| random_k_spurious    |         24     |                 0.0885 |                        0.9115 |             0.8098 |                 0.6055 |              0.6192 |

### table_7_real_subject_verb

| layer   | method                |   discoveries |   completeness_r2 |   centered_r2 |   abs_effect_fraction |   selected_full_corr |   sign_agreement |
|:--------|:----------------------|--------------:|------------------:|--------------:|----------------------:|---------------------:|-----------------:|
| L8      | bh                    |            15 |            0.9676 |        0.6341 |                0.9684 |               0.8152 |           1      |
| L8      | by_bh                 |             9 |            0.9678 |        0.636  |                0.9697 |               0.8149 |           1      |
| L8      | e_bh_pcal             |             6 |            0.9685 |        0.6436 |                0.9757 |               0.8168 |           1      |
| L8      | p_lt_q                |            52 |            0.9651 |        0.6059 |                0.9509 |               0.8101 |           1      |
| L8      | top_score_k_256       |           nan |            0.9637 |        0.5893 |                0.961  |               0.7993 |           1      |
| L8      | top_score_k_e_bh_pcal |           nan |            0.9634 |        0.5859 |                0.9493 |               0.7921 |           1      |
| L8      | track_e_bh_pcal       |             1 |            0.9501 |        0.4355 |                0.9061 |               0.7397 |           1      |
| L12     | bh                    |            29 |            0.9275 |        0.181  |                0.8168 |               0.7386 |           1      |
| L12     | by_bh                 |            18 |            0.9271 |        0.1755 |                0.8205 |               0.7287 |           1      |
| L12     | e_bh_pcal             |             7 |            0.9281 |        0.1874 |                0.8269 |               0.7259 |           1      |
| L12     | p_lt_q                |            54 |            0.9292 |        0.1997 |                0.8245 |               0.7325 |           1      |
| L12     | top_score_k_256       |           nan |            0.9448 |        0.3756 |                0.8694 |               0.7536 |           1      |
| L12     | top_score_k_e_bh_pcal |           nan |            0.9465 |        0.3954 |                0.8725 |               0.7664 |           1      |
| L12     | track_e_bh_pcal       |             1 |            0.9565 |        0.5081 |                0.9235 |               0.7615 |           1      |
| L16     | bh                    |            51 |            0.9651 |        0.6052 |                0.9726 |               0.7879 |           1      |
| L16     | by_bh                 |            37 |            0.9621 |        0.5711 |                0.9641 |               0.772  |           1      |
| L16     | e_bh_pcal             |            23 |            0.9632 |        0.5842 |                0.9587 |               0.7802 |           1      |
| L16     | p_lt_q                |            90 |            0.9665 |        0.6217 |                0.9608 |               0.8033 |           1      |
| L16     | top_score_k_256       |           nan |            0.9642 |        0.5948 |                1.0046 |               0.7911 |           1      |
| L16     | top_score_k_e_bh_pcal |           nan |            0.9645 |        0.5982 |                0.9324 |               0.8076 |           1      |
| L16     | track_e_bh_pcal       |             1 |            0.5719 |       -3.8389 |                0.3662 |               0.5495 |           1      |
| L20     | bh                    |            47 |            0.5908 |       -3.6259 |                0.4013 |               0.3801 |           0.9938 |
| L20     | by_bh                 |            29 |            0.5521 |       -4.063  |                0.3777 |               0.1664 |           0.9938 |
| L20     | e_bh_pcal             |            17 |            0.5215 |       -4.4097 |                0.3508 |               0.1493 |           0.9938 |
| L20     | p_lt_q                |            72 |            0.5924 |       -3.6072 |                0.4007 |               0.3946 |           1      |
| L20     | top_score_k_256       |           nan |            0.5943 |       -3.5867 |                0.4012 |               0.4054 |           1      |
| L20     | top_score_k_e_bh_pcal |           nan |            0.4365 |       -5.3696 |                0.2944 |               0.008  |           0.9812 |
| L20     | track_e_bh_pcal       |             0 |            0      |      -10.3044 |                0      |             nan      |           0      |

### table_8_bounded_bias_probe

| method    |   discoveries |   overall_acc |   worst_group_acc |   group_gap |   delta_overall_acc_vs_baseline |   delta_worst_group_acc_vs_baseline |
|:----------|--------------:|--------------:|------------------:|------------:|--------------------------------:|------------------------------------:|
| bh        |             1 |      nan      |               nan |       nan   |                          nan    |                                 nan |
| by_bh     |             0 |      nan      |               nan |       nan   |                          nan    |                                 nan |
| clean     |           nan |        0.0167 |                 0 |         0.5 |                            0    |                                   0 |
| e_bh_pcal |             0 |        0.0167 |                 0 |         0.5 |                            0    |                                   0 |
| p_lt_q    |             5 |      nan      |               nan |       nan   |                          nan    |                                 nan |
| top_score |           nan |        0.0667 |                 0 |         1   |                            0.05 |                                   0 |

### table_9_real_decoy_reliability

| layer   | method                      | selection_rule        |   discoveries_mean |   known_null_decoys_selected_mean |   known_null_fdp_mean |
|:--------|:----------------------------|:----------------------|-------------------:|----------------------------------:|----------------------:|
| L8      | top_score_fixed_k_256       | screen_score_manual_k |            256     |                           256     |                1      |
| L8      | top_score_matched_e_bh_pcal | screen_score_manual_k |              3     |                             3     |                1      |
| L8      | bh                          | test_split_fdr        |             12.695 |                             0.69  |                0.0504 |
| L8      | by_bh                       | test_split_fdr        |              8.095 |                             0.09  |                0.0098 |
| L8      | e_bh_pcal                   | test_split_fdr        |              3     |                             0     |                0      |
| L8      | p_lt_q                      | test_split_fdr        |             77.305 |                            25.305 |                0.3249 |
| L12     | top_score_fixed_k_256       | screen_score_manual_k |            256     |                           256     |                1      |
| L12     | top_score_matched_e_bh_pcal | screen_score_manual_k |              6     |                             6     |                1      |
| L12     | bh                          | test_split_fdr        |             24.99  |                             1.32  |                0.0498 |
| L12     | by_bh                       | test_split_fdr        |             12.095 |                             0.095 |                0.0072 |
| L12     | e_bh_pcal                   | test_split_fdr        |              6     |                             0     |                0      |
| L12     | p_lt_q                      | test_split_fdr        |             79.805 |                            25.805 |                0.3206 |
| L16     | top_score_fixed_k_256       | screen_score_manual_k |            256     |                           256     |                1      |
| L16     | top_score_matched_e_bh_pcal | screen_score_manual_k |             23     |                            23     |                1      |
| L16     | bh                          | test_split_fdr        |             45.17  |                             2.465 |                0.0527 |
| L16     | by_bh                       | test_split_fdr        |             31.435 |                             0.23  |                0.0069 |
| L16     | e_bh_pcal                   | test_split_fdr        |             23     |                             0     |                0      |
| L16     | p_lt_q                      | test_split_fdr        |            115.135 |                            25.135 |                0.2171 |
| L20     | top_score_fixed_k_256       | screen_score_manual_k |            256     |                           256     |                1      |
| L20     | top_score_matched_e_bh_pcal | screen_score_manual_k |             15     |                            15     |                1      |
| L20     | bh                          | test_split_fdr        |             41.51  |                             1.96  |                0.0454 |
| L20     | by_bh                       | test_split_fdr        |             27.165 |                             0.165 |                0.0059 |
| L20     | e_bh_pcal                   | test_split_fdr        |             15     |                             0     |                0      |
| L20     | p_lt_q                      | test_split_fdr        |             97.575 |                            25.575 |                0.2605 |

### table_10_real_selection_stability

| layer   | estimand                   | method          |   full_discoveries |   discoveries_mean |   jaccard_mean |   recall_full_mean |
|:--------|:---------------------------|:----------------|-------------------:|-------------------:|---------------:|-------------------:|
| L8      | mean_effect                | bh              |                 15 |             43.615 |         0.4215 |             0.8623 |
| L8      | mean_effect                | e_bh_pcal       |                  6 |              5.405 |         0.6722 |             0.7508 |
| L8      | mean_effect                | p_lt_q          |                 52 |             83.7   |         0.4564 |             0.7754 |
| L8      | prompt_tracking_covariance | track_e_bh_pcal |                  1 |              1.015 |         0.9925 |             1      |
| L12     | mean_effect                | bh              |                 29 |             47.06  |         0.5318 |             0.8386 |
| L12     | mean_effect                | e_bh_pcal       |                  7 |              8.44  |         0.6603 |             0.8593 |
| L12     | mean_effect                | p_lt_q          |                 54 |             82.54  |         0.5171 |             0.822  |
| L12     | prompt_tracking_covariance | track_e_bh_pcal |                  1 |              1.07  |         0.9742 |             1      |
| L16     | mean_effect                | bh              |                 51 |             74.14  |         0.5919 |             0.8876 |
| L16     | mean_effect                | e_bh_pcal       |                 23 |             27.215 |         0.8077 |             0.9693 |
| L16     | mean_effect                | p_lt_q          |                 90 |            104.105 |         0.6107 |             0.8063 |
| L16     | prompt_tracking_covariance | track_e_bh_pcal |                  1 |              1.165 |         0.8562 |             0.94   |
| L20     | mean_effect                | bh              |                 47 |             64.94  |         0.6006 |             0.8394 |
| L20     | mean_effect                | e_bh_pcal       |                 17 |             20.25  |         0.7447 |             0.9132 |
| L20     | mean_effect                | p_lt_q          |                 72 |             95.575 |         0.5856 |             0.8213 |
| L20     | prompt_tracking_covariance | track_e_bh_pcal |                  0 |              0.195 |         0.805  |             0.805  |

### table_11_real_q_grid

| layer   | estimand                   |    q | method                            |   discoveries | selection_rule                     |
|:--------|:---------------------------|-----:|:----------------------------------|--------------:|:-----------------------------------|
| L8      | mean_effect                | 0.01 | e_bh_pcal                         |             3 | fdr_at_q                           |
| L8      | mean_effect                | 0.01 | bh                                |             9 | fdr_at_q                           |
| L8      | mean_effect                | 0.01 | p_lt_q                            |            18 | uncorrected_p_threshold            |
| L8      | mean_effect                | 0.01 | top_score_matched_e_bh_pcal       |             3 | manual_k_equal_to_e_bh_discoveries |
| L8      | prompt_tracking_covariance | 0.01 | track_e_bh_pcal                   |             1 | fdr_at_q                           |
| L8      | prompt_tracking_covariance | 0.01 | track_p_lt_q                      |             3 | uncorrected_p_threshold            |
| L8      | prompt_tracking_covariance | 0.01 | top_score_matched_track_e_bh_pcal |             1 | manual_k_equal_to_e_bh_discoveries |
| L8      | mean_effect                | 0.05 | e_bh_pcal                         |             3 | fdr_at_q                           |
| L8      | mean_effect                | 0.05 | bh                                |            12 | fdr_at_q                           |
| L8      | mean_effect                | 0.05 | p_lt_q                            |            37 | uncorrected_p_threshold            |
| L8      | mean_effect                | 0.05 | top_score_matched_e_bh_pcal       |             3 | manual_k_equal_to_e_bh_discoveries |
| L8      | prompt_tracking_covariance | 0.05 | track_e_bh_pcal                   |             1 | fdr_at_q                           |
| L8      | prompt_tracking_covariance | 0.05 | track_p_lt_q                      |            12 | uncorrected_p_threshold            |
| L8      | prompt_tracking_covariance | 0.05 | top_score_matched_track_e_bh_pcal |             1 | manual_k_equal_to_e_bh_discoveries |
| L8      | mean_effect                | 0.1  | e_bh_pcal                         |             6 | fdr_at_q                           |
| L8      | mean_effect                | 0.1  | bh                                |            15 | fdr_at_q                           |
| L8      | mean_effect                | 0.1  | p_lt_q                            |            52 | uncorrected_p_threshold            |
| L8      | mean_effect                | 0.1  | top_score_matched_e_bh_pcal       |             6 | manual_k_equal_to_e_bh_discoveries |
| L8      | prompt_tracking_covariance | 0.1  | track_e_bh_pcal                   |             1 | fdr_at_q                           |
| L8      | prompt_tracking_covariance | 0.1  | track_p_lt_q                      |            20 | uncorrected_p_threshold            |
| L8      | prompt_tracking_covariance | 0.1  | top_score_matched_track_e_bh_pcal |             1 | manual_k_equal_to_e_bh_discoveries |
| L8      | mean_effect                | 0.2  | e_bh_pcal                         |             6 | fdr_at_q                           |
| L8      | mean_effect                | 0.2  | bh                                |            26 | fdr_at_q                           |
| L8      | mean_effect                | 0.2  | p_lt_q                            |            86 | uncorrected_p_threshold            |
| L8      | mean_effect                | 0.2  | top_score_matched_e_bh_pcal       |             6 | manual_k_equal_to_e_bh_discoveries |
| L8      | prompt_tracking_covariance | 0.2  | track_e_bh_pcal                   |             1 | fdr_at_q                           |
| L8      | prompt_tracking_covariance | 0.2  | track_p_lt_q                      |            30 | uncorrected_p_threshold            |
| L8      | prompt_tracking_covariance | 0.2  | top_score_matched_track_e_bh_pcal |             1 | manual_k_equal_to_e_bh_discoveries |
| L8      | mean_effect                | 0.3  | e_bh_pcal                         |             7 | fdr_at_q                           |
| L8      | mean_effect                | 0.3  | bh                                |            34 | fdr_at_q                           |
| L8      | mean_effect                | 0.3  | p_lt_q                            |           115 | uncorrected_p_threshold            |
| L8      | mean_effect                | 0.3  | top_score_matched_e_bh_pcal       |             7 | manual_k_equal_to_e_bh_discoveries |
| L8      | prompt_tracking_covariance | 0.3  | track_e_bh_pcal                   |             1 | fdr_at_q                           |
| L8      | prompt_tracking_covariance | 0.3  | track_p_lt_q                      |            52 | uncorrected_p_threshold            |
| L8      | prompt_tracking_covariance | 0.3  | top_score_matched_track_e_bh_pcal |             1 | manual_k_equal_to_e_bh_discoveries |
| L12     | mean_effect                | 0.01 | e_bh_pcal                         |             4 | fdr_at_q                           |
| L12     | mean_effect                | 0.01 | bh                                |            14 | fdr_at_q                           |
| L12     | mean_effect                | 0.01 | p_lt_q                            |            29 | uncorrected_p_threshold            |
| L12     | mean_effect                | 0.01 | top_score_matched_e_bh_pcal       |             4 | manual_k_equal_to_e_bh_discoveries |
| L12     | prompt_tracking_covariance | 0.01 | track_e_bh_pcal                   |             1 | fdr_at_q                           |
| L12     | prompt_tracking_covariance | 0.01 | track_p_lt_q                      |            10 | uncorrected_p_threshold            |
| L12     | prompt_tracking_covariance | 0.01 | top_score_matched_track_e_bh_pcal |             1 | manual_k_equal_to_e_bh_discoveries |
| L12     | mean_effect                | 0.05 | e_bh_pcal                         |             6 | fdr_at_q                           |
| L12     | mean_effect                | 0.05 | bh                                |            23 | fdr_at_q                           |
| L12     | mean_effect                | 0.05 | p_lt_q                            |            45 | uncorrected_p_threshold            |
| L12     | mean_effect                | 0.05 | top_score_matched_e_bh_pcal       |             6 | manual_k_equal_to_e_bh_discoveries |
| L12     | prompt_tracking_covariance | 0.05 | track_e_bh_pcal                   |             1 | fdr_at_q                           |
| L12     | prompt_tracking_covariance | 0.05 | track_p_lt_q                      |            27 | uncorrected_p_threshold            |
| L12     | prompt_tracking_covariance | 0.05 | top_score_matched_track_e_bh_pcal |             1 | manual_k_equal_to_e_bh_discoveries |
| L12     | mean_effect                | 0.1  | e_bh_pcal                         |             7 | fdr_at_q                           |
| L12     | mean_effect                | 0.1  | bh                                |            29 | fdr_at_q                           |
| L12     | mean_effect                | 0.1  | p_lt_q                            |            54 | uncorrected_p_threshold            |
| L12     | mean_effect                | 0.1  | top_score_matched_e_bh_pcal       |             7 | manual_k_equal_to_e_bh_discoveries |
| L12     | prompt_tracking_covariance | 0.1  | track_e_bh_pcal                   |             1 | fdr_at_q                           |
| L12     | prompt_tracking_covariance | 0.1  | track_p_lt_q                      |            59 | uncorrected_p_threshold            |
| L12     | prompt_tracking_covariance | 0.1  | top_score_matched_track_e_bh_pcal |             1 | manual_k_equal_to_e_bh_discoveries |
| L12     | mean_effect                | 0.2  | e_bh_pcal                         |             9 | fdr_at_q                           |
| L12     | mean_effect                | 0.2  | bh                                |            41 | fdr_at_q                           |
| L12     | mean_effect                | 0.2  | p_lt_q                            |            77 | uncorrected_p_threshold            |
| L12     | mean_effect                | 0.2  | top_score_matched_e_bh_pcal       |             9 | manual_k_equal_to_e_bh_discoveries |
| L12     | prompt_tracking_covariance | 0.2  | track_e_bh_pcal                   |             1 | fdr_at_q                           |
| L12     | prompt_tracking_covariance | 0.2  | track_p_lt_q                      |           107 | uncorrected_p_threshold            |
| L12     | prompt_tracking_covariance | 0.2  | top_score_matched_track_e_bh_pcal |             1 | manual_k_equal_to_e_bh_discoveries |
| L12     | mean_effect                | 0.3  | e_bh_pcal                         |             9 | fdr_at_q                           |
| L12     | mean_effect                | 0.3  | bh                                |            45 | fdr_at_q                           |
| L12     | mean_effect                | 0.3  | p_lt_q                            |            94 | uncorrected_p_threshold            |
| L12     | mean_effect                | 0.3  | top_score_matched_e_bh_pcal       |             9 | manual_k_equal_to_e_bh_discoveries |
| L12     | prompt_tracking_covariance | 0.3  | track_e_bh_pcal                   |             1 | fdr_at_q                           |
| L12     | prompt_tracking_covariance | 0.3  | track_p_lt_q                      |           160 | uncorrected_p_threshold            |
| L12     | prompt_tracking_covariance | 0.3  | top_score_matched_track_e_bh_pcal |             1 | manual_k_equal_to_e_bh_discoveries |
| L16     | mean_effect                | 0.01 | e_bh_pcal                         |            20 | fdr_at_q                           |
| L16     | mean_effect                | 0.01 | bh                                |            36 | fdr_at_q                           |
| L16     | mean_effect                | 0.01 | p_lt_q                            |            45 | uncorrected_p_threshold            |
| L16     | mean_effect                | 0.01 | top_score_matched_e_bh_pcal       |            20 | manual_k_equal_to_e_bh_discoveries |
| L16     | prompt_tracking_covariance | 0.01 | track_e_bh_pcal                   |             1 | fdr_at_q                           |
| L16     | prompt_tracking_covariance | 0.01 | track_p_lt_q                      |            13 | uncorrected_p_threshold            |
| L16     | prompt_tracking_covariance | 0.01 | top_score_matched_track_e_bh_pcal |             1 | manual_k_equal_to_e_bh_discoveries |
| L16     | mean_effect                | 0.05 | e_bh_pcal                         |            23 | fdr_at_q                           |
| L16     | mean_effect                | 0.05 | bh                                |            42 | fdr_at_q                           |
| L16     | mean_effect                | 0.05 | p_lt_q                            |            69 | uncorrected_p_threshold            |
| L16     | mean_effect                | 0.05 | top_score_matched_e_bh_pcal       |            23 | manual_k_equal_to_e_bh_discoveries |
| L16     | prompt_tracking_covariance | 0.05 | track_e_bh_pcal                   |             1 | fdr_at_q                           |
| L16     | prompt_tracking_covariance | 0.05 | track_p_lt_q                      |            38 | uncorrected_p_threshold            |
| L16     | prompt_tracking_covariance | 0.05 | top_score_matched_track_e_bh_pcal |             1 | manual_k_equal_to_e_bh_discoveries |
| L16     | mean_effect                | 0.1  | e_bh_pcal                         |            23 | fdr_at_q                           |
| L16     | mean_effect                | 0.1  | bh                                |            51 | fdr_at_q                           |
| L16     | mean_effect                | 0.1  | p_lt_q                            |            90 | uncorrected_p_threshold            |
| L16     | mean_effect                | 0.1  | top_score_matched_e_bh_pcal       |            23 | manual_k_equal_to_e_bh_discoveries |
| L16     | prompt_tracking_covariance | 0.1  | track_e_bh_pcal                   |             1 | fdr_at_q                           |
| L16     | prompt_tracking_covariance | 0.1  | track_p_lt_q                      |            60 | uncorrected_p_threshold            |
| L16     | prompt_tracking_covariance | 0.1  | top_score_matched_track_e_bh_pcal |             1 | manual_k_equal_to_e_bh_discoveries |
| L16     | mean_effect                | 0.2  | e_bh_pcal                         |            27 | fdr_at_q                           |
| L16     | mean_effect                | 0.2  | bh                                |            80 | fdr_at_q                           |
| L16     | mean_effect                | 0.2  | p_lt_q                            |           111 | uncorrected_p_threshold            |
| L16     | mean_effect                | 0.2  | top_score_matched_e_bh_pcal       |            27 | manual_k_equal_to_e_bh_discoveries |
| L16     | prompt_tracking_covariance | 0.2  | track_e_bh_pcal                   |             1 | fdr_at_q                           |
| L16     | prompt_tracking_covariance | 0.2  | track_p_lt_q                      |           104 | uncorrected_p_threshold            |
| L16     | prompt_tracking_covariance | 0.2  | top_score_matched_track_e_bh_pcal |             1 | manual_k_equal_to_e_bh_discoveries |
| L16     | mean_effect                | 0.3  | e_bh_pcal                         |            29 | fdr_at_q                           |
| L16     | mean_effect                | 0.3  | bh                                |            90 | fdr_at_q                           |
| L16     | mean_effect                | 0.3  | p_lt_q                            |           138 | uncorrected_p_threshold            |
| L16     | mean_effect                | 0.3  | top_score_matched_e_bh_pcal       |            29 | manual_k_equal_to_e_bh_discoveries |
| L16     | prompt_tracking_covariance | 0.3  | track_e_bh_pcal                   |             1 | fdr_at_q                           |
| L16     | prompt_tracking_covariance | 0.3  | track_p_lt_q                      |           146 | uncorrected_p_threshold            |
| L16     | prompt_tracking_covariance | 0.3  | top_score_matched_track_e_bh_pcal |             1 | manual_k_equal_to_e_bh_discoveries |
| L20     | mean_effect                | 0.01 | e_bh_pcal                         |            12 | fdr_at_q                           |
| L20     | mean_effect                | 0.01 | bh                                |            27 | fdr_at_q                           |
| L20     | mean_effect                | 0.01 | p_lt_q                            |            40 | uncorrected_p_threshold            |
| L20     | mean_effect                | 0.01 | top_score_matched_e_bh_pcal       |            12 | manual_k_equal_to_e_bh_discoveries |
| L20     | prompt_tracking_covariance | 0.01 | track_e_bh_pcal                   |             0 | fdr_at_q                           |
| L20     | prompt_tracking_covariance | 0.01 | track_p_lt_q                      |             5 | uncorrected_p_threshold            |
| L20     | prompt_tracking_covariance | 0.01 | top_score_matched_track_e_bh_pcal |             0 | manual_k_equal_to_e_bh_discoveries |
| L20     | mean_effect                | 0.05 | e_bh_pcal                         |            15 | fdr_at_q                           |
| L20     | mean_effect                | 0.05 | bh                                |            39 | fdr_at_q                           |
| L20     | mean_effect                | 0.05 | p_lt_q                            |            58 | uncorrected_p_threshold            |
| L20     | mean_effect                | 0.05 | top_score_matched_e_bh_pcal       |            15 | manual_k_equal_to_e_bh_discoveries |
| L20     | prompt_tracking_covariance | 0.05 | track_e_bh_pcal                   |             0 | fdr_at_q                           |
| L20     | prompt_tracking_covariance | 0.05 | track_p_lt_q                      |             5 | uncorrected_p_threshold            |
| L20     | prompt_tracking_covariance | 0.05 | top_score_matched_track_e_bh_pcal |             0 | manual_k_equal_to_e_bh_discoveries |
| L20     | mean_effect                | 0.1  | e_bh_pcal                         |            17 | fdr_at_q                           |
| L20     | mean_effect                | 0.1  | bh                                |            47 | fdr_at_q                           |
| L20     | mean_effect                | 0.1  | p_lt_q                            |            72 | uncorrected_p_threshold            |
| L20     | mean_effect                | 0.1  | top_score_matched_e_bh_pcal       |            17 | manual_k_equal_to_e_bh_discoveries |
| L20     | prompt_tracking_covariance | 0.1  | track_e_bh_pcal                   |             0 | fdr_at_q                           |
| L20     | prompt_tracking_covariance | 0.1  | track_p_lt_q                      |             9 | uncorrected_p_threshold            |
| L20     | prompt_tracking_covariance | 0.1  | top_score_matched_track_e_bh_pcal |             0 | manual_k_equal_to_e_bh_discoveries |
| L20     | mean_effect                | 0.2  | e_bh_pcal                         |            18 | fdr_at_q                           |
| L20     | mean_effect                | 0.2  | bh                                |            57 | fdr_at_q                           |
| L20     | mean_effect                | 0.2  | p_lt_q                            |            92 | uncorrected_p_threshold            |
| L20     | mean_effect                | 0.2  | top_score_matched_e_bh_pcal       |            18 | manual_k_equal_to_e_bh_discoveries |
| L20     | prompt_tracking_covariance | 0.2  | track_e_bh_pcal                   |             0 | fdr_at_q                           |
| L20     | prompt_tracking_covariance | 0.2  | track_p_lt_q                      |            22 | uncorrected_p_threshold            |
| L20     | prompt_tracking_covariance | 0.2  | top_score_matched_track_e_bh_pcal |             0 | manual_k_equal_to_e_bh_discoveries |
| L20     | mean_effect                | 0.3  | e_bh_pcal                         |            21 | fdr_at_q                           |
| L20     | mean_effect                | 0.3  | bh                                |            68 | fdr_at_q                           |
| L20     | mean_effect                | 0.3  | p_lt_q                            |           108 | uncorrected_p_threshold            |
| L20     | mean_effect                | 0.3  | top_score_matched_e_bh_pcal       |            21 | manual_k_equal_to_e_bh_discoveries |
| L20     | prompt_tracking_covariance | 0.3  | track_e_bh_pcal                   |             0 | fdr_at_q                           |
| L20     | prompt_tracking_covariance | 0.3  | track_p_lt_q                      |            41 | uncorrected_p_threshold            |
| L20     | prompt_tracking_covariance | 0.3  | top_score_matched_track_e_bh_pcal |             0 | manual_k_equal_to_e_bh_discoveries |

### table_12_reviewer_qf_sensitivity

| layer   | q_variant                 |   discoveries |   jaccard_to_prompt_uniform_ebh |   recall_of_prompt_uniform_ebh |   median_abs_tau |
|:--------|:--------------------------|--------------:|--------------------------------:|-------------------------------:|-----------------:|
| L12     | attractor_number_balanced |             7 |                          1      |                         1      |           0.0314 |
| L12     | cluster_mean_resample     |             6 |                          0.8571 |                         0.8571 |           0.0318 |
| L12     | prompt_uniform_resample   |             7 |                          1      |                         1      |           0.0314 |
| L12     | subject_number_balanced   |             7 |                          1      |                         1      |           0.0314 |
| L12     | winsorized_5_95           |             8 |                          0.875  |                         1      |           0.0293 |
| L16     | attractor_number_balanced |            23 |                          1      |                         1      |           0.0534 |
| L16     | cluster_mean_resample     |            25 |                          0.92   |                         1      |           0.0519 |
| L16     | prompt_uniform_resample   |            23 |                          1      |                         1      |           0.0534 |
| L16     | subject_number_balanced   |            23 |                          1      |                         1      |           0.0534 |
| L16     | winsorized_5_95           |            24 |                          0.9583 |                         1      |           0.0521 |
| L20     | attractor_number_balanced |            17 |                          1      |                         1      |           0.0429 |
| L20     | cluster_mean_resample     |            15 |                          0.7778 |                         0.8235 |           0.0429 |
| L20     | prompt_uniform_resample   |            17 |                          1      |                         1      |           0.0429 |
| L20     | subject_number_balanced   |            17 |                          1      |                         1      |           0.0429 |
| L20     | winsorized_5_95           |            21 |                          0.8095 |                         1      |           0.0295 |
| L8      | attractor_number_balanced |             6 |                          1      |                         1      |           0.0865 |
| L8      | cluster_mean_resample     |             3 |                          0.5    |                         0.5    |           0.2329 |
| L8      | prompt_uniform_resample   |             6 |                          1      |                         1      |           0.0865 |
| L8      | subject_number_balanced   |             6 |                          1      |                         1      |           0.0865 |
| L8      | winsorized_5_95           |             7 |                          0.8571 |                         1      |           0.0332 |

### table_13_reviewer_pvalue_robustness

| layer   | p_value_method          |   discoveries |   jaccard_to_paired_t_ebh |   recall_of_paired_t_ebh |   median_p_selected |
|:--------|:------------------------|--------------:|--------------------------:|-------------------------:|--------------------:|
| L12     | centered_wild_bootstrap |             0 |                    0      |                   0      |                 nan |
| L12     | paired_t                |             7 |                    1      |                   1      |                   0 |
| L12     | signflip_normal_approx  |             6 |                    0.8571 |                   0.8571 |                   0 |
| L12     | signflip_randomization  |             0 |                    0      |                   0      |                 nan |
| L16     | centered_wild_bootstrap |             0 |                    0      |                   0      |                 nan |
| L16     | paired_t                |            23 |                    1      |                   1      |                   0 |
| L16     | signflip_normal_approx  |            23 |                    1      |                   1      |                   0 |
| L16     | signflip_randomization  |             0 |                    0      |                   0      |                 nan |
| L20     | centered_wild_bootstrap |             0 |                    0      |                   0      |                 nan |
| L20     | paired_t                |            17 |                    1      |                   1      |                   0 |
| L20     | signflip_normal_approx  |            17 |                    1      |                   1      |                   0 |
| L20     | signflip_randomization  |             0 |                    0      |                   0      |                 nan |
| L8      | centered_wild_bootstrap |             0 |                    0      |                   0      |                 nan |
| L8      | paired_t                |             6 |                    1      |                   1      |                   0 |
| L8      | signflip_normal_approx  |             3 |                    0.5    |                   0.5    |                   0 |
| L8      | signflip_randomization  |             0 |                    0      |                   0      |                 nan |

### table_14_reviewer_method_comparison

| layer   | method               |   discoveries |   jaccard_to_ebh |   recall_of_ebh | selection_rule             |   knockoff_negative_count |   knockoff_threshold |
|:--------|:---------------------|--------------:|-----------------:|----------------:|:---------------------------|--------------------------:|---------------------:|
| L12     | adapt_lite           |            33 |           0.2121 |               1 | p_value_fdr                |                       nan |             nan      |
| L12     | bh                   |            29 |           0.2414 |               1 | p_value_fdr                |                       nan |             nan      |
| L12     | by_bh                |            18 |           0.3889 |               1 | p_value_fdr                |                       nan |             nan      |
| L12     | e_bh_pcal            |             7 |           1      |               1 | e_bh_p_calibrated          |                       nan |             nan      |
| L12     | ihw_quantile         |            23 |           0.3043 |               1 | p_value_fdr                |                       nan |             nan      |
| L12     | p_lt_q               |            54 |           0.1296 |               1 | uncorrected_p_threshold    |                       nan |             nan      |
| L12     | paired_knockoff_plus |           256 |           0.0273 |               1 | paired_decoy_knockoff_plus |                         0 |               0.0004 |
| L12     | weighted_bh_screen   |            33 |           0.2121 |               1 | p_value_fdr                |                       nan |             nan      |
| L16     | adapt_lite           |            51 |           0.451  |               1 | p_value_fdr                |                       nan |             nan      |
| L16     | bh                   |            51 |           0.451  |               1 | p_value_fdr                |                       nan |             nan      |
| L16     | by_bh                |            37 |           0.6216 |               1 | p_value_fdr                |                       nan |             nan      |
| L16     | e_bh_pcal            |            23 |           1      |               1 | e_bh_p_calibrated          |                       nan |             nan      |
| L16     | ihw_quantile         |            41 |           0.561  |               1 | p_value_fdr                |                       nan |             nan      |
| L16     | p_lt_q               |            90 |           0.2556 |               1 | uncorrected_p_threshold    |                       nan |             nan      |
| L16     | paired_knockoff_plus |           256 |           0.0898 |               1 | paired_decoy_knockoff_plus |                         0 |               0.0016 |
| L16     | weighted_bh_screen   |            51 |           0.451  |               1 | p_value_fdr                |                       nan |             nan      |
| L20     | adapt_lite           |            44 |           0.3864 |               1 | p_value_fdr                |                       nan |             nan      |
| L20     | bh                   |            47 |           0.3617 |               1 | p_value_fdr                |                       nan |             nan      |
| L20     | by_bh                |            29 |           0.5862 |               1 | p_value_fdr                |                       nan |             nan      |
| L20     | e_bh_pcal            |            17 |           1      |               1 | e_bh_p_calibrated          |                       nan |             nan      |
| L20     | ihw_quantile         |            34 |           0.5    |               1 | p_value_fdr                |                       nan |             nan      |
| L20     | p_lt_q               |            72 |           0.2361 |               1 | uncorrected_p_threshold    |                       nan |             nan      |
| L20     | paired_knockoff_plus |           256 |           0.0664 |               1 | paired_decoy_knockoff_plus |                         0 |               0.0016 |
| L20     | weighted_bh_screen   |            49 |           0.3469 |               1 | p_value_fdr                |                       nan |             nan      |
| L8      | adapt_lite           |            15 |           0.4    |               1 | p_value_fdr                |                       nan |             nan      |
| L8      | bh                   |            15 |           0.4    |               1 | p_value_fdr                |                       nan |             nan      |
| L8      | by_bh                |             9 |           0.6667 |               1 | p_value_fdr                |                       nan |             nan      |
| L8      | e_bh_pcal            |             6 |           1      |               1 | e_bh_p_calibrated          |                       nan |             nan      |
| L8      | ihw_quantile         |            14 |           0.4286 |               1 | p_value_fdr                |                       nan |             nan      |
| L8      | p_lt_q               |            52 |           0.1154 |               1 | uncorrected_p_threshold    |                       nan |             nan      |
| L8      | paired_knockoff_plus |           256 |           0.0234 |               1 | paired_decoy_knockoff_plus |                         0 |               0.0014 |
| L8      | weighted_bh_screen   |            16 |           0.375  |               1 | p_value_fdr                |                       nan |             nan      |

### table_15_reviewer_multisplit

| layer   | aggregation             |   discoveries |   jaccard_to_single_split_ebh |   recall_of_single_split_ebh |   mean_selection_frequency_selected |
|:--------|:------------------------|--------------:|------------------------------:|-----------------------------:|------------------------------------:|
| L12     | crossfit_stouffer_4fold |             7 |                        1      |                       1      |                              0.3214 |
| L12     | frequency_ge_0.5        |             2 |                        0.2857 |                       0.2857 |                              1      |
| L12     | multi_split_quantile_p  |             2 |                        0.2857 |                       0.2857 |                              1      |
| L12     | single_split_ebh        |             7 |                        1      |                       1      |                              0.3214 |
| L16     | crossfit_stouffer_4fold |            23 |                        1      |                       1      |                              0.6049 |
| L16     | frequency_ge_0.5        |            12 |                        0.5217 |                       0.5217 |                              0.9667 |
| L16     | multi_split_quantile_p  |            12 |                        0.5217 |                       0.5217 |                              0.9667 |
| L16     | single_split_ebh        |            23 |                        1      |                       1      |                              0.6049 |
| L20     | crossfit_stouffer_4fold |            17 |                        1      |                       1      |                              0.4691 |
| L20     | frequency_ge_0.5        |             7 |                        0.4118 |                       0.4118 |                              0.9929 |
| L20     | multi_split_quantile_p  |             7 |                        0.4118 |                       0.4118 |                              0.9929 |
| L20     | single_split_ebh        |            17 |                        1      |                       1      |                              0.4691 |
| L8      | crossfit_stouffer_4fold |             4 |                        0.6667 |                       0.6667 |                              0.75   |
| L8      | frequency_ge_0.5        |             3 |                        0.5    |                       0.5    |                              1      |
| L8      | multi_split_quantile_p  |             3 |                        0.5    |                       0.5    |                              1      |
| L8      | single_split_ebh        |             6 |                        1      |                       1      |                              0.5042 |

### table_16_reviewer_decoy_robustness

| layer   | decoy_scheme          | method                      |   discoveries_mean |   known_null_decoys_selected_mean |   known_null_fdp_mean |
|:--------|:----------------------|:----------------------------|-------------------:|----------------------------------:|----------------------:|
| L12     | centered_permutation  | adapt_lite                  |            23      |                            0      |                0      |
| L12     | centered_permutation  | bh                          |            23      |                            0      |                0      |
| L12     | centered_permutation  | by_bh                       |            12      |                            0      |                0      |
| L12     | centered_permutation  | e_bh_pcal                   |             6      |                            0      |                0      |
| L12     | centered_permutation  | ihw_quantile                |            18      |                            0      |                0      |
| L12     | centered_permutation  | p_lt_q                      |            54      |                            0      |                0      |
| L12     | centered_permutation  | top_score_matched_e_bh_pcal |             6      |                            3      |                0.5    |
| L12     | centered_permutation  | weighted_bh_screen          |            27      |                            0      |                0      |
| L12     | high_score_signflip   | adapt_lite                  |            25.8917 |                            1.35   |                0.0493 |
| L12     | high_score_signflip   | bh                          |            25.0583 |                            1.3667 |                0.0515 |
| L12     | high_score_signflip   | by_bh                       |            12.1    |                            0.1    |                0.0075 |
| L12     | high_score_signflip   | e_bh_pcal                   |             6      |                            0      |                0      |
| L12     | high_score_signflip   | ihw_quantile                |            19.075  |                            0.075  |                0.0037 |
| L12     | high_score_signflip   | p_lt_q                      |            79.5417 |                           25.5417 |                0.3183 |
| L12     | high_score_signflip   | top_score_matched_e_bh_pcal |             6      |                            6      |                1      |
| L12     | high_score_signflip   | weighted_bh_screen          |            23.85   |                            1.9167 |                0.0748 |
| L12     | low_score_signflip    | adapt_lite                  |            25.9167 |                            1.375  |                0.0508 |
| L12     | low_score_signflip    | bh                          |            25.1917 |                            1.425  |                0.054  |
| L12     | low_score_signflip    | by_bh                       |            12.0917 |                            0.0917 |                0.0071 |
| L12     | low_score_signflip    | e_bh_pcal                   |             6      |                            0      |                0      |
| L12     | low_score_signflip    | ihw_quantile                |            22.0167 |                            0.0167 |                0.0007 |
| L12     | low_score_signflip    | p_lt_q                      |            80.3667 |                           26.3667 |                0.3257 |
| L12     | low_score_signflip    | top_score_matched_e_bh_pcal |             6      |                            0      |                0      |
| L12     | low_score_signflip    | weighted_bh_screen          |            27.9417 |                            0.9417 |                0.0327 |
| L12     | random_score_signflip | adapt_lite                  |            25.9    |                            1.4583 |                0.0529 |
| L12     | random_score_signflip | bh                          |            25.0833 |                            1.4    |                0.0524 |
| L12     | random_score_signflip | by_bh                       |            12.1083 |                            0.1083 |                0.0083 |
| L12     | random_score_signflip | e_bh_pcal                   |             6      |                            0      |                0      |
| L12     | random_score_signflip | ihw_quantile                |            18.6167 |                            0.4667 |                0.0235 |
| L12     | random_score_signflip | p_lt_q                      |            79.95   |                           25.95   |                0.3222 |
| L12     | random_score_signflip | top_score_matched_e_bh_pcal |             6      |                            3      |                0.5    |
| L12     | random_score_signflip | weighted_bh_screen          |            28.5833 |                            1.5833 |                0.0528 |
| L16     | centered_permutation  | adapt_lite                  |            42      |                            0      |                0      |
| L16     | centered_permutation  | bh                          |            42      |                            0      |                0      |
| L16     | centered_permutation  | by_bh                       |            31      |                            0      |                0      |
| L16     | centered_permutation  | e_bh_pcal                   |            23      |                            0      |                0      |
| L16     | centered_permutation  | ihw_quantile                |            38      |                            0      |                0      |
| L16     | centered_permutation  | p_lt_q                      |            90      |                            0      |                0      |
| L16     | centered_permutation  | top_score_matched_e_bh_pcal |            23      |                           12      |                0.5217 |
| L16     | centered_permutation  | weighted_bh_screen          |            43      |                            0      |                0      |
| L16     | high_score_signflip   | adapt_lite                  |            49.5417 |                            1.8917 |                0.0371 |
| L16     | high_score_signflip   | bh                          |            44.9583 |                            2.2833 |                0.0491 |
| L16     | high_score_signflip   | by_bh                       |            31.475  |                            0.25   |                0.0075 |
| L16     | high_score_signflip   | e_bh_pcal                   |            23      |                            0      |                0      |
| L16     | high_score_signflip   | ihw_quantile                |            38.0667 |                            0.0667 |                0.0017 |
| L16     | high_score_signflip   | p_lt_q                      |           115.783  |                           25.7833 |                0.221  |
| L16     | high_score_signflip   | top_score_matched_e_bh_pcal |            23      |                           23      |                1      |
| L16     | high_score_signflip   | weighted_bh_screen          |            42.3583 |                            2.9    |                0.0662 |
| L16     | low_score_signflip    | adapt_lite                  |            49.7583 |                            1.9667 |                0.0384 |
| L16     | low_score_signflip    | bh                          |            45.1917 |                            2.4167 |                0.0514 |
| L16     | low_score_signflip    | by_bh                       |            31.3167 |                            0.1583 |                0.0048 |
| L16     | low_score_signflip    | e_bh_pcal                   |            23      |                            0      |                0      |
| L16     | low_score_signflip    | ihw_quantile                |            43.0167 |                            0.0167 |                0.0004 |
| L16     | low_score_signflip    | p_lt_q                      |           114.308  |                           24.3083 |                0.2112 |
| L16     | low_score_signflip    | top_score_matched_e_bh_pcal |            23      |                            0      |                0      |
| L16     | low_score_signflip    | weighted_bh_screen          |            49.45   |                            1.625  |                0.0321 |
| L16     | random_score_signflip | adapt_lite                  |            46.6083 |                            2.325  |                0.0483 |
| L16     | random_score_signflip | bh                          |            45.175  |                            2.3    |                0.0487 |
| L16     | random_score_signflip | by_bh                       |            31.5167 |                            0.275  |                0.0083 |
| L16     | random_score_signflip | e_bh_pcal                   |            23.0083 |                            0.0083 |                0.0003 |
| L16     | random_score_signflip | ihw_quantile                |            38.8583 |                            0.8417 |                0.0209 |
| L16     | random_score_signflip | p_lt_q                      |           115.3    |                           25.3    |                0.2184 |
| L16     | random_score_signflip | top_score_matched_e_bh_pcal |            23.0083 |                           11.5083 |                0.5002 |
| L16     | random_score_signflip | weighted_bh_screen          |            46.325  |                            2.2833 |                0.0475 |
| L20     | centered_permutation  | adapt_lite                  |            39      |                            0      |                0      |
| L20     | centered_permutation  | bh                          |            39      |                            0      |                0      |
| L20     | centered_permutation  | by_bh                       |            27      |                            0      |                0      |
| L20     | centered_permutation  | e_bh_pcal                   |            15      |                            0      |                0      |
| L20     | centered_permutation  | ihw_quantile                |            29      |                            0      |                0      |
| L20     | centered_permutation  | p_lt_q                      |            72      |                            0      |                0      |
| L20     | centered_permutation  | top_score_matched_e_bh_pcal |            15      |                            8      |                0.5333 |
| L20     | centered_permutation  | weighted_bh_screen          |            37      |                            0      |                0      |
| L20     | high_score_signflip   | adapt_lite                  |            41.0167 |                            2      |                0.0476 |
| L20     | high_score_signflip   | bh                          |            41.975  |                            2.3    |                0.0533 |
| L20     | high_score_signflip   | by_bh                       |            27.225  |                            0.225  |                0.008  |
| L20     | high_score_signflip   | e_bh_pcal                   |            15      |                            0      |                0      |
| L20     | high_score_signflip   | ihw_quantile                |            30.0583 |                            0.0583 |                0.0019 |
| L20     | high_score_signflip   | p_lt_q                      |            97.7417 |                           25.7417 |                0.2612 |
| L20     | high_score_signflip   | top_score_matched_e_bh_pcal |            15      |                           15      |                1      |
| L20     | high_score_signflip   | weighted_bh_screen          |            36.9167 |                            2.8167 |                0.0741 |
| L20     | low_score_signflip    | adapt_lite                  |            40.9    |                            1.8833 |                0.0448 |
| L20     | low_score_signflip    | bh                          |            41.7833 |                            2.175  |                0.0504 |
| L20     | low_score_signflip    | by_bh                       |            27.1833 |                            0.1833 |                0.0065 |
| L20     | low_score_signflip    | e_bh_pcal                   |            15      |                            0      |                0      |
| L20     | low_score_signflip    | ihw_quantile                |            36.05   |                            0.05   |                0.0014 |
| L20     | low_score_signflip    | p_lt_q                      |            98.0167 |                           26.0167 |                0.2636 |
| L20     | low_score_signflip    | top_score_matched_e_bh_pcal |            15      |                            0      |                0      |
| L20     | low_score_signflip    | weighted_bh_screen          |            41.4583 |                            1.325  |                0.031  |
| L20     | random_score_signflip | adapt_lite                  |            40.775  |                            2.075  |                0.0494 |
| L20     | random_score_signflip | bh                          |            41.6167 |                            2.0333 |                0.0476 |
| L20     | random_score_signflip | by_bh                       |            27.1833 |                            0.1833 |                0.0065 |
| L20     | random_score_signflip | e_bh_pcal                   |            15.0167 |                            0.0083 |                0.0005 |
| L20     | random_score_signflip | ihw_quantile                |            29.575  |                            0.5583 |                0.0184 |
| L20     | random_score_signflip | p_lt_q                      |            97.35   |                           25.35   |                0.2584 |
| L20     | random_score_signflip | top_score_matched_e_bh_pcal |            15.0167 |                            7.525  |                0.5011 |
| L20     | random_score_signflip | weighted_bh_screen          |            40.6917 |                            2.1667 |                0.0516 |
| L8      | centered_permutation  | adapt_lite                  |            12      |                            0      |                0      |
| L8      | centered_permutation  | bh                          |            12      |                            0      |                0      |
| L8      | centered_permutation  | by_bh                       |             8      |                            0      |                0      |
| L8      | centered_permutation  | e_bh_pcal                   |             3      |                            0      |                0      |
| L8      | centered_permutation  | ihw_quantile                |            10      |                            0      |                0      |
| L8      | centered_permutation  | p_lt_q                      |            52      |                            0      |                0      |
| L8      | centered_permutation  | top_score_matched_e_bh_pcal |             3      |                            1      |                0.3333 |
| L8      | centered_permutation  | weighted_bh_screen          |            13      |                            0      |                0      |
| L8      | high_score_signflip   | adapt_lite                  |            13.7583 |                            0.7083 |                0.0465 |
| L8      | high_score_signflip   | bh                          |            12.725  |                            0.7167 |                0.0519 |
| L8      | high_score_signflip   | by_bh                       |             8.075  |                            0.075  |                0.0083 |
| L8      | high_score_signflip   | e_bh_pcal                   |             3      |                            0      |                0      |
| L8      | high_score_signflip   | ihw_quantile                |            11.075  |                            0.075  |                0.0062 |
| L8      | high_score_signflip   | p_lt_q                      |            78.5083 |                           26.5083 |                0.3356 |
| L8      | high_score_signflip   | top_score_matched_e_bh_pcal |             3      |                            3      |                1      |
| L8      | high_score_signflip   | weighted_bh_screen          |            12.95   |                            0.95   |                0.0675 |
| L8      | low_score_signflip    | adapt_lite                  |            13.6667 |                            0.6417 |                0.0428 |
| L8      | low_score_signflip    | bh                          |            12.7083 |                            0.7    |                0.0511 |
| L8      | low_score_signflip    | by_bh                       |             8.05   |                            0.05   |                0.0056 |
| L8      | low_score_signflip    | e_bh_pcal                   |             3      |                            0      |                0      |
| L8      | low_score_signflip    | ihw_quantile                |            14.0083 |                            0.0083 |                0.0006 |
| L8      | low_score_signflip    | p_lt_q                      |            77.325  |                           25.325  |                0.325  |
| L8      | low_score_signflip    | top_score_matched_e_bh_pcal |             3      |                            0      |                0      |
| L8      | low_score_signflip    | weighted_bh_screen          |            14.5833 |                            0.4917 |                0.031  |
| L8      | random_score_signflip | adapt_lite                  |            12.7    |                            0.6167 |                0.0442 |
| L8      | random_score_signflip | bh                          |            12.6083 |                            0.6083 |                0.0445 |
| L8      | random_score_signflip | by_bh                       |             8.0833 |                            0.075  |                0.008  |
| L8      | random_score_signflip | e_bh_pcal                   |             3      |                            0      |                0      |
| L8      | random_score_signflip | ihw_quantile                |            10.3    |                            0.2667 |                0.0229 |
| L8      | random_score_signflip | p_lt_q                      |            77.375  |                           25.375  |                0.3253 |
| L8      | random_score_signflip | top_score_matched_e_bh_pcal |             3      |                            1.4917 |                0.4972 |
| L8      | random_score_signflip | weighted_bh_screen          |            14.5167 |                            0.8917 |                0.0553 |

### table_17_reviewer_type_sm

| method               |   removed_mean |   task_irrelevant_harmful_recall_mean |   task_feature_removal_rate_mean |   proxy_or_noise_removal_rate_mean |   type_s_rate_selected_nonzero_mean |   type_m_median_selected_nonzero_mean |   worst_group_acc_mean |   conflict_acc_mean |
|:---------------------|---------------:|--------------------------------------:|---------------------------------:|-----------------------------------:|------------------------------------:|--------------------------------------:|-----------------------:|--------------------:|
| bh                   |        24.1917 |                                   1   |                           0.0075 |                                0   |                              0.0039 |                                0.9998 |                 1      |              1      |
| by_bh                |        24.025  |                                   1   |                           0.001  |                                0   |                              0.0007 |                                0.9993 |                 1      |              1      |
| e_bh_pcal            |        24      |                                   1   |                           0      |                                0   |                              0      |                                0.9993 |                 1      |              1      |
| p_lt_q               |        26.55   |                                   1   |                           0.0932 |                                0   |                              0.0478 |                                1.009  |                 1      |              1      |
| top_score_k_spurious |        24      |                                   0.5 |                           0      |                                0.5 |                              0      |                                0.9979 |                 0.9728 |              0.9766 |

### table_18_second_round_decoy_bh_by

| layer   | decoy_scheme          | method                      |   discoveries_mean |   known_null_decoys_selected_mean |   known_null_fdp_mean |   decoy_admission_rate_mean |
|:--------|:----------------------|:----------------------------|-------------------:|----------------------------------:|----------------------:|----------------------------:|
| L12     | centered_permutation  | bh                          |            23      |                            0      |                0      |                      0      |
| L12     | centered_permutation  | by_bh                       |            12      |                            0      |                0      |                      0      |
| L12     | centered_permutation  | e_bh_pcal                   |             6      |                            0      |                0      |                      0      |
| L12     | centered_permutation  | p_lt_q                      |            54      |                            0      |                0      |                      0      |
| L12     | centered_permutation  | top_score_matched_e_bh_pcal |             6      |                            3      |                0.5    |                      0.0117 |
| L12     | high_score_signflip   | bh                          |            25.0583 |                            1.3667 |                0.0515 |                      0.0053 |
| L12     | high_score_signflip   | by_bh                       |            12.1    |                            0.1    |                0.0075 |                      0.0004 |
| L12     | high_score_signflip   | e_bh_pcal                   |             6      |                            0      |                0      |                      0      |
| L12     | high_score_signflip   | p_lt_q                      |            79.5417 |                           25.5417 |                0.3183 |                      0.0998 |
| L12     | high_score_signflip   | top_score_matched_e_bh_pcal |             6      |                            6      |                1      |                      0.0234 |
| L12     | low_score_signflip    | bh                          |            25.1917 |                            1.425  |                0.054  |                      0.0056 |
| L12     | low_score_signflip    | by_bh                       |            12.0917 |                            0.0917 |                0.0071 |                      0.0004 |
| L12     | low_score_signflip    | e_bh_pcal                   |             6      |                            0      |                0      |                      0      |
| L12     | low_score_signflip    | p_lt_q                      |            80.3667 |                           26.3667 |                0.3257 |                      0.103  |
| L12     | low_score_signflip    | top_score_matched_e_bh_pcal |             6      |                            0      |                0      |                      0      |
| L12     | random_score_signflip | bh                          |            25.0833 |                            1.4    |                0.0524 |                      0.0055 |
| L12     | random_score_signflip | by_bh                       |            12.1083 |                            0.1083 |                0.0083 |                      0.0004 |
| L12     | random_score_signflip | e_bh_pcal                   |             6      |                            0      |                0      |                      0      |
| L12     | random_score_signflip | p_lt_q                      |            79.95   |                           25.95   |                0.3222 |                      0.1014 |
| L12     | random_score_signflip | top_score_matched_e_bh_pcal |             6      |                            3      |                0.5    |                      0.0117 |
| L16     | centered_permutation  | bh                          |            42      |                            0      |                0      |                      0      |
| L16     | centered_permutation  | by_bh                       |            31      |                            0      |                0      |                      0      |
| L16     | centered_permutation  | e_bh_pcal                   |            23      |                            0      |                0      |                      0      |
| L16     | centered_permutation  | p_lt_q                      |            90      |                            0      |                0      |                      0      |
| L16     | centered_permutation  | top_score_matched_e_bh_pcal |            23      |                           12      |                0.5217 |                      0.0469 |
| L16     | high_score_signflip   | bh                          |            44.9583 |                            2.2833 |                0.0491 |                      0.0089 |
| L16     | high_score_signflip   | by_bh                       |            31.475  |                            0.25   |                0.0075 |                      0.001  |
| L16     | high_score_signflip   | e_bh_pcal                   |            23      |                            0      |                0      |                      0      |
| L16     | high_score_signflip   | p_lt_q                      |           115.783  |                           25.7833 |                0.221  |                      0.1007 |
| L16     | high_score_signflip   | top_score_matched_e_bh_pcal |            23      |                           23      |                1      |                      0.0898 |
| L16     | low_score_signflip    | bh                          |            45.1917 |                            2.4167 |                0.0514 |                      0.0094 |
| L16     | low_score_signflip    | by_bh                       |            31.3167 |                            0.1583 |                0.0048 |                      0.0006 |
| L16     | low_score_signflip    | e_bh_pcal                   |            23      |                            0      |                0      |                      0      |
| L16     | low_score_signflip    | p_lt_q                      |           114.308  |                           24.3083 |                0.2112 |                      0.095  |
| L16     | low_score_signflip    | top_score_matched_e_bh_pcal |            23      |                            0      |                0      |                      0      |
| L16     | random_score_signflip | bh                          |            45.175  |                            2.3    |                0.0487 |                      0.009  |
| L16     | random_score_signflip | by_bh                       |            31.5167 |                            0.275  |                0.0083 |                      0.0011 |
| L16     | random_score_signflip | e_bh_pcal                   |            23.0083 |                            0.0083 |                0.0003 |                      0      |
| L16     | random_score_signflip | p_lt_q                      |           115.3    |                           25.3    |                0.2184 |                      0.0988 |
| L16     | random_score_signflip | top_score_matched_e_bh_pcal |            23.0083 |                           11.5083 |                0.5002 |                      0.045  |
| L20     | centered_permutation  | bh                          |            39      |                            0      |                0      |                      0      |
| L20     | centered_permutation  | by_bh                       |            27      |                            0      |                0      |                      0      |
| L20     | centered_permutation  | e_bh_pcal                   |            15      |                            0      |                0      |                      0      |
| L20     | centered_permutation  | p_lt_q                      |            72      |                            0      |                0      |                      0      |
| L20     | centered_permutation  | top_score_matched_e_bh_pcal |            15      |                            8      |                0.5333 |                      0.0312 |
| L20     | high_score_signflip   | bh                          |            41.975  |                            2.3    |                0.0533 |                      0.009  |
| L20     | high_score_signflip   | by_bh                       |            27.225  |                            0.225  |                0.008  |                      0.0009 |
| L20     | high_score_signflip   | e_bh_pcal                   |            15      |                            0      |                0      |                      0      |
| L20     | high_score_signflip   | p_lt_q                      |            97.7417 |                           25.7417 |                0.2612 |                      0.1006 |
| L20     | high_score_signflip   | top_score_matched_e_bh_pcal |            15      |                           15      |                1      |                      0.0586 |
| L20     | low_score_signflip    | bh                          |            41.7833 |                            2.175  |                0.0504 |                      0.0085 |
| L20     | low_score_signflip    | by_bh                       |            27.1833 |                            0.1833 |                0.0065 |                      0.0007 |
| L20     | low_score_signflip    | e_bh_pcal                   |            15      |                            0      |                0      |                      0      |
| L20     | low_score_signflip    | p_lt_q                      |            98.0167 |                           26.0167 |                0.2636 |                      0.1016 |
| L20     | low_score_signflip    | top_score_matched_e_bh_pcal |            15      |                            0      |                0      |                      0      |
| L20     | random_score_signflip | bh                          |            41.6167 |                            2.0333 |                0.0476 |                      0.0079 |
| L20     | random_score_signflip | by_bh                       |            27.1833 |                            0.1833 |                0.0065 |                      0.0007 |
| L20     | random_score_signflip | e_bh_pcal                   |            15.0167 |                            0.0083 |                0.0005 |                      0      |
| L20     | random_score_signflip | p_lt_q                      |            97.35   |                           25.35   |                0.2584 |                      0.099  |
| L20     | random_score_signflip | top_score_matched_e_bh_pcal |            15.0167 |                            7.525  |                0.5011 |                      0.0294 |
| L8      | centered_permutation  | bh                          |            12      |                            0      |                0      |                      0      |
| L8      | centered_permutation  | by_bh                       |             8      |                            0      |                0      |                      0      |
| L8      | centered_permutation  | e_bh_pcal                   |             3      |                            0      |                0      |                      0      |
| L8      | centered_permutation  | p_lt_q                      |            52      |                            0      |                0      |                      0      |
| L8      | centered_permutation  | top_score_matched_e_bh_pcal |             3      |                            1      |                0.3333 |                      0.0039 |
| L8      | high_score_signflip   | bh                          |            12.725  |                            0.7167 |                0.0519 |                      0.0028 |
| L8      | high_score_signflip   | by_bh                       |             8.075  |                            0.075  |                0.0083 |                      0.0003 |
| L8      | high_score_signflip   | e_bh_pcal                   |             3      |                            0      |                0      |                      0      |
| L8      | high_score_signflip   | p_lt_q                      |            78.5083 |                           26.5083 |                0.3356 |                      0.1035 |
| L8      | high_score_signflip   | top_score_matched_e_bh_pcal |             3      |                            3      |                1      |                      0.0117 |
| L8      | low_score_signflip    | bh                          |            12.7083 |                            0.7    |                0.0511 |                      0.0027 |
| L8      | low_score_signflip    | by_bh                       |             8.05   |                            0.05   |                0.0056 |                      0.0002 |
| L8      | low_score_signflip    | e_bh_pcal                   |             3      |                            0      |                0      |                      0      |
| L8      | low_score_signflip    | p_lt_q                      |            77.325  |                           25.325  |                0.325  |                      0.0989 |
| L8      | low_score_signflip    | top_score_matched_e_bh_pcal |             3      |                            0      |                0      |                      0      |
| L8      | random_score_signflip | bh                          |            12.6083 |                            0.6083 |                0.0445 |                      0.0024 |
| L8      | random_score_signflip | by_bh                       |             8.0833 |                            0.075  |                0.008  |                      0.0003 |
| L8      | random_score_signflip | e_bh_pcal                   |             3      |                            0      |                0      |                      0      |
| L8      | random_score_signflip | p_lt_q                      |            77.375  |                           25.375  |                0.3253 |                      0.0991 |
| L8      | random_score_signflip | top_score_matched_e_bh_pcal |             3      |                            1.4917 |                0.4972 |                      0.0058 |

### table_19_second_round_gamma_synthetic

|   gamma |   discoveries_mean |   fdp_mean |   power_mean |   jaccard_to_gamma_0_5_mean |   recall_of_gamma_0_5_mean |
|--------:|-------------------:|-----------:|-------------:|----------------------------:|---------------------------:|
|    0.25 |             19.3   |     0      |       0.8042 |                      0.9987 |                     0.9987 |
|    0.5  |             19.325 |     0.0013 |       0.8042 |                      1      |                     1      |
|    0.75 |             19.375 |     0.0038 |       0.8042 |                      0.9975 |                     1      |

### table_20_second_round_gamma_real

| layer   |   gamma |   discoveries |   jaccard_to_gamma_0_5 |   recall_of_gamma_0_5 |   min_p_selected |
|:--------|--------:|--------------:|-----------------------:|----------------------:|-----------------:|
| L12     |    0.25 |             2 |                 0.2857 |                0.2857 |                0 |
| L12     |    0.5  |             7 |                 1      |                1      |                0 |
| L12     |    0.75 |            10 |                 0.7    |                1      |                0 |
| L16     |    0.25 |            12 |                 0.5217 |                0.5217 |                0 |
| L16     |    0.5  |            23 |                 1      |                1      |                0 |
| L16     |    0.75 |            29 |                 0.7931 |                1      |                0 |
| L20     |    0.25 |             7 |                 0.4118 |                0.4118 |                0 |
| L20     |    0.5  |            17 |                 1      |                1      |                0 |
| L20     |    0.75 |            22 |                 0.7727 |                1      |                0 |
| L8      |    0.25 |             3 |                 0.5    |                0.5    |                0 |
| L8      |    0.5  |             6 |                 1      |                1      |                0 |
| L8      |    0.75 |             8 |                 0.75   |                1      |                0 |

### table_21_second_round_real_ci_type_s

| layer   | selection    |   features |   ci_width_median |   ci_width_p90 |   ci_crosses_zero_rate |   cluster_bootstrap_sign_flip_rate_max |   type_s_diagnostic_rate |
|:--------|:-------------|-----------:|------------------:|---------------:|-----------------------:|---------------------------------------:|-------------------------:|
| L12     | all_screened |        256 |            0.0167 |         0.0206 |                 0.8242 |                                 0.55   |                   0.8242 |
| L12     | e_bh_pcal    |          7 |            0.0222 |         0.2033 |                 0      |                                 0      |                   0      |
| L12     | by_bh        |         18 |            0.0202 |         0.0419 |                 0      |                                 0      |                   0      |
| L12     | bh           |         29 |            0.0197 |         0.0281 |                 0      |                                 0.0075 |                   0      |
| L16     | all_screened |        256 |            0.0155 |         0.0216 |                 0.707  |                                 0.52   |                   0.707  |
| L16     | e_bh_pcal    |         23 |            0.0272 |         0.0763 |                 0      |                                 0      |                   0      |
| L16     | by_bh        |         37 |            0.022  |         0.0422 |                 0      |                                 0.0025 |                   0      |
| L16     | bh           |         51 |            0.0204 |         0.0346 |                 0      |                                 0.0075 |                   0      |
| L20     | all_screened |        256 |            0.014  |         0.0206 |                 0.7812 |                                 0.52   |                   0.7812 |
| L20     | e_bh_pcal    |         17 |            0.0261 |         0.0751 |                 0      |                                 0      |                   0      |
| L20     | by_bh        |         29 |            0.0226 |         0.0638 |                 0      |                                 0.0025 |                   0      |
| L20     | bh           |         47 |            0.0196 |         0.0611 |                 0      |                                 0.0225 |                   0      |
| L8      | all_screened |        256 |            0.0186 |         0.0222 |                 0.8438 |                                 0.515  |                   0.8438 |
| L8      | e_bh_pcal    |          6 |            0.0377 |         0.2249 |                 0      |                                 0      |                   0      |
| L8      | by_bh        |          9 |            0.0259 |         0.1206 |                 0      |                                 0      |                   0      |
| L8      | bh           |         15 |            0.025  |         0.0499 |                 0      |                                 0.0025 |                   0      |

### table_22_second_round_adaptive_ebh

| setting          | method                |   discoveries_mean |   fdp_mean |   power_mean |   jaccard_to_default |   recall_of_default |   gain_vs_default_discoveries |
|:-----------------|:----------------------|-------------------:|-----------:|-------------:|---------------------:|--------------------:|------------------------------:|
| synthetic_gate_b | e_bh_pcal             |             19.325 |     0.0013 |       0.8042 |               1      |              1      |                             0 |
| synthetic_gate_b | screen_stratified_ebh |             19.325 |     0.0013 |       0.8042 |               1      |              1      |                             0 |
| real_L8          | e_bh_pcal             |              6     |   nan      |     nan      |               1      |              1      |                             0 |
| real_L8          | screen_stratified_ebh |              5     |   nan      |     nan      |               0.8333 |              0.8333 |                            -1 |
| real_L12         | e_bh_pcal             |              7     |   nan      |     nan      |               1      |              1      |                             0 |
| real_L12         | screen_stratified_ebh |              9     |   nan      |     nan      |               0.7778 |              1      |                             2 |
| real_L16         | e_bh_pcal             |             23     |   nan      |     nan      |               1      |              1      |                             0 |
| real_L16         | screen_stratified_ebh |             23     |   nan      |     nan      |               0.9167 |              0.9565 |                             0 |
| real_L20         | e_bh_pcal             |             17     |   nan      |     nan      |               1      |              1      |                             0 |
| real_L20         | screen_stratified_ebh |             17     |   nan      |     nan      |               1      |              1      |                             0 |

### table_23_second_round_cluster_permutation

| layer   | p_value_method                 | selection_method   |   clusters |   discoveries |   jaccard_to_prompt_paired_t_ebh |   recall_of_prompt_paired_t_ebh |
|:--------|:-------------------------------|:-------------------|-----------:|--------------:|---------------------------------:|--------------------------------:|
| L12     | cluster_mean_t                 | bh                 |        152 |            30 |                           0.2333 |                          1      |
| L12     | cluster_mean_t                 | by_bh              |        152 |            15 |                           0.4667 |                          1      |
| L12     | cluster_mean_t                 | e_bh_pcal          |        152 |             6 |                           0.8571 |                          0.8571 |
| L12     | cluster_signflip_normal        | bh                 |        152 |            30 |                           0.2333 |                          1      |
| L12     | cluster_signflip_normal        | by_bh              |        152 |            12 |                           0.5833 |                          1      |
| L12     | cluster_signflip_normal        | e_bh_pcal          |        152 |             6 |                           0.8571 |                          0.8571 |
| L12     | cluster_signflip_randomization | bh                 |        152 |            27 |                           0.2593 |                          1      |
| L12     | cluster_signflip_randomization | by_bh              |        152 |             0 |                           0      |                          0      |
| L12     | cluster_signflip_randomization | e_bh_pcal          |        152 |             0 |                           0      |                          0      |
| L12     | paired_t_prompt_level          | bh                 |        152 |            29 |                           0.2414 |                          1      |
| L12     | paired_t_prompt_level          | by_bh              |        152 |            18 |                           0.3889 |                          1      |
| L12     | paired_t_prompt_level          | e_bh_pcal          |        152 |             7 |                           1      |                          1      |
| L16     | cluster_mean_t                 | bh                 |        152 |            56 |                           0.4107 |                          1      |
| L16     | cluster_mean_t                 | by_bh              |        152 |            36 |                           0.6389 |                          1      |
| L16     | cluster_mean_t                 | e_bh_pcal          |        152 |            25 |                           0.92   |                          1      |
| L16     | cluster_signflip_normal        | bh                 |        152 |            56 |                           0.4107 |                          1      |
| L16     | cluster_signflip_normal        | by_bh              |        152 |            36 |                           0.6389 |                          1      |
| L16     | cluster_signflip_normal        | e_bh_pcal          |        152 |            24 |                           0.9583 |                          1      |
| L16     | cluster_signflip_randomization | bh                 |        152 |            60 |                           0.3833 |                          1      |
| L16     | cluster_signflip_randomization | by_bh              |        152 |            33 |                           0.697  |                          1      |
| L16     | cluster_signflip_randomization | e_bh_pcal          |        152 |             0 |                           0      |                          0      |
| L16     | paired_t_prompt_level          | bh                 |        152 |            51 |                           0.451  |                          1      |
| L16     | paired_t_prompt_level          | by_bh              |        152 |            37 |                           0.6216 |                          1      |
| L16     | paired_t_prompt_level          | e_bh_pcal          |        152 |            23 |                           1      |                          1      |
| L20     | cluster_mean_t                 | bh                 |        152 |            39 |                           0.4359 |                          1      |
| L20     | cluster_mean_t                 | by_bh              |        152 |            24 |                           0.7083 |                          1      |
| L20     | cluster_mean_t                 | e_bh_pcal          |        152 |            15 |                           0.7778 |                          0.8235 |
| L20     | cluster_signflip_normal        | bh                 |        152 |            39 |                           0.4359 |                          1      |
| L20     | cluster_signflip_normal        | by_bh              |        152 |            23 |                           0.7391 |                          1      |
| L20     | cluster_signflip_normal        | e_bh_pcal          |        152 |            14 |                           0.8235 |                          0.8235 |
| L20     | cluster_signflip_randomization | bh                 |        152 |            44 |                           0.3864 |                          1      |
| L20     | cluster_signflip_randomization | by_bh              |        152 |            21 |                           0.8095 |                          1      |
| L20     | cluster_signflip_randomization | e_bh_pcal          |        152 |             0 |                           0      |                          0      |
| L20     | paired_t_prompt_level          | bh                 |        152 |            47 |                           0.3617 |                          1      |
| L20     | paired_t_prompt_level          | by_bh              |        152 |            29 |                           0.5862 |                          1      |
| L20     | paired_t_prompt_level          | e_bh_pcal          |        152 |            17 |                           1      |                          1      |
| L8      | cluster_mean_t                 | bh                 |        152 |            19 |                           0.3158 |                          1      |
| L8      | cluster_mean_t                 | by_bh              |        152 |             9 |                           0.6667 |                          1      |
| L8      | cluster_mean_t                 | e_bh_pcal          |        152 |             3 |                           0.5    |                          0.5    |
| L8      | cluster_signflip_normal        | bh                 |        152 |            19 |                           0.3158 |                          1      |
| L8      | cluster_signflip_normal        | by_bh              |        152 |             9 |                           0.6667 |                          1      |
| L8      | cluster_signflip_normal        | e_bh_pcal          |        152 |             3 |                           0.5    |                          0.5    |
| L8      | cluster_signflip_randomization | bh                 |        152 |            19 |                           0.3158 |                          1      |
| L8      | cluster_signflip_randomization | by_bh              |        152 |             0 |                           0      |                          0      |
| L8      | cluster_signflip_randomization | e_bh_pcal          |        152 |             0 |                           0      |                          0      |
| L8      | paired_t_prompt_level          | bh                 |        152 |            15 |                           0.4    |                          1      |
| L8      | paired_t_prompt_level          | by_bh              |        152 |             9 |                           0.6667 |                          1      |
| L8      | paired_t_prompt_level          | e_bh_pcal          |        152 |             6 |                           1      |                          1      |

## Figures

- `figure_1_gate_b_metrics.png`: Gate B FDP, power, and CI coverage summary. Source: `results/synthetic_gate_b/gate_b_metrics.png`.
- `figure_2_q_grid_fdp_power.png`: FDP and power across nominal q values. Source: `results/synthetic_gate_b/q_grid_fdp_power.png`.
- `figure_3_synthetic_frontier_fdp_power.png`: Robustness frontier across dependence, effect, screen, and nuisance scenarios. Source: `results/synthetic_frontier/frontier_fdp_power.png`.
- `figure_4_ci_frontier_fdp_power.png`: CI and sample-size frontier. Source: `results/synthetic_ci_frontier/frontier_fdp_power.png`.
- `figure_5_downstream_debias.png`: Worst-group accuracy versus erroneous-removal rate. Source: `results/synthetic_debias/debias_worst_group_vs_error.png`.
- `figure_6_reviewer_empirical_gaps.png`: Summary of the six reviewer-requested empirical gap analyses. Source: `results/reviewer_empirical_gaps/reviewer_gap_summary.png`.
- `figure_7_second_round_real_ci_type_s.png`: Real per-feature CI width distribution and Type S sign-instability diagnostic. Source: `results/second_round_reviewer/real_ci_type_s_summary.png`.
- `figure_8_second_round_summary.png`: Summary of second-round reviewer empirical analyses. Source: `results/second_round_reviewer/second_round_summary.png`.

## Inventory

Tracked files: 911

See `artifact_inventory.csv` for file sizes and SHA-256 prefixes.
