# Synthetic SHIFT-style Debiasing Report

This experiment evaluates FDR-controlled removal of task-irrelevant
gender-spurious features in a controlled downstream classification task.

## Aggregate metrics

| method               |   removed_mean |   spurious_recall_mean |   erroneous_removal_rate_mean |   overall_acc_mean |   worst_group_acc_mean |   conflict_acc_mean |   gap_aligned_conflict_mean |
|:---------------------|---------------:|-----------------------:|------------------------------:|-------------------:|-----------------------:|--------------------:|----------------------------:|
| none                 |          0     |              0         |                    0          |           0.817719 |               0.619863 |            0.634923 |                  0.365077   |
| oracle_spurious      |         24     |              1         |                    0          |           0.999984 |               0.999937 |            0.999969 |                  3.1407e-05 |
| e_bh_pcal            |         24     |              1         |                    0          |           0.999984 |               0.999937 |            0.999969 |                  3.1407e-05 |
| by_bh                |         24.025 |              1         |                    0.001      |           0.999984 |               0.999937 |            0.999969 |                  3.1407e-05 |
| bh                   |         24.2   |              1         |                    0.00792308 |           0.999984 |               0.999937 |            0.999969 |                  3.1407e-05 |
| p_lt_q               |         26.65  |              1         |                    0.0965841  |           0.999984 |               0.999937 |            0.999969 |                  3.1407e-05 |
| top_score_k_spurious |         24     |              0.217708  |                    0.782292   |           0.920078 |               0.827242 |            0.840035 |                  0.159965   |
| random_k_spurious    |         24     |              0.0885417 |                    0.911458   |           0.80975  |               0.605511 |            0.619228 |                  0.380772   |

## Configuration

```json
{
  "replicates": 40,
  "output_dir": "results/synthetic_debias",
  "config": {
    "n_train": 1600,
    "n_test": 1600,
    "n_features": 256,
    "n_task": 24,
    "n_spurious": 24,
    "n_proxy": 24,
    "n_blocks": 32,
    "within_block_corr": 0.25,
    "task_signal": 1.0,
    "spurious_signal": 1.0,
    "proxy_signal": 1.1,
    "task_weight": 0.9,
    "spurious_weight": 0.8,
    "train_alignment_prob": 0.9,
    "test_alignment_prob": 0.5,
    "screen_fraction": 0.4,
    "test_fraction": 0.4,
    "q": 0.1,
    "e_gamma": 0.5,
    "seed": 20260620
  }
}
```
