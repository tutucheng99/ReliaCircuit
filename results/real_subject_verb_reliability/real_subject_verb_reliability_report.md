# Real Subject-Verb Reliability Extensions

These analyses use only existing real Gemma/Gemma Scope caches. No new GPU
runs are required for the null-decoy, stability, or q-grid analyses.

The screen-score decoy stress test constructs known-null candidate features
by random sign flips of real test-split feature effects, while assigning the
decoys high screen scores. Decoys are therefore null by construction on the
test estimand but attractive to screen-only top-score selection.

## Headline Null-Decoy Result

| layer   | method                      | selection_rule        |   discoveries_mean |   discoveries_std |   known_null_decoys_selected_mean |   known_null_decoys_selected_std |   known_null_fdp_mean |   known_null_fdp_std |
|:--------|:----------------------------|:----------------------|-------------------:|------------------:|----------------------------------:|---------------------------------:|----------------------:|---------------------:|
| L8      | top_score_fixed_k_256       | screen_score_manual_k |            256     |           0       |                           256     |                          0       |              1        |            0         |
| L8      | top_score_matched_e_bh_pcal | screen_score_manual_k |              3     |           0       |                             3     |                          0       |              1        |            0         |
| L8      | e_bh_pcal                   | test_split_fdr        |              3     |           0       |                             0     |                          0       |              0        |            0         |
| L8      | p_lt_q                      | test_split_fdr        |             77.305 |           4.6917  |                            25.305 |                          4.6917  |              0.32486  |            0.0411891 |
| L12     | top_score_fixed_k_256       | screen_score_manual_k |            256     |           0       |                           256     |                          0       |              1        |            0         |
| L12     | top_score_matched_e_bh_pcal | screen_score_manual_k |              6     |           0       |                             6     |                          0       |              1        |            0         |
| L12     | e_bh_pcal                   | test_split_fdr        |              6     |           0       |                             0     |                          0       |              0        |            0         |
| L12     | p_lt_q                      | test_split_fdr        |             79.805 |           5.08984 |                            25.805 |                          5.08984 |              0.320579 |            0.0438427 |
| L16     | top_score_fixed_k_256       | screen_score_manual_k |            256     |           0       |                           256     |                          0       |              1        |            0         |
| L16     | top_score_matched_e_bh_pcal | screen_score_manual_k |             23     |           0       |                            23     |                          0       |              1        |            0         |
| L16     | e_bh_pcal                   | test_split_fdr        |             23     |           0       |                             0     |                          0       |              0        |            0         |
| L16     | p_lt_q                      | test_split_fdr        |            115.135 |           4.48524 |                            25.135 |                          4.48524 |              0.217131 |            0.0304367 |
| L20     | top_score_fixed_k_256       | screen_score_manual_k |            256     |           0       |                           256     |                          0       |              1        |            0         |
| L20     | top_score_matched_e_bh_pcal | screen_score_manual_k |             15     |           0       |                            15     |                          0       |              1        |            0         |
| L20     | e_bh_pcal                   | test_split_fdr        |             15     |           0       |                             0     |                          0       |              0        |            0         |
| L20     | p_lt_q                      | test_split_fdr        |             97.575 |           4.51623 |                            25.575 |                          4.51623 |              0.260537 |            0.0341206 |

## Prompt-Resampling Stability

| layer   | estimand                   | method          |   discoveries_mean |   discoveries_std |   jaccard_mean |   jaccard_std |   recall_full_mean |   recall_full_std |   full_discoveries |
|:--------|:---------------------------|:----------------|-------------------:|------------------:|---------------:|--------------:|-------------------:|------------------:|-------------------:|
| L8      | mean_effect                | bh              |             43.615 |         40.0759   |       0.421538 |     0.192845  |           0.862333 |         0.100268  |                 15 |
| L8      | mean_effect                | e_bh_pcal       |              5.405 |          1.43572  |       0.672182 |     0.156743  |           0.750833 |         0.129421  |                  6 |
| L8      | mean_effect                | p_lt_q          |             83.7   |         38.7812   |       0.456414 |     0.120314  |           0.775385 |         0.143571  |                 52 |
| L8      | prompt_tracking_covariance | track_e_bh_pcal |              1.015 |          0.121857 |       0.9925   |     0.0609287 |           1        |         0         |                  1 |
| L12     | mean_effect                | bh              |             47.06  |         25.6297   |       0.531777 |     0.148431  |           0.838621 |         0.085433  |                 29 |
| L12     | mean_effect                | e_bh_pcal       |              8.44  |          2.92733  |       0.660302 |     0.157676  |           0.859286 |         0.170948  |                  7 |
| L12     | mean_effect                | p_lt_q          |             82.54  |         26.6164   |       0.517126 |     0.12832   |           0.822037 |         0.0652894 |                 54 |
| L12     | prompt_tracking_covariance | track_e_bh_pcal |              1.07  |          0.368482 |       0.974167 |     0.121465  |           1        |         0         |                  1 |
| L16     | mean_effect                | bh              |             74.14  |         18.8173   |       0.591949 |     0.114727  |           0.887647 |         0.0451988 |                 51 |
| L16     | mean_effect                | e_bh_pcal       |             27.215 |          3.35036  |       0.807722 |     0.085198  |           0.969348 |         0.0328492 |                 23 |
| L16     | mean_effect                | p_lt_q          |            104.105 |         16.8088   |       0.610747 |     0.108241  |           0.806333 |         0.0743941 |                 90 |
| L16     | prompt_tracking_covariance | track_e_bh_pcal |              1.165 |          0.700162 |       0.85625  |     0.299233  |           0.94     |         0.238083  |                  1 |
| L20     | mean_effect                | bh              |             64.94  |         32.5874   |       0.60059  |     0.146195  |           0.839362 |         0.0674766 |                 47 |
| L20     | mean_effect                | e_bh_pcal       |             20.25  |          7.91522  |       0.74468  |     0.116463  |           0.913235 |         0.0634968 |                 17 |
| L20     | mean_effect                | p_lt_q          |             95.575 |         33.0615   |       0.585558 |     0.144428  |           0.821319 |         0.0653034 |                 72 |
| L20     | prompt_tracking_covariance | track_e_bh_pcal |              0.195 |          0.397195 |       0.805    |     0.397195  |           0.805    |         0.397195  |                  0 |

## Layer Scan

| layer   | method                |   discoveries |   completeness_r2 |   centered_r2 |   selected_full_corr |   abs_effect_fraction |   sign_agreement |
|:--------|:----------------------|--------------:|------------------:|--------------:|---------------------:|----------------------:|-----------------:|
| L8      | e_bh_pcal             |             6 |          0.968474 |      0.643614 |           0.816815   |              0.975706 |          1       |
| L8      | top_score_k_256       |           nan |          0.963671 |      0.589315 |           0.799335   |              0.960985 |          1       |
| L8      | top_score_k_e_bh_pcal |           nan |          0.963372 |      0.585936 |           0.792131   |              0.949334 |          1       |
| L8      | track_e_bh_pcal       |             1 |          0.950063 |      0.435492 |           0.739686   |              0.906093 |          1       |
| L12     | e_bh_pcal             |             7 |          0.928115 |      0.187378 |           0.725867   |              0.826864 |          1       |
| L12     | top_score_k_256       |           nan |          0.944764 |      0.375587 |           0.753603   |              0.869361 |          1       |
| L12     | top_score_k_e_bh_pcal |           nan |          0.94652  |      0.395435 |           0.766367   |              0.872505 |          1       |
| L12     | track_e_bh_pcal       |             1 |          0.956483 |      0.50806  |           0.761473   |              0.923485 |          1       |
| L16     | e_bh_pcal             |            23 |          0.963221 |      0.58423  |           0.780224   |              0.958715 |          1       |
| L16     | top_score_k_256       |           nan |          0.964158 |      0.594825 |           0.791069   |              1.00464  |          1       |
| L16     | top_score_k_e_bh_pcal |           nan |          0.964459 |      0.598225 |           0.807632   |              0.93242  |          1       |
| L16     | track_e_bh_pcal       |             1 |          0.571944 |     -3.83893  |           0.549454   |              0.366182 |          1       |
| L20     | e_bh_pcal             |            17 |          0.521452 |     -4.40972  |           0.149339   |              0.350849 |          0.99375 |
| L20     | top_score_k_256       |           nan |          0.594259 |     -3.58668  |           0.405365   |              0.401172 |          1       |
| L20     | top_score_k_e_bh_pcal |           nan |          0.436537 |     -5.36964  |           0.00798189 |              0.294398 |          0.98125 |
| L20     | track_e_bh_pcal       |             0 |          0        |    -10.3044   |         nan          |              0        |          0       |

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

Reporting guardrails: single-feature tracking results are labeled as such;
top-score circuit metrics are reported as baselines, not as FDR-controlled
discoveries; completeness is always paired with centered R2 and correlation.
